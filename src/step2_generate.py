import os, re, yaml, logging, sys, time
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Handle imports for different contexts (standalone vs web app)
try:
    from src.utils import logging_setup
    from src.utils.version import get_version
except ImportError:
    # When called from web app context, src is not in the module path
    try:
        from utils import logging_setup
        from utils.version import get_version
    except ImportError:
        # Last resort - add src to path and try again
        import sys
        from pathlib import Path
        src_path = str(Path(__file__).parent)
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        from utils import logging_setup
        from utils.version import get_version

# Get current version
VERSION = get_version()

# Import modular generation system
try:
    from utils.modular_generator import ModularResumeGenerator
    from utils.modular_config import get_config
    MODULAR_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Modular generation system not available: {e}")
    MODULAR_AVAILABLE = False

# Set up logger for this module
logger = logging_setup.get_logger(__name__)

def force_flush_logs():
    """Force flush all logging handlers and stdout to ensure immediate output"""
    return logging_setup.force_flush_logs()


def sanitize_filename(text):
    """
    Sanitize text for use in filenames and directory names.
    Consistent function used throughout the application.
    """
    if not text:
        return "Unknown"
    
    # Replace problematic characters with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', text)
    # Replace spaces and multiple underscores with single underscore
    sanitized = re.sub(r'[\s_]+', '_', sanitized)
    # Remove leading/trailing underscores and limit length
    return sanitized.strip('_')[:50]



def load_resume_file(resume_file: Path | str = 'stephen') -> dict:
    """
    Loads the named "resume" file from the `src/resumes` directory, and returns the parsed YAML data as a dictionary.
    If the file is not found, returns None.

    Args:
        resume_file: a Path or string indicating a file in the `src/resumes/` folder.  If only a name is provided, `src/resumes/` is assumed.

    Returns: 
        dict: dictionary containing loaded YAML data.

    """
    logger.info(f"Loading resume file: {resume_file}")
    
    # Convert to Path object and handle relative paths
    if isinstance(resume_file, str):
        if not resume_file.endswith('.yaml'):
            resume_file = f"{resume_file}.yaml"
        resume_path = Path(__file__).parent / 'resumes' / resume_file
    elif isinstance(resume_file, Path):
        resume_path = resume_file
    else: 
        logger.error(f"Invalid resume_file type: {type(resume_file)}")
        raise ValueError(f"Parameter 'resume_file' must be type str or Path, you provided: {type(resume_file)}")
        
    # Check if file exists
    if not resume_path.exists():
        logger.error(f"Resume file not found: {resume_path.resolve()}")
        raise ValueError(f"Parameter 'resume_file' did not resolve to a resume file: {resume_path.resolve()}")
        
    # Load and parse YAML
    try:
        with open(resume_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Replace tabs with spaces to fix YAML parsing issues
            content = content.replace('\t', '  ')
            resume_data = yaml.safe_load(content)
            
        logger.info(f"Successfully loaded resume for: {resume_data.get('name', 'Unknown')}")
        return resume_data
        
    except Exception as e:
        logger.error(f"Error loading resume file {resume_path}: {str(e)}", exc_info=True)
        return None 



def load_queued_jobs(force:bool = False, specific_job_id: str = None) -> list[dict]:
    """
    Loads all jobs from the `src/jobs/1_queued` directory, and returns them as a list of dictionaries.
    Now handles subfolder structure where each job is in its own subfolder.
    Excludes any that appear in any other `src/jobs/*` folder, unless force=True, in which case
    older generation work is simply overwritten.

    Args:
        force (bool, optional): Ignores previous run exclusion logic, and forces a new run.
        specific_job_id (str, optional): If provided, only loads the job with this specific ID.

    Returns:
        list[dict]: list of dictionaries, each representing a job.
    """
    logger.info(f"Loading queued jobs (force={force}, specific_job_id={specific_job_id})")
    
    jobs_dir = Path(__file__).parent / 'jobs'
    exclude_dirs = [d.name for d in jobs_dir.iterdir() if d.is_dir() and d.name != '1_queued']
    queued_dir = jobs_dir / '1_queued'
    
    if not queued_dir.exists(): 
        logger.error(f"Queued directory not found: {queued_dir.resolve()}")
        raise ValueError(f"Directory '1_queued' does not exist: {queued_dir.resolve()}")
    
    jobs = []
    processed_ids = set()
    
    # If not forcing, collect IDs from other directories to exclude
    if not force:
        logger.info("Checking for previously processed jobs")
        for exclude_dir in exclude_dirs:
            exclude_path = jobs_dir / exclude_dir
            if exclude_path.exists():
                # Check both flat files and subdirectories for job IDs
                for file_path in exclude_path.rglob('*.yaml'):
                    # Extract job ID from filename (format: timestamp.id.company.title.yaml)
                    filename_parts = file_path.stem.split('.')
                    if len(filename_parts) >= 2:
                        job_id = filename_parts[1]
                        processed_ids.add(job_id)
        logger.info(f"Found {len(processed_ids)} previously processed job IDs")
    
    # Load jobs from queued directory - now checking both flat files and subfolders
    jobs_found = 0
    
    # First check for any remaining flat files (backward compatibility)
    flat_files = list(queued_dir.glob('*.yaml'))
    if flat_files:
        logger.info(f"Found {len(flat_files)} flat queued job files (legacy format)")
        
        for yaml_file in flat_files:
            try:
                # Extract job ID from filename
                filename_parts = yaml_file.stem.split('.')
                if len(filename_parts) >= 2:
                    job_id = filename_parts[1]
                    
                    # If specific job ID requested, skip if this isn't it
                    if specific_job_id and job_id != specific_job_id:
                        continue
                    
                    jobs_found += 1
                    
                    # Skip if already processed (unless forcing)
                    if not force and job_id in processed_ids:
                        logger.info(f"Skipping already processed job: {job_id}")
                        continue
                
                # Load the YAML file
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    job_data = yaml.safe_load(f)
                    if job_data: 
                        jobs.append(job_data)
                        logger.info(f"Loaded job: {job_data.get('company', 'Unknown')} - {job_data.get('title', 'Unknown')}")
                        
                        # If we found the specific job, we can return early
                        if specific_job_id and job_id == specific_job_id:
                            logger.info(f"Found specific job ID {specific_job_id}, returning early")
                            return jobs
                        
            except Exception as e:
                logger.error(f"Error loading job file {yaml_file}: {str(e)}", exc_info=True)
                continue
    
    # Now check for subfolder structure (new format)
    subfolders = [d for d in queued_dir.iterdir() if d.is_dir()]
    if subfolders:
        logger.info(f"Found {len(subfolders)} queued job subfolders")
        
        for subfolder in subfolders:
            try:
                # Find YAML files in the subfolder
                yaml_files = list(subfolder.glob('*.yaml'))
                if not yaml_files:
                    logger.warning(f"No YAML files found in subfolder: {subfolder.name}")
                    continue
                
                # Take the first YAML file (should only be one per subfolder)
                yaml_file = yaml_files[0]
                
                # Extract job ID from filename
                filename_parts = yaml_file.stem.split('.')
                if len(filename_parts) >= 2:
                    job_id = filename_parts[1]
                    
                    # If specific job ID requested, skip if this isn't it
                    if specific_job_id and job_id != specific_job_id:
                        continue
                    
                    jobs_found += 1
                    
                    # Skip if already processed (unless forcing)
                    if not force and job_id in processed_ids:
                        logger.info(f"Skipping already processed job: {job_id}")
                        continue
                
                # Load the YAML file
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    job_data = yaml.safe_load(f)
                    if job_data: 
                        jobs.append(job_data)
                        logger.info(f"Loaded job: {job_data.get('company', 'Unknown')} - {job_data.get('title', 'Unknown')}")
                        
                        # If we found the specific job, we can return early
                        if specific_job_id and job_id == specific_job_id:
                            logger.info(f"Found specific job ID {specific_job_id}, returning early")
                            return jobs
                        
            except Exception as e:
                logger.error(f"Error loading job from subfolder {subfolder}: {str(e)}", exc_info=True)
                continue
    
    if specific_job_id and not jobs:
        logger.warning(f"Specific job ID {specific_job_id} not found in queued jobs")
    
    logger.info(f"Found {jobs_found} total queued job files, successfully loaded {len(jobs)} jobs for processing")
    return jobs 



def validate_bullet_length(text, max_chars=180):
    """
    Validate that a bullet point is under the character limit to ensure 2-line formatting.
    
    Args:
        text (str): The bullet point text
        max_chars (int): Maximum characters allowed (default 180)
    
    Returns:
        tuple: (is_valid, character_count, estimated_lines)
    """
    char_count = len(text)
    is_valid = char_count <= max_chars
    
    # Rough estimation: ~90 chars per line for Calibri 10.5pt in 728px container
    estimated_lines = max(1, (char_count + 89) // 90)
    
    return is_valid, char_count, estimated_lines


def structure_resume(resume:dict) -> str:
    """
    Takes a resume dictionary and returns a string representation of the resume, structured for LLM consumption.
    """
    if not resume:
        return ""
    
    sections = []
    
    # Basic info
    if resume.get('name'):
        sections.append(f"Name: {resume['name']}")
    if resume.get('location'):
        sections.append(f"Location: {resume['location']}")
    
    # Summary
    if resume.get('Summary'):
        sections.append(f"\nSummary:\n{resume['Summary']}")
    
    # Contact information
    if resume.get('contacts'):
        sections.append("\nContact Information:")
        for contact in resume['contacts']:
            if contact.get('name') and contact.get('label'):
                contact_line = f"- {contact['name']}: {contact['label']}"
                if contact.get('url'):
                    contact_line += f" (URL: {contact['url']})"
                if contact.get('icon'):
                    # Handle local SVG icons - construct path for web server serving
                    icon_path = f"/resumes/icons/{contact['icon']}"
                    contact_line += f" (Icon: {icon_path})"
                sections.append(contact_line)
    
    # Skills
    if resume.get('skills'):
        sections.append(f"\nSkills:\n{', '.join(resume['skills'])}")
    
    # Experience
    if resume.get('experience'):
        sections.append("\nExperience:")
        for exp in resume['experience']:
            sections.append(f"\n{exp.get('company_name', 'Unknown Company')} ({exp.get('dates', 'Unknown dates')})")
            if exp.get('company_desc'):
                sections.append(f"Company: {exp['company_desc']}")
            
            if exp.get('roles'):
                for role in exp['roles']:
                    sections.append(f"\nRole: {role.get('role', 'Unknown role')} ({role.get('dates', 'Unknown dates')})")
                    if role.get('bullets'):
                        for bullet in role['bullets']:
                            sections.append(f"• {bullet}")
    
    # Education
    if resume.get('education'):
        sections.append("\nEducation:")
        for edu in resume['education']:
            course = edu.get('course', 'Unknown course')
            school = edu.get('school', 'Unknown school')
            dates = edu.get('dates', 'Unknown dates')
            sections.append(f"- {course} - {school} ({dates})")
    
    # Awards and keynotes
    if resume.get('awards_and_keynotes'):
        sections.append("\nAwards and Keynotes:")
        for award in resume['awards_and_keynotes']:
            award_name = award.get('award', 'Unknown award')
            dates = award.get('dates', 'Unknown dates')
            sections.append(f"- {award_name} ({dates})")
    
    # Passions
    if resume.get('passions'):
        sections.append(f"\nPassions:\n{chr(10).join(f'• {passion}' for passion in resume['passions'])}")
    
    return "\n".join(sections)


def structure_job(job:dict) -> str:
    """
    Takes a job dictionary and returns a string representation of the job, structured for LLM consumption.
    """
    if not job:
        return ""
    
    sections = []
    
    # Basic job info
    if job.get('title'):
        sections.append(f"Job Title: {job['title']}")
    if job.get('company'):
        sections.append(f"Company: {job['company']}")
    if job.get('location'):
        sections.append(f"Location: {job['location']}")
    if job.get('salary'):
        sections.append(f"Salary: {job['salary']}")
    if job.get('link'):
        sections.append(f"Job Link: {job['link']}")
    if job.get('date_received'):
        sections.append(f"Date Received: {job['date_received']}")
    if job.get('tags'):
        sections.append(f"Tags: {job['tags']}")
    
    # Job description
    if job.get('description'):
        sections.append(f"\nJob Description:\n{job['description']}")
    
    return "\n".join(sections)



def llm_call(llm_provider:str=None, llm_model:str=None, llm_api_key:str=None, sys_prompt:str=None, user_prompt:str=None, section_name:str=None) -> str:
    """
    Executes supplied prompts against the supplied LLM, and returns string response. 

    Args: 
        llm_provider (str): The company or model provider, i.e., OpenAI, Anthropic, etc.
        llm_model (str): The specific LLM model, i.e., gpt-5-mini, etc.
        llm_api_key (str): The API key that authorizes the request
        sys_prompt (str): System prompt for the request
        user_prompt (str): User prompt for the request
        section_name (str): Optional section name for logging purposes
    """
    load_dotenv()
    llm_provider = llm_provider if llm_provider else os.getenv("LLM_MODEL_PROVIDER")
    llm_model    = llm_model if llm_model else os.getenv("LLM_MODEL")
    llm_api_key  = llm_api_key if llm_api_key else os.getenv("LLM_API_KEY")

    section_suffix = f" for {section_name}" if section_name else ""
    logger.info(f"Making LLM call to {llm_provider}/{llm_model}{section_suffix}")
    
    # Force flush to ensure this log appears immediately
    force_flush_logs()
    
    if not llm_api_key or not llm_model or not llm_provider:
        logger.error("LLM configuration missing")
        raise ValueError("LLM configuration missing. Please set LLM_API_KEY, LLM_MODEL, and LLM_MODEL_PROVIDER in your .env file")
    if not user_prompt: 
        logger.error("No user_prompt provided")
        raise ValueError("No user_prompt submitted. Confirm you've defined a user_prompt to execute.")

    messages=[{"role": "user", "content": user_prompt}]
    if sys_prompt: messages.append({"role": "system", "content": sys_prompt})
    
    logger.debug(f"User prompt length: {len(user_prompt)} characters")
    if sys_prompt:
        logger.debug(f"System prompt length: {len(sys_prompt)} characters")
         
    try:
        if llm_provider.lower() == "openai":
            import openai
            
            logger.info(f"Starting OpenAI API call with 6-minute timeout and 10 retries{section_suffix}")
            start_time = time.time()
            
            # Simple retry logic: 10 attempts with 6-minute timeout each
            max_retries = 10
            timeout_seconds = 360  # 6 minutes
            
            for attempt in range(max_retries):
                try:
                    # Create client with 5-minute timeout
                    client = openai.OpenAI(
                        api_key=llm_api_key,
                        timeout=float(timeout_seconds)
                    )
                    
                    attempt_start = time.time()
                    logger.info(f"Attempt {attempt + 1}/{max_retries} with {timeout_seconds}s timeout{section_suffix}")
                    
                    # Use reliable chat.completions API with flex pricing
                    logger.info(f"Making OpenAI API call{section_suffix}...")
                    response = client.chat.completions.create(
                        model=llm_model,
                        max_completion_tokens=32000,
                        messages=messages,
                        service_tier="flex",  # Use flex tier for cheapest rates
                        timeout=timeout_seconds
                    )
                    
                    attempt_time = time.time() - attempt_start
                    total_time = time.time() - start_time
                    result = response.choices[0].message.content
                    
                    logger.info(f"LLM response received: {len(result)} characters in {attempt_time:.1f}s (attempt {attempt + 1}, total {total_time:.1f}s){section_suffix}")
                    
                    # Force flush after LLM response
                    force_flush_logs()
                    
                    return result
                    
                except Exception as e:
                    attempt_time = time.time() - attempt_start
                    total_time = time.time() - start_time
                    
                    if attempt < max_retries - 1:  # Not the last attempt
                        logger.warning(f"Attempt {attempt + 1}/{max_retries} failed after {attempt_time:.1f}s{section_suffix}: {str(e)}")
                        logger.info(f"Retrying{section_suffix} in 10 seconds... (attempt {attempt + 2}/{max_retries})")
                        
                        # Brief pause before retry (10 seconds)
                        time.sleep(10)
                        continue
                    else:  # Final attempt failed
                        logger.error(f"Final attempt {attempt + 1}/{max_retries} failed after {attempt_time:.1f}s (total {total_time:.1f}s){section_suffix}: {str(e)}")
                        raise Exception(f"OpenAI API failed after {max_retries} attempts with 6-minute timeouts (total {total_time:.1f}s)")
            
        elif llm_provider.lower() == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=llm_api_key)
            
            response = client.messages.create(
                model=llm_model,
                max_tokens=4000,
                temperature=0.7,
                messages=messages
            )
            result = response.content[0].text
            logger.info(f"LLM response received: {len(result)} characters")
            
            # Force flush after LLM response
            force_flush_logs()
            
            return result
            
        else:
            logger.error(f"Unsupported LLM provider: {llm_provider}")
            raise ValueError(f"Unsupported LLM provider: {llm_provider}. Supported providers: openai, anthropic")
            
    except Exception as e:
        logger.error(f"Error in LLM call: {str(e)}", exc_info=True)
        
        # Force flush after error
        force_flush_logs()
        
        return f"Error generating LLM Request: {str(e)}"



def llm_generate_custom_resume(resume:dict, job:dict, additional_prompt:str = None) -> str:
    """
    Accepts a resume and job, and returns a string containing a custom resume tailored to the job.
    Uses an LLM to generate the resume, and returns the generated resume as a string.
    The prompt is pre-defined, but can be appended to arbitrarily using the additional_prompt variable.

    Args: 
        resume (dict): loaded content from `src/resumes/name.yaml` file.
        job (dict): loaded content from `src/jobs/1_queued/job.yaml` file.
        additional_prompt (str, optional): prompt string to be appended to the standard prompt. 

    Returns:
        str: html resume customized for the supplied job (by the LLM)
    """
    # Check if modular generation is available and enabled
    if MODULAR_AVAILABLE:
        try:
            config = get_config()
            if config.is_modular_enabled():
                logger.info("Using modular resume generation")
                
                # Determine job directory for caching
                job_directory = None
                job_id = job.get('id')
                if job_id:
                    # Look for job directory in queued first, then generated
                    from pathlib import Path
                    
                    # Get expected directory name using consistent sanitization
                    job_company = job.get('company', 'Unknown_Company')
                    job_title = job.get('title', 'Unknown_Title')
                    company_clean = sanitize_filename(job_company)
                    title_clean = sanitize_filename(job_title)
                    
                    # Check in queued directory (for active processing)
                    queued_base = Path(__file__).parent / 'jobs' / '1_queued'
                    if queued_base.exists():
                        for job_dir in queued_base.iterdir():
                            if job_dir.is_dir():
                                # Check if directory matches expected pattern: {company}.{title}.{id}.{timestamp}
                                if (job_id in job_dir.name and 
                                    company_clean in job_dir.name and 
                                    title_clean in job_dir.name):
                                    job_directory = str(job_dir)
                                    logger.info(f"Found job directory for caching: {job_directory}")
                                    break
                    
                    # If not found in queued, check generated directory
                    if not job_directory:
                        generated_base = Path(__file__).parent / 'jobs' / '2_generated'
                        if generated_base.exists():
                            for job_dir in generated_base.iterdir():
                                if job_dir.is_dir():
                                    # Check if directory matches expected pattern: {company}.{title}.{id}.{timestamp}
                                    if (job_id in job_dir.name and 
                                        company_clean in job_dir.name and 
                                        title_clean in job_dir.name):
                                        job_directory = str(job_dir)
                                        logger.info(f"Found job directory in generated: {job_directory}")
                                        break
                
                return llm_generate_custom_resume_modular(resume, job, additional_prompt, job_directory)
        except Exception as e:
            logger.warning(f"Modular generation failed, falling back to legacy: {str(e)}")
    
    # Use legacy generation
    logger.info("Using legacy resume generation")
    return llm_generate_custom_resume_legacy(resume, job, additional_prompt)


def llm_generate_custom_resume_modular(resume:dict, job:dict, additional_prompt:str = None, job_directory: str = None, use_cache: bool = True) -> str:
    """
    Generate resume using the new modular system.
    
    Args: 
        resume (dict): loaded content from `src/resumes/name.yaml` file.
        job (dict): loaded content from `src/jobs/1_queued/job.yaml` file.
        additional_prompt (str, optional): prompt string to be appended to the standard prompt.
        job_directory (str, optional): path to job directory for caching AI content
        use_cache (bool): whether to use cached content when available

    Returns:
        str: html resume customized for the supplied job (by the modular system)
    """
    try:
        # Create modular generator
        config = get_config()
        generator = ModularResumeGenerator(config.to_dict())
        
        # Generate job ID for tracking
        job_id = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate resume using modular approach with caching support
        result = generator.generate_resume(resume, job, job_id, job_directory, use_cache)
        
        if result.get('success'):
            logger.info(f"Modular generation successful for job {job_id}")
            return result.get('html_resume', '')
        else:
            logger.error(f"Modular generation failed: {result.get('error', 'Unknown error')}")
            raise Exception(f"Modular generation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"Error in modular resume generation: {str(e)}", exc_info=True)
        raise


def regenerate_html_from_cached_content(job_directory: str, job_data: dict, resume_data: dict = None) -> dict:
    """
    Regenerate HTML and PDF files using cached AI content without re-running AI generation.
    
    Args:
        job_directory (str): path to job directory containing cached AI content
        job_data (dict): job information for template rendering
        
    Returns:
        dict: result containing HTML content and metadata
    """
    try:
        logger.info(f"Regenerating HTML from cached content in: {job_directory}")
        
        # Create modular generator
        config = get_config()
        generator = ModularResumeGenerator(config.to_dict())
        
        # Regenerate from cache
        result = generator.regenerate_html_from_cache(job_directory, job_data, resume_data)
        
        if result.get('success'):
            logger.info("Successfully regenerated HTML/PDF from cached content")
            return result
        else:
            logger.error(f"Failed to regenerate from cache: {result.get('error', 'Unknown error')}")
            raise Exception(f"Failed to regenerate from cache: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"Error regenerating from cached content: {str(e)}", exc_info=True)
        raise


def llm_generate_custom_resume_legacy(resume:dict, job:dict, additional_prompt:str = None) -> str:
    """
    Legacy resume generation function (original implementation).
    
    Args: 
        resume (dict): loaded content from `src/resumes/name.yaml` file.
        job (dict): loaded content from `src/jobs/1_queued/job.yaml` file.
        additional_prompt (str, optional): prompt string to be appended to the standard prompt. 

    Returns:
        str: html resume customized for the supplied job (by the LLM)
    """

    resume_str = structure_resume(resume)
    job_str = structure_job(job)
    with open( Path(__file__).parent / 'resources' / 'templates' / 'example.resume.html') as fh:
        example_html_str = fh.read()

    sys_prompt = """
    You are a professional resume writer who creates tailored resumes in HTML format. Return ONLY the requested output. 
    Do NOT include explanations, commentary, preambles, apologies, or formatting outside what is explicitly requested.
    If the output cannot be produced, return an empty string.
    
    Output constraints:
    - Return only valid HTML.
    - Do not wrap the output in code fences.
    - Do not include conversational text.
    - Do not include explanations.
    """

    user_prompt = f"""
Create a tailored HTML resume for this job opportunity using the provided example template as your guide.

CONTENT GUIDELINES:
- 🚨 CRITICAL: Keep all factual information accurate - NEVER fabricate ideas, skills, experiences, education, or achievements
- NEVER invent or add skills, experiences, education, or awards not present in the original resume
- Select and emphasize the most relevant experience, skills, and achievements for this role
- Reword for clarity and to maximize relevence to the job opportunity, but always maintain factual accuracy
- Follow the structure and CSS classes shown in the example template
- **IMPORTANT**: Always craft responses within character counts provided in each section detail (including spaces)

KEY SECTIONS TO CUSTOMIZE:
1. **Professional Summary**: Create a Professional Summary tailored to the specific job description provided, using between 580 and 630 characters.
2. **Selected Achievements**: Create 5 achievement bullets, each between 300 and 350 characters, that best demonstrate fit for this role - must be based on actual resume content.
3. **Core Skills**: Select 12 most relevant skills from resume, arranged in 3 columns of 4 skills each. Each skill must be between 20 and 36 characters. 🚨 CRITICAL: NEVER FABRICATE OR INVENT NEW SKILLS - only use skills from the resume or logical combinations/expansions of existing skills (e.g., "AWS" becomes "AWS cloud services", "SQL" becomes "SQL database management"). DO NOT add skills not represented in the candidate's actual background.
4. **Experience**: Prioritize and reorder bullets within each role to highlight job-relevant accomplishments first.
   - Company name line: ONLY the company name (no descriptions or extra text)
   - Company description line: Brief description WITHOUT "Company:" prefix
   - Follow the exact 3-level hierarchy shown in the example template
   - Display companies / roles in the order they appear in the YAML file
   - Each role's bullet MUST be between 90 and 115 characters, OR between 180 and 240 (2 lines) characters, including spaces.  
   - Each role's bullet may NOT be between 115 and 180 characters.  Each role's bullet may NOT be less than 90 NOR greater than 240.
5. **Education**: ALWAYS include ALL "education" entries from the resume (never skip any) without dates/years - show only course and school
6. **Awards & Speaking**: ALWAYS Include ALL "awards_and_keynotes" entries from the resume (never skip any) without dates/years - show only the award/keynote title

STRUCTURE REQUIREMENTS:
- Use the exact HTML structure from the example template, with new content
- Include all contact information with proper icons:
  - For Material Icons (single words like "home_pin", "mail", "mobile"): use <span class="material-symbols-outlined">icon_name</span>
  - For local SVG files (ending in .svg): use <img src="/resumes/icons/filename.svg" alt="Icon" style="width: 12px; height: 12px;" />
- Contact format: icon + clickable label only (no text labels like "Email:")
- Maintain 2-character indentation hierarchy in Experience section
- Keep to 2 pages maximum

CANDIDATE RESUME:
{resume_str}

JOB DESCRIPTION:
{job_str}

EXAMPLE TEMPLATE:
```
{example_html_str}
```

Generate the complete HTML resume following the example template structure and CSS classes.
"""

    # Add additional prompt if provided
    if additional_prompt:
        user_prompt += f"\n\nADDITIONAL INSTRUCTIONS:\n{additional_prompt}"

    response = llm_call(sys_prompt=sys_prompt, user_prompt=user_prompt)    
    return response




def llm_generate_custom_coverletter(resume:dict, job:dict, custom_resume:str, additional_prompt:str = None) -> str:
    """
    Accepts the final html output from `llm_generate_custom_resume()`, and uses an LLM to generate a matching
    cover letter.  The cover letter can be addressed to the hiring committee for the company name in the job 
    information provided. The prompt is pre-defined, but can be appended to arbitrarily using the additional_prompt.

    Args: 
        custom_resume (str): html content returned from `llm_generate_custom_resume()`
        job (dict): loaded content from `src/jobs/1_queued/job.yaml` file.
        additional_prompt (str, optional): prompt string to be appended to the standard prompt. 

    Returns:
        str: html cover letter customized for the supplied job (by the LLM) and matching the style of the custom_resume
    """
    # Check if modular generation is available and enabled
    if MODULAR_AVAILABLE:
        try:
            config = get_config()
            if config.is_modular_enabled():
                logger.info("Using modular cover letter generation")
                return llm_generate_custom_coverletter_modular(resume, job, custom_resume, additional_prompt)
        except Exception as e:
            logger.warning(f"Modular cover letter generation failed, falling back to legacy: {str(e)}")
    
    # Use legacy generation
    logger.info("Using legacy cover letter generation")
    return llm_generate_custom_coverletter_legacy(resume, job, custom_resume, additional_prompt)


def llm_generate_custom_coverletter_modular(resume:dict, job:dict, custom_resume:str, additional_prompt:str = None) -> str:
    """
    Generate cover letter using the new modular system.
    
    Args: 
        resume (dict): loaded content from `src/resumes/name.yaml` file.
        job (dict): loaded content from `src/jobs/1_queued/job.yaml` file.
        custom_resume (str): html content returned from `llm_generate_custom_resume()`
        additional_prompt (str, optional): prompt string to be appended to the standard prompt. 

    Returns:
        str: html cover letter customized for the supplied job (by the modular system)
    """
    try:
        # Create modular generator
        config = get_config()
        generator = ModularResumeGenerator(config.to_dict())
        
        # Generate job ID for tracking
        job_id = f"cover_letter_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate cover letter using modular approach
        result = generator.generate_resume(resume, job, job_id)
        
        if result.get('success'):
            logger.info(f"Modular cover letter generation successful for job {job_id}")
            return result.get('html_cover_letter', '')
        else:
            logger.error(f"Modular cover letter generation failed: {result.get('error', 'Unknown error')}")
            raise Exception(f"Modular cover letter generation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"Error in modular cover letter generation: {str(e)}", exc_info=True)
        raise


def llm_generate_custom_coverletter_legacy(resume:dict, job:dict, custom_resume:str, additional_prompt:str = None) -> str:
    """
    Legacy cover letter generation function (original implementation).
    
    Args: 
        resume (dict): loaded content from `src/resumes/name.yaml` file.
        job (dict): loaded content from `src/jobs/1_queued/job.yaml` file.
        custom_resume (str): html content returned from `llm_generate_custom_resume()`
        additional_prompt (str, optional): prompt string to be appended to the standard prompt. 

    Returns:
        str: html cover letter customized for the supplied job (by the LLM) and matching the style of the custom_resume
    """
    
    job_str = structure_job(job)
    co_name = job['company']+' ' if 'company' in job else ''
    
    coverletter_prefix = f"""
    {datetime.now().strftime('%b. %d, %Y')}

    Dear {co_name}hiring team,
    """
    
    coverletter_suffix = f"""
    Should you ever have questions, feel free to contact me at any time.

    Thank you,

    Stephen Hilton
    """

    user_prompt = f"""
Generate a tailored HTML cover letter that matches the style and content of the provided resume.

GUIDELINES:
- Keep it professional and concise (max 350 words)
- Use impactful language highlighting the candidate's fit for this role
- Match the header format from the resume (same contact info with icons, no text labels)
- For icons: Material Icons use <span class="material-symbols-outlined">icon_name</span>, SVG files use <img src="/resumes/icons/filename.svg" alt="Icon" style="width: 12px; height: 12px;" />
- Use the same CSS classes and structure as the resume
- Always start the letter body with the coverletter_prefix, and end with the suffix. 
- Add whitespace and newlines liberally, as needed.

PREFIX:
{coverletter_prefix}


SUFFIX:
{coverletter_suffix}


CUSTOMIZED RESUME:
```
{custom_resume}
```

JOB DESCRIPTION:
{job_str}

Generate the complete HTML cover letter using the same CSS classes and structure as the resume.
    """

    # Add additional prompt if provided
    if additional_prompt:
        user_prompt += f"\n\nADDITIONAL INSTRUCTIONS:\n{additional_prompt}"

    sys_prompt = """
    You are a professional resume writer who creates tailored cover letters in HTML format. Return ONLY the requested output. 
    Do NOT include explanations, commentary, preambles, apologies, or formatting outside what is explicitly requested.
    If the output cannot be produced, return an empty string.
    
    Output constraints:
    - Return only valid HTML.
    - Do not wrap the output in code fences.
    - Do not include conversational text.
    - Do not include explanations.
    """

    response = llm_call(sys_prompt=sys_prompt, user_prompt=user_prompt)
    return response
 

def llm_generate_job_summary(job:dict) -> str:
    """
    Accepts the original job description from LinkedIn and generates a high-level summary, in HTML form. 

    Args: 
        job (dict): loaded content from `src/jobs/1_queued/job.yaml` file.

    Returns:
        str: html summary of the job.
    """
    job_str = structure_job(job)
    
    sys_prompt = f"""
    You are a careful job summarizer; you take job descriptions and prepare a brief summary report using human-readable HTML that reports on:
    Company: <short description>
    LinkedIn Posting: <link / url to linkedin posting>
    Job Desc: <short job description>
    Requirements & Expected Activities: <small bullet list>
    """
    
    user_prompt = f"""
    Generate your brief summary report for this job:

    JOB DESCRIPTION:
    {job_str}
    """
    response = llm_call(sys_prompt=sys_prompt, user_prompt=user_prompt)
    return response



def move_queued_to_errored(id:str) -> bool:
    """
    Accepts an id that has errored during generation, then moves all files in either
    `src/jobs/1_queued/{id}*` or `src/jobs/1_queued/*/` containing files with {id} or 
    `src/jobs/2_generated/{id}*` over to `src/jobs/8_errors/`. 
    Now handles both flat files (legacy) and subfolder structure.
    """
    logger.info(f"Moving files for job ID {id} to errors directory due to generation failure")
    
    try:
        # Get the jobs directory
        jobs_dir = Path(__file__).parent / 'jobs'
        queued_dir = jobs_dir / '1_queued'
        generated_dir = jobs_dir / '2_generated'
        errors_dir = jobs_dir / '8_errors'
        
        # Ensure errors directory exists
        errors_dir.mkdir(exist_ok=True)
        
        # Find all files matching the job ID pattern in both directories
        pattern = f"*.{id}.*"
        matching_files = []
        subfolders_to_move = []
        
        # Check queued directory for flat files
        if queued_dir.exists():
            queued_files = list(queued_dir.glob(pattern))
            matching_files.extend([(f, 'queued') for f in queued_files])
            
            # Check queued directory for subfolders containing the job ID
            for subfolder in queued_dir.iterdir():
                if subfolder.is_dir():
                    subfolder_files = list(subfolder.glob(f"*.{id}.*"))
                    if subfolder_files:
                        subfolders_to_move.append((subfolder, 'queued'))
            
        # Check generated directory for flat files
        if generated_dir.exists():
            generated_files = list(generated_dir.glob(pattern))
            matching_files.extend([(f, 'generated') for f in generated_files])
            
            # Check generated directory for subfolders containing the job ID
            for subfolder in generated_dir.iterdir():
                if subfolder.is_dir():
                    subfolder_files = list(subfolder.glob(f"*.{id}.*"))
                    if subfolder_files:
                        subfolders_to_move.append((subfolder, 'generated'))
        
        if not matching_files and not subfolders_to_move:
            logger.warning(f"No files or subfolders found matching job ID {id} in queued or generated directories")
            return False
        
        logger.info(f"Found {len(matching_files)} files and {len(subfolders_to_move)} subfolders to move to errors directory for job ID {id}")
        
        # Move flat files
        moved_count = 0
        for file_path, source_type in matching_files:
            try:
                destination = errors_dir / file_path.name
                
                # If destination exists, remove it first
                if destination.exists():
                    logger.debug(f"Removing existing error file: {destination}")
                    destination.unlink()
                
                # Move the file
                file_path.rename(destination)
                logger.debug(f"Moved from {source_type}: {file_path.name} -> {destination}")
                moved_count += 1
                
            except Exception as e:
                logger.error(f"Error moving file {file_path} to errors directory: {str(e)}")
                continue
        
        # Move subfolders
        subfolders_moved = 0
        for subfolder, source_type in subfolders_to_move:
            try:
                destination_folder = errors_dir / subfolder.name
                
                # If destination exists, remove it first
                if destination_folder.exists():
                    logger.debug(f"Removing existing error folder: {destination_folder}")
                    import shutil
                    shutil.rmtree(destination_folder)
                
                # Move the entire subfolder
                subfolder.rename(destination_folder)
                logger.debug(f"Moved subfolder from {source_type}: {subfolder.name} -> {destination_folder.name}")
                subfolders_moved += 1
                
            except Exception as e:
                logger.error(f"Error moving subfolder {subfolder} to errors directory: {str(e)}")
                continue
        
        total_moved = moved_count + subfolders_moved
        if total_moved > 0:
            logger.info(f"Successfully moved {moved_count} files and {subfolders_moved} subfolders to errors directory for job ID {id}")
            return True
        else:
            logger.error(f"Failed to move any files or subfolders to errors directory for job ID {id}")
            return False
            
    except Exception as e:
        logger.error(f"Error in move_queued_to_errored for job ID {id}: {str(e)}", exc_info=True)
        return False


def move_queued_to_generated_with_validation(id: str) -> bool:
    """
    Moves a job from queued to generated after all 7 ai_content files are created,
    and validates all existing jobs in 2_generated to ensure they have complete ai_content.
    Returns any incomplete jobs back to 1_queued.
    
    Args:
        id (str): Job ID that has completed AI content generation
        
    Returns:
        bool: True if move was successful, False otherwise
    """
    logger.info(f"Moving job {id} to generated and validating all generated jobs")
    
    try:
        # Get the jobs directory
        jobs_dir = Path(__file__).parent / 'jobs'
        queued_dir = jobs_dir / '1_queued'
        generated_dir = jobs_dir / '2_generated'
        
        # Ensure directories exist
        if not queued_dir.exists():
            logger.error(f"Queued directory does not exist: {queued_dir}")
            return False
            
        generated_dir.mkdir(exist_ok=True)
        
        # First, move the current job to generated (same logic as move_queued_to_generated)
        move_success = move_queued_to_generated(id)
        if not move_success:
            logger.error(f"Failed to move job {id} to generated directory")
            return False
        
        logger.info(f"Successfully moved job {id} to generated directory")
        
        # Now validate all jobs in 2_generated directory
        logger.info("Validating all jobs in generated directory for complete ai_content...")
        
        incomplete_jobs = []
        
        # Check all subfolders in generated directory
        for subfolder in generated_dir.iterdir():
            if not subfolder.is_dir():
                continue
                
            ai_content_dir = subfolder / 'ai_content'
            
            # Skip if no ai_content directory exists
            if not ai_content_dir.exists():
                logger.debug(f"Subfolder {subfolder.name} has no ai_content directory, skipping validation")
                continue
            
            # Count YAML files in ai_content directory
            yaml_files = list(ai_content_dir.glob('*.yaml'))
            yaml_count = len(yaml_files)
            
            logger.debug(f"Subfolder {subfolder.name} has {yaml_count} ai_content files: {[f.stem for f in yaml_files]}")
            
            # If less than 7 files, mark for return to queued
            if yaml_count < 7:
                incomplete_jobs.append(subfolder)
                logger.warning(f"Found incomplete job {subfolder.name} with only {yaml_count}/7 ai_content files")
        
        # Move incomplete jobs back to queued directory
        moved_back_count = 0
        for incomplete_job_dir in incomplete_jobs:
            try:
                # Determine destination path in queued directory
                destination = queued_dir / incomplete_job_dir.name
                
                # If destination already exists, remove it first
                if destination.exists():
                    logger.debug(f"Removing existing queued folder: {destination}")
                    import shutil
                    shutil.rmtree(destination)
                
                # Move the incomplete job back to queued
                incomplete_job_dir.rename(destination)
                logger.info(f"Moved incomplete job back to queued: {incomplete_job_dir.name}")
                moved_back_count += 1
                
            except Exception as e:
                logger.error(f"Error moving incomplete job {incomplete_job_dir} back to queued: {str(e)}")
                continue
        
        if moved_back_count > 0:
            logger.info(f"Moved {moved_back_count} incomplete jobs back to queued directory")
        else:
            logger.info("All jobs in generated directory have complete ai_content (7 files each)")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in move_queued_to_generated_with_validation for job ID {id}: {str(e)}", exc_info=True)
        return False


def move_queued_to_generated(id:str) -> bool:
    """
    Accepts an id that has completed generation, then moves all files in
    `src/jobs/1_queued/{id}*` or `src/jobs/1_queued/*/` containing files with {id} over to `src/jobs/2_generated/`. 
    Now handles both flat files (legacy) and subfolder structure.
    """
    logger.info(f"Moving queued files for job ID {id} to generated directory")
    
    try:
        # Get the jobs directory
        jobs_dir = Path(__file__).parent / 'jobs'
        queued_dir = jobs_dir / '1_queued'
        generated_dir = jobs_dir / '2_generated'
        
        # Ensure directories exist
        if not queued_dir.exists():
            logger.error(f"Queued directory does not exist: {queued_dir}")
            return False
            
        generated_dir.mkdir(exist_ok=True)
        
        # First check for flat files (legacy format)
        pattern = f"*.{id}.*"
        flat_files = list(queued_dir.glob(pattern))
        
        if flat_files:
            logger.info(f"Found {len(flat_files)} flat files to move for job ID {id}")
            
            # Move each matching flat file
            moved_count = 0
            for file_path in flat_files:
                try:
                    destination = generated_dir / file_path.name
                    
                    # If destination exists, remove it first
                    if destination.exists():
                        logger.debug(f"Removing existing file: {destination}")
                        destination.unlink()
                    
                    # Move the file
                    file_path.rename(destination)
                    logger.debug(f"Moved: {file_path.name} -> {destination}")
                    moved_count += 1
                    
                except Exception as e:
                    logger.error(f"Error moving file {file_path}: {str(e)}")
                    continue
            
            if moved_count > 0:
                logger.info(f"Successfully moved {moved_count} flat files for job ID {id}")
                return True
        
        # Now check for subfolder structure (new format)
        subfolders_moved = 0
        for subfolder in queued_dir.iterdir():
            if not subfolder.is_dir():
                continue
                
            # Check if this subfolder contains files with the target job ID
            matching_files = list(subfolder.glob(f"*.{id}.*"))
            if matching_files:
                logger.info(f"Found subfolder with job ID {id}: {subfolder.name}")
                
                try:
                    # Move the entire subfolder to generated directory
                    destination_folder = generated_dir / subfolder.name
                    
                    # If destination exists, remove it first
                    if destination_folder.exists():
                        logger.debug(f"Removing existing folder: {destination_folder}")
                        import shutil
                        shutil.rmtree(destination_folder)
                    
                    # Move the entire subfolder
                    subfolder.rename(destination_folder)
                    logger.info(f"Moved subfolder: {subfolder.name} -> {destination_folder.name}")
                    subfolders_moved += 1
                    
                except Exception as e:
                    logger.error(f"Error moving subfolder {subfolder}: {str(e)}")
                    continue
        
        if subfolders_moved > 0:
            logger.info(f"Successfully moved {subfolders_moved} subfolders for job ID {id}")
            return True
        
        # If we get here, no files were found
        logger.warning(f"No files or subfolders found matching job ID {id} in {queued_dir}")
        return False
            
    except Exception as e:
        logger.error(f"Error in move_queued_to_generated for job ID {id}: {str(e)}", exc_info=True)
        return False




def print_pdf(job_id: str = None, output_dir: str = None):
    """
    Convert HTML resume and cover letter files to PDF format.
    
    This function now uses the PDFManager class for better maintainability.
    
    Args:
        job_id (str, optional): Specific job ID to convert. If None, converts all jobs in 2_generated.
        output_dir (str, optional): Output directory for PDFs. If None, saves PDFs alongside HTML files.
    
    Returns:
        dict: Summary of conversion results
    """
    from src.utils.pdf_mgr import print_pdf as pdf_print_pdf
    return pdf_print_pdf(job_id, output_dir)



def bundle_to_directory(ids:str|list) -> Path:
    """
    Accepts a job id (second part of job .yaml/.html files) and 
      (1) confirms there is a job.yaml file in `src/2_generated/` with an id that matches
      (2) creates a new directory under `src/2_generated/` named `{company}.{title}.{id}.{date}`
      (3) moves all files within `src/2_generated/*.{id}.*` to that newly created directory
      (4) returns the Path object for the newly created and populated directory
    """
    if not isinstance(ids, list): ids = [str(ids)]
    
    try:
        for id in ids:
            logger.info(f"Bundling files for job ID {id} into directory")

            # Get the generated directory
            jobs_dir = Path(__file__).parent / 'jobs'
            generated_dir = jobs_dir / '2_generated'
            
            if not generated_dir.exists():
                logger.error(f"Generated directory does not exist: {generated_dir.name}")
                raise ValueError(f"Generated directory does not exist: {generated_dir.name}")
            
            # Find all files matching the job ID pattern
            pattern = f"*.{id}.*"
            matching_files = list(generated_dir.glob(pattern))
            
            if not matching_files:
                logger.warning(f"No files found matching pattern {pattern} in {generated_dir.name}")
                continue
            
            # Find the job YAML file to extract company and title
            job_yaml_file = None
            for file_path in matching_files:
                if file_path.suffix == '.yaml':
                    job_yaml_file = file_path
                    break
            
            if not job_yaml_file:
                logger.warning(f"No job YAML file found for job ID {id}")
                continue
            
            # Load the job data to get company and title
            try:
                with open(job_yaml_file, 'r', encoding='utf-8') as f:
                    job_data = yaml.safe_load(f)
            except Exception as e:
                logger.error(f"Error loading job YAML file {job_yaml_file}: {str(e)}")
                continue
            
            # Extract company and title, sanitize for directory name
            company = job_data.get('company', 'Unknown_Company')
            title = job_data.get('title', 'Unknown_Title')
            
            company_clean = sanitize_filename(company)
            title_clean = sanitize_filename(title)
            
            # Extract timestamp from the first file (they should all have the same timestamp)
            filename_parts = matching_files[0].stem.split('.')
            timestamp = filename_parts[0] if len(filename_parts) > 0 else datetime.now().strftime('%Y%m%d%H%M%S')
            
            # Create directory name: {company}.{title}.{id}.{date}
            directory_name = f"{company_clean}.{title_clean}.{id}.{timestamp}"
            bundle_dir = generated_dir / directory_name
            
            # Create the directory
            bundle_dir.mkdir(exist_ok=True)
            logger.info(f"Created bundle directory: {bundle_dir}")
            
            # Move all matching files to the new directory
            moved_count = 0
            for file_path in matching_files:
                try:
                    destination = bundle_dir / file_path.name
                    
                    # If destination exists, remove it first
                    if destination.exists():
                        logger.debug(f"Removing existing file: {destination}")
                        destination.unlink()
                    
                    # Move the file
                    file_path.rename(destination)
                    logger.debug(f"Moved: {file_path.name} -> {destination}")
                    moved_count += 1
                    
                except Exception as e:
                    logger.error(f"Error moving file {file_path}: {str(e)}")
                    continue
            
            if moved_count > 0:
                logger.info(f"Successfully bundled {moved_count} files for job ID {id} into {bundle_dir}")
            else:
                logger.warning(f"Failed to move ANY files for job ID {id}")
                # Clean up empty directory
                if bundle_dir.exists() and not any(bundle_dir.iterdir()): bundle_dir.rmdir()
            
    except Exception as e:
        logger.error(f"Error in bundle_to_directory for job ID {id}: {str(e)}", exc_info=True)
        raise 



def generate(force:bool=False, id:str=None, additional_prompt:str=None):
    """
    Main function to demonstrate the functionality of the jobs_2_generate module.
    Loads resume and jobs, then generates custom resumes and cover letters for each job.

    Args: 
        force (bool): Allows you to force generation, regardless if whether the ID pre-exists
        id (str): Selects a specific ID to generate, rather than all queued work; id must exist in 1_queued/
    """
    logger.info("Starting resume generation process")
    
    # Create progress file for web UI tracking
    progress_file = Path(__file__).parent / 'jobs' / '.step2_progress.json'
    
    def update_progress(status, message, current_job=0, total_jobs=0, current_job_name='', error=None):
        """Update progress file for web UI"""
        try:
            import json
            progress_data = {
                'status': status,
                'message': message,
                'current_job': current_job,
                'total_jobs': total_jobs,
                'current_job_name': current_job_name,
                'progress_percent': int((current_job / total_jobs * 100)) if total_jobs > 0 else 0,
                'completed': status == 'completed',
                'error': error,
                'timestamp': datetime.now().isoformat()
            }
            with open(progress_file, 'w') as f:
                json.dump(progress_data, f)
        except Exception as e:
            logger.warning(f"Could not update progress file: {e}")
    
    # Initialize progress
    update_progress('starting', 'Initializing resume generation...')
    
    # Load resume
    logger.info("Loading resume...")
    update_progress('starting', 'Loading resume file...')
    try:
        resume = load_resume_file('Stephen_Hilton')
        if not resume:
            logger.error("Failed to load resume file")
            update_progress('error', 'Failed to load resume file', error='Resume file not found')
            return
        
        logger.info(f"Loaded resume for: {resume.get('name', 'Unknown')}")
    except Exception as e:
        logger.error(f"Error loading resume: {str(e)}", exc_info=True)
        update_progress('error', f'Error loading resume: {str(e)}', error=str(e))
        return
    
    # Load queued jobs
    logger.info("Loading queued jobs...")
    update_progress('starting', 'Loading queued jobs...')
    try:
        jobs = load_queued_jobs(force=force, specific_job_id=id)
        if id: 
            logger.info(f"Generating for specified ID: {id} (type: {type(id)})")
            # Jobs should already be filtered by load_queued_jobs, but double-check
            if not jobs:
                logger.warning(f"No jobs found for specific ID: {id}")
                update_progress('completed', f'No jobs found for ID: {id}', 0, 0)
                return
            elif len(jobs) > 1:
                logger.warning(f"Multiple jobs found for ID {id}, using first one")
                jobs = jobs[:1]
        logger.info(f"Found {len(jobs)} jobs to process")
        
        if not jobs:
            logger.warning("No jobs found to process")
            update_progress('completed', 'No jobs found to process', 0, 0)
            return
    except Exception as e:
        logger.error(f"Error loading jobs: {str(e)}", exc_info=True)
        update_progress('error', f'Error loading jobs: {str(e)}', error=str(e))
        return
    
    # Create output directory
    jobs_dir = Path(__file__).parent / 'jobs' / '2_generated'
    jobs_dir.mkdir(exist_ok=True)
    logger.info(f"Output directory: {jobs_dir}")
    
    # Get resume filename for output naming
    resume_filename = resume.get('name', '').replace(' ','_')
    if not resume_filename: 
        logger.error("Resume file missing 'name' key")
        error_msg = "Resume file missing 'name' key"
        update_progress('error', error_msg, error=error_msg)
        raise ValueError(f"Supplied src/resumes/YourName.yaml file did not include a 'name' key, please double-check the yaml file structure and try again.")
    
    # Start processing
    total_jobs = len(jobs)
    successful_jobs = 0
    failed_jobs = 0
    
    update_progress('running', f'Starting to process {total_jobs} jobs...', 0, total_jobs)
    
    # Process each job
    for i, job in enumerate(jobs):
        job_title = job.get('title', 'Unknown')
        job_company = job.get('company', 'Unknown')
        
        # CRITICAL FIX: Ensure job ID is never empty or "Unknown"
        job_id = job.get('id')
        if not job_id or job_id == 'Unknown' or job_id.strip() == '':
            # Generate a proper job ID based on company and title
            import hashlib
            job_content = f"{job_company}_{job_title}_{i}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            job_id = str(abs(hash(job_content)) % 10000000000)  # 10-digit ID
            logger.warning(f"Generated new job ID {job_id} for job with missing/invalid ID: {job_title} at {job_company}")
            # Update the job data with the new ID
            job['id'] = job_id
        
        current_job_name = f"{job_title} at {job_company}"
        logger.info(f"Processing job {i+1}/{len(jobs)}: {current_job_name} (ID: {job_id})")
        
        # Update progress for current job
        update_progress('running', f'Processing {current_job_name}...', i, total_jobs, current_job_name)
        
        try:
            # Find the original queued file to extract timestamp and get job YAML path
            queued_dir = Path(__file__).parent / 'jobs' / '1_queued'
            timestamp = None
            job_yaml_path = None
            
            # Look for the matching job file by ID - check both flat files and subfolders
            # First check flat files (legacy format)
            for queued_file in queued_dir.glob('*.yaml'):
                filename_parts = queued_file.stem.split('.')
                if len(filename_parts) >= 2 and filename_parts[1] == job_id:
                    timestamp = filename_parts[0]
                    job_yaml_path = queued_file
                    break
            
            # If not found in flat files, check subfolders (new format)
            if not timestamp:
                for subfolder in queued_dir.iterdir():
                    if subfolder.is_dir():
                        for queued_file in subfolder.glob('*.yaml'):
                            filename_parts = queued_file.stem.split('.')
                            if len(filename_parts) >= 2 and filename_parts[1] == job_id:
                                timestamp = filename_parts[0]
                                job_yaml_path = queued_file
                                break
                        if timestamp:
                            break
            
            if not timestamp:
                logger.warning(f"Could not find timestamp for job {job_id}, using current time")
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # IMPROVED: Create job directory immediately instead of loose files
            # Sanitize company and title for directory name
            company_clean = sanitize_filename(job_company)
            title_clean = sanitize_filename(job_title)
            
            # Create job directory: {company}.{title}.{id}.{timestamp}
            job_directory_name = f"{company_clean}.{title_clean}.{job_id}.{timestamp}"
            job_output_dir = jobs_dir / job_directory_name
            job_output_dir.mkdir(exist_ok=True)
            
            # Create ai_content subdirectory for caching
            ai_content_dir = job_output_dir / 'ai_content'
            ai_content_dir.mkdir(exist_ok=True)
            
            logger.info(f"Created job directory: {job_directory_name}")
            
            # ------------------------------------------------------------
            # Generate custom resume
            logger.info("Generating custom resume...")
            update_progress('running', f'Generating resume for {current_job_name}...', i, total_jobs, current_job_name)
            force_flush_logs()
            custom_resume = llm_generate_custom_resume(resume, job, additional_prompt)
            logger.info(f"Generated resume length: {len(custom_resume)} characters")
            force_flush_logs()
            
            # Save resume in job directory
            resume_filename_output = f"{timestamp}.{job_id}.{company_clean}.resume.html"
            # Add version info to HTML content
            if len(custom_resume) > 0:
                # Add version to footer
                custom_resume = custom_resume.replace(
                    '</body>',
                    f'<div class="version-footer"><a href="https://github.com/Stephen-Hilton/resumai" target="_blank" style="color: inherit; text-decoration: none;">ResumeAI v{VERSION}</a></div></body>'
                )
                
                resume_output_path = job_output_dir / resume_filename_output
                with open(resume_output_path, 'w', encoding='utf-8') as f:
                    f.write(custom_resume)
                logger.info(f"Resume saved: {resume_output_path}")
            else:
                logger.error("Generated resume is empty, not saving")
                move_queued_to_errored(job_id)
                continue


            # ------------------------------------------------------------
            # Generate custom cover letter
            logger.info("Generating custom cover letter...")
            update_progress('running', f'Generating cover letter for {current_job_name}...', i, total_jobs, current_job_name)
            force_flush_logs()
            custom_coverletter = llm_generate_custom_coverletter(resume, job, custom_resume, additional_prompt)
            logger.info(f"Generated cover letter length: {len(custom_coverletter)} characters")
            force_flush_logs()

            # Save cover letter in job directory
            coverletter_filename_output = f"{timestamp}.{job_id}.{company_clean}.coverletter.html"
            # Add version info to cover letter HTML content  
            if len(custom_coverletter) > 0:
                # Add version to footer
                custom_coverletter = custom_coverletter.replace(
                    '</body>',
                    f'<div class="version-footer"><a href="https://github.com/Stephen-Hilton/resumai" target="_blank" style="color: inherit; text-decoration: none;">ResumeAI v{VERSION}</a></div></body>'
                )
                
                coverletter_output_path = job_output_dir / coverletter_filename_output
                with open(coverletter_output_path, 'w', encoding='utf-8') as f:
                    f.write(custom_coverletter)
                logger.info(f"Cover letter saved: {coverletter_output_path}")
            else:
                logger.error("Generated cover letter is empty, not saving")
                move_queued_to_errored(job_id)
                continue


            # ------------------------------------------------------------
            # Generate job summary
            logger.info("Generating job summary...")
            update_progress('running', f'Generating summary for {current_job_name}...', i, total_jobs, current_job_name)
            force_flush_logs()
            custom_summary = llm_generate_job_summary(job)
            logger.info(f"Generated summary length: {len(custom_summary)} characters")
            force_flush_logs()

            # Save summary in job directory
            summary_filename_output = f"{timestamp}.{job_id}.{company_clean}.!SUMMARY.html"
            if len(custom_summary) > 0:
                summary_output_path = job_output_dir / summary_filename_output
                with open(summary_output_path, 'w', encoding='utf-8') as f:
                    f.write(custom_summary)
                logger.info(f"Summary saved: {summary_output_path}")
            else:
                logger.error("Generated summary is empty, not saving")
                move_queued_to_errored(job_id)
                continue

            # Copy the original job YAML file to the job directory
            if job_yaml_path and job_yaml_path.exists():
                job_yaml_destination = job_output_dir / job_yaml_path.name
                import shutil
                shutil.copy2(job_yaml_path, job_yaml_destination)
                logger.info(f"Copied job YAML to: {job_yaml_destination}")

            # Note: Job is already moved to generated after AI content creation in modular system
            # For legacy generation, we need to move it here
            if not MODULAR_AVAILABLE or not get_config().is_modular_enabled():
                logger.info("Using legacy generation - moving job to generated directory")
                update_progress('running', f'Finalizing {current_job_name}...', i, total_jobs, current_job_name)
                move_queued_to_generated_with_validation(job_id)
            else:
                logger.info("Modular generation used - job already moved to generated directory")

            # ------------------------------------------------------------
            # Generate PDF files for resume and cover letter
            print_pdf(job_id)

            # No need to bundle since files are already in proper directory structure

            successful_jobs += 1
            logger.info(f"Successfully processed job {job_id} in directory {job_directory_name}")
            


        except Exception as e:
            failed_jobs += 1
            logger.error(f"Error processing job {job_id}: {str(e)}", exc_info=True)
            move_queued_to_errored(job_id)
            continue
    
    # Final progress update
    final_message = f"Completed processing: {successful_jobs} successful, {failed_jobs} failed out of {total_jobs} total jobs"
    logger.info(final_message)
    update_progress('completed', final_message, total_jobs, total_jobs)
    
    # Return exit code based on results
    if failed_jobs > 0:
        logger.error(f"Job processing completed with {failed_jobs} failures")
        return 1  # Error exit code
    else:
        logger.info("All jobs processed successfully")
        return 0  # Success exit code
    
    # Clean up progress file after a delay
    try:
        import threading
        def cleanup_progress():
            import time
            time.sleep(30)  # Keep progress visible for 30 seconds
            try:
                if progress_file.exists():
                    progress_file.unlink()
            except:
                pass
        
        cleanup_thread = threading.Thread(target=cleanup_progress)
        cleanup_thread.daemon = True
        cleanup_thread.start()
    except:
        pass
     
    


if __name__ == '__main__':
    import sys
    
    # Check if we should process a single job (from environment variable)
    single_job_id = os.getenv('RESUMEAI_SINGLE_JOB_ID')
    
    if single_job_id:
        logger.info(f"Processing single job with ID: {single_job_id}")
        exit_code = generate(id=single_job_id)
    else:
        # The bundling is already handled within the generate() function
        # No need to call bundle_to_directory here as it would create duplicates
        exit_code = generate()
    
    sys.exit(exit_code)
    
    