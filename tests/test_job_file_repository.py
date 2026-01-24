"""
Property-based tests for JobFileRepository.

Feature: database-centric-file-management
"""

import sqlite3
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

from src.db.models import JobFile
from src.db.schema import create_schema
from src.repositories.job_file_repository import JobFileRepository


# =============================================================================
# TEST HELPERS
# =============================================================================

@contextmanager
def temp_test_db():
    """
    Create a temporary test database with schema.
    
    Yields a connection that is cleaned up after use.
    """
    # Create a temporary database file
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = Path(f.name)
    
    # Create connection and schema
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    create_schema(conn)
    
    try:
        yield conn
    finally:
        # Cleanup
        conn.close()
        db_path.unlink(missing_ok=True)


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
# CUSTOM STRATEGIES
# =============================================================================

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
def job_file_data(draw):
    """
    Generate random valid JobFile data.
    
    Returns a dictionary with all required fields for creating a JobFile.
    Note: job_id must be provided separately since it requires a valid FK.
    """
    # Generate a unique filename using UUID-like pattern
    uuid_part = draw(st.text(
        alphabet="abcdef0123456789",
        min_size=8,
        max_size=8
    ))
    
    file_purpose = draw(st.sampled_from(FILE_PURPOSES))
    file_source = draw(st.sampled_from(FILE_SOURCES))
    
    # Determine extension based on purpose
    if file_purpose.endswith("_pdf"):
        extension = "pdf"
    else:
        extension = "html"
    
    # Generate partition folder (YYYYMM format)
    year = draw(st.integers(min_value=2024, max_value=2030))
    month = draw(st.integers(min_value=1, max_value=12))
    partition = f"{year}{month:02d}"
    
    filename = f"job_{file_purpose}_{uuid_part}.{extension}"
    file_path = f"src/files/{partition}/{filename}"
    
    return {
        "filename": filename,
        "file_path": file_path,
        "file_purpose": file_purpose,
        "file_source": file_source,
    }


# =============================================================================
# PROPERTY TESTS
# =============================================================================

@given(file_data=job_file_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 5: Repository Round-Trip Consistency")
def test_repository_round_trip_consistency(file_data):
    """
    Property 5: Repository Round-Trip Consistency
    
    For any valid JobFile record created via JobFileRepository.create(),
    retrieving it via get_by_job_and_purpose() with the same job_id and
    file_purpose shall return an equivalent record.
    
    **Validates: Requirements 3.1, 3.3**
    """
    with temp_test_db() as conn:
        # Create a fresh job for each test iteration to avoid unique constraint violations
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.test{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create repository with test connection
        repo = JobFileRepository(conn=conn)
        
        # Create the JobFile record
        job_file = JobFile(
            job_id=job_id,
            filename=file_data["filename"],
            file_path=file_data["file_path"],
            file_purpose=file_data["file_purpose"],
            file_source=file_data["file_source"],
        )
        
        # Create the record in the database
        created_id = repo.create(job_file)
        
        # Verify the ID was returned
        assert created_id is not None
        assert created_id > 0
        
        # Retrieve the record using get_by_job_and_purpose
        retrieved = repo.get_by_job_and_purpose(job_id, file_data["file_purpose"])
        
        # Verify the record was retrieved
        assert retrieved is not None, "Retrieved record should not be None"
        
        # Verify all fields match the original data
        assert retrieved.job_id == job_id, "job_id should match"
        assert retrieved.filename == file_data["filename"], "filename should match"
        assert retrieved.file_path == file_data["file_path"], "file_path should match"
        assert retrieved.file_purpose == file_data["file_purpose"], "file_purpose should match"
        assert retrieved.file_source == file_data["file_source"], "file_source should match"
        
        # Verify the ID was assigned
        assert retrieved.id == created_id, "id should match the created id"
        
        # Verify timestamps were set (they should be auto-generated by the database)
        assert retrieved.created_at is not None, "created_at should be set"
        assert retrieved.updated_at is not None, "updated_at should be set"


@given(file_data=job_file_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 6: Repository Existence Check Accuracy")
def test_repository_existence_check_accuracy(file_data):
    """
    Property 6: Repository Existence Check Accuracy
    
    For any job_id and file_purpose, JobFileRepository.exists() shall return
    True if and only if a record with that combination exists in the database.
    
    This test verifies:
    1. exists() returns False for non-existent records
    2. exists() returns True after creating a record
    3. exists() returns False after deleting a record
    
    **Validates: Requirements 3.4, 3.6**
    """
    with temp_test_db() as conn:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.exist{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create repository with test connection
        repo = JobFileRepository(conn=conn)
        
        file_purpose = file_data["file_purpose"]
        
        # 1. Verify exists() returns False for non-existent records
        assert repo.exists(job_id, file_purpose) is False, \
            "exists() should return False before record is created"
        
        # 2. Create the JobFile record
        job_file = JobFile(
            job_id=job_id,
            filename=file_data["filename"],
            file_path=file_data["file_path"],
            file_purpose=file_purpose,
            file_source=file_data["file_source"],
        )
        created_id = repo.create(job_file)
        
        # Verify exists() returns True after creating a record
        assert repo.exists(job_id, file_purpose) is True, \
            "exists() should return True after record is created"
        
        # 3. Delete the record
        deleted = repo.delete(created_id)
        assert deleted is True, "delete() should return True for existing record"
        
        # Verify exists() returns False after deleting a record
        assert repo.exists(job_id, file_purpose) is False, \
            "exists() should return False after record is deleted"


# =============================================================================
# DATABASE CONSTRAINT PROPERTY TESTS
# =============================================================================

@given(file_data=job_file_data())
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 1: CASCADE Delete Removes File Records")
def test_cascade_delete_removes_file_records(file_data):
    """
    Property 1: CASCADE Delete Removes File Records
    
    For any job with associated file records in the Job_Files_Table, when the
    job is deleted from the jobs table, all associated file records shall be
    automatically deleted.
    
    **Validates: Requirements 1.2, 1.4**
    """
    with temp_test_db() as conn:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.cascade{id(file_data)}"
        job_id = create_job(conn, folder_name)
        
        # Create repository with test connection
        repo = JobFileRepository(conn=conn)
        
        # Create a file record for the job
        job_file = JobFile(
            job_id=job_id,
            filename=file_data["filename"],
            file_path=file_data["file_path"],
            file_purpose=file_data["file_purpose"],
            file_source=file_data["file_source"],
        )
        created_id = repo.create(job_file)
        
        # Verify the file record exists
        assert repo.exists(job_id, file_data["file_purpose"]) is True, \
            "File record should exist after creation"
        
        # Delete the job (this should CASCADE delete the file records)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
        cursor.close()
        
        # Verify the file record was automatically deleted via CASCADE
        assert repo.exists(job_id, file_data["file_purpose"]) is False, \
            "File record should be deleted when parent job is deleted (CASCADE)"
        
        # Also verify by direct query
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM job_files WHERE job_id = ?", (job_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        
        assert count == 0, \
            "No file records should remain after parent job is deleted"


@given(
    file_data1=job_file_data(),
    file_data2=job_file_data()
)
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 2: Unique Constraint Enforcement")
def test_unique_constraint_enforcement(file_data1, file_data2):
    """
    Property 2: Unique Constraint Enforcement
    
    For any job_id and file_purpose combination, attempting to create a second
    file record with the same combination shall fail with a constraint violation.
    
    **Validates: Requirements 1.3**
    """
    with temp_test_db() as conn:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.unique{id(file_data1)}"
        job_id = create_job(conn, folder_name)
        
        # Create repository with test connection
        repo = JobFileRepository(conn=conn)
        
        # Use the same file_purpose for both records to test unique constraint
        shared_purpose = file_data1["file_purpose"]
        
        # Create the first file record
        job_file1 = JobFile(
            job_id=job_id,
            filename=file_data1["filename"],
            file_path=file_data1["file_path"],
            file_purpose=shared_purpose,
            file_source=file_data1["file_source"],
        )
        created_id = repo.create(job_file1)
        
        # Verify the first record was created
        assert created_id is not None, "First record should be created successfully"
        assert repo.exists(job_id, shared_purpose) is True, \
            "First file record should exist"
        
        # Attempt to create a second record with the same job_id and file_purpose
        job_file2 = JobFile(
            job_id=job_id,
            filename=file_data2["filename"],  # Different filename
            file_path=file_data2["file_path"],  # Different path
            file_purpose=shared_purpose,  # SAME purpose - should violate constraint
            file_source=file_data2["file_source"],
        )
        
        # This should raise an IntegrityError due to UNIQUE constraint
        import sqlite3
        with pytest.raises(sqlite3.IntegrityError) as exc_info:
            repo.create(job_file2)
        
        # Verify the error is about the unique constraint
        error_message = str(exc_info.value).lower()
        assert "unique" in error_message or "constraint" in error_message, \
            f"Error should mention unique constraint violation: {exc_info.value}"
        
        # Verify only one record exists
        files = repo.get_by_job_id(job_id)
        assert len(files) == 1, \
            "Only one file record should exist after constraint violation"
        assert files[0].id == created_id, \
            "The original record should still exist"


@given(
    num_files=st.integers(min_value=1, max_value=5)
)
@settings(max_examples=100, deadline=None)
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 1: CASCADE Delete Removes Multiple File Records")
def test_cascade_delete_removes_multiple_file_records(num_files):
    """
    Property 1 (Extended): CASCADE Delete Removes Multiple File Records
    
    For any job with multiple associated file records in the Job_Files_Table,
    when the job is deleted from the jobs table, ALL associated file records
    shall be automatically deleted.
    
    **Validates: Requirements 1.2, 1.4**
    """
    with temp_test_db() as conn:
        # Create a fresh job for each test iteration
        folder_name = f"TestCorp.Engineer.{datetime.now().strftime('%Y%m%d-%H%M%S%f')}.multi{num_files}"
        job_id = create_job(conn, folder_name)
        
        # Create repository with test connection
        repo = JobFileRepository(conn=conn)
        
        # Create multiple file records with different purposes
        purposes_to_create = FILE_PURPOSES[:num_files]
        created_ids = []
        
        for i, purpose in enumerate(purposes_to_create):
            ext = "pdf" if purpose.endswith("_pdf") else "html"
            job_file = JobFile(
                job_id=job_id,
                filename=f"test_{i}_{purpose}.{ext}",
                file_path=f"src/files/202601/test_{i}_{purpose}.{ext}",
                file_purpose=purpose,
                file_source="generated",
            )
            created_id = repo.create(job_file)
            created_ids.append(created_id)
        
        # Verify all file records exist
        files_before = repo.get_by_job_id(job_id)
        assert len(files_before) == num_files, \
            f"Should have {num_files} file records before deletion"
        
        # Delete the job (this should CASCADE delete all file records)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
        cursor.close()
        
        # Verify all file records were automatically deleted via CASCADE
        files_after = repo.get_by_job_id(job_id)
        assert len(files_after) == 0, \
            "All file records should be deleted when parent job is deleted (CASCADE)"
        
        # Also verify by direct query
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM job_files WHERE job_id = ?", (job_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        
        assert count == 0, \
            "No file records should remain after parent job is deleted"
