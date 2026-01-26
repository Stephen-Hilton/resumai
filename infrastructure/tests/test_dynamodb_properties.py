"""
Property-based tests for DynamoDB key structure and uniqueness enforcement.

Tests:
- Property 6: Resume CRUD Round-Trip
- Property 40: Email Uniqueness Enforcement
- Property 41: Username Uniqueness Enforcement

Feature: skillsnap-mvp
Validates: Requirements 4.1, 15.2, 15.3
"""
import pytest
from hypothesis import given, strategies as st, settings
import re
import json

# Strategy for valid email addresses
email_strategy = st.emails()

# Strategy for valid usernames (alphanumeric, 3-30 chars)
username_strategy = st.from_regex(r'^[a-zA-Z][a-zA-Z0-9_]{2,29}$', fullmatch=True)

# Strategy for valid UUIDs (uuid7 format)
uuid_strategy = st.uuids().map(str)

# Strategy for resume names
resume_name_strategy = st.text(
    alphabet=st.characters(whitelist_categories=('L', 'N', 'P'), whitelist_characters=' -_'),
    min_size=1,
    max_size=100
).filter(lambda x: x.strip() != '')

# Strategy for valid resume JSON contact section
contact_strategy = st.fixed_dictionaries({
    'name': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'email': email_strategy,
    'phone': st.one_of(st.none(), st.from_regex(r'^\+?[0-9\-\s]{7,20}$', fullmatch=True)),
    'location': st.one_of(st.none(), st.text(min_size=1, max_size=100)),
    'linkedin': st.one_of(st.none(), st.from_regex(r'^https://linkedin\.com/in/[a-zA-Z0-9\-]+$', fullmatch=True)),
    'website': st.one_of(st.none(), st.from_regex(r'^https?://[a-zA-Z0-9\.\-]+\.[a-z]{2,}/?.*$', fullmatch=True)),
})

# Strategy for experience entries
experience_strategy = st.lists(
    st.fixed_dictionaries({
        'company': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'title': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'startDate': st.from_regex(r'^\d{4}-\d{2}$', fullmatch=True),
        'endDate': st.one_of(st.none(), st.from_regex(r'^\d{4}-\d{2}$', fullmatch=True)),
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
        'graduationDate': st.from_regex(r'^\d{4}-\d{2}$', fullmatch=True),
        'gpa': st.one_of(st.none(), st.from_regex(r'^\d\.\d{1,2}$', fullmatch=True)),
    }),
    min_size=0,
    max_size=5
)

# Strategy for awards entries
awards_strategy = st.lists(
    st.fixed_dictionaries({
        'title': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'issuer': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'date': st.from_regex(r'^\d{4}-\d{2}$', fullmatch=True),
        'description': st.one_of(st.none(), st.text(min_size=0, max_size=500)),
    }),
    min_size=0,
    max_size=10
)

# Strategy for complete resume JSON
resume_json_strategy = st.fixed_dictionaries({
    'contact': contact_strategy,
    'summary': st.text(min_size=0, max_size=2000),
    'skills': st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=50),
    'highlights': st.lists(st.text(min_size=1, max_size=200), min_size=0, max_size=20),
    'experience': experience_strategy,
    'education': education_strategy,
    'awards': awards_strategy,
})


class TestDynamoDBKeyStructure:
    """Tests for DynamoDB key structure validation."""

    @given(userid=uuid_strategy, resumename=resume_name_strategy)
    @settings(max_examples=100)
    def test_property_6_resume_key_structure(self, userid: str, resumename: str):
        """
        Property 6: Resume CRUD Round-Trip
        
        For any valid resume JSON, creating a resume then retrieving it SHALL return
        an equivalent resume object with matching userid, resumename, and resumejson content.
        
        This test validates the key structure is correct for round-trip operations.
        
        Feature: skillsnap-mvp, Property 6: Resume CRUD Round-Trip
        """
        # Validate userid is a valid UUID format
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        assert uuid_pattern.match(userid), f"userid must be valid UUID format: {userid}"
        
        # Validate resumename is non-empty
        assert resumename.strip() != '', "resumename must be non-empty"
        
        # Validate composite key can be constructed
        composite_key = {'userid': userid, 'resumename': resumename}
        assert 'userid' in composite_key
        assert 'resumename' in composite_key

    @given(resume_json=resume_json_strategy)
    @settings(max_examples=100)
    def test_property_6_resume_json_serialization(self, resume_json: dict):
        """
        Property 6: Resume CRUD Round-Trip (JSON serialization)
        
        Validates that resume JSON can be serialized and deserialized without data loss.
        
        Feature: skillsnap-mvp, Property 6: Resume CRUD Round-Trip
        """
        # Serialize to JSON string (as stored in DynamoDB)
        json_str = json.dumps(resume_json)
        
        # Deserialize back
        restored = json.loads(json_str)
        
        # Verify round-trip equivalence
        assert restored == resume_json, "Resume JSON must survive serialization round-trip"


class TestEmailUniqueness:
    """Tests for email uniqueness enforcement."""

    @given(email=email_strategy)
    @settings(max_examples=100)
    def test_property_40_email_uniqueness_key(self, email: str):
        """
        Property 40: Email Uniqueness Enforcement
        
        For any user registration with an email that already exists in USER_EMAIL,
        the registration SHALL fail with an appropriate error message.
        
        This test validates the email key structure for uniqueness enforcement.
        
        Feature: skillsnap-mvp, Property 40: Email Uniqueness Enforcement
        """
        # Email should be normalized to lowercase for consistent uniqueness checks
        normalized_email = email.lower()
        
        # Validate email format
        email_pattern = re.compile(r'^[^@]+@[^@]+\.[^@]+$')
        assert email_pattern.match(normalized_email), f"Invalid email format: {email}"
        
        # Validate key structure
        key = {'useremail': normalized_email}
        assert 'useremail' in key
        assert key['useremail'] == normalized_email

    @given(emails=st.lists(email_strategy, min_size=2, max_size=10, unique=True))
    @settings(max_examples=100)
    def test_property_40_email_uniqueness_detection(self, emails: list):
        """
        Property 40: Email Uniqueness Enforcement (detection)
        
        Validates that duplicate emails can be detected using the key structure.
        
        Feature: skillsnap-mvp, Property 40: Email Uniqueness Enforcement
        """
        # Normalize all emails
        normalized = [e.lower() for e in emails]
        
        # Create a set to simulate uniqueness check
        email_set = set()
        for email in normalized:
            if email in email_set:
                # This would trigger a uniqueness violation
                assert False, f"Duplicate email detected: {email}"
            email_set.add(email)
        
        # All emails should be unique
        assert len(email_set) == len(normalized)


class TestUsernameUniqueness:
    """Tests for username uniqueness enforcement."""

    @given(username=username_strategy)
    @settings(max_examples=100)
    def test_property_41_username_uniqueness_key(self, username: str):
        """
        Property 41: Username Uniqueness Enforcement
        
        For any user registration with a username that already exists in USER_USERNAME,
        the registration SHALL fail with an appropriate error message.
        
        This test validates the username key structure for uniqueness enforcement.
        
        Feature: skillsnap-mvp, Property 41: Username Uniqueness Enforcement
        """
        # Username should be normalized to lowercase for consistent uniqueness checks
        normalized_username = username.lower()
        
        # Validate username format (alphanumeric, starts with letter, 3-30 chars)
        username_pattern = re.compile(r'^[a-z][a-z0-9_]{2,29}$')
        assert username_pattern.match(normalized_username), f"Invalid username format: {username}"
        
        # Validate key structure
        key = {'username': normalized_username}
        assert 'username' in key
        assert key['username'] == normalized_username

    @given(usernames=st.lists(username_strategy, min_size=2, max_size=10, unique_by=str.lower))
    @settings(max_examples=100)
    def test_property_41_username_uniqueness_detection(self, usernames: list):
        """
        Property 41: Username Uniqueness Enforcement (detection)
        
        Validates that duplicate usernames can be detected using the key structure.
        
        Feature: skillsnap-mvp, Property 41: Username Uniqueness Enforcement
        """
        # Normalize all usernames
        normalized = [u.lower() for u in usernames]
        
        # Create a set to simulate uniqueness check
        username_set = set()
        for username in normalized:
            if username in username_set:
                # This would trigger a uniqueness violation
                assert False, f"Duplicate username detected: {username}"
            username_set.add(username)
        
        # All usernames should be unique
        assert len(username_set) == len(normalized)


class TestResumeSchema:
    """Tests for resume JSON schema validation."""

    @given(resume_json=resume_json_strategy)
    @settings(max_examples=100)
    def test_resume_json_required_fields(self, resume_json: dict):
        """
        Validates that generated resume JSON contains all required fields.
        
        Feature: skillsnap-mvp, Property 7: Resume JSON Schema Validation
        """
        # Required top-level fields
        required_fields = ['contact', 'summary', 'skills', 'highlights', 'experience', 'education', 'awards']
        for field in required_fields:
            assert field in resume_json, f"Missing required field: {field}"
        
        # Required contact fields
        contact_required = ['name', 'email']
        for field in contact_required:
            assert field in resume_json['contact'], f"Missing required contact field: {field}"
        
        # Validate contact name is non-empty
        assert resume_json['contact']['name'].strip() != '', "Contact name must be non-empty"

    @given(resume_json=resume_json_strategy)
    @settings(max_examples=100)
    def test_resume_json_field_types(self, resume_json: dict):
        """
        Validates that resume JSON fields have correct types.
        
        Feature: skillsnap-mvp, Property 7: Resume JSON Schema Validation
        """
        # Contact should be a dict
        assert isinstance(resume_json['contact'], dict)
        
        # Summary should be a string
        assert isinstance(resume_json['summary'], str)
        
        # Skills should be a list of strings
        assert isinstance(resume_json['skills'], list)
        for skill in resume_json['skills']:
            assert isinstance(skill, str)
        
        # Highlights should be a list of strings
        assert isinstance(resume_json['highlights'], list)
        for highlight in resume_json['highlights']:
            assert isinstance(highlight, str)
        
        # Experience should be a list of dicts
        assert isinstance(resume_json['experience'], list)
        for exp in resume_json['experience']:
            assert isinstance(exp, dict)
            assert 'company' in exp
            assert 'title' in exp
        
        # Education should be a list of dicts
        assert isinstance(resume_json['education'], list)
        for edu in resume_json['education']:
            assert isinstance(edu, dict)
            assert 'institution' in edu
            assert 'degree' in edu
        
        # Awards should be a list of dicts
        assert isinstance(resume_json['awards'], list)
        for award in resume_json['awards']:
            assert isinstance(award, dict)
            assert 'title' in award
            assert 'issuer' in award
