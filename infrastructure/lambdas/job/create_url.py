"""
Job Create URL Lambda Handler

Creates a new job by scraping a job posting URL.

Requirements: 5.2, 5.6
"""
import json
import os
import re
import sys
from datetime import datetime
from urllib.parse import urlparse

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
    import requests
    from bs4 import BeautifulSoup
    HAS_SCRAPING = True
except ImportError:
    HAS_SCRAPING = False

from shared.response import api_response, bad_request, internal_error
from shared.dynamodb import DynamoDBClient
from shared.validation import make_safe_url_segment, VALID_SUBCOMPONENTS


def get_default_generation_types(db: DynamoDBClient, userid: str) -> dict:
    """Get user's default generation types for all subcomponents."""
    prefs = db.get_user_prefs(userid)
    # Default generation types (contact defaults to manual, others to ai)
    defaults = {
        'contact': 'manual',
        'summary': 'ai',
        'skills': 'ai',
        'highlights': 'ai',
        'experience': 'ai',
        'education': 'ai',
        'awards': 'ai',
        'keynotes': 'ai',
        'coverletter': 'ai',
    }
    result = {}
    for component in VALID_SUBCOMPONENTS:
        pref_name = f"default_gen_{component}"
        result[component] = prefs.get(pref_name, defaults.get(component, 'ai'))
    return result


def extract_salary_from_text(text: str) -> str:
    """
    Extract salary information from text using regex patterns.
    Returns the first salary match found, or empty string.
    """
    if not text:
        return ''
    
    # Patterns for salary extraction (ordered by specificity)
    salary_patterns = [
        # Range with K notation: $120K - $150K, $120k-$150k
        r'\$\d{2,3}[kK]\s*[-–—to]+\s*\$?\d{2,3}[kK](?:\s*(?:per\s+)?(?:year|yr|annually|/yr|/year))?',
        # Range with full numbers: $120,000 - $150,000
        r'\$\d{1,3}(?:,\d{3})+\s*[-–—to]+\s*\$?\d{1,3}(?:,\d{3})+(?:\s*(?:per\s+)?(?:year|yr|annually|/yr|/year))?',
        # Range without commas: $120000 - $150000
        r'\$\d{5,7}\s*[-–—to]+\s*\$?\d{5,7}(?:\s*(?:per\s+)?(?:year|yr|annually|/yr|/year))?',
        # Single K notation: $150K, $150k/year
        r'\$\d{2,3}[kK](?:\s*(?:per\s+)?(?:year|yr|annually|/yr|/year))?',
        # Single full number: $150,000/year
        r'\$\d{1,3}(?:,\d{3})+(?:\s*(?:per\s+)?(?:year|yr|annually|/yr|/year))?',
        # Hourly range: $50 - $75/hr, $50-$75 per hour
        r'\$\d{2,3}\s*[-–—to]+\s*\$?\d{2,3}\s*(?:per\s+)?(?:hour|hr|/hr|/hour)',
        # Single hourly: $75/hr
        r'\$\d{2,3}\s*(?:per\s+)?(?:hour|hr|/hr|/hour)',
    ]
    
    for pattern in salary_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()[:100]
    
    return ''


def extract_linkedin_job_data(soup: BeautifulSoup, url: str) -> dict:
    """
    LinkedIn-specific job data extraction.
    Focuses on the main job posting section, avoiding recommended jobs at bottom.
    """
    job_data = {
        'jobcompany': '',
        'jobtitle': '',
        'jobdesc': '',
        'joblocation': '',
        'jobsalary': '',
        'jobposteddate': datetime.utcnow().strftime('%Y-%m-%d'),
        'jobtags': []
    }
    
    # LinkedIn title selectors (main job only)
    title_selectors = [
        'h1.top-card-layout__title',
        'h1.topcard__title', 
        '.job-details-jobs-unified-top-card__job-title h1',
        '.jobs-unified-top-card__job-title',
        'h1[class*="job-title"]',
        'h1'
    ]
    for selector in title_selectors:
        elem = soup.select_one(selector)
        if elem and elem.get_text(strip=True):
            job_data['jobtitle'] = elem.get_text(strip=True)[:200]
            break
    
    # LinkedIn company selectors
    company_selectors = [
        '.topcard__org-name-link',
        '.top-card-layout__card a[data-tracking-control-name*="company"]',
        '.job-details-jobs-unified-top-card__company-name',
        '.jobs-unified-top-card__company-name a',
        'a[class*="company-name"]',
        '[class*="topcard"] [class*="company"]'
    ]
    for selector in company_selectors:
        elem = soup.select_one(selector)
        if elem and elem.get_text(strip=True):
            job_data['jobcompany'] = elem.get_text(strip=True)[:100]
            break
    
    # LinkedIn location selectors
    location_selectors = [
        '.topcard__flavor--bullet',
        '.top-card-layout__bullet',
        '.job-details-jobs-unified-top-card__bullet',
        '.jobs-unified-top-card__bullet',
        '[class*="topcard"] [class*="location"]'
    ]
    for selector in location_selectors:
        elem = soup.select_one(selector)
        if elem and elem.get_text(strip=True):
            job_data['joblocation'] = elem.get_text(strip=True)[:100]
            break
    
    # LinkedIn job description selectors - MAIN JOB ONLY
    # These selectors target the primary job description, not recommended jobs
    desc_selectors = [
        '.description__text',
        '.show-more-less-html__markup',
        '.jobs-description__content',
        '.job-details-jobs-unified-top-card__job-insight',
        '#job-details',
        '.jobs-box__html-content'
    ]
    
    main_job_desc = ''
    for selector in desc_selectors:
        elem = soup.select_one(selector)
        if elem:
            main_job_desc = elem.get_text(separator='\n', strip=True)[:10000]
            break
    
    job_data['jobdesc'] = main_job_desc
    
    # Extract salary ONLY from the main job description text
    # This avoids picking up salary from recommended jobs at bottom of page
    if main_job_desc:
        job_data['jobsalary'] = extract_salary_from_text(main_job_desc)
    
    # If no salary in description, check the job insights section (top card only)
    if not job_data['jobsalary']:
        insight_selectors = [
            '.job-details-jobs-unified-top-card__job-insight',
            '.jobs-unified-top-card__job-insight',
            '.compensation__salary',
            '.salary-main-rail__salary-range'
        ]
        for selector in insight_selectors:
            elem = soup.select_one(selector)
            if elem:
                insight_text = elem.get_text(strip=True)
                salary = extract_salary_from_text(insight_text)
                if salary:
                    job_data['jobsalary'] = salary
                    break
    
    return job_data


def extract_job_data(url: str) -> dict:
    """
    Scrape job posting page and extract structured data.
    
    Returns dict with: jobcompany, jobtitle, jobdesc, joblocation, 
                       jobsalary, jobposteddate, jobtags
    """
    if not HAS_SCRAPING:
        raise ImportError("requests and beautifulsoup4 required for URL scraping")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check if this is a LinkedIn URL - use specialized extraction
    parsed_url = urlparse(url)
    is_linkedin = 'linkedin.com' in parsed_url.netloc.lower()
    
    if is_linkedin:
        return extract_linkedin_job_data(soup, url)
    
    # Generic extraction for non-LinkedIn sites
    job_data = {
        'jobcompany': '',
        'jobtitle': '',
        'jobdesc': '',
        'joblocation': '',
        'jobsalary': '',
        'jobposteddate': datetime.utcnow().strftime('%Y-%m-%d'),
        'jobtags': []
    }
    
    # Try to extract title from common selectors
    title_selectors = [
        'h1.job-title', 'h1.posting-headline', 'h1[data-testid="job-title"]',
        '.job-title h1', '.posting-title', 'h1.topcard__title',
        'h1', '[class*="job-title"]', '[class*="JobTitle"]'
    ]
    for selector in title_selectors:
        elem = soup.select_one(selector)
        if elem and elem.get_text(strip=True):
            job_data['jobtitle'] = elem.get_text(strip=True)[:200]
            break
    
    # Try to extract company from common selectors
    company_selectors = [
        '.company-name', '.topcard__org-name-link', '[data-testid="company-name"]',
        '.posting-company', '.employer-name', '[class*="company"]',
        '[class*="Company"]', '.job-company'
    ]
    for selector in company_selectors:
        elem = soup.select_one(selector)
        if elem and elem.get_text(strip=True):
            job_data['jobcompany'] = elem.get_text(strip=True)[:100]
            break
    
    # Fallback: extract company from domain
    if not job_data['jobcompany']:
        parsed = urlparse(url)
        domain_parts = parsed.netloc.split('.')
        if len(domain_parts) >= 2:
            job_data['jobcompany'] = domain_parts[-2].title()
    
    # Try to extract description
    desc_selectors = [
        '.job-description', '.description__text', '[data-testid="job-description"]',
        '.posting-description', '#job-description', '.job-details',
        '[class*="description"]', '[class*="Description"]', 'article'
    ]
    for selector in desc_selectors:
        elem = soup.select_one(selector)
        if elem:
            job_data['jobdesc'] = elem.get_text(separator='\n', strip=True)[:10000]
            break
    
    # Fallback: use body text
    if not job_data['jobdesc']:
        body = soup.find('body')
        if body:
            job_data['jobdesc'] = body.get_text(separator='\n', strip=True)[:5000]
    
    # Try to extract location
    location_selectors = [
        '.job-location', '.topcard__flavor--bullet', '[data-testid="job-location"]',
        '.posting-location', '[class*="location"]', '[class*="Location"]'
    ]
    for selector in location_selectors:
        elem = soup.select_one(selector)
        if elem and elem.get_text(strip=True):
            job_data['joblocation'] = elem.get_text(strip=True)[:100]
            break
    
    # Try to extract salary - first from dedicated elements, then from description
    salary_selectors = [
        '.salary', '.compensation', '[data-testid="salary"]',
        '[class*="salary"]', '[class*="Salary"]', '[class*="compensation"]'
    ]
    for selector in salary_selectors:
        elem = soup.select_one(selector)
        if elem and elem.get_text(strip=True):
            job_data['jobsalary'] = elem.get_text(strip=True)[:100]
            break
    
    # Fallback: extract salary from description text using regex
    if not job_data['jobsalary'] and job_data['jobdesc']:
        job_data['jobsalary'] = extract_salary_from_text(job_data['jobdesc'])
    
    # Extract tags from keywords or skills sections
    tag_selectors = [
        '.skill-tag', '.job-tag', '[class*="skill"]', '[class*="tag"]',
        '.keywords li', '.requirements li'
    ]
    tags = set()
    for selector in tag_selectors:
        elems = soup.select(selector)[:10]
        for elem in elems:
            text = elem.get_text(strip=True)
            if text and len(text) < 50:
                tags.add(text)
    job_data['jobtags'] = list(tags)[:10]
    
    return job_data


def handler(event, context):
    """
    Create a job from a URL by scraping the job posting.
    
    Request body:
    {
        "url": "string",
        "resumeid": "string" (resume name to use)
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
        
        url = body.get('url')
        resumeid = body.get('resumeid')
        
        if not url:
            return bad_request("url is required")
        if not resumeid:
            return bad_request("resumeid is required")
        
        # Validate URL format
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return bad_request("Invalid URL format")
        
        db = DynamoDBClient()
        
        # Verify resume exists
        resume = db.get_resume(userid, resumeid)
        if not resume:
            return bad_request(f"Resume '{resumeid}' not found")
        
        # Scrape job data from URL
        try:
            scraped_data = extract_job_data(url)
        except Exception as e:
            print(f"Scraping error: {e}")
            return bad_request(f"Failed to scrape job posting: {str(e)}")
        
        # Validate required fields were extracted
        if not scraped_data.get('jobtitle'):
            return bad_request("Could not extract job title from URL")
        if not scraped_data.get('jobcompany'):
            return bad_request("Could not extract company name from URL")
        
        # Generate job ID
        jobid = str(uuid7.uuid7())
        
        # Create safe URL segment for job title
        jobtitlesafe = make_safe_url_segment(scraped_data['jobtitle'])
        
        # Create JOB record
        job_data = {
            'jobid': jobid,
            'postedts': datetime.utcnow().isoformat(),
            'jobcompany': scraped_data['jobcompany'],
            'jobtitle': scraped_data['jobtitle'],
            'jobtitlesafe': jobtitlesafe,
            'jobdesc': scraped_data.get('jobdesc', ''),
            'joblocation': scraped_data.get('joblocation', ''),
            'jobsalary': scraped_data.get('jobsalary', ''),
            'jobposteddate': scraped_data.get('jobposteddate', datetime.utcnow().strftime('%Y-%m-%d')),
            'joburl': url,
            'jobcompanylogo': '',
            'jobtags': scraped_data.get('jobtags', []),
        }
        
        created_job = db.create_job(job_data)
        
        # Get user's default generation types
        gen_types = get_default_generation_types(db, userid)
        
        # Determine initial phase based on data completeness
        has_required = bool(scraped_data.get('jobcompany') and 
                          scraped_data.get('jobtitle') and 
                          scraped_data.get('jobdesc'))
        initial_phase = 'Queued' if has_required else 'Queued'
        
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
            'datakeynotes': '',
            'datacoverletter': '',
            
            # Generation states (all start as "ready")
            'statecontact': 'ready',
            'statesummary': 'ready',
            'stateskills': 'ready',
            'statehighlights': 'ready',
            'stateexperience': 'ready',
            'stateeducation': 'ready',
            'stateawards': 'ready',
            'statekeynotes': 'ready',
            'statecoverletter': 'ready',
            
            # Generation types (from user preferences)
            'typecontact': gen_types['contact'],
            'typesummary': gen_types['summary'],
            'typeskills': gen_types['skills'],
            'typehighlights': gen_types['highlights'],
            'typeexperience': gen_types['experience'],
            'typeeducation': gen_types['education'],
            'typeawards': gen_types['awards'],
            'typekeynotes': gen_types['keynotes'],
            'typecoverletter': gen_types['coverletter'],
            
            # Final file locations (empty initially)
            's3locresumehtml': '',
            's3locresumepdf': '',
            's3loccoverletterhtml': '',
            's3loccoverletterpdf': '',
        }
        
        created_user_job = db.create_user_job(user_job_data)
        
        return api_response(201, {
            'message': 'Job created successfully from URL',
            'job': created_job,
            'userJob': created_user_job
        })
        
    except json.JSONDecodeError:
        return bad_request("Invalid JSON in request body")
    except Exception as e:
        print(f"Error creating job from URL: {e}")
        return internal_error("Failed to create job from URL")
