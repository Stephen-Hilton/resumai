"""
Job Create Gmail Lambda Handler

Creates jobs by fetching LinkedIn Job Alert emails from Gmail.

Requirements: 5.1
"""
import json
import os
import re
import sys
from datetime import datetime
from typing import List, Dict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    import uuid7
except ImportError:
    import uuid
    class uuid7:
        @staticmethod
        def uuid7():
            return uuid.uuid4()

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    import base64
    from bs4 import BeautifulSoup
    HAS_GMAIL = True
except ImportError:
    HAS_GMAIL = False

from shared.response import api_response, bad_request, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import make_safe_url_segment, VALID_SUBCOMPONENTS


def get_default_generation_types(db: DynamoDBClient, userid: str) -> dict:
    """Get user's default generation types for all subcomponents."""
    prefs = db.get_user_prefs(userid)
    defaults = {}
    for component in VALID_SUBCOMPONENTS:
        pref_name = f"default_gen_{component}"
        defaults[component] = prefs.get(pref_name, 'ai')
    return defaults


def get_gmail_service(refresh_token: str):
    """Create Gmail API service using refresh token."""
    if not HAS_GMAIL:
        raise ImportError("google-api-python-client required for Gmail integration")
    
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError("Google OAuth credentials not configured")
    
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret,
        scopes=['https://www.googleapis.com/auth/gmail.readonly']
    )
    
    return build('gmail', 'v1', credentials=creds)


def extract_jobs_from_linkedin_email(message_data: dict) -> List[Dict]:
    """
    Extract job listings from a LinkedIn Job Alert email.
    
    Returns list of dicts with: jobcompany, jobtitle, jobdesc, joblocation, joburl
    """
    jobs = []
    
    # Get email body
    payload = message_data.get('payload', {})
    body_data = None
    
    # Check for multipart message
    parts = payload.get('parts', [])
    for part in parts:
        if part.get('mimeType') == 'text/html':
            body_data = part.get('body', {}).get('data')
            break
    
    # Fallback to direct body
    if not body_data:
        body_data = payload.get('body', {}).get('data')
    
    if not body_data:
        return jobs
    
    # Decode base64 body
    html_content = base64.urlsafe_b64decode(body_data).decode('utf-8')
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # LinkedIn Job Alert emails have job cards with specific structure
    # Look for job listing patterns
    job_cards = soup.select('[class*="job"], [class*="Job"], .entity-result')
    
    if not job_cards:
        # Try alternative selectors for LinkedIn emails
        job_cards = soup.select('table tr, .job-card, [data-job-id]')
    
    for card in job_cards[:20]:  # Limit to 20 jobs per email
        job = {
            'jobcompany': '',
            'jobtitle': '',
            'jobdesc': '',
            'joblocation': '',
            'joburl': ''
        }
        
        # Extract job title
        title_elem = card.select_one('a[href*="linkedin.com/jobs"], h3, h4, .job-title, [class*="title"]')
        if title_elem:
            job['jobtitle'] = title_elem.get_text(strip=True)[:200]
            # Extract URL if available
            if title_elem.name == 'a':
                job['joburl'] = title_elem.get('href', '')
            else:
                link = card.select_one('a[href*="linkedin.com/jobs"]')
                if link:
                    job['joburl'] = link.get('href', '')
        
        # Extract company name
        company_elem = card.select_one('.company, [class*="company"], [class*="Company"], .subtitle')
        if company_elem:
            job['jobcompany'] = company_elem.get_text(strip=True)[:100]
        
        # Extract location
        location_elem = card.select_one('.location, [class*="location"], [class*="Location"]')
        if location_elem:
            job['joblocation'] = location_elem.get_text(strip=True)[:100]
        
        # Only add if we have at least title and company
        if job['jobtitle'] and job['jobcompany']:
            jobs.append(job)
    
    return jobs


def fetch_linkedin_job_alerts(service, max_results: int = 50) -> List[Dict]:
    """
    Fetch LinkedIn Job Alert emails and extract job listings.
    
    Returns list of job dicts.
    """
    all_jobs = []
    
    # Search for LinkedIn Job Alert emails
    query = 'from:jobs-noreply@linkedin.com subject:"job alert" newer_than:7d'
    
    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()
    
    messages = results.get('messages', [])
    
    for msg in messages:
        try:
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            jobs = extract_jobs_from_linkedin_email(message)
            all_jobs.extend(jobs)
            
        except Exception as e:
            print(f"Error processing message {msg['id']}: {e}")
            continue
    
    return all_jobs


def handler(event, context):
    """
    Create jobs from LinkedIn Job Alert emails in Gmail.
    
    Request body:
    {
        "resumeid": "string" (resume name to use for all jobs)
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
        resumeid = body.get('resumeid')
        
        if not resumeid:
            return bad_request("resumeid is required")
        
        db = DynamoDBClient()
        
        # Verify resume exists
        resume = db.get_resume(userid, resumeid)
        if not resume:
            return bad_request(f"Resume '{resumeid}' not found")
        
        # Get user record to check Gmail connection
        user = db.get_user(userid)
        if not user:
            return bad_request("User not found")
        
        if not user.get('gmailConnected'):
            return bad_request("Gmail not connected. Please connect Gmail first.")
        
        refresh_token = user.get('gmailRefreshToken')
        if not refresh_token:
            return bad_request("Gmail refresh token not found. Please reconnect Gmail.")
        
        # Fetch jobs from Gmail
        try:
            service = get_gmail_service(refresh_token)
            extracted_jobs = fetch_linkedin_job_alerts(service)
        except Exception as e:
            print(f"Gmail API error: {e}")
            return bad_request(f"Failed to fetch emails from Gmail: {str(e)}")
        
        if not extracted_jobs:
            return api_response(200, {
                'message': 'No new job alerts found in Gmail',
                'jobs': [],
                'count': 0
            })
        
        # Get user's default generation types
        gen_types = get_default_generation_types(db, userid)
        
        created_jobs = []
        
        for job_data in extracted_jobs:
            try:
                # Generate job ID
                jobid = str(uuid7.uuid7())
                
                # Create safe URL segment for job title
                jobtitlesafe = make_safe_url_segment(job_data['jobtitle'])
                
                # Create JOB record
                job_record = {
                    'jobid': jobid,
                    'postedts': datetime.utcnow().isoformat(),
                    'jobcompany': job_data['jobcompany'],
                    'jobtitle': job_data['jobtitle'],
                    'jobtitlesafe': jobtitlesafe,
                    'jobdesc': job_data.get('jobdesc', ''),
                    'joblocation': job_data.get('joblocation', ''),
                    'jobsalary': '',
                    'jobposteddate': datetime.utcnow().strftime('%Y-%m-%d'),
                    'joburl': job_data.get('joburl', ''),
                    'jobcompanylogo': '',
                    'jobtags': ['LinkedIn'],
                }
                
                created_job = db.create_job(job_record)
                
                # Determine initial phase - Search since we don't have full description
                initial_phase = 'Search'
                
                # Create USER_JOB record
                user_job_data = {
                    'userid': userid,
                    'jobid': jobid,
                    'resumeid': resumeid,
                    'jobphase': initial_phase,
                    
                    # Subcomponent data (empty initially)
                    'datacontact': '',
                    'datasummary': '',
                    'dataskills': '',
                    'datahighlights': '',
                    'dataexperience': '',
                    'dataeducation': '',
                    'dataawards': '',
                    'datacoverletter': '',
                    
                    # Generation states (all start as "ready")
                    'statecontact': 'ready',
                    'statesummary': 'ready',
                    'stateskills': 'ready',
                    'statehighlights': 'ready',
                    'stateexperience': 'ready',
                    'stateeducation': 'ready',
                    'stateawards': 'ready',
                    'statecoverletter': 'ready',
                    
                    # Generation types (from user preferences)
                    'typecontact': gen_types['contact'],
                    'typesummary': gen_types['summary'],
                    'typeskills': gen_types['skills'],
                    'typehighlights': gen_types['highlights'],
                    'typeexperience': gen_types['experience'],
                    'typeeducation': gen_types['education'],
                    'typeawards': gen_types['awards'],
                    'typecoverletter': gen_types['coverletter'],
                    
                    # Final file locations (empty initially)
                    's3locresumehtml': '',
                    's3locresumepdf': '',
                    's3loccoverletterhtml': '',
                    's3loccoverletterpdf': '',
                }
                
                created_user_job = db.create_user_job(user_job_data)
                
                created_jobs.append({
                    'job': created_job,
                    'userJob': created_user_job
                })
                
            except Exception as e:
                print(f"Error creating job {job_data.get('jobtitle')}: {e}")
                continue
        
        return api_response(201, {
            'message': f'Created {len(created_jobs)} jobs from Gmail',
            'jobs': created_jobs,
            'count': len(created_jobs)
        })
        
    except json.JSONDecodeError:
        return bad_request("Invalid JSON in request body")
    except Exception as e:
        print(f"Error creating jobs from Gmail: {e}")
        return internal_error("Failed to create jobs from Gmail")
