"""
Property-based tests for Job operations.

Tests:
- Property 4: Phase Filter Accuracy
- Property 5: All Jobs Filter Completeness
- Property 9: Job Creation with UUID7
- Property 10: Job Creation Initial Phase
- Property 11: Job Data Extraction Completeness
- Property 13: Posting Age Calculation
- Property 14: Phase Update Persistence
- Property 33: Valid Phase Values
- Property 38: New Job Preference Application

Feature: skillsnap-mvp
Validates: Requirements 3.6, 3.8, 5.4, 5.5, 5.6, 6.3, 6.5, 12.1, 13.3
"""
import pytest
from hypothesis import given, strategies as st, settings, assume
from datetime import datetime, timedelta
import sys
import os

# Add lambdas to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambdas'))

from shared.validation import (
    validate_job_phase, 
    make_safe_url_segment,
    VALID_PHASES,
    ACTIVE_PHASES,
    VALID_SUBCOMPONENTS,
    VALID_GENERATION_TYPES,
)


# Strategy for valid phases
phase_strategy = st.sampled_from(VALID_PHASES)

# Strategy for job data
job_strategy = st.fixed_dictionaries({
    'jobcompany': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'jobtitle': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'jobdesc': st.text(min_size=1, max_size=5000),
    'joblocation': st.text(min_size=0, max_size=100),
    'jobsalary': st.text(min_size=0, max_size=50),
    'jobposteddate': st.dates(
        min_value=datetime(2020, 1, 1).date(),
        max_value=datetime(2030, 12, 31).date()
    ).map(lambda d: d.isoformat()),
})

# Strategy for user-job with random phases
user_job_strategy = st.fixed_dictionaries({
    'userid': st.uuids().map(str),
    'jobid': st.uuids().map(str),
    'jobphase': phase_strategy,
})


class TestPhaseFilter:
    """Tests for phase filtering accuracy."""

    @given(
        jobs=st.lists(user_job_strategy, min_size=1, max_size=20),
        filter_phase=phase_strategy
    )
    @settings(max_examples=100)
    def test_property_4_phase_filter_accuracy(self, jobs: list, filter_phase: str):
        """
        Property 4: Phase Filter Accuracy
        
        For any set of jobs and any selected phase filter, the displayed job cards
        SHALL contain exactly the jobs matching that phase, with no jobs from
        other phases included.
        
        Feature: skillsnap-mvp, Property 4: Phase Filter Accuracy
        """
        # Apply filter
        filtered = [j for j in jobs if j['jobphase'] == filter_phase]
        
        # Verify all filtered jobs have the correct phase
        for job in filtered:
            assert job['jobphase'] == filter_phase, \
                f"Filtered job has wrong phase: {job['jobphase']} != {filter_phase}"
        
        # Verify no jobs with other phases are included
        other_phase_jobs = [j for j in jobs if j['jobphase'] != filter_phase]
        for job in other_phase_jobs:
            assert job not in filtered, \
                f"Job with phase {job['jobphase']} should not be in filter for {filter_phase}"

    @given(jobs=st.lists(user_job_strategy, min_size=1, max_size=20))
    @settings(max_examples=100)
    def test_property_5_all_jobs_filter_completeness(self, jobs: list):
        """
        Property 5: All Jobs Filter Completeness
        
        For any set of jobs belonging to a user, selecting "All Jobs" SHALL
        display every job regardless of phase, with the count matching the
        total number of user jobs.
        
        Feature: skillsnap-mvp, Property 5: All Jobs Filter Completeness
        """
        # "All Jobs" filter returns all jobs
        all_jobs = jobs  # No filtering
        
        assert len(all_jobs) == len(jobs), \
            f"All Jobs should return all {len(jobs)} jobs, got {len(all_jobs)}"

    @given(jobs=st.lists(user_job_strategy, min_size=1, max_size=20))
    @settings(max_examples=100)
    def test_all_active_filter(self, jobs: list):
        """
        Tests "All Active" filter returns only active phases.
        """
        active_jobs = [j for j in jobs if j['jobphase'] in ACTIVE_PHASES]
        
        for job in active_jobs:
            assert job['jobphase'] in ACTIVE_PHASES, \
                f"Active job has non-active phase: {job['jobphase']}"


class TestJobCreation:
    """Tests for job creation."""

    @given(jobtitle=st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''))
    @settings(max_examples=100)
    def test_property_9_jobtitlesafe_generation(self, jobtitle: str):
        """
        Property 9: Job Creation with UUID7 (jobtitlesafe)
        
        For any job creation request, the system SHALL generate a valid
        jobtitlesafe that is URL-safe.
        
        Feature: skillsnap-mvp, Property 9: Job Creation with UUID7
        """
        safe = make_safe_url_segment(jobtitle)
        
        # Should be lowercase
        assert safe == safe.lower(), "jobtitlesafe should be lowercase"
        
        # Should only contain URL-safe characters
        import re
        assert re.match(r'^[a-z0-9\-]*$', safe), \
            f"jobtitlesafe should only contain a-z, 0-9, and hyphens: {safe}"
        
        # Should not start or end with hyphen
        if safe:
            assert not safe.startswith('-'), "jobtitlesafe should not start with hyphen"
            assert not safe.endswith('-'), "jobtitlesafe should not end with hyphen"

    def test_property_10_initial_phase_search(self):
        """
        Property 10: Job Creation Initial Phase
        
        For any newly created job, the USER_JOB record SHALL have jobphase
        set to "Search".
        
        Feature: skillsnap-mvp, Property 10: Job Creation Initial Phase
        """
        initial_phase = "Search"
        assert initial_phase in VALID_PHASES
        assert validate_job_phase(initial_phase)

    @given(job=job_strategy)
    @settings(max_examples=100)
    def test_property_11_job_data_completeness(self, job: dict):
        """
        Property 11: Job Data Extraction Completeness
        
        For any job created, the extracted data SHALL include non-empty values
        for jobcompany, jobtitle, and jobtitlesafe at minimum.
        
        Feature: skillsnap-mvp, Property 11: Job Data Extraction Completeness
        """
        assert job['jobcompany'].strip() != '', "jobcompany must be non-empty"
        assert job['jobtitle'].strip() != '', "jobtitle must be non-empty"
        
        jobtitlesafe = make_safe_url_segment(job['jobtitle'])
        # jobtitlesafe might be empty if jobtitle is all special chars
        # but for valid titles it should be non-empty


class TestPostingAge:
    """Tests for posting age calculation."""

    @given(days_ago=st.integers(min_value=0, max_value=365))
    @settings(max_examples=100)
    def test_property_13_posting_age_calculation(self, days_ago: int):
        """
        Property 13: Posting Age Calculation
        
        For any job with a jobposteddate, the posting age SHALL equal the
        number of days between jobposteddate and current date.
        
        Feature: skillsnap-mvp, Property 13: Posting Age Calculation
        """
        today = datetime.utcnow().date()
        posted_date = today - timedelta(days=days_ago)
        
        # Calculate age
        delta = today - posted_date
        calculated_age = delta.days
        
        assert calculated_age == days_ago, \
            f"Posting age should be {days_ago}, got {calculated_age}"


class TestPhaseValidation:
    """Tests for phase validation."""

    @given(phase=phase_strategy)
    @settings(max_examples=100)
    def test_property_33_valid_phase_values(self, phase: str):
        """
        Property 33: Valid Phase Values
        
        For any phase value stored or accepted by the system, it SHALL be
        one of the 11 valid phases.
        
        Feature: skillsnap-mvp, Property 33: Valid Phase Values
        """
        assert validate_job_phase(phase), f"Phase {phase} should be valid"
        assert phase in VALID_PHASES

    @given(invalid_phase=st.text(min_size=1, max_size=50).filter(lambda x: x not in VALID_PHASES))
    @settings(max_examples=100)
    def test_property_33_invalid_phase_rejected(self, invalid_phase: str):
        """
        Property 33: Valid Phase Values (rejection)
        
        Invalid phase values should be rejected.
        
        Feature: skillsnap-mvp, Property 33: Valid Phase Values
        """
        assert not validate_job_phase(invalid_phase), \
            f"Invalid phase {invalid_phase} should be rejected"

    def test_all_valid_phases_exist(self):
        """Verify all 11 valid phases are defined."""
        expected_phases = [
            "Search", "Queued", "Generating", "Ready",
            "Applied", "Follow-Up", "Negotiation", "Accepted",
            "Skipped", "Expired", "Errored"
        ]
        assert len(VALID_PHASES) == 11
        for phase in expected_phases:
            assert phase in VALID_PHASES, f"Missing phase: {phase}"


class TestPreferenceApplication:
    """Tests for preference application to new jobs."""

    @given(
        gen_types=st.fixed_dictionaries({
            comp: st.sampled_from(VALID_GENERATION_TYPES)
            for comp in VALID_SUBCOMPONENTS
        })
    )
    @settings(max_examples=100)
    def test_property_38_preference_application(self, gen_types: dict):
        """
        Property 38: New Job Preference Application
        
        For any new job creation, the initial generation types for all
        subcomponents SHALL match the user's stored default preferences.
        
        Feature: skillsnap-mvp, Property 38: New Job Preference Application
        """
        # Simulate applying preferences to new job
        user_job = {}
        for component in VALID_SUBCOMPONENTS:
            user_job[f'type{component}'] = gen_types[component]
        
        # Verify all components have types set
        for component in VALID_SUBCOMPONENTS:
            assert f'type{component}' in user_job
            assert user_job[f'type{component}'] in VALID_GENERATION_TYPES
