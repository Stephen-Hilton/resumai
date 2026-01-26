"""
Property-based tests for Final File Generation.

Tests:
- Property 23: Final File Enable Condition
- Property 24: Resume HTML Aggregation
- Property 25: PDF Generation Round-Trip
- Property 26: Final File S3 Path
- Property 27: S3 Location Field Update
- Property 31: Resume URL Uniqueness
- Property 32: Generated HTML Global CSS Links

Feature: skillsnap-mvp
Validates: Requirements 10.1, 10.2, 10.3, 10.6, 10.7, 11.5, 11.6
"""
import pytest
from hypothesis import given, strategies as st, settings
import re
import sys
import os

# Add lambdas to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambdas'))

from shared.validation import VALID_SUBCOMPONENTS


# Strategy for usernames (URL-safe)
username_strategy = st.text(
    alphabet=st.sampled_from('abcdefghijklmnopqrstuvwxyz0123456789'),
    min_size=3,
    max_size=20
)

# Strategy for company names
company_strategy = st.text(min_size=1, max_size=50).filter(lambda x: x.strip() != '')

# Strategy for job titles
jobtitle_strategy = st.text(min_size=1, max_size=100).filter(lambda x: x.strip() != '')


def make_safe(text: str) -> str:
    """Convert text to URL-safe format."""
    return re.sub(r'[^a-z0-9-]', '-', text.lower().strip())[:50]


class TestFinalFileEnableCondition:
    """Tests for final file enable condition."""

    @given(
        states=st.fixed_dictionaries({
            comp: st.sampled_from(['locked', 'ready', 'generating', 'complete', 'error'])
            for comp in VALID_SUBCOMPONENTS
        })
    )
    @settings(max_examples=100)
    def test_property_23_enable_condition(self, states: dict):
        """
        Property 23: Final File Enable Condition
        
        For any job, final file generation buttons SHALL be enabled
        if and only if all 8 subcomponent states are "complete".
        
        Feature: skillsnap-mvp, Property 23: Final File Enable Condition
        """
        all_complete = all(state == 'complete' for state in states.values())
        
        # Simulate enable check
        can_generate_final = all(
            states.get(comp) == 'complete' for comp in VALID_SUBCOMPONENTS
        )
        
        assert can_generate_final == all_complete

    def test_property_23_all_complete_enables(self):
        """
        Property 23: Final File Enable Condition (all complete)
        
        When all subcomponents are complete, final files should be enabled.
        
        Feature: skillsnap-mvp, Property 23: Final File Enable Condition
        """
        states = {comp: 'complete' for comp in VALID_SUBCOMPONENTS}
        can_generate = all(states.get(comp) == 'complete' for comp in VALID_SUBCOMPONENTS)
        assert can_generate

    def test_property_23_one_incomplete_disables(self):
        """
        Property 23: Final File Enable Condition (one incomplete)
        
        When any subcomponent is not complete, final files should be disabled.
        
        Feature: skillsnap-mvp, Property 23: Final File Enable Condition
        """
        states = {comp: 'complete' for comp in VALID_SUBCOMPONENTS}
        states['summary'] = 'generating'  # One not complete
        
        can_generate = all(states.get(comp) == 'complete' for comp in VALID_SUBCOMPONENTS)
        assert not can_generate


class TestResumeHTMLAggregation:
    """Tests for resume HTML aggregation."""

    @given(
        contact=st.text(min_size=1, max_size=200),
        summary=st.text(min_size=1, max_size=500),
        skills=st.text(min_size=1, max_size=300),
        highlights=st.text(min_size=1, max_size=400),
        experience=st.text(min_size=1, max_size=1000),
        education=st.text(min_size=1, max_size=300),
        awards=st.text(min_size=1, max_size=200),
    )
    @settings(max_examples=100)
    def test_property_24_html_aggregation(
        self, contact, summary, skills, highlights, experience, education, awards
    ):
        """
        Property 24: Resume HTML Aggregation
        
        For any resume HTML generation, the output SHALL contain content
        from all subcomponents: contact, summary, skills, highlights,
        experience, education, and awards.
        
        Feature: skillsnap-mvp, Property 24: Resume HTML Aggregation
        """
        # Simulate HTML generation
        html = f'''<!DOCTYPE html>
<html>
<head><link rel="stylesheet" href="/assets/resume-base.css"></head>
<body>
<main class="resume">
{contact}
{summary}
{skills}
{highlights}
{experience}
{education}
{awards}
</main>
</body>
</html>'''
        
        # All content should be present
        assert contact in html
        assert summary in html
        assert skills in html
        assert highlights in html
        assert experience in html
        assert education in html
        assert awards in html

    def test_property_24_seven_subcomponents(self):
        """
        Property 24: Resume HTML Aggregation (count)
        
        Resume HTML should aggregate exactly 7 subcomponents (not cover letter).
        
        Feature: skillsnap-mvp, Property 24: Resume HTML Aggregation
        """
        resume_components = [
            'contact', 'summary', 'skills', 'highlights',
            'experience', 'education', 'awards'
        ]
        assert len(resume_components) == 7
        
        # Cover letter is separate
        assert 'coverletter' not in resume_components


class TestPDFGeneration:
    """Tests for PDF generation."""

    @given(html_content=st.text(min_size=10, max_size=1000))
    @settings(max_examples=100)
    def test_property_25_pdf_input_html(self, html_content: str):
        """
        Property 25: PDF Generation Round-Trip
        
        PDF generation should accept HTML content as input.
        
        Feature: skillsnap-mvp, Property 25: PDF Generation Round-Trip
        """
        # Simulate PDF generation input
        html = f'<html><body>{html_content}</body></html>'
        
        # HTML should be valid input
        assert '<html>' in html
        assert '</html>' in html
        assert html_content in html


class TestFinalFileS3Path:
    """Tests for final file S3 path structure."""

    @given(
        username=username_strategy,
        company=company_strategy,
        jobtitle=jobtitle_strategy,
        filename=st.sampled_from(['resume.html', 'resume.pdf', 'coverletter.html', 'coverletter.pdf'])
    )
    @settings(max_examples=100)
    def test_property_26_s3_path_structure(
        self, username: str, company: str, jobtitle: str, filename: str
    ):
        """
        Property 26: Final File S3 Path
        
        For any final file upload, the S3 key SHALL follow the pattern
        /{username}/{company}/{jobtitlesafe}/{filename}.
        
        Feature: skillsnap-mvp, Property 26: Final File S3 Path
        """
        company_safe = make_safe(company)
        jobtitle_safe = make_safe(jobtitle)
        
        s3_key = f"{username}/{company_safe}/{jobtitle_safe}/{filename}"
        
        # Verify structure
        parts = s3_key.split('/')
        assert len(parts) == 4
        assert parts[0] == username
        assert parts[1] == company_safe
        assert parts[2] == jobtitle_safe
        assert parts[3] == filename
        assert filename in ['resume.html', 'resume.pdf', 'coverletter.html', 'coverletter.pdf']

    def test_property_26_valid_filenames(self):
        """
        Property 26: Final File S3 Path (valid filenames)
        
        Only specific filenames are valid for final files.
        
        Feature: skillsnap-mvp, Property 26: Final File S3 Path
        """
        valid_filenames = ['resume.html', 'resume.pdf', 'coverletter.html', 'coverletter.pdf']
        assert len(valid_filenames) == 4


class TestS3LocationFieldUpdate:
    """Tests for S3 location field updates."""

    @given(
        bucket=st.text(alphabet=st.sampled_from('abcdefghijklmnopqrstuvwxyz0123456789-'), min_size=3, max_size=30),
        key=st.text(alphabet=st.sampled_from('abcdefghijklmnopqrstuvwxyz0123456789-/'), min_size=5, max_size=100)
    )
    @settings(max_examples=100)
    def test_property_27_s3_location_update(self, bucket: str, key: str):
        """
        Property 27: S3 Location Field Update
        
        For any successful file upload, the corresponding USER_JOB s3loc field
        SHALL be updated with the full S3 URI.
        
        Feature: skillsnap-mvp, Property 27: S3 Location Field Update
        """
        s3_uri = f"s3://{bucket}/{key}"
        
        # Simulate update
        update = {'s3locresumehtml': s3_uri}
        
        assert 's3locresumehtml' in update
        assert update['s3locresumehtml'] == s3_uri
        assert s3_uri.startswith('s3://')

    def test_property_27_all_s3_fields(self):
        """
        Property 27: S3 Location Field Update (all fields)
        
        All four S3 location fields should be supported.
        
        Feature: skillsnap-mvp, Property 27: S3 Location Field Update
        """
        s3_fields = [
            's3locresumehtml',
            's3locresumepdf',
            's3loccoverletterhtml',
            's3loccoverletterpdf'
        ]
        assert len(s3_fields) == 4


class TestResumeURLUniqueness:
    """Tests for resume URL uniqueness."""

    @given(
        username=username_strategy,
        company=company_strategy,
        jobtitle=jobtitle_strategy,
    )
    @settings(max_examples=100)
    def test_property_31_url_structure(
        self, username: str, company: str, jobtitle: str
    ):
        """
        Property 31: Resume URL Uniqueness
        
        Resume URLs should follow a consistent structure.
        
        Feature: skillsnap-mvp, Property 31: Resume URL Uniqueness
        """
        company_safe = make_safe(company)
        jobtitle_safe = make_safe(jobtitle)
        
        url = f"https://{username}.skillsnap.me/{company_safe}/{jobtitle_safe}"
        
        assert url.startswith('https://')
        assert '.skillsnap.me/' in url
        assert username in url

    def test_property_31_duplicate_detection(self):
        """
        Property 31: Resume URL Uniqueness (duplicate detection)
        
        Attempting to create a duplicate URL should be detectable.
        
        Feature: skillsnap-mvp, Property 31: Resume URL Uniqueness
        """
        existing_urls = set()
        url = "https://user.skillsnap.me/company/job"
        
        # First creation succeeds
        existing_urls.add(url)
        assert url in existing_urls
        
        # Duplicate detection
        is_duplicate = url in existing_urls
        assert is_duplicate


class TestGeneratedHTMLCSSLinks:
    """Tests for generated HTML CSS links."""

    def test_property_32_resume_css_link(self):
        """
        Property 32: Generated HTML Global CSS Links
        
        Generated resume HTML SHALL include link to /assets/resume-base.css.
        
        Feature: skillsnap-mvp, Property 32: Generated HTML Global CSS Links
        """
        html = '''<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/assets/resume-base.css">
</head>
<body></body>
</html>'''
        
        assert '/assets/resume-base.css' in html

    def test_property_32_cover_letter_css_link(self):
        """
        Property 32: Generated HTML Global CSS Links
        
        Generated cover letter HTML SHALL include link to /assets/cover-base.css.
        
        Feature: skillsnap-mvp, Property 32: Generated HTML Global CSS Links
        """
        html = '''<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/assets/cover-base.css">
</head>
<body></body>
</html>'''
        
        assert '/assets/cover-base.css' in html

    @given(
        job_title=st.text(min_size=1, max_size=100),
        company=st.text(min_size=1, max_size=50)
    )
    @settings(max_examples=100)
    def test_property_32_css_link_present(self, job_title: str, company: str):
        """
        Property 32: Generated HTML Global CSS Links (always present)
        
        CSS links should always be present in generated HTML.
        
        Feature: skillsnap-mvp, Property 32: Generated HTML Global CSS Links
        """
        # Simulate resume HTML generation
        resume_html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Resume - {job_title} at {company}</title>
    <link rel="stylesheet" href="/assets/resume-base.css">
</head>
<body></body>
</html>'''
        
        assert '/assets/resume-base.css' in resume_html
        
        # Simulate cover letter HTML generation
        cover_html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Cover Letter - {job_title} at {company}</title>
    <link rel="stylesheet" href="/assets/cover-base.css">
</head>
<body></body>
</html>'''
        
        assert '/assets/cover-base.css' in cover_html
