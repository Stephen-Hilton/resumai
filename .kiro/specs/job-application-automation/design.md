# Design Document

## Overview

ResumAI Dohickey is a local-first job application automation system that streamlines the process of applying to multiple job postings. The system uses an event-driven architecture to manage jobs through a multi-phase workflow, automatically generates customized resumes and cover letters using LLM technology, and provides a web-based UI for monitoring and managing the application pipeline.

The system operates entirely on the user's local machine, storing all data in a structured file system hierarchy. Jobs progress through defined phases from initial collection through final acceptance, with each phase containing specific files and supporting specific operations. The event-driven architecture enables parallel processing of multiple jobs while maintaining clear separation of concerns and extensibility.

## Architecture

### High-Level Architecture

The system follows a three-tier architecture:

1. **Presentation Layer**: Flask-based web UI with WebSocket support for real-time updates
2. **Business Logic Layer**: Event-driven processing engine with async/await support
3. **Data Layer**: File system-based storage with YAML for structured data

```
┌─────────────────────────────────────────────────────────────┐
│                      Web Browser (UI)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Dashboard   │  │  Job Cards   │  │   App Logs       │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└────────────┬────────────────────────────────────┬───────────┘
             │ HTTP/WebSocket                     │
┌────────────┴────────────────────────────────────┴───────────┐
│                    Flask Web Server                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Routes     │  │  WebSocket   │  │   API Handlers   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└────────────┬────────────────────────────────────────────────┘
             │
┌────────────┴────────────────────────────────────────────────┐
│                      Event Bus                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │Event Discovery│ │Event Routing │  │ Parallel Exec    │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└────────────┬────────────────────────────────────────────────┘
             │
┌────────────┴────────────────────────────────────────────────┐
│                        Events                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │Job Data  │ │Content   │ │Document  │ │Phase         │  │
│  │Collection│ │Generation│ │Generation│ │Management    │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
└────────────┬────────────────────────────────────────────────┘
             │
┌────────────┴────────────────────────────────────────────────┐
│                   File System Storage                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Job Folders │  │  Resumes     │  │   Logs           │  │
│  │  (by phase)  │  │  (.yaml)     │  │   (daily)        │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Event-Driven Architecture

The core of the system is an event bus that discovers, routes, and executes events. Each event is a Python module in `src/events/` with `execute()` and `test()` functions. Events are discovered dynamically at runtime by scanning the events directory.

**Event Execution Flow:**
1. UI or system triggers an event by name
2. Event bus discovers and imports the event module
3. Event bus creates EventContext with job path and configuration
4. Event executes asynchronously, performing its operation
5. Event returns EventResult with success status and updated job path
6. Event bus handles errors, retries, and logging
7. UI receives updates via WebSocket

**Event Types:**
- **Data Collection**: `get_gmail_linkedin`, `get_url`, `create_jobfolder`
- **Content Generation**: `gen_llm_subcontent_*`, `gen_static_subcontent_*`
- **Document Generation**: `gen_resume_html`, `gen_resume_pdf`, `gen_coverletter_html`, `gen_coverletter_pdf`
- **Phase Management**: `move_queue`, `move_data_gen`, `move_docs_gen`, `move_applied`, etc.
- **Batch Operations**: `batch_gen_data`, `batch_gen_docs`
- **Utilities**: `log_message`, `notify_user`, `upload_s3`

## Components and Interfaces

### 1. Event Bus (`src/events/event_bus.py`)

**Purpose**: Discover, route, and execute events dynamically

**Key Functions:**
- `discover_events() -> Dict[str, str]`: Scans `src/events/` and returns mapping of event names to module paths
- `run_event(event_name: str, job_path: Path, ctx: EventContext) -> EventResult`: Executes a single event
- `run_events_parallel(event_names: list[str], job_path: Path, ctx: EventContext) -> list[EventResult]`: Executes multiple events in parallel
- `run_event_sync(event_name: str, job_path: Path, ctx: EventContext) -> EventResult`: Synchronous wrapper for event execution

**Interface:**
```python
async def run_event(event_name: str, job_path: Path, ctx: EventContext) -> EventResult:
    """
    Execute an event by name.
    
    Args:
        event_name: Name of the event module (e.g., "create_jobfolder")
        job_path: Path to the job folder
        ctx: Event context with configuration and state
        
    Returns:
        EventResult with success status, updated job path, message, and artifacts
    """
```

### 2. Event Context (`src/lib/types.py`)

**Purpose**: Provide configuration and state to events

**Structure:**
```python
@dataclass
class EventContext:
    jobs_root: Path              # Root directory for all job folders
    resumes_root: Path           # Directory containing resume.yaml files
    default_resume: str          # Name of the default resume file
    verbose: bool = False        # Enable verbose logging
    test_mode: bool = False      # Run in test mode (non-destructive)
    state: dict[str, Any] = field(default_factory=dict)  # Runtime state
```

### 3. Event Result (`src/lib/types.py`)

**Purpose**: Return execution results from events

**Structure:**
```python
@dataclass
class EventResult:
    ok: bool                     # Success status
    job_path: Path               # Updated job folder path (may change on phase transition)
    message: str = ""            # Human-readable message
    artifacts: list[str] = []    # List of files created/modified
    errors: list[dict] = []      # List of error details
```

### 4. Job Folder Manager (`src/lib/job_folders.py`)

**Purpose**: Manage job folder naming, parsing, and phase paths

**Key Functions:**
- `folder_name(identity: JobIdentity) -> str`: Generate folder name from job identity
- `parse_job_folder_name(name: str) -> Optional[JobIdentity]`: Parse folder name into components
- `phase_path(jobs_root: Path, phase: str) -> Path`: Get path to phase directory
- `slug_part(s: str) -> str`: Sanitize string for use in folder names

**Interface:**
```python
@dataclass
class JobIdentity:
    company: str
    title: str
    posted_at: datetime
    job_id: str

def folder_name(identity: JobIdentity) -> str:
    """Generate folder name: {company}.{title}.{date}.{id}"""
    
def parse_job_folder_name(name: str) -> Optional[JobIdentity]:
    """Parse folder name back into JobIdentity"""
```

### 5. Validation (`src/lib/validation.py`)

**Purpose**: Validate job.yaml and resume.yaml files

**Key Functions:**
- `validate_job_yaml(job_yaml: dict) -> Tuple[bool, list[str]]`: Validate job.yaml against Pydantic schema
- `validate_resume_yaml(resume_yaml: dict) -> Tuple[bool, list[str]]`: Validate resume.yaml structure

**Schemas:**
```python
class JobSource(BaseModel):
    type: str = "manual"         # url|email|manual
    provider: str | None = None  # linkedin|gmail-imap|etc
    url: str | None = None

class JobModel(BaseModel):
    id: str                      # LinkedIn job ID extracted from URL (e.g., "4352500475" from "https://www.linkedin.com/jobs/view/4352500475")
    company: str
    title: str
    date: str                    # Date/time the email was sent (YYYY-MM-DD HH:MM:SS format)
    location: str | None = None
    salary: str | None = None
    tags: list[str] | None = None
    source: str = "manual"       # Source identifier (e.g., "gmail_linkedin", "manual", "url")
    url: str                     # Job posting URL (LinkedIn URLs should not include /comm/ path)
    description: str | None = None
    subcontent_events: list[dict[str, str]] | None = None
```

### 6. LLM Interface (`src/lib/llm.py`)

**Purpose**: Abstract LLM provider interactions

**Key Functions:**
- `generate_content(prompt: str, job_yaml: dict, resume_yaml: dict, section: str) -> str`: Generate customized content
- `configure_provider(provider: str, model: str, api_key: str)`: Configure LLM provider
- `estimate_cost(tokens: int) -> float`: Estimate API cost

**Interface:**
```python
async def generate_content(
    prompt: str,
    job_yaml: dict,
    resume_yaml: dict,
    section: str,
    timeout: int = 300
) -> str:
    """
    Generate customized resume content using LLM.
    
    Args:
        prompt: System prompt for the LLM
        job_yaml: Job posting data
        resume_yaml: Resume data
        section: Section being generated (summary, skills, etc.)
        timeout: Maximum time in seconds (default 5 minutes)
        
    Returns:
        Generated content as string
        
    Raises:
        TimeoutError: If generation exceeds timeout
        LLMError: If API call fails after retries
    """
```

### 7. Document Generator (`src/lib/document_generator.py`)

**Purpose**: Generate HTML and PDF documents from subcontent files

**Key Functions:**
- `generate_resume_html(job_path: Path, subcontent_files: list[Path]) -> Path`: Combine subcontent into resume.html
- `generate_coverletter_html(job_path: Path, coverletter_file: Path) -> Path`: Generate coverletter.html
- `generate_pdf(html_path: Path) -> Path`: Convert HTML to PDF using Playwright
- `generate_css_files(job_path: Path)`: Generate main.css and per-section CSS files

**CSS Architecture:**
```
job_folder/
├── css/
│   ├── main.css              # Universal styles (colors, fonts, sizes)
│   ├── contacts.css          # Section-specific styles
│   ├── summary.css
│   ├── skills.css
│   ├── highlights.css
│   ├── experience.css
│   ├── education.css
│   ├── awards.css
│   └── coverletter.css
├── resume.html               # References all CSS files
└── coverletter.html          # References main.css and coverletter.css
```

### 8. Flask Web Server (`src/ui/app.py`)

**Purpose**: Serve web UI and handle API requests

**Routes:**
- `GET /`: Dashboard page
- `GET /job/<job_folder_name>`: Job detail page
- `POST /api/toggle_generation`: Toggle LLM/static generation for a section
- `POST /api/generate_data`: Trigger batch_gen_data for a job
- `POST /api/generate_docs`: Trigger batch_gen_docs for a job
- `POST /api/move_phase`: Move job to a different phase
- `POST /api/fetch_email`: Trigger get_gmail_linkedin
- `POST /api/add_url`: Trigger get_url with provided URL
- `POST /api/manual_entry`: Create job from manual form data
- `GET /api/logs`: Get recent application logs
- `GET /api/job_stats`: Get job counts by phase
- `WebSocket /ws`: Real-time updates

### 9. WebSocket Manager (`src/ui/websocket.py`)

**Purpose**: Push real-time updates to connected clients

**Messages:**
- `toast`: Display toast notification
- `job_update`: Update job card status
- `phase_update`: Update phase counts
- `log_update`: New log entries available
- `file_status`: Update file status icon

**Interface:**
```python
async def broadcast_toast(message: str, job_folder_name: str):
    """Send toast notification to all connected clients"""
    
async def broadcast_job_update(job_folder_name: str, updates: dict):
    """Send job card updates to all connected clients"""
    
async def broadcast_phase_update(phase_counts: dict):
    """Send updated phase counts to all connected clients"""
```

### 10. Logging Utilities (`src/lib/logging_utils.py`)

**Purpose**: Manage application and job-specific logging

**Key Functions:**
- `append_app_log(logs_dir: Path, message: str)`: Append to daily application log
- `append_job_log(job_path: Path, message: str)`: Append to job-specific log
- `rotate_logs(logs_dir: Path)`: Compress old log files
- `get_recent_logs(logs_dir: Path, count: int = 100) -> list[str]`: Get recent log entries

**Log Format:**
```
{YYYY-MM-DD HH:MM:SS} - {context} - {message}

Examples:
2026-01-14 08:00:01 - APPLICATION START - Resumai2 v1.0.0
2026-01-14 08:17:52 - EVENT - create_jobfolder started for job_id=4123456789
2026-01-14 08:26:54 - LLM - Response received: 342 tokens, $0.0137 cost
2026-01-14 14:37:24 - ERROR - All retry attempts exhausted for gen_llm_subcontent_summary
```

## Data Models

### Job Folder Structure

Each job is stored in a folder with the naming convention: `{company}.{title}.{date}.{id}/`

**Phase 1: Queued**
```
jobs/1_Queued/TechCorp.SeniorEngineer.20260113-143022.4123456789/
├── job.yaml          # Required: Job metadata including full description
├── job.html          # Required for LinkedIn jobs: Raw HTML from job posting page
└── job.log           # Log of all operations on this job
```

**Note**: For jobs collected via `get_gmail_linkedin`, the system fetches the full job posting HTML from the LinkedIn URL and saves it to `job.html`. This allows the job description to be parsed and preserved even if the posting is later removed from LinkedIn. The full description is extracted from the HTML and stored in the `description` field of `job.yaml`.

**Phase 2: Data Generated**
```
jobs/2_Data_Generated/TechCorp.SeniorEngineer.20260113-143022.4123456789/
├── job.yaml
├── job.html
├── job.log
├── subcontent.contacts.yaml
├── subcontent.summary.yaml
├── subcontent.skills.yaml
├── subcontent.highlights.yaml
├── subcontent.experience.yaml
├── subcontent.education.yaml
├── subcontent.awards.yaml
└── subcontent.coverletter.yaml
```

**Phase 3: Docs Generated**
```
jobs/3_Docs_Generated/TechCorp.SeniorEngineer.20260113-143022.4123456789/
├── job.yaml
├── job.html
├── job.log
├── subcontent.*.yaml (all 8 files)
├── css/
│   ├── main.css
│   ├── contacts.css
│   ├── summary.css
│   ├── skills.css
│   ├── highlights.css
│   ├── experience.css
│   ├── education.css
│   └── awards.css
├── resume.html
├── resume.pdf
├── coverletter.html
└── coverletter.pdf
```

**Errored Phase**
```
jobs/Errored/TechCorp.SeniorEngineer.20260113-143022.4123456789/
├── job.yaml
├── job.log
├── error.md          # Error details and recommended actions
└── ... (other files from previous phase)
```

### job.yaml Schema

```yaml
id: "4123456789"
company: "TechCorp"
title: "Senior Engineer"
date: "2026-01-13 14:30:22"
location: "Remote"
salary: "$150K-$200K / year"
tags: ["python", "aws", "kubernetes"]
source: "LinkedIn"
url: "https://www.linkedin.com/jobs/view/4123456789"
subcontent_events:
  - contacts: gen_static_subcontent_contacts
  - summary: gen_llm_subcontent_summary
  - skills: gen_llm_subcontent_skills
  - highlights: gen_llm_subcontent_highlights
  - experience: gen_llm_subcontent_experience
  - education: gen_static_subcontent_education
  - awards: gen_static_subcontent_awards
  - coverletter: gen_llm_subcontent_coverletter
description: |
  Full job description text...
```

### resume.yaml Schema

```yaml
name: "First Last"
location: "San Francisco Bay Area"

summary: |
  Results-driven technical leader with 20 years of experience...

internal:
  folders:
    - icons: https://path/to/icons/

contacts:
  - name: location
    label: "San Francisco Bay Area"
    url: "https://www.google.com/maps/..."
    icon: house-solid.svg
  - name: Email
    label: "first.last@example.com"
    url: "mailto:first.last@example.com"
    icon: at-solid.svg
  - name: Mobile
    label: "555-555-5555"
    url: "tel:+15555555555"
    icon: phone-volume-solid.svg
  - name: Webpage
    label: "example.com"
    url: "https://example.com"
    icon: globe-solid.svg
  - name: GitHub
    label: "username"
    url: "https://github.com/username"
    icon: github-brands.svg
  - name: LinkedIn
    label: "username"
    url: "https://www.linkedin.com/in/username/"
    icon: linkedin-brands-solid.svg

skills:
  - "Application Architecture"
  - "Application Development"
  - "AI Strategy"
  - "Cloud architecture & deployment"
  - "AWS, Azure, GCP experience"

experience:
  - company_name: "TechCorp"
    company_urls: "https://techcorp.com"
    employees: 500
    dates: "2020 - Present"
    location: "Remote"
    company_description: "Leading technology company..."
    
    roles:
      - role: "Principal Engineer"
        id: 1
        dates: "2020 - Present"
        location: "Remote"
        bullets:
          - id: 101
            tags: [aws, kubernetes, python]
            text: "Led migration to microservices architecture"
          - id: 102
            tags: [aws, cost_optimization]
            text: "Reduced infrastructure costs by 40%"

education:
  - course: "Masters in Business Administration"
    school: "University Name"
    dates: "2010"
  - course: "B.S. Computer Science"
    school: "State University"
    dates: "2005"

awards_and_keynotes:
  - award: "Keynote: Scaling Microservices"
    reward: "Trip to Paris"
    dates: "2023"
  - award: "AWS Community Builder"
    reward: "Recognition"
    dates: "2022"

passions:
  - "Intersection of AI and UX"
  - "Building lean, world-class teams"
  - "Creating world-class customer success"

enjoys:
  - "Family"
  - "Travel"
  - "Reading"
  - "Technology"
```

### subcontent.{section}.yaml Schema

Each subcontent file contains the generated content for a specific resume section:

```yaml
# subcontent.contacts.yaml
contacts:
  - name: location
    label: "San Francisco Bay Area"
    url: "https://www.google.com/maps/..."
    icon: house-solid.svg
  - name: Email
    label: "first.last@example.com"
    url: "mailto:first.last@example.com"
    icon: at-solid.svg
  - name: Mobile
    label: "555-555-5555"
    url: "tel:+15555555555"
    icon: phone-volume-solid.svg
  - name: GitHub
    label: "username"
    url: "https://github.com/username"
    icon: github-brands.svg
  - name: LinkedIn
    label: "username"
    url: "https://www.linkedin.com/in/username/"
    icon: linkedin-brands-solid.svg

# subcontent.summary.yaml
summary: |
  Experienced Principal Engineer with 10+ years of expertise in cloud architecture,
  microservices, and team leadership. Proven track record of reducing costs and
  improving system reliability at scale. Passionate about building scalable systems
  and mentoring engineering teams.

# subcontent.skills.yaml
skills:
  - "Python"
  - "AWS (EC2, ECS, Lambda, RDS)"
  - "Kubernetes"
  - "PostgreSQL"
  - "CI/CD (GitHub Actions, Jenkins)"
  - "Microservices Architecture"
  - "System Design"
  - "Team Leadership"

# subcontent.highlights.yaml
highlights:
  - "Led migration to microservices architecture, improving deployment frequency by 10x"
  - "Reduced infrastructure costs by 40% through optimization and right-sizing"
  - "Mentored team of 5 engineers, improving code quality and delivery speed"
  - "Designed and implemented CI/CD pipeline reducing deployment time from hours to minutes"
  - "Architected multi-region disaster recovery solution with 99.99% uptime"

# subcontent.experience.yaml
experience:
  - company_name: "TechCorp"
    company_urls: "https://techcorp.com"
    employees: 500
    dates: "2020 - Present"
    location: "Remote"
    company_description: "Leading technology company specializing in cloud solutions"
    
    roles:
      - role: "Principal Engineer"
        id: 1
        dates: "Jan 2020 - Present"
        location: "Remote"
        bullets:
          - id: 101
            tags: [aws, kubernetes, python]
            text: "Led migration to microservices architecture, improving deployment frequency by 10x and reducing time-to-market for new features"
          - id: 102
            tags: [aws, cost_optimization]
            text: "Reduced infrastructure costs by 40% through optimization, right-sizing, and implementation of auto-scaling policies"
          - id: 103
            tags: [leadership, mentoring]
            text: "Mentored team of 5 engineers, improving code quality metrics by 60% and delivery speed by 35%"
          - id: 104
            tags: [ci_cd, devops]
            text: "Designed and implemented CI/CD pipeline reducing deployment time from 4 hours to 15 minutes"
          - id: 105
            tags: [aws, reliability]
            text: "Architected multi-region disaster recovery solution achieving 99.99% uptime SLA"

  - company_name: "StartupCo"
    company_urls: "https://startupco.com"
    employees: 50
    dates: "2015 - 2020"
    location: "San Francisco, CA"
    company_description: "Fast-growing SaaS startup in the fintech space"
    
    roles:
      - role: "Senior Software Engineer"
        id: 2
        dates: "2015 - 2020"
        location: "San Francisco, CA"
        bullets:
          - id: 201
            tags: [python, api]
            text: "Built RESTful API serving 1M+ requests per day with sub-100ms latency"
          - id: 202
            tags: [postgresql, performance]
            text: "Optimized database queries reducing average response time by 70%"
          - id: 203
            tags: [security]
            text: "Implemented OAuth2 authentication and authorization system"

# subcontent.education.yaml
education:
  - course: "Masters in Business Administration"
    school: "University of Phoenix"
    dates: "2010"
  - course: "B.S. Computer Science"
    school: "State University"
    dates: "2005"
  - course: "AWS Solution Architect Certification"
    school: "AWS"
    dates: "2020"
  - course: "Kubernetes Administrator Certification"
    school: "CNCF"
    dates: "2019"

# subcontent.awards.yaml
awards_and_keynotes:
  - award: "Keynote: Scaling Microservices at DevConf"
    reward: "Speaking engagement"
    dates: "2023"
  - award: "AWS Community Builder"
    reward: "Recognition program"
    dates: "2022"
  - award: "Employee of the Year"
    reward: "Company recognition"
    dates: "2021"
  - award: "Best Technical Blog Post"
    reward: "Industry award"
    dates: "2020"

# subcontent.coverletter.yaml
coverletter:
  greeting: "Dear Hiring Manager,"
  
  opening: |
    I am writing to express my strong interest in the Senior Engineer position at TechCorp.
    With over 10 years of experience in cloud architecture and microservices, I am excited
    about the opportunity to contribute to your team's mission of building scalable,
    reliable systems.
  
  body_paragraphs:
    - |
      In my current role as Principal Engineer, I have led the migration of our monolithic
      application to a microservices architecture, resulting in a 10x improvement in
      deployment frequency and a 40% reduction in infrastructure costs. This experience
      has given me deep expertise in AWS, Kubernetes, and distributed systems design,
      which aligns perfectly with the requirements outlined in your job posting.
    
    - |
      Beyond technical skills, I am passionate about mentoring and growing engineering
      teams. I have successfully mentored 5 engineers, helping them advance their careers
      while improving our team's code quality and delivery speed. I believe that building
      great products requires building great teams, and I am excited about the opportunity
      to contribute to TechCorp's engineering culture.
    
    - |
      I am particularly drawn to TechCorp's focus on innovation and customer success.
      Your recent work on [specific project from job posting] resonates with my own
      experience in building customer-facing systems at scale. I am confident that my
      background in cloud architecture, combined with my passion for solving complex
      technical challenges, would make me a valuable addition to your team.
  
  closing: |
    Thank you for considering my application. I would welcome the opportunity to discuss
    how my experience and skills can contribute to TechCorp's continued success. I look
    forward to speaking with you soon.
  
  signature: |
    Sincerely,
    First Last
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

Before writing the correctness properties, let me analyze each acceptance criterion to determine which are testable as properties, examples, or edge cases.


### Property 1: Folder Name Round Trip
*For any* valid job data (company, title, date, id), generating a folder name and then parsing it back should produce equivalent job identity components.
**Validates: Requirements 1.1, 1.4**

### Property 2: Folder Name Sanitization
*For any* string containing special characters, the sanitized folder name component should contain only alphanumeric characters and underscores, with no consecutive special characters.
**Validates: Requirements 1.2**

### Property 3: Unique ID Generation
*For any* job data without an ID, creating a job folder should generate a unique identifier that doesn't collide with existing job IDs.
**Validates: Requirements 1.3**

### Property 4: Folder Creation Idempotence
*For any* job folder, attempting to create it twice should return the existing path on the second attempt with success=False, without creating duplicates.
**Validates: Requirements 1.6**

### Property 5: Phase Transition File Preservation
*For any* job folder with files, moving it to a different phase should preserve all existing files in the new location.
**Validates: Requirements 2.3, 2.4**

### Property 6: Phase Transition Logging
*For any* job folder, moving it to a new phase should append a log entry to job.log documenting the transition with timestamp and phase names.
**Validates: Requirements 2.5**

### Property 7: Event Discovery Completeness
*For any* Python module in `src/events/` (excluding event_bus.py), the event bus should discover and include it in the events mapping.
**Validates: Requirements 3.1**

### Property 8: Event Execution Error Handling
*For any* event that raises an exception, the event bus should catch it, log to application logs, and return a failed EventResult without crashing.
**Validates: Requirements 3.6**

### Property 9: Job YAML Validation
*For any* dictionary representing job data, validation should succeed if and only if it contains required fields (id, company, title, date, url) with correct types.
**Validates: Requirements 4.7, 14.1, 14.2**

### Property 10: Static Content Round Trip
*For any* resume section that exists in resume.yaml, generating static subcontent and reading it back should produce equivalent content.
**Validates: Requirements 6.1, 6.2**

### Property 11: Subcontent File Completeness
*For any* job folder, moving from phase 2 to phase 3 should only succeed if all 8 subcontent files (contacts, summary, skills, highlights, experience, education, awards, coverletter) exist.
**Validates: Requirements 7.1, 22.1**

### Property 12: CSS File Generation
*For any* job folder in phase 3, the css/ directory should contain main.css and all 7 section-specific CSS files (contacts, summary, skills, highlights, experience, education, awards).
**Validates: Requirements 7.4, 7.5**

### Property 13: HTML to PDF Dependency
*For any* job folder, attempting to generate resume.pdf should fail if resume.html does not exist, and succeed if it does exist.
**Validates: Requirements 22.2**

### Property 14: Log Entry Format
*For any* log message written to job.log or application log, the entry should match the format `{YYYY-MM-DD HH:MM:SS} - {context} - {message}` with valid timestamp.
**Validates: Requirements 8.2, 8.3**

### Property 15: Error File Creation
*For any* job that fails 3 times, moving to the Errored phase should create an error.md file containing error details, context, originating phase, and recommended actions.
**Validates: Requirements 10.3, 8.7**

### Property 16: Retry Logic
*For any* event that fails, the system should retry it up to 3 times before moving the job to Errored phase.
**Validates: Requirements 10.1, 10.2**

### Property 17: Phase Count Accuracy
*For any* set of job folders across all phases, the calculated phase counts should sum to the total job count, with no jobs counted twice.
**Validates: Requirements 26.2, 26.4**

### Property 18: File Dependency Enforcement
*For any* file with dependencies (PDF depends on HTML, HTML depends on subcontent), attempting to generate it without dependencies should fail with a descriptive error.
**Validates: Requirements 22.7**

### Property 19: Batch Processing Completeness
*For any* set of jobs in a phase, batch processing should attempt to process all jobs, with failed jobs moved to Errored without stopping processing of remaining jobs.
**Validates: Requirements 27.4, 27.9**

### Property 20: Resume Selection Persistence
*For any* resume selection change, the selected resume should persist across browser sessions and be used for all subsequent content generation operations.
**Validates: Requirements 25.5, 25.7, 25.8**

### Property 21: WebSocket Message Delivery
*For any* important event (job creation, phase transition, generation completion, error), a WebSocket message should be sent to all connected clients within 1 second.
**Validates: Requirements 21.1, 21.2, 21.3, 21.4**

### Property 22: Log File Rotation
*For any* day boundary (midnight), the system should close the current log file and create a new one with the next day's date.
**Validates: Requirements 8.6, 23.8**

### Property 23: Folder Name Correction
*For any* job folder where the folder name doesn't match job.yaml contents, the system should rename the folder to match job.yaml.
**Validates: Requirements 1.5**

### Property 24: Event Context Immutability
*For any* event execution, modifications to the EventContext.state should not affect other concurrent event executions.
**Validates: Requirements 3.7**

### Property 25: Subcontent Event Configuration
*For any* job with subcontent_events defined in job.yaml, generating subcontent should use the specified event for each section (LLM or static).
**Validates: Requirements 5.3, 6.5**

## Error Handling

### Error Categories

1. **Validation Errors**: Invalid job.yaml, missing required fields, malformed data
2. **External Service Errors**: LLM API failures, Gmail connection issues, S3 upload failures
3. **File System Errors**: Permission denied, disk full, file not found
4. **Timeout Errors**: LLM calls exceeding 5 minutes, network timeouts
5. **Dependency Errors**: Missing subcontent files, missing HTML for PDF generation

### Error Handling Strategy

**Retry Logic:**
- Events that fail are retried up to 3 times with exponential backoff
- Retries wait for other events to complete before retrying
- After 3 failures, job moves to Errored phase

**Error Logging:**
- All errors logged to both application log and job.log
- Error details include: event name, job path, error message, stack trace
- Recommended next steps included in error.md file

**Error Recovery:**
- Users can retry errored jobs from the UI
- Retrying returns job to the phase before the error
- Previous error.md preserved for reference

**Graceful Degradation:**
- S3 upload failures don't move job to Errored phase
- Missing optional files (job.html) don't block processing
- UI continues to function if WebSocket connection drops

### Error Messages

Error messages should be:
- **Specific**: Include exact field names, file paths, and error details
- **Actionable**: Suggest concrete steps to resolve the issue
- **Contextual**: Include relevant job information and phase

**Examples:**
```
ERROR: job.yaml validation failed
- Field 'company': required field missing
- Field 'date': invalid date format, expected YYYY-MM-DD HH:MM:SS
Recommended action: Edit job.yaml and ensure all required fields are present

ERROR: LLM generation timeout after 300s
- Event: gen_llm_subcontent_summary
- Job: TechCorp.SeniorEngineer.20260113-143022.4123456789
Recommended action: Check OpenAI API status, verify API key, retry after service restoration

ERROR: Missing dependencies for resume.pdf generation
- Required: resume.html
- Found: None
Recommended action: Run gen_resume_html first, then retry PDF generation
```

## Testing Strategy

### Dual Testing Approach

The system uses both unit tests and property-based tests to ensure comprehensive coverage:

**Unit Tests:**
- Verify specific examples and edge cases
- Test integration points between components
- Validate error conditions with known inputs
- Test UI components and API endpoints

**Property-Based Tests:**
- Verify universal properties across all inputs
- Use randomized input generation to find edge cases
- Test invariants and round-trip properties
- Validate error handling across many scenarios

### Property-Based Testing Configuration

**Framework**: Use `hypothesis` for Python property-based testing

**Configuration:**
- Minimum 100 iterations per property test
- Each test tagged with: `Feature: job-application-automation, Property {number}: {property_text}`
- Tests run in CI/CD pipeline on every commit

**Example Property Test:**
```python
from hypothesis import given, strategies as st
import pytest

@given(
    company=st.text(min_size=1, max_size=100),
    title=st.text(min_size=1, max_size=100),
    date=st.datetimes(),
    job_id=st.text(min_size=1, max_size=20)
)
@pytest.mark.property
@pytest.mark.tag("Feature: job-application-automation, Property 1: Folder Name Round Trip")
def test_folder_name_round_trip(company, title, date, job_id):
    """
    Property 1: For any valid job data, generating a folder name and parsing it
    back should produce equivalent job identity components.
    """
    identity = JobIdentity(
        company=company,
        title=title,
        posted_at=date,
        job_id=job_id
    )
    
    folder = folder_name(identity)
    parsed = parse_job_folder_name(folder)
    
    assert parsed is not None
    assert parsed.company == slug_part(company)
    assert parsed.title == slug_part(title)
    assert parsed.job_id == job_id
```

### Unit Testing Strategy

**Test Organization:**
- `tests/test_src_events/`: Event module tests
- `tests/test_src_ui/`: Web UI and API tests
- `tests/test_src/`: Library function tests

**Coverage Goals:**
- 80% code coverage minimum
- 100% coverage for critical paths (event bus, validation, error handling)
- All public APIs have unit tests

**Mocking Strategy:**
- Mock external services (LLM, Gmail, S3) in unit tests
- Use test fixtures for file system operations
- Mock WebSocket connections for UI tests

### Integration Testing

**Test Scenarios:**
1. **End-to-End Job Processing**: Create job → Generate data → Generate docs → Move to Applied
2. **Error Recovery**: Simulate failures and verify retry logic
3. **Batch Processing**: Process multiple jobs in parallel
4. **UI Interactions**: Test button clicks, form submissions, WebSocket updates

### Test Data

**Fixtures:**
- Sample job.yaml files with various configurations
- Sample resume.yaml files with different structures
- Mock LLM responses for different sections
- Sample HTML job postings from different sources

**Generators:**
- Random job data generator for property tests
- Random resume data generator
- Random file content generator

## Implementation Notes

### Technology Stack

- **Backend**: Python 3.11+, Flask, asyncio
- **Frontend**: HTML, CSS, JavaScript (vanilla), WebSocket
- **PDF Generation**: Playwright (Chromium)
- **Data Format**: YAML for structured data, HTML for documents
- **Testing**: pytest, hypothesis
- **LLM**: OpenAI API (configurable)
- **Email**: IMAP for Gmail
- **Storage**: Local file system, optional S3

### Performance Considerations

**Parallel Processing:**
- Use asyncio for concurrent event execution
- Batch operations process jobs serially to avoid API rate limits
- WebSocket updates sent asynchronously

**Caching:**
- Cache event discovery results
- Cache resume.yaml parsing
- Cache phase counts (invalidate on job moves)

**File I/O:**
- Use buffered I/O for log writes
- Batch file operations where possible
- Use atomic writes for critical files (job.yaml)

### Security Considerations

**API Keys:**
- Store in .env file, never commit to git
- Use environment variables for all secrets
- Validate API keys before use

**File System:**
- Validate all file paths to prevent directory traversal
- Sanitize folder names to prevent injection
- Use safe YAML loading (no arbitrary code execution)

**Web UI:**
- Validate all user inputs
- Sanitize HTML output to prevent XSS
- Use CSRF tokens for state-changing operations

### Scalability Considerations

**Current Design:**
- Single-user, local-first application
- No database required
- All data in file system

**Future Enhancements:**
- Multi-user support with user directories
- Database for job metadata (faster queries)
- Distributed processing for large job queues
- Cloud deployment option

### Deployment

**Local Deployment:**
1. Clone repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Install Playwright: `python -m playwright install chromium`
5. Copy .env.example to .env and configure
6. Run: `./run_webserver.sh`

**Configuration:**
- `.env` file for environment variables
- `resumes/` directory for resume.yaml files
- `jobs/` directory created automatically

**Dependencies:**
- Python 3.11+
- Playwright (for PDF generation)
- OpenAI API key (for LLM generation)
- Gmail credentials (for email collection)
- AWS credentials (optional, for S3 upload)

## Future Enhancements

1. **Additional Job Sources**: Indeed, Monster, Glassdoor parsers
2. **Resume Templates**: Multiple HTML/CSS templates to choose from
3. **Application Tracking**: Track application status, interviews, offers
4. **Analytics**: Success rates, time-to-hire, cost per application
5. **Mobile App**: iOS/Android app for on-the-go management
6. **AI Improvements**: Fine-tuned models for better content generation
7. **Collaboration**: Share resumes and cover letters with mentors/friends
8. **Integration**: ATS integration for direct application submission
