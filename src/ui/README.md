# ResumeAI Web UI

A Flask-based web interface for managing generated job applications.

## Features

- **View Applications**: Browse all generated job applications in a card-based interface
- **Job Details**: Click into any job to see detailed information from the YAML file
- **Edit Job Data**: Modify job information with a built-in YAML editor with validation
- **Preview Files**: View generated HTML resumes and cover letters in the browser
- **Open Job Links**: Directly open the original job posting URLs
- **Mark as Applied**: Move completed applications to the applied directory with confirmation

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Web UI**:
   ```bash
   python run.py
   ```

3. **Open Browser**:
   Navigate to http://127.0.0.1:5000

## Directory Structure

```
src/ui/
├── app.py              # Main Flask application
├── run.py              # Startup script
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── templates/         # HTML templates
    ├── base.html      # Base template with Bootstrap
    ├── index.html     # Job listing page
    ├── job_detail.html # Job detail page
    └── edit_job.html  # YAML editor page
```

## Usage

### Main Dashboard
- Shows all job folders from `src/jobs/2_generated/`
- Cards display company, position, location, salary, and file count
- Quick actions: View original job link, Mark as applied

### Job Detail Page
- Complete job information from YAML file
- List of all generated files (resume, cover letter, summary)
- Preview HTML files directly in browser
- Edit job data or mark as applied

### YAML Editor
- Full-featured editor with syntax validation
- Real-time syntax checking
- Helpful tips and common field reference
- Validation modal with error details

### Mark as Applied
- Confirmation dialog before moving files
- Moves entire job folder to `src/jobs/3_applied/`
- Handles duplicate names with timestamps

## Technical Details

- **Framework**: Flask 2.3.3
- **Frontend**: Bootstrap 5.1.3 + Font Awesome 6.0
- **YAML Processing**: PyYAML 6.0.1
- **File Management**: Python pathlib + shutil
- **Logging**: Integrated with existing logging_setup module

## File Operations

The web UI performs these file operations:

1. **Read**: Scans `src/jobs/2_generated/` for job folders
2. **Display**: Shows job data from YAML files
3. **Edit**: Modifies YAML files in place
4. **Move**: Transfers entire folders to `src/jobs/3_applied/` when marked as applied
5. **Preview**: Serves HTML files for browser viewing

## Security Notes

- Runs on localhost only (127.0.0.1)
- No external network access required
- File operations limited to job directories
- YAML validation prevents malformed data