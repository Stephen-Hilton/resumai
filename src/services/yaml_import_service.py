"""
YAML import service for migrating data to SQLite.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional
import yaml

from ..db.connection import get_connection
from ..db.models import (
    Resume, Contact, Company, Role, Bullet, Education, Award,
    Job
)
from ..repositories.resume_repository import ResumeRepository
from ..repositories.job_repository import JobRepository
from ..repositories.subcontent_repository import SubcontentRepository


class YamlImportService:
    """
    Service for importing YAML data into SQLite.

    Used for initial migration from file-based storage.
    """

    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize the service.

        Args:
            conn: Optional database connection.
        """
        self.conn = conn or get_connection()
        self.resume_repo = ResumeRepository(self.conn)
        self.job_repo = JobRepository(self.conn)
        self.subcontent_repo = SubcontentRepository(self.conn)

    # =========================================================================
    # RESUME IMPORT
    # =========================================================================

    def import_resume(self, yaml_path: Path) -> int:
        """
        Import a resume YAML file into the database.

        Args:
            yaml_path: Path to the YAML file.

        Returns:
            ID of the imported resume.
        """
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        slug = yaml_path.stem  # Filename without extension
        resume = self._parse_resume(slug, data)

        return self.resume_repo.upsert(resume)

    def import_all_resumes(self, resumes_root: Path) -> list[str]:
        """
        Import all resume YAML files from a directory.

        Args:
            resumes_root: Path to the resumes directory.

        Returns:
            List of imported resume slugs.
        """
        imported = []

        for yaml_path in resumes_root.glob("*.yaml"):
            try:
                self.import_resume(yaml_path)
                imported.append(yaml_path.stem)
            except Exception as e:
                print(f"Error importing {yaml_path}: {e}")

        return imported

    def _parse_resume(self, slug: str, data: dict) -> Resume:
        """Parse YAML data into a Resume object."""
        # Extract icon folder URL from internal section
        icon_folder_url = None
        if 'internal' in data and 'folders' in data['internal']:
            for folder in data['internal']['folders']:
                if 'icons' in folder:
                    icon_folder_url = folder['icons']
                    break

        # Parse contacts
        contacts = []
        for i, c in enumerate(data.get('contacts', [])):
            contacts.append(Contact(
                name=c.get('name', ''),
                label=c.get('label', ''),
                url=c.get('url'),
                icon=c.get('icon'),
                sort_order=i,
            ))

        # Parse skills
        skills = data.get('skills', [])

        # Parse experience
        experience = []
        for i, comp in enumerate(data.get('experience', [])):
            experience.append(self._parse_company(comp, i))

        # Parse education
        education = []
        for i, edu in enumerate(data.get('education', [])):
            education.append(Education(
                course=edu.get('course', ''),
                school=edu.get('school', ''),
                dates=edu.get('dates'),
                sort_order=i,
            ))

        # Parse awards
        awards = []
        for i, award in enumerate(data.get('awards_and_keynotes', [])):
            awards.append(Award(
                award=award.get('award', ''),
                reward=award.get('reward'),
                dates=award.get('dates'),
                sort_order=i,
            ))

        # Parse passions and enjoys
        passions = data.get('passions', [])
        enjoys = data.get('enjoys', [])

        return Resume(
            slug=slug,
            name=data.get('name', ''),
            location=data.get('location'),
            summary=data.get('summary'),
            icon_folder_url=icon_folder_url,
            contacts=contacts,
            skills=skills,
            experience=experience,
            education=education,
            awards_and_keynotes=awards,
            passions=passions,
            enjoys=enjoys,
        )

    def _parse_company(self, data: dict, sort_order: int) -> Company:
        """Parse a company from YAML data."""
        # Handle company_urls - can be string or list
        urls = data.get('company_urls', [])
        if isinstance(urls, str):
            urls = [urls]

        # Parse roles
        roles = []
        for i, role_data in enumerate(data.get('roles', [])):
            roles.append(self._parse_role(role_data, i))

        return Company(
            company_name=data.get('company_name', ''),
            company_urls=urls,
            employees=data.get('employees'),
            dates=data.get('dates'),
            location=data.get('location'),
            company_description=data.get('company_description'),
            roles=roles,
            sort_order=sort_order,
        )

    def _parse_role(self, data: dict, sort_order: int) -> Role:
        """Parse a role from YAML data."""
        bullets = []
        for i, bullet_data in enumerate(data.get('bullets', [])):
            bullets.append(self._parse_bullet(bullet_data, i))

        return Role(
            role=data.get('role', ''),
            original_id=data.get('id'),
            dates=data.get('dates'),
            location=data.get('location'),
            bullets=bullets,
            sort_order=sort_order,
        )

    def _parse_bullet(self, data: dict, sort_order: int) -> Bullet:
        """Parse a bullet from YAML data."""
        return Bullet(
            text=data.get('text', ''),
            original_id=data.get('id'),
            tags=data.get('tags', []),
            sort_order=sort_order,
        )

    # =========================================================================
    # JOB IMPORT
    # =========================================================================

    def import_job_folder(self, folder_path: Path, phase: str) -> Optional[int]:
        """
        Import a job folder into the database.

        Args:
            folder_path: Path to the job folder.
            phase: Phase the job is in (e.g., "1_Queued").

        Returns:
            ID of the imported job, or None if no job.yaml found.
        """
        job_yaml_path = folder_path / "job.yaml"
        if not job_yaml_path.exists():
            return None

        with open(job_yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        folder_name = folder_path.name
        job = self._parse_job(folder_name, phase, data)

        job_id = self.job_repo.upsert_by_folder_name(job)

        # Import subcontent files
        self._import_subcontent(job_id, folder_path)

        return job_id

    def import_all_jobs(self, jobs_root: Path) -> dict:
        """
        Import all job folders from a jobs directory.

        Walks all phase directories and imports each job folder.

        Args:
            jobs_root: Path to the jobs root directory.

        Returns:
            Dictionary with phase: count mappings.
        """
        results = {}

        # Phase directories to scan
        phases = [
            "1_Queued",
            "2_Data_Generated",
            "3_Docs_Generated",
            "4_Applied",
            "5_FollowUp",
            "6_Interviewing",
            "7_Negotiating",
            "8_Accepted",
            "Skipped",
            "Expired",
            "Errored",
        ]

        for phase in phases:
            phase_dir = jobs_root / phase
            if not phase_dir.exists():
                continue

            count = 0
            for folder_path in phase_dir.iterdir():
                if folder_path.is_dir():
                    try:
                        job_id = self.import_job_folder(folder_path, phase)
                        if job_id:
                            count += 1
                    except Exception as e:
                        print(f"Error importing {folder_path}: {e}")

            results[phase] = count

        return results

    def _parse_job(self, folder_name: str, phase: str, data: dict) -> Job:
        """Parse YAML data into a Job object."""
        # Parse subcontent_events from list of single-key dicts
        # Handle null/None values by using empty list as fallback
        subcontent_events = {}
        subcontent_events_raw = data.get('subcontent_events') or []
        for item in subcontent_events_raw:
            if isinstance(item, dict):
                for section, event in item.items():
                    subcontent_events[section] = event

        # Handle null/None tags
        tags = data.get('tags') or []

        return Job(
            folder_name=folder_name,
            company=data.get('company', ''),
            title=data.get('title', ''),
            external_id=str(data.get('id', '')) if data.get('id') else None,
            url=data.get('url'),
            location=data.get('location'),
            salary=data.get('salary'),
            source=data.get('source'),
            date_posted=data.get('date'),
            description=data.get('description'),
            phase=phase,
            tags=tags,
            subcontent_events=subcontent_events,
        )

    def _import_subcontent(self, job_id: int, folder_path: Path) -> None:
        """Import subcontent files for a job."""
        # Import contacts
        contacts_path = folder_path / "subcontent.contacts.yaml"
        if contacts_path.exists():
            self._import_contacts(job_id, contacts_path)

        # Import summary
        summary_path = folder_path / "subcontent.summary.yaml"
        if summary_path.exists():
            self._import_summary(job_id, summary_path)

        # Import skills
        skills_path = folder_path / "subcontent.skills.yaml"
        if skills_path.exists():
            self._import_skills(job_id, skills_path)

        # Import highlights
        highlights_path = folder_path / "subcontent.highlights.yaml"
        if highlights_path.exists():
            self._import_highlights(job_id, highlights_path)

        # Import experience
        experience_path = folder_path / "subcontent.experience.yaml"
        if experience_path.exists():
            self._import_experience(job_id, experience_path)

        # Import education
        education_path = folder_path / "subcontent.education.yaml"
        if education_path.exists():
            self._import_education(job_id, education_path)

        # Import awards
        awards_path = folder_path / "subcontent.awards.yaml"
        if awards_path.exists():
            self._import_awards(job_id, awards_path)

        # Import coverletter
        coverletter_path = folder_path / "subcontent.coverletter.yaml"
        if coverletter_path.exists():
            self._import_coverletter(job_id, coverletter_path)

        # Import artifacts (HTML, PDF)
        self._import_artifacts(job_id, folder_path)

    def _import_contacts(self, job_id: int, path: Path) -> None:
        """Import contacts subcontent."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data:
            return

        contacts = []
        for i, c in enumerate(data):
            contacts.append(Contact(
                name=c.get('name', ''),
                label=c.get('label', ''),
                url=c.get('url'),
                icon=c.get('icon'),
                sort_order=i,
            ))

        self.subcontent_repo.save_contacts(job_id, contacts)

    def _import_summary(self, job_id: int, path: Path) -> None:
        """Import summary subcontent."""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        # Summary might be raw text or YAML-encoded string
        if content:
            # Try to parse as YAML first (in case it's a quoted string)
            try:
                parsed = yaml.safe_load(content)
                if isinstance(parsed, str):
                    content = parsed
            except:
                pass

            self.subcontent_repo.save_summary(job_id, content)

    def _import_skills(self, job_id: int, path: Path) -> None:
        """Import skills subcontent."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if data and isinstance(data, list):
            self.subcontent_repo.save_skills(job_id, data)

    def _import_highlights(self, job_id: int, path: Path) -> None:
        """Import highlights subcontent."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if data and isinstance(data, list):
            self.subcontent_repo.save_highlights(job_id, data)

    def _import_experience(self, job_id: int, path: Path) -> None:
        """Import experience subcontent."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data:
            return

        companies = []
        for i, comp in enumerate(data):
            companies.append(self._parse_company(comp, i))

        self.subcontent_repo.save_experience(job_id, companies)

    def _import_education(self, job_id: int, path: Path) -> None:
        """Import education subcontent."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data:
            return

        education = []
        for i, edu in enumerate(data):
            education.append(Education(
                course=edu.get('course', ''),
                school=edu.get('school', ''),
                dates=edu.get('dates'),
                sort_order=i,
            ))

        self.subcontent_repo.save_education(job_id, education)

    def _import_awards(self, job_id: int, path: Path) -> None:
        """Import awards subcontent."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data:
            return

        awards = []
        for i, award in enumerate(data):
            awards.append(Award(
                award=award.get('award', ''),
                reward=award.get('reward'),
                dates=award.get('dates'),
                sort_order=i,
            ))

        self.subcontent_repo.save_awards(job_id, awards)

    def _import_coverletter(self, job_id: int, path: Path) -> None:
        """Import coverletter subcontent."""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if content:
            # Try to parse as YAML first
            try:
                parsed = yaml.safe_load(content)
                if isinstance(parsed, str):
                    content = parsed
            except:
                pass

            self.subcontent_repo.save_coverletter(job_id, content)

    def _import_artifacts(self, job_id: int, folder_path: Path) -> None:
        """Import artifact files (HTML, PDF)."""
        artifact_mappings = [
            ("resume.html", "resume_html", "text/html"),
            ("resume.pdf", "resume_pdf", "application/pdf"),
            ("coverletter.html", "coverletter_html", "text/html"),
            ("coverletter.pdf", "coverletter_pdf", "application/pdf"),
        ]

        for filename, artifact_type, content_type in artifact_mappings:
            path = folder_path / filename
            if path.exists():
                with open(path, 'rb') as f:
                    content = f.read()
                self.subcontent_repo.save_artifact(
                    job_id, artifact_type, filename, content, content_type
                )
