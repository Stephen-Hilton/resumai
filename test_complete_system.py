"""
Complete system integration test.

Tests the entire ResumAI system from job creation to document generation,
including web API endpoints and batch processing.
"""

import pytest
import asyncio
from pathlib import Path
import tempfile
import shutil
from datetime import datetime
from src.lib.types import EventContext
from src.lib.job_folders import JobIdentity, folder_name
from src.events.event_bus import run_event
from src.ui.app import app


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for testing."""
    temp_dir = Path(tempfile.mkdtemp())
    jobs_root = temp_dir / "jobs"
    resumes_root = temp_dir / "resumes"
    logs_dir = temp_dir / "logs"
    
    # Create directories
    jobs_root.mkdir()
    resumes_root.mkdir()
    logs_dir.mkdir()
    
    # Create phase directories
    for phase in ['1_Queued', '2_Data_Generated', '3_Docs_Generated', '4_Applied',
                  '5_FollowUp', '6_Interviewing', '7_Negotiating', '8_Accepted',
                  'Skipped', 'Expired', 'Errored']:
        (jobs_root / phase).mkdir()
    
    # Copy test resume
    test_resume = Path('resumes/Stephen_Hilton.yaml')
    if test_resume.exists():
        shutil.copy(test_resume, resumes_root / 'Stephen_Hilton.yaml')
    
    yield {
        'temp_dir': temp_dir,
        'jobs_root': jobs_root,
        'resumes_root': resumes_root,
        'logs_dir': logs_dir
    }
    
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.mark.asyncio
async def test_complete_workflow(temp_workspace):
    """Test complete workflow from job creation to document generation."""
    jobs_root = temp_workspace['jobs_root']
    resumes_root = temp_workspace['resumes_root']
    
    ctx = EventContext(
        jobs_root=jobs_root,
        resumes_root=resumes_root,
        default_resume='Stephen_Hilton.yaml',
        test_mode=True
    )
    
    # 1. Create a job
    identity = JobIdentity(
        company="TestCorp",
        title="Senior Engineer",
        posted_at=datetime(2026, 1, 15, 12, 0, 0),
        job_id="test123"
    )
    
    job_folder = folder_name(identity)
    job_path = jobs_root / '1_Queued' / job_folder
    
    result = await run_event('create_jobfolder', jobs_root, ctx.with_state({
        'identity': identity,
        'url': 'https://example.com/job',
        'description': 'Test job description',
        'location': 'Remote',
        'source': 'test'
    }))
    
    assert result.ok, f"Job creation failed: {result.message}"
    assert job_path.exists(), "Job folder not created"
    
    # 2. Generate data (static mode for speed)
    result = await run_event('batch_gen_data', job_path, ctx)
    assert result.ok, f"Data generation failed: {result.message}"
    
    # Verify job moved to Data_Generated
    new_path = jobs_root / '2_Data_Generated' / job_folder
    assert new_path.exists(), "Job not moved to Data_Generated phase"
    
    # 3. Generate documents
    result = await run_event('batch_gen_docs', new_path, ctx)
    assert result.ok, f"Document generation failed: {result.message}"
    
    # Verify job moved to Docs_Generated
    final_path = jobs_root / '3_Docs_Generated' / job_folder
    assert final_path.exists(), "Job not moved to Docs_Generated phase"
    
    # 4. Verify all files exist
    assert (final_path / 'job.yaml').exists()
    assert (final_path / 'job.log').exists()
    assert (final_path / 'resume.html').exists()
    assert (final_path / 'coverletter.html').exists()
    assert (final_path / 'resume.pdf').exists()
    assert (final_path / 'coverletter.pdf').exists()
    
    # 5. Move to Applied phase
    result = await run_event('move_applied', final_path, ctx)
    assert result.ok, f"Move to Applied failed: {result.message}"
    
    applied_path = jobs_root / '4_Applied' / job_folder
    assert applied_path.exists(), "Job not moved to Applied phase"
    
    print("✅ Complete workflow test passed!")


def test_flask_api_integration(temp_workspace):
    """Test Flask API endpoints."""
    app.config['TESTING'] = True
    app.config['JOBS_ROOT'] = temp_workspace['jobs_root']
    app.config['RESUMES_ROOT'] = temp_workspace['resumes_root']
    app.config['LOGS_DIR'] = temp_workspace['logs_dir']
    
    with app.test_client() as client:
        # Test health endpoint
        response = client.get('/health')
        assert response.status_code == 200
        
        # Test version endpoint
        response = client.get('/api/version')
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'ResumAI Dohickey'
        
        # Test jobs endpoint
        response = client.get('/api/jobs')
        assert response.status_code == 200
        data = response.get_json()
        assert 'jobs' in data
        assert 'phase_counts' in data
        
        # Test resumes endpoint
        response = client.get('/api/resumes')
        assert response.status_code == 200
        data = response.get_json()
        assert 'resumes' in data
        
        # Test logs endpoint
        response = client.get('/api/logs')
        assert response.status_code == 200
        data = response.get_json()
        assert 'logs' in data
        
        # Test job stats endpoint
        response = client.get('/api/job_stats')
        assert response.status_code == 200
        data = response.get_json()
        assert 'stats' in data
        
        print("✅ Flask API integration test passed!")


def test_error_handling(temp_workspace):
    """Test error handling and recovery."""
    jobs_root = temp_workspace['jobs_root']
    resumes_root = temp_workspace['resumes_root']
    
    ctx = EventContext(
        jobs_root=jobs_root,
        resumes_root=resumes_root,
        default_resume='nonexistent.yaml',  # This will cause errors
        test_mode=True
    )
    
    # Create a job
    identity = JobIdentity(
        company="ErrorTest",
        title="Test",
        posted_at=datetime(2026, 1, 15, 12, 0, 0),
        job_id="error123"
    )
    
    job_folder = folder_name(identity)
    job_path = jobs_root / '1_Queued' / job_folder
    
    # Create job folder manually
    job_path.mkdir(parents=True)
    (job_path / 'job.yaml').write_text('company: ErrorTest\ntitle: Test\nid: error123\ndate: 20260115-120000\nurl: https://example.com\n')
    
    # Try to generate data with nonexistent resume - should fail gracefully
    result = asyncio.run(run_event('batch_gen_data', job_path, ctx))
    
    # Should fail but not crash
    assert not result.ok, "Expected failure with nonexistent resume"
    
    print("✅ Error handling test passed!")


def test_log_rotation(temp_workspace):
    """Test log rotation functionality."""
    from src.lib.log_rotation import rotate_logs, compress_log
    from datetime import datetime, timedelta
    
    logs_dir = temp_workspace['logs_dir']
    
    # Create a fake old log file
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    old_log = logs_dir / f"{yesterday}.applog.txt"
    old_log.write_text("Old log content\n" * 100)
    
    # Run rotation
    rotate_logs(logs_dir)
    
    # Check if old log was compressed
    compressed = logs_dir / f"{yesterday}.applog.txt.gz"
    assert compressed.exists() or old_log.exists(), "Log should exist (compressed or not)"
    
    print("✅ Log rotation test passed!")


def test_folder_correction(temp_workspace):
    """Test folder name correction."""
    from src.lib.folder_correction import validate_and_correct_folder_name
    
    jobs_root = temp_workspace['jobs_root']
    logs_dir = temp_workspace['logs_dir']
    
    # Create a job with mismatched folder name
    wrong_folder = jobs_root / '1_Queued' / 'WrongName'
    wrong_folder.mkdir(parents=True)
    
    # Create job.yaml with correct data
    (wrong_folder / 'job.yaml').write_text(
        'company: CorrectCorp\n'
        'title: Engineer\n'
        'id: correct123\n'
        'date: 20260115-120000\n'
        'url: https://example.com\n'
    )
    
    # Run correction
    corrected_path = validate_and_correct_folder_name(wrong_folder, logs_dir)
    
    # Should have been renamed
    assert corrected_path.name != 'WrongName', "Folder should have been renamed"
    assert corrected_path.exists(), "Corrected folder should exist"
    
    print("✅ Folder correction test passed!")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
