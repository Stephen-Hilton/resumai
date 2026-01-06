#!/usr/bin/env python3
"""
Web UI for managing job applications
Provides interface to view, edit, and manage generated job applications
"""

import os
import sys
import yaml
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response
import re

# Add parent directory to path to import logging_setup
sys.path.append(str(Path(__file__).parent.parent))
import logging_setup

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
            if phase == 'generated':
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
    
    if phase == 'generated':
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
                         folders=folders, 
                         queued_count=queued_count,
                         phase_counts=phase_counts,
                         current_phase=phase)

@app.route('/job/<folder_name>')
def job_detail(folder_name):
    """Detail page for a specific job"""
    job_path = GENERATED_DIR / folder_name
    
    if not job_path.exists() or not job_path.is_dir():
        flash(f'Job folder "{folder_name}" not found', 'error')
        return redirect(url_for('index'))
    
    # Find YAML file
    yaml_files = list(job_path.glob('*.yaml'))
    if not yaml_files:
        flash(f'No job YAML file found in "{folder_name}"', 'error')
        return redirect(url_for('index'))
    
    yaml_file = yaml_files[0]
    
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            job_data = yaml.safe_load(f)
    except Exception as e:
        flash(f'Error loading job data: {e}', 'error')
        return redirect(url_for('index'))
    
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
                         folder_name=folder_name,
                         job_data=job_data,
                         yaml_file=yaml_file,
                         files=files)

@app.route('/edit_job/<folder_name>', methods=['GET', 'POST'])
def edit_job(folder_name):
    """Edit job YAML data"""
    job_path = GENERATED_DIR / folder_name
    
    if not job_path.exists():
        flash(f'Job folder "{folder_name}" not found', 'error')
        return redirect(url_for('index'))
    
    yaml_files = list(job_path.glob('*.yaml'))
    if not yaml_files:
        flash(f'No job YAML file found in "{folder_name}"', 'error')
        return redirect(url_for('index'))
    
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
            return redirect(url_for('job_detail', folder_name=folder_name))
            
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
        return redirect(url_for('job_detail', folder_name=folder_name))
    
    return render_template('edit_job.html', 
                         folder_name=folder_name,
                         yaml_content=yaml_content)

@app.route('/view_file/<folder_name>/<filename>')
def view_file(folder_name, filename):
    """View HTML files in browser"""
    file_path = GENERATED_DIR / folder_name / filename
    
    if not file_path.exists():
        flash(f'File "{filename}" not found', 'error')
        return redirect(url_for('job_detail', folder_name=folder_name))
    
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
            return redirect(url_for('job_detail', folder_name=folder_name))
    else:
        flash('Only HTML files can be viewed in browser', 'warning')
        return redirect(url_for('job_detail', folder_name=folder_name))

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
        
        # Move original files back to queued
        files_moved = []
        
        # Move YAML file
        yaml_destination = queued_dir / original_yaml.name
        if yaml_destination.exists():
            yaml_destination.unlink()  # Remove existing file
        original_yaml.rename(yaml_destination)
        files_moved.append(original_yaml.name)
        
        # Move HTML file if it exists
        if original_html:
            html_destination = queued_dir / original_html.name
            if html_destination.exists():
                html_destination.unlink()  # Remove existing file
            original_html.rename(html_destination)
            files_moved.append(original_html.name)
        
        # Remove the entire job directory and all remaining files
        shutil.rmtree(job_path)
        
        logger.info(f"Reset job {folder_name} to queued: moved {files_moved}, removed directory")
        return jsonify({
            'success': True, 
            'message': f'Job reset to queued. Moved {len(files_moved)} files back to queue and cleaned up generated files.'
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
    job_path = GENERATED_DIR / folder_name
    
    if not job_path.exists():
        return jsonify({'success': False, 'message': f'Job folder "{folder_name}" not found'})
    
    try:
        # Get additional prompt from request
        data = request.get_json() or {}
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
        
        # Move YAML file to queued directory
        queued_dir = JOBS_DIR / '1_queued'
        queued_dir.mkdir(parents=True, exist_ok=True)
        
        queued_destination = queued_dir / job_yaml.name
        if queued_destination.exists():
            queued_destination.unlink()  # Remove existing file
        
        # Copy (don't move) the YAML file to queued so we can regenerate
        import shutil as sh
        sh.copy2(job_yaml, queued_destination)
        
        # Import and call the generate function in a separate thread
        import threading
        import sys
        from pathlib import Path
        
        # Add the parent directory to sys.path to import step2_generate
        parent_dir = Path(__file__).parent.parent
        if str(parent_dir) not in sys.path:
            sys.path.append(str(parent_dir))
        
        def run_generation():
            try:
                import step2_generate
                # Call generate with force=True and specific job_id
                step2_generate.generate(force=True, job_id=job_id, additional_prompt=additional_prompt)
            except Exception as e:
                logger.error(f"Error in background generation: {e}")
        
        # Start generation in background thread
        generation_thread = threading.Thread(target=run_generation)
        generation_thread.daemon = True
        generation_thread.start()
        
        logger.info(f"Started regeneration for job ID {job_id} with additional prompt: '{additional_prompt}'")
        return jsonify({
            'success': True, 
            'message': f'AI regeneration started for job ID {job_id}. This may take a minute to complete.'
        })
        
    except Exception as e:
        logger.error(f"Error starting regeneration for {folder_name}: {e}")
        return jsonify({'success': False, 'message': f'Error starting regeneration: {e}'})

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
                
                # Run step2_generate.py script
                script_path = BASE_DIR / 'step2_generate.py'
                result = subprocess.run([sys.executable, str(script_path)], 
                                      capture_output=True, text=True, cwd=str(BASE_DIR))
                
                logger.info(f"Step2 generate completed with return code: {result.returncode}")
                if result.stdout:
                    logger.info(f"Step2 stdout: {result.stdout}")
                if result.stderr:
                    logger.error(f"Step2 stderr: {result.stderr}")
                
                # Update final progress
                if result.returncode == 0:
                    app.config['step2_progress']['status'] = 'completed'
                    app.config['step2_progress']['message'] = 'Job processing completed successfully!'
                    app.config['step2_progress']['completed'] = True
                else:
                    app.config['step2_progress']['status'] = 'error'
                    app.config['step2_progress']['message'] = 'Job processing failed. Check logs for details.'
                    app.config['step2_progress']['error'] = result.stderr or 'Unknown error'
                    
            except Exception as e:
                logger.error(f"Error running step2_generate: {e}")
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

@app.route('/get_step2_progress')
def get_step2_progress():
    """Get current progress of step2_generate process"""
    try:
        import subprocess
        import time
        
        # Check if step2_generate process is actually running
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            step2_running = 'step2_generate.py' in result.stdout
        except:
            step2_running = False
        
        # Get progress from app config, or return default if not set
        progress = app.config.get('step2_progress', {
            'status': 'idle',
            'message': 'No processing in progress',
            'current_job': 0,
            'total_jobs': 0,
            'current_job_name': '',
            'completed': False,
            'error': None
        })
        
        # If we think process is running but it's not actually running, update status
        if progress['status'] == 'running' and not step2_running:
            progress['status'] = 'completed'
            progress['message'] = 'Job processing completed (process finished)'
            progress['completed'] = True
            app.config['step2_progress'] = progress
        
        # If process is actually running, get real-time progress by checking files
        if step2_running:
            # Count jobs in queue vs generated to estimate progress
            queued_dir = JOBS_DIR / '1_queued'
            generated_dir = JOBS_DIR / '2_generated'
            
            queued_count = 0
            if queued_dir.exists():
                queued_count = len([f for f in queued_dir.glob('*.yaml') if f.is_file()])
            
            # Count only jobs completed since this session started
            completed_count = 0
            session_start_time = progress.get('session_start_time', current_time - (2 * 60 * 60))
            
            if generated_dir.exists():
                for item in generated_dir.iterdir():
                    if item.is_dir() and item.stat().st_ctime > session_start_time:
                        completed_count += 1
            
            # Total jobs for this run is just queued + completed since session start
            total_jobs = queued_count + completed_count
            
            # Get recently modified directories in generated (indicates recent processing)
            recent_dirs = []
            if generated_dir.exists():
                for item in generated_dir.iterdir():
                    if item.is_dir():
                        # Check if created since this session started
                        if current_time - item.stat().st_ctime < (2 * 60 * 60):
                            recent_dirs.append(item)
            
            # Update progress with real-time info
            progress['status'] = 'running'
            progress['current_job'] = completed_count
            progress['total_jobs'] = total_jobs
            
            if recent_dirs:
                # Sort by modification time, get most recent
                recent_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                latest_dir = recent_dirs[0]
                
                # Try to extract company name from directory
                dir_parts = latest_dir.name.split('.')
                if len(dir_parts) >= 2:
                    company_name = dir_parts[0].replace('_', ' ')
                    progress['current_job_name'] = company_name
                    progress['message'] = f'Processing job for {company_name}... ({queued_count} remaining in queue)'
                else:
                    progress['message'] = f'Processing jobs... ({queued_count} remaining in queue)'
            else:
                progress['message'] = f'Processing jobs... ({queued_count} remaining in queue)'
            
            # Estimate progress percentage
            if total_jobs > 0:
                progress_percent = int((completed_count / total_jobs) * 100)
                progress['progress_percent'] = progress_percent
            else:
                progress['progress_percent'] = 0
            
            # Update the stored progress
            app.config['step2_progress'] = progress
        
        return jsonify({'success': True, 'progress': progress})
        
    except Exception as e:
        logger.error(f"Error getting step2 progress: {e}")
        return jsonify({'success': False, 'message': f'Error getting progress: {e}'})

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

def cleanup_duplicate_jobs():
    """
    Remove duplicate job files from the queue if they already exist in other job directories.
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
        
        # Check queued files for duplicates
        queued_files = list(queued_dir.glob('*.yaml'))
        files_to_remove = []
        
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
        
        # Remove duplicate files
        removed_count = 0
        for file_to_remove in files_to_remove:
            try:
                file_to_remove.unlink()
                logger.debug(f"Removed duplicate file: {file_to_remove.name}")
                removed_count += 1
            except Exception as e:
                logger.error(f"Error removing file {file_to_remove}: {e}")
        
        if removed_count > 0:
            logger.debug(f"Cleanup completed: removed {removed_count} duplicate files")
        
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
        source_path = JOBS_DIR / '2_generated' / folder_name
        if not source_path.exists():
            return jsonify({'success': False, 'message': f'Job folder not found: {folder_name}'})
        
        # Create skipped directory if it doesn't exist
        skipped_dir = JOBS_DIR / '9_skipped'
        skipped_dir.mkdir(exist_ok=True)
        
        # Move folder to skipped
        dest_path = skipped_dir / folder_name
        if dest_path.exists():
            import shutil
            shutil.rmtree(dest_path)
        
        source_path.rename(dest_path)
        
        logger.info(f"Skipped job: {folder_name}")
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
            queued_count = len([f for f in queued_dir.glob('*.yaml') if f.is_file()])
        
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