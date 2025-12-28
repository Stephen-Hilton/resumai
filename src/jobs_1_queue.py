import os, re, yaml, requests
from pathlib import Path
from datetime import datetime
import gmail_mgr
import parse_linkedin_emails



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



def load(gmail_address:str = None, gmail_app_password:str = None):

    # Gmail credentials
    if not gmail_address: gmail_address = os.getenv('GMAIL_ADDRESS')
    if not gmail_app_password: gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')
    job_files = Path(__file__).parent / 'jobs'

    # Retrieve recent LinkedIn job alert emails
    # -------------------------------------------------------------
    emails = gmail_mgr.get_gmails(
        gmail_address,
        gmail_app_password,
        sender_filters=['LinkedIn Job Alerts'],
        unread_only=False,
        mark_as_read=False,
        max_results=5
    )

    # Parse emails to extract job listings
    # -------------------------------------------------------------
    jobs = parse_linkedin_emails.parse_emails_to_jobs(emails)
    file_count = 0

    print(f'Parsed {len(jobs)} jobs from {len(emails)} emails.')
 
    # For each job, fetch linkedin page html and parse job details
    for job in jobs:
        link = job.get('link', None)
        id = job.get('id', None)
        title = job.get('title', None)
        company = job.get('company', None)
        if not link or not id or not title: continue
         
        # look to see if we've already processed this id:
        found = list(job_files.rglob(f'**/{id}.*')) # anywhere in `src/jobs/*`
        if found: continue

        # open public webpage (no access token needed) and collect JD html
        response = requests.get(job.get('link'), headers={})
        if response.status_code != 200: continue

        # try to get the Job Description, if possible:
        jd = parse_linkedin_emails.parse_job_description(response.text)
        job['description'] = LiteralStr(jd.strip() or '')

        # set processing time, so all files have same timestamp
        proctime = datetime.fromisoformat(job.get('date_received')).strftime("%Y%m%d%H%M%S")

        # sanitize company/title for safe filenames
        def _sanitize_fn(s: str) -> str:
            if not s:
                return 'NA'
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

        with open(job_files / '1_queued' / f'{proctime}.{id}.{company}.{title}.yaml', 'w', encoding='utf-8') as f:
            yaml.safe_dump(job, f, sort_keys=False, allow_unicode=True)
            file_count += 1

        with open(job_files / '1_queued' / f'{proctime}.{id}.{company}.{title}.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
            file_count += 1
    
    print(f'Parsed {len(jobs)} jobs from {len(emails)} emails, and saved to {file_count} files.')
    return None


