"""
Resume Import Process Lambda Handler

Processes uploaded files and maps them to ResumeJSON using AI.

Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7
"""
import json
import os
import sys
import re
import boto3
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, not_found, internal_error, error_response

# AWS clients
s3_client = boto3.client('s3', region_name='us-west-2')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

# Bucket name from environment
IMPORTS_BUCKET = os.environ.get('IMPORTS_BUCKET', 'skillsnap-imports-temp')

# Valid MIME types mapped to file extensions (Requirement 9.1)
VALID_MIME_TYPES = {
    'application/json': ['.json'],
    'application/x-yaml': ['.yaml', '.yml'],
    'text/yaml': ['.yaml', '.yml'],
    'text/x-yaml': ['.yaml', '.yml'],
    'application/pdf': ['.pdf'],
    'binary/octet-stream': ['.pdf', '.yaml', '.yml', '.json'],  # Fallback for S3
    'application/octet-stream': ['.pdf', '.yaml', '.yml', '.json'],  # Fallback for S3
}


def validate_mime_type(content_type: str, file_extension: str) -> tuple[bool, str]:
    """
    Validate that the MIME type matches the file extension.
    
    Requirements: 9.1 - MIME type validation
    Returns (is_valid, error_message)
    """
    if not content_type:
        # If no content type, rely on file extension
        return True, ""
    
    # Normalize content type (remove charset and other parameters)
    content_type = content_type.split(';')[0].strip().lower()
    file_extension = file_extension.lower()
    
    # Check if content type is known
    if content_type not in VALID_MIME_TYPES:
        # Unknown content type - log warning but allow based on extension
        print(f"Warning: Unknown content type '{content_type}' for file extension '{file_extension}'")
        return True, ""
    
    # Check if extension matches content type
    allowed_extensions = VALID_MIME_TYPES[content_type]
    if file_extension not in allowed_extensions:
        return False, f"File type does not match extension. Content type '{content_type}' is not valid for '{file_extension}' files"
    
    return True, ""

# ResumeJSON schema for AI prompt
RESUME_JSON_SCHEMA = """
{
  "contact": {
    "name": "string (required)",
    "location": "string (optional)",
    "items": [
      {
        "icon": "string (icon name without .svg, e.g., 'email-at', 'linkedin', 'github')",
        "title": "string (display text)",
        "url": "string (optional link URL)"
      }
    ]
  },
  "summary": "string (professional summary)",
  "skills": ["string array of skills"],
  "highlights": ["string array - leave empty, AI generates these"],
  "experience": [
    {
      "name": "string (company name)",
      "url": "string (company URL, optional)",
      "employees": "number (optional)",
      "location": "string (optional)",
      "description": "string (company description, optional)",
      "startDate": "string (e.g., 'January 2020')",
      "endDate": "string (e.g., 'December 2022', or empty if current)",
      "current": "boolean (true if currently employed)",
      "roles": [
        {
          "title": "string (job title)",
          "startDate": "string",
          "endDate": "string",
          "current": "boolean",
          "location": "string (optional)",
          "bullets": [
            {
              "text": "string (achievement/responsibility)",
              "tags": ["string array of tags, optional"]
            }
          ]
        }
      ]
    }
  ],
  "education": [
    {
      "degree": "string (degree or certification name)",
      "institution": "string (school name)",
      "graduationDate": "string (year or date)",
      "field": "string (optional)",
      "gpa": "string (optional)"
    }
  ],
  "awards": [
    {
      "title": "string (award name)",
      "description": "string (optional)",
      "date": "string"
    }
  ],
  "keynotes": [
    {
      "title": "string (presentation title)",
      "event": "string (event name)",
      "date": "string",
      "location": "string (optional)"
    }
  ]
}
"""


def sanitize_text(text: str) -> str:
    """
    Sanitize extracted text before sending to AI.
    Removes potential script tags, injection patterns, and malicious content.
    
    Requirements: 9.5 - Input sanitization
    """
    if not text:
        return ""
    
    # Remove script tags and their content
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove style tags and their content
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove HTML comments (can contain malicious content)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    
    # Remove HTML tags but preserve content
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove potential SQL injection patterns
    text = re.sub(r'(--|;|\'|\")\s*(DROP|DELETE|INSERT|UPDATE|SELECT|UNION|ALTER|CREATE|TRUNCATE)', '', text, flags=re.IGNORECASE)
    
    # Remove potential prompt injection patterns - comprehensive list
    prompt_injection_patterns = [
        r'(ignore|forget|disregard)\s+(previous|above|all|prior|earlier)\s+(instructions?|prompts?|context|rules?)',
        r'(new|override|replace)\s+(instructions?|prompts?|rules?)',
        r'(you\s+are\s+now|act\s+as|pretend\s+to\s+be|roleplay\s+as)',
        r'(system\s*:?\s*prompt|assistant\s*:?\s*prompt)',
        r'(jailbreak|bypass|escape)\s+(mode|filter|restriction)',
        r'\[\s*(SYSTEM|INST|ASSISTANT)\s*\]',
    ]
    for pattern in prompt_injection_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove null bytes and other control characters (except newlines and tabs)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    # Remove excessive blank lines while preserving structure
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    # Note: Do NOT modify leading whitespace as it breaks YAML/Python indentation
    # Only collapse excessive inline spaces (spaces preceded by a non-space, non-newline character)
    # This preserves indentation at the start of lines
    text = re.sub(r'(?<=[^\s\n]) {4,}', '   ', text)
    
    return text.strip()


def parse_date_range(date_str: str) -> tuple[str, str, bool]:
    """
    Parse date range string into startDate, endDate, current.
    Examples: "January 2020 - Present", "2015 - 2020", "2018"
    """
    if not date_str:
        return "", "", False
    
    date_str = str(date_str).strip()
    
    # Check for "Present" or "Current"
    is_current = bool(re.search(r'\b(present|current|now)\b', date_str, re.IGNORECASE))
    
    # Split by common separators
    parts = re.split(r'\s*[-–—]\s*', date_str)
    
    start_date = parts[0].strip() if parts else ""
    end_date = ""
    
    if len(parts) > 1:
        end_part = parts[1].strip()
        if not re.search(r'\b(present|current|now)\b', end_part, re.IGNORECASE):
            end_date = end_part
    
    return start_date, end_date, is_current


def map_icon_name(icon: str) -> str:
    """Map input icon names to internal icon names."""
    if not icon:
        return "globe-solid"
    
    # Remove .svg extension if present
    icon = re.sub(r'\.svg$', '', icon, flags=re.IGNORECASE)
    
    # Map common variations
    icon_map = {
        'at-solid': 'email-at',
        'email': 'email-at',
        'mail': 'email-at',
        'phone-volume-solid': 'phone-volume',
        'phone-solid': 'phone',
        'linkedin-brands-solid': 'linkedin',
        'linkedin-brands': 'linkedin',
        'github-brands': 'github',
        'github-brands-solid': 'github',
        'telegram-brands': 'telegram',
        'house-solid': 'house-solid',
        'home': 'house-solid',
        'location': 'house-solid',
        'globe': 'globe-solid',
        'website': 'globe-solid',
        'web': 'globe-solid',
        'twitter': 'x-twitter',
        'x': 'x-twitter',
    }
    
    return icon_map.get(icon.lower(), icon)


def get_default_resume_json() -> dict:
    """Return default empty ResumeJSON structure."""
    return {
        "contact": {
            "name": "",
            "location": "",
            "items": []
        },
        "summary": "",
        "skills": [],
        "highlights": [],
        "experience": [],
        "education": [],
        "awards": [],
        "keynotes": []
    }


def map_yaml_to_resume_json(data: dict) -> dict:
    """
    Map YAML/JSON input format to internal ResumeJSON format.
    This handles the direct mapping without AI for structured files.
    """
    result = get_default_resume_json()
    
    # Map contact info
    result["contact"]["name"] = data.get("name", "")
    result["contact"]["location"] = data.get("location", "")
    
    # Map contacts array to items
    contacts = data.get("contacts", [])
    for contact in contacts:
        item = {
            "icon": map_icon_name(contact.get("icon", "")),
            "title": contact.get("label", ""),
            "url": contact.get("url", "")
        }
        result["contact"]["items"].append(item)
    
    # Map summary
    result["summary"] = data.get("summary", "")
    
    # Map skills
    result["skills"] = data.get("skills", [])
    
    # Highlights are always empty - AI generates them
    result["highlights"] = []
    
    # Map experience
    for exp in data.get("experience", []):
        start_date, end_date, is_current = parse_date_range(exp.get("dates", ""))
        
        # Handle company_urls - can be string or array
        company_url = exp.get("company_urls", "")
        if isinstance(company_url, list):
            company_url = company_url[0] if company_url else ""
        
        experience_item = {
            "name": exp.get("company_name", ""),
            "url": company_url,
            "employees": exp.get("employees"),
            "location": exp.get("location", ""),
            "description": exp.get("company_description", ""),
            "startDate": start_date,
            "endDate": end_date,
            "current": is_current,
            "roles": []
        }
        
        # Map roles
        for role in exp.get("roles", []):
            role_start, role_end, role_current = parse_date_range(role.get("dates", ""))
            
            # Handle bullets - can be list of dicts or list of strings
            bullets = []
            for bullet in role.get("bullets", []):
                if isinstance(bullet, dict):
                    bullets.append({
                        "text": bullet.get("text", ""),
                        "tags": bullet.get("tags", [])
                    })
                elif isinstance(bullet, str):
                    bullets.append({"text": bullet, "tags": []})
            
            role_item = {
                "title": role.get("role", ""),
                "startDate": role_start,
                "endDate": role_end,
                "current": role_current,
                "location": role.get("location", ""),
                "bullets": bullets
            }
            experience_item["roles"].append(role_item)
        
        result["experience"].append(experience_item)
    
    # Map education
    for edu in data.get("education", []):
        education_item = {
            "degree": edu.get("course", ""),
            "institution": edu.get("school", ""),
            "graduationDate": str(edu.get("dates", "")),
            "field": edu.get("field", ""),
            "gpa": edu.get("gpa", "")
        }
        result["education"].append(education_item)
    
    # Map awards
    for award in data.get("awards", []):
        award_item = {
            "title": award.get("award", ""),
            "description": award.get("reward", ""),
            "date": str(award.get("dates", ""))
        }
        result["awards"].append(award_item)
    
    # Map keynotes
    for keynote in data.get("keynotes", []):
        keynote_item = {
            "title": keynote.get("keynote", ""),
            "event": keynote.get("event", ""),
            "date": str(keynote.get("dates", "")),
            "location": keynote.get("location", "")
        }
        result["keynotes"].append(keynote_item)
    
    return result


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text content from PDF bytes.
    Uses PyPDF2 for text extraction.
    """
    try:
        import io
        from PyPDF2 import PdfReader
        
        pdf_file = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_file)
        
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        
        return "\n\n".join(text_parts)
    except ImportError:
        raise Exception("PyPDF2 not available for PDF processing")
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def process_with_ai(content: str, source_type: str) -> dict:
    """
    Use Nova Micro to map unstructured content to ResumeJSON.
    
    Requirements: 5.4, 5.5
    """
    prompt = f"""You are a resume data extraction assistant. Extract information from the following resume content and map it to the specified JSON schema.

RESUME CONTENT:
{content}

TARGET SCHEMA (ResumeJSON):
{RESUME_JSON_SCHEMA}

FIELD MAPPING RULES:
1. Map the person's name to contact.name
2. Map location to contact.location
3. For contact items, use appropriate icons: email-at, phone, phone-volume, linkedin, github, globe-solid, house-solid, x-twitter, etc.
4. Parse date ranges like "January 2020 - Present" into startDate/endDate/current fields
5. For experience, group roles under companies
6. For role bullets, extract each achievement/responsibility as a separate bullet object with:
   - "text": the actual bullet point content (NOT the word "text")
   - "tags": an array of relevant skill/technology tags (can be empty array if no tags, NOT the word "tags")
   Example: {"text": "Led team of 5 engineers", "tags": ["leadership", "management"]}
7. Map education course/school/dates to degree/institution/graduationDate
8. Map awards to title/description/date
9. Map keynotes/speaking to title/event/date
10. Leave highlights as an empty array - they are AI-generated separately
11. If a field cannot be determined, use an empty string or empty array
12. IMPORTANT: Do NOT use field names as values - extract the actual content from the resume

Return ONLY valid JSON matching the ResumeJSON schema, no additional text or markdown formatting.

OUTPUT:"""

    try:
        response = bedrock_runtime.invoke_model(
            modelId='amazon.nova-micro-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                'inputText': prompt,
                'textGenerationConfig': {
                    'maxTokenCount': 4096,
                    'temperature': 0.3,
                    'topP': 0.9,
                }
            })
        )
        
        result = json.loads(response['body'].read())
        output_text = result.get('results', [{}])[0].get('outputText', '')
        
        # Try to parse the JSON from the response
        # Remove any markdown code blocks if present
        output_text = re.sub(r'^```json\s*', '', output_text.strip())
        output_text = re.sub(r'\s*```$', '', output_text)
        
        return json.loads(output_text)
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse AI response as JSON: {e}")
        raise Exception("AI failed to produce valid JSON")
    except Exception as e:
        print(f"Bedrock error: {e}")
        raise


def apply_defaults(resume_json: dict) -> dict:
    """
    Apply defaults for any missing fields in the ResumeJSON.
    
    Requirements: 5.7
    """
    defaults = get_default_resume_json()
    
    # Ensure all top-level keys exist
    for key in defaults:
        if key not in resume_json:
            resume_json[key] = defaults[key]
    
    # Ensure contact has required structure
    if not isinstance(resume_json.get("contact"), dict):
        resume_json["contact"] = defaults["contact"]
    else:
        contact = resume_json["contact"]
        if "name" not in contact:
            contact["name"] = ""
        if "location" not in contact:
            contact["location"] = ""
        if "items" not in contact or not isinstance(contact["items"], list):
            contact["items"] = []
    
    # Ensure arrays are arrays
    for key in ["skills", "highlights", "experience", "education", "awards", "keynotes"]:
        if not isinstance(resume_json.get(key), list):
            resume_json[key] = []
    
    # Ensure summary is string
    if not isinstance(resume_json.get("summary"), str):
        resume_json["summary"] = str(resume_json.get("summary", ""))
    
    # Highlights should always be empty (AI generates them during resume generation)
    resume_json["highlights"] = []
    
    return resume_json


def handler(event, context):
    """
    Process uploaded file and return mapped ResumeJSON.
    
    Request body:
    {
        "s3Key": "string"
    }
    
    Response:
    {
        "resumejson": { ... },
        "warnings": ["string"],
        "source": "yaml" | "json" | "pdf"
    }
    
    Error Handling (Requirements 8.1-8.5):
    - Network/S3 errors: "File not found or expired. Please try uploading again."
    - Auth errors: Handled by API Gateway (401)
    - Timeout: "Processing took too long. Please try a smaller file or simpler format."
    - Corrupted file: "Could not read file. Please ensure it's a valid YAML, JSON, or PDF file."
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            print("Error: User ID not found in token claims")
            return bad_request("User ID not found in token")
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        s3_key = body.get('s3Key')
        
        if not s3_key:
            print("Error: s3Key not provided in request body")
            return bad_request("s3Key is required")
        
        # Verify the s3_key belongs to this user
        expected_prefix = f"temp-imports/{userid}/"
        if not s3_key.startswith(expected_prefix):
            print(f"Error: Access denied - s3Key '{s3_key}' does not match user '{userid}'")
            return bad_request("Invalid s3Key - access denied")
        
        # Determine file type from key
        file_ext = os.path.splitext(s3_key)[1].lower()
        
        # Retrieve file from S3
        try:
            response = s3_client.get_object(Bucket=IMPORTS_BUCKET, Key=s3_key)
            file_content = response['Body'].read()
            content_type = response.get('ContentType', '')
            
            # MIME type validation (Requirement 9.1)
            is_valid, mime_error = validate_mime_type(content_type, file_ext)
            if not is_valid:
                print(f"Error: MIME type validation failed - {mime_error}")
                return bad_request(mime_error)
                
        except s3_client.exceptions.NoSuchKey:
            print(f"Error: File not found in S3 - key: {s3_key}")
            return not_found("File not found or expired. Please try uploading again.")
        except Exception as e:
            print(f"S3 error retrieving file: {e}")
            return not_found("File not found or expired. Please try uploading again.")
        
        warnings = []
        source_type = "unknown"
        
        try:
            if file_ext in ['.yaml', '.yml']:
                # Parse YAML directly
                source_type = "yaml"
                try:
                    text_content = file_content.decode('utf-8')
                except UnicodeDecodeError as e:
                    print(f"Error: YAML file encoding error - {e}")
                    return bad_request("Could not read file. Please ensure it's a valid YAML file with UTF-8 encoding.")
                
                # Parse YAML directly without sanitizing (YAML is structured data, not unstructured text)
                data = yaml.safe_load(text_content)
                
                if data is None:
                    print("Error: YAML file is empty")
                    return bad_request("Could not read file. The YAML file appears to be empty.")
                
                if not isinstance(data, dict):
                    print(f"Error: YAML structure is not a dict, got {type(data)}")
                    return bad_request("Could not read file. Please ensure it's a valid YAML file with the expected resume structure.")
                
                # Direct mapping for structured YAML
                try:
                    resume_json = map_yaml_to_resume_json(data)
                except Exception as map_error:
                    print(f"Error mapping YAML structure: {map_error}")
                    import traceback
                    traceback.print_exc()
                    return bad_request(f"YAML file structure doesn't match expected format. Please check the template at /skillsnap-resume-template.yaml for the correct structure.")
                
            elif file_ext == '.json':
                # Parse JSON directly
                source_type = "json"
                try:
                    text_content = file_content.decode('utf-8')
                except UnicodeDecodeError as e:
                    print(f"Error: JSON file encoding error - {e}")
                    return bad_request("Could not read file. Please ensure it's a valid JSON file with UTF-8 encoding.")
                
                # Parse JSON directly without sanitizing (JSON is structured data, not unstructured text)
                data = json.loads(text_content)
                
                if not isinstance(data, dict):
                    print(f"Error: JSON structure is not a dict, got {type(data)}")
                    return bad_request("Could not read file. Please ensure it's a valid JSON file with the expected resume structure.")
                
                # Check if it's already in ResumeJSON format
                if "contact" in data and "experience" in data:
                    resume_json = data
                else:
                    # Try to map from input format
                    try:
                        resume_json = map_yaml_to_resume_json(data)
                    except Exception as map_error:
                        print(f"Error mapping JSON structure: {map_error}")
                        import traceback
                        traceback.print_exc()
                        return bad_request(f"JSON file structure doesn't match expected format. Please check the template for the correct structure.")
                
            elif file_ext == '.pdf':
                # Extract text from PDF and use AI
                source_type = "pdf"
                try:
                    text_content = extract_text_from_pdf(file_content)
                except Exception as e:
                    print(f"Error: PDF extraction failed - {e}")
                    return bad_request("Could not read file. Please ensure it's a valid PDF file that is not password-protected.")
                
                if not text_content.strip():
                    print("Error: PDF text extraction returned empty content")
                    return bad_request("Could not extract text from PDF. The file may be image-based or password-protected.")
                
                # Sanitize and process with AI (Requirement 9.5)
                sanitized_content = sanitize_text(text_content)
                
                try:
                    resume_json = process_with_ai(sanitized_content, source_type)
                except Exception as e:
                    error_msg = str(e).lower()
                    if 'timeout' in error_msg or 'timed out' in error_msg:
                        print(f"Error: AI processing timeout - {e}")
                        return error_response(504, "Timeout", "Processing took too long. Please try a smaller file or simpler format.")
                    print(f"Error: AI processing failed - {e}")
                    return internal_error("Failed to process resume file. Please try again.")
                    
                warnings.append("PDF content was processed by AI - please verify accuracy")
                
            else:
                print(f"Error: Unsupported file extension - {file_ext}")
                return bad_request(f"Unsupported file type. Please select a YAML, JSON, or PDF file.")
            
            # Apply defaults for any missing fields
            resume_json = apply_defaults(resume_json)
            
        except yaml.YAMLError as e:
            print(f"Error: YAML parsing failed - {e}")
            error_msg = str(e)
            line_info = ""
            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                line_info = f" (line {mark.line + 1}, column {mark.column + 1})"
            return bad_request(f"YAML syntax error{line_info}. Please verify your file at https://yamlchecker.com/ or check the template format.")
        except json.JSONDecodeError as e:
            print(f"Error: JSON parsing failed - {e}")
            line_info = f" at line {e.lineno}" if hasattr(e, 'lineno') else ""
            return bad_request(f"JSON syntax error{line_info}. Please verify your file with a JSON validator.")
        except Exception as e:
            print(f"Processing error: {e}")
            import traceback
            traceback.print_exc()
            return bad_request("Could not process file. Please ensure it matches the expected format (see template) or verify YAML syntax at https://yamlchecker.com/")
        
        # Delete temp file after processing
        try:
            s3_client.delete_object(Bucket=IMPORTS_BUCKET, Key=s3_key)
        except Exception as e:
            print(f"Warning: Failed to delete temp file {s3_key}: {e}")
            # Don't fail the request for cleanup errors
        
        return api_response(200, {
            'resumejson': resume_json,
            'warnings': warnings,
            'source': source_type
        })
        
    except json.JSONDecodeError:
        print("Error: Invalid JSON in request body")
        return bad_request("Invalid JSON in request body")
    except Exception as e:
        print(f"Unexpected error processing import: {e}")
        return internal_error("Failed to process resume file. Please try again.")
