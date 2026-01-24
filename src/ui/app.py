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
import threading
import time
from datetime import datetime, timedelta
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


def _db_enabled() -> bool:
    """Check if database is enabled (hardcoded path: src/db/resumai.db)."""
    from src.db.connection import get_db_path
    return get_db_path().exists()


def _init_db():
    """Initialize database at hardcoded path src/db/resumai.db."""
    from src.db import init_db
    init_db()


def _get_resume_service():
    """Get ResumeService instance."""
    from src.services.resume_service import ResumeService
    return ResumeService()


def _get_job_service():
    """Get JobService instance."""
    from src.services.job_service import JobService
    return JobService()


def _get_subcontent_repo():
    """Get SubcontentRepository instance."""
    from src.repositories.subcontent_repository import SubcontentRepository
    return SubcontentRepository()


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
    # Use database if enabled
    if _db_enabled():
        try:
            resume_service = _get_resume_service()
            resumes_data = resume_service.get_resumes_for_ui()
            resumes = [f"{r['slug']}.yaml" for r in resumes_data]
            resumes.sort()
            selected = app.config['DEFAULT_RESUME']
            return jsonify({"resumes": resumes, "selected": selected})
        except Exception as e:
            # Fall back to filesystem on error
            pass

    # Filesystem fallback
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
        phase_filter = request.args.get('phase', 'all-active')

        append_app_log(app.config['LOGS_DIR'], f"GET_JOBS_START phase={phase_filter}")

        # Use database if enabled
        if _db_enabled():
            try:
                job_service = _get_job_service()
                result = job_service.get_jobs_for_ui(phase_filter)

                # Add special counts
                counts = result['phase_counts']
                active_phases = ['1_Queued', '2_Data_Generated', '3_Docs_Generated', '4_Applied',
                                 '5_FollowUp', '6_Interviewing', '7_Negotiating']

                # Map count keys to phase names
                phase_key_map = {
                    '1_Queued': 'queued',
                    '2_Data_Generated': 'data_generated',
                    '3_Docs_Generated': 'docs_generated',
                    '4_Applied': 'applied',
                    '5_FollowUp': 'followup',
                    '6_Interviewing': 'interviewing',
                    '7_Negotiating': 'negotiating',
                    '8_Accepted': 'accepted',
                    'Skipped': 'skipped',
                    'Expired': 'expired',
                    'Errored': 'errored',
                }

                # Convert counts to phase name format for UI
                phase_counts = {}
                for phase_name, count_key in phase_key_map.items():
                    phase_counts[phase_name] = counts.get(count_key, 0)

                # Calculate special counts
                phase_counts['all-active'] = sum(phase_counts.get(p, 0) for p in active_phases)
                phase_counts['all-jobs'] = sum(counts.values())

                # Sort jobs by company
                jobs = result['jobs']
                jobs.sort(key=lambda x: x.get('company', '').lower())

                append_app_log(app.config['LOGS_DIR'], f"GET_JOBS_SUCCESS phase={phase_filter} count={len(jobs)}")

                return jsonify({"jobs": jobs, "phase_counts": phase_counts})
            except Exception as e:
                append_app_log(app.config['LOGS_DIR'], f"GET_JOBS_DB_ERROR: {e}, falling back to filesystem")

        # Filesystem fallback
        jobs_root = app.config['JOBS_ROOT']

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
        company = job_data.get('company', 'Unknown')
        title = job_data.get('title', 'Unknown')
        subcontent_events = job_data.get('subcontent_events', [])

        # Convert list of dicts to dict for lookup
        subcontent_events_dict = {}
        for item in subcontent_events:
            if isinstance(item, dict):
                subcontent_events_dict.update(item)

        # Get the event for this section
        event_name = subcontent_events_dict.get(section, f'gen_static_subcontent_{section}')

        append_app_log(app.config['LOGS_DIR'], f"Generating section: {section} ({event_name})", company=company, title=title)
        append_job_log(job_path, f"Generating section: {section} using event: {event_name}", company=company, title=title)
        
        ctx = EventContext(
            jobs_root=jobs_root,
            resumes_root=app.config['RESUMES_ROOT'],
            default_resume=app.config['DEFAULT_RESUME'],
            test_mode=False
        )
        
        # Run the event
        result = asyncio.run(run_event(event_name, job_path, ctx))

        if result.ok:
            append_app_log(app.config['LOGS_DIR'], f"Generated section: {section}", company=company, title=title)
            append_job_log(job_path, f"Successfully generated section: {section}", company=company, title=title)
        else:
            append_app_log(app.config['LOGS_DIR'], f"Failed to generate {section}: {result.message}", company=company, title=title)
            append_job_log(job_path, f"Failed to generate section {section}: {result.message}", company=company, title=title)
        
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


@app.route('/api/generate_doc', methods=['POST'])
def generate_doc():
    """Generate a single document (HTML or PDF) for a job."""
    try:
        import asyncio
        from src.lib.logging_utils import append_app_log, append_job_log

        data = request.get_json()
        job_folder_name = data.get('job_folder_name')
        doc_type = data.get('doc_type')

        if not job_folder_name or not doc_type:
            return jsonify({
                "ok": False,
                "message": "job_folder_name and doc_type are required"
            }), 400

        # Map doc_type to event name
        doc_events = {
            'resume_html': 'gen_resume_html',
            'coverletter_html': 'gen_coverletter_html',
            'resume_pdf': 'gen_resume_pdf',
            'coverletter_pdf': 'gen_coverletter_pdf'
        }

        event_name = doc_events.get(doc_type)
        if not event_name:
            return jsonify({
                "ok": False,
                "message": f"Invalid doc_type: {doc_type}"
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
            error_msg = f"Job folder not found: {job_folder_name}"
            append_app_log(app.config['LOGS_DIR'], f"ERROR generate_doc: {error_msg}")
            return jsonify({
                "ok": False,
                "message": error_msg
            }), 404

        # Load job.yaml to get company/title for logging
        job_yaml = job_path / 'job.yaml'
        company = 'Unknown'
        title = 'Unknown'
        if job_yaml.exists():
            job_data = load_yaml(job_yaml)
            company = job_data.get('company', 'Unknown')
            title = job_data.get('title', 'Unknown')

        append_app_log(app.config['LOGS_DIR'], f"Generating document: {doc_type}", company=company, title=title)
        append_job_log(job_path, f"Generating document: {doc_type}", company=company, title=title)

        ctx = EventContext(
            jobs_root=jobs_root,
            resumes_root=app.config['RESUMES_ROOT'],
            default_resume=app.config['DEFAULT_RESUME'],
            test_mode=False
        )

        # Run the event
        result = asyncio.run(run_event(event_name, job_path, ctx))

        if result.ok:
            append_app_log(app.config['LOGS_DIR'], f"Generated document: {doc_type}", company=company, title=title)
            append_job_log(job_path, f"Successfully generated document: {doc_type}", company=company, title=title)
        else:
            append_app_log(app.config['LOGS_DIR'], f"Failed to generate {doc_type}: {result.message}", company=company, title=title)
            append_job_log(job_path, f"Failed to generate document {doc_type}: {result.message}", company=company, title=title)

        return jsonify({
            "ok": result.ok,
            "message": result.message if result.ok else f"Failed to generate {doc_type}: {result.message}"
        })
    except Exception as e:
        error_msg = f"Error generating document: {str(e)}"
        from src.lib.logging_utils import append_app_log, append_job_log
        append_app_log(app.config['LOGS_DIR'], f"ERROR generate_doc: {error_msg}")
        if 'job_path' in locals() and job_path:
            append_job_log(job_path, f"ERROR: {error_msg}")
        return jsonify({
            "ok": False,
            "message": error_msg
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
        # Use database if enabled
        if _db_enabled():
            try:
                job_service = _get_job_service()
                stats = job_service.get_job_stats()
                return jsonify({"stats": {
                    "total_jobs": stats['total'],
                    "by_phase": stats['phase_counts'],
                    "by_source": stats['source_counts']
                }})
            except Exception:
                pass  # Fall through to filesystem

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


@app.route('/api/job/<path:job_folder_name>')
def get_job_detail(job_folder_name):
    """Get detailed information about a specific job."""
    try:
        from src.lib.logging_utils import append_app_log, append_job_log
        from dataclasses import asdict

        append_app_log(app.config['LOGS_DIR'], f"GET_JOB_DETAIL job={job_folder_name}")

        jobs_root = app.config['JOBS_ROOT']

        # Use database if enabled
        if _db_enabled():
            try:
                job_service = _get_job_service()
                job_detail = job_service.get_job_detail(job_folder_name)

                if job_detail:
                    job = job_detail.job
                    job_data = {
                        'id': job.external_id,
                        'company': job.company,
                        'title': job.title,
                        'url': job.url,
                        'location': job.location,
                        'salary': job.salary,
                        'tags': job.tags,
                        'source': job.source,
                        'date': str(job.date_posted) if job.date_posted else None,
                        'description': job.description,
                        'folder_name': job.folder_name,
                        'phase': job.phase,
                    }

                    # Convert subcontent status to expected format
                    subcontent_status = {}
                    status = job_detail.subcontent_status
                    for section in ['contacts', 'summary', 'skills', 'highlights',
                                    'experience', 'education', 'awards', 'coverletter']:
                        subcontent_status[section] = {
                            "exists": getattr(status, section),
                            "filename": f"subcontent.{section}.yaml"
                        }

                    # Query JobFileRepository for all files associated with job
                    # Requirements: 8.1, 8.2, 8.3, 8.4
                    file_service = _get_file_storage_service()
                    job_files = file_service.get_files_for_job(job.id)
                    
                    # Build doc_status from database records
                    doc_purposes = ['resume_html', 'resume_pdf', 'coverletter_html', 'coverletter_pdf']
                    job_files_by_purpose = {f.file_purpose: f for f in job_files}
                    
                    doc_status = {
                        "resume_html": 'resume_html' in job_files_by_purpose,
                        "coverletter_html": 'coverletter_html' in job_files_by_purpose,
                        "resume_pdf": 'resume_pdf' in job_files_by_purpose,
                        "coverletter_pdf": 'coverletter_pdf' in job_files_by_purpose,
                        "error_md": False,  # Check filesystem for this
                    }
                    
                    # Build files array with purpose, path, source, timestamps
                    # Also detect inconsistencies (database record exists but file missing)
                    files = {}
                    file_inconsistencies = []
                    
                    for job_file in job_files:
                        file_path = Path(job_file.file_path)
                        file_exists_on_disk = file_path.exists()
                        
                        file_info = {
                            "exists": file_exists_on_disk,
                            "purpose": job_file.file_purpose,
                            "path": job_file.file_path,
                            "source": job_file.file_source,
                            "created_at": str(job_file.created_at) if job_file.created_at else None,
                            "updated_at": str(job_file.updated_at) if job_file.updated_at else None,
                        }
                        
                        # Add file size if file exists
                        if file_exists_on_disk:
                            file_info["size"] = file_path.stat().st_size
                            file_info["modified"] = file_path.stat().st_mtime
                        else:
                            # Track inconsistency: database record exists but file missing
                            file_inconsistencies.append({
                                "purpose": job_file.file_purpose,
                                "expected_path": job_file.file_path,
                                "error": "File missing from disk"
                            })
                        
                        files[job_file.filename] = file_info
                    
                    # Also check filesystem for legacy files and error.md
                    job_path = None
                    for phase_dir in jobs_root.iterdir():
                        if phase_dir.is_dir():
                            potential_path = phase_dir / job_folder_name
                            if potential_path.exists():
                                job_path = potential_path
                                break
                    
                    if job_path:
                        for file_path in job_path.iterdir():
                            if file_path.is_file() and file_path.name not in files:
                                files[file_path.name] = {
                                    "exists": True,
                                    "size": file_path.stat().st_size,
                                    "modified": file_path.stat().st_mtime,
                                    "source": "legacy_filesystem"
                                }
                        doc_status["error_md"] = "error.md" in files

                    append_app_log(app.config['LOGS_DIR'], f"SUCCESS get_job_detail job={job_folder_name}")

                    response_data = {
                        "job": job_data,
                        "files": files,
                        "subcontent_status": subcontent_status,
                        "subcontent_events": job.subcontent_events,
                        "doc_status": doc_status
                    }
                    
                    # Include inconsistencies if any detected (Requirement 8.4)
                    if file_inconsistencies:
                        response_data["file_inconsistencies"] = file_inconsistencies
                    
                    return jsonify(response_data)
            except Exception as e:
                append_app_log(app.config['LOGS_DIR'], f"GET_JOB_DETAIL_DB_ERROR: {e}, falling back to filesystem")

        # Filesystem fallback
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

        # Use database if enabled
        if _db_enabled():
            try:
                job_service = _get_job_service()
                new_event = job_service.toggle_generation_mode(job_folder_name, section)
                if new_event:
                    return jsonify({
                        "ok": True,
                        "message": f"Toggled {section} to {new_event}",
                        "new_event": new_event
                    })
            except Exception as e:
                # Fall through to filesystem
                pass

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


def _get_file_storage_service():
    """Get FileStorageService instance."""
    from src.services.file_storage_service import FileStorageService
    return FileStorageService()


def _file_exists_in_db(job_id: int, file_purpose: str) -> bool:
    """
    Check if a file record exists in the database.
    
    Uses JobFileRepository.exists() for database-centric file existence checks.
    
    Requirements: 6.4
    
    Args:
        job_id: Database ID of the job.
        file_purpose: Purpose of the file (e.g., 'resume_html', 'resume_pdf').
    
    Returns:
        True if a record exists in the database, False otherwise.
    """
    try:
        file_service = _get_file_storage_service()
        return file_service.file_repo.exists(job_id, file_purpose)
    except Exception:
        return False


@app.route('/api/view/<int:job_id>/<file_purpose>')
def view_file_by_job_id(job_id: int, file_purpose: str):
    """
    Serve a file for viewing by job_id and file_purpose.

    This endpoint queries the Job_Files_Table to find the file location
    and serves the content from the database-stored path.

    Requirements: 6.1, 6.2, 6.3

    Args:
        job_id: Database ID of the job.
        file_purpose: Purpose of the file (e.g., 'resume_html', 'resume_pdf').

    Returns:
        File content with appropriate content type, or error response.
    """
    from flask import Response

    try:
        file_service = _get_file_storage_service()
        file_record = file_service.file_repo.get_by_job_and_purpose(job_id, file_purpose)

        # Return 404 if no record found in database
        if not file_record:
            return jsonify({
                "error": "File not found",
                "job_id": job_id,
                "purpose": file_purpose
            }), 404

        # Get the file path from the database record
        file_path = Path(file_record.file_path)

        # Check if file exists on disk - return 500 if inconsistency detected
        if not file_path.exists():
            return jsonify({
                "error": "File inconsistency",
                "job_id": job_id,
                "purpose": file_purpose,
                "expected_path": str(file_path)
            }), 500

        # Determine content type based on file extension
        extension = file_path.suffix.lower()
        content_types = {
            '.html': 'text/html',
            '.pdf': 'application/pdf',
            '.yaml': 'text/plain',
            '.yml': 'text/plain',
            '.txt': 'text/plain',
            '.log': 'text/plain',
            '.md': 'text/markdown',
        }
        content_type = content_types.get(extension, 'application/octet-stream')

        # Read and serve file content
        if extension == '.pdf':
            content = file_path.read_bytes()
        else:
            content = file_path.read_text()

        return Response(content, mimetype=content_type)

    except Exception as e:
        return jsonify({
            "error": "Database error",
            "details": str(e)
        }), 500


@app.route('/api/view/<job_folder_name>/<path:filename>', methods=['GET'])
def view_file(job_folder_name, filename):
    """Serve a file directly for viewing in browser (legacy filesystem-based endpoint)."""
    try:
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
            return f"Job folder not found: {job_folder_name}", 404

        file_path = job_path / filename
        if not file_path.exists():
            return f"File not found: {filename}", 404

        # Determine content type based on file extension
        extension = file_path.suffix.lower()
        content_types = {
            '.html': 'text/html',
            '.pdf': 'application/pdf',
            '.yaml': 'text/plain',
            '.yml': 'text/plain',
            '.txt': 'text/plain',
            '.log': 'text/plain',
            '.md': 'text/markdown',
        }
        content_type = content_types.get(extension, 'application/octet-stream')

        # For binary files like PDF, read as binary
        if extension == '.pdf':
            content = file_path.read_bytes()
            from flask import Response
            return Response(content, mimetype=content_type)
        else:
            content = file_path.read_text()
            from flask import Response
            return Response(content, mimetype=content_type)

    except Exception as e:
        return f"Error viewing file: {str(e)}", 500


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


# =============================================================================
# RESUME EDITOR ROUTES
# =============================================================================

@app.route('/resume-editor')
def resume_editor():
    """Render the resume editor page."""
    return render_template('resume_editor.html')


@app.route('/api/resume/list')
def list_resumes_full():
    """Get all resumes with full metadata."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        resume_service = _get_resume_service()
        resumes = resume_service.get_resumes_for_ui()
        return jsonify({"ok": True, "resumes": resumes})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/resume/<slug>')
def get_resume(slug):
    """Get a single resume with all nested data."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository
        repo = ResumeRepository()
        resume = repo.get_by_slug(slug)

        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        # Convert to dict for JSON
        resume_dict = repo.to_dict_by_slug(slug)
        resume_dict['id'] = resume.id
        resume_dict['slug'] = resume.slug

        return jsonify({"ok": True, "resume": resume_dict})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/resume', methods=['POST'])
def create_resume():
    """Create a new resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository
        from src.db.models import Resume

        data = request.get_json()

        if not data.get('name') or not data.get('slug'):
            return jsonify({"ok": False, "error": "Name and slug are required"}), 400

        repo = ResumeRepository()

        # Check if slug exists
        if repo.exists(data['slug']):
            return jsonify({"ok": False, "error": "Resume with this slug already exists"}), 400

        resume = Resume(
            slug=data['slug'],
            name=data['name'],
            location=data.get('location'),
            summary=data.get('summary'),
        )

        resume_id = repo.create(resume)

        return jsonify({"ok": True, "id": resume_id, "message": "Resume created"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/resume/<slug>', methods=['PUT'])
def update_resume(slug):
    """Update resume basic info (name, summary, location)."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository

        data = request.get_json()
        repo = ResumeRepository()

        resume = repo.get_by_slug(slug)
        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        # Update fields
        if 'name' in data:
            resume.name = data['name']
        if 'summary' in data:
            resume.summary = data['summary']
        if 'location' in data:
            resume.location = data['location']

        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Resume updated"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/resume/<slug>', methods=['DELETE'])
def delete_resume(slug):
    """Delete a resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository

        repo = ResumeRepository()
        resume = repo.get_by_slug(slug)

        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        repo.delete(resume.id)

        return jsonify({"ok": True, "message": "Resume deleted"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# -----------------------------------------------------------------------------
# Contact CRUD
# -----------------------------------------------------------------------------

@app.route('/api/resume/<slug>/contact', methods=['POST'])
def add_contact(slug):
    """Add a contact to a resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository
        from src.db.models import Contact

        data = request.get_json()
        repo = ResumeRepository()

        resume = repo.get_by_slug(slug)
        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        contact = Contact(
            name=data.get('name', ''),
            label=data.get('label', ''),
            url=data.get('url'),
            icon=data.get('icon'),
            sort_order=len(resume.contacts)
        )
        resume.contacts.append(contact)

        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Contact added"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/resume/<slug>/contact/<int:index>', methods=['DELETE'])
def delete_contact(slug, index):
    """Delete a contact from a resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository

        repo = ResumeRepository()
        resume = repo.get_by_slug(slug)

        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        if index < 0 or index >= len(resume.contacts):
            return jsonify({"ok": False, "error": "Contact index out of range"}), 400

        resume.contacts.pop(index)
        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Contact deleted"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# -----------------------------------------------------------------------------
# Skill CRUD
# -----------------------------------------------------------------------------

@app.route('/api/resume/<slug>/skill', methods=['POST'])
def add_skill(slug):
    """Add a skill to a resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository

        data = request.get_json()
        repo = ResumeRepository()

        resume = repo.get_by_slug(slug)
        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        skill = data.get('skill', '').strip()
        if not skill:
            return jsonify({"ok": False, "error": "Skill text is required"}), 400

        resume.skills.append(skill)
        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Skill added"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/resume/<slug>/skill/<int:index>', methods=['DELETE'])
def delete_skill(slug, index):
    """Delete a skill from a resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository

        repo = ResumeRepository()
        resume = repo.get_by_slug(slug)

        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        if index < 0 or index >= len(resume.skills):
            return jsonify({"ok": False, "error": "Skill index out of range"}), 400

        resume.skills.pop(index)
        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Skill deleted"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# -----------------------------------------------------------------------------
# Education CRUD
# -----------------------------------------------------------------------------

@app.route('/api/resume/<slug>/education', methods=['POST'])
def add_education(slug):
    """Add education entry to a resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository
        from src.db.models import Education

        data = request.get_json()
        repo = ResumeRepository()

        resume = repo.get_by_slug(slug)
        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        education = Education(
            course=data.get('course', ''),
            school=data.get('school', ''),
            dates=data.get('dates'),
            sort_order=len(resume.education)
        )
        resume.education.append(education)

        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Education added"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/resume/<slug>/education/<int:index>', methods=['DELETE'])
def delete_education(slug, index):
    """Delete education entry from a resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository

        repo = ResumeRepository()
        resume = repo.get_by_slug(slug)

        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        if index < 0 or index >= len(resume.education):
            return jsonify({"ok": False, "error": "Education index out of range"}), 400

        resume.education.pop(index)
        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Education deleted"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# -----------------------------------------------------------------------------
# Award CRUD
# -----------------------------------------------------------------------------

@app.route('/api/resume/<slug>/award', methods=['POST'])
def add_award(slug):
    """Add award entry to a resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository
        from src.db.models import Award

        data = request.get_json()
        repo = ResumeRepository()

        resume = repo.get_by_slug(slug)
        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        award = Award(
            award=data.get('award', ''),
            reward=data.get('reward'),
            dates=data.get('dates'),
            sort_order=len(resume.awards_and_keynotes)
        )
        resume.awards_and_keynotes.append(award)

        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Award added"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/resume/<slug>/award/<int:index>', methods=['DELETE'])
def delete_award(slug, index):
    """Delete award entry from a resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository

        repo = ResumeRepository()
        resume = repo.get_by_slug(slug)

        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        if index < 0 or index >= len(resume.awards_and_keynotes):
            return jsonify({"ok": False, "error": "Award index out of range"}), 400

        resume.awards_and_keynotes.pop(index)
        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Award deleted"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# -----------------------------------------------------------------------------
# Company CRUD
# -----------------------------------------------------------------------------

@app.route('/api/resume/<slug>/company', methods=['POST'])
def add_company(slug):
    """Add a company to a resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository
        from src.db.models import Company

        data = request.get_json()
        repo = ResumeRepository()

        resume = repo.get_by_slug(slug)
        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        company = Company(
            company_name=data.get('company_name', ''),
            location=data.get('location'),
            dates=data.get('dates'),
            company_description=data.get('company_description'),
            sort_order=len(resume.experience)
        )
        resume.experience.append(company)

        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Company added"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/resume/<slug>/company/<int:index>', methods=['DELETE'])
def delete_company(slug, index):
    """Delete a company from a resume."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository

        repo = ResumeRepository()
        resume = repo.get_by_slug(slug)

        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        if index < 0 or index >= len(resume.experience):
            return jsonify({"ok": False, "error": "Company index out of range"}), 400

        resume.experience.pop(index)
        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Company deleted"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# -----------------------------------------------------------------------------
# Role CRUD (child of Company)
# -----------------------------------------------------------------------------

@app.route('/api/resume/<slug>/company/<int:company_index>/role', methods=['POST'])
def add_role(slug, company_index):
    """Add a role to a company."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository
        from src.db.models import Role

        data = request.get_json()
        repo = ResumeRepository()

        resume = repo.get_by_slug(slug)
        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        if company_index < 0 or company_index >= len(resume.experience):
            return jsonify({"ok": False, "error": "Company index out of range"}), 400

        company = resume.experience[company_index]

        role = Role(
            role=data.get('role', ''),
            dates=data.get('dates'),
            location=data.get('location'),
            sort_order=len(company.roles)
        )
        company.roles.append(role)

        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Role added"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/resume/<slug>/company/<int:company_index>/role/<int:role_index>', methods=['DELETE'])
def delete_role(slug, company_index, role_index):
    """Delete a role from a company."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository

        repo = ResumeRepository()
        resume = repo.get_by_slug(slug)

        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        if company_index < 0 or company_index >= len(resume.experience):
            return jsonify({"ok": False, "error": "Company index out of range"}), 400

        company = resume.experience[company_index]

        if role_index < 0 or role_index >= len(company.roles):
            return jsonify({"ok": False, "error": "Role index out of range"}), 400

        company.roles.pop(role_index)
        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Role deleted"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# -----------------------------------------------------------------------------
# Bullet CRUD (child of Role)
# -----------------------------------------------------------------------------

@app.route('/api/resume/<slug>/company/<int:company_index>/role/<int:role_index>/bullet', methods=['POST'])
def add_bullet(slug, company_index, role_index):
    """Add a bullet to a role."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository
        from src.db.models import Bullet

        data = request.get_json()
        repo = ResumeRepository()

        resume = repo.get_by_slug(slug)
        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        if company_index < 0 or company_index >= len(resume.experience):
            return jsonify({"ok": False, "error": "Company index out of range"}), 400

        company = resume.experience[company_index]

        if role_index < 0 or role_index >= len(company.roles):
            return jsonify({"ok": False, "error": "Role index out of range"}), 400

        role = company.roles[role_index]

        bullet = Bullet(
            text=data.get('text', ''),
            tags=data.get('tags', []),
            sort_order=len(role.bullets)
        )
        role.bullets.append(bullet)

        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Bullet added"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/resume/<slug>/company/<int:company_index>/role/<int:role_index>/bullet/<int:bullet_index>', methods=['DELETE'])
def delete_bullet(slug, company_index, role_index, bullet_index):
    """Delete a bullet from a role."""
    if not _db_enabled():
        return jsonify({"error": "Database not enabled"}), 500

    try:
        from src.repositories.resume_repository import ResumeRepository

        repo = ResumeRepository()
        resume = repo.get_by_slug(slug)

        if not resume:
            return jsonify({"ok": False, "error": "Resume not found"}), 404

        if company_index < 0 or company_index >= len(resume.experience):
            return jsonify({"ok": False, "error": "Company index out of range"}), 400

        company = resume.experience[company_index]

        if role_index < 0 or role_index >= len(company.roles):
            return jsonify({"ok": False, "error": "Role index out of range"}), 400

        role = company.roles[role_index]

        if bullet_index < 0 or bullet_index >= len(role.bullets):
            return jsonify({"ok": False, "error": "Bullet index out of range"}), 400

        role.bullets.pop(bullet_index)
        repo.update(resume.id, resume)

        return jsonify({"ok": True, "message": "Bullet deleted"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# =============================================================================
# BACKGROUND JOB EXPIRATION
# =============================================================================

EXPIRATION_DAYS = 14
EXPIRATION_CHECK_INTERVAL = 3600  # Check every hour (in seconds)

_expiration_thread = None
_expiration_stop_event = threading.Event()


def check_and_expire_old_jobs():
    """Check for jobs older than EXPIRATION_DAYS and move them to Expired."""
    import asyncio
    from src.lib.logging_utils import append_app_log

    jobs_root = app.config['JOBS_ROOT']
    logs_dir = app.config['LOGS_DIR']

    # Active phases to check (exclude already-terminal states)
    active_phases = ['1_Queued', '2_Data_Generated', '3_Docs_Generated']

    cutoff_date = datetime.now() - timedelta(days=EXPIRATION_DAYS)
    expired_count = 0

    for phase_name in active_phases:
        phase_dir = jobs_root / phase_name
        if not phase_dir.exists():
            continue

        for job_folder in phase_dir.iterdir():
            if not job_folder.is_dir():
                continue

            job_yaml = job_folder / 'job.yaml'
            if not job_yaml.exists():
                continue

            try:
                job_data = load_yaml(job_yaml)
                date_str = job_data.get('date') or job_data.get('created_at')

                if not date_str:
                    continue

                # Parse the date
                if isinstance(date_str, datetime):
                    job_date = date_str
                else:
                    # Try common date formats
                    for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S']:
                        try:
                            job_date = datetime.strptime(str(date_str)[:19], fmt)
                            break
                        except ValueError:
                            continue
                    else:
                        continue  # Skip if date can't be parsed

                # Check if job is older than cutoff
                if job_date < cutoff_date:
                    # Move to Expired
                    from src.events._helpers import move_job_to_phase, append
                    new_path = move_job_to_phase(job_folder, jobs_root, "Expired")
                    append(new_path, f"auto_expire: moved to Expired (>{EXPIRATION_DAYS} days old)")
                    expired_count += 1

                    company = job_data.get('company', 'Unknown')
                    title = job_data.get('title', 'Unknown')
                    append_app_log(logs_dir, f"AUTO_EXPIRE: {company} - {title} ({job_folder.name})")

            except Exception as e:
                # Log but don't crash - continue checking other jobs
                print(f"Error checking job {job_folder.name} for expiration: {e}")
                continue

    if expired_count > 0:
        append_app_log(logs_dir, f"AUTO_EXPIRE: Moved {expired_count} jobs to Expired")

    return expired_count


def expiration_timer_loop():
    """Background thread that periodically checks for expired jobs."""
    while not _expiration_stop_event.is_set():
        try:
            check_and_expire_old_jobs()
        except Exception as e:
            print(f"Expiration check error: {e}")

        # Wait for the interval or until stop is signaled
        _expiration_stop_event.wait(EXPIRATION_CHECK_INTERVAL)


def start_expiration_timer():
    """Start the background expiration timer thread."""
    global _expiration_thread
    if _expiration_thread is not None and _expiration_thread.is_alive():
        return  # Already running

    _expiration_stop_event.clear()
    _expiration_thread = threading.Thread(target=expiration_timer_loop, daemon=True)
    _expiration_thread.start()
    print(f"Expiration timer started (checking every {EXPIRATION_CHECK_INTERVAL}s for jobs >{EXPIRATION_DAYS} days old)")


def stop_expiration_timer():
    """Stop the background expiration timer thread."""
    global _expiration_thread
    _expiration_stop_event.set()
    if _expiration_thread is not None:
        _expiration_thread.join(timeout=5)
        _expiration_thread = None


if __name__ == '__main__':
    # Run the Flask development server with SocketIO
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    print(f"Starting ResumAI web server on http://localhost:{port}")
    print(f"Debug mode: {debug}")

    # Initialize database if configured
    if _db_enabled():
        print("Database mode enabled: src/db/resumai.db")
        try:
            _init_db()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")
    else:
        print("Database mode disabled")

    # Schedule log rotation (runs at startup)
    from src.lib.log_rotation import rotate_logs
    try:
        rotate_logs(app.config['LOGS_DIR'])
    except Exception as e:
        print(f"Log rotation error: {e}")

    # Start the expiration timer
    start_expiration_timer()

    # Run initial expiration check at startup
    try:
        expired = check_and_expire_old_jobs()
        if expired > 0:
            print(f"Initial expiration check: moved {expired} jobs to Expired")
    except Exception as e:
        print(f"Initial expiration check error: {e}")

    socketio.run(app, host='0.0.0.0', port=port, debug=debug, allow_unsafe_werkzeug=True)
