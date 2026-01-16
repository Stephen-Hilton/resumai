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
