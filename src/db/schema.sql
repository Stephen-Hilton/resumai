-- ResumAI Database Schema
-- SQLite database for resume and job management

-- =============================================================================
-- RESUME TABLES
-- =============================================================================

-- Core resume profile
CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,           -- filename without .yaml (e.g., 'Stephen_Hilton')
    name TEXT NOT NULL,
    location TEXT,
    summary TEXT,
    icon_folder_url TEXT,                -- internal.folders[].icons
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resume contact entries
CREATE TABLE IF NOT EXISTS resume_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER NOT NULL,
    name TEXT NOT NULL,                  -- identifier (e.g., 'email', 'phone')
    label TEXT NOT NULL,                 -- display text
    url TEXT,                            -- clickable link
    icon TEXT,                           -- SVG filename
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
);

-- Resume skills list
CREATE TABLE IF NOT EXISTS resume_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER NOT NULL,
    skill TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
);

-- Work history companies
CREATE TABLE IF NOT EXISTS resume_companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER NOT NULL,
    company_name TEXT NOT NULL,
    employees INTEGER,
    dates TEXT,
    location TEXT,
    company_description TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
);

-- Company URLs (one-to-many)
CREATE TABLE IF NOT EXISTS resume_company_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (company_id) REFERENCES resume_companies(id) ON DELETE CASCADE
);

-- Roles within companies
CREATE TABLE IF NOT EXISTS resume_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    original_id INTEGER,                 -- id from YAML for reference
    role TEXT NOT NULL,
    dates TEXT,
    location TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (company_id) REFERENCES resume_companies(id) ON DELETE CASCADE
);

-- Bullet points with original IDs
CREATE TABLE IF NOT EXISTS resume_bullets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    original_id INTEGER,                 -- id from YAML for reference
    text TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (role_id) REFERENCES resume_roles(id) ON DELETE CASCADE
);

-- Tags on bullets
CREATE TABLE IF NOT EXISTS resume_bullet_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bullet_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (bullet_id) REFERENCES resume_bullets(id) ON DELETE CASCADE
);

-- Education entries
CREATE TABLE IF NOT EXISTS resume_education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER NOT NULL,
    course TEXT NOT NULL,
    school TEXT NOT NULL,
    dates TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
);

-- Awards and keynotes
CREATE TABLE IF NOT EXISTS resume_awards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER NOT NULL,
    award TEXT NOT NULL,
    reward TEXT,
    dates TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
);

-- Passions list
CREATE TABLE IF NOT EXISTS resume_passions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER NOT NULL,
    passion TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
);

-- Enjoys list
CREATE TABLE IF NOT EXISTS resume_enjoys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER NOT NULL,
    enjoy TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
);

-- =============================================================================
-- JOB TABLES
-- =============================================================================

-- Core job record
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    external_id TEXT,                    -- LinkedIn job ID or external source ID
    folder_name TEXT UNIQUE NOT NULL,    -- company.title.datetime.id format
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT,
    location TEXT,
    salary TEXT,
    source TEXT,                         -- gmail_linkedin, manual, url
    date_posted TIMESTAMP,
    description TEXT,
    phase TEXT NOT NULL DEFAULT '1_Queued',
    resume_slug TEXT,                    -- which resume to use
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job tags
CREATE TABLE IF NOT EXISTS job_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Job files (tracks all files associated with jobs)
CREATE TABLE IF NOT EXISTS job_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_purpose TEXT NOT NULL,
    file_source TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(job_id, file_purpose),
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Event configuration per job/section
CREATE TABLE IF NOT EXISTS job_subcontent_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    section TEXT NOT NULL,               -- contacts, summary, skills, etc.
    event_name TEXT NOT NULL,            -- gen_static_*, gen_llm_*
    UNIQUE(job_id, section),
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- =============================================================================
-- SUBCONTENT TABLES (generated per job)
-- =============================================================================

-- Contacts subcontent
CREATE TABLE IF NOT EXISTS job_subcontent_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    label TEXT NOT NULL,
    url TEXT,
    icon TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Summary subcontent
CREATE TABLE IF NOT EXISTS job_subcontent_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL UNIQUE,
    content TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Skills subcontent
CREATE TABLE IF NOT EXISTS job_subcontent_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    skill TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Highlights subcontent
CREATE TABLE IF NOT EXISTS job_subcontent_highlights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    highlight TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Experience subcontent - companies
CREATE TABLE IF NOT EXISTS job_subcontent_companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    company_name TEXT NOT NULL,
    employees INTEGER,
    dates TEXT,
    location TEXT,
    company_description TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Experience subcontent - company URLs
CREATE TABLE IF NOT EXISTS job_subcontent_company_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subcontent_company_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (subcontent_company_id) REFERENCES job_subcontent_companies(id) ON DELETE CASCADE
);

-- Experience subcontent - roles
CREATE TABLE IF NOT EXISTS job_subcontent_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subcontent_company_id INTEGER NOT NULL,
    original_id INTEGER,
    role TEXT NOT NULL,
    dates TEXT,
    location TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (subcontent_company_id) REFERENCES job_subcontent_companies(id) ON DELETE CASCADE
);

-- Experience subcontent - bullets
CREATE TABLE IF NOT EXISTS job_subcontent_bullets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subcontent_role_id INTEGER NOT NULL,
    original_id INTEGER,
    text TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (subcontent_role_id) REFERENCES job_subcontent_roles(id) ON DELETE CASCADE
);

-- Experience subcontent - bullet tags
CREATE TABLE IF NOT EXISTS job_subcontent_bullet_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subcontent_bullet_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (subcontent_bullet_id) REFERENCES job_subcontent_bullets(id) ON DELETE CASCADE
);

-- Education subcontent
CREATE TABLE IF NOT EXISTS job_subcontent_education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    course TEXT NOT NULL,
    school TEXT NOT NULL,
    dates TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Awards subcontent
CREATE TABLE IF NOT EXISTS job_subcontent_awards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    award TEXT NOT NULL,
    reward TEXT,
    dates TEXT,
    sort_order INTEGER DEFAULT 0,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Cover letter subcontent
CREATE TABLE IF NOT EXISTS job_subcontent_coverletter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL UNIQUE,
    content TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- =============================================================================
-- SUPPORT TABLES
-- =============================================================================

-- Generated artifacts (HTML, PDF files)
CREATE TABLE IF NOT EXISTS job_artifacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    artifact_type TEXT NOT NULL,         -- resume_html, resume_pdf, coverletter_html, coverletter_pdf
    filename TEXT NOT NULL,
    content BLOB,                        -- For HTML, store as text; for PDF, store as blob
    content_type TEXT,                   -- text/html, application/pdf
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(job_id, artifact_type),
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Event/job log entries
CREATE TABLE IF NOT EXISTS job_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    level TEXT NOT NULL DEFAULT 'INFO',  -- INFO, WARNING, ERROR, DEBUG
    event_name TEXT,
    message TEXT NOT NULL,
    details TEXT,                        -- JSON for additional data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- Error tracking
CREATE TABLE IF NOT EXISTS job_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    event_name TEXT,
    error_type TEXT,
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    retry_count INTEGER DEFAULT 0,
    resolved BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

-- =============================================================================
-- INDEXES
-- =============================================================================

-- Resume indexes
CREATE INDEX IF NOT EXISTS idx_resume_contacts_resume_id ON resume_contacts(resume_id);
CREATE INDEX IF NOT EXISTS idx_resume_skills_resume_id ON resume_skills(resume_id);
CREATE INDEX IF NOT EXISTS idx_resume_companies_resume_id ON resume_companies(resume_id);
CREATE INDEX IF NOT EXISTS idx_resume_company_urls_company_id ON resume_company_urls(company_id);
CREATE INDEX IF NOT EXISTS idx_resume_roles_company_id ON resume_roles(company_id);
CREATE INDEX IF NOT EXISTS idx_resume_bullets_role_id ON resume_bullets(role_id);
CREATE INDEX IF NOT EXISTS idx_resume_bullet_tags_bullet_id ON resume_bullet_tags(bullet_id);
CREATE INDEX IF NOT EXISTS idx_resume_education_resume_id ON resume_education(resume_id);
CREATE INDEX IF NOT EXISTS idx_resume_awards_resume_id ON resume_awards(resume_id);
CREATE INDEX IF NOT EXISTS idx_resume_passions_resume_id ON resume_passions(resume_id);
CREATE INDEX IF NOT EXISTS idx_resume_enjoys_resume_id ON resume_enjoys(resume_id);

-- Job indexes
CREATE INDEX IF NOT EXISTS idx_jobs_phase ON jobs(phase);
CREATE INDEX IF NOT EXISTS idx_jobs_external_id ON jobs(external_id);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at);
CREATE INDEX IF NOT EXISTS idx_job_tags_job_id ON job_tags(job_id);
CREATE INDEX IF NOT EXISTS idx_job_subcontent_events_job_id ON job_subcontent_events(job_id);
CREATE INDEX IF NOT EXISTS idx_job_files_job_id ON job_files(job_id);
CREATE INDEX IF NOT EXISTS idx_job_files_purpose ON job_files(file_purpose);

-- Subcontent indexes
CREATE INDEX IF NOT EXISTS idx_job_subcontent_contacts_job_id ON job_subcontent_contacts(job_id);
CREATE INDEX IF NOT EXISTS idx_job_subcontent_skills_job_id ON job_subcontent_skills(job_id);
CREATE INDEX IF NOT EXISTS idx_job_subcontent_highlights_job_id ON job_subcontent_highlights(job_id);
CREATE INDEX IF NOT EXISTS idx_job_subcontent_companies_job_id ON job_subcontent_companies(job_id);
CREATE INDEX IF NOT EXISTS idx_job_subcontent_company_urls_company_id ON job_subcontent_company_urls(subcontent_company_id);
CREATE INDEX IF NOT EXISTS idx_job_subcontent_roles_company_id ON job_subcontent_roles(subcontent_company_id);
CREATE INDEX IF NOT EXISTS idx_job_subcontent_bullets_role_id ON job_subcontent_bullets(subcontent_role_id);
CREATE INDEX IF NOT EXISTS idx_job_subcontent_bullet_tags_bullet_id ON job_subcontent_bullet_tags(subcontent_bullet_id);
CREATE INDEX IF NOT EXISTS idx_job_subcontent_education_job_id ON job_subcontent_education(job_id);
CREATE INDEX IF NOT EXISTS idx_job_subcontent_awards_job_id ON job_subcontent_awards(job_id);

-- Support table indexes
CREATE INDEX IF NOT EXISTS idx_job_artifacts_job_id ON job_artifacts(job_id);
CREATE INDEX IF NOT EXISTS idx_job_logs_job_id ON job_logs(job_id);
CREATE INDEX IF NOT EXISTS idx_job_logs_created_at ON job_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_job_errors_job_id ON job_errors(job_id);
CREATE INDEX IF NOT EXISTS idx_job_errors_resolved ON job_errors(resolved);
