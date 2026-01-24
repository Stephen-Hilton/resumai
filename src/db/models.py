"""
Data models for ResumAI database entities.

These are plain dataclasses used for type hints and data transfer.
They map to the database tables but are not ORM objects.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# =============================================================================
# RESUME MODELS
# =============================================================================

@dataclass
class Contact:
    """Contact entry (email, phone, LinkedIn, etc.)"""
    name: str
    label: str
    url: Optional[str] = None
    icon: Optional[str] = None
    id: Optional[int] = None
    sort_order: int = 0


@dataclass
class BulletTag:
    """Tag on a bullet point."""
    tag: str
    id: Optional[int] = None


@dataclass
class Bullet:
    """Bullet point in a role."""
    text: str
    original_id: Optional[int] = None
    tags: list[str] = field(default_factory=list)
    id: Optional[int] = None
    sort_order: int = 0


@dataclass
class Role:
    """Role within a company."""
    role: str
    original_id: Optional[int] = None
    dates: Optional[str] = None
    location: Optional[str] = None
    bullets: list[Bullet] = field(default_factory=list)
    id: Optional[int] = None
    sort_order: int = 0


@dataclass
class Company:
    """Work history company."""
    company_name: str
    company_urls: list[str] = field(default_factory=list)
    employees: Optional[int] = None
    dates: Optional[str] = None
    location: Optional[str] = None
    company_description: Optional[str] = None
    roles: list[Role] = field(default_factory=list)
    id: Optional[int] = None
    sort_order: int = 0


@dataclass
class Education:
    """Education entry."""
    course: str
    school: str
    dates: Optional[str] = None
    id: Optional[int] = None
    sort_order: int = 0


@dataclass
class Award:
    """Award or keynote entry."""
    award: str
    reward: Optional[str] = None
    dates: Optional[str] = None
    id: Optional[int] = None
    sort_order: int = 0


@dataclass
class Resume:
    """Full resume with all nested data."""
    slug: str
    name: str
    location: Optional[str] = None
    summary: Optional[str] = None
    icon_folder_url: Optional[str] = None
    contacts: list[Contact] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    experience: list[Company] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    awards_and_keynotes: list[Award] = field(default_factory=list)
    passions: list[str] = field(default_factory=list)
    enjoys: list[str] = field(default_factory=list)
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# =============================================================================
# JOB MODELS
# =============================================================================

@dataclass
class SubcontentEvent:
    """Event configuration for a subcontent section."""
    section: str
    event_name: str
    id: Optional[int] = None


@dataclass
class Job:
    """Core job record."""
    folder_name: str
    company: str
    title: str
    external_id: Optional[str] = None
    url: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    source: Optional[str] = None
    date_posted: Optional[datetime] = None
    description: Optional[str] = None
    phase: str = "1_Queued"
    resume_slug: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    subcontent_events: dict[str, str] = field(default_factory=dict)
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class JobSummary:
    """Minimal job info for list views."""
    id: int
    folder_name: str
    company: str
    title: str
    phase: str
    location: Optional[str] = None
    salary: Optional[str] = None
    source: Optional[str] = None
    date_posted: Optional[datetime] = None
    tags: list[str] = field(default_factory=list)


# =============================================================================
# SUBCONTENT MODELS
# =============================================================================

@dataclass
class SubcontentContacts:
    """Contacts subcontent for a job."""
    job_id: int
    contacts: list[Contact] = field(default_factory=list)


@dataclass
class SubcontentSummary:
    """Summary subcontent for a job."""
    job_id: int
    content: str
    id: Optional[int] = None


@dataclass
class SubcontentSkills:
    """Skills subcontent for a job."""
    job_id: int
    skills: list[str] = field(default_factory=list)


@dataclass
class SubcontentHighlights:
    """Highlights subcontent for a job."""
    job_id: int
    highlights: list[str] = field(default_factory=list)


@dataclass
class SubcontentExperience:
    """Experience subcontent for a job."""
    job_id: int
    companies: list[Company] = field(default_factory=list)


@dataclass
class SubcontentEducation:
    """Education subcontent for a job."""
    job_id: int
    education: list[Education] = field(default_factory=list)


@dataclass
class SubcontentAwards:
    """Awards subcontent for a job."""
    job_id: int
    awards: list[Award] = field(default_factory=list)


@dataclass
class SubcontentCoverletter:
    """Cover letter subcontent for a job."""
    job_id: int
    content: str
    id: Optional[int] = None


# =============================================================================
# SUPPORT MODELS
# =============================================================================

@dataclass
class JobFile:
    """File metadata record for a job.
    
    Tracks files stored in the partitioned file system (src/files/YYYYMM/).
    
    Attributes:
        job_id: Foreign key to the jobs table.
        filename: Name of the file on disk.
        file_path: Full path to the file relative to project root.
        file_purpose: Purpose of the file (job_posting_html, resume_html, 
                      resume_pdf, coverletter_html, coverletter_pdf).
        file_source: How the file was obtained (url_fetch, generated).
        id: Primary key (auto-generated).
        created_at: Timestamp when record was created.
        updated_at: Timestamp when record was last updated.
    """
    job_id: int
    filename: str
    file_path: str
    file_purpose: str  # job_posting_html, resume_html, resume_pdf, coverletter_html, coverletter_pdf
    file_source: str   # url_fetch, generated
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Artifact:
    """Generated artifact (HTML, PDF)."""
    job_id: int
    artifact_type: str
    filename: str
    content: Optional[bytes] = None
    content_type: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class LogEntry:
    """Job log entry."""
    job_id: int
    message: str
    level: str = "INFO"
    event_name: Optional[str] = None
    details: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class ErrorEntry:
    """Job error entry."""
    job_id: int
    error_message: str
    event_name: Optional[str] = None
    error_type: Optional[str] = None
    stack_trace: Optional[str] = None
    retry_count: int = 0
    resolved: bool = False
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


# =============================================================================
# UI/API MODELS
# =============================================================================

@dataclass
class PhaseCounts:
    """Job counts by phase."""
    queued: int = 0
    data_generated: int = 0
    docs_generated: int = 0
    applied: int = 0
    followup: int = 0
    interviewing: int = 0
    negotiating: int = 0
    accepted: int = 0
    skipped: int = 0
    expired: int = 0
    errored: int = 0


@dataclass
class JobListResponse:
    """Response for job list API."""
    jobs: list[JobSummary]
    phase_counts: PhaseCounts


@dataclass
class SubcontentStatus:
    """Status of subcontent sections for a job."""
    contacts: bool = False
    summary: bool = False
    skills: bool = False
    highlights: bool = False
    experience: bool = False
    education: bool = False
    awards: bool = False
    coverletter: bool = False


@dataclass
class DocStatus:
    """Status of generated documents for a job."""
    resume_html: bool = False
    resume_pdf: bool = False
    coverletter_html: bool = False
    coverletter_pdf: bool = False


@dataclass
class JobDetail:
    """Full job details with status information."""
    job: Job
    subcontent_status: SubcontentStatus
    doc_status: DocStatus
