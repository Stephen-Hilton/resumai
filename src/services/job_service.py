"""
Job service for business logic.
"""

import sqlite3
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..db.connection import get_connection
from ..db.models import (
    Job, JobSummary, JobDetail, PhaseCounts,
    SubcontentStatus, DocStatus
)
from ..repositories.job_repository import JobRepository, PHASES, ACTIVE_PHASES
from ..repositories.subcontent_repository import SubcontentRepository


class JobService:
    """
    Service for job business logic.

    Provides high-level operations for job management including
    phase transitions and subcontent status.
    """

    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize the service.

        Args:
            conn: Optional database connection.
        """
        self.conn = conn or get_connection()
        self.job_repo = JobRepository(self.conn)
        self.subcontent_repo = SubcontentRepository(self.conn)

    # =========================================================================
    # READ OPERATIONS
    # =========================================================================

    def get_job(self, folder_name: str) -> Optional[Job]:
        """
        Get a job by folder name.

        Args:
            folder_name: Job folder name.

        Returns:
            Job object or None if not found.
        """
        return self.job_repo.get_by_folder_name(folder_name)

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        """
        Get a job by ID.

        Args:
            job_id: Database ID.

        Returns:
            Job object or None if not found.
        """
        return self.job_repo.get_by_id(job_id)

    def get_job_detail(self, folder_name: str) -> Optional[JobDetail]:
        """
        Get full job details with status information.

        Args:
            folder_name: Job folder name.

        Returns:
            JobDetail with job, subcontent status, and doc status.
        """
        job = self.job_repo.get_by_folder_name(folder_name)
        if not job:
            return None

        subcontent_status = self.subcontent_repo.get_subcontent_status(job.id)
        doc_status = self.subcontent_repo.get_doc_status(job.id)

        return JobDetail(
            job=job,
            subcontent_status=subcontent_status,
            doc_status=doc_status,
        )

    def get_jobs_for_ui(
        self,
        phase_filter: Optional[str] = None
    ) -> dict:
        """
        Get jobs and counts for UI display.

        Args:
            phase_filter: Optional filter - "all-active", "all-jobs", or specific phase.

        Returns:
            Dictionary with 'jobs' and 'phase_counts' keys.
        """
        jobs, counts = self.job_repo.get_all_with_counts(phase_filter)

        return {
            "jobs": [self._job_summary_to_dict(j) for j in jobs],
            "phase_counts": asdict(counts),
        }

    def get_phase_counts(self) -> PhaseCounts:
        """
        Get job counts by phase.

        Returns:
            PhaseCounts object.
        """
        return self.job_repo.get_phase_counts()

    def job_exists(self, folder_name: str) -> bool:
        """
        Check if a job exists.

        Args:
            folder_name: Job folder name.

        Returns:
            True if job exists.
        """
        return self.job_repo.exists(folder_name)

    def external_id_exists(self, external_id: str) -> bool:
        """
        Check if a job with the given external ID exists.

        Args:
            external_id: External job ID.

        Returns:
            True if job exists.
        """
        return self.job_repo.external_id_exists(external_id)

    # =========================================================================
    # WRITE OPERATIONS
    # =========================================================================

    def create_job(self, job: Job) -> int:
        """
        Create a new job.

        Args:
            job: Job object.

        Returns:
            ID of the created job.
        """
        return self.job_repo.create(job)

    def update_job(self, folder_name: str, job: Job) -> bool:
        """
        Update an existing job.

        Args:
            folder_name: Job folder name.
            job: Job object with new data.

        Returns:
            True if updated, False if not found.
        """
        existing = self.job_repo.get_by_folder_name(folder_name)
        if not existing:
            return False

        self.job_repo.update(existing.id, job)
        return True

    def update_job_data(self, folder_name: str, data: dict) -> bool:
        """
        Update specific fields of a job.

        Args:
            folder_name: Job folder name.
            data: Dictionary of fields to update.

        Returns:
            True if updated, False if not found.
        """
        existing = self.job_repo.get_by_folder_name(folder_name)
        if not existing:
            return False

        # Merge with existing job
        job = Job(
            folder_name=existing.folder_name,
            company=data.get('company', existing.company),
            title=data.get('title', existing.title),
            external_id=data.get('id', existing.external_id),
            url=data.get('url', existing.url),
            location=data.get('location', existing.location),
            salary=data.get('salary', existing.salary),
            source=data.get('source', existing.source),
            date_posted=data.get('date', existing.date_posted),
            description=data.get('description', existing.description),
            phase=existing.phase,
            resume_slug=existing.resume_slug,
            tags=data.get('tags', existing.tags),
            subcontent_events=self._parse_subcontent_events(
                data.get('subcontent_events', [])
            ) if 'subcontent_events' in data else existing.subcontent_events,
        )

        self.job_repo.update(existing.id, job)
        return True

    def upsert_job(self, job: Job) -> int:
        """
        Create or update a job based on folder name.

        Args:
            job: Job object.

        Returns:
            ID of the job.
        """
        return self.job_repo.upsert_by_folder_name(job)

    def delete_job(self, folder_name: str) -> bool:
        """
        Delete a job and all related data.

        Args:
            folder_name: Job folder name.

        Returns:
            True if deleted, False if not found.
        """
        existing = self.job_repo.get_by_folder_name(folder_name)
        if not existing:
            return False

        return self.job_repo.delete(existing.id)

    # =========================================================================
    # PHASE MANAGEMENT
    # =========================================================================

    def move_to_phase(self, folder_name: str, phase: str) -> bool:
        """
        Move a job to a different phase.

        Args:
            folder_name: Job folder name.
            phase: Target phase name.

        Returns:
            True if moved, False if job not found.

        Raises:
            ValueError: If phase is invalid.
        """
        if phase not in PHASES:
            raise ValueError(f"Invalid phase: {phase}. Valid phases: {PHASES}")

        return self.job_repo.update_phase_by_folder(folder_name, phase)

    def move_to_queue(self, folder_name: str) -> bool:
        """Move job to 1_Queued."""
        return self.move_to_phase(folder_name, "1_Queued")

    def move_to_data_generated(self, folder_name: str) -> bool:
        """Move job to 2_Data_Generated."""
        return self.move_to_phase(folder_name, "2_Data_Generated")

    def move_to_docs_generated(self, folder_name: str) -> bool:
        """Move job to 3_Docs_Generated."""
        return self.move_to_phase(folder_name, "3_Docs_Generated")

    def move_to_applied(self, folder_name: str) -> bool:
        """Move job to 4_Applied."""
        return self.move_to_phase(folder_name, "4_Applied")

    def move_to_followup(self, folder_name: str) -> bool:
        """Move job to 5_FollowUp."""
        return self.move_to_phase(folder_name, "5_FollowUp")

    def move_to_interviewing(self, folder_name: str) -> bool:
        """Move job to 6_Interviewing."""
        return self.move_to_phase(folder_name, "6_Interviewing")

    def move_to_negotiating(self, folder_name: str) -> bool:
        """Move job to 7_Negotiating."""
        return self.move_to_phase(folder_name, "7_Negotiating")

    def move_to_accepted(self, folder_name: str) -> bool:
        """Move job to 8_Accepted."""
        return self.move_to_phase(folder_name, "8_Accepted")

    def move_to_skipped(self, folder_name: str) -> bool:
        """Move job to Skipped."""
        return self.move_to_phase(folder_name, "Skipped")

    def move_to_expired(self, folder_name: str) -> bool:
        """Move job to Expired."""
        return self.move_to_phase(folder_name, "Expired")

    def move_to_errored(self, folder_name: str) -> bool:
        """Move job to Errored."""
        return self.move_to_phase(folder_name, "Errored")

    # =========================================================================
    # SUBCONTENT EVENT MANAGEMENT
    # =========================================================================

    def update_subcontent_event(
        self,
        folder_name: str,
        section: str,
        event_name: str
    ) -> bool:
        """
        Update a subcontent event for a job.

        Args:
            folder_name: Job folder name.
            section: Section name (contacts, summary, etc.).
            event_name: Event handler name.

        Returns:
            True if updated, False if job not found.
        """
        job = self.job_repo.get_by_folder_name(folder_name)
        if not job:
            return False

        self.job_repo.update_subcontent_event(job.id, section, event_name)
        return True

    def toggle_generation_mode(
        self,
        folder_name: str,
        section: str
    ) -> Optional[str]:
        """
        Toggle between static and LLM generation for a section.

        Args:
            folder_name: Job folder name.
            section: Section name.

        Returns:
            New event name, or None if job not found.
        """
        job = self.job_repo.get_by_folder_name(folder_name)
        if not job:
            return None

        current_event = job.subcontent_events.get(section, "")

        # Toggle between static and LLM
        if current_event.startswith("gen_static_"):
            new_event = current_event.replace("gen_static_", "gen_llm_")
        elif current_event.startswith("gen_llm_"):
            new_event = current_event.replace("gen_llm_", "gen_static_")
        else:
            # Default to LLM if unknown
            new_event = f"gen_llm_subcontent_{section}"

        self.job_repo.update_subcontent_event(job.id, section, new_event)
        return new_event

    # =========================================================================
    # EXPORT
    # =========================================================================

    def export_to_dict(self, folder_name: str) -> Optional[dict]:
        """
        Export a job as a YAML-compatible dictionary.

        Args:
            folder_name: Job folder name.

        Returns:
            Dictionary matching job.yaml structure.
        """
        return self.job_repo.to_dict_by_folder(folder_name)

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_job_stats(self) -> dict:
        """
        Get job statistics for dashboard.

        Returns:
            Dictionary with various statistics.
        """
        counts = self.job_repo.get_phase_counts()

        # Source counts
        source_rows = self.job_repo._fetch_all(
            "SELECT source, COUNT(*) as count FROM jobs GROUP BY source"
        )
        sources = {r['source'] or 'unknown': r['count'] for r in source_rows}

        return {
            "phase_counts": asdict(counts),
            "source_counts": sources,
            "total": sum(asdict(counts).values()),
            "active": (
                counts.queued + counts.data_generated + counts.docs_generated +
                counts.applied + counts.followup + counts.interviewing +
                counts.negotiating
            ),
        }

    # =========================================================================
    # PRIVATE HELPERS
    # =========================================================================

    def _job_summary_to_dict(self, job: JobSummary) -> dict:
        """Convert JobSummary to dict for UI."""
        return {
            "id": job.id,
            "folder_name": job.folder_name,
            "company": job.company,
            "title": job.title,
            "phase": job.phase,
            "location": job.location,
            "salary": job.salary,
            "source": job.source,
            "date": str(job.date_posted) if job.date_posted else None,
            "tags": job.tags,
        }

    def _parse_subcontent_events(self, events_list: list) -> dict[str, str]:
        """
        Parse subcontent_events from YAML format to dict.

        YAML format is a list of single-key dicts:
        - contacts: gen_static_subcontent_contacts
        - summary: gen_llm_subcontent_summary
        """
        result = {}
        for item in events_list:
            if isinstance(item, dict):
                for section, event in item.items():
                    result[section] = event
        return result
