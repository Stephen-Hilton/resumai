#!/usr/bin/env python3
"""
Web UI for managing job applications
Provides interface to view, edit, and manage generated job applications
"""

import os
import sys
import yaml
import shutil
import time
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response
import re

# Add parent directory to path to import logging_setup
sys.path.append(str(Path(__file__).parent.parent))

# Handle imports for different contexts
try:
    from utils import logging_setup
    from utils.version import get_version
except ImportError:
    try:
        from src.utils import logging_setup
        from src.utils.version import get_version
    except ImportError:
        # Last resort - try relative import
        import logging_setup

# Import sanitize function for URL job processing
try:
    from step1_queue import sanitize_text_for_yaml
except ImportError:
    # Fallback if import fails
    def sanitize_text_for_yaml(text):
        return str(text) if text else ''
        from version import get_version

# Get current version
VERSION = get_version()

# Set up logger
logger = logging_setup.get_logger(__name__)

app = Flask(__name__)
app.secret_key = 'resumai_web_ui_secret_key_change_in_production'
app.config['SERVER_NAME'] = None  # Allow any host
app.config['PORT'] = 5001

# Base paths
BASE_DIR = Path(__file__).parent.parent
JOBS_DIR = BASE_DIR / 'jobs'
GENERATED_DIR = JOBS_DIR / '2_generated'
APPLIED_DIR = JOBS_DIR / '3_applied'

def calculate_days_old(date_str):
    """Calculate how many days old a job is based on date_received"""
    try:
        if not date_str:
            return "Unknown"
            
        # Clean up the date string
        clean_date_str = str(date_str).strip()
        
        # Handle timezone by removing it
        # Format is like: '2025-12-29 10:45:48-08:00'
        # Remove the timezone part (-08:00, +05:30, etc.)
        if len(clean_date_str) >= 6:
            # Check if last 6 characters match timezone pattern like -08:00 or +05:30
            timezone_part = clean_date_str[-6:]
            if (timezone_part[0] in ['-', '+'] and 
                timezone_part[3] == ':' and 
                timezone_part[1:3].isdigit() and 
                timezone_part[4:6].isdigit()):
                clean_date_str = clean_date_str[:-6].strip()
        
        # Try different date formats
        date_formats = [
            '%Y-%m-%d %H:%M:%S',        # 2025-12-29 10:45:48
            '%Y-%m-%d',                 # 2025-12-29
            '%m/%d/%Y',                 # 12/29/2025
            '%d/%m/%Y',                 # 29/12/2025
            '%Y-%m-%d %H:%M:%S.%f',     # 2025-12-29 10:45:48.123456
            '%m/%d/%Y %H:%M:%S'         # 12/29/2025 10:45:48
        ]
        
        job_date = None
        for fmt in date_formats:
            try:
                job_date = datetime.strptime(clean_date_str, fmt)
                break
            except ValueError:
                continue
        
        if job_date is None:
            logger.warning(f"Could not parse date: '{date_str}' (cleaned: '{clean_date_str}')")
            return "Unknown"
        
        # Calculate days difference using date-only comparison for more intuitive results
        now = datetime.now()
        days_diff = (now.date() - job_date.date()).days
        result = max(0, days_diff)  # Don't show negative days
        
        # Debug logging for troubleshooting
        logger.debug(f"Date calculation: '{date_str}' -> parsed: {job_date} -> now: {now} -> days: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error calculating days old for date '{date_str}': {e}")
        return "Unknown"

# Make the function available in templates
app.jinja_env.globals.update(calculate_days_old=calculate_days_old)

def ensure_directories():
    """Ensure required directories exist"""
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    APPLIED_DIR.mkdir(parents=True, exist_ok=True)

def get_job_folders():
    """Get all job folders from the generated directory"""
    ensure_directories()
    folders = []
    
    for item in GENERATED_DIR.iterdir():
        if item.is_dir():
            # Look for job YAML file in the directory
            yaml_files = list(item.glob('*.yaml'))
            if yaml_files:
                job_yaml = yaml_files[0]  # Take the first YAML file
                try:
                    with open(job_yaml, 'r', encoding='utf-8') as f:
                        job_data = yaml.safe_load(f)
                    
                    # Check for file existence
                    resume_html = list(item.glob('*.resume.html'))
                    coverletter_html = list(item.glob('*.coverletter.html'))
                    summary_html = list(item.glob('*.!SUMMARY.html'))  # Changed to glob pattern
                    resume_pdf = list(item.glob('*.resume.pdf'))
                    coverletter_pdf = list(item.glob('*.coverletter.pdf'))
                    
                    folders.append({
                        'name': item.name,
                        'path': item,
                        'yaml_file': job_yaml,
                        'job_data': job_data,
                        'files': list(item.glob('*')),
                        'modified': datetime.fromtimestamp(item.stat().st_mtime),
                        'file_exists': {
                            'resume': len(resume_html) > 0,
                            'coverletter': len(coverletter_html) > 0,
                            'summary': len(summary_html) > 0,  # Changed to check glob results
                            'resume_pdf': len(resume_pdf) > 0,
                            'coverletter_pdf': len(coverletter_pdf) > 0
                        }
                    })
                except Exception as e:
                    logger.error(f"Error loading job data from {job_yaml}: {e}")
                    folders.append({
                        'name': item.name,
                        'path': item,
                        'yaml_file': job_yaml,
                        'job_data': {'error': f'Failed to load: {e}'},
                        'files': list(item.glob('*')),
                        'modified': datetime.fromtimestamp(item.stat().st_mtime),
                        'file_exists': {
                            'resume': False,
                            'coverletter': False,
                            'summary': False,
                            'resume_pdf': False,
                            'coverletter_pdf': False
                        }
                    })
    
    # Sort alphabetically by folder name (company.title.id format)
    folders.sort(key=lambda x: x['name'].lower())
    return folders

def get_phase_counts():
    """Get counts for all job phases"""
    ensure_directories()
    
    phase_counts = {
        'queued': 0,
        'generated': 0,
        'applied': 0,
        'communications': 0,
        'interviews': 0,
        'errors': 0,
        'expired': 0,
        'skipped': 0
    }
    
    # Count files in each directory
    phase_dirs = {
        'queued': '1_queued',
        'generated': '2_generated', 
        'applied': '3_applied',
        'communications': '4_communications',
        'interviews': '5_interviews',
        'errors': '8_errors',
        'expired': '9_expired',
        'skipped': '9_skipped'
    }
    
    for phase, dir_name in phase_dirs.items():
        phase_dir = JOBS_DIR / dir_name
        if phase_dir.exists():
            if phase == 'queued':
                # Count both flat YAML files (legacy) and subfolders with valid YAML files (new format)
                flat_files = len(list(phase_dir.glob('*.yaml')))
                
                # Count subfolders that contain YAML files
                valid_subfolders = 0
                for subfolder in phase_dir.iterdir():
                    if subfolder.is_dir():
                        yaml_files = list(subfolder.glob('*.yaml'))
                        if yaml_files:  # Only count if it has YAML files
                            valid_subfolders += 1
                
                phase_counts[phase] = flat_files + valid_subfolders
            elif phase == 'generated':
                # Count directories in generated (bundled jobs)
                phase_counts[phase] = len([d for d in phase_dir.iterdir() if d.is_dir()])
            else:
                # Count YAML files in other directories
                phase_counts[phase] = len(list(phase_dir.glob('*.yaml')))
    
    return phase_counts

def get_jobs_by_phase(phase='generated'):
    """Get jobs for a specific phase"""
    ensure_directories()
    folders = []
    
    phase_dirs = {
        'queued': '1_queued',
        'generated': '2_generated', 
        'applied': '3_applied',
        'communications': '4_communications',
        'interviews': '5_interviews',
        'errors': '8_errors',
        'expired': '9_expired',
        'skipped': '9_skipped'
    }
    
    if phase not in phase_dirs:
        return folders
    
    phase_dir = JOBS_DIR / phase_dirs[phase]
    
    if not phase_dir.exists():
        return folders
    
    if phase == 'queued':
        # Handle both flat files (legacy) and subfolders (new format) in queued
        
        # First, handle flat YAML files (legacy format)
        for yaml_file in phase_dir.glob('*.yaml'):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    job_data = yaml.safe_load(f)
                
                folders.append({
                    'name': yaml_file.stem,
                    'path': yaml_file.parent,
                    'yaml_file': yaml_file,
                    'job_data': job_data,
                    'files': [yaml_file],
                    'modified': datetime.fromtimestamp(yaml_file.stat().st_mtime),
                    'phase': phase,
                    'file_exists': {
                        'resume': False,
                        'coverletter': False,
                        'summary': False,
                        'resume_pdf': False,
                        'coverletter_pdf': False
                    }
                })
            except Exception as e:
                logger.error(f"Error loading job data from {yaml_file}: {e}")
                continue
        
        # Then, handle subfolders (new format)
        for item in phase_dir.iterdir():
            if item.is_dir():
                # Look for job YAML file in the directory
                yaml_files = list(item.glob('*.yaml'))
                if yaml_files:
                    job_yaml = yaml_files[0]
                    try:
                        with open(job_yaml, 'r', encoding='utf-8') as f:
                            job_data = yaml.safe_load(f)
                        
                        folders.append({
                            'name': item.name,
                            'path': item,
                            'yaml_file': job_yaml,
                            'job_data': job_data,
                            'files': list(item.glob('*')),
                            'modified': datetime.fromtimestamp(item.stat().st_mtime),
                            'phase': phase,
                            'file_exists': {
                                'resume': False,
                                'coverletter': False,
                                'summary': False,
                                'resume_pdf': False,
                                'coverletter_pdf': False
                            }
                        })
                    except Exception as e:
                        logger.error(f"Error loading job data from {job_yaml}: {e}")
                        continue
                        
    elif phase == 'generated':
        # Handle bundled directories in generated
        for item in phase_dir.iterdir():
            if item.is_dir():
                # Look for job YAML file in the directory
                yaml_files = list(item.glob('*.yaml'))
                if yaml_files:
                    job_yaml = yaml_files[0]
                    try:
                        with open(job_yaml, 'r', encoding='utf-8') as f:
                            job_data = yaml.safe_load(f)
                        
                        # Check for file existence
                        resume_html = list(item.glob('*.resume.html'))
                        coverletter_html = list(item.glob('*.coverletter.html'))
                        summary_html = list(item.glob('*.!SUMMARY.html'))
                        resume_pdf = list(item.glob('*.resume.pdf'))
                        coverletter_pdf = list(item.glob('*.coverletter.pdf'))
                        
                        folders.append({
                            'name': item.name,
                            'path': item,
                            'yaml_file': job_yaml,
                            'job_data': job_data,
                            'files': list(item.glob('*')),
                            'modified': datetime.fromtimestamp(item.stat().st_mtime),
                            'phase': phase,
                            'file_exists': {
                                'resume': len(resume_html) > 0,
                                'coverletter': len(coverletter_html) > 0,
                                'summary': len(summary_html) > 0,
                                'resume_pdf': len(resume_pdf) > 0,
                                'coverletter_pdf': len(coverletter_pdf) > 0
                            }
                        })
                    except Exception as e:
                        logger.error(f"Error loading job data from {job_yaml}: {e}")
                        continue
    else:
        # Handle YAML files in other directories
        for yaml_file in phase_dir.glob('*.yaml'):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    job_data = yaml.safe_load(f)
                
                folders.append({
                    'name': yaml_file.stem,
                    'path': yaml_file.parent,
                    'yaml_file': yaml_file,
                    'job_data': job_data,
                    'files': [yaml_file],
                    'modified': datetime.fromtimestamp(yaml_file.stat().st_mtime),
                    'phase': phase,
                    'file_exists': {
                        'resume': False,
                        'coverletter': False,
                        'summary': False,
                        'resume_pdf': False,
                        'coverletter_pdf': False
                    }
                })
            except Exception as e:
                logger.error(f"Error loading job data from {yaml_file}: {e}")
                continue
    
    # Sort alphabetically by folder name
    folders.sort(key=lambda x: x['name'].lower())
    return folders

@app.route('/')
@app.route('/phase/<phase>')
def index(phase='generated'):
    """Main page showing jobs for selected phase"""
    # Automatically clean up duplicates when page loads (silently)
    cleanup_duplicate_jobs()
    
    # Get phase counts for stats bar
    phase_counts = get_phase_counts()
    
    # Get jobs for selected phase
    folders = get_jobs_by_phase(phase)
    
    # Get queued count for backward compatibility
    queued_count = phase_counts['queued']
    
    return render_template('index.html', 
                         version=VERSION,
                         folders=folders, 
                         queued_count=queued_count,
                         phase_counts=phase_counts,
                         current_phase=phase)

@app.route('/manually_enter')
def manually_enter():
    """Manual job entry form page"""
    return render_template('manual_job_entry.html', version=VERSION)

@app.route('/manual_job_entry', methods=['POST'])
def manual_job_entry():
    """Handle manual job entry form submission"""
    try:
        import yaml
        import uuid
        from datetime import datetime
        
        # Get JSON data from request
        job_data = request.get_json()
        
        if not job_data:
            return jsonify({'success': False, 'message': 'No job data provided'})
        
        # Validate required fields
        required_fields = ['company', 'title', 'description']
        for field in required_fields:
            if not job_data.get(field, '').strip():
                return jsonify({'success': False, 'message': f'Missing required field: {field}'})
        
        # Generate unique job ID and timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        job_id = str(abs(hash(f"{job_data['company']}{job_data['title']}{timestamp}")) % 10000000000)
        
        # Clean company and title for filename
        company_clean = re.sub(r'[^\w\s-]', '', job_data['company']).strip()
        company_clean = re.sub(r'[-\s]+', '_', company_clean)
        title_clean = re.sub(r'[^\w\s-]', '', job_data['title']).strip()
        title_clean = re.sub(r'[-\s]+', '_', title_clean)
        
        # Create filename
        filename = f"{timestamp}.{job_id}.{company_clean}.{title_clean}.yaml"
        
        # Prepare YAML structure
        yaml_data = {
            'company': job_data['company'].strip(),
            'title': job_data['title'].strip(),
            'location': job_data.get('location', '').strip() or 'Not specified',
            'salary': job_data.get('salary', '').strip() or 'Not specified',
            'description': job_data['description'].strip(),
            'link': job_data.get('link', '').strip() or '',
            'source': job_data.get('source', 'Manual Entry'),
            'priority': job_data.get('priority', 'Medium'),
            'notes': job_data.get('notes', '').strip(),
            'date_received': datetime.now().strftime('%Y-%m-%d'),
            'date_added': datetime.now().isoformat(),
            'manually_entered': True
        }
        
        # Ensure queued directory exists
        queued_dir = JOBS_DIR / '1_queued'
        queued_dir.mkdir(parents=True, exist_ok=True)
        
        # Write YAML file
        yaml_file_path = queued_dir / filename
        with open(yaml_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        logger.info(f"Manual job entry created: {filename}")
        
        return jsonify({
            'success': True, 
            'message': f'Job "{job_data["title"]}" at {job_data["company"]} added to queue successfully!',
            'filename': filename,
            'job_id': job_id
        })
        
    except Exception as e:
        logger.error(f"Error in manual job entry: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': f'Error adding job: {str(e)}'})

@app.route('/add_job_by_url')
def add_job_by_url():
    """Add job by URL form page"""
    return render_template('add_job_by_url.html', version=VERSION)

@app.route('/extract_job_from_url', methods=['POST'])
def extract_job_from_url():
    """Extract job details from LinkedIn URL"""
    try:
        import requests
        import sys
        from pathlib import Path
        
        # Add src directory to path for imports
        src_path = Path(__file__).parent.parent
        if str(src_path) not in sys.path:
            sys.path.append(str(src_path))
        
        # Import the LinkedIn parsing functions
        try:
            import parse_linkedin_emails
            from step1_queue import sanitize_job_data, sanitize_text_for_yaml
        except ImportError as e:
            logger.error(f"Error importing LinkedIn parsing modules: {e}")
            return jsonify({'success': False, 'message': 'LinkedIn parsing modules not available'})
        
        # Get JSON data from request
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        job_url = request_data.get('job_url', '').strip()
        
        if not job_url:
            return jsonify({'success': False, 'message': 'No job URL provided'})
        
        # Validate LinkedIn URL
        if 'linkedin.com/jobs/view/' not in job_url:
            logger.info(f"Non-LinkedIn URL requested: {job_url}")
            return jsonify({
                'success': False, 
                'message': 'Currently only LinkedIn job postings are supported. Please provide a LinkedIn job URL.'
            })
        
        # Extract job ID from URL
        try:
            # LinkedIn URLs are like: https://www.linkedin.com/jobs/view/1234567890
            job_id = job_url.split('/jobs/view/')[-1].split('?')[0].split('/')[0]
            if not job_id.isdigit():
                raise ValueError("Invalid job ID")
        except Exception as e:
            logger.error(f"Error extracting job ID from URL {job_url}: {e}")
            return jsonify({'success': False, 'message': 'Invalid LinkedIn job URL format'})
        
        logger.info(f"Extracting job details from LinkedIn URL: {job_url} (ID: {job_id})")
        
        # Fetch the job page
        try:
            response = requests.get(job_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }, timeout=30)
            
            if response.status_code != 200:
                logger.warning(f"Failed to fetch job page: HTTP {response.status_code}")
                return jsonify({'success': False, 'message': f'Failed to fetch job page (HTTP {response.status_code})'})
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching job page: {job_url}")
            return jsonify({'success': False, 'message': 'Timeout fetching job page. Please try again.'})
        except Exception as e:
            logger.error(f"Error fetching job page {job_url}: {e}")
            return jsonify({'success': False, 'message': f'Error fetching job page: {str(e)}'})
        
        # Parse job details from the HTML
        try:
            # Extract job description
            job_description = parse_linkedin_emails.parse_job_description(response.text)
            job_description = sanitize_text_for_yaml(job_description.strip() if job_description else '')
            
            # Try to extract basic job info from the HTML
            # This is a simplified extraction - the parse_linkedin_emails module 
            # is designed for email parsing, so we'll do basic HTML parsing here
            import re
            from html import unescape
            
            html_content = response.text
            
            # Extract job title
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
            if title_match:
                title = unescape(title_match.group(1))
                # Clean up LinkedIn's title format (usually "Job Title - Company Name | LinkedIn")
                title = re.sub(r'\s*\|\s*LinkedIn\s*$', '', title)
                title = re.sub(r'\s*-\s*[^-]+$', '', title)  # Remove company part
                title = title.strip()
            else:
                title = 'Job Title Not Found'
            
            # Extract company name
            company_match = re.search(r'"hiringOrganization":\s*{\s*"name":\s*"([^"]+)"', html_content)
            if not company_match:
                company_match = re.search(r'<span[^>]*class="[^"]*topcard__flavor[^"]*"[^>]*>([^<]+)</span>', html_content)
            
            if company_match:
                company = unescape(company_match.group(1)).strip()
            else:
                company = 'Company Not Found'
            
            # Extract location
            location_match = re.search(r'"jobLocation":\s*{\s*"address":\s*{\s*"addressLocality":\s*"([^"]+)"', html_content)
            if not location_match:
                location_match = re.search(r'<span[^>]*class="[^"]*topcard__flavor--bullet[^"]*"[^>]*>([^<]+)</span>', html_content)
            
            if location_match:
                location = unescape(location_match.group(1)).strip()
            else:
                location = 'Location Not Found'
            
            # Create job data structure
            job_data = {
                'id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'link': job_url,
                'description': job_description,
                'date_received': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'URL Entry'
            }
            
            # Sanitize all job data
            job_data = sanitize_job_data(job_data)
            
            logger.info(f"Successfully extracted job: {job_data['title']} at {job_data['company']}")
            
            return jsonify({
                'success': True,
                'message': 'Job details extracted successfully',
                'job_data': job_data
            })
            
        except Exception as e:
            logger.error(f"Error parsing job details from {job_url}: {e}", exc_info=True)
            return jsonify({'success': False, 'message': f'Error parsing job details: {str(e)}'})
            
    except Exception as e:
        logger.error(f"Error in extract_job_from_url: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': f'Error extracting job: {str(e)}'})

@app.route('/add_extracted_job_to_queue', methods=['POST'])
def add_extracted_job_to_queue():
    """Add extracted job data to the queue"""
    try:
        import yaml
        from datetime import datetime
        from step1_queue import sanitize_job_data, get_all_ids
        
        # Get JSON data from request
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        job_data = request_data.get('job_data')
        
        if not job_data:
            return jsonify({'success': False, 'message': 'No job data provided'})
        
        # Check if job ID already exists
        existing_ids = get_all_ids()
        job_id = job_data.get('id')
        
        if job_id in existing_ids:
            return jsonify({'success': False, 'message': f'Job with ID {job_id} already exists in the system'})
        
        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Clean company and title for filename
        def _sanitize_fn(s: str) -> str:
            if not s:
                return 'NA'
            # Apply text sanitization
            s = sanitize_text_for_yaml(s)
            # Replace path separators, dots and other unsafe chars with underscores
            out = re.sub(r'[\\/:*?"<>|.]+', '_', s)
            # Also replace control chars and other non-printables
            out = re.sub(r'[^\w\- ]+', '_', out)
            # Collapse whitespace to single space
            out = re.sub(r'\s+', ' ', out).strip()
            out = out.replace(' _ ', ' ')
            # Limit length
            return out[:200]
        
        company_clean = _sanitize_fn(job_data.get('company', 'Unknown'))
        title_clean = _sanitize_fn(job_data.get('title', 'Unknown'))
        
        # Create subfolder for this job in queued directory
        subfolder_name = f"{company_clean}.{title_clean}.{job_id}.{timestamp}"
        queued_dir = JOBS_DIR / '1_queued'
        job_subfolder = queued_dir / subfolder_name
        job_subfolder.mkdir(parents=True, exist_ok=True)
        
        # Prepare YAML data
        yaml_data = {
            'id': job_id,
            'company': job_data.get('company', 'Unknown'),
            'title': job_data.get('title', 'Unknown'),
            'location': job_data.get('location', 'Not specified'),
            'link': job_data.get('link', ''),
            'description': job_data.get('description', ''),
            'date_received': job_data.get('date_received', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'date_added': datetime.now().isoformat(),
            'source': 'URL Entry',
            'extracted_from_url': True
        }
        
        # Sanitize all data
        yaml_data = sanitize_job_data(yaml_data)
        
        # Save YAML file
        yaml_filename = f'{timestamp}.{job_id}.{company_clean}.{title_clean}.yaml'
        yaml_file_path = job_subfolder / yaml_filename
        
        with open(yaml_file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(yaml_data, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        logger.info(f"URL job entry created: {subfolder_name}")
        
        return jsonify({
            'success': True,
            'message': f'Job "{yaml_data["title"]}" at {yaml_data["company"]} added to queue successfully!',
            'folder_name': subfolder_name,
            'job_id': job_id
        })
        
    except Exception as e:
        logger.error(f"Error adding extracted job to queue: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': f'Error adding job to queue: {str(e)}'})

@app.route('/job/<folder_name>')
@app.route('/job/<phase>/<folder_name>')
def job_detail(folder_name, phase='generated'):
    """Detail page for a specific job"""
    
    # Determine which directory to look in based on phase
    phase_dirs = {
        'queued': JOBS_DIR / '1_queued',
        'generated': JOBS_DIR / '2_generated', 
        'applied': JOBS_DIR / '3_applied',
        'communications': JOBS_DIR / '4_communications',
        'interviews': JOBS_DIR / '5_interviews',
        'errors': JOBS_DIR / '8_errors',
        'expired': JOBS_DIR / '9_expired',
        'skipped': JOBS_DIR / '9_skipped'
    }
    
    if phase not in phase_dirs:
        flash(f'Invalid phase: {phase}', 'error')
        return redirect(url_for('index'))
    
    phase_dir = phase_dirs[phase]
    
    # For queued phase, handle both flat files and subfolders
    if phase == 'queued':
        # First try as a subfolder
        job_path = phase_dir / folder_name
        if job_path.exists() and job_path.is_dir():
            # It's a subfolder, proceed normally
            pass
        else:
            # Try as a flat file (legacy format)
            yaml_file_path = phase_dir / f"{folder_name}.yaml"
            if yaml_file_path.exists():
                # Create a temporary job_path for flat file handling
                job_path = phase_dir
                # We'll handle this case specially below
            else:
                flash(f'Job "{folder_name}" not found in {phase} directory', 'error')
                return redirect(url_for('index', phase=phase))
    else:
        # For other phases, look for the folder
        job_path = phase_dir / folder_name
        if not job_path.exists():
            flash(f'Job folder "{folder_name}" not found in {phase} directory', 'error')
            return redirect(url_for('index', phase=phase))
    
    # Handle flat file case for queued jobs
    if phase == 'queued' and not (phase_dir / folder_name).is_dir():
        # This is a flat file case
        yaml_file = phase_dir / f"{folder_name}.yaml"
        html_file = phase_dir / f"{folder_name}.html"
        
        if not yaml_file.exists():
            flash(f'Job YAML file "{folder_name}.yaml" not found', 'error')
            return redirect(url_for('index', phase=phase))
        
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                job_data = yaml.safe_load(f)
        except Exception as e:
            flash(f'Error loading job data: {e}', 'error')
            return redirect(url_for('index', phase=phase))
        
        # Get files for flat file case
        files = []
        if yaml_file.exists():
            files.append({
                'name': yaml_file.name,
                'path': yaml_file,
                'size': yaml_file.stat().st_size,
                'modified': datetime.fromtimestamp(yaml_file.stat().st_mtime),
                'is_html': False,
                'is_yaml': True
            })
        if html_file.exists():
            files.append({
                'name': html_file.name,
                'path': html_file,
                'size': html_file.stat().st_size,
                'modified': datetime.fromtimestamp(html_file.stat().st_mtime),
                'is_html': True,
                'is_yaml': False
            })
        
        return render_template('job_detail.html', 
                             version=VERSION,
                             folder_name=folder_name,
                             job_data=job_data,
                             yaml_file=yaml_file,
                             files=files,
                             phase=phase)
    
    # Handle directory case (subfolders)
    if not job_path.is_dir():
        flash(f'Job folder "{folder_name}" not found', 'error')
        return redirect(url_for('index', phase=phase))
    
    # Find YAML file in directory
    yaml_files = list(job_path.glob('*.yaml'))
    if not yaml_files:
        flash(f'No job YAML file found in "{folder_name}"', 'error')
        return redirect(url_for('index', phase=phase))
    
    yaml_file = yaml_files[0]
    
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            job_data = yaml.safe_load(f)
    except Exception as e:
        flash(f'Error loading job data: {e}', 'error')
        return redirect(url_for('index', phase=phase))
    
    # Get all files in the directory
    files = []
    for file_path in job_path.glob('*'):
        if file_path.is_file():
            files.append({
                'name': file_path.name,
                'path': file_path,
                'size': file_path.stat().st_size,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                'is_html': file_path.suffix.lower() == '.html',
                'is_yaml': file_path.suffix.lower() == '.yaml'
            })
    
    files.sort(key=lambda x: x['name'])
    
    return render_template('job_detail.html', 
                         version=VERSION,
                         folder_name=folder_name,
                         job_data=job_data,
                         yaml_file=yaml_file,
                         files=files,
                         phase=phase)

@app.route('/edit_job/<folder_name>', methods=['GET', 'POST'])
@app.route('/edit_job/<phase>/<folder_name>', methods=['GET', 'POST'])
def edit_job(folder_name, phase='generated'):
    """Edit job YAML data"""
    
    # Determine which directory to look in based on phase
    phase_dirs = {
        'queued': JOBS_DIR / '1_queued',
        'generated': JOBS_DIR / '2_generated', 
        'applied': JOBS_DIR / '3_applied',
        'communications': JOBS_DIR / '4_communications',
        'interviews': JOBS_DIR / '5_interviews',
        'errors': JOBS_DIR / '8_errors',
        'expired': JOBS_DIR / '9_expired',
        'skipped': JOBS_DIR / '9_skipped'
    }
    
    if phase not in phase_dirs:
        flash(f'Invalid phase: {phase}', 'error')
        return redirect(url_for('index'))
    
    phase_dir = phase_dirs[phase]
    
    # Handle both flat files and subfolders for queued phase
    if phase == 'queued':
        # First try as a subfolder
        job_path = phase_dir / folder_name
        if job_path.exists() and job_path.is_dir():
            yaml_files = list(job_path.glob('*.yaml'))
        else:
            # Try as a flat file (legacy format)
            yaml_file_path = phase_dir / f"{folder_name}.yaml"
            if yaml_file_path.exists():
                yaml_files = [yaml_file_path]
            else:
                yaml_files = []
    else:
        # For other phases, look for the folder
        job_path = phase_dir / folder_name
        if job_path.exists():
            yaml_files = list(job_path.glob('*.yaml'))
        else:
            yaml_files = []
    
    if not yaml_files:
        flash(f'Job "{folder_name}" not found in {phase} directory', 'error')
        return redirect(url_for('index', phase=phase))
    
    yaml_file = yaml_files[0]
    
    if request.method == 'POST':
        try:
            # Get the edited YAML content
            yaml_content = request.form['yaml_content']
            
            # Validate YAML syntax
            yaml.safe_load(yaml_content)
            
            # Save the file
            with open(yaml_file, 'w', encoding='utf-8') as f:
                f.write(yaml_content)
            
            flash('Job data updated successfully', 'success')
            logger.info(f"Updated job YAML file: {yaml_file}")
            return redirect(url_for('job_detail', folder_name=folder_name, phase=phase))
            
        except yaml.YAMLError as e:
            flash(f'Invalid YAML syntax: {e}', 'error')
        except Exception as e:
            flash(f'Error saving job data: {e}', 'error')
            logger.error(f"Error saving job YAML file {yaml_file}: {e}")
    
    # Load current content for editing
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_content = f.read()
    except Exception as e:
        flash(f'Error loading job data: {e}', 'error')
        return redirect(url_for('job_detail', folder_name=folder_name, phase=phase))
    
    return render_template('edit_job.html', 
                         version=VERSION,
                         folder_name=folder_name,
                         yaml_content=yaml_content,
                         phase=phase)

@app.route('/view_file/<folder_name>/<filename>')
@app.route('/view_file/<phase>/<folder_name>/<filename>')
def view_file(folder_name, filename, phase='generated'):
    """View HTML files in browser"""
    
    # Determine which directory to look in based on phase
    phase_dirs = {
        'queued': JOBS_DIR / '1_queued',
        'generated': JOBS_DIR / '2_generated', 
        'applied': JOBS_DIR / '3_applied',
        'communications': JOBS_DIR / '4_communications',
        'interviews': JOBS_DIR / '5_interviews',
        'errors': JOBS_DIR / '8_errors',
        'expired': JOBS_DIR / '9_expired',
        'skipped': JOBS_DIR / '9_skipped'
    }
    
    if phase not in phase_dirs:
        flash(f'Invalid phase: {phase}', 'error')
        return redirect(url_for('index'))
    
    phase_dir = phase_dirs[phase]
    
    # Handle both flat files and subfolders for queued phase
    if phase == 'queued':
        # First try as a subfolder
        job_path = phase_dir / folder_name
        if job_path.exists() and job_path.is_dir():
            file_path = job_path / filename
        else:
            # Try as a flat file (legacy format) - file is directly in phase_dir
            file_path = phase_dir / filename
    else:
        # For other phases, look in the folder
        file_path = phase_dir / folder_name / filename
    
    if not file_path.exists():
        flash(f'File "{filename}" not found', 'error')
        return redirect(url_for('job_detail', folder_name=folder_name, phase=phase))
    
    if file_path.suffix.lower() == '.html':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix the CSS path to point to our Flask route
            css_route = url_for('serve_css')
            content = content.replace('href="../../css/styles.css"', f'href="{css_route}"')
            
            return content
        except Exception as e:
            flash(f'Error reading file: {e}', 'error')
            return redirect(url_for('job_detail', folder_name=folder_name, phase=phase))
    else:
        flash('Only HTML files can be viewed in browser', 'warning')
        return redirect(url_for('job_detail', folder_name=folder_name, phase=phase))

@app.route('/mark_applied/<folder_name>', methods=['POST'])
def mark_applied(folder_name):
    """Mark job as applied and move to applied directory"""
    job_path = GENERATED_DIR / folder_name
    
    if not job_path.exists():
        return jsonify({'success': False, 'message': f'Job folder "{folder_name}" not found'})
    
    try:
        # Ensure applied directory exists
        APPLIED_DIR.mkdir(parents=True, exist_ok=True)
        
        # Move the entire directory
        destination = APPLIED_DIR / folder_name
        
        # If destination exists, add timestamp to make it unique
        if destination.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            destination = APPLIED_DIR / f"{folder_name}_{timestamp}"
        
        shutil.move(str(job_path), str(destination))
        
        logger.info(f"Moved job folder from {job_path} to {destination}")
        return jsonify({'success': True, 'message': f'Job marked as applied and moved to {destination.name}'})
        
    except Exception as e:
        logger.error(f"Error moving job folder {job_path}: {e}")
        return jsonify({'success': False, 'message': f'Error marking as applied: {e}'})

@app.route('/open_link/<folder_name>')
def open_link(folder_name):
    """Get the job link URL for opening in new tab"""
    job_path = GENERATED_DIR / folder_name
    
    if not job_path.exists():
        return jsonify({'success': False, 'message': 'Job not found'})
    
    yaml_files = list(job_path.glob('*.yaml'))
    if not yaml_files:
        return jsonify({'success': False, 'message': 'No job data found'})
    
    try:
        with open(yaml_files[0], 'r', encoding='utf-8') as f:
            job_data = yaml.safe_load(f)
        
        link = job_data.get('link')
        if link:
            return jsonify({'success': True, 'url': link})
        else:
            return jsonify({'success': False, 'message': 'No link found in job data'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error loading job data: {e}'})

@app.route('/view_custom_file/<folder_name>/<file_type>')
def view_custom_file(folder_name, file_type):
    """View custom resume or cover letter files"""
    job_path = GENERATED_DIR / folder_name
    
    if not job_path.exists():
        flash(f'Job folder "{folder_name}" not found', 'error')
        return redirect(url_for('index'))
    
    # Find the appropriate file
    if file_type == 'resume':
        pattern = '*.resume.html'
    elif file_type == 'coverletter':
        pattern = '*.coverletter.html'
    else:
        flash(f'Invalid file type: {file_type}', 'error')
        return redirect(url_for('job_detail', folder_name=folder_name))
    
    matching_files = list(job_path.glob(pattern))
    
    if not matching_files:
        flash(f'No {file_type} file found for this job', 'error')
        return redirect(url_for('job_detail', folder_name=folder_name))
    
    file_path = matching_files[0]  # Take the first matching file
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the CSS path to point to our Flask route
        # Replace relative CSS path with absolute Flask route
        css_route = url_for('serve_css')
        content = content.replace('href="../../css/styles.css"', f'href="{css_route}"')
        
        return content
    except Exception as e:
        flash(f'Error reading {file_type} file: {e}', 'error')
        return redirect(url_for('job_detail', folder_name=folder_name))

@app.route('/css/styles.css')
def serve_css():
    """Serve the CSS file for HTML previews"""
    css_path = JOBS_DIR / 'css' / 'styles.css'
    
    if not css_path.exists():
        return "/* CSS file not found */", 404, {'Content-Type': 'text/css'}
    
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        return css_content, 200, {'Content-Type': 'text/css'}
    except Exception as e:
        logger.error(f"Error serving CSS file: {e}")
        return f"/* Error loading CSS: {e} */", 500, {'Content-Type': 'text/css'}

@app.route('/resumes/icons/<filename>')
def serve_icons(filename):
    """Serve SVG icon files for HTML previews"""
    try:
        # Icons are in src/resources/icons/
        icon_path = BASE_DIR / 'resources' / 'icons' / filename
        
        if not icon_path.exists():
            logger.warning(f"Icon file not found: {icon_path}")
            return "Icon not found", 404
        
        # Only serve SVG files for security
        if not filename.lower().endswith('.svg'):
            logger.warning(f"Non-SVG file requested: {filename}")
            return "Only SVG files allowed", 403
        
        with open(icon_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        return svg_content, 200, {'Content-Type': 'image/svg+xml'}
        
    except Exception as e:
        logger.error(f"Error serving icon {filename}: {e}")
        return "Error loading icon", 500
        return f"Error loading icon: {e}", 500

@app.route('/reset_to_queued/<folder_name>', methods=['POST'])
def reset_to_queued(folder_name):
    """Reset job to queued state by moving original files back and cleaning up generated files"""
    job_path = GENERATED_DIR / folder_name
    
    if not job_path.exists():
        return jsonify({'success': False, 'message': f'Job folder "{folder_name}" not found'})
    
    try:
        # Ensure queued directory exists
        queued_dir = JOBS_DIR / '1_queued'
        queued_dir.mkdir(parents=True, exist_ok=True)
        
        # Find the original YAML and HTML files to move back
        yaml_files = list(job_path.glob('*.yaml'))
        original_html_files = list(job_path.glob('*.html'))
        
        # Filter to find the original job files (not generated resume/cover letter)
        original_yaml = None
        original_html = None
        
        for yaml_file in yaml_files:
            # Original YAML should not contain resume-specific names
            if not any(keyword in yaml_file.name.lower() for keyword in ['resume', 'coverletter', 'summary']):
                original_yaml = yaml_file
                break
        
        for html_file in original_html_files:
            # Original HTML should not be resume/coverletter/summary
            if not any(keyword in html_file.name.lower() for keyword in ['resume', 'coverletter', 'summary']):
                original_html = html_file
                break
        
        if not original_yaml:
            return jsonify({'success': False, 'message': 'Original YAML file not found'})
        
        # Create subfolder in queued directory using the same folder name structure
        # The folder_name should already be in format: Company.Position.id.timestamp
        queued_subfolder = queued_dir / folder_name
        queued_subfolder.mkdir(exist_ok=True)
        
        # Move original files back to queued subfolder
        files_moved = []
        
        # Move YAML file
        yaml_destination = queued_subfolder / original_yaml.name
        if yaml_destination.exists():
            yaml_destination.unlink()  # Remove existing file
        original_yaml.rename(yaml_destination)
        files_moved.append(original_yaml.name)
        
        # Move HTML file if it exists
        if original_html:
            html_destination = queued_subfolder / original_html.name
            if html_destination.exists():
                html_destination.unlink()  # Remove existing file
            original_html.rename(html_destination)
            files_moved.append(original_html.name)
        
        # Remove the entire job directory and all remaining files
        shutil.rmtree(job_path)
        
        logger.info(f"Reset job {folder_name} to queued: moved {files_moved} to subfolder, removed directory")
        return jsonify({
            'success': True, 
            'message': f'Job reset to queued. Moved {len(files_moved)} files back to queue subfolder and cleaned up generated files.'
        })
        
    except Exception as e:
        logger.error(f"Error resetting job {folder_name} to queued: {e}")
        return jsonify({'success': False, 'message': f'Error resetting job: {e}'})

@app.route('/move_job/<folder_name>/<destination>', methods=['POST'])
def move_job(folder_name, destination):
    """Move job folder to different directories based on status"""
    job_path = GENERATED_DIR / folder_name
    
    if not job_path.exists():
        return jsonify({'success': False, 'message': f'Job folder "{folder_name}" not found'})
    
    # Define destination directories
    destinations = {
        'applied': JOBS_DIR / '3_applied',
        'communications': JOBS_DIR / '4_communications', 
        'interviews': JOBS_DIR / '5_interviews',
        'skipped': JOBS_DIR / '9_skipped'
    }
    
    if destination not in destinations:
        return jsonify({'success': False, 'message': f'Invalid destination: {destination}'})
    
    try:
        dest_dir = destinations[destination]
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Move the entire directory
        final_destination = dest_dir / folder_name
        
        # If destination exists, add timestamp to make it unique
        if final_destination.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            final_destination = dest_dir / f"{folder_name}_{timestamp}"
        
        shutil.move(str(job_path), str(final_destination))
        
        # Create user-friendly messages
        messages = {
            'applied': 'marked as applied',
            'communications': 'moved to communications',
            'interviews': 'moved to interviews', 
            'skipped': 'skipped/hidden'
        }
        
        logger.info(f"Moved job folder from {job_path} to {final_destination}")
        return jsonify({
            'success': True, 
            'message': f'Job {messages[destination]} and moved to {final_destination.name}'
        })
        
    except Exception as e:
        logger.error(f"Error moving job folder {job_path} to {destination}: {e}")
        return jsonify({'success': False, 'message': f'Error moving job: {e}'})

@app.route('/regenerate_job/<folder_name>', methods=['POST'])
def regenerate_job(folder_name):
    """Regenerate resume and cover letter for a specific job"""
    
    # Look for the job in multiple directories (generated first, then queued)
    job_path = None
    for directory in [GENERATED_DIR, JOBS_DIR / '1_queued']:
        potential_path = directory / folder_name
        if potential_path.exists():
            job_path = potential_path
            break
    
    if not job_path:
        return jsonify({'success': False, 'message': f'Job folder "{folder_name}" not found in any directory'})
    
    try:
        # Get selected resume from form data (before starting background thread)
        selected_resume = request.form.get('selected_resume', 'Stephen_Hilton')  # Default fallback
        
        # Get additional prompt from request - handle case where no JSON is sent
        try:
            data = request.get_json() or {}
        except Exception:
            # If JSON parsing fails, use empty dict
            data = {}
        additional_prompt = data.get('additional_prompt', '').strip()
        
        # Find the job YAML file
        yaml_files = list(job_path.glob('*.yaml'))
        if not yaml_files:
            return jsonify({'success': False, 'message': 'No job YAML file found'})
        
        job_yaml = yaml_files[0]
        
        # Load job data to get the ID
        with open(job_yaml, 'r', encoding='utf-8') as f:
            job_data = yaml.safe_load(f)
        
        job_id = job_data.get('id')
        if not job_id:
            return jsonify({'success': False, 'message': 'No job ID found in YAML file'})
        
        # Move job to queued directory if it's not already there
        queued_dir = JOBS_DIR / '1_queued'
        queued_dir.mkdir(parents=True, exist_ok=True)
        
        if job_path.parent.name != '1_queued':
            # Job is in generated directory, need to move it to queued
            queued_destination = queued_dir / job_path.name
            if queued_destination.exists():
                import shutil
                shutil.rmtree(queued_destination)  # Remove existing directory
            
            # Move the entire job directory to queued
            import shutil
            shutil.move(str(job_path), str(queued_destination))
            logger.info(f"Moved job from {job_path} to {queued_destination} for regeneration")
        else:
            # Job is already in queued directory
            logger.info(f"Job {folder_name} is already in queued directory")
        
        # Import and call the generate function in a separate thread
        import threading
        import sys
        from pathlib import Path
        
        # Add the parent directory to sys.path to import step2_generate
        parent_dir = Path(__file__).parent.parent
        if str(parent_dir) not in sys.path:
            sys.path.append(str(parent_dir))
        
        def run_generation(selected_resume_param):
            try:
                import time
                start_time = time.time()
                
                logger.info(f"Background thread started for job ID {job_id}")
                
                # Set initial progress with detailed tracking
                app.config['job_regeneration_progress'] = {
                    'status': 'running',
                    'message': f'Starting AI regeneration for job ID {job_id}...',
                    'job_id': job_id,
                    'folder_name': folder_name,
                    'completed': False,
                    'error': None,
                    'phase': 'initializing',
                    'sections': {},
                    'start_time': start_time,
                    'elapsed_time': 0
                }
                
                # Try to use modular system first
                try:
                    logger.info(f"Attempting to use modular generation system for job ID {job_id}")
                    
                    # Update progress
                    app.config['job_regeneration_progress'].update({
                        'phase': 'loading_data',
                        'message': 'Loading job data and resume information...'
                    })
                    
                    # Load job data (use the job_path we already found)
                    current_job_path = job_path if job_path.parent.name == '1_queued' else JOBS_DIR / '1_queued' / folder_name
                    yaml_files = list(current_job_path.glob("*.yaml"))
                    
                    if not yaml_files:
                        raise Exception("No YAML file found for job data")
                    
                    import yaml
                    with open(yaml_files[0], 'r') as f:
                        job_data = yaml.safe_load(f)
                    
                    # Load resume data from the selected resume file
                    from step2_generate import load_resume_file
                    resume_data = load_resume_file(selected_resume_param)  # Use selected resume
                    
                    if not resume_data:
                        raise Exception("Could not load resume data")
                    
                    # Use modular generation system
                    from utils.modular_generator import ModularResumeGenerator
                    
                    modular_generator = ModularResumeGenerator()
                    
                    # Update progress
                    app.config['job_regeneration_progress'].update({
                        'phase': 'modular_generation',
                        'message': 'Starting modular AI generation...',
                        'sections': {
                            'summary': {'status': 'starting', 'progress': 0},
                            'skills': {'status': 'starting', 'progress': 0},
                            'experience': {'status': 'starting', 'progress': 0},
                            'education': {'status': 'starting', 'progress': 0},
                            'cover_letter': {'status': 'starting', 'progress': 0}
                        }
                    })
                    
                    logger.info(f"Starting modular generation for job ID {job_id}")
                    
                    # Generate using modular system with caching support
                    result = modular_generator.generate_resume(resume_data, job_data, job_id, str(current_job_path), use_cache=True)
                    
                    if not result.get('success'):
                        raise Exception(f"Modular generation failed: {result.get('error', 'Unknown error')}")
                    
                    logger.info(f"Modular generation completed successfully for job ID {job_id}")
                    
                    # Log cache information if available
                    cache_info = result.get('cache_info')
                    if cache_info:
                        cached_sections = cache_info.get('cached_sections', [])
                        logger.info(f"AI content cached for sections: {cached_sections}")
                    
                except Exception as modular_error:
                    logger.error(f"Modular generation failed: {modular_error}")
                    raise Exception(f"Generation failed: {str(modular_error)}")
                
                elapsed = time.time() - start_time
                logger.info(f"step2_generate.generate completed successfully for job ID {job_id} in {elapsed:.1f}s")
                
                # Set completion status
                app.config['job_regeneration_progress'] = {
                    'status': 'completed',
                    'message': f'AI regeneration completed successfully for job ID {job_id} in {elapsed:.1f}s',
                    'job_id': job_id,
                    'folder_name': folder_name,
                    'completed': True,
                    'error': None,
                    'phase': 'completed',
                    'sections': {
                        'resume': {'status': 'completed', 'progress': 1.0},
                        'cover_letter': {'status': 'completed', 'progress': 1.0},
                        'summary': {'status': 'completed', 'progress': 1.0}
                    },
                    'start_time': start_time,
                    'elapsed_time': elapsed,
                    'elapsed_formatted': f"{int(elapsed//60)}:{int(elapsed%60):02d}"
                }
                
            except Exception as e:
                elapsed = time.time() - start_time if 'start_time' in locals() else 0
                logger.error(f"Error in background generation for job ID {job_id}: {e}", exc_info=True)
                app.config['job_regeneration_progress'] = {
                    'status': 'error',
                    'message': f'AI regeneration failed after {elapsed:.1f}s: {str(e)}',
                    'job_id': job_id,
                    'folder_name': folder_name,
                    'completed': True,
                    'error': str(e),
                    'phase': 'error',
                    'sections': {},
                    'elapsed_time': elapsed
                }
        
        # Start generation in background thread
        generation_thread = threading.Thread(target=run_generation, args=(selected_resume,))
        generation_thread.daemon = True
        generation_thread.start()
        
        logger.info(f"Started regeneration for job ID {job_id} with additional prompt: '{additional_prompt}'")
        
        # Initialize progress tracking with detailed information
        import time
        app.config['job_regeneration_progress'] = {
            'status': 'starting',
            'message': f'Initializing AI regeneration for job ID {job_id}...',
            'job_id': job_id,
            'folder_name': folder_name,
            'completed': False,
            'error': None,
            'phase': 'starting',
            'sections': {},
            'start_time': time.time(),
            'elapsed_time': 0
        }
        
        return jsonify({
            'success': True, 
            'message': f'AI regeneration started for job ID {job_id}. This may take a minute to complete.'
        })
        
    except Exception as e:
        logger.error(f"Error starting regeneration for {folder_name}: {e}")
        return jsonify({'success': False, 'message': f'Error starting regeneration: {e}'})

@app.route('/get_available_resumes')
def get_available_resumes():
    """Get list of available resume files"""
    try:
        resumes_dir = Path("src/resumes")
        if not resumes_dir.exists():
            return jsonify({'resumes': [], 'error': 'Resumes directory not found'})
        
        resume_files = []
        for yaml_file in resumes_dir.glob("*.yaml"):
            # Get filename without extension
            resume_name = yaml_file.stem
            resume_files.append(resume_name)
        
        # Sort alphabetically
        resume_files.sort()
        
        return jsonify({
            'resumes': resume_files,
            'default': resume_files[0] if resume_files else None
        })
        
    except Exception as e:
        logger.error(f"Error getting available resumes: {str(e)}")
        return jsonify({'resumes': [], 'error': str(e)})

@app.route('/get_job_regeneration_progress')
def get_job_regeneration_progress():
    """Get current progress of job regeneration process"""
    try:
        # Get progress from app config
        progress = app.config.get('job_regeneration_progress', {
            'status': 'idle',
            'message': 'No job regeneration in progress',
            'job_id': None,
            'folder_name': None,
            'completed': False,
            'error': None,
            'sections': {},
            'phase': 'idle',
            'start_time': None,
            'elapsed_time': 0
        })
        
        # Add elapsed time calculation if job is running
        if progress.get('start_time') and not progress.get('completed'):
            elapsed = time.time() - progress['start_time']
            progress['elapsed_time'] = round(elapsed, 1)
            progress['elapsed_formatted'] = f"{int(elapsed//60)}:{int(elapsed%60):02d}"
        
        return jsonify({'success': True, 'progress': progress})
        
    except Exception as e:
        logger.error(f"Error getting job regeneration progress: {e}")
        return jsonify({
            'success': False, 
            'message': f'Error getting progress: {e}',
            'progress': {
                'status': 'error',
                'message': f'Progress tracking error: {e}',
                'job_id': None,
                'folder_name': None,
                'completed': True,
                'error': str(e),
                'sections': {},
                'phase': 'error'
            }
        })

@app.route('/get_summary/<folder_name>')
def get_summary(folder_name):
    """Get job summary content for accordion"""
    job_path = GENERATED_DIR / folder_name
    
    if not job_path.exists():
        return jsonify({'success': False, 'message': 'Job folder not found'})
    
    # Find summary file
    summary_files = list(job_path.glob('*.!SUMMARY.html'))
    
    if not summary_files:
        return jsonify({'success': False, 'message': 'No summary file found'})
    
    try:
        with open(summary_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean up the HTML content for display in accordion
        # Remove html, head, body tags if present and just get the content
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        if body_match:
            content = body_match.group(1)
        
        return jsonify({'success': True, 'content': content})
        
    except Exception as e:
        logger.error(f"Error reading summary file: {e}")
        return jsonify({'success': False, 'message': f'Error reading summary: {e}'})

@app.route('/run_step1_queue', methods=['POST'])
def run_step1_queue():
    """Run step1_queue.py to pull LinkedIn job alerts from email"""
    try:
        import threading
        import subprocess
        import sys
        from pathlib import Path
        
        def run_step1():
            try:
                # Run step1_queue.py script
                script_path = BASE_DIR / 'step1_queue.py'
                result = subprocess.run([sys.executable, str(script_path)], 
                                      capture_output=True, text=True, cwd=str(BASE_DIR))
                
                logger.info(f"Step1 queue completed with return code: {result.returncode}")
                if result.stdout:
                    logger.info(f"Step1 stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Step1 stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Error running step1_queue: {e}")
        
        # Start in background thread
        thread = threading.Thread(target=run_step1)
        thread.daemon = True
        thread.start()
        
        logger.info("Started step1_queue.py in background")
        return jsonify({
            'success': True, 
            'message': 'Started pulling LinkedIn job alerts from email. This may take a moment to complete.'
        })
        
    except Exception as e:
        logger.error(f"Error starting step1_queue: {e}")
        return jsonify({'success': False, 'message': f'Error starting email processing: {e}'})

@app.route('/run_step2_generate', methods=['POST'])
def run_step2_generate():
    """Run step2_generate.py to process jobs in queue"""
    try:
        import threading
        import subprocess
        import sys
        from pathlib import Path
        import time
        
        # First, clean up any duplicate jobs
        logger.info("Cleaning up duplicate jobs before processing")
        removed_count = cleanup_duplicate_jobs()
        if removed_count > 0:
            logger.info(f"Removed {removed_count} duplicate files before processing")
        
        # Store session start time for progress tracking
        session_start_time = time.time()
        
        # Clear any existing progress and set session start time
        app.config['step2_progress'] = {
            'status': 'starting',
            'message': 'Initializing job processing...',
            'current_job': 0,
            'total_jobs': 0,
            'current_job_name': '',
            'completed': False,
            'error': None,
            'session_start_time': session_start_time
        }
        
        def run_step2():
            try:
                # Update progress
                app.config['step2_progress']['status'] = 'running'
                app.config['step2_progress']['message'] = 'Starting AI resume generation...'
                
                # Run step2_generate.py script with real-time logging
                script_path = BASE_DIR / 'step2_generate.py'
                
                logger.info("🚀 STARTING STEP2_GENERATE.PY - Real-time logging enabled")
                logger.info(f"📂 Script path: {script_path}")
                logger.info(f"🌍 Working directory: {BASE_DIR}")
                
                # Use Popen for real-time output streaming
                import subprocess
                process = subprocess.Popen(
                    [sys.executable, str(script_path)], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT,  # Merge stderr into stdout
                    text=True, 
                    cwd=str(BASE_DIR),
                    bufsize=1,  # Line buffered
                    universal_newlines=True
                )
                
                # Stream output in real-time
                output_lines = []
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        output_lines.append(output.strip())
                        # Log each line immediately with subprocess prefix
                        logger.info(f"📋 SUBPROCESS: {output.strip()}")
                
                # Wait for process to complete
                return_code = process.poll()
                
                logger.info(f"✅ Process completed with return code: {return_code}")
                
                # Update final progress
                if return_code == 0:
                    app.config['step2_progress']['status'] = 'completed'
                    app.config['step2_progress']['message'] = 'Job processing completed successfully!'
                    app.config['step2_progress']['completed'] = True
                    logger.info("🎉 SUCCESS: All jobs processed successfully!")
                else:
                    app.config['step2_progress']['status'] = 'error'
                    app.config['step2_progress']['message'] = 'Job processing failed. Check logs for details.'
                    app.config['step2_progress']['error'] = f'Process exited with code {return_code}'
                    logger.error(f"❌ FAILED: Process exited with code {return_code}")
                    
            except Exception as e:
                logger.error(f"❌ Error running step2_generate: {e}")
                app.config['step2_progress']['status'] = 'error'
                app.config['step2_progress']['message'] = f'Error: {str(e)}'
                app.config['step2_progress']['error'] = str(e)
        
        # Start in background thread
        thread = threading.Thread(target=run_step2)
        thread.daemon = True
        thread.start()
        
        logger.info("Started step2_generate.py in background")
        
        return jsonify({
            'success': True, 
            'message': 'Started processing jobs in queue. Progress updates will be shown below.'
        })
        
    except Exception as e:
        logger.error(f"Error starting step2_generate: {e}")
        return jsonify({'success': False, 'message': f'Error starting job processing: {e}'})

@app.route('/process_single_job/<folder_name>', methods=['POST'])
def process_single_job(folder_name):
    """Process a single job by folder name"""
    try:
        import threading
        import subprocess
        import sys
        from pathlib import Path
        import time
        
        logger.info(f"Processing single job: {folder_name}")
        
        # Store session start time for progress tracking
        session_start_time = time.time()
        
        # Clear any existing progress and set session start time
        app.config['single_job_progress'] = {
            'status': 'starting',
            'message': f'Initializing processing for {folder_name}...',
            'folder_name': folder_name,
            'completed': False,
            'error': None,
            'session_start_time': session_start_time,
            'smart_cache_info': None  # Will be populated during processing
        }
        
        def run_single_job():
            job_id = None  # Initialize job_id at the start
            try:
                # Update progress
                app.config['single_job_progress']['status'] = 'running'
                app.config['single_job_progress']['message'] = f'Starting AI resume generation for {folder_name}...'
                
                print(f"\n🚀 STARTING SINGLE JOB PROCESSING: {folder_name}")
                print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
                
                # Extract job ID from folder name
                # Handle different folder name formats:
                # 1. Subfolder format: Company.Title.ID.Timestamp
                # 2. Flat file format: Timestamp.ID.Company.Title
                folder_parts = folder_name.split('.')
                
                logger.info(f"Folder name: {folder_name}, parts: {folder_parts}")
                print(f"🔍 Parsing folder: {folder_name}")
                print(f"📝 Folder parts: {folder_parts}")
                
                # Try to find the job ID from folder parts
                if len(folder_parts) >= 3:
                    # For flat file format: Timestamp.ID.Company.Title
                    # For subfolder format: Company.Title.ID.Timestamp
                    # LinkedIn job IDs are typically 10 digits, timestamps are 14 digits
                    
                    # First, look for a 10-digit number (typical LinkedIn job ID)
                    for i, part in enumerate(folder_parts):
                        if part.isdigit() and len(part) == 10:
                            job_id = part
                            logger.info(f"Found 10-digit job ID: {job_id} at position {i}")
                            print(f"✅ Found 10-digit job ID: {job_id} at position {i}")
                            break
                    
                    # If no 10-digit ID found, look for any 8+ digit number that's not 14 digits (timestamp)
                    if not job_id:
                        for i, part in enumerate(folder_parts):
                            if part.isdigit() and len(part) >= 8 and len(part) != 14:
                                job_id = part
                                logger.info(f"Found job ID: {job_id} at position {i}")
                                print(f"✅ Found job ID: {job_id} at position {i}")
                                break
                
                if not job_id:
                    # Try to find job ID by looking in the queued folder
                    queued_dir = JOBS_DIR / '1_queued'
                    print(f"🔍 Searching in queued directory: {queued_dir}")
                    
                    # Check if it's a subfolder
                    job_subfolder = queued_dir / folder_name
                    if job_subfolder.exists() and job_subfolder.is_dir():
                        # Look for YAML file in subfolder
                        yaml_files = list(job_subfolder.glob('*.yaml'))
                        if yaml_files:
                            yaml_file = yaml_files[0]
                            yaml_parts = yaml_file.stem.split('.')
                            logger.info(f"YAML file: {yaml_file.name}, parts: {yaml_parts}")
                            print(f"📄 Found YAML file: {yaml_file.name}")
                            print(f"📝 YAML parts: {yaml_parts}")
                            # Find the job ID in the YAML filename
                            for part in yaml_parts:
                                if part.isdigit() and len(part) >= 8:
                                    job_id = part
                                    logger.info(f"Found job ID from YAML: {job_id}")
                                    print(f"✅ Found job ID from YAML: {job_id}")
                                    break
                    
                    # If still not found, try flat file
                    if not job_id:
                        yaml_file = queued_dir / f"{folder_name}.yaml"
                        if yaml_file.exists():
                            yaml_parts = yaml_file.stem.split('.')
                            logger.info(f"Flat YAML file: {yaml_file.name}, parts: {yaml_parts}")
                            print(f"📄 Found flat YAML file: {yaml_file.name}")
                            print(f"📝 Flat YAML parts: {yaml_parts}")
                            # Find the job ID in the flat YAML filename
                            for part in yaml_parts:
                                if part.isdigit() and len(part) >= 8:
                                    job_id = part
                                    logger.info(f"Found job ID from flat YAML: {job_id}")
                                    print(f"✅ Found job ID from flat YAML: {job_id}")
                                    break
                
                if not job_id:
                    error_msg = f"Could not extract job ID from folder name: {folder_name}. Folder parts: {folder_parts}"
                    print(f"❌ ERROR: {error_msg}")
                    raise ValueError(error_msg)
                
                logger.info(f"Extracted job ID: {job_id} from folder: {folder_name}")
                print(f"🎯 Successfully extracted job ID: {job_id}")
                print(f"📋 Job ID: {job_id}")
                
                # Check if we need to create subfolder structure for flat files
                queued_dir = JOBS_DIR / '1_queued'
                job_subfolder = queued_dir / folder_name
                flat_yaml_file = queued_dir / f"{folder_name}.yaml"
                
                # If it's a flat file (not a subfolder), create the subfolder structure
                if flat_yaml_file.exists() and not job_subfolder.exists():
                    logger.info(f"Converting flat file to subfolder structure: {folder_name}")
                    print(f"📁 Creating subfolder structure for flat file: {folder_name}")
                    
                    # Create the subfolder
                    job_subfolder.mkdir(exist_ok=True)
                    
                    # Move the YAML file into the subfolder
                    new_yaml_path = job_subfolder / flat_yaml_file.name
                    flat_yaml_file.rename(new_yaml_path)
                    
                    logger.info(f"Moved {flat_yaml_file.name} to {new_yaml_path}")
                    print(f"✅ Moved {flat_yaml_file.name} to subfolder")
                
                # Run step2_generate.py script with specific job ID
                script_path = BASE_DIR / 'step2_generate.py'
                
                # Set environment variable to pass job ID
                env = os.environ.copy()
                env['RESUMEAI_SINGLE_JOB_ID'] = job_id
                
                print(f"🔧 Running step2_generate.py with job ID: {job_id}")
                print(f"📂 Script path: {script_path}")
                print(f"🌍 Environment: RESUMEAI_SINGLE_JOB_ID={job_id}")
                print(f"📁 Working directory: {BASE_DIR}")
                
                # Run with real-time output
                process = subprocess.Popen([
                    sys.executable, str(script_path)
                ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                   cwd=str(BASE_DIR), env=env, text=True, bufsize=1, universal_newlines=True)
                
                print(f"🚀 Process started with PID: {process.pid}")
                
                # Read output in real-time
                output_lines = []
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        output_lines.append(output.strip())
                        print(f"📋 SUBPROCESS: {output.strip()}")
                
                # Wait for process to complete
                return_code = process.poll()
                
                print(f"✅ Process completed with return code: {return_code}")
                logger.info(f"Single job processing completed with return code: {return_code}")
                
                # Get any remaining output
                remaining_output, _ = process.communicate()
                if remaining_output:
                    for line in remaining_output.split('\n'):
                        if line.strip():
                            output_lines.append(line.strip())
                            print(f"📋 SUBPROCESS: {line.strip()}")
                
                # Log all output
                full_output = '\n'.join(output_lines)
                if full_output:
                    logger.info(f"Single job stdout: {full_output}")
                
                # Update final progress
                if return_code == 0:
                    app.config['single_job_progress']['status'] = 'completed'
                    app.config['single_job_progress']['message'] = f'Job {folder_name} processed successfully!'
                    app.config['single_job_progress']['completed'] = True
                    print(f"🎉 SUCCESS: Job {folder_name} processed successfully!")
                else:
                    app.config['single_job_progress']['status'] = 'error'
                    app.config['single_job_progress']['message'] = f'Job {folder_name} processing failed with return code {return_code}'
                    app.config['single_job_progress']['error'] = f'Process exited with code {return_code}'
                    print(f"❌ ERROR: Job {folder_name} failed with return code {return_code}")
                    
            except Exception as e:
                error_msg = f"Error processing single job {folder_name}: {e}"
                logger.error(error_msg)
                print(f"❌ EXCEPTION: {error_msg}")
                if job_id:
                    print(f"📋 Job ID was: {job_id}")
                else:
                    print(f"📋 Job ID extraction failed")
                app.config['single_job_progress']['status'] = 'error'
                app.config['single_job_progress']['message'] = f'Error: {str(e)}'
                app.config['single_job_progress']['error'] = str(e)
        
        # Start in background thread
        thread = threading.Thread(target=run_single_job)
        thread.daemon = True
        thread.start()
        
        logger.info(f"Started processing single job {folder_name} in background")
        
        return jsonify({
            'success': True, 
            'message': f'Started processing job {folder_name}. This may take a few minutes.'
        })
        
    except Exception as e:
        logger.error(f"Error starting single job processing: {e}")
        return jsonify({'success': False, 'message': f'Error starting job processing: {e}'})

@app.route('/get_single_job_progress')
def get_single_job_progress():
    """Get current progress of single job processing"""
    try:
        import json
        import time
        
        # First check if there's a progress file from step2_generate.py
        progress_file = JOBS_DIR / '.step2_progress.json'
        
        if progress_file.exists():
            try:
                with open(progress_file, 'r') as f:
                    file_progress = json.load(f)
                
                # Check if the progress file is recent (within last 5 minutes)
                from datetime import datetime
                try:
                    file_timestamp = datetime.fromisoformat(file_progress.get('timestamp', ''))
                    age_seconds = (datetime.now() - file_timestamp).total_seconds()
                    
                    if age_seconds < 300:  # 5 minutes
                        # Use progress from file and add folder_name from stored progress
                        stored_progress = app.config.get('single_job_progress', {})
                        file_progress['folder_name'] = stored_progress.get('folder_name', '')
                        
                        logger.debug(f"Using single job progress from file: {file_progress['message']}")
                        return jsonify({'success': True, 'progress': file_progress})
                    else:
                        # File is too old, fall back to stored progress
                        logger.debug(f"Single job progress file is {age_seconds} seconds old, falling back to stored progress")
                except (ValueError, KeyError):
                    # Invalid timestamp, fall back to stored progress
                    logger.debug("Invalid timestamp in single job progress file, falling back to stored progress")
                    
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not read single job progress file: {e}")
        
        # Fall back to stored progress from app config
        progress = app.config.get('single_job_progress', {
            'status': 'idle',
            'message': 'No job processing in progress',
            'folder_name': '',
            'completed': False,
            'error': None
        })
        
        return jsonify({'success': True, 'progress': progress})
        
    except Exception as e:
        logger.error(f"Error getting single job progress: {e}", exc_info=True)
        return jsonify({
            'success': False, 
            'message': f'Error getting progress: {e}',
            'progress': {
                'status': 'error',
                'message': f'Progress tracking error: {e}',
                'folder_name': '',
                'completed': False,
                'error': str(e)
            }
        })

@app.route('/get_step2_progress')
def get_step2_progress():
    """Get current progress of step2_generate process"""
    try:
        import json
        import time
        
        # First check if there's a progress file from step2_generate.py
        progress_file = JOBS_DIR / '.step2_progress.json'
        
        if progress_file.exists():
            try:
                with open(progress_file, 'r') as f:
                    file_progress = json.load(f)
                
                # Check if the progress file is recent (within last 5 minutes)
                from datetime import datetime
                try:
                    file_timestamp = datetime.fromisoformat(file_progress.get('timestamp', ''))
                    age_seconds = (datetime.now() - file_timestamp).total_seconds()
                    
                    if age_seconds < 300:  # 5 minutes
                        # Use progress from file
                        logger.debug(f"Using progress from file: {file_progress['message']}")
                        return jsonify({'success': True, 'progress': file_progress})
                    else:
                        # File is too old, fall back to process checking
                        logger.debug(f"Progress file is {age_seconds} seconds old, falling back to process checking")
                except (ValueError, KeyError):
                    # Invalid timestamp, fall back to process checking
                    logger.debug("Invalid timestamp in progress file, falling back to process checking")
                    
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not read progress file: {e}")
        
        # Fall back to original process-based progress tracking
        current_time = time.time()
        
        # Check if step2_generate process is actually running
        try:
            import subprocess
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            step2_running = 'step2_generate.py' in result.stdout
        except Exception as ps_error:
            logger.warning(f"Could not check process status: {ps_error}")
            step2_running = False
        
        # Get progress from app config, or return default if not set
        progress = app.config.get('step2_progress', {
            'status': 'idle',
            'message': 'No processing in progress',
            'current_job': 0,
            'total_jobs': 0,
            'current_job_name': '',
            'completed': False,
            'error': None,
            'progress_percent': 0
        })
        
        # If we think process is running but it's not actually running, update status
        if progress['status'] == 'running' and not step2_running:
            progress['status'] = 'completed'
            progress['message'] = 'Job processing completed (process finished)'
            progress['completed'] = True
            progress['progress_percent'] = 100
            app.config['step2_progress'] = progress
        
        # If process is actually running, get real-time progress by checking files
        if step2_running and progress['status'] in ['starting', 'running']:
            # Count jobs in queue vs generated to estimate progress
            queued_dir = JOBS_DIR / '1_queued'
            generated_dir = JOBS_DIR / '2_generated'
            
            # Count current queued jobs
            queued_count = 0
            if queued_dir.exists():
                # Count both flat YAML files (legacy) and subfolders (new format)
                flat_files = len([f for f in queued_dir.glob('*.yaml') if f.is_file()])
                subfolders = len([d for d in queued_dir.iterdir() if d.is_dir()])
                queued_count = flat_files + subfolders
            
            # Get initial job count from when processing started
            initial_queued_count = progress.get('initial_queued_count', queued_count)
            if 'initial_queued_count' not in progress:
                # First time - store the initial count
                progress['initial_queued_count'] = queued_count
                initial_queued_count = queued_count
            
            # Calculate jobs processed (initial count - current count)
            jobs_processed = max(0, initial_queued_count - queued_count)
            total_jobs = initial_queued_count
            
            # Get recently modified directories in generated (indicates recent processing)
            recent_dirs = []
            current_job_name = ''
            if generated_dir.exists():
                for item in generated_dir.iterdir():
                    if item.is_dir():
                        # Check if modified recently (within last 10 minutes)
                        if current_time - item.stat().st_mtime < (10 * 60):
                            recent_dirs.append(item)
            
            # Update progress with real-time info
            progress['status'] = 'running'
            progress['current_job'] = jobs_processed
            progress['total_jobs'] = total_jobs
            
            if recent_dirs:
                # Sort by modification time, get most recent
                recent_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                latest_dir = recent_dirs[0]
                
                # Try to extract company name from directory
                dir_parts = latest_dir.name.split('.')
                if len(dir_parts) >= 1:
                    company_name = dir_parts[0].replace('_', ' ')
                    progress['current_job_name'] = company_name
                    current_job_name = company_name
                    progress['message'] = f'Processing job for {company_name}... ({queued_count} remaining in queue)'
                else:
                    progress['message'] = f'Processing jobs... ({queued_count} remaining in queue)'
            else:
                progress['message'] = f'Processing jobs... ({queued_count} remaining in queue)'
            
            # Calculate progress percentage
            if total_jobs > 0:
                progress_percent = int((jobs_processed / total_jobs) * 100)
                progress['progress_percent'] = progress_percent
            else:
                progress['progress_percent'] = 0
            
            # Check if processing is complete (no more queued jobs)
            if queued_count == 0 and jobs_processed > 0:
                progress['status'] = 'completed'
                progress['message'] = 'Job processing completed!'
                progress['completed'] = True
                progress['progress_percent'] = 100
            
            # Update the stored progress
            app.config['step2_progress'] = progress
        
        return jsonify({'success': True, 'progress': progress})
        
    except Exception as e:
        logger.error(f"Error getting step2 progress: {e}", exc_info=True)
        return jsonify({
            'success': False, 
            'message': f'Error getting progress: {e}',
            'progress': {
                'status': 'error',
                'message': f'Progress tracking error: {e}',
                'current_job': 0,
                'total_jobs': 0,
                'current_job_name': '',
                'completed': False,
                'error': str(e),
                'progress_percent': 0
            }
        })

@app.route('/run_main', methods=['POST'])
def run_main():
    """Run main.py to do all processing steps"""
    try:
        import threading
        import subprocess
        import sys
        from pathlib import Path
        
        def run_main():
            try:
                # Run main.py script
                script_path = BASE_DIR / 'main.py'
                result = subprocess.run([sys.executable, str(script_path)], 
                                      capture_output=True, text=True, cwd=str(BASE_DIR))
                
                logger.info(f"Main script completed with return code: {result.returncode}")
                if result.stdout:
                    logger.info(f"Main stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Main stderr: {result.stderr}")
                    
            except Exception as e:
                logger.error(f"Error running main.py: {e}")
        
        # Start in background thread
        thread = threading.Thread(target=run_main)
        thread.daemon = True
        thread.start()
        
        logger.info("Started main.py in background")
        return jsonify({
            'success': True, 
            'message': 'Started full ResumeAI processing pipeline. This may take several minutes to complete.'
        })
        
    except Exception as e:
        logger.error(f"Error starting main.py: {e}")
        return jsonify({'success': False, 'message': f'Error starting full processing: {e}'})

@app.route('/regenerate_pdfs', methods=['POST'])
def regenerate_pdfs():
    """Regenerate PDFs from existing HTML files in generated directory"""
    try:
        import threading
        import sys
        from pathlib import Path
        
        def run_pdf_regeneration():
            try:
                # Import PDF manager
                from utils.pdf_mgr import PDFManager
                
                # Initialize PDF manager
                pdf_manager = PDFManager()
                
                # Find all HTML files in generated directory
                generated_dir = JOBS_DIR / '2_generated'
                html_files = pdf_manager.find_html_files(generated_dir)
                
                logger.info(f"Found {len(html_files)} HTML files to convert to PDF")
                
                if html_files:
                    # Convert all HTML files to PDF
                    result = pdf_manager.convert_multiple_files(html_files)
                    
                    # Store result in app config for progress tracking
                    app.config['pdf_regeneration_result'] = result
                    
                    logger.info(f"PDF regeneration completed: {result['message']}")
                else:
                    app.config['pdf_regeneration_result'] = {
                        'success': True,
                        'message': 'No HTML files found to convert',
                        'converted': 0,
                        'failed': 0
                    }
                    logger.info("No HTML files found for PDF regeneration")
                    
            except Exception as e:
                logger.error(f"Error during PDF regeneration: {e}", exc_info=True)
                app.config['pdf_regeneration_result'] = {
                    'success': False,
                    'message': f'PDF regeneration failed: {str(e)}',
                    'converted': 0,
                    'failed': 0,
                    'error': str(e)
                }
        
        # Start PDF regeneration in background thread
        thread = threading.Thread(target=run_pdf_regeneration)
        thread.daemon = True
        thread.start()
        
        # Initialize progress tracking
        app.config['pdf_regeneration_result'] = {
            'success': None,  # None means still running
            'message': 'Starting PDF regeneration...',
            'converted': 0,
            'failed': 0
        }
        
        logger.info("Started PDF regeneration in background")
        return jsonify({
            'success': True, 
            'message': 'Started PDF regeneration. This may take a few minutes to complete.'
        })
        
    except Exception as e:
        logger.error(f"Error starting PDF regeneration: {e}")
        return jsonify({'success': False, 'message': f'Error starting PDF regeneration: {e}'})

@app.route('/regenerate_html_only/<folder_name>', methods=['POST'])
def regenerate_html_only(folder_name):
    """Regenerate HTML files (resume + cover letter) from cached AI content without AI calls"""
    try:
        import yaml
        from pathlib import Path
        
        # Import the new regeneration function
        try:
            from step2_generate import regenerate_html_from_cached_content
        except ImportError:
            from src.step2_generate import regenerate_html_from_cached_content
        
        # Find the job folder
        job_path = JOBS_DIR / '2_generated' / folder_name
        
        if not job_path.exists():
            return jsonify({
                'success': False,
                'message': f'Job folder not found: {folder_name}'
            })
        
        # Find YAML file for job data
        yaml_files = list(job_path.glob("*.yaml"))
        if not yaml_files:
            return jsonify({
                'success': False,
                'message': 'No YAML file found in job folder'
            })
        
        yaml_file = yaml_files[0]
        logger.info(f"Regenerating HTML from cached AI content: {yaml_file.name}")
        
        # Load job data
        with open(yaml_file, 'r') as f:
            job_data = yaml.safe_load(f)
        
        # Load resume data
        try:
            from step2_generate import load_resume_file
            resume_data = load_resume_file('Stephen_Hilton')
        except ImportError:
            from src.step2_generate import load_resume_file
            resume_data = load_resume_file('Stephen_Hilton')
        
        # Use the new caching-aware regeneration function
        result = regenerate_html_from_cached_content(str(job_path), job_data, resume_data)
        
        if result.get('success'):
            # Save the regenerated HTML files
            files_generated = []
            
            # Save resume HTML
            if result.get('html_resume'):
                resume_file = job_path / f"{yaml_file.stem}.resume.html"
                with open(resume_file, 'w', encoding='utf-8') as f:
                    f.write(result['html_resume'])
                files_generated.append('resume.html')
                logger.info(f"Resume HTML regenerated from cache: {resume_file.name}")
            
            # Save cover letter HTML
            if result.get('html_cover_letter'):
                cover_letter_file = job_path / f"{yaml_file.stem}.coverletter.html"
                with open(cover_letter_file, 'w', encoding='utf-8') as f:
                    f.write(result['html_cover_letter'])
                files_generated.append('coverletter.html')
                logger.info(f"Cover letter HTML regenerated from cache: {cover_letter_file.name}")
            
            # Also regenerate PDFs if available
            if result.get('pdf_results'):
                files_generated.extend(['resume.pdf', 'coverletter.pdf'])
            
            cache_info = result.get('cache_info', {})
            cached_sections = cache_info.get('cached_sections', [])
            
            return jsonify({
                'success': True,
                'message': f'Generated from cached AI content: {", ".join(files_generated)}',
                'cached_sections': cached_sections,
                'generation_method': result.get('generation_method', 'cached_content')
            })
        else:
            # Fallback to legacy method if no cached content
            logger.warning("No cached AI content found, falling back to legacy regeneration")
            return self._regenerate_html_legacy(job_path, yaml_file, job_data)
            
    except Exception as e:
        logger.error(f"Error in HTML-only regeneration for {folder_name}: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

def _regenerate_html_legacy(job_path, yaml_file, job_data):
    """Legacy HTML regeneration method (fallback when no cached content)"""
    try:
        # Import template engine
        try:
            from utils.template_engine import TemplateEngine
        except ImportError:
            from src.utils.template_engine import TemplateEngine
        
        # Initialize template engine
        template_engine = TemplateEngine()
        
        # Extract content sections from YAML
        content_data = {
            'name': job_data.get('resume', {}).get('name', 'Name Not Found'),
            'email': job_data.get('resume', {}).get('email', ''),
            'phone': job_data.get('resume', {}).get('phone', ''),
            'location': job_data.get('resume', {}).get('location', ''),
            'summary': job_data.get('resume', {}).get('summary', ''),
            'skills': job_data.get('resume', {}).get('skills', {}),
            'experience': job_data.get('resume', {}).get('experience', []),
            'education': job_data.get('resume', {}).get('education', []),
            'awards': job_data.get('resume', {}).get('awards', []),
            'cover_letter': job_data.get('cover_letter', {})
        }
        
        files_generated = []
        
        # Generate resume HTML
        try:
            resume_html = template_engine.render_resume(content_data)
            resume_file = job_path / f"{yaml_file.stem}.resume.html"
            
            with open(resume_file, 'w', encoding='utf-8') as f:
                f.write(resume_html)
            files_generated.append('resume.html')
            logger.info(f"Resume HTML regenerated (legacy): {resume_file.name}")
        except Exception as e:
            logger.error(f"Error generating resume HTML: {e}")
        
        # Generate cover letter HTML
        try:
            cover_letter_html = template_engine.render_cover_letter(content_data, job_data)
            cover_letter_file = job_path / f"{yaml_file.stem}.coverletter.html"
            
            with open(cover_letter_file, 'w', encoding='utf-8') as f:
                f.write(cover_letter_html)
            files_generated.append('coverletter.html')
            logger.info(f"Cover letter HTML regenerated (legacy): {cover_letter_file.name}")
        except Exception as e:
            logger.error(f"Error generating cover letter HTML: {e}")
        
        if files_generated:
            return jsonify({
                'success': True,
                'message': f'Generated (legacy method): {", ".join(files_generated)}',
                'generation_method': 'legacy_fallback'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to generate any HTML files'
            })
            
    except Exception as e:
        logger.error(f"Error in legacy HTML regeneration: {e}")
        return jsonify({
            'success': False,
            'message': f'Legacy regeneration error: {str(e)}'
        })

@app.route('/regenerate_job_pdfs/<folder_name>', methods=['POST'])
def regenerate_job_pdfs(folder_name):
    """Regenerate PDFs for a specific job from existing HTML files"""
    try:
        import sys
        from pathlib import Path
        
        # Import PDF manager
        from utils.pdf_mgr import PDFManager
        
        # Initialize PDF manager
        pdf_manager = PDFManager()
        
        # Check if any PDF engines are available
        engine_info = pdf_manager.get_engine_info()
        logger.info(f"PDF engine check for job {folder_name}: {engine_info['total_available']} engines available, preferred: {engine_info['preferred_engine']}")
        
        # Debug: Log detailed engine status
        for engine, details in engine_info['available_engines'].items():
            status = "available" if details.get('available', False) else "unavailable"
            logger.info(f"Engine {engine}: {status} - {details.get('description', details.get('error', 'Unknown'))}")
        
        if engine_info['total_available'] == 0:
            error_msg = "WeasyPrint PDF engine is not available. Please install the required dependencies:\n"
            for engine, details in engine_info['available_engines'].items():
                if not details.get('available', False):
                    error_msg += f"• {details.get('error', 'Unknown error')}\n"
            
            logger.error(f"WeasyPrint not available for job {folder_name}: {error_msg}")
            return jsonify({'success': False, 'message': error_msg.strip()})
        
        # Find the job directory
        job_path = GENERATED_DIR / folder_name
        
        if not job_path.exists() or not job_path.is_dir():
            return jsonify({'success': False, 'message': f'Job folder "{folder_name}" not found'})
        
        # Find HTML files in this specific job directory
        html_files = []
        for html_file in job_path.glob('*.html'):
            # Only include resume and cover letter files (not summary)
            if any(file_type in html_file.name.lower() for file_type in ['resume', 'coverletter']):
                html_files.append(html_file)
        
        if not html_files:
            return jsonify({'success': False, 'message': 'No HTML files found for this job'})
        
        logger.info(f"Regenerating PDFs for job {folder_name}: found {len(html_files)} HTML files using {pdf_manager.preferred_engine}")
        
        # Convert HTML files to PDF
        result = pdf_manager.convert_multiple_files(html_files)
        
        if result['success']:
            message = f"Successfully regenerated {result['converted']} PDF files for this job"
            if result['failed'] > 0:
                message += f" ({result['failed']} failed)"
            
            logger.info(f"PDF regeneration completed for job {folder_name}: {message}")
            return jsonify({'success': True, 'message': message})
        else:
            # Provide detailed error information
            error_details = []
            if result.get('results'):
                for file_result in result['results']:
                    if not file_result.get('success', False):
                        file_name = Path(file_result.get('file', 'unknown')).name
                        error = file_result.get('error', 'Unknown error')
                        error_details.append(f"{file_name}: {error}")
            
            if error_details:
                detailed_message = f"PDF regeneration failed:\n" + "\n".join(error_details)
            else:
                detailed_message = result.get('message', 'PDF regeneration failed for unknown reasons')
            
            logger.error(f"PDF regeneration failed for job {folder_name}: {detailed_message}")
            return jsonify({'success': False, 'message': detailed_message})
        
    except Exception as e:
        logger.error(f"Error regenerating PDFs for job {folder_name}: {e}", exc_info=True)
        return jsonify({'success': False, 'message': f'Error regenerating PDFs: {str(e)}'})

@app.route('/get_pdf_regeneration_progress')
def get_pdf_regeneration_progress():
    """Get current progress of PDF regeneration process"""
    try:
        # Get progress from app config
        result = app.config.get('pdf_regeneration_result', {
            'success': None,
            'message': 'No PDF regeneration in progress',
            'converted': 0,
            'failed': 0
        })
        
        # Check if process is still running
        if result.get('success') is None:
            status = 'running'
            completed = False
        elif result.get('success') is True:
            status = 'completed'
            completed = True
        else:
            status = 'error'
            completed = True
        
        progress_data = {
            'status': status,
            'message': result.get('message', 'Processing...'),
            'converted': result.get('converted', 0),
            'failed': result.get('failed', 0),
            'completed': completed,
            'error': result.get('error', None)
        }
        
        return jsonify({'success': True, 'progress': progress_data})
        
    except Exception as e:
        logger.error(f"Error getting PDF regeneration progress: {e}")
        return jsonify({
            'success': False, 
            'message': f'Error getting progress: {e}',
            'progress': {
                'status': 'error',
                'message': f'Progress tracking error: {e}',
                'converted': 0,
                'failed': 0,
                'completed': True,
                'error': str(e)
            }
        })

@app.route('/pdf_engine_status')
def pdf_engine_status():
    """Get PDF engine status for debugging"""
    try:
        import sys
        from pathlib import Path
        
        # Import PDF manager
        from utils.pdf_mgr import PDFManager
        
        # Initialize PDF manager
        pdf_manager = PDFManager()
        engine_info = pdf_manager.get_engine_info()
        
        # Test WeasyPrint directly
        weasyprint_test = "unknown"
        try:
            from weasyprint import HTML
            test_html = HTML(string='<html><body><p>Test</p></body></html>')
            pdf_bytes = test_html.write_pdf()
            weasyprint_test = f"working ({len(pdf_bytes)} bytes)"
        except Exception as e:
            weasyprint_test = f"failed: {str(e)}"
        
        return jsonify({
            'success': True,
            'total_available': engine_info['total_available'],
            'preferred_engine': engine_info['preferred_engine'],
            'engines': engine_info['available_engines'],
            'weasyprint_direct_test': weasyprint_test,
            'python_executable': sys.executable,
            'working_directory': str(Path.cwd()),
            'virtual_env': sys.path[0] if sys.path else 'unknown'
        })
        
    except Exception as e:
        logger.error(f"Error getting PDF engine status: {e}")
        return jsonify({
            'success': False,
            'message': f'Error checking PDF engines: {str(e)}'
        })

def cleanup_duplicate_jobs():
    """
    Remove duplicate job files from the queue if they already exist in other job directories.
    Now handles both flat files (legacy) and subfolder structure in queued directory.
    Returns the number of files cleaned up.
    """
    try:
        jobs_dir = Path(__file__).parent.parent / 'jobs'
        queued_dir = jobs_dir / '1_queued'
        
        if not queued_dir.exists():
            return 0
        
        # Get all job IDs that exist in other directories (not queued)
        existing_job_ids = set()
        
        for subdir in jobs_dir.iterdir():
            if subdir.is_dir() and subdir.name != '1_queued':
                # Check both files and subdirectories
                for item in subdir.rglob('*.yaml'):
                    # Extract job ID from filename (format: timestamp.id.company.title.yaml)
                    filename_parts = item.stem.split('.')
                    if len(filename_parts) >= 2:
                        job_id = filename_parts[1]
                        existing_job_ids.add(job_id)
        
        # Check queued files for duplicates - handle both flat files and subfolders
        files_to_remove = []
        subfolders_to_remove = []
        
        # Check flat files (legacy format)
        queued_files = list(queued_dir.glob('*.yaml'))
        for yaml_file in queued_files:
            filename_parts = yaml_file.stem.split('.')
            if len(filename_parts) >= 2:
                job_id = filename_parts[1]
                if job_id in existing_job_ids:
                    files_to_remove.append(yaml_file)
                    # Also remove corresponding HTML file if it exists
                    html_file = yaml_file.with_suffix('.html')
                    if html_file.exists():
                        files_to_remove.append(html_file)
        
        # Check subfolders (new format)
        for subfolder in queued_dir.iterdir():
            if subfolder.is_dir():
                # Check if any YAML files in this subfolder have duplicate job IDs
                yaml_files_in_subfolder = list(subfolder.glob('*.yaml'))
                for yaml_file in yaml_files_in_subfolder:
                    filename_parts = yaml_file.stem.split('.')
                    if len(filename_parts) >= 2:
                        job_id = filename_parts[1]
                        if job_id in existing_job_ids:
                            # Mark entire subfolder for removal
                            subfolders_to_remove.append(subfolder)
                            break  # No need to check other files in this subfolder
        
        # Remove duplicate files
        removed_count = 0
        for file_to_remove in files_to_remove:
            try:
                file_to_remove.unlink()
                logger.debug(f"Removed duplicate file: {file_to_remove.name}")
                removed_count += 1
            except Exception as e:
                logger.error(f"Error removing file {file_to_remove}: {e}")
        
        # Remove duplicate subfolders
        for subfolder_to_remove in subfolders_to_remove:
            try:
                import shutil
                shutil.rmtree(subfolder_to_remove)
                logger.debug(f"Removed duplicate subfolder: {subfolder_to_remove.name}")
                removed_count += 1  # Count as one removal per subfolder
            except Exception as e:
                logger.error(f"Error removing subfolder {subfolder_to_remove}: {e}")
        
        if removed_count > 0:
            logger.debug(f"Cleanup completed: removed {removed_count} duplicate files/folders")
        
        return removed_count
        
    except Exception as e:
        logger.error(f"Error in cleanup_duplicate_jobs: {e}")
        return 0


@app.route('/view_summary/<folder_name>')
def view_summary(folder_name):
    """View job summary HTML file"""
    try:
        folder_path = JOBS_DIR / '2_generated' / folder_name
        if not folder_path.exists():
            flash(f'Job folder not found: {folder_name}', 'error')
            return redirect(url_for('index'))
        
        # Find summary file with pattern *.!SUMMARY.html
        summary_files = list(folder_path.glob('*.!SUMMARY.html'))
        if not summary_files:
            flash(f'Summary file not found for {folder_name}', 'error')
            return redirect(url_for('job_detail', folder_name=folder_name))
        
        summary_file = summary_files[0]  # Take the first match
        
        # Read and serve the HTML content
        html_content = summary_file.read_text(encoding='utf-8')
        
        # Add CSS link if not present
        if 'styles.css' not in html_content and '<head>' in html_content:
            css_link = '<link rel="stylesheet" href="/css/styles.css">'
            html_content = html_content.replace('<head>', f'<head>\n    {css_link}')
        
        return html_content
        
    except Exception as e:
        logger.error(f"Error viewing summary for {folder_name}: {e}")
        flash(f'Error loading summary: {e}', 'error')
        return redirect(url_for('job_detail', folder_name=folder_name))

@app.route('/mark_communications/<folder_name>', methods=['POST'])
def mark_communications(folder_name):
    """Mark job as in communications and move to communications directory"""
    try:
        source_path = JOBS_DIR / '2_generated' / folder_name
        if not source_path.exists():
            return jsonify({'success': False, 'message': f'Job folder not found: {folder_name}'})
        
        # Create communications directory if it doesn't exist
        communications_dir = JOBS_DIR / '4_communications'
        communications_dir.mkdir(exist_ok=True)
        
        # Move folder to communications
        dest_path = communications_dir / folder_name
        if dest_path.exists():
            import shutil
            shutil.rmtree(dest_path)
        
        source_path.rename(dest_path)
        
        logger.info(f"Marked job as in communications: {folder_name}")
        return jsonify({'success': True, 'message': f'Job {folder_name} marked as in communications'})
        
    except Exception as e:
        logger.error(f"Error marking job as communications {folder_name}: {e}")
        return jsonify({'success': False, 'message': f'Error marking as communications: {e}'})

@app.route('/mark_interviewing/<folder_name>', methods=['POST'])
def mark_interviewing(folder_name):
    """Mark job as interviewing and move to interviews directory"""
    try:
        source_path = JOBS_DIR / '2_generated' / folder_name
        if not source_path.exists():
            return jsonify({'success': False, 'message': f'Job folder not found: {folder_name}'})
        
        # Create interviews directory if it doesn't exist
        interviews_dir = JOBS_DIR / '5_interviews'
        interviews_dir.mkdir(exist_ok=True)
        
        # Move folder to interviews
        dest_path = interviews_dir / folder_name
        if dest_path.exists():
            import shutil
            shutil.rmtree(dest_path)
        
        source_path.rename(dest_path)
        
        logger.info(f"Marked job as interviewing: {folder_name}")
        return jsonify({'success': True, 'message': f'Job {folder_name} marked as interviewing'})
        
    except Exception as e:
        logger.error(f"Error marking job as interviewing {folder_name}: {e}")
        return jsonify({'success': False, 'message': f'Error marking as interviewing: {e}'})

@app.route('/mark_expired/<folder_name>', methods=['POST'])
def mark_expired(folder_name):
    """Mark job as expired and move to expired directory"""
    try:
        source_path = JOBS_DIR / '2_generated' / folder_name
        if not source_path.exists():
            return jsonify({'success': False, 'message': f'Job folder not found: {folder_name}'})
        
        # Create expired directory if it doesn't exist
        expired_dir = JOBS_DIR / '9_expired'
        expired_dir.mkdir(exist_ok=True)
        
        # Move folder to expired
        dest_path = expired_dir / folder_name
        if dest_path.exists():
            import shutil
            shutil.rmtree(dest_path)
        
        source_path.rename(dest_path)
        
        logger.info(f"Marked job as expired: {folder_name}")
        return jsonify({'success': True, 'message': f'Job {folder_name} marked as expired'})
        
    except Exception as e:
        logger.error(f"Error marking job as expired {folder_name}: {e}")
        return jsonify({'success': False, 'message': f'Error marking as expired: {e}'})

@app.route('/view_pdf/<folder_name>/<file_type>')
def view_pdf(folder_name, file_type):
    """Serve existing PDF file for viewing in browser"""
    try:
        folder_path = JOBS_DIR / '2_generated' / folder_name
        if not folder_path.exists():
            flash(f'Job folder not found: {folder_name}', 'error')
            return redirect(url_for('index'))
        
        # Find the PDF file
        pdf_files = list(folder_path.glob(f'*.{file_type}.pdf'))
        if not pdf_files:
            flash(f'No {file_type} PDF file found for {folder_name}', 'error')
            return redirect(url_for('job_detail', folder_name=folder_name))
        
        pdf_file = pdf_files[0]
        
        # Read and serve the PDF
        pdf_content = pdf_file.read_bytes()
        
        # Create response for viewing (not downloading)
        response = make_response(pdf_content)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename="{pdf_file.name}"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error serving PDF for {folder_name}/{file_type}: {e}")
        flash(f'Error loading PDF: {e}', 'error')
        return redirect(url_for('job_detail', folder_name=folder_name))

@app.route('/download_pdf/<folder_name>/<file_type>')
def download_pdf(folder_name, file_type):
    """Generate and download PDF for resume or cover letter"""
    try:
        folder_path = JOBS_DIR / '2_generated' / folder_name
        if not folder_path.exists():
            flash(f'Job folder not found: {folder_name}', 'error')
            return redirect(url_for('index'))
        
        # Find the HTML file
        html_files = list(folder_path.glob(f'*.{file_type}.html'))
        if not html_files:
            flash(f'No {file_type} HTML file found for {folder_name}', 'error')
            return redirect(url_for('job_detail', folder_name=folder_name))
        
        html_file = html_files[0]
        
        # Try to generate PDF using available libraries
        try:
            # Try WeasyPrint first
            from weasyprint import HTML, CSS
            
            # Read HTML content
            html_content = html_file.read_text(encoding='utf-8')
            
            # Read CSS file
            css_file = Path(__file__).parent.parent / 'jobs' / 'css' / 'styles.css'
            css_content = css_file.read_text(encoding='utf-8') if css_file.exists() else ""
            
            # Generate PDF
            html_doc = HTML(string=html_content, base_url=str(folder_path))
            css_doc = CSS(string=css_content) if css_content else None
            
            pdf_bytes = html_doc.write_pdf(stylesheets=[css_doc] if css_doc else None)
            
            # Create response
            response = make_response(pdf_bytes)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename="{folder_name}.{file_type}.pdf"'
            
            return response
            
        except ImportError:
            # Fallback to pdfkit if WeasyPrint is not available
            try:
                import pdfkit
                
                # Read HTML content
                html_content = html_file.read_text(encoding='utf-8')
                
                # Generate PDF
                pdf_bytes = pdfkit.from_string(html_content, False)
                
                # Create response
                response = make_response(pdf_bytes)
                response.headers['Content-Type'] = 'application/pdf'
                response.headers['Content-Disposition'] = f'attachment; filename="{folder_name}.{file_type}.pdf"'
                
                return response
                
            except ImportError:
                flash('PDF generation not available. Please install WeasyPrint or pdfkit.', 'error')
                return redirect(url_for('job_detail', folder_name=folder_name))
        
    except Exception as e:
        logger.error(f"Error generating PDF for {folder_name}/{file_type}: {e}")
        flash(f'Error generating PDF: {e}', 'error')
        return redirect(url_for('job_detail', folder_name=folder_name))

@app.route('/skip_job/<folder_name>', methods=['POST'])
def skip_job(folder_name):
    """Skip job and move to skipped directory"""
    try:
        # Search for the job in all possible directories
        search_dirs = [
            ('1_queued', 'folder'),
            ('2_generated', 'folder'), 
            ('3_applied', 'folder'),
            ('4_communications', 'folder'),
            ('5_interviews', 'folder'),
            ('8_errors', 'folder'),
            ('9_expired', 'folder')
        ]
        
        source_path = None
        source_type = None
        
        for dir_name, item_type in search_dirs:
            if item_type == 'folder':
                potential_path = JOBS_DIR / dir_name / folder_name
                if potential_path.exists() and potential_path.is_dir():
                    source_path = potential_path
                    source_type = 'folder'
                    break
        
        # Also check for YAML files in directories that store individual files
        if not source_path:
            yaml_dirs = ['3_applied', '4_communications', '5_interviews', '8_errors', '9_expired']
            for dir_name in yaml_dirs:
                potential_path = JOBS_DIR / dir_name / f"{folder_name}.yaml"
                if potential_path.exists():
                    source_path = potential_path
                    source_type = 'yaml'
                    break
        
        if not source_path:
            return jsonify({'success': False, 'message': f'Job not found in any directory: {folder_name}'})
        
        # Create skipped directory if it doesn't exist
        skipped_dir = JOBS_DIR / '9_skipped'
        skipped_dir.mkdir(exist_ok=True)
        
        # Move to skipped directory
        if source_type == 'folder':
            dest_path = skipped_dir / folder_name
            if dest_path.exists():
                import shutil
                shutil.rmtree(dest_path)
            source_path.rename(dest_path)
        else:  # YAML file
            dest_path = skipped_dir / f"{folder_name}.yaml"
            if dest_path.exists():
                dest_path.unlink()
            source_path.rename(dest_path)
        
        logger.info(f"Skipped job: {folder_name} (moved from {source_path.parent.name})")
        return jsonify({'success': True, 'message': f'Job {folder_name} has been skipped'})
        
    except Exception as e:
        logger.error(f"Error skipping job {folder_name}: {e}")
        return jsonify({'success': False, 'message': f'Error skipping job: {e}'})

@app.route('/get_queue_count')
def get_queue_count():
    """Get current count of jobs in queue (automatically cleans duplicates)"""
    try:
        # Automatically clean up duplicates first (silently)
        cleanup_duplicate_jobs()
        
        queued_dir = JOBS_DIR / '1_queued'
        queued_count = 0
        if queued_dir.exists():
            # Count both flat YAML files (legacy) and subfolders (new format)
            flat_files = len([f for f in queued_dir.glob('*.yaml') if f.is_file()])
            subfolders = len([d for d in queued_dir.iterdir() if d.is_dir()])
            queued_count = flat_files + subfolders
        
        return jsonify({'success': True, 'count': queued_count})
        
    except Exception as e:
        logger.error(f"Error getting queue count: {e}")
        return jsonify({'success': False, 'message': f'Error getting queue count: {e}'})

if __name__ == '__main__':
    try:
        ensure_directories()
        logger.info("Starting ResumeAI Web UI on http://127.0.0.1:5001")
        app.run(debug=True, host='0.0.0.0', port=5001)
    except Exception as e:
        logger.error(f"Error starting ResumeAI Web UI: {e}")
        print(f"❌ Error starting web UI: {e}")
        sys.exit(1)