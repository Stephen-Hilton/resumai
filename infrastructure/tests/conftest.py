"""
Pytest configuration for Skillsnap infrastructure tests.
"""
import pytest
import sys
import os

# Add lambdas directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambdas'))


@pytest.fixture
def sample_resume_json():
    """Sample valid resume JSON for testing."""
    return {
        'contact': {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1-555-123-4567',
            'location': 'San Francisco, CA',
            'linkedin': 'https://linkedin.com/in/johndoe',
            'website': 'https://johndoe.dev',
        },
        'summary': 'Experienced software engineer with 10+ years in full-stack development.',
        'skills': ['Python', 'JavaScript', 'AWS', 'React', 'Node.js'],
        'highlights': [
            'Led team of 5 engineers to deliver $2M project',
            'Reduced system latency by 40%',
        ],
        'experience': [
            {
                'company': 'Tech Corp',
                'title': 'Senior Software Engineer',
                'startDate': '2020-01',
                'endDate': None,
                'current': True,
                'description': 'Leading backend development team.',
                'achievements': ['Implemented CI/CD pipeline', 'Mentored junior developers'],
            },
        ],
        'education': [
            {
                'institution': 'MIT',
                'degree': 'Bachelor of Science',
                'field': 'Computer Science',
                'graduationDate': '2014-05',
                'gpa': '3.8',
            },
        ],
        'awards': [
            {
                'title': 'Employee of the Year',
                'issuer': 'Tech Corp',
                'date': '2022-12',
                'description': 'Recognized for outstanding contributions.',
            },
        ],
    }


@pytest.fixture
def sample_job():
    """Sample job data for testing."""
    return {
        'jobid': '01234567-89ab-cdef-0123-456789abcdef',
        'jobcompany': 'Acme Inc',
        'jobtitle': 'Senior Software Engineer',
        'jobtitlesafe': 'senior-software-engineer',
        'jobdesc': 'We are looking for a senior software engineer...',
        'joblocation': 'Remote',
        'jobsalary': '$150,000 - $200,000',
        'jobposteddate': '2026-01-20',
        'joburl': 'https://acme.com/jobs/123',
        'jobtags': ['remote', 'senior', 'python'],
    }


@pytest.fixture
def sample_user_job():
    """Sample user-job relationship for testing."""
    return {
        'userid': 'user-123',
        'jobid': 'job-456',
        'resumeid': 'My Resume',
        'jobphase': 'Search',
        'datacontact': '',
        'datasummary': '',
        'dataskills': '',
        'datahighlights': '',
        'dataexperience': '',
        'dataeducation': '',
        'dataawards': '',
        'datacoverletter': '',
        'statecontact': 'ready',
        'statesummary': 'ready',
        'stateskills': 'ready',
        'statehighlights': 'ready',
        'stateexperience': 'ready',
        'stateeducation': 'ready',
        'stateawards': 'ready',
        'statecoverletter': 'ready',
        'typecontact': 'manual',
        'typesummary': 'ai',
        'typeskills': 'ai',
        'typehighlights': 'ai',
        'typeexperience': 'ai',
        'typeeducation': 'manual',
        'typeawards': 'manual',
        'typecoverletter': 'ai',
    }
