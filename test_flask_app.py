"""
Test Flask application endpoints.
"""

import pytest
from src.ui.app import app
from pathlib import Path


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['JOBS_ROOT'] = Path('jobs')
    app.config['RESUMES_ROOT'] = Path('resumes')
    app.config['LOGS_DIR'] = Path('src/logs')
    
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['service'] == 'ResumAI'


def test_version_endpoint(client):
    """Test version endpoint."""
    response = client.get('/api/version')
    assert response.status_code == 200
    data = response.get_json()
    assert 'version' in data
    assert 'name' in data
    assert data['name'] == 'ResumAI Dohickey'


def test_resumes_endpoint(client):
    """Test resumes endpoint."""
    response = client.get('/api/resumes')
    assert response.status_code == 200
    data = response.get_json()
    assert 'resumes' in data
    assert 'selected' in data
    assert isinstance(data['resumes'], list)


def test_jobs_endpoint(client):
    """Test jobs endpoint."""
    response = client.get('/api/jobs')
    assert response.status_code == 200
    data = response.get_json()
    assert 'jobs' in data
    assert 'phase_counts' in data
    assert isinstance(data['jobs'], list)
    assert isinstance(data['phase_counts'], dict)


def test_jobs_endpoint_with_phase_filter(client):
    """Test jobs endpoint with phase filter."""
    response = client.get('/api/jobs?phase=1_Queued')
    assert response.status_code == 200
    data = response.get_json()
    assert 'jobs' in data
    # All returned jobs should be in Queued phase
    for job in data['jobs']:
        assert job['phase'] == '1_Queued'


def test_logs_endpoint(client):
    """Test logs endpoint."""
    response = client.get('/api/logs')
    assert response.status_code == 200
    data = response.get_json()
    assert 'logs' in data
    assert isinstance(data['logs'], str)


def test_job_stats_endpoint(client):
    """Test job stats endpoint."""
    response = client.get('/api/job_stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'stats' in data
    assert isinstance(data['stats'], dict)


def test_manual_entry_missing_fields(client):
    """Test manual entry with missing fields."""
    response = client.post('/api/manual_entry', 
                          json={'company': 'Test Corp'},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert data['ok'] is False
    assert 'Missing required field' in data['message']


def test_add_url_missing_url(client):
    """Test add URL with missing URL."""
    response = client.post('/api/add_url', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert data['ok'] is False
    assert 'URL is required' in data['message']


def test_generate_data_missing_job(client):
    """Test generate data with missing job folder name."""
    response = client.post('/api/generate_data', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert data['ok'] is False
    assert 'job_folder_name is required' in data['message']


def test_move_phase_missing_params(client):
    """Test move phase with missing parameters."""
    response = client.post('/api/move_phase', 
                          json={'job_folder_name': 'test'},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert data['ok'] is False


def test_toggle_generation_missing_params(client):
    """Test toggle generation with missing parameters."""
    response = client.post('/api/toggle_generation', 
                          json={'job_folder_name': 'test'},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert data['ok'] is False


def test_job_detail_not_found(client):
    """Test job detail endpoint with non-existent job."""
    response = client.get('/api/job/nonexistent-job')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data


def test_index_page(client):
    """Test index page renders."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'ResumAI' in response.data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# ============================================================================
# Tests for new database-centric file viewing endpoint
# Requirements: 6.1, 6.2, 6.3
# ============================================================================

import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.db.models import JobFile


@pytest.fixture
def temp_files_dir():
    """Create a temporary directory for file storage."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


def test_view_file_by_job_id_returns_404_when_no_record(client):
    """
    Test that the endpoint returns 404 when no file record exists.
    
    Requirements: 6.3
    """
    with patch('src.ui.app._get_file_storage_service') as mock_service:
        mock_instance = MagicMock()
        mock_instance.file_repo.get_by_job_and_purpose.return_value = None
        mock_service.return_value = mock_instance
        
        response = client.get('/api/view/99999/resume_html')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'File not found'
        assert data['job_id'] == 99999
        assert data['purpose'] == 'resume_html'


def test_view_file_by_job_id_returns_file_content(client, temp_files_dir):
    """
    Test that the endpoint returns file content when record exists.
    
    Requirements: 6.1, 6.2
    """
    # Create a test file
    test_content = '<html><body>Test Resume</body></html>'
    test_file = temp_files_dir / 'test_resume.html'
    test_file.write_text(test_content)
    
    # Mock the file storage service
    mock_job_file = JobFile(
        id=1,
        job_id=42,
        filename='test_resume.html',
        file_path=str(test_file),
        file_purpose='resume_html',
        file_source='generated'
    )
    
    with patch('src.ui.app._get_file_storage_service') as mock_service:
        mock_instance = MagicMock()
        mock_instance.file_repo.get_by_job_and_purpose.return_value = mock_job_file
        mock_service.return_value = mock_instance
        
        response = client.get('/api/view/42/resume_html')
        
        assert response.status_code == 200
        assert 'text/html' in response.content_type
        assert response.data.decode() == test_content


def test_view_file_by_job_id_returns_500_when_file_missing(client, temp_files_dir):
    """
    Test that the endpoint returns 500 when record exists but file is missing.
    
    Requirements: 6.3 (inconsistency detection)
    """
    # Create a mock job file record pointing to a non-existent file
    mock_job_file = JobFile(
        id=1,
        job_id=42,
        filename='missing_file.html',
        file_path=str(temp_files_dir / 'missing_file.html'),
        file_purpose='resume_html',
        file_source='generated'
    )
    
    with patch('src.ui.app._get_file_storage_service') as mock_service:
        mock_instance = MagicMock()
        mock_instance.file_repo.get_by_job_and_purpose.return_value = mock_job_file
        mock_service.return_value = mock_instance
        
        response = client.get('/api/view/42/resume_html')
        
        assert response.status_code == 500
        data = response.get_json()
        assert data['error'] == 'File inconsistency'
        assert data['job_id'] == 42
        assert data['purpose'] == 'resume_html'
        assert 'expected_path' in data


def test_view_file_by_job_id_serves_pdf_as_binary(client, temp_files_dir):
    """
    Test that PDF files are served with correct content type.
    
    Requirements: 6.1, 6.2
    """
    # Create a test PDF file (just binary content for testing)
    test_content = b'%PDF-1.4 test content'
    test_file = temp_files_dir / 'test_resume.pdf'
    test_file.write_bytes(test_content)
    
    mock_job_file = JobFile(
        id=1,
        job_id=42,
        filename='test_resume.pdf',
        file_path=str(test_file),
        file_purpose='resume_pdf',
        file_source='generated'
    )
    
    with patch('src.ui.app._get_file_storage_service') as mock_service:
        mock_instance = MagicMock()
        mock_instance.file_repo.get_by_job_and_purpose.return_value = mock_job_file
        mock_service.return_value = mock_instance
        
        response = client.get('/api/view/42/resume_pdf')
        
        assert response.status_code == 200
        assert response.content_type == 'application/pdf'
        assert response.data == test_content


def test_view_file_by_job_id_handles_database_error(client):
    """
    Test that the endpoint handles database errors gracefully.
    """
    with patch('src.ui.app._get_file_storage_service') as mock_service:
        mock_instance = MagicMock()
        mock_instance.file_repo.get_by_job_and_purpose.side_effect = Exception('Database connection failed')
        mock_service.return_value = mock_instance
        
        response = client.get('/api/view/42/resume_html')
        
        assert response.status_code == 500
        data = response.get_json()
        assert data['error'] == 'Database error'
        assert 'Database connection failed' in data['details']


def test_view_file_by_job_id_different_file_purposes(client, temp_files_dir):
    """
    Test that the endpoint works with different file purposes.
    
    Requirements: 6.1
    """
    file_purposes = [
        ('job_posting_html', '.html', 'text/html'),
        ('resume_html', '.html', 'text/html'),
        ('coverletter_html', '.html', 'text/html'),
        ('resume_pdf', '.pdf', 'application/pdf'),
        ('coverletter_pdf', '.pdf', 'application/pdf'),
    ]
    
    for purpose, ext, expected_content_type in file_purposes:
        # Create test file
        if ext == '.pdf':
            test_content = b'%PDF-1.4 test'
            test_file = temp_files_dir / f'test{ext}'
            test_file.write_bytes(test_content)
        else:
            test_content = '<html>test</html>'
            test_file = temp_files_dir / f'test{ext}'
            test_file.write_text(test_content)
        
        mock_job_file = JobFile(
            id=1,
            job_id=42,
            filename=f'test{ext}',
            file_path=str(test_file),
            file_purpose=purpose,
            file_source='generated'
        )
        
        with patch('src.ui.app._get_file_storage_service') as mock_service:
            mock_instance = MagicMock()
            mock_instance.file_repo.get_by_job_and_purpose.return_value = mock_job_file
            mock_service.return_value = mock_instance
            
            response = client.get(f'/api/view/42/{purpose}')
            
            assert response.status_code == 200, f"Failed for purpose: {purpose}"
            assert expected_content_type in response.content_type, f"Wrong content type for: {purpose}"


# ============================================================================
# Property-Based Tests for API Database Lookup
# Feature: database-centric-file-management
# ============================================================================

from hypothesis import given, settings, strategies as st, HealthCheck


# Valid file purposes as defined in the design document
FILE_PURPOSES = [
    "job_posting_html",
    "resume_html",
    "resume_pdf",
    "coverletter_html",
    "coverletter_pdf",
]


@given(
    job_id=st.integers(min_value=1, max_value=10000),
    file_purpose=st.sampled_from(FILE_PURPOSES)
)
@settings(max_examples=100, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 10: API Database Lookup")
def test_property_api_database_lookup(client, temp_files_dir, job_id, file_purpose):
    """
    Property 10: API Database Lookup
    
    For any file request to the view API with a valid job_id and file_purpose,
    the file content returned shall be read from the path stored in the 
    Job_Files_Table, not from a hardcoded filesystem location.
    
    **Validates: Requirements 6.2, 6.4**
    """
    # Determine extension based on purpose
    if file_purpose.endswith('_pdf'):
        ext = '.pdf'
        test_content = b'%PDF-1.4 test content for property test'
    else:
        ext = '.html'
        test_content = '<html><body>Property test content</body></html>'
    
    # Create a test file at a unique path (not the legacy location)
    unique_filename = f'property_test_{job_id}_{file_purpose}{ext}'
    test_file = temp_files_dir / unique_filename
    
    if ext == '.pdf':
        test_file.write_bytes(test_content)
    else:
        test_file.write_text(test_content)
    
    # Create mock job file record pointing to our unique path
    mock_job_file = JobFile(
        id=job_id,
        job_id=job_id,
        filename=unique_filename,
        file_path=str(test_file),
        file_purpose=file_purpose,
        file_source='generated'
    )
    
    with patch('src.ui.app._get_file_storage_service') as mock_service:
        mock_instance = MagicMock()
        mock_instance.file_repo.get_by_job_and_purpose.return_value = mock_job_file
        mock_service.return_value = mock_instance
        
        response = client.get(f'/api/view/{job_id}/{file_purpose}')
        
        # Verify the API returns the content from the database-stored path
        assert response.status_code == 200, \
            f"Expected 200 for job_id={job_id}, purpose={file_purpose}"
        
        # Verify the content matches what we stored at the database path
        if ext == '.pdf':
            assert response.data == test_content, \
                "Content should be read from database-stored path"
        else:
            assert response.data.decode() == test_content, \
                "Content should be read from database-stored path"
        
        # Verify the repository was queried with correct parameters
        mock_instance.file_repo.get_by_job_and_purpose.assert_called_once_with(
            job_id, file_purpose
        )


@given(
    job_id=st.integers(min_value=1, max_value=10000),
    file_purpose=st.sampled_from(FILE_PURPOSES)
)
@settings(max_examples=100, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 11: API 404 on Missing Records")
def test_property_api_404_on_missing_records(client, job_id, file_purpose):
    """
    Property 11: API 404 on Missing Records
    
    For any file request to the view API where no Job_Files_Table record exists
    for the given job_id and file_purpose, the API shall return a 404 status code.
    
    **Validates: Requirements 6.3**
    """
    with patch('src.ui.app._get_file_storage_service') as mock_service:
        mock_instance = MagicMock()
        # Simulate no record found in database
        mock_instance.file_repo.get_by_job_and_purpose.return_value = None
        mock_service.return_value = mock_instance
        
        response = client.get(f'/api/view/{job_id}/{file_purpose}')
        
        # Verify 404 is returned
        assert response.status_code == 404, \
            f"Expected 404 for missing record: job_id={job_id}, purpose={file_purpose}"
        
        # Verify error response structure
        data = response.get_json()
        assert data['error'] == 'File not found', \
            "Error message should indicate file not found"
        assert data['job_id'] == job_id, \
            "Response should include the requested job_id"
        assert data['purpose'] == file_purpose, \
            "Response should include the requested purpose"


@given(
    job_id=st.integers(min_value=1, max_value=10000),
    num_files=st.integers(min_value=0, max_value=5)
)
@settings(max_examples=100, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 12: Job Detail File Completeness")
def test_property_job_detail_file_completeness(client, temp_files_dir, job_id, num_files):
    """
    Property 12: Job Detail File Completeness
    
    For any job with file records in the Job_Files_Table, the job detail API
    response shall include all file records with their purpose, path, source,
    and timestamps.
    
    **Validates: Requirements 8.1, 8.2, 8.3**
    """
    from datetime import datetime
    
    # Select random file purposes for this test
    selected_purposes = FILE_PURPOSES[:num_files] if num_files > 0 else []
    
    # Create mock job files
    mock_job_files = []
    for i, purpose in enumerate(selected_purposes):
        ext = '.pdf' if purpose.endswith('_pdf') else '.html'
        filename = f'test_{job_id}_{purpose}{ext}'
        file_path = temp_files_dir / filename
        
        # Create actual file on disk
        if ext == '.pdf':
            file_path.write_bytes(b'%PDF-1.4 test')
        else:
            file_path.write_text('<html>test</html>')
        
        mock_job_files.append(JobFile(
            id=i + 1,
            job_id=job_id,
            filename=filename,
            file_path=str(file_path),
            file_purpose=purpose,
            file_source='generated',
            created_at=datetime.now(),
            updated_at=datetime.now()
        ))
    
    # Mock the job service and file storage service
    with patch('src.ui.app._db_enabled', return_value=True), \
         patch('src.ui.app._get_job_service') as mock_job_svc, \
         patch('src.ui.app._get_file_storage_service') as mock_file_svc:
        
        # Create mock job detail
        mock_job = MagicMock()
        mock_job.id = job_id
        mock_job.external_id = f'ext_{job_id}'
        mock_job.company = 'TestCorp'
        mock_job.title = 'Engineer'
        mock_job.url = 'https://example.com/job'
        mock_job.location = 'Remote'
        mock_job.salary = '$100k'
        mock_job.tags = ['python', 'flask']
        mock_job.source = 'linkedin'
        mock_job.date_posted = datetime.now()
        mock_job.description = 'Test job description'
        mock_job.folder_name = f'TestCorp.Engineer.{job_id}'
        mock_job.phase = '1_Queued'
        mock_job.subcontent_events = {}
        
        mock_job_detail = MagicMock()
        mock_job_detail.job = mock_job
        mock_job_detail.subcontent_status = MagicMock(
            contacts=False, summary=False, skills=False, highlights=False,
            experience=False, education=False, awards=False, coverletter=False
        )
        mock_job_detail.doc_status = MagicMock(
            resume_html=False, resume_pdf=False,
            coverletter_html=False, coverletter_pdf=False
        )
        
        mock_job_svc_instance = MagicMock()
        mock_job_svc_instance.get_job_detail.return_value = mock_job_detail
        mock_job_svc.return_value = mock_job_svc_instance
        
        mock_file_svc_instance = MagicMock()
        mock_file_svc_instance.get_files_for_job.return_value = mock_job_files
        mock_file_svc.return_value = mock_file_svc_instance
        
        response = client.get(f'/api/job/TestCorp.Engineer.{job_id}')
        
        # Should return 200 (job found)
        assert response.status_code == 200, \
            f"Expected 200 for job detail: job_id={job_id}"
        
        data = response.get_json()
        
        # Verify files are included in response
        assert 'files' in data, "Response should include files"
        
        # Verify all file records are present with required metadata
        for job_file in mock_job_files:
            assert job_file.filename in data['files'], \
                f"File {job_file.filename} should be in response"
            
            file_info = data['files'][job_file.filename]
            assert 'purpose' in file_info, "File info should include purpose"
            assert 'path' in file_info, "File info should include path"
            assert 'source' in file_info, "File info should include source"
            assert file_info['purpose'] == job_file.file_purpose
            assert file_info['path'] == job_file.file_path
            assert file_info['source'] == job_file.file_source


@given(
    job_id=st.integers(min_value=1, max_value=10000),
    file_purpose=st.sampled_from(FILE_PURPOSES)
)
@settings(max_examples=100, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@pytest.mark.property
@pytest.mark.tag("Feature: database-centric-file-management, Property 13: Inconsistency Detection")
def test_property_inconsistency_detection(client, temp_files_dir, job_id, file_purpose):
    """
    Property 13: Inconsistency Detection
    
    For any job where a Job_Files_Table record exists but the referenced file
    is missing from disk, the job detail API shall indicate this inconsistency
    in the response.
    
    **Validates: Requirements 8.4**
    """
    from datetime import datetime
    
    # Create a mock job file record pointing to a non-existent file
    ext = '.pdf' if file_purpose.endswith('_pdf') else '.html'
    filename = f'missing_{job_id}_{file_purpose}{ext}'
    missing_file_path = temp_files_dir / filename  # File does NOT exist
    
    mock_job_file = JobFile(
        id=1,
        job_id=job_id,
        filename=filename,
        file_path=str(missing_file_path),
        file_purpose=file_purpose,
        file_source='generated',
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Mock the job service and file storage service
    with patch('src.ui.app._db_enabled', return_value=True), \
         patch('src.ui.app._get_job_service') as mock_job_svc, \
         patch('src.ui.app._get_file_storage_service') as mock_file_svc:
        
        # Create mock job detail
        mock_job = MagicMock()
        mock_job.id = job_id
        mock_job.external_id = f'ext_{job_id}'
        mock_job.company = 'TestCorp'
        mock_job.title = 'Engineer'
        mock_job.url = 'https://example.com/job'
        mock_job.location = 'Remote'
        mock_job.salary = '$100k'
        mock_job.tags = ['python', 'flask']
        mock_job.source = 'linkedin'
        mock_job.date_posted = datetime.now()
        mock_job.description = 'Test job description'
        mock_job.folder_name = f'TestCorp.Engineer.{job_id}'
        mock_job.phase = '1_Queued'
        mock_job.subcontent_events = {}
        
        mock_job_detail = MagicMock()
        mock_job_detail.job = mock_job
        mock_job_detail.subcontent_status = MagicMock(
            contacts=False, summary=False, skills=False, highlights=False,
            experience=False, education=False, awards=False, coverletter=False
        )
        mock_job_detail.doc_status = MagicMock(
            resume_html=False, resume_pdf=False,
            coverletter_html=False, coverletter_pdf=False
        )
        
        mock_job_svc_instance = MagicMock()
        mock_job_svc_instance.get_job_detail.return_value = mock_job_detail
        mock_job_svc.return_value = mock_job_svc_instance
        
        mock_file_svc_instance = MagicMock()
        mock_file_svc_instance.get_files_for_job.return_value = [mock_job_file]
        mock_file_svc.return_value = mock_file_svc_instance
        
        response = client.get(f'/api/job/TestCorp.Engineer.{job_id}')
        
        # Should return 200 (job found, but with inconsistency info)
        assert response.status_code == 200, \
            f"Expected 200 for job detail: job_id={job_id}"
        
        data = response.get_json()
        
        # Verify inconsistency is detected and reported
        assert 'file_inconsistencies' in data, \
            "Response should include file_inconsistencies when files are missing"
        
        # Verify the inconsistency details
        inconsistencies = data['file_inconsistencies']
        assert len(inconsistencies) > 0, \
            "Should have at least one inconsistency"
        
        # Find the inconsistency for our file
        found_inconsistency = False
        for inc in inconsistencies:
            if inc['purpose'] == file_purpose:
                found_inconsistency = True
                assert 'expected_path' in inc, \
                    "Inconsistency should include expected_path"
                assert 'error' in inc, \
                    "Inconsistency should include error message"
                assert str(missing_file_path) in inc['expected_path'], \
                    "Expected path should match the missing file path"
        
        assert found_inconsistency, \
            f"Should detect inconsistency for purpose: {file_purpose}"
        
        # Verify the file is marked as not existing
        assert filename in data['files'], \
            f"File {filename} should be in response"
        assert data['files'][filename]['exists'] is False, \
            "File should be marked as not existing"
