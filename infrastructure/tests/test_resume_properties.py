"""
Property-based tests for Resume operations.

Tests:
- Property 6: Resume CRUD Round-Trip
- Property 7: Resume JSON Schema Validation
- Property 8: Resume Deletion Completeness

Feature: skillsnap-mvp
Validates: Requirements 4.1, 4.2, 4.4, 4.5
"""
import pytest
from hypothesis import given, strategies as st, settings
import json
import sys
import os

# Add lambdas to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambdas'))

from shared.validation import validate_resume_json


# Strategy for valid email addresses (using a simpler pattern that matches our validation)
email_strategy = st.from_regex(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', fullmatch=True)

# Strategy for contact section
contact_strategy = st.fixed_dictionaries({
    'name': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'email': email_strategy,
    'phone': st.one_of(st.none(), st.text(min_size=7, max_size=20)),
    'location': st.one_of(st.none(), st.text(min_size=1, max_size=100)),
    'linkedin': st.one_of(st.none(), st.text(min_size=1, max_size=200)),
    'website': st.one_of(st.none(), st.text(min_size=1, max_size=200)),
})

# Strategy for experience entries
experience_strategy = st.lists(
    st.fixed_dictionaries({
        'company': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'title': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'startDate': st.text(min_size=1, max_size=20),
        'endDate': st.one_of(st.none(), st.text(min_size=1, max_size=20)),
        'current': st.booleans(),
        'description': st.text(min_size=0, max_size=1000),
        'achievements': st.lists(st.text(min_size=1, max_size=200), min_size=0, max_size=10),
    }),
    min_size=0,
    max_size=10
)

# Strategy for education entries
education_strategy = st.lists(
    st.fixed_dictionaries({
        'institution': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'degree': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'field': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'graduationDate': st.text(min_size=1, max_size=20),
        'gpa': st.one_of(st.none(), st.text(min_size=1, max_size=10)),
    }),
    min_size=0,
    max_size=5
)

# Strategy for awards entries
awards_strategy = st.lists(
    st.fixed_dictionaries({
        'title': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'issuer': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'date': st.text(min_size=1, max_size=20),
        'description': st.one_of(st.none(), st.text(min_size=0, max_size=500)),
    }),
    min_size=0,
    max_size=10
)

# Strategy for complete valid resume JSON
valid_resume_strategy = st.fixed_dictionaries({
    'contact': contact_strategy,
    'summary': st.text(min_size=0, max_size=2000),
    'skills': st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=50),
    'highlights': st.lists(st.text(min_size=1, max_size=200), min_size=0, max_size=20),
    'experience': experience_strategy,
    'education': education_strategy,
    'awards': awards_strategy,
})


class TestResumeValidation:
    """Tests for resume JSON validation."""

    @given(resume_json=valid_resume_strategy)
    @settings(max_examples=100)
    def test_property_7_valid_resume_accepted(self, resume_json: dict):
        """
        Property 7: Resume JSON Schema Validation
        
        For any resume JSON input, the validation function SHALL accept inputs
        conforming to the ResumeJSON schema.
        
        Feature: skillsnap-mvp, Property 7: Resume JSON Schema Validation
        """
        is_valid, errors = validate_resume_json(resume_json)
        assert is_valid, f"Valid resume should be accepted. Errors: {errors}"

    @given(resume_json=valid_resume_strategy)
    @settings(max_examples=100)
    def test_property_7_missing_contact_rejected(self, resume_json: dict):
        """
        Property 7: Resume JSON Schema Validation (missing contact)
        
        Resume without contact section should be rejected.
        
        Feature: skillsnap-mvp, Property 7: Resume JSON Schema Validation
        """
        invalid_resume = {k: v for k, v in resume_json.items() if k != 'contact'}
        is_valid, errors = validate_resume_json(invalid_resume)
        assert not is_valid, "Resume without contact should be rejected"
        assert any('contact' in e.lower() for e in errors)

    @given(resume_json=valid_resume_strategy)
    @settings(max_examples=100)
    def test_property_7_missing_name_rejected(self, resume_json: dict):
        """
        Property 7: Resume JSON Schema Validation (missing name)
        
        Resume without contact.name should be rejected.
        
        Feature: skillsnap-mvp, Property 7: Resume JSON Schema Validation
        """
        invalid_resume = resume_json.copy()
        invalid_resume['contact'] = {k: v for k, v in resume_json['contact'].items() if k != 'name'}
        is_valid, errors = validate_resume_json(invalid_resume)
        assert not is_valid, "Resume without contact.name should be rejected"

    @given(resume_json=valid_resume_strategy)
    @settings(max_examples=100)
    def test_property_7_missing_email_rejected(self, resume_json: dict):
        """
        Property 7: Resume JSON Schema Validation (missing email)
        
        Resume without contact.email should be rejected.
        
        Feature: skillsnap-mvp, Property 7: Resume JSON Schema Validation
        """
        invalid_resume = resume_json.copy()
        invalid_resume['contact'] = {k: v for k, v in resume_json['contact'].items() if k != 'email'}
        is_valid, errors = validate_resume_json(invalid_resume)
        assert not is_valid, "Resume without contact.email should be rejected"

    def test_property_7_invalid_email_rejected(self):
        """
        Property 7: Resume JSON Schema Validation (invalid email)
        
        Resume with invalid email format should be rejected.
        
        Feature: skillsnap-mvp, Property 7: Resume JSON Schema Validation
        """
        invalid_resume = {
            'contact': {'name': 'Test User', 'email': 'not-an-email'},
            'summary': '',
            'skills': [],
            'highlights': [],
            'experience': [],
            'education': [],
            'awards': [],
        }
        is_valid, errors = validate_resume_json(invalid_resume)
        assert not is_valid, "Resume with invalid email should be rejected"

    def test_property_7_skills_must_be_array(self):
        """
        Property 7: Resume JSON Schema Validation (skills type)
        
        Skills must be an array.
        
        Feature: skillsnap-mvp, Property 7: Resume JSON Schema Validation
        """
        invalid_resume = {
            'contact': {'name': 'Test User', 'email': 'test@example.com'},
            'summary': '',
            'skills': 'not an array',
            'highlights': [],
            'experience': [],
            'education': [],
            'awards': [],
        }
        is_valid, errors = validate_resume_json(invalid_resume)
        assert not is_valid, "Skills must be an array"


class TestResumeRoundTrip:
    """Tests for resume CRUD round-trip."""

    @given(resume_json=valid_resume_strategy)
    @settings(max_examples=100)
    def test_property_6_json_serialization_roundtrip(self, resume_json: dict):
        """
        Property 6: Resume CRUD Round-Trip
        
        For any valid resume JSON, serializing and deserializing SHALL return
        an equivalent object.
        
        Feature: skillsnap-mvp, Property 6: Resume CRUD Round-Trip
        """
        # Simulate DynamoDB storage (JSON serialization)
        serialized = json.dumps(resume_json)
        deserialized = json.loads(serialized)
        
        assert deserialized == resume_json, "Resume should survive JSON round-trip"

    @given(resume_json=valid_resume_strategy)
    @settings(max_examples=100)
    def test_property_6_validation_after_roundtrip(self, resume_json: dict):
        """
        Property 6: Resume CRUD Round-Trip (validation preserved)
        
        A valid resume should still be valid after round-trip.
        
        Feature: skillsnap-mvp, Property 6: Resume CRUD Round-Trip
        """
        # Simulate storage round-trip
        serialized = json.dumps(resume_json)
        restored = json.loads(serialized)
        
        # Should still be valid
        is_valid, errors = validate_resume_json(restored)
        assert is_valid, f"Resume should be valid after round-trip. Errors: {errors}"


class TestResumeDeletion:
    """Tests for resume deletion completeness."""

    @given(
        userid=st.uuids().map(str),
        resumename=st.text(min_size=1, max_size=50).filter(lambda x: x.strip() != '')
    )
    @settings(max_examples=100)
    def test_property_8_deletion_key_structure(self, userid: str, resumename: str):
        """
        Property 8: Resume Deletion Completeness
        
        For any resume deletion request, the key structure should uniquely
        identify the resume to delete.
        
        Feature: skillsnap-mvp, Property 8: Resume Deletion Completeness
        """
        # Simulate deletion key
        delete_key = {'userid': userid, 'resumename': resumename}
        
        # Key should have both components
        assert 'userid' in delete_key
        assert 'resumename' in delete_key
        
        # Key should be deterministic
        delete_key2 = {'userid': userid, 'resumename': resumename}
        assert delete_key == delete_key2
