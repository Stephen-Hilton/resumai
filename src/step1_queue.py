import os, re, yaml, requests, logging, unicodedata
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from utils import gmail_mgr
from utils import parse_linkedin_emails
from utils import logging_setup

# Set up logger for this module
logger = logging_setup.get_logger(__name__)



def sanitize_text_for_yaml(text):
    """
    Sanitize text content to remove problematic characters that can cause YAML parsing issues.
    
    Args:
        text (str): Input text to sanitize
        
    Returns:
        str: Sanitized text safe for YAML processing
    """
    if not isinstance(text, str):
        return text
    
    # Step 1: Normalize Unicode characters (decompose and recompose)
    text = unicodedata.normalize('NFKC', text)
    
    # Step 2: Remove or replace problematic Unicode categories
    # Remove control characters (except newlines, tabs, carriage returns)
    text = ''.join(char for char in text if unicodedata.category(char) not in ['Cc'] or char in ['\n', '\t', '\r'])
    
    # Step 3: Remove specific problematic characters that can break YAML
    # Remove zero-width characters
    text = re.sub(r'[\u200b-\u200f\u2028-\u202f\u205f-\u206f\ufeff]', '', text)
    
    # Step 4: Replace smart quotes and similar characters with ASCII equivalents
    replacements = {
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
        '\u2026': '...',  # Horizontal ellipsis
        '\u00a0': ' ',  # Non-breaking space
        '\u00ad': '',   # Soft hyphen
    }
    
    for old_char, new_char in replacements.items():
        text = text.replace(old_char, new_char)
    
    # Step 5: Remove any remaining non-printable characters except common whitespace
    text = ''.join(char for char in text if char.isprintable() or char in ['\n', '\t', '\r', ' '])
    
    # Step 6: Clean up excessive whitespace
    # Replace multiple consecutive spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple consecutive newlines with maximum of 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def sanitize_job_data(job_data):
    """
    Recursively sanitize all string values in a job data dictionary.
    
    Args:
        job_data (dict): Job data dictionary to sanitize
        
    Returns:
        dict: Sanitized job data dictionary
    """
    if isinstance(job_data, dict):
        return {key: sanitize_job_data(value) for key, value in job_data.items()}
    elif isinstance(job_data, list):
        return [sanitize_job_data(item) for item in job_data]
    elif isinstance(job_data, str):
        return sanitize_text_for_yaml(job_data)
    else:
        return job_data



# helper to force YAML literal block for specific strings
# ------------------------------------------------------
# Purpose: LiteralStr is a tiny subclass of str used only to tag specific string values so the YAML dumper can treat them differently.
# How it’s used: we register a YAML representer for LiteralStr that emits that value with style '|' (block literal). 
# Wrapping job['job_description'] = LiteralStr(text) makes that one field produce a multi-line literal in the YAML output 
# while leaving all other strings unchanged.
class LiteralStr(str):
    pass

def _literal_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

yaml.SafeDumper.add_representer(LiteralStr, _literal_representer)
# ------------------------------------------------------



def get_all_ids(job_path:Path = None) -> list:
    """
    Recursively iterate thru the supplied job_path and collect a unique list of
    all IDs found in any html or yaml file.  The ID is always the second element of
    the filename, delimited by period (.), of 4 elements.
    Now handles both flat files and subfolder structures.

    Args:
        job_path (Path): Path object to recursively iterate over, looking for any yaml or html files. 

    Returns: 
        list: unique list of all IDs found. 
    """
    if not job_path: job_path = Path('src/jobs/')

    logger.debug(f"Scanning for IDs in: {job_path}")
    
    if not job_path.exists():
        logger.warning(f"Path does not exist: {job_path}")
        return []
    
    ids = set()  # Use set to automatically handle uniqueness
    
    try:
        # Recursively find all .yaml and .html files (handles both flat files and subfolders)
        for file_path in job_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.yaml', '.html']:
                # Split filename by periods
                filename_parts = file_path.stem.split('.')
                
                # Check if filename has exactly 4 parts (timestamp.id.company.title)
                if len(filename_parts) == 4:
                    # Extract the ID (second element, index 1)
                    job_id = filename_parts[1]
                    ids.add(job_id)
                    logger.debug(f"Found ID {job_id} in file: {file_path.name}")
                else:
                    logger.debug(f"Skipping file with unexpected format: {file_path.name}")
    
    except Exception as e:
        logger.error(f"Error scanning directory {job_path}: {str(e)}", exc_info=True)
        return []
    
    unique_ids = sorted(list(ids))  # Convert to sorted list
    logger.info(f"Found {len(unique_ids)} unique IDs in {job_path}")
    
    return unique_ids 



def load(gmail_address:str = None, gmail_app_password:str = None):
    logger.info("Starting job queue loading process")
    
    # Gmail credentials
    load_dotenv()
    if not gmail_address: gmail_address = os.getenv('GMAIL_ADDRESS')
    if not gmail_app_password: gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not gmail_address or not gmail_app_password:
        logger.error("Gmail credentials not provided")
        raise ValueError("Gmail credentials required")
        
    logger.info(f"Using Gmail address: {gmail_address}")
    
    job_files = Path(__file__).parent / 'jobs'

    # Retrieve recent LinkedIn job alert emails
    # -------------------------------------------------------------
    logger.info("Retrieving LinkedIn job alert emails")
    try:
        emails = gmail_mgr.get_gmails(
            gmail_address,
            gmail_app_password,
            sender_filters=['LinkedIn Job Alerts'],
            unread_only=False,
            mark_as_read=False,
            max_results=5
        )
        logger.info(f"Retrieved {len(emails)} emails")
    except Exception as e:
        logger.error(f"Error retrieving emails: {str(e)}", exc_info=True)
        return

    # Parse emails to extract job listings
    # -------------------------------------------------------------
    logger.info("Parsing emails to extract job listings")
    try:
        jobs = parse_linkedin_emails.parse_emails_to_jobs(emails)
        logger.info(f"Parsed {len(jobs)} jobs from {len(emails)} emails")
    except Exception as e:
        logger.error(f"Error parsing emails: {str(e)}", exc_info=True)
        return
    
    file_count = 0

    # collect all existing IDs
    existing_ids = get_all_ids()


    # For each job, fetch linkedin page html and parse job details
    for i, job in enumerate(jobs):
        link = job.get('link', None)
        id = job.get('id', None)
        title = job.get('title', None)
        company = job.get('company', None)
        logger.info(f"Processing job {i+1}/{len(jobs)}: {title} at {company} (ID: {id})")

        if id in existing_ids: 
            logger.info(f"    SKIPPING: ID {id} already exists")
            continue
        
        if not link or not id or not title: 
            logger.warning(f"    SKIPPING: job with missing data: link={bool(link)}, id={bool(id)}, title={bool(title)}")
            continue

        # open public webpage (no access token needed) and collect JD html
        logger.debug(f"Fetching job description from: {link}")
        try:
            response = requests.get(job.get('link'), headers={})
            if response.status_code != 200: 
                logger.warning(f"Failed to fetch job page: HTTP {response.status_code}")
                continue
        except Exception as e:
            logger.error(f"Error fetching job page: {str(e)}")
            continue

        # try to get the Job Description, if possible:
        try:
            jd = parse_linkedin_emails.parse_job_description(response.text)
            # Sanitize the job description before wrapping in LiteralStr
            jd_sanitized = sanitize_text_for_yaml(jd.strip() or '')
            job['description'] = LiteralStr(jd_sanitized)
            logger.debug(f"Extracted job description: {len(jd_sanitized)} characters")
        except Exception as e:
            logger.error(f"Error parsing job description: {str(e)}")
            job['description'] = LiteralStr('')

        # Sanitize all job data before saving
        job_sanitized = sanitize_job_data(job)
        
        # set processing time, so all files have same timestamp
        proctime = datetime.fromisoformat(job_sanitized.get('date_received')).strftime("%Y%m%d%H%M%S")

        # sanitize company/title for safe filenames
        def _sanitize_fn(s: str) -> str:
            if not s:
                return 'NA'
            # First apply text sanitization
            s = sanitize_text_for_yaml(s)
            # replace path separators, dots and other unsafe chars with underscores
            out = re.sub(r'[\\/:*?"<>|.]+', '_', s)
            # also replace control chars and other non-printables (disallow dot)
            out = re.sub(r'[^\w\- ]+', '_', out)
            # collapse whitespace to single space
            out = re.sub(r'\s+', ' ', out).strip()
            out = out.replace(' _ ', ' ')
            # limit length
            return out[:200]

        company = _sanitize_fn(company)
        title = _sanitize_fn(title)

        # Create subfolder for this job in queued directory
        # Format: Company.Position.id.timestamp
        subfolder_name = f"{company}.{title}.{id}.{proctime}"
        job_subfolder = job_files / '1_queued' / subfolder_name
        job_subfolder.mkdir(exist_ok=True)
        
        logger.info(f"Created job subfolder: {job_subfolder}")

        # Save files in the subfolder
        with open(job_subfolder / f'{proctime}.{id}.{company}.{title}.yaml', 'w', encoding='utf-8') as f:
            yaml.safe_dump(job_sanitized, f, sort_keys=False, allow_unicode=True)
            file_count += 1

        with open(job_subfolder / f'{proctime}.{id}.{company}.{title}.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
            file_count += 1
    
    print(f'Parsed {len(jobs)} jobs from {len(emails)} emails, and saved to {file_count} files.')
    return None



if __name__ == '__main__': 
    load()
    pass