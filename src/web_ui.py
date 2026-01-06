#!/usr/bin/env python3
"""
Web UI for managing job applications
Provides interface to view, edit, and manage generated job applications
"""

import os
import yaml
import shutil
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import logging_setup

# Set up logger
logger = logging_setup.get_logger(__name__)

app = Flask(__name__)
app.secret_key = 'resumai_web_ui_secret_key_change_in_production'

# Base paths
BASE_DIR = Path(__file__).parent
JOBS_DIR = BASE_DIR / 'jobs'
GENERATED_DIR = JOBS_DIR / '2_generated'
APPLIED_DIR = JOBS_DIR / '3_applied'

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
                    
                    folders.append({
                        'name': item.name,
                        'path': item,
                        'yaml_file': job_yaml,
                        'job_data': job_data,
                        'files': list(item.glob('*')),
                        'modified': datetime.fromtimestamp(item.stat().st_mtime)
                    })
                except Exception as e:
                    logger.error(f"Error loading job data from {job_yaml}: {e}")
                    folders.append({
                        'name': item.name,
                        'path': item,
                        'yaml_file': job_yaml,
                        'job_data': {'error': f'Failed to load: {e}'},
                        'files': list(item.glob('*')),
                        'modified': datetime.fromtimestamp(item.stat().st_mtime)
                    })
    
    # Sort by modification time (newest first)
    folders.sort(key=lambda x: x['modified'], reverse=True)
    return folders

@app.route('/')
def index():
    """Main page showing all job folders"""
    folders = get_job_folders()
    return render_template('index.html', folders=folders)

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

if __name__ == '__main__':
    ensure_directories()
    logger.info("Starting ResumeAI Web UI")
    app.run(debug=True, host='127.0.0.1', port=5000)