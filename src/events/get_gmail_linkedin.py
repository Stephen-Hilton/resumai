"""
Event: get_gmail_linkedin

Connects to Gmail via IMAP and searches for LinkedIn Job Alert emails from the last 2 weeks.
Parses email HTML to extract job listings and creates job folders for each listing.
For each job, fetches the full job posting HTML from LinkedIn and extracts the description.

Requirements: 4.1, 4.2
"""

from pathlib import Path
from src.lib.types import EventContext, EventResult
from src.lib.logging_utils import append_app_log
import os
from datetime import datetime, timedelta
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import re
import httpx

# Logs directory
LOGS_DIR = Path("src/logs")


def fetch_linkedin_job_html(url: str, timeout: int = 30) -> str:
    """
    Fetch HTML from LinkedIn job posting URL.
    
    Args:
        url: LinkedIn job URL (e.g., https://www.linkedin.com/jobs/view/4352500475/)
        timeout: Request timeout in seconds
        
    Returns:
        HTML content as string, or None if fetch fails
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = httpx.get(url, headers=headers, timeout=timeout, follow_redirects=True)
        response.raise_for_status()
        return response.text
    except Exception as e:
        append_app_log(LOGS_DIR, f"get_gmail_linkedin: Failed to fetch {url}: {type(e).__name__}: {str(e)}")
        return None


def sanitize_text_for_yaml(text: str) -> str:
    """
    Sanitize text to remove problematic characters for YAML.
    
    Replaces:
    - Smart quotes with regular quotes
    - Em/en dashes with regular hyphens
    - Non-breaking spaces with regular spaces
    - Other problematic Unicode characters
    
    Args:
        text: Raw text that may contain problematic characters
        
    Returns:
        Sanitized text safe for YAML
    """
    if not text:
        return text
    
    # Replace smart quotes
    text = text.replace('\u2018', "'")  # Left single quote
    text = text.replace('\u2019', "'")  # Right single quote
    text = text.replace('\u201c', '"')  # Left double quote
    text = text.replace('\u201d', '"')  # Right double quote
    
    # Replace dashes
    text = text.replace('\u2013', '-')  # En dash
    text = text.replace('\u2014', '-')  # Em dash
    
    # Replace spaces
    text = text.replace('\u00a0', ' ')  # Non-breaking space
    text = text.replace('\u2009', ' ')  # Thin space
    text = text.replace('\u200b', '')   # Zero-width space
    
    # Replace ellipsis
    text = text.replace('\u2026', '...')  # Horizontal ellipsis
    
    # Replace bullet points
    text = text.replace('\u2022', '*')  # Bullet
    text = text.replace('\u2023', '*')  # Triangular bullet
    
    # Remove other control characters and problematic Unicode
    # Keep only printable ASCII and common whitespace
    import unicodedata
    text = ''.join(
        char if (ord(char) < 128 or char in '\n\r\t') or unicodedata.category(char)[0] not in ['C', 'Z']
        else ' ' if unicodedata.category(char)[0] == 'Z'
        else ''
        for char in text
    )
    
    return text


def parse_linkedin_job_description(html: str) -> str:
    """
    Parse job description from LinkedIn job posting HTML.
    
    LinkedIn job descriptions are typically in a div with class "description__text" or similar.
    This function extracts the text content from the description section.
    
    Args:
        html: HTML content from LinkedIn job page
        
    Returns:
        Job description text, or None if parsing fails
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try multiple selectors for job description
        # LinkedIn uses different class names depending on the page variant
        selectors = [
            'div.description__text',
            'div.show-more-less-html__markup',
            'div[class*="description"]',
            'section.description',
            'article.jobs-description',
        ]
        
        for selector in selectors:
            description_elem = soup.select_one(selector)
            if description_elem:
                # Get text content, preserving some structure
                text = description_elem.get_text(separator='\n', strip=True)
                if text and len(text) > 100:  # Ensure we got substantial content
                    # Sanitize text before returning
                    return sanitize_text_for_yaml(text)
        
        # If no description found with selectors, try to find any large text block
        # This is a fallback for when LinkedIn changes their HTML structure
        all_text = soup.get_text(separator='\n', strip=True)
        if len(all_text) > 500:
            append_app_log(LOGS_DIR, f"get_gmail_linkedin: Using fallback text extraction (no description selector matched)")
            # Sanitize text before returning
            return sanitize_text_for_yaml(all_text)
        
        append_app_log(LOGS_DIR, f"get_gmail_linkedin: Could not find job description in HTML")
        return None
        
    except Exception as e:
        append_app_log(LOGS_DIR, f"get_gmail_linkedin: Error parsing job description: {type(e).__name__}: {str(e)}")
        return None


def extract_job_id_from_url(url: str) -> str:
    """
    Extract LinkedIn job ID from URL.
    
    Example: https://www.linkedin.com/jobs/view/4352500475 -> 4352500475
    """
    match = re.search(r'/jobs/view/(\d+)', url)
    if match:
        return match.group(1)
    return None


def parse_linkedin_job_card(job_card_td) -> dict:
    """
    Parse a LinkedIn job card from the email HTML.
    
    The structure is:
    <td data-test-id="job-card">
      <table>
        <tr>
          <td class="pr-1 w-6"><img src="company_logo" alt="Company Name"></td>
          <td>
            <a href="job_url">
              <h3>Job Title</h3>
              <p>Company · Location</p>
              <p>Salary</p>
              <div>Tags (Easy Apply, Fast growing, etc.)</div>
            </a>
          </td>
        </tr>
      </table>
    </td>
    """
    try:
        # Find the main job link
        job_link = job_card_td.find('a', href=re.compile(r'/jobs/view/\d+'))
        if not job_link:
            return None
        
        # Extract URL and clean it
        job_url = job_link.get('href', '')
        if '?' in job_url:
            job_url = job_url.split('?')[0]
        
        # Remove /comm/ from LinkedIn URLs
        job_url = job_url.replace('/comm/jobs/view/', '/jobs/view/')
        
        # Extract job ID from URL
        job_id = extract_job_id_from_url(job_url)
        if not job_id:
            return None
        
        # Extract job title - it's in an <a> tag with class containing "font-bold" and "text-md"
        # The title link is nested inside the job_link
        title_link = job_card_td.find('a', class_=re.compile(r'font-bold.*text-md'))
        if title_link:
            job_title = title_link.get_text(strip=True)
        else:
            job_title = "Unknown Title"
        
        # Extract company and location from <p> with class containing "text-system-gray-100" and "text-xs"
        company_location_elem = job_card_td.find('p', class_=re.compile(r'text-system-gray-100.*text-xs'))
        company = "Unknown Company"
        location = None
        
        if company_location_elem:
            text = company_location_elem.get_text(strip=True)
            # Format is usually "Company · Location" (with middot character)
            if '·' in text:
                parts = text.split('·')
                if len(parts) >= 1:
                    company = parts[0].strip()
                if len(parts) >= 2:
                    location = parts[1].strip()
            else:
                # If no middot, assume it's just the company
                company = text
        
        # Extract salary from <p> with class containing "text-system-gray-70" and "text-xs"
        salary_elem = job_card_td.find('p', class_=re.compile(r'text-system-gray-70.*text-xs'))
        salary = salary_elem.get_text(strip=True) if salary_elem else None
        
        # Extract tags (Easy Apply, Fast growing, school alumni, etc.)
        tags = []
        
        # Look for company logo alt text for company name if we didn't get it
        if company == "Unknown Company":
            logo_img = job_card_td.find('img', alt=True)
            if logo_img and logo_img.get('alt'):
                company = logo_img.get('alt')
        
        # Find all job-card-flavor__detail elements for tags
        flavor_details = job_card_td.find_all('p', class_='job-card-flavor__detail')
        for detail in flavor_details:
            tag_text = detail.get_text(strip=True)
            if tag_text:
                tags.append(tag_text)
        
        return {
            "id": job_id,
            "company": sanitize_text_for_yaml(company),
            "title": sanitize_text_for_yaml(job_title),
            "url": job_url,
            "location": sanitize_text_for_yaml(location) if location else None,
            "salary": sanitize_text_for_yaml(salary) if salary else None,
            "tags": [sanitize_text_for_yaml(tag) for tag in tags] if tags else None
        }
    
    except Exception as e:
        append_app_log(LOGS_DIR, f"get_gmail_linkedin: Error parsing job card: {type(e).__name__}: {str(e)}")
        return None


async def execute(job_path: Path, ctx: EventContext) -> EventResult:
    """
    Connect to Gmail and fetch LinkedIn job alert emails from the last 2 weeks.
    
    Args:
        job_path: Not used (this creates new jobs)
        ctx: Event context with configuration
        
    Returns:
        EventResult with list of created job folders
    """
    try:
        import imapclient
        
        # Get credentials from environment
        username = os.getenv("GMAIL_USERNAME")
        password = os.getenv("GMAIL_APP_PASSWORD")
        
        if not username or not password:
            error_dict = {
                "message": "Gmail credentials not found in environment variables",
                "details": {"missing": "GMAIL_USERNAME or GMAIL_APP_PASSWORD"}
            }
            append_app_log(LOGS_DIR, f"get_gmail_linkedin: ERROR: {error_dict['message']}")
            return EventResult(ok=False, message=error_dict['message'], errors=[error_dict], job_path=job_path)
        
        append_app_log(LOGS_DIR, f"get_gmail_linkedin: Connecting to Gmail as {username}")
        
        # Connect to Gmail IMAP
        server = imapclient.IMAPClient('imap.gmail.com', ssl=True)
        server.login(username, password)
        
        # Select inbox
        server.select_folder('INBOX', readonly=True)
        
        # Search for LinkedIn job alerts from last 2 weeks
        two_weeks_ago = datetime.now() - timedelta(days=14)
        search_criteria = [
            'FROM', 'jobalerts-noreply@linkedin.com',
            'SINCE', two_weeks_ago.strftime('%d-%b-%Y')
        ]
        
        append_app_log(LOGS_DIR, f"get_gmail_linkedin: Searching for emails since {two_weeks_ago.strftime('%Y-%m-%d')}")
        
        message_ids = server.search(search_criteria)
        append_app_log(LOGS_DIR, f"get_gmail_linkedin: Found {len(message_ids)} LinkedIn job alert emails")
        
        if not message_ids:
            server.logout()
            return EventResult(
                ok=True,
                message="No LinkedIn job alerts found in the last 2 weeks",
                job_path=job_path
            )
        
        # Fetch and parse emails
        jobs_created = []
        jobs_skipped = []
        
        for msg_id in message_ids:
            try:
                # Fetch the email
                raw_message = server.fetch([msg_id], ['RFC822'])
                email_data = raw_message[msg_id][b'RFC822']
                email_message = email.message_from_bytes(email_data)
                
                # Get email date
                email_date = email_message.get('Date', '')
                if email_date:
                    from email.utils import parsedate_to_datetime
                    try:
                        date_obj = parsedate_to_datetime(email_date)
                        email_sent_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        email_sent_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                else:
                    email_sent_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Extract subject
                subject = email_message.get('Subject', '')
                if isinstance(subject, str):
                    subject_decoded = subject
                else:
                    decoded = decode_header(subject)
                    subject_decoded = decoded[0][0]
                    if isinstance(subject_decoded, bytes):
                        subject_decoded = subject_decoded.decode()
                
                # Get email body (HTML)
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/html":
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            break
                else:
                    body = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
                
                if not body:
                    continue
                
                # Parse HTML
                soup = BeautifulSoup(body, 'html.parser')
                
                # Find all job cards (td elements with data-test-id="job-card")
                job_cards = soup.find_all('td', attrs={'data-test-id': 'job-card'})
                
                append_app_log(LOGS_DIR, f"get_gmail_linkedin: Email '{subject_decoded[:50]}...' contains {len(job_cards)} job cards")
                
                for job_card in job_cards:
                    try:
                        job_data = parse_linkedin_job_card(job_card)
                        
                        if not job_data:
                            continue
                        
                        # Add additional fields
                        job_data["source"] = "gmail_linkedin"
                        job_data["date"] = email_sent_date  # Use email sent date, not current date
                        job_data["description"] = f"Job found in LinkedIn email alert: {subject_decoded}"
                        # subcontent_events will be loaded from template by dump_job_yaml
                        
                        # Check if job already exists (by ID)
                        job_exists = False
                        for phase_dir in ctx.jobs_root.glob("*"):
                            if phase_dir.is_dir():
                                for existing_job in phase_dir.iterdir():
                                    if existing_job.is_dir():
                                        job_yaml = existing_job / "job.yaml"
                                        if job_yaml.exists():
                                            from src.lib.yaml_utils import load_yaml
                                            existing_data = load_yaml(job_yaml)
                                            if existing_data.get("id") == job_data["id"]:
                                                job_exists = True
                                                jobs_skipped.append(job_data["id"])
                                                break
                            if job_exists:
                                break
                        
                        if job_exists:
                            continue
                        
                        # Fetch job HTML and parse description before creating folder
                        job_html = None
                        full_description = None
                        
                        if job_data.get("url"):
                            append_app_log(LOGS_DIR, f"get_gmail_linkedin: Fetching HTML for job {job_data['id']}")
                            job_html = fetch_linkedin_job_html(job_data["url"])
                            
                            if job_html:
                                full_description = parse_linkedin_job_description(job_html)
                                if full_description:
                                    # Update job_data with full description
                                    job_data["description"] = full_description
                                    append_app_log(LOGS_DIR, f"get_gmail_linkedin: Extracted description ({len(full_description)} chars) for job {job_data['id']}")
                                else:
                                    append_app_log(LOGS_DIR, f"get_gmail_linkedin: Could not parse description for job {job_data['id']}")
                            else:
                                append_app_log(LOGS_DIR, f"get_gmail_linkedin: Could not fetch HTML for job {job_data['id']}")
                        
                        # Create job folder
                        from src.events.event_bus import run_event
                        create_ctx = EventContext(
                            jobs_root=ctx.jobs_root,
                            resumes_root=ctx.resumes_root,
                            default_resume=ctx.default_resume,
                            test_mode=ctx.test_mode,
                            state={"job": job_data}
                        )
                        
                        result = await run_event("create_jobfolder", Path("placeholder"), create_ctx)
                        
                        if result.ok:
                            # Save job.html if we fetched it
                            if job_html:
                                job_html_path = result.job_path / "job.html"
                                try:
                                    job_html_path.write_text(job_html, encoding='utf-8')
                                    append_app_log(LOGS_DIR, f"get_gmail_linkedin: Saved job.html for job {job_data['id']}")
                                except Exception as e:
                                    append_app_log(LOGS_DIR, f"get_gmail_linkedin: Failed to save job.html for job {job_data['id']}: {str(e)}")
                            
                            jobs_created.append(str(result.job_path))
                            append_app_log(LOGS_DIR, f"get_gmail_linkedin: Created job {job_data['id']}: {job_data['company']} - {job_data['title']}")
                        else:
                            append_app_log(LOGS_DIR, f"get_gmail_linkedin: Failed to create job {job_data['id']}: {result.message}")
                    
                    except Exception as e:
                        append_app_log(LOGS_DIR, f"get_gmail_linkedin: Error processing job card: {type(e).__name__}: {str(e)}")
                        continue
            
            except Exception as e:
                append_app_log(LOGS_DIR, f"get_gmail_linkedin: Error processing email {msg_id}: {type(e).__name__}: {str(e)}")
                continue
        
        # Logout
        server.logout()
        
        message = f"Created {len(jobs_created)} new jobs, skipped {len(jobs_skipped)} existing jobs"
        append_app_log(LOGS_DIR, f"get_gmail_linkedin: {message}")
        
        return EventResult(
            ok=True,
            message=message,
            job_path=job_path,
            artifacts=jobs_created
        )
    
    except Exception as e:
        import traceback
        error_dict = {
            "message": f"Failed to fetch Gmail jobs: {str(e)}",
            "details": {
                "exception_type": type(e).__name__, 
                "exception": str(e),
                "traceback": traceback.format_exc()
            }
        }
        append_app_log(LOGS_DIR, f"get_gmail_linkedin: ERROR: {error_dict['message']}")
        append_app_log(LOGS_DIR, f"get_gmail_linkedin: TRACEBACK: {traceback.format_exc()}")
        return EventResult(ok=False, message=error_dict['message'], errors=[error_dict], job_path=job_path)


async def test(job_path: Path, ctx: EventContext) -> EventResult:
    """Test mode - same as execute but with test_mode flag."""
    return await execute(job_path, ctx)
