from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from pprint import pprint
import os
import logging
from . import gmail_mgr as gmail
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from . import logging_setup

# Set up logger for this module
logger = logging_setup.get_logger(__name__)
    

def get_emails_html():
    load_dotenv('.env')
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    gmail_address = os.getenv("GMAIL_ADDRESS")

    emails = gmail.get_gmails(gmail_address, app_password, 
                        sender_filters=['LinkedIn Job Alerts'],
                        sent_since=datetime.now() - timedelta(days=3),
                        unread_only=False, 
                        mark_as_read=False, 
                        max_results=10)
    return emails


def parse_emails_to_jobs(emails:list=None):
    """
    Parse a set of N-number of LinkedIn Job Alert emails, each which contain N-number of jobs, 
    and return a single structured list of dictionaries, each representing a job.
    Each job dictionary will include:
    - title: The title of the job
    - company: The name of the company offering the job
    - location: The location of the job (if available)
    - connections: The number of connections to the company (if available)
    - link: The URL to the job description page on LinkedIn
    - date_received: The sent date of the email

    Returns a list of dictionaries, each representing a job with the above details.
    """
    if not emails:
        emails = get_emails_html()

    jobs = []
    seen_links = set()
    errors = []
    def log_error(dt:datetime, subject:str, msg:str, other_data:dict=None):
        err = {"email":subject, "date":dt, "message":msg}
        if other_data: err['other_data'] = other_data
        errors.append(err)
        print('Error parsing email:', msg)

    
    # Parse Emails:
    for em in emails:
        date_received = em.get('date').replace('T', ' ')
        html = em.get('body_html') or em.get('body_text') or ''
        if not html: continue

        # Parse HTML content
        soup = BeautifulSoup(html, 'html.parser')

        # Heuristic: job links in LinkedIn alerts often contain '/jobs/' or 'linkedin.com/jobs'
        anchors = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/jobs/' in href or 'linkedin.com/jobs' in href or 'jobs/view' in href:
                anchors.append(a)

        # If none found, fall back to any anchor with non-empty text
        if not anchors:
            anchors = [a for a in soup.find_all('a') if a.get_text(strip=True)]


        # loop thru all achors and extract job info
        # ---------------------------------------------
        for a in anchors:
            # determine job section and extract title
            text = [p.strip() for p in a.get_text().strip().split('  ') if len(p)>1]
            title = company = location = salary = connections = tags = href = None
            if len(text) < 3: continue

            title = text[0]
            if '·' in text[1]:
                company, location = [p.strip() for p in text[1].split('·', 1)]
            else: 
                company = text[1]
            if '$' in text[2]:
                salary = text[2]
            if len(text) >3: 
                tags = ', '.join(text[3:])

            pass
                
  
                
            # extract Job ID from href, build link and dedupe
            full_href = a['href']
            job_id = [p for p in full_href.split('?')[0].split('/') if len(p) >1][-1]
            href = f"https://www.linkedin.com/jobs/view/{job_id}/"
            if href in seen_links: continue

            job = {
                'id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
                'link': href,
                'date_received': date_received.isoformat() if isinstance(date_received, datetime) else date_received,
                'tags': tags,
            }
            
            jobs.append(job)
            seen_links.add(href)

    return jobs



def parse_job_description(html:str) -> str:
    """
    Parse out the "About the Opportunity" section from a LinkedIn job description HTML document.
    This should be everything between html.lower().find('about the opportunity') and the next <div> tag.
    It should be neatly formatted, and include newlines or other formatting as appropriate. 
    
    Args: 
        html (str): The full HTML content of the LinkedIn job description page.
    
    Returns:
        str: The extracted "About the Opportunity" section as plain text, or an empty string if not found.
    """
    # Prefer the LinkedIn job description container which often uses this class
    # when content is clamped with a 'show more' control. Fall back to the
    # previous heuristic if not found.
    def _extract_from_div(soup):
        # CSS selector matching the clamped markup container
        sel = 'div.show-more-less-html__markup.show-more-less-html__markup--clamp-after-5.relative.overflow-hidden'
        node = soup.select_one(sel)
        if node:
            return node.get_text(separator='\n', strip=True)
        # fallback: try matching by substring in class attribute
        for div in soup.find_all('div', class_=True):
            cls = ' '.join(div.get('class'))
            if 'show-more-less-html__markup' in cls and 'clamp-after-5' in cls:
                return div.get_text(separator='\n', strip=True)
        return None

    soup = BeautifulSoup(html, 'html.parser')

    extracted = _extract_from_div(soup)
    if extracted: return extracted 

    # Fallback: older heuristic that searched for the 'About the Opportunity' heading
    text = soup.get_text(separator='\n')
    lower_text = text.lower()
    start_idx = lower_text.find("""<div class="show-more-less-html__markup show-more-less-html__markup--clamp-after-5
            relative overflow-hidden">""")
    if start_idx == -1:
        return ''

    end_idx = lower_text.find('\n\n', start_idx)
    if end_idx == -1:
        end_idx = len(text)

    about_section = text[start_idx:end_idx].strip()
    return about_section




if __name__ == "__main__":
    jobs = parse_emails_to_jobs()

    pass