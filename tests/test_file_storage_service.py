"""
Unit tests for FileStorageService.

Feature: database-centric-file-management
"""

import sqlite3
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from src.db.models import JobFile
from src.db.schema import create_schema
from src.repositories.job_file_repository import JobFileRepository
from src.services.file_storage_service import FileStorageService


# =============================================================================
# TEST HELPERS
# =============================================================================

@contextmanager
def temp_test_db():
    """
    Create a temporary test database with schema.
    
    Yields a connection that is cleaned up after use.
    """
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = Path(f.name)
    
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    create_schema(conn)
    
    try:
        yield conn
    finally:
        conn.close()
        db_path.unlink(missing_ok=True)


@contextmanager
def temp_file_storage():
    """
    Create a temporary directory for file storage.
    
    Yields the path that is cleaned up after use.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def create_job(conn: sqlite3.Connection, folder_name: str) -> int:
    """Helper to create a job record and return its ID."""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO jobs (folder_name, company, title, phase)
        VALUES (?, ?, ?, ?)
        """,
        (folder_name, "TestCorp", "Engineer", "1_Queued")
    )
    conn.commit()
    job_id = cursor.lastrowid
    cursor.close()
    return job_id


# =============================================================================
# UNIT TESTS
# =============================================================================

class TestFileStorageServiceInit:
    """Tests for FileStorageService initialization."""

    def test_default_base_path(self):
        """Service should use src/files as default base path."""
        service = FileStorageService()
        assert service.base_path == Path("src/files")

    def test_custom_base_path(self):
        """Service should accept custom base path."""
        custom_path = Path("/custom/path")
        service = FileStorageService(base_path=custom_path)
        assert service.base_path == custom_path

    def test_has_file_repository(self):
        """Service should have a JobFileRepository instance."""
        service = FileStorageService()
        assert isinstance(service.file_repo, JobFileRepository)


class TestGeneratePartitionPath:
    """Tests for _generate_partition_path method."""

    def test_returns_path_object(self):
        """Should return a Path object."""
        service = FileStorageService()
        result = service._generate_partition_path()
        assert isinstance(result, Path)

    def test_format_yyyymm(self):
        """Should return path in YYYYMM format."""
        service = FileStorageService()
        result = service._generate_partition_path()
        # Should be 6 characters: YYYYMM
        assert len(str(result)) == 6
        # Should be all digits
        assert str(result).isdigit()

    @patch('src.services.file_storage_service.datetime')
    def test_uses_current_date(self, mock_datetime):
        """Should use current date for partition."""
        mock_datetime.now.return_value = datetime(2026, 3, 15)
        service = FileStorageService()
        result = service._generate_partition_path()
        assert str(result) == "202603"


class TestGenerateUniqueFilename:
    """Tests for _generate_unique_filename method."""

    def test_includes_job_id(self):
        """Filename should include job_id."""
        service = FileStorageService()
        filename = service._generate_unique_filename(42, "resume_html", "html")
        assert filename.startswith("42_")

    def test_includes_purpose(self):
        """Filename should include purpose."""
        service = FileStorageService()
        filename = service._generate_unique_filename(42, "resume_html", "html")
        assert "_resume_html_" in filename

    def test_includes_extension(self):
        """Filename should include extension."""
        service = FileStorageService()
        filename = service._generate_unique_filename(42, "resume_html", "html")
        assert filename.endswith(".html")

    def test_handles_extension_with_dot(self):
        """Should handle extension with leading dot."""
        service = FileStorageService()
        filename = service._generate_unique_filename(42, "resume_pdf", ".pdf")
        assert filename.endswith(".pdf")
        assert ".." not in filename

    def test_unique_filenames(self):
        """Should generate unique filenames for same inputs."""
        service = FileStorageService()
        filenames = set()
        for _ in range(100):
            filename = service._generate_unique_filename(42, "resume_html", "html")
            filenames.add(filename)
        # All 100 filenames should be unique
        assert len(filenames) == 100

    def test_filename_pattern(self):
        """Filename should match pattern {job_id}_{purpose}_{uuid8}.{ext}."""
        service = FileStorageService()
        filename = service._generate_unique_filename(123, "coverletter_pdf", "pdf")
        parts = filename.split("_")
        assert parts[0] == "123"
        assert parts[1] == "coverletter"
        assert parts[2] == "pdf"
        # Last part should be uuid8.ext
        last_part = parts[3]
        uuid_part, ext = last_part.rsplit(".", 1)
        assert len(uuid_part) == 8
        assert ext == "pdf"


class TestStoreFile:
    """Tests for store_file method."""

    def test_stores_text_content(self):
        """Should store text content to disk."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test1")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            content = "<html><body>Test Resume</body></html>"
            result = service.store_file(
                job_id=job_id,
                content=content,
                file_purpose="resume_html",
                file_source="generated",
                extension="html"
            )
            
            # Verify file was created
            file_path = Path(result.file_path)
            assert file_path.exists()
            assert file_path.read_text() == content

    def test_stores_binary_content(self):
        """Should store binary content to disk."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test2")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            content = b"%PDF-1.4 binary content here"
            result = service.store_file(
                job_id=job_id,
                content=content,
                file_purpose="resume_pdf",
                file_source="generated",
                extension="pdf"
            )
            
            # Verify file was created
            file_path = Path(result.file_path)
            assert file_path.exists()
            assert file_path.read_bytes() == content

    def test_creates_partition_folder(self):
        """Should create partition folder if it doesn't exist."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test3")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            result = service.store_file(
                job_id=job_id,
                content="test",
                file_purpose="resume_html",
                file_source="generated",
                extension="html"
            )
            
            # Verify partition folder was created
            file_path = Path(result.file_path)
            partition_folder = file_path.parent
            assert partition_folder.exists()
            assert partition_folder.is_dir()

    def test_creates_database_record(self):
        """Should create database record for stored file."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test4")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            result = service.store_file(
                job_id=job_id,
                content="test content",
                file_purpose="resume_html",
                file_source="generated",
                extension="html"
            )
            
            # Verify database record was created
            assert result.id is not None
            assert result.job_id == job_id
            assert result.file_purpose == "resume_html"
            assert result.file_source == "generated"
            
            # Verify we can retrieve it
            retrieved = service.file_repo.get_by_job_and_purpose(job_id, "resume_html")
            assert retrieved is not None
            assert retrieved.id == result.id

    def test_returns_job_file(self):
        """Should return JobFile with all fields populated."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test5")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            result = service.store_file(
                job_id=job_id,
                content="test",
                file_purpose="coverletter_html",
                file_source="generated",
                extension="html"
            )
            
            assert isinstance(result, JobFile)
            assert result.id is not None
            assert result.job_id == job_id
            assert result.filename is not None
            assert result.file_path is not None
            assert result.file_purpose == "coverletter_html"
            assert result.file_source == "generated"


class TestGetFilePath:
    """Tests for get_file_path method."""

    def test_returns_path_for_existing_file(self):
        """Should return path for existing file."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test6")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            stored = service.store_file(
                job_id=job_id,
                content="test",
                file_purpose="resume_html",
                file_source="generated",
                extension="html"
            )
            
            result = service.get_file_path(job_id, "resume_html")
            assert result is not None
            assert isinstance(result, Path)
            assert str(result) == stored.file_path

    def test_returns_none_for_nonexistent_file(self):
        """Should return None for non-existent file."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test7")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            result = service.get_file_path(job_id, "resume_html")
            assert result is None


class TestGetFileContent:
    """Tests for get_file_content method."""

    def test_returns_text_content(self):
        """Should return text content for HTML files."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test8")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            original_content = "<html><body>Test</body></html>"
            service.store_file(
                job_id=job_id,
                content=original_content,
                file_purpose="resume_html",
                file_source="generated",
                extension="html"
            )
            
            result = service.get_file_content(job_id, "resume_html")
            assert result == original_content
            assert isinstance(result, str)

    def test_returns_binary_content(self):
        """Should return binary content for PDF files."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test9")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            original_content = b"%PDF-1.4 binary content"
            service.store_file(
                job_id=job_id,
                content=original_content,
                file_purpose="resume_pdf",
                file_source="generated",
                extension="pdf"
            )
            
            result = service.get_file_content(job_id, "resume_pdf")
            assert result == original_content
            assert isinstance(result, bytes)

    def test_returns_none_for_nonexistent_record(self):
        """Should return None when no database record exists."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test10")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            result = service.get_file_content(job_id, "resume_html")
            assert result is None

    def test_raises_for_missing_file(self):
        """Should raise FileNotFoundError when record exists but file is missing."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test11")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            # Store a file
            stored = service.store_file(
                job_id=job_id,
                content="test",
                file_purpose="resume_html",
                file_source="generated",
                extension="html"
            )
            
            # Delete the file from disk but keep the record
            Path(stored.file_path).unlink()
            
            # Should raise FileNotFoundError
            with pytest.raises(FileNotFoundError):
                service.get_file_content(job_id, "resume_html")


class TestDeleteFile:
    """Tests for delete_file method."""

    def test_deletes_file_and_record(self):
        """Should delete both file and database record."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test12")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            stored = service.store_file(
                job_id=job_id,
                content="test",
                file_purpose="resume_html",
                file_source="generated",
                extension="html"
            )
            
            file_path = Path(stored.file_path)
            assert file_path.exists()
            
            result = service.delete_file(job_id, "resume_html")
            
            assert result is True
            assert not file_path.exists()
            assert service.file_repo.get_by_job_and_purpose(job_id, "resume_html") is None

    def test_returns_false_for_nonexistent(self):
        """Should return False when no record exists."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test13")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            result = service.delete_file(job_id, "resume_html")
            assert result is False

    def test_deletes_record_even_if_file_missing(self):
        """Should delete record even if file is already missing from disk."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test14")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            stored = service.store_file(
                job_id=job_id,
                content="test",
                file_purpose="resume_html",
                file_source="generated",
                extension="html"
            )
            
            # Delete file from disk manually
            Path(stored.file_path).unlink()
            
            # delete_file should still succeed
            result = service.delete_file(job_id, "resume_html")
            
            assert result is True
            assert service.file_repo.get_by_job_and_purpose(job_id, "resume_html") is None


class TestGetFilesForJob:
    """Tests for get_files_for_job method."""

    def test_returns_all_files_for_job(self):
        """Should return all files for a job."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test15")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            # Store multiple files
            service.store_file(job_id, "html1", "resume_html", "generated", "html")
            service.store_file(job_id, b"pdf1", "resume_pdf", "generated", "pdf")
            service.store_file(job_id, "html2", "coverletter_html", "generated", "html")
            
            result = service.get_files_for_job(job_id)
            
            assert len(result) == 3
            purposes = {f.file_purpose for f in result}
            assert purposes == {"resume_html", "resume_pdf", "coverletter_html"}

    def test_returns_empty_list_for_no_files(self):
        """Should return empty list when job has no files."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test16")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            result = service.get_files_for_job(job_id)
            
            assert result == []

    def test_returns_job_file_objects(self):
        """Should return list of JobFile objects."""
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.test17")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            service.store_file(job_id, "test", "resume_html", "generated", "html")
            
            result = service.get_files_for_job(job_id)
            
            assert len(result) == 1
            assert isinstance(result[0], JobFile)


# =============================================================================
# FAILURE HANDLING AND ROLLBACK TESTS
# Validates: Requirements 7.4, 7.5
# =============================================================================

class TestFileWriteFailureHandling:
    """
    Tests for failure handling when file write fails.
    
    Validates: Requirement 7.4
    IF a file write fails, THEN THE File_Storage_Service SHALL NOT create a database record.
    """

    def test_no_database_record_on_file_write_failure(self):
        """
        Should NOT create database record when file write fails.
        
        Validates: Requirement 7.4
        """
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.fail1")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            # Make the partition path read-only to cause write failure
            partition_path = storage_path / service._generate_partition_path()
            partition_path.mkdir(parents=True, exist_ok=True)
            partition_path.chmod(0o444)  # Read-only
            
            try:
                with pytest.raises(OSError):
                    service.store_file(
                        job_id=job_id,
                        content="test content",
                        file_purpose="resume_html",
                        file_source="generated",
                        extension="html"
                    )
                
                # Verify no database record was created
                record = service.file_repo.get_by_job_and_purpose(job_id, "resume_html")
                assert record is None
            finally:
                # Restore permissions for cleanup
                partition_path.chmod(0o755)

    def test_no_orphan_files_on_write_failure(self):
        """
        Should not leave orphan files when write fails.
        
        Validates: Requirement 7.4
        """
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.fail2")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            # Make the partition path read-only to cause write failure
            partition_path = storage_path / service._generate_partition_path()
            partition_path.mkdir(parents=True, exist_ok=True)
            partition_path.chmod(0o444)  # Read-only
            
            try:
                with pytest.raises(OSError):
                    service.store_file(
                        job_id=job_id,
                        content="test content",
                        file_purpose="resume_html",
                        file_source="generated",
                        extension="html"
                    )
                
                # Verify no files were created in the partition
                files_in_partition = list(partition_path.glob("*"))
                assert len(files_in_partition) == 0
            finally:
                # Restore permissions for cleanup
                partition_path.chmod(0o755)

    def test_raises_oserror_on_file_write_failure(self):
        """
        Should raise OSError when file write fails.
        
        Validates: Requirement 7.4
        """
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.fail3")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            # Mock the file write to fail
            with patch.object(Path, 'write_text', side_effect=OSError("Disk full")):
                with pytest.raises(OSError) as exc_info:
                    service.store_file(
                        job_id=job_id,
                        content="test content",
                        file_purpose="resume_html",
                        file_source="generated",
                        extension="html"
                    )
                
                assert "Disk full" in str(exc_info.value)


class TestDatabaseInsertFailureHandling:
    """
    Tests for failure handling when database insert fails after file write.
    
    Validates: Requirement 7.5
    IF a database record creation fails after file write, THEN THE File_Storage_Service 
    SHALL delete the written file to maintain consistency.
    """

    def test_file_cleanup_on_database_failure(self):
        """
        Should delete written file when database insert fails.
        
        Validates: Requirement 7.5
        """
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.fail4")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            # Track the file path that would be created
            partition_path = storage_path / service._generate_partition_path()
            
            # Mock the repository create to fail after file is written
            original_create = service.file_repo.create
            def failing_create(job_file):
                raise sqlite3.IntegrityError("Simulated database failure")
            
            service.file_repo.create = failing_create
            
            with pytest.raises(sqlite3.IntegrityError):
                service.store_file(
                    job_id=job_id,
                    content="test content",
                    file_purpose="resume_html",
                    file_source="generated",
                    extension="html"
                )
            
            # Verify no files remain in the partition folder
            if partition_path.exists():
                files_in_partition = list(partition_path.glob("*"))
                assert len(files_in_partition) == 0, \
                    f"Orphan files found: {files_in_partition}"

    def test_no_orphan_database_records_on_failure(self):
        """
        Should not leave orphan database records when insert fails.
        
        Validates: Requirement 7.5
        """
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.fail5")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            # Mock the repository create to fail
            def failing_create(job_file):
                raise sqlite3.IntegrityError("Simulated database failure")
            
            service.file_repo.create = failing_create
            
            with pytest.raises(sqlite3.IntegrityError):
                service.store_file(
                    job_id=job_id,
                    content="test content",
                    file_purpose="resume_html",
                    file_source="generated",
                    extension="html"
                )
            
            # Verify no database record exists
            record = service.file_repo.get_by_job_and_purpose(job_id, "resume_html")
            assert record is None

    def test_raises_original_exception_after_cleanup(self):
        """
        Should re-raise the original database exception after cleanup.
        
        Validates: Requirement 7.5
        """
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.fail6")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            # Mock the repository create to fail with specific error
            def failing_create(job_file):
                raise sqlite3.IntegrityError("UNIQUE constraint failed")
            
            service.file_repo.create = failing_create
            
            with pytest.raises(sqlite3.IntegrityError) as exc_info:
                service.store_file(
                    job_id=job_id,
                    content="test content",
                    file_purpose="resume_html",
                    file_source="generated",
                    extension="html"
                )
            
            assert "UNIQUE constraint failed" in str(exc_info.value)

    def test_cleanup_handles_already_deleted_file(self):
        """
        Should handle case where file is already deleted during cleanup.
        
        Validates: Requirement 7.5
        """
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.fail7")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            file_written = []
            
            # Mock to track file path and fail on create
            original_create = service.file_repo.create
            def failing_create_with_file_delete(job_file):
                # Delete the file before the cleanup runs
                file_path = Path(job_file.file_path)
                if file_path.exists():
                    file_path.unlink()
                    file_written.append(str(file_path))
                raise sqlite3.IntegrityError("Simulated failure")
            
            service.file_repo.create = failing_create_with_file_delete
            
            # Should not raise during cleanup even if file is already gone
            with pytest.raises(sqlite3.IntegrityError):
                service.store_file(
                    job_id=job_id,
                    content="test content",
                    file_purpose="resume_html",
                    file_source="generated",
                    extension="html"
                )
            
            # Verify the file was written and then deleted
            assert len(file_written) == 1


class TestConsistencyOnFailure:
    """
    Tests for overall consistency when failures occur.
    
    Validates: Requirements 7.4, 7.5
    For any failed store operation, there shall be no orphan files on disk 
    without database records AND no orphan database records without files on disk.
    """

    def test_consistency_after_file_write_failure(self):
        """
        Should maintain consistency (no orphans) after file write failure.
        
        Validates: Requirements 7.4, 7.5
        """
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.cons1")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            # Mock file write to fail
            with patch.object(Path, 'write_text', side_effect=OSError("Write failed")):
                with pytest.raises(OSError):
                    service.store_file(
                        job_id=job_id,
                        content="test content",
                        file_purpose="resume_html",
                        file_source="generated",
                        extension="html"
                    )
            
            # Verify consistency: no database record
            record = service.file_repo.get_by_job_and_purpose(job_id, "resume_html")
            assert record is None
            
            # Verify consistency: no orphan files
            partition_path = storage_path / service._generate_partition_path()
            if partition_path.exists():
                files = list(partition_path.glob("*"))
                assert len(files) == 0

    def test_consistency_after_database_insert_failure(self):
        """
        Should maintain consistency (no orphans) after database insert failure.
        
        Validates: Requirements 7.4, 7.5
        """
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.cons2")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            # Mock database insert to fail
            def failing_create(job_file):
                raise sqlite3.IntegrityError("Insert failed")
            
            service.file_repo.create = failing_create
            
            with pytest.raises(sqlite3.IntegrityError):
                service.store_file(
                    job_id=job_id,
                    content="test content",
                    file_purpose="resume_html",
                    file_source="generated",
                    extension="html"
                )
            
            # Verify consistency: no database record
            record = service.file_repo.get_by_job_and_purpose(job_id, "resume_html")
            assert record is None
            
            # Verify consistency: no orphan files
            partition_path = storage_path / service._generate_partition_path()
            if partition_path.exists():
                files = list(partition_path.glob("*"))
                assert len(files) == 0

    def test_successful_store_maintains_consistency(self):
        """
        Should maintain consistency on successful store (both file and record exist).
        
        Validates: Requirements 7.4, 7.5
        """
        with temp_test_db() as conn, temp_file_storage() as storage_path:
            job_id = create_job(conn, "TestCorp.Engineer.20260115.cons3")
            
            service = FileStorageService(base_path=storage_path)
            service.file_repo = JobFileRepository(conn=conn)
            
            result = service.store_file(
                job_id=job_id,
                content="test content",
                file_purpose="resume_html",
                file_source="generated",
                extension="html"
            )
            
            # Verify consistency: database record exists
            record = service.file_repo.get_by_job_and_purpose(job_id, "resume_html")
            assert record is not None
            assert record.id == result.id
            
            # Verify consistency: file exists at recorded path
            file_path = Path(result.file_path)
            assert file_path.exists()
            assert file_path.read_text() == "test content"


# =============================================================================
# PROPERTY-BASED TESTS
# =============================================================================

import re
from hypothesis import given, settings, strategies as st


# Valid file purposes as defined in the design document
FILE_PURPOSES = [
    "job_posting_html",
    "resume_html",
    "resume_pdf",
    "coverletter_html",
    "coverletter_pdf",
]

# Valid file sources as defined in the design document
FILE_SOURCES = [
    "url_fetch",
    "generated",
]


@st.composite
def file_storage_data(draw):
    """
    Generate random valid data for file storage operations.
    
    Returns a dictionary with all required fields for storing a file.
    
    Note: For text content, we exclude lone carriage returns (\r) because
    Python's text mode file operations normalize line endings in a
    platform-specific way. This is expected behavior for text files.
    We use an alphabet that includes common text characters and newlines (\n)
    but excludes \r to ensure consistent behavior across platforms.
    """
    file_purpose = draw(st.sampled_from(FILE_PURPOSES))
    file_source = draw(st.sampled_from(FILE_SOURCES))
    
    # Determine extension based on purpose
    if file_purpose.endswith("_pdf"):
        extension = "pdf"
        # Generate binary content for PDF
        content = draw(st.binary(min_size=1, max_size=1000))
    else:
        extension = "html"
        # Generate text content for HTML
        # Exclude \r (carriage return) to avoid platform-specific line ending
        # normalization issues. Use printable characters plus newline and tab.
        text_alphabet = st.characters(
            whitelist_categories=('L', 'N', 'P', 'S', 'Zs'),  # Letters, Numbers, Punctuation, Symbols, Space separators
            whitelist_characters='\n\t',  # Allow newline and tab
            blacklist_characters='\r'  # Exclude carriage return
        )
        content = draw(st.text(alphabet=text_alphabet, min_size=1, max_size=1000))
    
    return {
        "content": content,
        "file_purpose": file_purpose,
        "file_source": file_source,
        "extension": extension,
    }


@given(file_data=file_storage_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 3: File Storage Location Invariant")
def test_file_storage_location_invariant(file_data):
    """
    Property 3: File Storage Location Invariant
    
    For any file stored via FileStorageService, the file_path shall match the
    pattern `src/files/YYYYMM/{filename}` where YYYYMM corresponds to the
    current year and month at storage time.
    
    This test verifies:
    1. Files are stored in the base_path directory
    2. Files are in YYYYMM partition folders
    3. The partition folder matches the current date
    4. No per-job folders are created
    
    **Validates: Requirements 2.1, 2.2, 2.5**
    """
    with temp_test_db() as conn, temp_file_storage() as storage_path:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.loc{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create service with test storage path
        service = FileStorageService(base_path=storage_path)
        service.file_repo = JobFileRepository(conn=conn)
        
        # Get the expected partition (YYYYMM) at storage time
        expected_partition = datetime.now().strftime("%Y%m")
        
        # Store the file
        result = service.store_file(
            job_id=job_id,
            content=file_data["content"],
            file_purpose=file_data["file_purpose"],
            file_source=file_data["file_source"],
            extension=file_data["extension"]
        )
        
        # Verify the file_path is not None
        assert result.file_path is not None, "file_path should not be None"
        
        file_path = Path(result.file_path)
        
        # 1. Verify files are stored in the base_path directory
        # The file_path should start with the base_path
        assert str(file_path).startswith(str(storage_path)), \
            f"File path {file_path} should start with base_path {storage_path}"
        
        # 2. Verify files are in YYYYMM partition folders
        # The path structure should be: base_path/YYYYMM/filename
        relative_path = file_path.relative_to(storage_path)
        path_parts = relative_path.parts
        
        assert len(path_parts) == 2, \
            f"Path should have exactly 2 parts (partition/filename), got {len(path_parts)}: {path_parts}"
        
        partition_folder = path_parts[0]
        filename = path_parts[1]
        
        # Verify partition folder matches YYYYMM pattern (6 digits)
        yyyymm_pattern = re.compile(r"^\d{6}$")
        assert yyyymm_pattern.match(partition_folder), \
            f"Partition folder '{partition_folder}' should match YYYYMM pattern (6 digits)"
        
        # 3. Verify the partition folder matches the current date
        # Note: There's a small chance of test flakiness if the test runs exactly at month boundary
        # We accept the partition being the expected one
        assert partition_folder == expected_partition, \
            f"Partition folder '{partition_folder}' should match current date '{expected_partition}'"
        
        # 4. Verify no per-job folders are created
        # The path should be base_path/YYYYMM/filename, not base_path/YYYYMM/job_id/filename
        # or base_path/job_id/YYYYMM/filename
        assert len(path_parts) == 2, \
            f"No per-job folders should exist. Path parts: {path_parts}"
        
        # Additional verification: the file should actually exist at the path
        assert file_path.exists(), \
            f"File should exist at path {file_path}"
        
        # Verify the filename follows the expected pattern: {job_id}_{purpose}_{uuid8}.{ext}
        filename_pattern = re.compile(
            rf"^{job_id}_{file_data['file_purpose']}_[a-f0-9]{{8}}\.{file_data['extension']}$"
        )
        assert filename_pattern.match(filename), \
            f"Filename '{filename}' should match pattern {{job_id}}_{{purpose}}_{{uuid8}}.{{ext}}"
        
        # Verify the database record has the correct path
        db_record = service.file_repo.get_by_job_and_purpose(job_id, file_data["file_purpose"])
        assert db_record is not None, "Database record should exist"
        assert db_record.file_path == str(file_path), \
            f"Database file_path '{db_record.file_path}' should match actual path '{file_path}'"


@st.composite
def filename_generation_inputs(draw):
    """
    Generate random valid inputs for _generate_unique_filename method.
    
    Returns a dictionary with job_id, purpose, and extension.
    """
    job_id = draw(st.integers(min_value=1, max_value=1000000))
    purpose = draw(st.sampled_from(FILE_PURPOSES))
    
    # Determine extension based on purpose
    if purpose.endswith("_pdf"):
        extension = draw(st.sampled_from(["pdf", ".pdf"]))
    else:
        extension = draw(st.sampled_from(["html", ".html"]))
    
    return {
        "job_id": job_id,
        "purpose": purpose,
        "extension": extension,
    }


@given(inputs=filename_generation_inputs())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 4: Unique Filename Generation")
def test_unique_filename_generation_property(inputs):
    """
    Property 4: Unique Filename Generation
    
    For any two files stored via FileStorageService (even with the same job_id
    and purpose at different times), the generated filenames shall be different.
    
    This test verifies:
    1. Multiple calls to _generate_unique_filename() with the same inputs produce different filenames
    2. Filenames are unique even for the same job_id and purpose
    
    **Validates: Requirements 2.3**
    """
    service = FileStorageService()
    
    job_id = inputs["job_id"]
    purpose = inputs["purpose"]
    extension = inputs["extension"]
    
    # Generate multiple filenames with the same inputs
    # Using 10 iterations per test case to verify uniqueness
    generated_filenames = set()
    num_iterations = 10
    
    for _ in range(num_iterations):
        filename = service._generate_unique_filename(job_id, purpose, extension)
        generated_filenames.add(filename)
    
    # All generated filenames should be unique
    assert len(generated_filenames) == num_iterations, \
        f"Expected {num_iterations} unique filenames, but got {len(generated_filenames)}. " \
        f"Duplicate filenames detected for job_id={job_id}, purpose={purpose}, extension={extension}"


@given(
    job_id=st.integers(min_value=1, max_value=1000000),
    purpose=st.sampled_from(FILE_PURPOSES)
)
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 4: Unique Filename Generation")
def test_unique_filename_across_multiple_calls(job_id, purpose):
    """
    Property 4: Unique Filename Generation (Extended)
    
    For any two files stored via FileStorageService (even with the same job_id
    and purpose at different times), the generated filenames shall be different.
    
    This test specifically verifies that even with identical inputs (same job_id
    and purpose), each call produces a unique filename.
    
    **Validates: Requirements 2.3**
    """
    service = FileStorageService()
    
    # Determine extension based on purpose
    extension = "pdf" if purpose.endswith("_pdf") else "html"
    
    # Generate a larger set of filenames to increase confidence in uniqueness
    num_filenames = 50
    generated_filenames = []
    
    for _ in range(num_filenames):
        filename = service._generate_unique_filename(job_id, purpose, extension)
        generated_filenames.append(filename)
    
    # Convert to set to check for duplicates
    unique_filenames = set(generated_filenames)
    
    # All filenames should be unique
    assert len(unique_filenames) == num_filenames, \
        f"Expected {num_filenames} unique filenames, but got {len(unique_filenames)}. " \
        f"Duplicates found for job_id={job_id}, purpose={purpose}"
    
    # Verify each filename follows the expected pattern
    expected_ext = extension.lstrip('.')
    for filename in generated_filenames:
        # Filename should start with job_id
        assert filename.startswith(f"{job_id}_"), \
            f"Filename '{filename}' should start with '{job_id}_'"
        
        # Filename should contain the purpose
        assert f"_{purpose}_" in filename, \
            f"Filename '{filename}' should contain '_{purpose}_'"
        
        # Filename should end with the correct extension
        assert filename.endswith(f".{expected_ext}"), \
            f"Filename '{filename}' should end with '.{expected_ext}'"


@given(file_data=file_storage_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 4: Unique Filename Generation")
def test_unique_filename_in_storage_context(file_data):
    """
    Property 4: Unique Filename Generation (Storage Context)
    
    For any two files stored via FileStorageService (even with the same job_id
    and purpose at different times), the generated filenames shall be different.
    
    This test verifies uniqueness in the context of actual file storage operations,
    ensuring that when files are stored with the same job_id and purpose (after
    deleting the previous one), they get unique filenames.
    
    **Validates: Requirements 2.3**
    """
    with temp_test_db() as conn, temp_file_storage() as storage_path:
        # Create a job for testing
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.uniq{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        service = FileStorageService(base_path=storage_path)
        service.file_repo = JobFileRepository(conn=conn)
        
        stored_filenames = []
        num_iterations = 5
        
        for i in range(num_iterations):
            # Store a file
            result = service.store_file(
                job_id=job_id,
                content=file_data["content"],
                file_purpose=file_data["file_purpose"],
                file_source=file_data["file_source"],
                extension=file_data["extension"]
            )
            
            stored_filenames.append(result.filename)
            
            # Delete the file to allow storing another with the same purpose
            # (due to unique constraint on job_id + file_purpose)
            service.delete_file(job_id, file_data["file_purpose"])
        
        # All stored filenames should be unique
        unique_filenames = set(stored_filenames)
        assert len(unique_filenames) == num_iterations, \
            f"Expected {num_iterations} unique filenames, but got {len(unique_filenames)}. " \
            f"Duplicates: {[f for f in stored_filenames if stored_filenames.count(f) > 1]}"


@given(file_data=file_storage_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 7: Atomic Store Operation")
def test_atomic_store_operation(file_data):
    """
    Property 7: Atomic Store Operation
    
    For any successful call to FileStorageService.store_file(), both the file
    shall exist on disk at the returned path AND a corresponding record shall
    exist in the Job_Files_Table.
    
    This test verifies:
    1. After store_file() succeeds, the file exists on disk
    2. After store_file() succeeds, a database record exists
    3. The database record's file_path matches the actual file location
    
    **Validates: Requirements 7.1**
    """
    with temp_test_db() as conn, temp_file_storage() as storage_path:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.atomic{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create service with test storage path
        service = FileStorageService(base_path=storage_path)
        service.file_repo = JobFileRepository(conn=conn)
        
        # Store the file
        result = service.store_file(
            job_id=job_id,
            content=file_data["content"],
            file_purpose=file_data["file_purpose"],
            file_source=file_data["file_source"],
            extension=file_data["extension"]
        )
        
        # 1. Verify the file exists on disk at the returned path
        file_path = Path(result.file_path)
        assert file_path.exists(), \
            f"File should exist on disk at path {file_path} after successful store_file()"
        
        # Verify the file content matches what was stored
        if isinstance(file_data["content"], bytes):
            actual_content = file_path.read_bytes()
        else:
            actual_content = file_path.read_text()
        
        assert actual_content == file_data["content"], \
            "File content on disk should match the content that was stored"
        
        # 2. Verify a database record exists
        db_record = service.file_repo.get_by_job_and_purpose(job_id, file_data["file_purpose"])
        assert db_record is not None, \
            f"Database record should exist for job_id={job_id}, file_purpose={file_data['file_purpose']} " \
            "after successful store_file()"
        
        # 3. Verify the database record's file_path matches the actual file location
        assert db_record.file_path == str(file_path), \
            f"Database record file_path '{db_record.file_path}' should match " \
            f"actual file location '{file_path}'"
        
        # Additional verifications for completeness
        assert db_record.job_id == job_id, \
            f"Database record job_id should be {job_id}, got {db_record.job_id}"
        
        assert db_record.file_purpose == file_data["file_purpose"], \
            f"Database record file_purpose should be '{file_data['file_purpose']}', " \
            f"got '{db_record.file_purpose}'"
        
        assert db_record.file_source == file_data["file_source"], \
            f"Database record file_source should be '{file_data['file_source']}', " \
            f"got '{db_record.file_source}'"
        
        assert db_record.filename == file_path.name, \
            f"Database record filename '{db_record.filename}' should match " \
            f"actual filename '{file_path.name}'"
        
        # Verify the returned JobFile object matches the database record
        assert result.id == db_record.id, \
            f"Returned JobFile id {result.id} should match database record id {db_record.id}"
        
        assert result.job_id == db_record.job_id, \
            f"Returned JobFile job_id should match database record"
        
        assert result.filename == db_record.filename, \
            f"Returned JobFile filename should match database record"
        
        assert result.file_path == db_record.file_path, \
            f"Returned JobFile file_path should match database record"


@given(file_data=file_storage_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 8: Atomic Delete Operation")
def test_atomic_delete_operation(file_data):
    """
    Property 8: Atomic Delete Operation
    
    For any successful call to FileStorageService.delete_file(), neither the file
    shall exist on disk NOR shall a corresponding record exist in the Job_Files_Table.
    
    This test verifies:
    1. After delete_file() succeeds, the file no longer exists on disk
    2. After delete_file() succeeds, no database record exists for that job_id and file_purpose
    
    **Validates: Requirements 7.3**
    """
    with temp_test_db() as conn, temp_file_storage() as storage_path:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.delete{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create service with test storage path
        service = FileStorageService(base_path=storage_path)
        service.file_repo = JobFileRepository(conn=conn)
        
        # First, store a file so we have something to delete
        stored_result = service.store_file(
            job_id=job_id,
            content=file_data["content"],
            file_purpose=file_data["file_purpose"],
            file_source=file_data["file_source"],
            extension=file_data["extension"]
        )
        
        # Capture the file path before deletion
        file_path = Path(stored_result.file_path)
        
        # Verify the file and record exist before deletion
        assert file_path.exists(), \
            f"File should exist at {file_path} before deletion"
        
        pre_delete_record = service.file_repo.get_by_job_and_purpose(
            job_id, file_data["file_purpose"]
        )
        assert pre_delete_record is not None, \
            f"Database record should exist for job_id={job_id}, " \
            f"file_purpose={file_data['file_purpose']} before deletion"
        
        # Perform the delete operation
        delete_result = service.delete_file(job_id, file_data["file_purpose"])
        
        # Verify delete_file() returned True (success)
        assert delete_result is True, \
            f"delete_file() should return True for successful deletion"
        
        # 1. Verify the file no longer exists on disk
        assert not file_path.exists(), \
            f"File should NOT exist on disk at path {file_path} after successful delete_file()"
        
        # 2. Verify no database record exists for that job_id and file_purpose
        post_delete_record = service.file_repo.get_by_job_and_purpose(
            job_id, file_data["file_purpose"]
        )
        assert post_delete_record is None, \
            f"Database record should NOT exist for job_id={job_id}, " \
            f"file_purpose={file_data['file_purpose']} after successful delete_file()"
        
        # Additional verification: exists() should return False
        exists_result = service.file_repo.exists(job_id, file_data["file_purpose"])
        assert exists_result is False, \
            f"exists() should return False for job_id={job_id}, " \
            f"file_purpose={file_data['file_purpose']} after successful delete_file()"


@given(file_data=file_storage_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 8: Atomic Delete Operation")
def test_atomic_delete_with_missing_file_on_disk(file_data):
    """
    Property 8: Atomic Delete Operation (Edge Case - Missing File)
    
    For any successful call to FileStorageService.delete_file(), neither the file
    shall exist on disk NOR shall a corresponding record exist in the Job_Files_Table.
    
    This test verifies the property holds even when the file is already missing
    from disk (but the database record exists). The delete operation should still
    succeed and remove the database record.
    
    **Validates: Requirements 7.3**
    """
    with temp_test_db() as conn, temp_file_storage() as storage_path:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.delmiss{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create service with test storage path
        service = FileStorageService(base_path=storage_path)
        service.file_repo = JobFileRepository(conn=conn)
        
        # Store a file
        stored_result = service.store_file(
            job_id=job_id,
            content=file_data["content"],
            file_purpose=file_data["file_purpose"],
            file_source=file_data["file_source"],
            extension=file_data["extension"]
        )
        
        # Capture the file path
        file_path = Path(stored_result.file_path)
        
        # Manually delete the file from disk (simulating external deletion or corruption)
        file_path.unlink()
        
        # Verify file is gone but record still exists
        assert not file_path.exists(), \
            "File should be manually deleted from disk"
        
        pre_delete_record = service.file_repo.get_by_job_and_purpose(
            job_id, file_data["file_purpose"]
        )
        assert pre_delete_record is not None, \
            "Database record should still exist after manual file deletion"
        
        # Perform the delete operation
        delete_result = service.delete_file(job_id, file_data["file_purpose"])
        
        # Verify delete_file() returned True (success)
        assert delete_result is True, \
            "delete_file() should return True even when file is already missing from disk"
        
        # 1. Verify the file still doesn't exist on disk (was already gone)
        assert not file_path.exists(), \
            f"File should NOT exist on disk at path {file_path}"
        
        # 2. Verify no database record exists
        post_delete_record = service.file_repo.get_by_job_and_purpose(
            job_id, file_data["file_purpose"]
        )
        assert post_delete_record is None, \
            f"Database record should NOT exist for job_id={job_id}, " \
            f"file_purpose={file_data['file_purpose']} after delete_file()"


@given(
    file_data=file_storage_data(),
    num_files=st.integers(min_value=1, max_value=3)
)
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 8: Atomic Delete Operation")
def test_atomic_delete_does_not_affect_other_files(file_data, num_files):
    """
    Property 8: Atomic Delete Operation (Isolation)
    
    For any successful call to FileStorageService.delete_file(), neither the file
    shall exist on disk NOR shall a corresponding record exist in the Job_Files_Table.
    
    This test verifies that deleting one file does not affect other files for the
    same job. The atomic delete should only remove the specified file and record.
    
    **Validates: Requirements 7.3**
    """
    with temp_test_db() as conn, temp_file_storage() as storage_path:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.deliso{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create service with test storage path
        service = FileStorageService(base_path=storage_path)
        service.file_repo = JobFileRepository(conn=conn)
        
        # Store multiple files with different purposes
        # Select purposes that are different from the one we'll delete
        all_purposes = FILE_PURPOSES.copy()
        target_purpose = file_data["file_purpose"]
        other_purposes = [p for p in all_purposes if p != target_purpose][:num_files]
        
        # Store the target file (the one we'll delete)
        target_result = service.store_file(
            job_id=job_id,
            content=file_data["content"],
            file_purpose=target_purpose,
            file_source=file_data["file_source"],
            extension=file_data["extension"]
        )
        target_file_path = Path(target_result.file_path)
        
        # Store other files that should NOT be affected by the delete
        other_files = []
        for purpose in other_purposes:
            ext = "pdf" if purpose.endswith("_pdf") else "html"
            content = b"other content" if ext == "pdf" else "other content"
            result = service.store_file(
                job_id=job_id,
                content=content,
                file_purpose=purpose,
                file_source="generated",
                extension=ext
            )
            other_files.append({
                "purpose": purpose,
                "path": Path(result.file_path),
                "record_id": result.id
            })
        
        # Delete the target file
        delete_result = service.delete_file(job_id, target_purpose)
        
        # Verify target file was deleted
        assert delete_result is True, \
            "delete_file() should return True"
        assert not target_file_path.exists(), \
            f"Target file should NOT exist at {target_file_path}"
        assert service.file_repo.get_by_job_and_purpose(job_id, target_purpose) is None, \
            "Target database record should NOT exist"
        
        # Verify other files were NOT affected
        for other_file in other_files:
            # File should still exist on disk
            assert other_file["path"].exists(), \
                f"Other file at {other_file['path']} should still exist after deleting target"
            
            # Database record should still exist
            record = service.file_repo.get_by_job_and_purpose(job_id, other_file["purpose"])
            assert record is not None, \
                f"Database record for purpose '{other_file['purpose']}' should still exist"
            assert record.id == other_file["record_id"], \
                f"Database record ID should be unchanged"


# =============================================================================
# PROPERTY 9: CONSISTENCY ON FAILURE
# =============================================================================

@st.composite
def failure_scenario_data(draw):
    """
    Generate random valid data for failure scenario testing.
    
    Returns a dictionary with all required fields for storing a file,
    plus a failure type indicator.
    """
    file_purpose = draw(st.sampled_from(FILE_PURPOSES))
    file_source = draw(st.sampled_from(FILE_SOURCES))
    
    # Determine extension based on purpose
    if file_purpose.endswith("_pdf"):
        extension = "pdf"
        # Generate binary content for PDF
        content = draw(st.binary(min_size=1, max_size=500))
    else:
        extension = "html"
        # Generate text content for HTML
        content = draw(st.text(min_size=1, max_size=500, alphabet=st.characters(
            whitelist_categories=('L', 'N', 'P', 'S', 'Z'),
            blacklist_characters='\x00'
        )))
    
    # Choose failure type: 'file_write' or 'database_insert'
    failure_type = draw(st.sampled_from(["file_write", "database_insert"]))
    
    return {
        "content": content,
        "file_purpose": file_purpose,
        "file_source": file_source,
        "extension": extension,
        "failure_type": failure_type,
    }


@given(file_data=failure_scenario_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 9: Consistency on Failure")
def test_consistency_on_failure_property(file_data):
    """
    Property 9: Consistency on Failure
    
    For any failed store operation (either disk write or database insert fails),
    there shall be no orphan files on disk without database records AND no orphan
    database records without files on disk.
    
    This test verifies:
    1. If file write fails, no database record is created
    2. If database insert fails after file write, the file is cleaned up
    3. No orphan files or records exist after any failure
    
    **Validates: Requirements 7.4, 7.5**
    """
    with temp_test_db() as conn, temp_file_storage() as storage_path:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.fail{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create service with test storage path
        service = FileStorageService(base_path=storage_path)
        service.file_repo = JobFileRepository(conn=conn)
        
        # Get the partition path that would be used
        partition_path = storage_path / service._generate_partition_path()
        
        failure_type = file_data["failure_type"]
        
        if failure_type == "file_write":
            # Simulate file write failure by mocking write_text/write_bytes
            if isinstance(file_data["content"], bytes):
                with patch.object(Path, 'write_bytes', side_effect=OSError("Simulated disk failure")):
                    with pytest.raises(OSError):
                        service.store_file(
                            job_id=job_id,
                            content=file_data["content"],
                            file_purpose=file_data["file_purpose"],
                            file_source=file_data["file_source"],
                            extension=file_data["extension"]
                        )
            else:
                with patch.object(Path, 'write_text', side_effect=OSError("Simulated disk failure")):
                    with pytest.raises(OSError):
                        service.store_file(
                            job_id=job_id,
                            content=file_data["content"],
                            file_purpose=file_data["file_purpose"],
                            file_source=file_data["file_source"],
                            extension=file_data["extension"]
                        )
        
        elif failure_type == "database_insert":
            # Simulate database insert failure
            original_create = service.file_repo.create
            def failing_create(job_file):
                raise sqlite3.IntegrityError("Simulated database failure")
            
            service.file_repo.create = failing_create
            
            with pytest.raises(sqlite3.IntegrityError):
                service.store_file(
                    job_id=job_id,
                    content=file_data["content"],
                    file_purpose=file_data["file_purpose"],
                    file_source=file_data["file_source"],
                    extension=file_data["extension"]
                )
        
        # VERIFY CONSISTENCY: No orphan files on disk without database records
        # Check all files in the partition folder
        if partition_path.exists():
            files_on_disk = list(partition_path.glob("*"))
            for file_on_disk in files_on_disk:
                # For each file on disk, verify there's a corresponding database record
                # Extract job_id from filename pattern: {job_id}_{purpose}_{uuid8}.{ext}
                filename = file_on_disk.name
                parts = filename.split("_")
                if len(parts) >= 3:
                    try:
                        file_job_id = int(parts[0])
                        # Reconstruct purpose from parts (e.g., "resume_html" from ["resume", "html", "uuid.ext"])
                        # Purpose is everything between job_id and the uuid part
                        purpose_parts = parts[1:-1]
                        file_purpose = "_".join(purpose_parts)
                        
                        # Check if database record exists for this file
                        db_record = service.file_repo.get_by_job_and_purpose(file_job_id, file_purpose)
                        
                        # If no database record exists, this is an orphan file
                        assert db_record is not None, \
                            f"Orphan file found on disk without database record: {file_on_disk}"
                        
                        # If database record exists, verify the path matches
                        assert db_record.file_path == str(file_on_disk), \
                            f"Database record path '{db_record.file_path}' doesn't match file on disk '{file_on_disk}'"
                    except (ValueError, IndexError):
                        # If we can't parse the filename, it's not a file we created
                        pass
        
        # VERIFY CONSISTENCY: No orphan database records without files on disk
        # Check all database records for this job
        all_records = service.file_repo.get_by_job_id(job_id)
        for record in all_records:
            file_path = Path(record.file_path)
            assert file_path.exists(), \
                f"Orphan database record found without file on disk: " \
                f"job_id={record.job_id}, purpose={record.file_purpose}, path={record.file_path}"
        
        # VERIFY: Specifically for the file we tried to store, neither should exist
        # after a failure
        failed_record = service.file_repo.get_by_job_and_purpose(
            job_id, file_data["file_purpose"]
        )
        assert failed_record is None, \
            f"Database record should not exist after failed store operation: " \
            f"job_id={job_id}, purpose={file_data['file_purpose']}"


@given(file_data=file_storage_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 9: Consistency on Failure")
def test_no_orphan_files_on_file_write_failure(file_data):
    """
    Property 9: Consistency on Failure - File Write Failure Case
    
    For any failed store operation where disk write fails, there shall be no
    orphan files on disk without database records.
    
    This test specifically verifies:
    1. If file write fails, no database record is created
    2. No orphan files exist after file write failure
    
    **Validates: Requirements 7.4, 7.5**
    """
    with temp_test_db() as conn, temp_file_storage() as storage_path:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.fwf{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create service with test storage path
        service = FileStorageService(base_path=storage_path)
        service.file_repo = JobFileRepository(conn=conn)
        
        # Get the partition path
        partition_path = storage_path / service._generate_partition_path()
        
        # Count files before the operation
        files_before = set()
        if partition_path.exists():
            files_before = set(f.name for f in partition_path.glob("*"))
        
        # Simulate file write failure
        if isinstance(file_data["content"], bytes):
            with patch.object(Path, 'write_bytes', side_effect=OSError("Disk full")):
                with pytest.raises(OSError):
                    service.store_file(
                        job_id=job_id,
                        content=file_data["content"],
                        file_purpose=file_data["file_purpose"],
                        file_source=file_data["file_source"],
                        extension=file_data["extension"]
                    )
        else:
            with patch.object(Path, 'write_text', side_effect=OSError("Disk full")):
                with pytest.raises(OSError):
                    service.store_file(
                        job_id=job_id,
                        content=file_data["content"],
                        file_purpose=file_data["file_purpose"],
                        file_source=file_data["file_source"],
                        extension=file_data["extension"]
                    )
        
        # Count files after the operation
        files_after = set()
        if partition_path.exists():
            files_after = set(f.name for f in partition_path.glob("*"))
        
        # No new files should have been created
        new_files = files_after - files_before
        assert len(new_files) == 0, \
            f"Orphan files created after file write failure: {new_files}"
        
        # No database record should exist
        record = service.file_repo.get_by_job_and_purpose(job_id, file_data["file_purpose"])
        assert record is None, \
            f"Database record should not exist after file write failure"


@given(file_data=file_storage_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 9: Consistency on Failure")
def test_no_orphan_files_on_database_insert_failure(file_data):
    """
    Property 9: Consistency on Failure - Database Insert Failure Case
    
    For any failed store operation where database insert fails after file write,
    the file shall be cleaned up and there shall be no orphan files on disk.
    
    This test specifically verifies:
    1. If database insert fails after file write, the file is cleaned up
    2. No orphan files exist after database insert failure
    
    **Validates: Requirements 7.4, 7.5**
    """
    with temp_test_db() as conn, temp_file_storage() as storage_path:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.dif{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create service with test storage path
        service = FileStorageService(base_path=storage_path)
        service.file_repo = JobFileRepository(conn=conn)
        
        # Get the partition path
        partition_path = storage_path / service._generate_partition_path()
        
        # Count files before the operation
        files_before = set()
        if partition_path.exists():
            files_before = set(f.name for f in partition_path.glob("*"))
        
        # Simulate database insert failure
        def failing_create(job_file):
            raise sqlite3.IntegrityError("Simulated database failure")
        
        service.file_repo.create = failing_create
        
        with pytest.raises(sqlite3.IntegrityError):
            service.store_file(
                job_id=job_id,
                content=file_data["content"],
                file_purpose=file_data["file_purpose"],
                file_source=file_data["file_source"],
                extension=file_data["extension"]
            )
        
        # Count files after the operation
        files_after = set()
        if partition_path.exists():
            files_after = set(f.name for f in partition_path.glob("*"))
        
        # No new files should remain (file should have been cleaned up)
        new_files = files_after - files_before
        assert len(new_files) == 0, \
            f"Orphan files found after database insert failure (file not cleaned up): {new_files}"
        
        # No database record should exist
        # Need to use a fresh repository instance since we mocked the create method
        fresh_repo = JobFileRepository(conn=conn)
        record = fresh_repo.get_by_job_and_purpose(job_id, file_data["file_purpose"])
        assert record is None, \
            f"Database record should not exist after database insert failure"


@given(file_data=file_storage_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 9: Consistency on Failure")
def test_no_orphan_records_on_any_failure(file_data):
    """
    Property 9: Consistency on Failure - No Orphan Records
    
    For any failed store operation, there shall be no orphan database records
    without files on disk.
    
    This test verifies that after any failure scenario, if a database record
    exists, the corresponding file must also exist on disk.
    
    **Validates: Requirements 7.4, 7.5**
    """
    with temp_test_db() as conn, temp_file_storage() as storage_path:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.nor{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create service with test storage path
        service = FileStorageService(base_path=storage_path)
        service.file_repo = JobFileRepository(conn=conn)
        
        # Simulate database insert failure (this is the scenario where orphan records
        # could potentially be created if the implementation is buggy)
        def failing_create(job_file):
            raise sqlite3.IntegrityError("Simulated database failure")
        
        service.file_repo.create = failing_create
        
        with pytest.raises(sqlite3.IntegrityError):
            service.store_file(
                job_id=job_id,
                content=file_data["content"],
                file_purpose=file_data["file_purpose"],
                file_source=file_data["file_source"],
                extension=file_data["extension"]
            )
        
        # Verify no orphan database records exist
        # Use a fresh repository to check
        fresh_repo = JobFileRepository(conn=conn)
        all_records = fresh_repo.get_by_job_id(job_id)
        
        for record in all_records:
            file_path = Path(record.file_path)
            assert file_path.exists(), \
                f"Orphan database record found without file on disk: " \
                f"job_id={record.job_id}, purpose={record.file_purpose}, " \
                f"path={record.file_path}"
