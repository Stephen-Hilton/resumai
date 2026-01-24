"""
Repository for job file metadata access.

Provides data access methods for the job_files table, which tracks
all files associated with jobs in the partitioned file system.
"""

from datetime import datetime
from typing import Optional

from .base_repository import BaseRepository
from ..db.models import JobFile


class JobFileRepository(BaseRepository):
    """
    Repository for managing job file metadata.

    Handles CRUD operations for the job_files table, which stores
    metadata about files stored in the src/files/YYYYMM/ directory structure.
    """

    # =========================================================================
    # CREATE OPERATIONS
    # =========================================================================

    def create(self, job_file: JobFile) -> int:
        """
        Create a new file record.

        Args:
            job_file: JobFile object containing file metadata.

        Returns:
            ID of the created file record.

        Raises:
            sqlite3.IntegrityError: If a record with the same job_id and 
                file_purpose already exists (unique constraint violation).
        """
        return self._insert("job_files", {
            "job_id": job_file.job_id,
            "filename": job_file.filename,
            "file_path": job_file.file_path,
            "file_purpose": job_file.file_purpose,
            "file_source": job_file.file_source,
        })

    # =========================================================================
    # READ OPERATIONS
    # =========================================================================

    def get_by_id(self, file_id: int) -> Optional[JobFile]:
        """
        Get a file record by ID.

        Args:
            file_id: File record database ID.

        Returns:
            JobFile object or None if not found.
        """
        row = self._fetch_one(
            "SELECT * FROM job_files WHERE id = ?",
            (file_id,)
        )
        if not row:
            return None
        return self._build_job_file(row)

    def get_by_job_id(self, job_id: int) -> list[JobFile]:
        """
        Get all files for a job.

        Args:
            job_id: Job database ID.

        Returns:
            List of JobFile objects. Returns empty list if no files found.
        """
        rows = self._fetch_all(
            "SELECT * FROM job_files WHERE job_id = ? ORDER BY created_at",
            (job_id,)
        )
        return [self._build_job_file(row) for row in rows]

    def get_by_job_and_purpose(
        self,
        job_id: int,
        file_purpose: str
    ) -> Optional[JobFile]:
        """
        Get a specific file by job and purpose.

        Args:
            job_id: Job database ID.
            file_purpose: Purpose of the file (e.g., 'resume_html', 'resume_pdf').

        Returns:
            JobFile object or None if not found.
        """
        row = self._fetch_one(
            "SELECT * FROM job_files WHERE job_id = ? AND file_purpose = ?",
            (job_id, file_purpose)
        )
        if not row:
            return None
        return self._build_job_file(row)

    def exists(self, job_id: int, file_purpose: str) -> bool:
        """
        Check if a file record exists for a given job and purpose.

        Args:
            job_id: Job database ID.
            file_purpose: Purpose of the file.

        Returns:
            True if a record exists, False otherwise.
        """
        return self._exists(
            "job_files",
            "job_id = ? AND file_purpose = ?",
            (job_id, file_purpose)
        )

    # =========================================================================
    # DELETE OPERATIONS
    # =========================================================================

    def delete(self, file_id: int) -> bool:
        """
        Delete a file record by ID.

        Args:
            file_id: File record database ID.

        Returns:
            True if a record was deleted, False if not found.
        """
        rowcount = self._delete("job_files", "id = ?", (file_id,))
        return rowcount > 0

    def delete_by_job_id(self, job_id: int) -> int:
        """
        Delete all file records for a job.

        Args:
            job_id: Job database ID.

        Returns:
            Number of records deleted.
        """
        return self._delete("job_files", "job_id = ?", (job_id,))

    # =========================================================================
    # EXPORT
    # =========================================================================

    def to_dict(self, file_id: int) -> Optional[dict]:
        """
        Export a file record as a dictionary.

        Args:
            file_id: File record database ID.

        Returns:
            Dictionary representation of the file record, or None if not found.
        """
        job_file = self.get_by_id(file_id)
        if not job_file:
            return None

        # Handle timestamps - they may be strings from SQLite or datetime objects
        created_at = job_file.created_at
        if created_at and hasattr(created_at, 'isoformat'):
            created_at = created_at.isoformat()
        
        updated_at = job_file.updated_at
        if updated_at and hasattr(updated_at, 'isoformat'):
            updated_at = updated_at.isoformat()

        return {
            "id": job_file.id,
            "job_id": job_file.job_id,
            "filename": job_file.filename,
            "file_path": job_file.file_path,
            "file_purpose": job_file.file_purpose,
            "file_source": job_file.file_source,
            "created_at": created_at,
            "updated_at": updated_at,
        }

    # =========================================================================
    # PRIVATE HELPERS
    # =========================================================================

    def _build_job_file(self, row: dict) -> JobFile:
        """
        Build a JobFile object from a database row.

        Args:
            row: Dictionary with column values from the database.

        Returns:
            JobFile object.
        """
        return JobFile(
            id=row['id'],
            job_id=row['job_id'],
            filename=row['filename'],
            file_path=row['file_path'],
            file_purpose=row['file_purpose'],
            file_source=row['file_source'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
        )
