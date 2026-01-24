"""
File storage service for coordinated file operations.

Provides atomic file storage operations that coordinate between the
filesystem and database, ensuring consistency between file locations
and their metadata records.
"""

import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

from ..db.models import JobFile
from ..repositories.job_file_repository import JobFileRepository


logger = logging.getLogger(__name__)


class FileStorageService:
    """
    Service for coordinated file storage operations.

    Manages file storage in partitioned YYYYMM folders and maintains
    database records for all stored files. Ensures atomic operations
    where both filesystem and database are kept in sync.

    Attributes:
        base_path: Base directory for file storage (default: src/files).
        file_repo: Repository for job file metadata.
    """

    def __init__(self, base_path: Path = Path("src/files")):
        """
        Initialize the file storage service.

        Args:
            base_path: Base directory for file storage.
        """
        self.base_path = base_path
        self.file_repo = JobFileRepository()
        logger.debug(f"FileStorageService initialized with base_path: {base_path}")

    # =========================================================================
    # PUBLIC METHODS
    # =========================================================================

    def store_file(
        self,
        job_id: int,
        content: Union[bytes, str],
        file_purpose: str,
        file_source: str,
        extension: str
    ) -> JobFile:
        """
        Store a file and create database record atomically.

        Creates the partition folder if needed, writes the file to disk,
        and creates a database record. If any step fails, ensures cleanup
        to maintain consistency.

        Args:
            job_id: ID of the job this file belongs to.
            content: File content (bytes or string).
            file_purpose: Purpose of the file (e.g., 'resume_html', 'resume_pdf').
            file_source: Source of the file (e.g., 'url_fetch', 'generated').
            extension: File extension without dot (e.g., 'html', 'pdf').

        Returns:
            JobFile record with the created file metadata.

        Raises:
            OSError: If file write fails.
            sqlite3.IntegrityError: If database record creation fails.
        """
        logger.info(
            f"Storing file for job_id={job_id}, purpose={file_purpose}, "
            f"source={file_source}, extension={extension}"
        )

        # Generate partition path and ensure it exists
        partition_path = self._generate_partition_path()
        full_partition_path = self.base_path / partition_path
        full_partition_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Partition path: {full_partition_path}")

        # Generate unique filename
        filename = self._generate_unique_filename(job_id, file_purpose, extension)
        file_path = partition_path / filename
        full_file_path = self.base_path / file_path
        logger.debug(f"Generated filename: {filename}, full path: {full_file_path}")

        # Write file to disk
        try:
            if isinstance(content, str):
                full_file_path.write_text(content, encoding='utf-8')
            else:
                full_file_path.write_bytes(content)
            logger.debug(f"File written successfully: {full_file_path}")
        except OSError as e:
            logger.error(f"Failed to write file {full_file_path}: {e}")
            raise

        # Create database record
        job_file = JobFile(
            job_id=job_id,
            filename=filename,
            file_path=str(self.base_path / file_path),
            file_purpose=file_purpose,
            file_source=file_source,
        )

        try:
            file_id = self.file_repo.create(job_file)
            job_file.id = file_id
            logger.info(
                f"File stored successfully: id={file_id}, path={job_file.file_path}"
            )
        except Exception as e:
            # Cleanup: remove the file if database insert fails
            logger.error(f"Database insert failed, cleaning up file: {e}")
            try:
                full_file_path.unlink()
                logger.debug(f"Cleaned up file: {full_file_path}")
            except OSError as cleanup_error:
                logger.warning(f"Failed to cleanup file {full_file_path}: {cleanup_error}")
            raise

        return job_file

    def get_file_path(self, job_id: int, file_purpose: str) -> Optional[Path]:
        """
        Get the filesystem path for a file.

        Args:
            job_id: ID of the job.
            file_purpose: Purpose of the file.

        Returns:
            Path to the file, or None if not found.
        """
        logger.debug(f"Getting file path for job_id={job_id}, purpose={file_purpose}")
        
        job_file = self.file_repo.get_by_job_and_purpose(job_id, file_purpose)
        if not job_file:
            logger.debug(f"No file record found for job_id={job_id}, purpose={file_purpose}")
            return None

        path = Path(job_file.file_path)
        logger.debug(f"Found file path: {path}")
        return path

    def get_file_content(
        self,
        job_id: int,
        file_purpose: str
    ) -> Optional[Union[bytes, str]]:
        """
        Read file content by job_id and purpose.

        Determines whether to read as text or binary based on file extension.
        HTML files are read as text, PDF files as binary.

        Args:
            job_id: ID of the job.
            file_purpose: Purpose of the file.

        Returns:
            File content (str for text files, bytes for binary), or None if not found.

        Raises:
            FileNotFoundError: If the database record exists but file is missing.
        """
        logger.debug(f"Getting file content for job_id={job_id}, purpose={file_purpose}")
        
        job_file = self.file_repo.get_by_job_and_purpose(job_id, file_purpose)
        if not job_file:
            logger.debug(f"No file record found for job_id={job_id}, purpose={file_purpose}")
            return None

        file_path = Path(job_file.file_path)
        if not file_path.exists():
            logger.error(
                f"File inconsistency: record exists but file missing at {file_path}"
            )
            raise FileNotFoundError(
                f"File record exists but file missing: {file_path}"
            )

        # Determine read mode based on extension
        extension = file_path.suffix.lower()
        if extension in ('.html', '.htm', '.txt', '.css', '.js', '.json', '.xml'):
            content = file_path.read_text(encoding='utf-8')
            logger.debug(f"Read text file: {file_path} ({len(content)} chars)")
        else:
            content = file_path.read_bytes()
            logger.debug(f"Read binary file: {file_path} ({len(content)} bytes)")

        return content

    def delete_file(self, job_id: int, file_purpose: str) -> bool:
        """
        Delete a file from disk and database.

        Removes both the filesystem file and the database record.
        If the file doesn't exist on disk but the record exists,
        still deletes the record.

        Args:
            job_id: ID of the job.
            file_purpose: Purpose of the file.

        Returns:
            True if the file was deleted, False if no record found.
        """
        logger.info(f"Deleting file for job_id={job_id}, purpose={file_purpose}")
        
        job_file = self.file_repo.get_by_job_and_purpose(job_id, file_purpose)
        if not job_file:
            logger.debug(f"No file record found for job_id={job_id}, purpose={file_purpose}")
            return False

        file_path = Path(job_file.file_path)

        # Delete database record first
        deleted = self.file_repo.delete(job_file.id)
        if deleted:
            logger.debug(f"Database record deleted: id={job_file.id}")
        
        # Delete file from disk
        if file_path.exists():
            try:
                file_path.unlink()
                logger.debug(f"File deleted from disk: {file_path}")
            except OSError as e:
                # Log warning but don't fail - record is already deleted
                logger.warning(f"Failed to delete file from disk {file_path}: {e}")
        else:
            logger.debug(f"File not found on disk (already deleted?): {file_path}")

        logger.info(f"File deletion complete for job_id={job_id}, purpose={file_purpose}")
        return True

    def get_files_for_job(self, job_id: int) -> list[JobFile]:
        """
        Get all file records for a job.

        Args:
            job_id: ID of the job.

        Returns:
            List of JobFile records for the job.
        """
        logger.debug(f"Getting all files for job_id={job_id}")
        
        files = self.file_repo.get_by_job_id(job_id)
        logger.debug(f"Found {len(files)} files for job_id={job_id}")
        return files

    # =========================================================================
    # PRIVATE METHODS
    # =========================================================================

    def _generate_partition_path(self) -> Path:
        """
        Generate YYYYMM partition folder path.

        Creates a path based on the current year and month.

        Returns:
            Path object for the partition folder (e.g., Path("202601")).
        """
        now = datetime.now()
        partition = now.strftime("%Y%m")
        return Path(partition)

    def _generate_unique_filename(
        self,
        job_id: int,
        purpose: str,
        extension: str
    ) -> str:
        """
        Generate a unique filename.

        Creates a filename following the pattern: {job_id}_{purpose}_{uuid8}.{ext}

        Args:
            job_id: ID of the job.
            purpose: Purpose of the file.
            extension: File extension without dot.

        Returns:
            Unique filename string.
        """
        # Generate 8-character UUID suffix for uniqueness
        uuid_suffix = uuid.uuid4().hex[:8]
        
        # Clean the extension (remove leading dot if present)
        ext = extension.lstrip('.')
        
        filename = f"{job_id}_{purpose}_{uuid_suffix}.{ext}"
        return filename
