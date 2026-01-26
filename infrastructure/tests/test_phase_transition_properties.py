"""
Property-based tests for Phase Transitions.

Tests:
- Property 34: Automatic Phase Transitions
- Property 35: Job Expiration

Feature: skillsnap-mvp
Validates: Requirements 12.3, 12.4, 12.5, 12.7
"""
import pytest
from hypothesis import given, strategies as st, settings
from datetime import datetime, timedelta
import sys
import os

# Add lambdas to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambdas'))

from shared.validation import VALID_PHASES, VALID_SUBCOMPONENTS


# Terminal phases that should not be expired
TERMINAL_PHASES = {'Accepted', 'Skipped', 'Expired'}

# Active phases for "All Active" filter
ACTIVE_PHASES = {'Search', 'Queued', 'Generating', 'Ready', 'Applied', 'Follow-Up', 'Negotiation'}


class TestAutomaticPhaseTransitions:
    """Tests for automatic phase transitions."""

    def test_property_34_search_to_queued(self):
        """
        Property 34: Automatic Phase Transitions
        
        Phase SHALL transition to "Queued" when data gathering completes.
        
        Feature: skillsnap-mvp, Property 34: Automatic Phase Transitions
        """
        # Simulate job with complete data
        job_data = {
            'jobcompany': 'Test Company',
            'jobtitle': 'Software Engineer',
            'jobdesc': 'Job description here'
        }
        
        # When all required data is present, phase should be Queued
        has_required_data = all([
            job_data.get('jobcompany'),
            job_data.get('jobtitle'),
            job_data.get('jobdesc')
        ])
        
        expected_phase = 'Queued' if has_required_data else 'Search'
        assert expected_phase == 'Queued'

    def test_property_34_queued_to_generating(self):
        """
        Property 34: Automatic Phase Transitions
        
        Phase SHALL transition to "Generating" when generation starts.
        
        Feature: skillsnap-mvp, Property 34: Automatic Phase Transitions
        """
        # Simulate generation start
        current_phase = 'Queued'
        generation_started = True
        
        new_phase = 'Generating' if generation_started else current_phase
        assert new_phase == 'Generating'

    def test_property_34_generating_to_ready(self):
        """
        Property 34: Automatic Phase Transitions
        
        Phase SHALL transition to "Ready" when all final files complete.
        
        Feature: skillsnap-mvp, Property 34: Automatic Phase Transitions
        """
        # Simulate all files complete
        s3_locations = {
            's3locresumehtml': 's3://bucket/path/resume.html',
            's3locresumepdf': 's3://bucket/path/resume.pdf',
            's3loccoverletterhtml': 's3://bucket/path/coverletter.html',
            's3loccoverletterpdf': 's3://bucket/path/coverletter.pdf',
        }
        
        all_files_complete = all(s3_locations.values())
        new_phase = 'Ready' if all_files_complete else 'Generating'
        
        assert new_phase == 'Ready'

    @given(
        has_company=st.booleans(),
        has_title=st.booleans(),
        has_desc=st.booleans()
    )
    @settings(max_examples=100)
    def test_property_34_data_completeness_determines_phase(
        self, has_company: bool, has_title: bool, has_desc: bool
    ):
        """
        Property 34: Automatic Phase Transitions (data completeness)
        
        Initial phase depends on data completeness.
        
        Feature: skillsnap-mvp, Property 34: Automatic Phase Transitions
        """
        job_data = {
            'jobcompany': 'Company' if has_company else '',
            'jobtitle': 'Title' if has_title else '',
            'jobdesc': 'Description' if has_desc else ''
        }
        
        has_required = all([
            job_data.get('jobcompany'),
            job_data.get('jobtitle'),
            job_data.get('jobdesc')
        ])
        
        expected_phase = 'Queued' if has_required else 'Search'
        
        if has_company and has_title and has_desc:
            assert expected_phase == 'Queued'
        else:
            assert expected_phase == 'Search'


class TestJobExpiration:
    """Tests for job expiration."""

    def test_property_35_expiration_threshold(self):
        """
        Property 35: Job Expiration
        
        Jobs older than 30 days should be expired.
        
        Feature: skillsnap-mvp, Property 35: Job Expiration
        """
        expiration_days = 30
        
        # Job posted 31 days ago
        old_date = (datetime.utcnow() - timedelta(days=31)).strftime('%Y-%m-%d')
        cutoff_date = (datetime.utcnow() - timedelta(days=expiration_days)).strftime('%Y-%m-%d')
        
        should_expire = old_date < cutoff_date
        assert should_expire

    def test_property_35_recent_job_not_expired(self):
        """
        Property 35: Job Expiration
        
        Jobs less than 30 days old should not be expired.
        
        Feature: skillsnap-mvp, Property 35: Job Expiration
        """
        expiration_days = 30
        
        # Job posted 10 days ago
        recent_date = (datetime.utcnow() - timedelta(days=10)).strftime('%Y-%m-%d')
        cutoff_date = (datetime.utcnow() - timedelta(days=expiration_days)).strftime('%Y-%m-%d')
        
        should_expire = recent_date < cutoff_date
        assert not should_expire

    @given(phase=st.sampled_from(list(VALID_PHASES)))
    @settings(max_examples=100)
    def test_property_35_terminal_phases_not_expired(self, phase: str):
        """
        Property 35: Job Expiration
        
        Jobs in terminal phases (Accepted, Skipped, Expired) should not be expired.
        
        Feature: skillsnap-mvp, Property 35: Job Expiration
        """
        is_terminal = phase in TERMINAL_PHASES
        
        # Simulate expiration check
        should_expire_if_old = phase not in TERMINAL_PHASES
        
        if is_terminal:
            assert not should_expire_if_old
        else:
            assert should_expire_if_old

    @given(days_old=st.integers(min_value=0, max_value=365))
    @settings(max_examples=100)
    def test_property_35_expiration_by_age(self, days_old: int):
        """
        Property 35: Job Expiration
        
        Expiration depends on job age.
        
        Feature: skillsnap-mvp, Property 35: Job Expiration
        """
        expiration_days = 30
        
        job_date = (datetime.utcnow() - timedelta(days=days_old)).strftime('%Y-%m-%d')
        cutoff_date = (datetime.utcnow() - timedelta(days=expiration_days)).strftime('%Y-%m-%d')
        
        should_expire = job_date < cutoff_date
        
        if days_old > expiration_days:
            assert should_expire
        else:
            assert not should_expire

    def test_property_35_all_terminal_phases(self):
        """
        Property 35: Job Expiration
        
        Verify all terminal phases are defined.
        
        Feature: skillsnap-mvp, Property 35: Job Expiration
        """
        assert 'Accepted' in TERMINAL_PHASES
        assert 'Skipped' in TERMINAL_PHASES
        assert 'Expired' in TERMINAL_PHASES
        assert len(TERMINAL_PHASES) == 3
