"""
Resume service for business logic.
"""

import sqlite3
from pathlib import Path
from typing import Optional

from ..db.connection import get_connection
from ..db.models import Resume
from ..repositories.resume_repository import ResumeRepository


class ResumeService:
    """
    Service for resume business logic.

    Provides high-level operations for resume management.
    """

    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize the service.

        Args:
            conn: Optional database connection.
        """
        self.conn = conn or get_connection()
        self.repo = ResumeRepository(self.conn)

    def get_resume(self, slug: str) -> Optional[Resume]:
        """
        Get a full resume by slug.

        Args:
            slug: Resume slug (filename without .yaml).

        Returns:
            Resume object or None if not found.
        """
        return self.repo.get_by_slug(slug)

    def get_resume_by_id(self, resume_id: int) -> Optional[Resume]:
        """
        Get a full resume by ID.

        Args:
            resume_id: Database ID.

        Returns:
            Resume object or None if not found.
        """
        return self.repo.get_by_id(resume_id)

    def get_all_resumes(self) -> list[Resume]:
        """
        Get all resumes (metadata only).

        Returns:
            List of Resume objects with basic info.
        """
        return self.repo.get_all()

    def get_resume_slugs(self) -> list[str]:
        """
        Get all resume slugs.

        Returns:
            List of slug strings.
        """
        return self.repo.get_all_slugs()

    def resume_exists(self, slug: str) -> bool:
        """
        Check if a resume exists.

        Args:
            slug: Resume slug.

        Returns:
            True if resume exists.
        """
        return self.repo.exists(slug)

    def create_resume(self, resume: Resume) -> int:
        """
        Create a new resume.

        Args:
            resume: Resume object.

        Returns:
            ID of the created resume.
        """
        return self.repo.create(resume)

    def update_resume(self, slug: str, resume: Resume) -> bool:
        """
        Update an existing resume.

        Args:
            slug: Resume slug.
            resume: Resume object with new data.

        Returns:
            True if updated, False if not found.
        """
        existing = self.repo.get_by_slug(slug)
        if not existing:
            return False

        self.repo.update(existing.id, resume)
        return True

    def upsert_resume(self, resume: Resume) -> int:
        """
        Create or update a resume.

        Args:
            resume: Resume object.

        Returns:
            ID of the resume.
        """
        return self.repo.upsert(resume)

    def delete_resume(self, slug: str) -> bool:
        """
        Delete a resume.

        Args:
            slug: Resume slug.

        Returns:
            True if deleted, False if not found.
        """
        existing = self.repo.get_by_slug(slug)
        if not existing:
            return False

        return self.repo.delete(existing.id)

    def export_to_dict(self, slug: str) -> Optional[dict]:
        """
        Export a resume as a YAML-compatible dictionary.

        Args:
            slug: Resume slug.

        Returns:
            Dictionary matching original YAML structure.
        """
        return self.repo.to_dict_by_slug(slug)

    def get_resumes_for_ui(self) -> list[dict]:
        """
        Get resumes formatted for UI display.

        Returns:
            List of dicts with slug and name.
        """
        resumes = self.repo.get_all()
        return [
            {
                "slug": r.slug,
                "name": r.name,
                "location": r.location,
            }
            for r in resumes
        ]
