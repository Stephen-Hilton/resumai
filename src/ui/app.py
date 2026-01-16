"""
Flask web application for ResumAI job application automation.

This module provides the web interface for managing job applications,
viewing job status, and triggering automation events.

Requirements: 12.1
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
from pathlib import Path
import os
from datetime import datetime
from dotenv import load_dotenv
from src.ui.websocket_manager import init_socketio
from src.lib.yaml_utils import load_yaml

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Enable CORS for API endpoints
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize WebSocket support
socketio = init_socketio(app)

# Configuration
app.config['JOBS_ROOT'] = Path(os.getenv('JOBS_ROOT', 'jobs'))
app.config['RESUMES_ROOT'] = Path(os.getenv('RESUMES_ROOT', 'resumes'))
app.config['LOGS_DIR'] = Path(os.getenv('LOGS_DIR', 'src/logs'))
app.config['DEFAULT_RESUME'] = os.getenv('DEFAULT_RESUME', 'Stephen_Hilton.yaml')


@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "ResumAI"})


@app.route('/api/version')
def version():
    """Get application version."""
    return jsonify({"version": "0.1.0", "name": "ResumAI Dohickey"})


@app.route('/api/resumes')
def get_resumes():
    """Get list of available resumes."""
    resumes_root = app.config['RESUMES_ROOT']
    
    if not resumes_root.exists():
        return jsonify({"resumes": [], "selected": None})
    
    # Find all .yaml files in resumes directory
    resumes = [f.name for f in resumes_root.glob('*.yaml')]
    resumes.sort()
    
    # Get selected resume from config or use default
    selected = app.config['DEFAULT_RESUME']
    
    return jsonify({"resumes": resumes, "selected": selected})


@app.route('/api/jobs')
def get_jobs():
    """Get list of jobs, optionally filtered by phase."""
    from src.lib.logging_utils import append_app_log
    
    try:
        jobs_root = app.config['JOBS_ROOT']
        phase_filter = request.args.get('phase', 'all-active')
        
        append_app_log(app.config['LOGS_DIR'], f"GET_JOBS_START phase={phase_filter}")
        
        if not jobs_root.exists():
            append_app_log(app.config['LOGS_DIR'], f"GET_JOBS jobs_root does not exist: {jobs_root}")
            return jsonify({"jobs": [], "phase_counts": {}})
        
        # Get all phase directories
        phase_dirs = [d for d in jobs_root.iterdir() if d.is_dir()]
        
        # Calculate phase counts
        phase_counts = {}
        all_jobs = []
        
        for phase_dir in phase_dirs:
            phase_name = phase_dir.name
            job_folders = [d for d in phase_dir.iterdir() if d.is_dir()]
            phase_counts[phase_name] = len(job_folders)
            
            # Collect job data
            for job_folder in job_folders:
                job_yaml = job_folder / 'job.yaml'
                if job_yaml.exists():
                    try:
                        job_data = load_yaml(job_yaml)
                        job_data['folder_name'] = job_folder.name
                        job_data['phase'] = phase_name
                        job_data['file_count'] = len(list(job_folder.iterdir()))
                        
                        # Remove description from list view to reduce payload size
                        if 'description' in job_data:
                            del job_data['description']
                        
                        all_jobs.append(job_data)
                    except Exception as e:
                        error_msg = f"ERROR loading job.yaml from {job_folder.name}: {e}"
                        append_app_log(app.config['LOGS_DIR'], error_msg)
                        print(error_msg)
        
        # Calculate special counts
        active_phases = ['1_Queued', '2_Data_Generated', '3_Docs_Generated', '4_Applied', 
                         '5_FollowUp', '6_Interviewing', '7_Negotiating']
        phase_counts['all-active'] = sum(phase_counts.get(p, 0) for p in active_phases)
        phase_counts['all-jobs'] = len(all_jobs)
        
        # Filter jobs by phase
        if phase_filter == 'all-active':
            filtered_jobs = [j for j in all_jobs if j['phase'] in active_phases]
        elif phase_filter == 'all-jobs':
            filtered_jobs = all_jobs
        else:
            filtered_jobs = [j for j in all_jobs if j['phase'] == phase_filter]
        
        # Sort alphabetically by company name
        filtered_jobs.sort(key=lambda x: x.get('company', '').lower())
        
        append_app_log(app.config['LOGS_DIR'], f"GET_JOBS_SUCCESS phase={phase_filter} count={len(filtered_jobs)}")
        
        return jsonify({"jobs": filtered_jobs, "phase_counts": phase_counts})
    except Exception as e:
        error_msg = f"GET_JOBS_ERROR: {str(e)}"
        append_app_log(app.config['LOGS_DIR'], error_msg)
        print(error_msg)
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "jobs": [], "phase_counts": {}}), 500


@app.route('/api/logs')
def get_logs():
    """Get recent application logs."""
    logs_dir = app.config['LOGS_DIR']
    
    if not logs_dir.exists():
        return jsonify({"logs": ""})
    
    # Get today's log file
    today = datetime.now().strftime('%Y%m%d')
    log_file = logs_dir / f"{today}.applog.txt"
    
    if not log_file.exists():
        return jsonify({"logs": ""})
    
    try:
        # Read last 50 lines
        with open(log_file, 'r') as f:
            lines = f.readlines()
            recent_lines = lines[-50:] if len(lines) > 50 else lines
            logs = ''.join(recent_lines)
        
        return jsonify({"logs": logs})
    except Exception as e:
        return jsonify({"logs": f"Error reading logs: {str(e)}"})


@app.route('/api/fetch_email', methods=['POST'])
def fetch_email():
    """Fetch jobs from Gmail LinkedIn alerts."""
    try:
        import asyncio
        from src.events.event_bus import run_event
        from src.lib.types import EventContext
        
        ctx = EventContext(
            jobs_root=app.config['JOBS_ROOT'],
            resumes_root=app.config['RESUMES_ROOT'],
            default_resume=app.config['DEFAULT_RESUME'],
            test_mode=False
        )
        
        # Run get_gmail_linkedin event
        result = asyncio.run(run_event('get_gmail_linkedin', app.config['JOBS_ROOT'], ctx))
        
        return jsonify({
            "ok": result.ok,
            "message": result.message
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Error fetching jobs: {str(e)}"
        }), 500


@app.route('/api/add_url', methods=['POST'])
def add_url():
    """Add a job from a URL."""
    try:
        import asyncio
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({
                "ok": False,
                "message": "URL is required"
            }), 400
        
        from src.events.event_bus import run_event
        from src.lib.types import EventContext
        
        ctx = EventContext(
            jobs_root=app.config['JOBS_ROOT'],
            resumes_root=app.config['RESUMES_ROOT'],
            default_resume=app.config['DEFAULT_RESUME'],
            test_mode=False,
            state={"url": url}
        )
        
        # Run get_url event
        result = asyncio.run(run_event('get_url', app.config['JOBS_ROOT'], ctx))
        
        return jsonify({
            "ok": result.ok,
            "message": result.message
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Error adding job: {str(e)}"
        }), 500


@app.route('/api/manual_entry', methods=['POST'])
def manual_entry():
    """Manually enter a job."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['company', 'title', 'url']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "ok": False,
                    "message": f"Missing required field: {field}"
                }), 400
        
        # TODO: Implement manual job entry
        return jsonify({
            "ok": False,
            "message": "Manual entry not yet implemented"
        }), 501
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Error creating job: {str(e)}"
        }), 500


@app.route('/api/generate_section', methods=['POST'])
def generate_section():
    """Generate a single subcontent section for a job."""
    try:
        import asyncio
        from src.lib.logging_utils import append_app_log, append_job_log
        
        data = request.get_json()
        job_folder_name = data.get('job_folder_name')
        section = data.get('section')
        
        if not job_folder_name or not section:
            return jsonify({
                "ok": False,
                "message": "job_folder_name and section are required"
            }), 400
        
        from src.events.event_bus import run_event
        from src.lib.types import EventContext
        from src.lib.yaml_utils import load_yaml
        
        # Find the job folder
        jobs_root = app.config['JOBS_ROOT']
        job_path = None
        for phase_dir in jobs_root.iterdir():
            if phase_dir.is_dir():
                potential_path = phase_dir / job_folder_name
                if potential_path.exists():
                    job_path = potential_path
                    break
        
        if not job_path:
            error_msg = f"Job folder not found: {job_folder_name}"
            append_app_log(app.config['LOGS_DIR'], f"ERROR generate_section: {error_msg}")
            return jsonify({
                "ok": False,
                "message": error_msg
            }), 404
        
        # Load job.yaml to get the event for this section
        job_yaml = job_path / 'job.yaml'
        if not job_yaml.exists():
            error_msg = f"job.yaml not found in {job_folder_name}"
            append_app_log(app.config['LOGS_DIR'], f"ERROR generate_section: {error_msg}")
            append_job_log(job_path, f"ERROR: {error_msg}")
            return jsonify({
                "ok": False,
                "message": "job.yaml not found"
            }), 404
        
        job_data = load_yaml(job_yaml)
        subcontent_events = job_data.get('subcontent_events', [])
        
        # Convert list of dicts to dict for lookup
        subcontent_events_dict = {}
        for item in subcontent_events:
            if isinstance(item, dict):
                subcontent_events_dict.update(item)
        
        # Get the event for this section
        event_name = subcontent_events_dict.get(section, f'gen_static_subcontent_{section}')
        
        append_app_log(app.config['LOGS_DIR'], f"GENERATE_SECTION job={job_path} section={section} event={event_name}")
        append_job_log(job_path, f"Generating section: {section} using event: {event_name}")
        
        ctx = EventContext(
            jobs_root=jobs_root,
            resumes_root=app.config['RESUMES_ROOT'],
            default_resume=app.config['DEFAULT_RESUME'],
            test_mode=False
        )
        
        # Run the event
        result = asyncio.run(run_event(event_name, job_path, ctx))
        
        if result.ok:
            append_app_log(app.config['LOGS_DIR'], f"SUCCESS generate_section job={job_path} section={section}")
            append_job_log(job_path, f"Successfully generated section: {section}")
        else:
            append_app_log(app.config['LOGS_DIR'], f"FAILED generate_section job={job_path} section={section} error={result.message}")
            append_job_log(job_path, f"Failed to generate section {section}: {result.message}")
        
        return jsonify({
            "ok": result.ok,
            "message": result.message if result.ok else f"Failed to generate {section}: {result.message}"
        })
    except Exception as e:
        error_msg = f"Error generating section: {str(e)}"
        append_app_log(app.config['LOGS_DIR'], f"ERROR generate_section: {error_msg}")
        if 'job_path' in locals():
            append_job_log(job_path, f"ERROR: {error_msg}")
        return jsonify({
            "ok": False,
            "message": error_msg
        }), 500


@app.route('/api/generate_data', methods=['POST'])
def generate_data():
    """Generate resume data for a job."""
    try:
        import asyncio
        data = request.get_json()
        job_folder_name = data.get('job_folder_name')
        
        if not job_folder_name:
            return jsonify({
                "ok": False,
                "message": "job_folder_name is required"
            }), 400
        
        from src.events.event_bus import run_event
        from src.lib.types import EventContext
        
        # Find the job folder
        jobs_root = app.config['JOBS_ROOT']
        job_path = None
        for phase_dir in jobs_root.iterdir():
            if phase_dir.is_dir():
                potential_path = phase_dir / job_folder_name
                if potential_path.exists():
                    job_path = potential_path
                    break
        
        if not job_path:
            return jsonify({
                "ok": False,
                "message": f"Job folder not found: {job_folder_name}"
            }), 404
        
        ctx = EventContext(
            jobs_root=jobs_root,
            resumes_root=app.config['RESUMES_ROOT'],
            default_resume=app.config['DEFAULT_RESUME'],
            test_mode=False
        )
        
        # Run batch_gen_data event
        result = asyncio.run(run_event('batch_gen_data', job_path, ctx))
        
        return jsonify({
            "ok": result.ok,
            "message": result.message
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Error generating data: {str(e)}"
        }), 500


@app.route('/api/generate_docs', methods=['POST'])
def generate_docs():
    """Generate documents for a job."""
    try:
        import asyncio
        data = request.get_json()
        job_folder_name = data.get('job_folder_name')
        
        if not job_folder_name:
            return jsonify({
                "ok": False,
                "message": "job_folder_name is required"
            }), 400
        
        from src.events.event_bus import run_event
        from src.lib.types import EventContext
        
        # Find the job folder
        jobs_root = app.config['JOBS_ROOT']
        job_path = None
        for phase_dir in jobs_root.iterdir():
            if phase_dir.is_dir():
                potential_path = phase_dir / job_folder_name
                if potential_path.exists():
                    job_path = potential_path
                    break
        
        if not job_path:
            return jsonify({
                "ok": False,
                "message": f"Job folder not found: {job_folder_name}"
            }), 404
        
        ctx = EventContext(
            jobs_root=jobs_root,
            resumes_root=app.config['RESUMES_ROOT'],
            default_resume=app.config['DEFAULT_RESUME'],
            test_mode=False
        )
        
        # Run batch_gen_docs event
        result = asyncio.run(run_event('batch_gen_docs', job_path, ctx))
        
        return jsonify({
            "ok": result.ok,
            "message": result.message
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Error generating docs: {str(e)}"
        }), 500


@app.route('/api/move_phase', methods=['POST'])
def move_phase():
    """Move a job to a different phase."""
    try:
        import asyncio
        data = request.get_json()
        job_folder_name = data.get('job_folder_name')
        target_phase = data.get('target_phase')
        
        if not job_folder_name or not target_phase:
            return jsonify({
                "ok": False,
                "message": "job_folder_name and target_phase are required"
            }), 400
        
        from src.events.event_bus import run_event
        from src.lib.types import EventContext
        
        # Find the job folder
        jobs_root = app.config['JOBS_ROOT']
        job_path = None
        for phase_dir in jobs_root.iterdir():
            if phase_dir.is_dir():
                potential_path = phase_dir / job_folder_name
                if potential_path.exists():
                    job_path = potential_path
                    break
        
        if not job_path:
            return jsonify({
                "ok": False,
                "message": f"Job folder not found: {job_folder_name}"
            }), 404
        
        ctx = EventContext(
            jobs_root=jobs_root,
            resumes_root=app.config['RESUMES_ROOT'],
            default_resume=app.config['DEFAULT_RESUME'],
            test_mode=False
        )
        
        # Map phase names to event names
        phase_to_event = {
            '1_Queued': 'move_queue',
            '2_Data_Generated': 'move_data_gen',
            '3_Docs_Generated': 'move_docs_gen',
            '4_Applied': 'move_applied',
            '5_FollowUp': 'move_followup',
            '6_Interviewing': 'move_interviewing',
            '7_Negotiating': 'move_negotiating',
            '8_Accepted': 'move_accepted',
            'Skipped': 'move_skipped',
            'Expired': 'move_expired',
            'Errored': 'move_errored'
        }
        
        event_name = phase_to_event.get(target_phase)
        if not event_name:
            return jsonify({
                "ok": False,
                "message": f"Invalid target phase: {target_phase}"
            }), 400
        
        # Run move event
        result = asyncio.run(run_event(event_name, job_path, ctx))
        
        return jsonify({
            "ok": result.ok,
            "message": result.message
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Error moving job: {str(e)}"
        }), 500


@app.route('/api/job_stats')
def get_job_stats():
    """Get job statistics."""
    try:
        jobs_root = app.config['JOBS_ROOT']
        
        if not jobs_root.exists():
            return jsonify({"stats": {}})
        
        stats = {
            "total_jobs": 0,
            "by_phase": {},
            "by_source": {}
        }
        
        for phase_dir in jobs_root.iterdir():
            if phase_dir.is_dir():
                phase_name = phase_dir.name
                job_folders = [d for d in phase_dir.iterdir() if d.is_dir()]
                stats["by_phase"][phase_name] = len(job_folders)
                stats["total_jobs"] += len(job_folders)
                
                # Count by source
                for job_folder in job_folders:
                    job_yaml = job_folder / 'job.yaml'
                    if job_yaml.exists():
                        try:
                            job_data = load_yaml(job_yaml)
                            source = job_data.get('source', 'unknown')
                            stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
                        except:
                            pass
        
        return jsonify({"stats": stats})
    except Exception as e:
        return jsonify({"stats": {}, "error": str(e)}), 500


@app.route('/api/job/<job_folder_name>')
def get_job_detail(job_folder_name):
    """Get detailed information about a specific job."""
    try:
        from src.lib.logging_utils import append_app_log, append_job_log
        
        append_app_log(app.config['LOGS_DIR'], f"GET_JOB_DETAIL job={job_folder_name}")
        
        jobs_root = app.config['JOBS_ROOT']
        
        # Find the job folder
        job_path = None
        for phase_dir in jobs_root.iterdir():
            if phase_dir.is_dir():
                potential_path = phase_dir / job_folder_name
                if potential_path.exists():
                    job_path = potential_path
                    break
        
        if not job_path:
            error_msg = f"Job folder not found: {job_folder_name}"
            append_app_log(app.config['LOGS_DIR'], f"ERROR get_job_detail: {error_msg}")
            return jsonify({"error": error_msg}), 404
        
        # Load job.yaml
        job_yaml = job_path / 'job.yaml'
        if not job_yaml.exists():
            error_msg = f"job.yaml not found in {job_folder_name}"
            append_app_log(app.config['LOGS_DIR'], f"ERROR get_job_detail: {error_msg}")
            append_job_log(job_path, f"ERROR: {error_msg}")
            return jsonify({"error": error_msg}), 404
        
        job_data = load_yaml(job_yaml)
        job_data['folder_name'] = job_folder_name
        job_data['phase'] = job_path.parent.name
        
        # Get file list with details
        files = {}
        for file_path in job_path.iterdir():
            if file_path.is_file():
                files[file_path.name] = {
                    "exists": True,
                    "size": file_path.stat().st_size,
                    "modified": file_path.stat().st_mtime
                }
        
        # Check for subcontent files
        subcontent_sections = ['contacts', 'summary', 'skills', 'highlights', 
                              'experience', 'education', 'awards', 'coverletter']
        subcontent_status = {}
        for section in subcontent_sections:
            filename = f"subcontent.{section}.yaml"
            subcontent_status[section] = {
                "exists": filename in files,
                "filename": filename
            }
        
        # Check for generated documents
        doc_status = {
            "resume_html": "resume.html" in files,
            "coverletter_html": "coverletter.html" in files,
            "resume_pdf": "resume.pdf" in files,
            "coverletter_pdf": "coverletter.pdf" in files,
            "error_md": "error.md" in files
        }
        
        # Get subcontent_events from job.yaml (it's a list of dicts)
        subcontent_events = job_data.get('subcontent_events', [])
        
        # Convert list of dicts to dict for easier lookup
        subcontent_events_dict = {}
        for item in subcontent_events:
            if isinstance(item, dict):
                subcontent_events_dict.update(item)
        
        append_app_log(app.config['LOGS_DIR'], f"SUCCESS get_job_detail job={job_folder_name}")
        
        return jsonify({
            "job": job_data,
            "files": files,
            "subcontent_status": subcontent_status,
            "subcontent_events": subcontent_events_dict,  # Send as dict for UI
            "doc_status": doc_status
        })
    except Exception as e:
        error_msg = f"Error getting job details: {str(e)}"
        append_app_log(app.config['LOGS_DIR'], f"ERROR get_job_detail job={job_folder_name}: {error_msg}")
        if 'job_path' in locals() and job_path:
            append_job_log(job_path, f"ERROR: {error_msg}")
        return jsonify({"error": error_msg}), 500


@app.route('/api/toggle_generation', methods=['POST'])
def toggle_generation():
    """Toggle generation type (LLM vs static) for a subcontent section."""
    try:
        data = request.get_json()
        job_folder_name = data.get('job_folder_name')
        section = data.get('section')
        
        if not job_folder_name or not section:
            return jsonify({
                "ok": False,
                "message": "job_folder_name and section are required"
            }), 400
        
        jobs_root = app.config['JOBS_ROOT']
        
        # Find the job folder
        job_path = None
        for phase_dir in jobs_root.iterdir():
            if phase_dir.is_dir():
                potential_path = phase_dir / job_folder_name
                if potential_path.exists():
                    job_path = potential_path
                    break
        
        if not job_path:
            return jsonify({
                "ok": False,
                "message": f"Job folder not found: {job_folder_name}"
            }), 404
        
        # Load job.yaml
        job_yaml = job_path / 'job.yaml'
        if not job_yaml.exists():
            return jsonify({
                "ok": False,
                "message": "job.yaml not found"
            }), 404
        
        job_data = load_yaml(job_yaml)
        
        # Get subcontent_events from job.yaml (it's a list of dicts)
        subcontent_events = job_data.get('subcontent_events', [])
        
        # Convert list of dicts to dict for easier manipulation
        subcontent_events_dict = {}
        for item in subcontent_events:
            if isinstance(item, dict):
                subcontent_events_dict.update(item)
        
        # Get current event for this section
        current_event = subcontent_events_dict.get(section, f'gen_static_subcontent_{section}')
        
        # Toggle between LLM and static
        if 'llm' in current_event:
            new_event = f'gen_static_subcontent_{section}'
        else:
            new_event = f'gen_llm_subcontent_{section}'
        
        # Update the dict
        subcontent_events_dict[section] = new_event
        
        # Convert back to list of dicts format
        subcontent_events_list = [{section: event} for section, event in subcontent_events_dict.items()]
        job_data['subcontent_events'] = subcontent_events_list
        
        # Save job.yaml safely with backup and validation
        from src.lib.yaml_safe_write import safe_write_yaml
        try:
            safe_write_yaml(job_yaml, job_data, create_backup=True)
        except Exception as e:
            return jsonify({
                "ok": False,
                "message": f"Failed to save job.yaml: {str(e)}"
            }), 500
        
        return jsonify({
            "ok": True,
            "message": f"Toggled {section} to {new_event}",
            "new_event": new_event
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Error toggling generation: {str(e)}"
        }), 500


@app.route('/api/batch_process', methods=['POST'])
def batch_process():
    """Process all jobs in queue (generate data and docs)."""
    try:
        import asyncio
        from src.events.event_bus import run_event
        from src.lib.types import EventContext
        
        jobs_root = app.config['JOBS_ROOT']
        
        # Find all jobs in Queued and Data_Generated phases
        queued_dir = jobs_root / '1_Queued'
        data_gen_dir = jobs_root / '2_Data_Generated'
        
        queued_jobs = []
        data_gen_jobs = []
        
        if queued_dir.exists():
            queued_jobs = [d for d in queued_dir.iterdir() if d.is_dir()]
        
        if data_gen_dir.exists():
            data_gen_jobs = [d for d in data_gen_dir.iterdir() if d.is_dir()]
        
        total_jobs = len(queued_jobs) + len(data_gen_jobs)
        
        if total_jobs == 0:
            return jsonify({
                "ok": True,
                "message": "No jobs to process"
            })
        
        ctx = EventContext(
            jobs_root=jobs_root,
            resumes_root=app.config['RESUMES_ROOT'],
            default_resume=app.config['DEFAULT_RESUME'],
            test_mode=False
        )
        
        processed = 0
        failed = 0
        
        # Process queued jobs (generate data)
        for job_path in queued_jobs:
            try:
                result = asyncio.run(run_event('batch_gen_data', job_path, ctx))
                if result.ok:
                    processed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"Error processing {job_path}: {e}")
                failed += 1
        
        # Process data generated jobs (generate docs)
        for job_path in data_gen_jobs:
            try:
                result = asyncio.run(run_event('batch_gen_docs', job_path, ctx))
                if result.ok:
                    processed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"Error processing {job_path}: {e}")
                failed += 1
        
        message = f"Batch processing complete: {processed} succeeded, {failed} failed out of {total_jobs} total"
        
        return jsonify({
            "ok": True,
            "message": message,
            "processed": processed,
            "failed": failed,
            "total": total_jobs
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Batch processing error: {str(e)}"
        }), 500


@app.route('/api/rotate_logs', methods=['POST'])
def rotate_logs_endpoint():
    """Manually trigger log rotation."""
    try:
        from src.lib.log_rotation import rotate_logs
        
        logs_dir = app.config['LOGS_DIR']
        rotate_logs(logs_dir)
        
        return jsonify({
            "ok": True,
            "message": "Log rotation completed"
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Log rotation error: {str(e)}"
        }), 500


@app.route('/api/validate_folders', methods=['POST'])
def validate_folders_endpoint():
    """Validate and correct all job folder names."""
    try:
        from src.lib.folder_correction import validate_all_folders
        
        jobs_root = app.config['JOBS_ROOT']
        logs_dir = app.config['LOGS_DIR']
        
        stats = validate_all_folders(jobs_root, logs_dir)
        
        message = f"Validated {stats['checked']} folders, corrected {stats['corrected']}, {stats['errors']} errors"
        
        return jsonify({
            "ok": True,
            "message": message,
            "stats": stats
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Folder validation error: {str(e)}"
        }), 500


@app.route('/api/file/<job_folder_name>/<path:filename>', methods=['GET'])
def get_file(job_folder_name, filename):
    """Get file content for viewing/editing."""
    try:
        from src.lib.logging_utils import append_app_log
        
        # Find the job folder
        jobs_root = app.config['JOBS_ROOT']
        job_path = None
        for phase_dir in jobs_root.iterdir():
            if phase_dir.is_dir():
                potential_path = phase_dir / job_folder_name
                if potential_path.exists():
                    job_path = potential_path
                    break
        
        if not job_path:
            return jsonify({
                "ok": False,
                "message": f"Job folder not found: {job_folder_name}"
            }), 404
        
        file_path = job_path / filename
        if not file_path.exists():
            # Extract section name from filename (e.g., "subcontent.experience.yaml" -> "experience")
            if filename.startswith('subcontent.') and filename.endswith('.yaml'):
                section_name = filename.replace('subcontent.', '').replace('.yaml', '')
                return jsonify({
                    "ok": False,
                    "message": f'The "{section_name}" file does not yet exist; please generate the file before editing.'
                }), 404
            else:
                return jsonify({
                    "ok": False,
                    "message": f"File not found: {filename}"
                }), 404
        
        # Read file content
        content = file_path.read_text()
        
        append_app_log(app.config['LOGS_DIR'], f"FILE_READ job={job_folder_name} file={filename}")
        
        return jsonify({
            "ok": True,
            "content": content,
            "filename": filename,
            "job_folder_name": job_folder_name
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Error reading file: {str(e)}"
        }), 500


@app.route('/api/file/<job_folder_name>/<path:filename>', methods=['POST'])
def save_file(job_folder_name, filename):
    """Save file content after editing."""
    try:
        from src.lib.logging_utils import append_app_log, append_job_log
        
        data = request.get_json()
        content = data.get('content')
        
        if content is None:
            return jsonify({
                "ok": False,
                "message": "Content is required"
            }), 400
        
        # Find the job folder
        jobs_root = app.config['JOBS_ROOT']
        job_path = None
        for phase_dir in jobs_root.iterdir():
            if phase_dir.is_dir():
                potential_path = phase_dir / job_folder_name
                if potential_path.exists():
                    job_path = potential_path
                    break
        
        if not job_path:
            return jsonify({
                "ok": False,
                "message": f"Job folder not found: {job_folder_name}"
            }), 404
        
        file_path = job_path / filename
        
        # Write file content
        file_path.write_text(content)
        
        append_app_log(app.config['LOGS_DIR'], f"FILE_SAVE job={job_folder_name} file={filename}")
        append_job_log(job_path, f"File saved: {filename}")
        
        return jsonify({
            "ok": True,
            "message": f"File saved: {filename}"
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Error saving file: {str(e)}"
        }), 500


@app.route('/api/job/<job_folder_name>', methods=['POST'])
def save_job(job_folder_name):
    """Save job.yaml data."""
    try:
        from src.lib.logging_utils import append_app_log, append_job_log
        from src.lib.yaml_safe_write import safe_write_yaml
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                "ok": False,
                "message": "No data provided"
            }), 400
        
        # Find the job folder
        jobs_root = app.config['JOBS_ROOT']
        job_path = None
        for phase_dir in jobs_root.iterdir():
            if phase_dir.is_dir():
                potential_path = phase_dir / job_folder_name
                if potential_path.exists():
                    job_path = potential_path
                    break
        
        if not job_path:
            return jsonify({
                "ok": False,
                "message": f"Job folder not found: {job_folder_name}"
            }), 404
        
        job_yaml = job_path / 'job.yaml'
        
        # Save using safe write (with backup and validation)
        safe_write_yaml(job_yaml, data, create_backup=True)
        
        append_app_log(app.config['LOGS_DIR'], f"JOB_SAVE job={job_folder_name}")
        append_job_log(job_path, f"Job details updated")
        
        return jsonify({
            "ok": True,
            "message": "Job details saved successfully"
        })
    except Exception as e:
        error_msg = f"Error saving job: {str(e)}"
        append_app_log(app.config['LOGS_DIR'], f"ERROR save_job: {error_msg}")
        if 'job_path' in locals():
            append_job_log(job_path, f"ERROR: {error_msg}")
        return jsonify({
            "ok": False,
            "message": error_msg
        }), 500


if __name__ == '__main__':
    # Run the Flask development server with SocketIO
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting ResumAI web server on http://localhost:{port}")
    print(f"Debug mode: {debug}")
    
    # Schedule log rotation (runs at startup)
    from src.lib.log_rotation import rotate_logs
    try:
        rotate_logs(app.config['LOGS_DIR'])
    except Exception as e:
        print(f"Log rotation error: {e}")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
