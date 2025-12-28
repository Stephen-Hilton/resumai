import os, re, yaml
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime



def load_resume_file(resume_file: Path | str = 'stephen') -> dict:
    """
    Loads the named "resume" file from the `src/resumes` directory, and returns the parsed YAML data as a dictionary.
    If the file is not found, returns None.

    Args:
        resume_file: a Path or string indicating a file in the `src/resumes/` folder.  If only a name is provided, `src/resumes/` is assumed.

    Returns: 
        dict: dictionary containing loaded YAML data.

    """
    # Convert to Path object and handle relative paths
    if isinstance(resume_file, str):
        if not resume_file.endswith('.yaml'):
            resume_file = f"{resume_file}.yaml"
        resume_path = Path(__file__).parent / 'resumes' / resume_file
    elif isinstance(resume_file, Path):
        resume_path = resume_file
    else: 
        raise ValueError(f"Parameter 'resume_file' must be type str or Path, you provided: {type(resume_file)}")
        
    # Check if file exists
    if not resume_path.exists():
        raise ValueError(f"Parameter 'resume_file' did not resolve to a resume file: {resume_path.resolve()}")
        
    # Load and parse YAML
    try:
        with open(resume_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Replace tabs with spaces to fix YAML parsing issues
            content = content.replace('\t', '  ')
            return yaml.safe_load(content)
    except Exception as e:
        print(f"Error loading resume file {resume_path}: {e}")
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
    jobs_dir = Path(__file__).parent / 'jobs'
    exclude_dirs = [d.name for d in jobs_dir.iterdir() if d.is_dir() and d.name != '1_queued']
    queued_dir = jobs_dir / '1_queued'
    
    if not queued_dir.exists(): 
        raise ValueError(f"Directory '1_queued' does not exist: {queued_dir.resolve()}")
    
    jobs = []
    processed_ids = set()
    
    # If not forcing, collect IDs from other directories to exclude
    if not force:
        for exclude_dir in exclude_dirs:
            exclude_path = jobs_dir / exclude_dir
            if exclude_path.exists():
                for file_path in exclude_path.glob('*.yaml'):
                    # Extract job ID from filename (format: timestamp.id.company.title.yaml)
                    filename_parts = file_path.stem.split('.')
                    if len(filename_parts) >= 2:
                        job_id = filename_parts[1]
                        processed_ids.add(job_id)
    
    # Load jobs from queued directory
    for yaml_file in queued_dir.glob('*.yaml'):
        try:
            # Extract job ID from filename
            filename_parts = yaml_file.stem.split('.')
            if len(filename_parts) >= 2:
                job_id = filename_parts[1]
                
                # Skip if already processed (unless forcing)
                if not force and job_id in processed_ids:
                    continue
            
            # Load the YAML file
            with open(yaml_file, 'r', encoding='utf-8') as f:
                job_data = yaml.safe_load(f)
                if job_data: jobs.append(job_data)
                    
        except Exception as e:
            print(f"Error loading job file {yaml_file}: {e}")
            continue
    
    return jobs 



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
                sections.append(f"- {contact['name']}: {contact['label']}")
    
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
    load_dotenv()
    llm_api_key = os.getenv("LLM_API_KEY")
    llm_model = os.getenv("LLM_MODEL")
    llm_provider = os.getenv("LLM_MODEL_PROVIDER")

    if not llm_api_key or not llm_model or not llm_provider:
        raise ValueError("LLM configuration missing. Please set LLM_API_KEY, LLM_MODEL, and LLM_MODEL_PROVIDER in your .env file")

    resume_str = structure_resume(resume)
    job_str = structure_job(job)

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

    prompt = f"""
    You are a helpful assistant that generates a custom resume, tailored to a job description.
    You are provided with a resume and a job description.
    
    Please create a customized HTML resume that highlights the most relevant experience, skills, and achievements from the candidate's background that align with the job requirements.
    
    Resume Guidelines:
    - Keep the same factual information - NEVER fabricate any information
    - You may select the most relevent information, and gently re-word for better clarity ONLY
    - Use the provided CSS classes for styling - DO NOT include inline styles or <style> tags
    - For icons, add this to the top of the html <head> section: 
        ```
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link rel="stylesheet" href="fonts.googleapis.com" />
        ```
    - There should be 7 sections to the resume:
      - Title and Contact section:
        - Create two columns, with the candidate's NAME on the left and stacked contact information on the right
        - The candidate name should be in 32pt font, and centered in it's column, both veritcally and horizontally
        - The contact information should be right-justified, black 8pt font 
        - Include all contact information in the yaml, in the same order
        - If a URL is included, always link the label (including <tel:> links)
        - If an `icon` is supplied, use that instead of the name
        - The contact information "icon" can be either:
          - A full http link to an icon image directly, or 
          - A Google material design logo name from https://fonts.google.com/icons
          - for example, 
            - if `icon: mobile_hand` then use the html:            
              '<span class="material-symbols-outlined">mobile_hand</span>'
            - if a full url is supplied, just plug in that, i.e.:
              `https://raw.githubusercontent.com/Stephen-Hilton/resumai/refs/heads/main/src/icons/globe-solid.svg`
      - Professional Experience section:
        - Tailor the summary/objective to the specific role, but do NOT fabricate any information
        - You have the most freedom to craft a targeted summary, but do NOT fabricate any information
        - Keep the total characters (including spaces) between 550 and 600
      - Selected Achievements for <job company name>:
        - Select the top 5 most relevent experiences, skills, and/or acheivements to highlight 
        - Unlike other sections, you will need to create this from scratch, using the rest of the resume.yaml information as a guide
        - Do NOT fabricate any skills or achievements, everything in this section must be justified somewhere else in the resume
        - Keep the total characters (including spaces) per line between 180 and 235
      - Core Skills section:
        - Select the top 12 most applicable skills to the provided job, from the resume yaml section provided
        - You can reword skills to adhere to the job, but do NOT fabricate any information
        - Keep the total character count (including spaces) to between 17 and 35 characters
      - Experience section: 
        - Experience section should be a 3 level hierarchy structure:
          - Employer Company information, including location, dates, and company description
          - each role worked at the above company, including title, location, and dates
          - bullet point list of responsibilities while in that position
        - Leave employment history in chronological order
        - You may reorder bullets inside of each role to highlight the most relevant information first
        - Emphasize relevant experience and skills that match the job requirements
        - You may omit bullets from the role that don't pertain to the job
        - Focus on achievements and quantifiable results where possible
      - Education // Awards & Speaking sections:
          - Make 2 columns at the bottom, the left for the Education section, the right for Awards & Speaking section
          - Remove any dates/years and institution names; keep the lines short and succinct  
          - Always include the same number of bullets between the two sections, so they use the same vertical space
      - Keep the overall resume to 2 pages total
    
    HTML Structure Requirements:
    - Use <link rel="stylesheet" href="../css/styles.css" /> in the head
    - Use non-rendering whitespace to make the HTML easier for direct human reading/editing
    - Use these CSS classes for styling:
      * both_body (for body tag)
      * both_container (main container div)
      * both_header (header section with flex layout)
      * both_header_left (left column for name)
      * both_header_right (right column for contact info)
      * both_h1 (main name heading - large font)
      * both_meta (contact info container)
      * both_meta_line (each contact info line)
      * both_section (each major section)
      * both_link (for links)
      * both_bold (for bold text)
      * both_muted (for muted text)
      * both_footer (footer section)
      * resume_h2 (section headings - dark blue)
      * resume_sub (job titles/company names)
      * resume_ul (unordered lists)
      * resume_li (list items)
      * resume_role_meta (job dates/location)
      * resume_skills (skills grid container)
      * resume_skills_column (each column in skills grid)
      * resume_skill_item (individual skill items - no pill styling)
      * resume_experience_item (each job experience)
      * resume_footer_availability (availability info)

    CANDIDATE RESUME:
    {resume_str}
    
    JOB DESCRIPTION:
    {job_str}
    
    ADDITIONAL USER INFORMATION:
    {additional_prompt if additional_prompt else "None."}
    
    Please generate a complete HTML resume that is tailored for this specific job opportunity using the specified CSS classes.
    """

    try:
        if llm_provider.lower() == "openai":
            import openai
            client = openai.OpenAI(api_key=llm_api_key)
            
            response = client.chat.completions.create(
                model=llm_model,
                messages=[
                    {"role": "system", "content": "You are a professional resume writer who creates tailored resumes in HTML format."},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=8000
            )
            
            return response.choices[0].message.content
            
        elif llm_provider.lower() == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=llm_api_key)
            
            response = client.messages.create(
                model=llm_model,
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}. Supported providers: openai, anthropic")
            
    except Exception as e:
        print(f"Error generating custom resume: {e}")
        return f"Error generating resume: {str(e)}"
    




def llm_generate_custom_coverletter(custom_resume:str, job:dict,  additional_prompt:str = None) -> str:
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
    load_dotenv()
    llm_api_key = os.getenv("LLM_API_KEY")
    llm_model = os.getenv("LLM_MODEL")
    llm_provider = os.getenv("LLM_MODEL_PROVIDER")

    if not llm_api_key or not llm_model or not llm_provider:
        raise ValueError("LLM configuration missing. Please set LLM_API_KEY, LLM_MODEL, and LLM_MODEL_PROVIDER in your .env file")
    
    job_str = structure_job(job)
    
    prompt = f"""
    You are a helpful assistant that generates a custom cover letter, tailored to match the tenor, style, and content of the supplied resume.
    You are provided with the resume html content, and the original job description.
    
    Please create a customized HTML cover letter that highlights the most relevant experience, skills, and achievements from the candidate's background that align with the job requirements.

    Cover Letter Guidelines:
    1. Use impactful introduction language that highlights the resume's fit for the job role
    2. Keep it short and professional, no more than 350 words total
    3. Use the provided CSS classes for styling - DO NOT include inline styles or <style> tags
    4. Include all contact information in a simple header, matching the resume
    5. As a small footer, include the line: `Generated by my ResumeAI project: https://github.com/Stephen-Hilton/ResumAI`
    
    HTML Structure Requirements:
    - Use <link rel="stylesheet" href="../css/styles.css" /> in the head
    - Use these CSS classes for styling:
      * both_body (for body tag)
      * both_container (main container div)
      * both_header (header section with flex layout)
      * both_header_left (left column for name)
      * both_header_right (right column for contact info)
      * both_h1 (main name heading - large font)
      * both_meta (contact info container)
      * both_meta_line (each contact info line)
      * both_section (each major section)
      * both_link (for links)
      * both_footer (footer section)
      * cover_p (paragraphs)
      * cover_ul (unordered lists)
      * cover_li (list items)
      * cover_sig (signature)
      * cover_subject (subject line)
      * cover_strengths_intro (intro to strengths list)
    
    CUSTOMIZED RESUME:
    ```
    {custom_resume}
    ```

    JOB DESCRIPTION:
    {job_str}
    
    ADDITIONAL USER INFORMATION:
    {additional_prompt if additional_prompt else "None."}
    
    Please generate a complete HTML cover letter that is tailored for this specific job opportunity using the specified CSS classes.
    """

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

    try:
        if llm_provider.lower() == "openai":
            import openai
            client = openai.OpenAI(api_key=llm_api_key)
            
            response = client.chat.completions.create(
                model=llm_model,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=8000
            )
            return response.choices[0].message.content
            
        elif llm_provider.lower() == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=llm_api_key)
            
            response = client.messages.create(
                model=llm_model,
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
            
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}. Supported providers: openai, anthropic")
            
    except Exception as e:
        print(f"Error generating custom resume: {e}")
        return f"Error generating resume: {str(e)}"
 



def generate(force:bool=False):
    """
    Main function to demonstrate the functionality of the jobs_2_generate module.
    Loads resume and jobs, then generates custom resumes and cover letters for each job.
    """
    # Load resume
    print("Loading resume...")
    resume = load_resume_file('Stephen_Hilton')
    if not resume:
        print("Failed to load resume file")
        return
    
    print(f"Loaded resume for: {resume.get('name', 'Unknown')}")
    
    # Load queued jobs
    print("\nLoading queued jobs...")
    jobs = load_queued_jobs(force=force)
    print(f"Found {len(jobs)} jobs to process")
    
    if not jobs:
        print("No jobs found to process")
        return
    
    # Create output directory
    jobs_dir = Path(__file__).parent / 'jobs' / '2_generated'
    jobs_dir.mkdir(exist_ok=True)
    
    # Get resume filename for output naming
    resume_filename = 'Stephen_Hilton'
    
    # Process each job
    for i, job in enumerate(jobs):
        job_title = job.get('title', 'Unknown')
        job_company = job.get('company', 'Unknown')
        job_id = job.get('id', f'job_{i}')
        
        print(f"\nProcessing job {i+1}/{len(jobs)}: {job_title} at {job_company}")
        
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
                print(f"  Warning: Could not find timestamp for job {job_id}, using current time")
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # Generate custom resume
            print(f"  Generating custom resume...  ", end='')
            custom_resume = llm_generate_custom_resume(resume, job)
            print(f" Length {len(custom_resume)}")

            # Generate custom cover letter
            print(f"  Generating custom cover letter...  ", end='')
            custom_coverletter = llm_generate_custom_coverletter(custom_resume, job)
            print(f" Length {len(custom_resume)}")

            # Create output filenames
            resume_filename_output = f"{timestamp}.{job_id}.{resume_filename}.resume.html"
            coverletter_filename_output = f"{timestamp}.{job_id}.{resume_filename}.coverletter.html"
            
            # Save resume
            resume_output_path = jobs_dir / resume_filename_output
            if len(custom_resume) >0:
                with open(resume_output_path, 'w', encoding='utf-8') as f:
                    f.write(custom_resume)
                print(f"  Resume saved: {resume_output_path}")
            
            # Save cover letter
            coverletter_output_path = jobs_dir / coverletter_filename_output
            if len(custom_coverletter) >0:
                with open(coverletter_output_path, 'w', encoding='utf-8') as f:
                    f.write(custom_coverletter)
                print(f"  Cover letter saved: {coverletter_output_path}")

            
        except Exception as e:
            print(f"  Error processing job {job_id}: {e}")
            continue
    
    print(f"\nCompleted processing {len(jobs)} jobs!")
     
    


if __name__ == '__main__':
    generate(force=True)
    pass