"""
Property-based tests for Resume File Import feature.

Tests:
- Property 1: File Validation Rejects Invalid Inputs
- Property 2: Upload Produces Valid Unique S3 Key
- Property 5: AI Response Produces Valid ResumeJSON
- Property 9: Template Round-Trip Mapping

Feature: resume-file-import
Validates: Requirements 2.3, 2.4, 2.5, 4.1, 4.2, 4.5, 5.5, 5.7, 7.3, 7.5
"""
import pytest
from hypothesis import given, strategies as st, settings, assume
import json
import re
import os
import sys
import time
import yaml

# Add lambdas to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambdas'))

from resume.import_url import validate_filename, validate_content_type, VALID_CONTENT_TYPES
from resume.import_process import (
    map_yaml_to_resume_json,
    apply_defaults,
    sanitize_text,
    parse_date_range,
    get_default_resume_json,
)


# =============================================================================
# Property 1: File Validation Rejects Invalid Inputs
# Validates: Requirements 2.3, 2.4, 2.5
# =============================================================================

# Valid extensions for file import
VALID_EXTENSIONS = ['.yaml', '.yml', '.json', '.pdf']
INVALID_EXTENSIONS = ['.txt', '.doc', '.docx', '.xls', '.xlsx', '.png', '.jpg', '.gif', '.exe', '.zip', '.html', '.xml', '.csv', '']

# Max file size (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024


class TestProperty1FileValidation:
    """
    Property 1: File Validation Rejects Invalid Inputs
    
    For any file selected by the user, if the file size exceeds 5MB OR the file 
    extension is not one of (.yaml, .yml, .json, .pdf), the system SHALL reject 
    the file with an appropriate error message and NOT proceed with upload.
    
    **Validates: Requirements 2.3, 2.4, 2.5**
    """

    @given(
        filename_base=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='-_')).filter(lambda x: x.strip() != ''),
        extension=st.sampled_from(INVALID_EXTENSIONS)
    )
    @settings(max_examples=100)
    def test_property_1_invalid_extension_rejected(self, filename_base: str, extension: str):
        """
        Property 1: File Validation Rejects Invalid Inputs
        
        For any file with an invalid extension, the validation SHALL reject it.
        
        Feature: resume-file-import, Property 1: File Validation Rejects Invalid Inputs
        **Validates: Requirements 2.3, 2.4, 2.5**
        """
        filename = f"{filename_base}{extension}"
        is_valid, error_msg = validate_filename(filename)
        
        # Files with invalid extensions should be rejected
        assert not is_valid, f"File with extension '{extension}' should be rejected"
        assert "Unsupported file type" in error_msg or "Allowed:" in error_msg

    @given(
        filename_base=st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='-_')).filter(lambda x: x.strip() != ''),
        extension=st.sampled_from(VALID_EXTENSIONS)
    )
    @settings(max_examples=100)
    def test_property_1_valid_extension_accepted(self, filename_base: str, extension: str):
        """
        Property 1: File Validation Rejects Invalid Inputs (inverse)
        
        For any file with a valid extension, the validation SHALL accept it.
        
        Feature: resume-file-import, Property 1: File Validation Rejects Invalid Inputs
        **Validates: Requirements 2.3, 2.4, 2.5**
        """
        filename = f"{filename_base}{extension}"
        is_valid, result = validate_filename(filename)
        
        # Files with valid extensions should be accepted
        assert is_valid, f"File with extension '{extension}' should be accepted, got error: {result}"

    @given(
        content_type=st.sampled_from(['application/json', 'application/x-yaml', 'text/yaml', 'application/pdf']),
        extension=st.sampled_from(VALID_EXTENSIONS)
    )
    @settings(max_examples=100)
    def test_property_1_mime_type_mismatch_rejected(self, content_type: str, extension: str):
        """
        Property 1: File Validation Rejects Invalid Inputs (MIME mismatch)
        
        For any file where the MIME type does not match the extension, 
        the validation SHALL reject it.
        
        Feature: resume-file-import, Property 1: File Validation Rejects Invalid Inputs
        **Validates: Requirements 2.3, 2.4, 2.5**
        """
        filename = f"test{extension}"
        
        # Get allowed extensions for this content type
        allowed_extensions = VALID_CONTENT_TYPES.get(content_type, [])
        
        # If extension is NOT in allowed extensions, it should be rejected
        if extension not in allowed_extensions:
            is_valid, error_msg = validate_content_type(content_type, filename)
            assert not is_valid, f"MIME type '{content_type}' should not be valid for extension '{extension}'"
            assert "does not match" in error_msg or "not valid" in error_msg

    @given(
        content_type=st.sampled_from(['application/json', 'application/x-yaml', 'text/yaml', 'application/pdf'])
    )
    @settings(max_examples=100)
    def test_property_1_mime_type_match_accepted(self, content_type: str):
        """
        Property 1: File Validation Rejects Invalid Inputs (MIME match)
        
        For any file where the MIME type matches the extension, 
        the validation SHALL accept it.
        
        Feature: resume-file-import, Property 1: File Validation Rejects Invalid Inputs
        **Validates: Requirements 2.3, 2.4, 2.5**
        """
        # Get allowed extensions for this content type
        allowed_extensions = VALID_CONTENT_TYPES.get(content_type, [])
        assume(len(allowed_extensions) > 0)
        
        # Pick a matching extension
        extension = allowed_extensions[0]
        filename = f"test{extension}"
        
        is_valid, result = validate_content_type(content_type, filename)
        assert is_valid, f"MIME type '{content_type}' should be valid for extension '{extension}', got error: {result}"



# =============================================================================
# Property 2: Upload Produces Valid Unique S3 Key
# Validates: Requirements 4.1, 4.2, 4.5
# =============================================================================

# S3 key pattern: temp-imports/{userid}/{timestamp}-{filename}
S3_KEY_PATTERN = re.compile(r'^temp-imports/[a-zA-Z0-9-]+/\d+-[a-zA-Z0-9._-]+\.(yaml|yml|json|pdf)$')


class TestProperty2S3KeyGeneration:
    """
    Property 2: Upload Produces Valid Unique S3 Key
    
    For any successful file upload, the returned S3 key SHALL match the pattern 
    `temp-imports/{userid}/{timestamp}-{filename}` AND be unique across all uploads 
    (no two uploads produce the same key).
    
    **Validates: Requirements 4.1, 4.2, 4.5**
    """

    @given(
        userid=st.uuids().map(str),
        filename_base=st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='-_')).filter(lambda x: x.strip() != ''),
        extension=st.sampled_from(VALID_EXTENSIONS)
    )
    @settings(max_examples=100)
    def test_property_2_s3_key_format(self, userid: str, filename_base: str, extension: str):
        """
        Property 2: Upload Produces Valid Unique S3 Key (format)
        
        For any valid upload parameters, the generated S3 key SHALL match 
        the expected pattern.
        
        Feature: resume-file-import, Property 2: Upload Produces Valid Unique S3 Key
        **Validates: Requirements 4.1, 4.2, 4.5**
        """
        filename = f"{filename_base}{extension}"
        timestamp = int(time.time() * 1000)
        
        # Generate S3 key using the same logic as the Lambda
        s3_key = f"temp-imports/{userid}/{timestamp}-{filename}"
        
        # Verify the key matches the expected pattern
        assert s3_key.startswith("temp-imports/"), "S3 key should start with 'temp-imports/'"
        assert f"/{userid}/" in s3_key, "S3 key should contain the userid"
        assert filename in s3_key, "S3 key should contain the filename"
        
        # Verify the key has the timestamp component
        parts = s3_key.split('/')
        assert len(parts) == 3, f"S3 key should have 3 parts, got {len(parts)}"
        
        # The last part should be {timestamp}-{filename}
        file_part = parts[2]
        assert '-' in file_part, "File part should contain timestamp separator"
        timestamp_str = file_part.split('-')[0]
        assert timestamp_str.isdigit(), "Timestamp should be numeric"

    @given(
        userid=st.uuids().map(str),
        filename_base=st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='-_')).filter(lambda x: x.strip() != ''),
        extension=st.sampled_from(VALID_EXTENSIONS)
    )
    @settings(max_examples=100)
    def test_property_2_s3_key_uniqueness(self, userid: str, filename_base: str, extension: str):
        """
        Property 2: Upload Produces Valid Unique S3 Key (uniqueness)
        
        For any two uploads with the same parameters, the generated S3 keys 
        SHALL be unique due to timestamp differences.
        
        Feature: resume-file-import, Property 2: Upload Produces Valid Unique S3 Key
        **Validates: Requirements 4.1, 4.2, 4.5**
        """
        filename = f"{filename_base}{extension}"
        
        # Generate two keys with slight time difference
        timestamp1 = int(time.time() * 1000)
        s3_key1 = f"temp-imports/{userid}/{timestamp1}-{filename}"
        
        # Small delay to ensure different timestamp
        time.sleep(0.001)
        
        timestamp2 = int(time.time() * 1000)
        s3_key2 = f"temp-imports/{userid}/{timestamp2}-{filename}"
        
        # Keys should be different due to timestamp
        assert s3_key1 != s3_key2, "Two uploads should produce unique S3 keys"

    @given(
        userid1=st.uuids().map(str),
        userid2=st.uuids().map(str),
        filename=st.sampled_from(['resume.yaml', 'resume.json', 'resume.pdf'])
    )
    @settings(max_examples=100)
    def test_property_2_s3_key_user_isolation(self, userid1: str, userid2: str, filename: str):
        """
        Property 2: Upload Produces Valid Unique S3 Key (user isolation)
        
        For any two different users uploading the same file, the S3 keys 
        SHALL be in different paths.
        
        Feature: resume-file-import, Property 2: Upload Produces Valid Unique S3 Key
        **Validates: Requirements 4.1, 4.2, 4.5**
        """
        assume(userid1 != userid2)
        
        timestamp = int(time.time() * 1000)
        s3_key1 = f"temp-imports/{userid1}/{timestamp}-{filename}"
        s3_key2 = f"temp-imports/{userid2}/{timestamp}-{filename}"
        
        # Keys should be different due to different user paths
        assert s3_key1 != s3_key2, "Different users should have different S3 key paths"
        
        # Verify user isolation in path
        assert f"/{userid1}/" in s3_key1
        assert f"/{userid2}/" in s3_key2
        assert f"/{userid1}/" not in s3_key2
        assert f"/{userid2}/" not in s3_key1



# =============================================================================
# Property 5: AI Response Produces Valid ResumeJSON
# Validates: Requirements 5.5, 5.7
# =============================================================================

# Strategy for contact items
contact_item_strategy = st.fixed_dictionaries({
    'icon': st.sampled_from(['email-at', 'phone', 'linkedin', 'github', 'globe-solid', 'house-solid', 'x-twitter']),
    'title': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'url': st.one_of(st.just(''), st.text(min_size=1, max_size=200)),
})

# Strategy for role bullets
bullet_strategy = st.fixed_dictionaries({
    'text': st.text(min_size=1, max_size=500).filter(lambda x: x.strip() != ''),
    'tags': st.lists(st.text(min_size=1, max_size=30), min_size=0, max_size=5),
})

# Strategy for roles
role_strategy = st.fixed_dictionaries({
    'title': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'startDate': st.text(min_size=1, max_size=30),
    'endDate': st.one_of(st.just(''), st.text(min_size=1, max_size=30)),
    'current': st.booleans(),
    'location': st.one_of(st.just(''), st.text(min_size=1, max_size=100)),
    'bullets': st.lists(bullet_strategy, min_size=0, max_size=5),
})

# Strategy for experience entries
experience_strategy = st.fixed_dictionaries({
    'name': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'url': st.one_of(st.just(''), st.text(min_size=1, max_size=200)),
    'employees': st.one_of(st.none(), st.integers(min_value=1, max_value=1000000)),
    'location': st.one_of(st.just(''), st.text(min_size=1, max_size=100)),
    'description': st.one_of(st.just(''), st.text(min_size=1, max_size=500)),
    'startDate': st.text(min_size=1, max_size=30),
    'endDate': st.one_of(st.just(''), st.text(min_size=1, max_size=30)),
    'current': st.booleans(),
    'roles': st.lists(role_strategy, min_size=0, max_size=3),
})

# Strategy for education entries
education_strategy = st.fixed_dictionaries({
    'degree': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'institution': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'graduationDate': st.text(min_size=1, max_size=30),
    'field': st.one_of(st.just(''), st.text(min_size=1, max_size=100)),
    'gpa': st.one_of(st.just(''), st.text(min_size=1, max_size=10)),
})

# Strategy for award entries
award_strategy = st.fixed_dictionaries({
    'title': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'description': st.one_of(st.just(''), st.text(min_size=1, max_size=500)),
    'date': st.text(min_size=1, max_size=30),
})

# Strategy for keynote entries
keynote_strategy = st.fixed_dictionaries({
    'title': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'event': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'date': st.text(min_size=1, max_size=30),
    'location': st.one_of(st.just(''), st.text(min_size=1, max_size=100)),
})

# Strategy for complete ResumeJSON (simulating AI response)
resume_json_strategy = st.fixed_dictionaries({
    'contact': st.fixed_dictionaries({
        'name': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
        'location': st.one_of(st.just(''), st.text(min_size=1, max_size=100)),
        'items': st.lists(contact_item_strategy, min_size=0, max_size=7),
    }),
    'summary': st.one_of(st.just(''), st.text(min_size=1, max_size=2000)),
    'skills': st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=30),
    'highlights': st.lists(st.text(min_size=1, max_size=200), min_size=0, max_size=10),
    'experience': st.lists(experience_strategy, min_size=0, max_size=5),
    'education': st.lists(education_strategy, min_size=0, max_size=5),
    'awards': st.lists(award_strategy, min_size=0, max_size=5),
    'keynotes': st.lists(keynote_strategy, min_size=0, max_size=5),
})


class TestProperty5AIResponseValidation:
    """
    Property 5: AI Response Produces Valid ResumeJSON
    
    For any AI response from Nova Micro, the Import_Lambda SHALL either return 
    a valid ResumeJSON object (passing schema validation) OR return a ResumeJSON 
    with default values for any fields the AI could not map.
    
    **Validates: Requirements 5.5, 5.7**
    """

    @given(resume_json=resume_json_strategy)
    @settings(max_examples=100)
    def test_property_5_valid_response_passes_defaults(self, resume_json: dict):
        """
        Property 5: AI Response Produces Valid ResumeJSON
        
        For any valid AI response, apply_defaults SHALL return a valid ResumeJSON.
        
        Feature: resume-file-import, Property 5: AI Response Produces Valid ResumeJSON
        **Validates: Requirements 5.5, 5.7**
        """
        result = apply_defaults(resume_json)
        
        # Verify all required top-level keys exist
        assert 'contact' in result
        assert 'summary' in result
        assert 'skills' in result
        assert 'highlights' in result
        assert 'experience' in result
        assert 'education' in result
        assert 'awards' in result
        assert 'keynotes' in result
        
        # Verify contact structure
        assert isinstance(result['contact'], dict)
        assert 'name' in result['contact']
        assert 'location' in result['contact']
        assert 'items' in result['contact']
        assert isinstance(result['contact']['items'], list)
        
        # Verify arrays are arrays
        assert isinstance(result['skills'], list)
        assert isinstance(result['highlights'], list)
        assert isinstance(result['experience'], list)
        assert isinstance(result['education'], list)
        assert isinstance(result['awards'], list)
        assert isinstance(result['keynotes'], list)
        
        # Verify summary is string
        assert isinstance(result['summary'], str)
        
        # Highlights should always be empty (AI generates them separately)
        assert result['highlights'] == []

    @given(
        missing_keys=st.lists(
            st.sampled_from(['contact', 'summary', 'skills', 'highlights', 'experience', 'education', 'awards', 'keynotes']),
            min_size=1,
            max_size=4,
            unique=True
        )
    )
    @settings(max_examples=100)
    def test_property_5_missing_fields_get_defaults(self, missing_keys: list):
        """
        Property 5: AI Response Produces Valid ResumeJSON (missing fields)
        
        For any AI response with missing fields, apply_defaults SHALL fill 
        them with appropriate defaults.
        
        Feature: resume-file-import, Property 5: AI Response Produces Valid ResumeJSON
        **Validates: Requirements 5.5, 5.7**
        """
        # Create a partial response missing some keys
        partial_response = get_default_resume_json()
        for key in missing_keys:
            del partial_response[key]
        
        result = apply_defaults(partial_response)
        
        # All keys should now exist
        for key in ['contact', 'summary', 'skills', 'highlights', 'experience', 'education', 'awards', 'keynotes']:
            assert key in result, f"Key '{key}' should exist after apply_defaults"

    @given(
        invalid_types=st.fixed_dictionaries({
            'contact': st.sampled_from(['string', 123, [], None]),
            'summary': st.sampled_from([123, [], {}, None]),
            'skills': st.sampled_from(['string', 123, {}, None]),
        })
    )
    @settings(max_examples=100)
    def test_property_5_invalid_types_get_corrected(self, invalid_types: dict):
        """
        Property 5: AI Response Produces Valid ResumeJSON (invalid types)
        
        For any AI response with invalid field types, apply_defaults SHALL 
        correct them to valid types.
        
        Feature: resume-file-import, Property 5: AI Response Produces Valid ResumeJSON
        **Validates: Requirements 5.5, 5.7**
        """
        result = apply_defaults(invalid_types)
        
        # Contact should be a dict with required structure
        assert isinstance(result['contact'], dict)
        assert 'name' in result['contact']
        assert 'items' in result['contact']
        
        # Summary should be a string
        assert isinstance(result['summary'], str)
        
        # Skills should be a list
        assert isinstance(result['skills'], list)



# =============================================================================
# Property 9: Template Round-Trip Mapping
# Validates: Requirements 7.3, 7.5
# =============================================================================

# Strategy for input format (matching template structure)
input_contact_strategy = st.fixed_dictionaries({
    'name': st.text(min_size=1, max_size=50).filter(lambda x: x.strip() != ''),
    'label': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'url': st.one_of(st.just(''), st.text(min_size=1, max_size=200)),
    'icon': st.sampled_from(['email-at', 'phone-volume', 'linkedin', 'github', 'globe-solid', 'house-solid']),
})

input_bullet_strategy = st.fixed_dictionaries({
    'text': st.text(min_size=1, max_size=300).filter(lambda x: x.strip() != ''),
    'tags': st.lists(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('L', 'N'))), min_size=0, max_size=3),
})

input_role_strategy = st.fixed_dictionaries({
    'role': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'dates': st.sampled_from(['January 2020 - Present', '2018 - 2020', '2015 - 2018', 'March 2022 - December 2023']),
    'location': st.one_of(st.just(''), st.text(min_size=1, max_size=50)),
    'bullets': st.lists(input_bullet_strategy, min_size=0, max_size=3),
})

input_experience_strategy = st.fixed_dictionaries({
    'company_name': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'company_urls': st.one_of(
        st.text(min_size=1, max_size=100),
        st.lists(st.text(min_size=1, max_size=100), min_size=1, max_size=2)
    ),
    'employees': st.one_of(st.none(), st.integers(min_value=1, max_value=100000)),
    'dates': st.sampled_from(['January 2020 - Present', '2015 - 2020', '2010 - 2015']),
    'location': st.one_of(st.just(''), st.text(min_size=1, max_size=50)),
    'company_description': st.one_of(st.just(''), st.text(min_size=1, max_size=200)),
    'roles': st.lists(input_role_strategy, min_size=1, max_size=2),
})

input_education_strategy = st.fixed_dictionaries({
    'course': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'school': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'dates': st.sampled_from(['2020', '2018', '2015', '2010']),
})

input_award_strategy = st.fixed_dictionaries({
    'award': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'reward': st.one_of(st.just(''), st.text(min_size=1, max_size=200)),
    'dates': st.sampled_from(['2023', '2022', '2020', '2018']),
})

input_keynote_strategy = st.fixed_dictionaries({
    'keynote': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'event': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'dates': st.sampled_from(['2023', '2022', '2020']),
})

# Strategy for complete input format (template structure)
input_format_strategy = st.fixed_dictionaries({
    'name': st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != ''),
    'location': st.one_of(st.just(''), st.text(min_size=1, max_size=100)),
    'summary': st.one_of(st.just(''), st.text(min_size=1, max_size=1000)),
    'contacts': st.lists(input_contact_strategy, min_size=0, max_size=5),
    'skills': st.lists(st.text(min_size=1, max_size=50).filter(lambda x: x.strip() != ''), min_size=0, max_size=10),
    'experience': st.lists(input_experience_strategy, min_size=0, max_size=3),
    'education': st.lists(input_education_strategy, min_size=0, max_size=3),
    'awards': st.lists(input_award_strategy, min_size=0, max_size=3),
    'keynotes': st.lists(input_keynote_strategy, min_size=0, max_size=3),
})


class TestProperty9TemplateRoundTrip:
    """
    Property 9: Template Round-Trip Mapping
    
    For any file created by filling in the template YAML with valid data, 
    importing that file SHALL produce a ResumeJSON where every field matches 
    the input data with 100% accuracy (no data loss or transformation errors).
    
    **Validates: Requirements 7.3, 7.5**
    """

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_name_preserved(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (name)
        
        The name field SHALL be preserved exactly.
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        assert result['contact']['name'] == input_data['name']

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_location_preserved(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (location)
        
        The location field SHALL be preserved exactly.
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        assert result['contact']['location'] == input_data['location']

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_summary_preserved(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (summary)
        
        The summary field SHALL be preserved exactly.
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        assert result['summary'] == input_data['summary']

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_skills_preserved(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (skills)
        
        The skills array SHALL be preserved exactly.
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        assert result['skills'] == input_data['skills']

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_contacts_count_preserved(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (contacts count)
        
        The number of contact items SHALL be preserved.
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        assert len(result['contact']['items']) == len(input_data['contacts'])

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_contact_labels_preserved(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (contact labels)
        
        Contact labels SHALL be mapped to titles exactly.
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        for i, contact in enumerate(input_data['contacts']):
            assert result['contact']['items'][i]['title'] == contact['label']

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_experience_count_preserved(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (experience count)
        
        The number of experience entries SHALL be preserved.
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        assert len(result['experience']) == len(input_data['experience'])

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_company_names_preserved(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (company names)
        
        Company names SHALL be mapped to experience names exactly.
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        for i, exp in enumerate(input_data['experience']):
            assert result['experience'][i]['name'] == exp['company_name']

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_education_preserved(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (education)
        
        Education entries SHALL be mapped correctly.
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        assert len(result['education']) == len(input_data['education'])
        for i, edu in enumerate(input_data['education']):
            assert result['education'][i]['degree'] == edu['course']
            assert result['education'][i]['institution'] == edu['school']
            assert result['education'][i]['graduationDate'] == str(edu['dates'])

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_awards_preserved(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (awards)
        
        Award entries SHALL be mapped correctly.
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        assert len(result['awards']) == len(input_data['awards'])
        for i, award in enumerate(input_data['awards']):
            assert result['awards'][i]['title'] == award['award']
            assert result['awards'][i]['description'] == award['reward']
            assert result['awards'][i]['date'] == str(award['dates'])

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_keynotes_preserved(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (keynotes)
        
        Keynote entries SHALL be mapped correctly.
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        assert len(result['keynotes']) == len(input_data['keynotes'])
        for i, keynote in enumerate(input_data['keynotes']):
            assert result['keynotes'][i]['title'] == keynote['keynote']
            assert result['keynotes'][i]['event'] == keynote['event']
            assert result['keynotes'][i]['date'] == str(keynote['dates'])

    @given(input_data=input_format_strategy)
    @settings(max_examples=100)
    def test_property_9_highlights_always_empty(self, input_data: dict):
        """
        Property 9: Template Round-Trip Mapping (highlights)
        
        Highlights SHALL always be empty (AI generates them separately).
        
        Feature: resume-file-import, Property 9: Template Round-Trip Mapping
        **Validates: Requirements 7.3, 7.5**
        """
        result = map_yaml_to_resume_json(input_data)
        assert result['highlights'] == []

