"""
Repository for job data access.
"""

import sqlite3
from datetime import datetime
from typing import Optional

from .base_repository import BaseRepository
from ..db.models import Job, JobSummary, PhaseCounts


# Valid phase names
PHASES = [
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

# Active phases (exclude terminal states)
ACTIVE_PHASES = [
    "1_Queued",
    "2_Data_Generated",
    "3_Docs_Generated",
    "4_Applied",
    "5_FollowUp",
    "6_Interviewing",
    "7_Negotiating",
]


class JobRepository(BaseRepository):
    """
    Repository for managing job data.

    Handles job CRUD, phase management, and tag/subcontent event storage.
    """

    # =========================================================================
    # READ OPERATIONS
    # =========================================================================

    def get_by_id(self, job_id: int) -> Optional[Job]:
        """
        Get a job by ID with tags and subcontent events.

        Args:
            job_id: Job database ID.

        Returns:
            Job object or None if not found.
        """
        row = self._fetch_one("SELECT * FROM jobs WHERE id = ?", (job_id,))
        if not row:
            return None

        return self._build_job(row)

    def get_by_folder_name(self, folder_name: str) -> Optional[Job]:
        """
        Get a job by folder name with tags and subcontent events.

        Args:
            folder_name: Job folder name (e.g., "Company.Title.20260115-133050.12345").

        Returns:
            Job object or None if not found.
        """
        row = self._fetch_one(
            "SELECT * FROM jobs WHERE folder_name = ?",
            (folder_name,)
        )
        if not row:
            return None

        return self._build_job(row)

    def get_by_external_id(self, external_id: str) -> Optional[Job]:
        """
        Get a job by external ID (e.g., LinkedIn job ID).

        Args:
            external_id: External job ID.

        Returns:
            Job object or None if not found.
        """
        row = self._fetch_one(
            "SELECT * FROM jobs WHERE external_id = ?",
            (external_id,)
        )
        if not row:
            return None

        return self._build_job(row)

    def get_by_phase(self, phase: str) -> list[JobSummary]:
        """
        Get all jobs in a specific phase.

        Args:
            phase: Phase name (e.g., "1_Queued").

        Returns:
            List of JobSummary objects.
        """
        rows = self._fetch_all(
            "SELECT * FROM jobs WHERE phase = ? ORDER BY created_at DESC",
            (phase,)
        )
        return [self._build_job_summary(row) for row in rows]

    def get_all(self) -> list[JobSummary]:
        """
        Get all jobs.

        Returns:
            List of JobSummary objects.
        """
        rows = self._fetch_all("SELECT * FROM jobs ORDER BY created_at DESC")
        return [self._build_job_summary(row) for row in rows]

    def get_active(self) -> list[JobSummary]:
        """
        Get all jobs in active phases (not Skipped/Expired/Errored/Accepted).

        Returns:
            List of JobSummary objects.
        """
        placeholders = ",".join("?" for _ in ACTIVE_PHASES)
        rows = self._fetch_all(
            f"SELECT * FROM jobs WHERE phase IN ({placeholders}) ORDER BY created_at DESC",
            tuple(ACTIVE_PHASES)
        )
        return [self._build_job_summary(row) for row in rows]

    def get_all_with_counts(self, phase_filter: Optional[str] = None) -> tuple[list[JobSummary], PhaseCounts]:
        """
        Get jobs with phase counts for UI.

        Args:
            phase_filter: Optional filter - "all-active", "all-jobs", or specific phase.

        Returns:
            Tuple of (jobs list, phase counts).
        """
        counts = self.get_phase_counts()

        if phase_filter == "all-jobs":
            jobs = self.get_all()
        elif phase_filter == "all-active":
            jobs = self.get_active()
        elif phase_filter and phase_filter in PHASES:
            jobs = self.get_by_phase(phase_filter)
        else:
            # Default to all active
            jobs = self.get_active()

        return jobs, counts

    def get_phase_counts(self) -> PhaseCounts:
        """
        Get job counts by phase.

        Returns:
            PhaseCounts object with counts for each phase.
        """
        rows = self._fetch_all(
            "SELECT phase, COUNT(*) as count FROM jobs GROUP BY phase"
        )

        counts = PhaseCounts()
        for row in rows:
            phase = row['phase']
            count = row['count']

            if phase == "1_Queued":
                counts.queued = count
            elif phase == "2_Data_Generated":
                counts.data_generated = count
            elif phase == "3_Docs_Generated":
                counts.docs_generated = count
            elif phase == "4_Applied":
                counts.applied = count
            elif phase == "5_FollowUp":
                counts.followup = count
            elif phase == "6_Interviewing":
                counts.interviewing = count
            elif phase == "7_Negotiating":
                counts.negotiating = count
            elif phase == "8_Accepted":
                counts.accepted = count
            elif phase == "Skipped":
                counts.skipped = count
            elif phase == "Expired":
                counts.expired = count
            elif phase == "Errored":
                counts.errored = count

        return counts

    def exists(self, folder_name: str) -> bool:
        """Check if a job with the given folder name exists."""
        return self._exists("jobs", "folder_name = ?", (folder_name,))

    def external_id_exists(self, external_id: str) -> bool:
        """Check if a job with the given external ID exists."""
        return self._exists("jobs", "external_id = ?", (external_id,))

    def company_title_exists(self, company: str, title: str) -> bool:
        """Check if a job with the given company and title exists."""
        return self._exists(
            "jobs",
            "LOWER(company) = LOWER(?) AND LOWER(title) = LOWER(?)",
            (company, title)
        )

    def get_by_company_and_title(self, company: str, title: str) -> Optional[Job]:
        """
        Get a job by company and title (case-insensitive).

        Args:
            company: Company name.
            title: Job title.

        Returns:
            Job object or None if not found.
        """
        row = self._fetch_one(
            "SELECT * FROM jobs WHERE LOWER(company) = LOWER(?) AND LOWER(title) = LOWER(?)",
            (company, title)
        )
        if not row:
            return None

        return self._build_job(row)

    # =========================================================================
    # WRITE OPERATIONS
    # =========================================================================

    def create(self, job: Job) -> int:
        """
        Create a new job with tags and subcontent events.

        Args:
            job: Job object to create.

        Returns:
            ID of the created job.
        """
        self.begin_transaction()
        try:
            # Parse date_posted if it's a string
            date_posted = job.date_posted
            if isinstance(date_posted, str):
                date_posted = date_posted

            job_id = self._insert("jobs", {
                "external_id": job.external_id,
                "folder_name": job.folder_name,
                "company": job.company,
                "title": job.title,
                "url": job.url,
                "location": job.location,
                "salary": job.salary,
                "source": job.source,
                "date_posted": date_posted,
                "description": job.description,
                "phase": job.phase,
                "resume_slug": job.resume_slug,
            })

            # Save tags
            self._save_tags(job_id, job.tags)

            # Save subcontent events
            self._save_subcontent_events(job_id, job.subcontent_events)

            self.commit()
            return job_id
        except Exception:
            self.rollback()
            raise

    def update(self, job_id: int, job: Job) -> None:
        """
        Update an existing job with tags and subcontent events.

        Args:
            job_id: ID of the job to update.
            job: Job object with new data.
        """
        self.begin_transaction()
        try:
            date_posted = job.date_posted
            if isinstance(date_posted, str):
                date_posted = date_posted

            self._update("jobs", {
                "external_id": job.external_id,
                "company": job.company,
                "title": job.title,
                "url": job.url,
                "location": job.location,
                "salary": job.salary,
                "source": job.source,
                "date_posted": date_posted,
                "description": job.description,
                "phase": job.phase,
                "resume_slug": job.resume_slug,
                "updated_at": datetime.now().isoformat(),
            }, "id = ?", (job_id,))

            # Replace tags
            self._delete("job_tags", "job_id = ?", (job_id,))
            self._save_tags(job_id, job.tags)

            # Replace subcontent events
            self._delete("job_subcontent_events", "job_id = ?", (job_id,))
            self._save_subcontent_events(job_id, job.subcontent_events)

            self.commit()
        except Exception:
            self.rollback()
            raise

    def update_phase(self, job_id: int, phase: str) -> None:
        """
        Update the phase of a job.

        Args:
            job_id: ID of the job.
            phase: New phase name.
        """
        if phase not in PHASES:
            raise ValueError(f"Invalid phase: {phase}")

        self._update("jobs", {
            "phase": phase,
            "updated_at": datetime.now().isoformat(),
        }, "id = ?", (job_id,))

    def update_phase_by_folder(self, folder_name: str, phase: str) -> bool:
        """
        Update the phase of a job by folder name.

        Args:
            folder_name: Job folder name.
            phase: New phase name.

        Returns:
            True if updated, False if not found.
        """
        if phase not in PHASES:
            raise ValueError(f"Invalid phase: {phase}")

        rowcount = self._update("jobs", {
            "phase": phase,
            "updated_at": datetime.now().isoformat(),
        }, "folder_name = ?", (folder_name,))

        return rowcount > 0

    def update_subcontent_event(
        self,
        job_id: int,
        section: str,
        event_name: str
    ) -> None:
        """
        Update a single subcontent event for a job.

        Args:
            job_id: Job ID.
            section: Section name (contacts, summary, etc.).
            event_name: Event handler name.
        """
        # Upsert the event
        existing = self._fetch_one(
            "SELECT id FROM job_subcontent_events WHERE job_id = ? AND section = ?",
            (job_id, section)
        )

        if existing:
            self._update("job_subcontent_events", {
                "event_name": event_name,
            }, "id = ?", (existing['id'],))
        else:
            self._insert("job_subcontent_events", {
                "job_id": job_id,
                "section": section,
                "event_name": event_name,
            })

    def delete(self, job_id: int) -> bool:
        """
        Delete a job and all related data.

        Args:
            job_id: ID of the job to delete.

        Returns:
            True if deleted, False if not found.
        """
        rowcount = self._delete("jobs", "id = ?", (job_id,))
        return rowcount > 0

    def upsert_by_external_id(self, job: Job) -> int:
        """
        Create or update a job based on external ID.

        Args:
            job: Job object.

        Returns:
            ID of the job.
        """
        if job.external_id:
            existing = self._fetch_one(
                "SELECT id FROM jobs WHERE external_id = ?",
                (job.external_id,)
            )
            if existing:
                self.update(existing['id'], job)
                return existing['id']

        return self.create(job)

    def upsert_by_folder_name(self, job: Job) -> int:
        """
        Create or update a job based on folder name.

        Args:
            job: Job object.

        Returns:
            ID of the job.
        """
        existing = self._fetch_one(
            "SELECT id FROM jobs WHERE folder_name = ?",
            (job.folder_name,)
        )
        if existing:
            self.update(existing['id'], job)
            return existing['id']

        return self.create(job)

    # =========================================================================
    # EXPORT
    # =========================================================================

    def to_dict(self, job_id: int) -> Optional[dict]:
        """
        Export a job as a YAML-compatible dictionary.

        Args:
            job_id: Job database ID.

        Returns:
            Dictionary matching job.yaml structure.
        """
        job = self.get_by_id(job_id)
        if not job:
            return None

        result = {
            "id": job.external_id,
            "company": job.company,
            "title": job.title,
        }

        if job.url:
            result["url"] = job.url
        if job.location:
            result["location"] = job.location
        if job.salary:
            result["salary"] = job.salary
        if job.tags:
            result["tags"] = job.tags
        if job.source:
            result["source"] = job.source
        if job.date_posted:
            result["date"] = str(job.date_posted)

        # Subcontent events as list of single-key dicts
        if job.subcontent_events:
            result["subcontent_events"] = [
                {section: event}
                for section, event in job.subcontent_events.items()
            ]

        if job.description:
            result["description"] = job.description

        return result

    def to_dict_by_folder(self, folder_name: str) -> Optional[dict]:
        """
        Export a job by folder name as a YAML-compatible dictionary.

        Args:
            folder_name: Job folder name.

        Returns:
            Dictionary matching job.yaml structure.
        """
        row = self._fetch_one(
            "SELECT id FROM jobs WHERE folder_name = ?",
            (folder_name,)
        )
        if not row:
            return None
        return self.to_dict(row['id'])

    # =========================================================================
    # PRIVATE HELPERS
    # =========================================================================

    def _build_job(self, row: dict) -> Job:
        """Build a full Job object from a database row."""
        job_id = row['id']

        # Load tags
        tag_rows = self._fetch_all(
            "SELECT tag FROM job_tags WHERE job_id = ?",
            (job_id,)
        )
        tags = [r['tag'] for r in tag_rows]

        # Load subcontent events as dict
        event_rows = self._fetch_all(
            "SELECT section, event_name FROM job_subcontent_events WHERE job_id = ?",
            (job_id,)
        )
        subcontent_events = {r['section']: r['event_name'] for r in event_rows}

        return Job(
            id=row['id'],
            external_id=row['external_id'],
            folder_name=row['folder_name'],
            company=row['company'],
            title=row['title'],
            url=row['url'],
            location=row['location'],
            salary=row['salary'],
            source=row['source'],
            date_posted=row['date_posted'],
            description=row['description'],
            phase=row['phase'],
            resume_slug=row['resume_slug'],
            tags=tags,
            subcontent_events=subcontent_events,
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )

    def _build_job_summary(self, row: dict) -> JobSummary:
        """Build a JobSummary object from a database row."""
        job_id = row['id']

        # Load tags
        tag_rows = self._fetch_all(
            "SELECT tag FROM job_tags WHERE job_id = ?",
            (job_id,)
        )
        tags = [r['tag'] for r in tag_rows]

        return JobSummary(
            id=row['id'],
            folder_name=row['folder_name'],
            company=row['company'],
            title=row['title'],
            phase=row['phase'],
            location=row['location'],
            salary=row['salary'],
            source=row['source'],
            date_posted=row['date_posted'],
            tags=tags,
        )

    def _save_tags(self, job_id: int, tags: list[str]) -> None:
        """Save tags for a job."""
        for tag in tags:
            self._insert("job_tags", {
                "job_id": job_id,
                "tag": tag,
            })

    def _save_subcontent_events(
        self,
        job_id: int,
        events: dict[str, str]
    ) -> None:
        """Save subcontent events for a job."""
        for section, event_name in events.items():
            self._insert("job_subcontent_events", {
                "job_id": job_id,
                "section": section,
                "event_name": event_name,
            })
