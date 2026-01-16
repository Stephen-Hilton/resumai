# ResumAI User Guide

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd resumai

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (for PDF generation)
playwright install chromium
```

### 2. Configuration

Create a `.env` file in the project root:

```bash
# Required: Gmail credentials for job alerts
GMAIL_USERNAME=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password

# Required: OpenAI API key for LLM content generation
OPENAI_API_KEY=sk-...

# Optional: S3 bucket for document storage
S3_RESUME_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Optional: Server configuration
PORT=5000
FLASK_DEBUG=False
```

#### Getting Gmail App Password

1. Enable 2-Factor Authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an app password for "Mail"
4. Use this password in `GMAIL_APP_PASSWORD`

### 3. Prepare Your Resume

Create a YAML file in the `resumes/` directory (e.g., `resumes/YourName.yaml`):

```yaml
contacts:
  name: Your Name
  email: your.email@example.com
  phone: "+1-555-0123"
  location: "San Francisco, CA"
  linkedin: "linkedin.com/in/yourprofile"
  github: "github.com/yourprofile"

summary: |
  Experienced software engineer with 5+ years...

skills:
  - Python
  - JavaScript
  - React
  - AWS

experience:
  - company: "Previous Company"
    title: "Senior Engineer"
    dates: "2020 - Present"
    description: |
      - Led development of...
      - Improved performance by...

education:
  - school: "University Name"
    degree: "BS Computer Science"
    dates: "2015 - 2019"
```

### 4. Start the Web Server

```bash
python src/ui/app.py
```

Access the dashboard at: **http://localhost:5000**

## 📋 Using the Dashboard

### Main Interface

The dashboard has four main sections:

1. **Header**: Resume selector and action buttons
2. **Phases Sidebar**: Filter jobs by phase
3. **Job Cards Grid**: View and manage jobs
4. **Logs Panel**: Real-time application logs

### Fetching Jobs

#### From Gmail LinkedIn Alerts

1. Click **"📧 Fetch Jobs from Email"**
2. System will:
   - Connect to Gmail via IMAP
   - Find LinkedIn Job Alert emails from last 2 weeks
   - Parse job details (company, title, location, salary)
   - Fetch full job descriptions from LinkedIn
   - Create job folders in `1_Queued` phase

#### From URL

1. Click **"🔗 Add Job by URL"**
2. Enter a LinkedIn job URL
3. System will fetch and parse the job

### Managing Jobs

#### Job Card Actions

Each job card shows different actions based on its phase:

**Queued Phase (1_Queued)**
- View subcontent generation status
- Toggle LLM/Static generation per section (click 🧠/⚙️ icons)
- Click **"🚀 Generate Resume Data"** to create tailored content
- Click **"⏭️ Skip this Job"** to move to Skipped phase

**Data Generated Phase (2_Data_Generated)**
- View document generation status
- Click **"📄 Generate All Resume Docs"** to create HTML/PDF
- View job.yaml, job.log, or error.md

**Docs Generated Phase (3_Docs_Generated+)**
- View all generated documents
- Download resume.pdf and coverletter.pdf
- Move to next phase using dropdown

#### Moving Between Phases

Use the **"Move to..."** dropdown on any job card to manually move jobs:
- 1_Queued → 2_Data_Generated → 3_Docs_Generated → 4_Applied
- 5_FollowUp → 6_Interviewing → 7_Negotiating → 8_Accepted
- Special: Skipped, Expired, Errored

### Batch Processing

Click **"⚡ Process All Jobs in Queue"** to:
1. Generate data for all jobs in `1_Queued`
2. Generate documents for all jobs in `2_Data_Generated`
3. Process serially to avoid rate limits

### Filtering Jobs

Click any phase in the sidebar to filter:
- **All Active**: Shows jobs in phases 1-7
- **All Jobs**: Shows all jobs
- **Specific Phase**: Shows only jobs in that phase

## 🎨 Customizing Content Generation

### LLM vs Static Generation

For each resume section, you can choose:

- **🧠 LLM Generation**: Uses OpenAI to tailor content to the job
- **⚙️ Static Generation**: Copies content directly from your resume

Toggle by clicking the icon on job cards in Queued phase.

### Editing Generated Content

1. Click on any subcontent file name (e.g., `subcontent.summary.yaml`)
2. Edit the YAML file
3. Regenerate documents to see changes

### Custom Prompts

Edit prompts in `src/lib/prompts.py` to customize LLM behavior.

## 📁 File Structure

### Job Folders

Each job creates a folder: `{Company}.{Title}.{Date}.{ID}`

Example: `Google.SeniorEngineer.20260115-120000.abc123`

### Job Files

- `job.yaml`: Job details (company, title, description, etc.)
- `job.log`: Event log for this job
- `job.html`: Saved LinkedIn page HTML
- `subcontent.*.yaml`: Generated content for each section
- `resume.html`: Generated resume HTML
- `coverletter.html`: Generated cover letter HTML
- `resume.pdf`: Final resume PDF
- `coverletter.pdf`: Final cover letter PDF
- `error.md`: Error details (if any failures)

### Phase Directories

```
jobs/
├── 1_Queued/           # New jobs
├── 2_Data_Generated/   # Content generated
├── 3_Docs_Generated/   # Documents created
├── 4_Applied/          # Application submitted
├── 5_FollowUp/         # Following up
├── 6_Interviewing/     # In interview process
├── 7_Negotiating/      # Negotiating offer
├── 8_Accepted/         # Offer accepted
├── Skipped/            # Jobs to skip
├── Expired/            # Expired postings
└── Errored/            # Jobs with errors
```

## 🔧 Advanced Features

### API Endpoints

The system provides REST API endpoints:

```bash
# Get all jobs
GET /api/jobs?phase=1_Queued

# Get job details
GET /api/job/{job_folder_name}

# Generate data
POST /api/generate_data
{"job_folder_name": "..."}

# Generate documents
POST /api/generate_docs
{"job_folder_name": "..."}

# Move phase
POST /api/move_phase
{"job_folder_name": "...", "target_phase": "4_Applied"}

# Toggle generation type
POST /api/toggle_generation
{"job_folder_name": "...", "section": "summary"}

# Batch process
POST /api/batch_process

# Fetch from email
POST /api/fetch_email

# Get logs
GET /api/logs

# Get statistics
GET /api/job_stats
```

### WebSocket Updates

Connect to WebSocket for real-time updates:

```javascript
const socket = io();

socket.on('toast', (data) => {
  console.log(data.message, data.level);
});

socket.on('job_update', (data) => {
  console.log('Job updated:', data.job_folder_name);
});

socket.on('phase_update', (data) => {
  console.log('Phase count:', data.phase, data.count);
});
```

### Log Rotation

Logs are automatically rotated daily:
- Current log: `src/logs/{YYYYMMDD}.applog.txt`
- Old logs compressed: `src/logs/{YYYYMMDD}.applog.txt.gz`
- Logs older than 30 days are deleted

### Folder Name Validation

Run folder validation to ensure consistency:

```bash
POST /api/validate_folders
```

This checks all job folders match their `job.yaml` data and renames if needed.

## 🧪 Testing

### Run All Tests

```bash
# All tests (31 total)
python -m pytest tests/test_properties.py test_e2e_workflow.py test_flask_app.py -v

# Property tests only (16 tests)
python -m pytest tests/test_properties.py -v

# End-to-end test (1 test)
python -m pytest test_e2e_workflow.py -v

# Flask API tests (14 tests)
python -m pytest test_flask_app.py -v

# Complete system test
python -m pytest test_complete_system.py -v
```

### Test Coverage

- ✅ Event discovery and execution
- ✅ Folder management and phase transitions
- ✅ Content generation (LLM and static)
- ✅ Document generation (HTML and PDF)
- ✅ Error handling and retry logic
- ✅ Flask API endpoints
- ✅ WebSocket communication
- ✅ Batch processing
- ✅ Log rotation
- ✅ Folder validation

## 🐛 Troubleshooting

### Gmail Connection Issues

**Problem**: Can't connect to Gmail

**Solutions**:
1. Verify 2FA is enabled on Google account
2. Use App Password, not regular password
3. Check `GMAIL_USERNAME` and `GMAIL_APP_PASSWORD` in `.env`
4. Ensure IMAP is enabled in Gmail settings

### OpenAI API Errors

**Problem**: LLM generation fails

**Solutions**:
1. Verify `OPENAI_API_KEY` is correct
2. Check API quota and rate limits
3. Visit https://status.openai.com/ for service status
4. Use static generation as fallback

### PDF Generation Fails

**Problem**: PDFs not generating

**Solutions**:
1. Ensure Playwright is installed: `playwright install chromium`
2. Check HTML files exist before PDF generation
3. Review error.md for specific issues
4. Try regenerating HTML first

### Jobs Not Moving Between Phases

**Problem**: Jobs stuck in one phase

**Solutions**:
1. Check job.log for errors
2. Review error.md if it exists
3. Manually move using dropdown
4. Regenerate failed content

### S3 Upload Fails

**Problem**: Documents not uploading to S3

**Solutions**:
1. Verify AWS credentials in `.env`
2. Check S3 bucket exists and is accessible
3. Ensure boto3 is installed
4. Note: S3 upload is optional and won't block workflow

## 💡 Tips & Best Practices

### Resume Optimization

1. **Keep resume YAML updated**: Regularly update your skills and experience
2. **Use LLM for tailoring**: Let AI customize content for each job
3. **Review generated content**: Always check LLM output before applying
4. **Maintain multiple resumes**: Create different YAML files for different roles

### Job Management

1. **Process in batches**: Use batch processing for efficiency
2. **Review before applying**: Check documents in Docs_Generated phase
3. **Track progress**: Use phases to organize your job search
4. **Clean up regularly**: Move old jobs to Expired or Skipped

### Performance

1. **Use static generation for speed**: Toggle to static for faster processing
2. **Batch process during off-hours**: Avoid API rate limits
3. **Monitor logs**: Watch for errors and bottlenecks
4. **Archive old jobs**: Move completed jobs out of active phases

### Security

1. **Never commit .env**: Keep credentials secure
2. **Use app passwords**: Don't use main Gmail password
3. **Rotate API keys**: Periodically update OpenAI key
4. **Review S3 permissions**: Ensure bucket is private

## 📊 Monitoring

### Dashboard Metrics

- **Phase counts**: Track jobs in each phase
- **File counts**: Monitor generated files per job
- **Real-time logs**: Watch system activity
- **Error indicators**: Spot issues quickly

### Log Files

View logs in `src/logs/`:
- Current day: `{YYYYMMDD}.applog.txt`
- Compressed: `{YYYYMMDD}.applog.txt.gz`

### Job Statistics

Access via API:
```bash
GET /api/job_stats
```

Returns:
- Total jobs
- Jobs by phase
- Jobs by source

## 🎯 Workflow Examples

### Example 1: Quick Application

1. Fetch jobs from email
2. Review jobs in Queued phase
3. Click "Generate Resume Data" on desired job
4. Click "Generate All Resume Docs"
5. Download PDFs from Docs_Generated phase
6. Move to Applied phase after submitting

### Example 2: Customized Application

1. Add job by URL
2. Toggle specific sections to LLM generation
3. Generate data
4. Edit subcontent files to refine
5. Regenerate documents
6. Review and download
7. Apply and track

### Example 3: Batch Processing

1. Fetch multiple jobs from email
2. Configure LLM/static for all jobs
3. Click "Process All Jobs in Queue"
4. Wait for batch completion
5. Review all generated documents
6. Apply to multiple positions
7. Track in respective phases

## 🆘 Support

### Getting Help

1. Check this user guide
2. Review IMPLEMENTATION_STATUS.md for technical details
3. Check error.md files for specific job issues
4. Review logs in src/logs/
5. Run tests to verify system health

### Common Issues

See Troubleshooting section above for solutions to common problems.

## 🎉 Success!

You're now ready to automate your job application process with ResumAI!

Remember:
- Keep your resume updated
- Review generated content
- Track your applications
- Follow up regularly

Good luck with your job search! 🚀
