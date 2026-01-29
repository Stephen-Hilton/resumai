"""
Resume Import URL Lambda Handler

Generates presigned S3 URLs for file uploads.

Requirements: 4.2, 4.4, 4.5
"""
import json
import os
import sys
import time
import boto3
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.response import api_response, bad_request, internal_error

# S3 client
s3_client = boto3.client('s3', region_name='us-west-2')

# Bucket name from environment
IMPORTS_BUCKET = os.environ.get('IMPORTS_BUCKET', 'skillsnap-imports-temp')

# Valid content types
VALID_CONTENT_TYPES = {
    'application/json': ['.json'],
    'application/x-yaml': ['.yaml', '.yml'],
    'text/yaml': ['.yaml', '.yml'],
    'application/pdf': ['.pdf'],
}

# Max file size (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_filename(filename: str) -> tuple[bool, str]:
    """Validate filename has allowed extension."""
    if not filename:
        return False, "filename is required"
    
    # Sanitize filename - remove path components
    filename = os.path.basename(filename)
    
    # Check for valid extension
    ext = os.path.splitext(filename)[1].lower()
    valid_extensions = ['.json', '.yaml', '.yml', '.pdf']
    
    if ext not in valid_extensions:
        return False, f"Unsupported file type. Allowed: {', '.join(valid_extensions)}"
    
    return True, filename


def validate_content_type(content_type: str, filename: str) -> tuple[bool, str]:
    """
    Validate content type matches file extension.
    
    Requirements: 9.1 - MIME type validation
    Returns 400 error for mismatched types.
    """
    if not content_type:
        return False, "contentType is required"
    
    ext = os.path.splitext(filename)[1].lower()
    
    # Check if content type is valid
    if content_type not in VALID_CONTENT_TYPES:
        return False, f"Unsupported content type: {content_type}. Allowed types: application/json, application/x-yaml, text/yaml, application/pdf"
    
    # Check if extension matches content type - MIME type validation (Requirement 9.1)
    allowed_extensions = VALID_CONTENT_TYPES[content_type]
    if ext not in allowed_extensions:
        return False, f"File type does not match extension. Content type '{content_type}' is not valid for '{ext}' files"
    
    return True, content_type


def handler(event, context):
    """
    Generate presigned URL for file upload.
    
    Request body:
    {
        "filename": "string",
        "contentType": "string"
    }
    
    Response:
    {
        "uploadUrl": "string",
        "s3Key": "string",
        "expiresIn": 60
    }
    """
    try:
        # Get user ID from Cognito authorizer
        claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
        userid = claims.get('custom:userid') or claims.get('sub')
        
        if not userid:
            return bad_request("User ID not found in token")
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        filename = body.get('filename')
        content_type = body.get('contentType')
        
        # Validate filename
        is_valid, result = validate_filename(filename)
        if not is_valid:
            return bad_request(result)
        filename = result
        
        # Validate content type
        is_valid, result = validate_content_type(content_type, filename)
        if not is_valid:
            return bad_request(result)
        
        # Generate unique S3 key
        timestamp = int(time.time() * 1000)
        s3_key = f"temp-imports/{userid}/{timestamp}-{filename}"
        
        # Generate presigned URL
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': IMPORTS_BUCKET,
                'Key': s3_key,
                'ContentType': content_type,
            },
            ExpiresIn=60,
        )
        
        return api_response(200, {
            'uploadUrl': presigned_url,
            's3Key': s3_key,
            'expiresIn': 60,
        })
        
    except json.JSONDecodeError:
        return bad_request("Invalid JSON in request body")
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return internal_error("Failed to generate upload URL")
