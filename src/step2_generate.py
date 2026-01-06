import os, re, yaml, logging, sys
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import logging_setup

# Set up logger for this module
logger = logging_setup.get_logger(__name__)

def force_flush_logs():
    """Force flush all logging handlers and stdout to ensure immediate output"""
    return logging_setup.force_flush_logs()



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



def load_queued_jobs(force:bool = False) -> list[dict]:
    """
    Loads all jobs from the `src/jobs/1_queued` directory, and returns them as a list of dictionaries.
    Excludes any that appear in any other `src/jobs/*` folder, unless force=True, in which case
    older generation work is simply overwritten.

    Args:
        force (bool, optional): Ignores previous run exclusion logic, and forces a new run.

    Returns:
        list[dict]: list of dictionaries, each representing a job.
    """
    logger.info(f"Loading queued jobs (force={force})")
    
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
                for file_path in exclude_path.glob('*.yaml'):
                    # Extract job ID from filename (format: timestamp.id.company.title.yaml)
                    filename_parts = file_path.stem.split('.')
                    if len(filename_parts) >= 2:
                        job_id = filename_parts[1]
                        processed_ids.add(job_id)
        logger.info(f"Found {len(processed_ids)} previously processed job IDs")
    
    # Load jobs from queued directory
    queued_files = list(queued_dir.glob('*.yaml'))
    logger.info(f"Found {len(queued_files)} queued job files")
    
    for yaml_file in queued_files:
        try:
            # Extract job ID from filename
            filename_parts = yaml_file.stem.split('.')
            if len(filename_parts) >= 2:
                job_id = filename_parts[1]
                
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
                    
        except Exception as e:
            logger.error(f"Error loading job file {yaml_file}: {str(e)}", exc_info=True)
            continue
    
    logger.info(f"Successfully loaded {len(jobs)} jobs for processing")
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
                    contact_line += f" (Icon: {contact['icon']})"
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



def llm_call(llm_provider:str=None, llm_model:str=None, llm_api_key:str=None, sys_prompt:str=None, user_prompt:str=None) -> str:
    """
    Executes supplied prompts against the supplied LLM, and returns string response. 

    Args: 
        llm_provider (str): The company or model provider, i.e., OpenAI, Anthropic, etc.
        llm_model (str): The specific LLM model, i.e., gpt-5-mini, etc.
        llm_api_key (str): The API key that authorizes the request
        sys_prompt (str): System prompt for the request
        user_prompt (str): User prompt for the request
    """
    load_dotenv()
    llm_provider = llm_provider if llm_provider else os.getenv("LLM_MODEL_PROVIDER")
    llm_model    = llm_model if llm_model else os.getenv("LLM_MODEL")
    llm_api_key  = llm_api_key if llm_api_key else os.getenv("LLM_API_KEY")

    logger.info(f"Making LLM call to {llm_provider}/{llm_model}")
    
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
            client = openai.OpenAI(api_key=llm_api_key)
            
            response = client.chat.completions.create(
                model=llm_model,
                max_completion_tokens=32000,
                messages=messages
            )
            result = response.choices[0].message.content
            logger.info(f"LLM response received: {len(result)} characters")
            
            # Force flush after LLM response
            force_flush_logs()
            
            return result
            
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

    resume_str = structure_resume(resume)
    job_str = structure_job(job)
    with open( Path(__file__).parent / 'jobs' / 'templates' / 'example.resume.html') as fh:
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
- Keep all factual information accurate - NEVER fabricate details
- Select and emphasize the most relevant experience, skills, and achievements for this role
- Reword for clarity when needed, but maintain factual accuracy
- Follow the structure and CSS classes shown in the example template
- **IMPORTANT**: Keep all bullet points under 290 characters to ensure they fit within 2 lines and avoid orphaned words

KEY SECTIONS TO CUSTOMIZE:
1. **Professional Summary**: 2-3 sentences (550-600 characters) tailored to this specific role
2. **Selected Achievements**: Create 5 achievement bullets (305-350 characters each) that best demonstrate fit for this role - must be based on actual resume content. Keep bullets concise to avoid orphaned words on third lines.
3. **Core Skills**: Select 12 most relevant skills from resume, arranged in 3 columns of 4 each. Each skill must be at least 20 characters long to ensure proper formatting and avoid awkward whitespace. Combine related short skills if needed (e.g., "AWS" becomes "AWS cloud services", "SQL" becomes "SQL database management").
4. **Experience**: Prioritize and reorder bullets within each role to highlight job-relevant accomplishments first. Keep each bullet under 250 characters to ensure clean 2-line formatting.
   - Company name line: ONLY the company name (no descriptions or extra text)
   - Company description line: Brief description WITHOUT "Company:" prefix
   - Follow the exact 3-level hierarchy shown in the example template
   - Display companies / roles in the order they appear in the YAML file
5. **Education/Awards**: Include same number of items in each column for balanced layout

STRUCTURE REQUIREMENTS:
- Use the exact HTML structure from the example template
- **IMPORTANT**: Change the CSS link from "../css/styles.css" to "../../css/styles.css" (files will be in subdirectories)
- Include all contact information with proper icons (Material Icons for single words, direct images for URLs)
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
- Use the same CSS classes and structure as the resume
- **IMPORTANT**: Use CSS link "../../css/styles.css" (files will be in subdirectories)
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
    `src/jobs/1_queued/{id}*` or `src/jobs/2_generated/{id}*` over to `src/jobs/8_errors/`. 
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
        
        # Check queued directory
        if queued_dir.exists():
            queued_files = list(queued_dir.glob(pattern))
            matching_files.extend([(f, 'queued') for f in queued_files])
            
        # Check generated directory
        if generated_dir.exists():
            generated_files = list(generated_dir.glob(pattern))
            matching_files.extend([(f, 'generated') for f in generated_files])
        
        if not matching_files:
            logger.warning(f"No files found matching pattern {pattern} in queued or generated directories")
            return False
        
        logger.info(f"Found {len(matching_files)} files to move to errors directory for job ID {id}")
        
        # Move each matching file
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
        
        if moved_count > 0:
            logger.info(f"Successfully moved {moved_count} files to errors directory for job ID {id}")
            return True
        else:
            logger.error(f"Failed to move any files to errors directory for job ID {id}")
            return False
            
    except Exception as e:
        logger.error(f"Error in move_queued_to_errored for job ID {id}: {str(e)}", exc_info=True)
        return False


def move_queued_to_generated(id:str) -> bool:
    """
    Accepts an id that has completed generation, then moves all files in
    `src/jobs/1_queued/{id}*` over to `src/jobs/2_generated/`. 
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
        
        # Find all files matching the job ID pattern
        pattern = f"*.{id}.*"
        matching_files = list(queued_dir.glob(pattern))
        
        if not matching_files:
            logger.warning(f"No files found matching pattern {pattern} in {queued_dir}")
            return False
        
        logger.info(f"Found {len(matching_files)} files to move for job ID {id}")
        
        # Move each matching file
        moved_count = 0
        for file_path in matching_files:
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
            logger.info(f"Successfully moved {moved_count} files for job ID {id}")
            return True
        else:
            logger.error(f"Failed to move any files for job ID {id}")
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
    from pdf_mgr import print_pdf as pdf_print_pdf
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
            
            # Sanitize strings for directory name (remove/replace invalid characters)
            def sanitize_filename(text):
                # Replace problematic characters with underscores
                sanitized = re.sub(r'[<>:"/\\|?*]', '_', text)
                # Replace spaces and multiple underscores with single underscore
                sanitized = re.sub(r'[\s_]+', '_', sanitized)
                # Remove leading/trailing underscores and limit length
                return sanitized.strip('_')[:50]
            
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
    
    # Load resume
    logger.info("Loading resume...")
    try:
        resume = load_resume_file('Stephen_Hilton')
        if not resume:
            logger.error("Failed to load resume file")
            return
        
        logger.info(f"Loaded resume for: {resume.get('name', 'Unknown')}")
    except Exception as e:
        logger.error(f"Error loading resume: {str(e)}", exc_info=True)
        return
    
    # Load queued jobs
    logger.info("Loading queued jobs...")
    try:
        jobs = load_queued_jobs(force=force)
        if id: 
            logger.info(f"Generating for specified ID: {id}")
            jobs = [j for j in jobs if j['id']==id]
        logger.info(f"Found {len(jobs)} jobs to process")
        
        if not jobs:
            logger.warning("No jobs found to process")
            return
    except Exception as e:
        logger.error(f"Error loading jobs: {str(e)}", exc_info=True)
        return
    
    # Create output directory
    jobs_dir = Path(__file__).parent / 'jobs' / '2_generated'
    jobs_dir.mkdir(exist_ok=True)
    logger.info(f"Output directory: {jobs_dir}")
    
    # Get resume filename for output naming
    resume_filename = resume.get('name', '').replace(' ','_')
    if not resume_filename: 
        logger.error("Resume file missing 'name' key")
        raise ValueError(f"Supplied src/resumes/YourName.yaml file did not include a 'name' key, please double-check the yaml file structure and try again.")
    
    # Process each job
    successful_jobs = 0
    failed_jobs = 0
    
    for i, job in enumerate(jobs):
        job_title = job.get('title', 'Unknown')
        job_company = job.get('company', 'Unknown')
        job_id = job.get('id', f'job_{i}')
        
        logger.info(f"Processing job {i+1}/{len(jobs)}: {job_title} at {job_company} (ID: {job_id})")
        
        try:
            # Find the original queued file to extract timestamp
            queued_dir = Path(__file__).parent / 'jobs' / '1_queued'
            timestamp = None
            
            # Look for the matching job file by ID
            for queued_file in queued_dir.glob('*.yaml'):
                filename_parts = queued_file.stem.split('.')
                if len(filename_parts) >= 2 and filename_parts[1] == job_id:
                    timestamp = filename_parts[0]
                    break
            
            if not timestamp:
                logger.warning(f"Could not find timestamp for job {job_id}, using current time")
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # ------------------------------------------------------------
            # Generate custom resume
            logger.info("Generating custom resume...")
            force_flush_logs()
            custom_resume = llm_generate_custom_resume(resume, job, additional_prompt)
            logger.info(f"Generated resume length: {len(custom_resume)} characters")
            force_flush_logs()
            
            # Save resume
            resume_filename_output = f"{timestamp}.{job_id}.{resume_filename}.resume.html"
            if len(custom_resume) > 0:
                resume_output_path = jobs_dir / resume_filename_output
                with open(resume_output_path, 'w', encoding='utf-8') as f:
                    f.write(custom_resume)
                logger.info(f"Resume saved: {resume_output_path.name}")
            else:
                logger.error("Generated resume is empty, not saving")
                move_queued_to_errored(job_id)
                continue


            # ------------------------------------------------------------
            # Generate custom cover letter
            logger.info("Generating custom cover letter...")
            force_flush_logs()
            custom_coverletter = llm_generate_custom_coverletter(resume, job, custom_resume, additional_prompt)
            logger.info(f"Generated cover letter length: {len(custom_coverletter)} characters")
            force_flush_logs()

            # Save cover letter
            coverletter_filename_output = f"{timestamp}.{job_id}.{resume_filename}.coverletter.html"
            if len(custom_coverletter) > 0:
                coverletter_output_path = jobs_dir / coverletter_filename_output
                with open(coverletter_output_path, 'w', encoding='utf-8') as f:
                    f.write(custom_coverletter)
                logger.info(f"Cover letter saved: {coverletter_output_path.name}")
            else:
                logger.error("Generated cover letter is empty, not saving")
                move_queued_to_errored(job_id)
                continue


            # ------------------------------------------------------------
            # Generate job summary
            logger.info("Generating job summary...")
            force_flush_logs()
            custom_summary = llm_generate_job_summary(job)
            logger.info(f"Generated summary length: {len(custom_summary)} characters")
            force_flush_logs()

            # Save summary
            summary_filename_output = f"{timestamp}.{job_id}.{resume_filename}.!SUMMARY.html"
            if len(custom_summary) > 0:
                summary_output_path = jobs_dir / summary_filename_output
                with open(summary_output_path, 'w', encoding='utf-8') as f:
                    f.write(custom_summary)
                logger.info(f"Summary saved: {summary_output_path.name}")
            else:
                logger.error("Generated summary is empty, not saving")
                move_queued_to_errored(job_id)
                continue

            # move all queued files to generated, to keep everything together.
            move_queued_to_generated(job_id)

            # ------------------------------------------------------------
            # Generate PDF files for resume and cover letter
            print_pdf(job_id)

            # bundle to a directory for easier navigation.
            bundle_to_directory(job_id)

            successful_jobs += 1
            logger.info(f"Successfully processed job {job_id}")
            


        except Exception as e:
            failed_jobs += 1
            logger.error(f"Error processing job {job_id}: {str(e)}", exc_info=True)
            move_queued_to_errored(job_id)
            continue
    


    logger.info(f"Completed processing: {successful_jobs} successful, {failed_jobs} failed out of {len(jobs)} total jobs")
     
    


if __name__ == '__main__':
    # The bundling is already handled within the generate() function
    # No need to call bundle_to_directory here as it would create duplicates
    generate()
    
    