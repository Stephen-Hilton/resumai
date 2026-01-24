"""
Database helper functions for event handlers.

These functions provide optional database integration for event handlers.
When DATABASE_PATH is set, data will be synced to the database in addition
to the filesystem.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.lib.yaml_utils import load_yaml, dump_yaml


def _db_enabled() -> bool:
    """Check if database is enabled (hardcoded path: src/db/resumai.db)."""
    from src.db.connection import get_db_path
    return get_db_path().exists()


def _get_job_repo():
    """Get JobRepository instance."""
    from src.repositories.job_repository import JobRepository
    return JobRepository()


def _get_resume_repo():
    """Get ResumeRepository instance."""
    from src.repositories.resume_repository import ResumeRepository
    return ResumeRepository()


def _get_subcontent_repo():
    """Get SubcontentRepository instance."""
    from src.repositories.subcontent_repository import SubcontentRepository
    return SubcontentRepository()


def get_job_id_from_path(job_path: Path) -> Optional[int]:
    """
    Get the database job ID for a job path.

    Args:
        job_path: Path to the job folder.

    Returns:
        Job ID or None if not found/database not enabled.
    """
    if not _db_enabled():
        return None

    folder_name = job_path.name
    job_repo = _get_job_repo()
    job = job_repo.get_by_folder_name(folder_name)
    return job.id if job else None


def load_resume_data(resumes_root: Path, resume_filename: str) -> dict:
    """
    Load resume data from database or filesystem.

    Args:
        resumes_root: Path to resumes directory.
        resume_filename: Resume filename (e.g., 'Stephen_Hilton.yaml').

    Returns:
        Resume data dictionary.
    """
    if _db_enabled():
        try:
            resume_repo = _get_resume_repo()
            slug = resume_filename.replace('.yaml', '')
            data = resume_repo.to_dict_by_slug(slug)
            if data:
                return data
        except Exception as e:
            # Database error, fall back to filesystem
            print(f"DB error loading resume, falling back to filesystem: {e}")

    # Fallback to filesystem
    resume_path = resumes_root / resume_filename
    if resume_path.exists():
        return load_yaml(resume_path)

    return {}


def save_subcontent_to_db(job_path: Path, section: str, data) -> bool:
    """
    Save subcontent data to database.

    This is called in addition to filesystem writes to keep DB in sync.

    Args:
        job_path: Path to the job folder.
        section: Section name (contacts, summary, etc.).
        data: Subcontent data.

    Returns:
        True if saved to database, False otherwise.
    """
    if not _db_enabled():
        return False

    job_id = get_job_id_from_path(job_path)
    if not job_id:
        return False

    try:
        subcontent_repo = _get_subcontent_repo()

        if section == "contacts":
            from src.db.models import Contact
            contacts = [
                Contact(
                    name=c.get('name', ''),
                    label=c.get('label', ''),
                    url=c.get('url'),
                    icon=c.get('icon'),
                )
                for c in (data if isinstance(data, list) else [])
            ]
            subcontent_repo.save_contacts(job_id, contacts)

        elif section == "summary":
            content = data if isinstance(data, str) else str(data)
            subcontent_repo.save_summary(job_id, content)

        elif section == "skills":
            skills = data if isinstance(data, list) else []
            subcontent_repo.save_skills(job_id, skills)

        elif section == "highlights":
            highlights = data if isinstance(data, list) else []
            subcontent_repo.save_highlights(job_id, highlights)

        elif section == "experience":
            from src.db.models import Company, Role, Bullet
            companies = []
            for i, comp_data in enumerate(data if isinstance(data, list) else []):
                # Parse company URLs
                urls = comp_data.get('company_urls', [])
                if isinstance(urls, str):
                    urls = [urls]

                # Parse roles
                roles = []
                for j, role_data in enumerate(comp_data.get('roles', [])):
                    # Parse bullets
                    bullets = []
                    for k, bullet_data in enumerate(role_data.get('bullets', [])):
                        bullets.append(Bullet(
                            text=bullet_data.get('text', ''),
                            original_id=bullet_data.get('id'),
                            tags=bullet_data.get('tags', []),
                            sort_order=k,
                        ))

                    roles.append(Role(
                        role=role_data.get('role', ''),
                        original_id=role_data.get('id'),
                        dates=role_data.get('dates'),
                        location=role_data.get('location'),
                        bullets=bullets,
                        sort_order=j,
                    ))

                companies.append(Company(
                    company_name=comp_data.get('company_name', ''),
                    company_urls=urls,
                    employees=comp_data.get('employees'),
                    dates=comp_data.get('dates'),
                    location=comp_data.get('location'),
                    company_description=comp_data.get('company_description'),
                    roles=roles,
                    sort_order=i,
                ))

            subcontent_repo.save_experience(job_id, companies)

        elif section == "education":
            from src.db.models import Education
            education = [
                Education(
                    course=e.get('course', ''),
                    school=e.get('school', ''),
                    dates=e.get('dates'),
                )
                for e in (data if isinstance(data, list) else [])
            ]
            subcontent_repo.save_education(job_id, education)

        elif section == "awards":
            from src.db.models import Award
            awards = [
                Award(
                    award=a.get('award', ''),
                    reward=a.get('reward'),
                    dates=a.get('dates'),
                )
                for a in (data if isinstance(data, list) else [])
            ]
            subcontent_repo.save_awards(job_id, awards)

        elif section == "coverletter":
            content = data if isinstance(data, str) else str(data)
            subcontent_repo.save_coverletter(job_id, content)

        return True

    except Exception as e:
        # Log error but don't fail the event
        print(f"Error saving subcontent to DB: {e}")
        return False


def job_is_duplicate(external_id: Optional[str], company: str, title: str) -> bool:
    """
    Check if a job already exists in the database.

    De-duplicates on:
    1. external_id (LinkedIn job ID)
    2. company + title combination (case-insensitive)

    Args:
        external_id: External job ID (e.g., LinkedIn job ID).
        company: Company name.
        title: Job title.

    Returns:
        True if job is a duplicate, False otherwise.
    """
    if not _db_enabled():
        return False

    try:
        job_repo = _get_job_repo()

        # Check by external_id first
        if external_id and job_repo.external_id_exists(external_id):
            return True

        # Check by company + title
        if job_repo.company_title_exists(company, title):
            return True

        return False
    except Exception as e:
        print(f"Error checking job duplicate: {e}")
        return False


def ingest_job_to_db(job_path: Path, job_data: dict, phase: str = "1_Queued") -> Optional[int]:
    """
    Ingest a job into the database from its data dict.

    Called after YAML file is created to sync job to SQLite.

    Args:
        job_path: Path to the job folder.
        job_data: Job data dictionary (same format as job.yaml).
        phase: Job phase (default "1_Queued").

    Returns:
        Job ID if ingested, None if not (database disabled or error).
    """
    if not _db_enabled():
        return None

    try:
        from src.db.models import Job

        # Parse subcontent_events from list of single-key dicts
        subcontent_events = {}
        for item in job_data.get('subcontent_events', []):
            if isinstance(item, dict):
                for section, event in item.items():
                    subcontent_events[section] = event

        # Create Job object
        job = Job(
            folder_name=job_path.name,
            company=job_data.get('company', ''),
            title=job_data.get('title', ''),
            external_id=str(job_data.get('id', '')) if job_data.get('id') else None,
            url=job_data.get('url'),
            location=job_data.get('location'),
            salary=job_data.get('salary'),
            source=job_data.get('source'),
            date_posted=job_data.get('date') or job_data.get('date_posted'),
            description=job_data.get('description'),
            phase=phase,
            tags=job_data.get('tags', []),
            subcontent_events=subcontent_events,
        )

        job_repo = _get_job_repo()
        job_id = job_repo.upsert_by_folder_name(job)
        return job_id

    except Exception as e:
        print(f"Error ingesting job to DB: {e}")
        return None


def save_artifact_to_db(job_path: Path, artifact_type: str, filename: str, content: bytes, content_type: str) -> bool:
    """
    Save an artifact (HTML, PDF) to the database.

    Args:
        job_path: Path to the job folder.
        artifact_type: Type of artifact (resume_html, resume_pdf, etc.).
        filename: Filename of the artifact.
        content: Binary content.
        content_type: MIME type.

    Returns:
        True if saved to database, False otherwise.
    """
    if not _db_enabled():
        return False

    job_id = get_job_id_from_path(job_path)
    if not job_id:
        return False

    try:
        subcontent_repo = _get_subcontent_repo()
        subcontent_repo.save_artifact(job_id, artifact_type, filename, content, content_type)
        return True
    except Exception as e:
        print(f"Error saving artifact to DB: {e}")
        return False
