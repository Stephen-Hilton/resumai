#!/usr/bin/env python3
"""
Property tests for template engine assembly

Tests that template engine correctly maps structured content to HTML templates.
"""

import pytest
from hypothesis import given, strategies as st, settings
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.template_engine import TemplateEngine

class TestTemplateEngineProperties:
    """Property-based tests for template engine assembly."""
    
    def setup_method(self):
        """Set up template engine for each test."""
        self.engine = TemplateEngine()
    
    @given(
        name=st.text(min_size=5, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs'))),
        summary=st.text(min_size=50, max_size=500),
        skills_per_column=st.lists(
            st.text(min_size=10, max_size=40, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs'))),
            min_size=3, max_size=4
        )
    )
    @settings(max_examples=20, deadline=5000)
    def test_template_engine_assembly_property(self, name, summary, skills_per_column):
        """
        Property 4: Template engine assembly
        For any complete set of structured sections, the template engine should produce valid HTML output.
        
        **Feature: modular-resume-generation, Property 4: Template engine assembly**
        **Validates: Requirements 1.4, 3.3, 4.3**
        """
        # Create structured content data
        content_data = {
            'summary': summary,
            'skills': {
                'column1': skills_per_column[:4] if len(skills_per_column) >= 4 else skills_per_column + ['Skill'] * (4 - len(skills_per_column)),
                'column2': skills_per_column[:4] if len(skills_per_column) >= 4 else skills_per_column + ['Skill'] * (4 - len(skills_per_column)),
                'column3': skills_per_column[:4] if len(skills_per_column) >= 4 else skills_per_column + ['Skill'] * (4 - len(skills_per_column))
            },
            'experience': [
                {
                    'company': 'Test Company',
                    'description': 'A test company for validation',
                    'roles': [
                        {
                            'title': 'Test Role',
                            'dates': '2020-2023',
                            'bullets': ['Test achievement 1', 'Test achievement 2']
                        }
                    ]
                }
            ],
            'education': [
                {'course': 'Computer Science', 'school': 'Test University'}
            ],
            'awards': [
                {'title': 'Test Award'}
            ],
            'cover_letter': {
                'opening': 'Dear Hiring Team,',
                'body_paragraphs': [
                    'I am interested in this position.',
                    'My experience is relevant.',
                    'I look forward to hearing from you.'
                ],
                'closing': 'Thank you,\\n\\nTest Candidate'
            }
        }
        
        # Test resume rendering
        html_resume = self.engine.render_resume(content_data)
        
        # Property 1: Should produce valid HTML structure
        assert isinstance(html_resume, str), "Resume output should be a string"
        assert len(html_resume) > 100, "Resume HTML should be substantial"
        assert '<!DOCTYPE html>' in html_resume, "Should have DOCTYPE declaration"
        assert '<html' in html_resume and '</html>' in html_resume, "Should have html tags"
        assert '<head>' in html_resume and '</head>' in html_resume, "Should have head section"
        assert '<body' in html_resume and '</body>' in html_resume, "Should have body section"
        
        # Property 2: Should contain the provided content
        assert name in html_resume, "Name should appear in HTML"
        assert summary in html_resume, "Summary should appear in HTML"
        
        # Property 3: Should contain skills from all columns
        for skill in skills_per_column[:4]:  # Check first 4 skills
            assert skill in html_resume, f"Skill '{skill}' should appear in HTML"
        
        # Property 4: Should have proper CSS class structure
        assert 'both_body' in html_resume, "Should use proper CSS classes"
        assert 'both_container' in html_resume, "Should have container class"
        assert 'both_header' in html_resume, "Should have header class"
        
        # Test cover letter rendering
        job_data = {'company': 'Test Company', 'title': 'Test Position'}
        html_cover_letter = self.engine.render_cover_letter(content_data, job_data)
        
        # Property 5: Cover letter should also be valid HTML
        assert isinstance(html_cover_letter, str), "Cover letter output should be a string"
        assert len(html_cover_letter) > 100, "Cover letter HTML should be substantial"
        assert '<!DOCTYPE html>' in html_cover_letter, "Should have DOCTYPE declaration"
        assert name in html_cover_letter, "Name should appear in cover letter"
        
        # Property 6: Cover letter should contain letter content
        cover_letter_content = content_data['cover_letter']
        assert cover_letter_content['opening'] in html_cover_letter, "Opening should appear"
        for paragraph in cover_letter_content['body_paragraphs']:
            assert paragraph in html_cover_letter, f"Paragraph '{paragraph}' should appear"
    
    def test_template_variable_mapping(self):
        """Test that template variables are correctly mapped."""
        content_data = {
            'summary': 'Test professional summary',
            'skills': {
                'column1': ['Python', 'JavaScript', 'SQL', 'Docker'],
                'column2': ['AWS', 'Kubernetes', 'Git', 'Linux'],
                'column3': ['Leadership', 'Communication', 'Problem Solving', 'Teamwork']
            },
            'experience': [],
            'education': [],
            'awards': []
        }
        
        html = self.engine.render_resume(content_data)
        
        # Check that all skills appear in the correct structure
        assert 'Python' in html
        assert 'JavaScript' in html
        assert 'Leadership' in html
        assert 'Communication' in html
        
        # Check that summary appears
        assert 'Test professional summary' in html
        
        # Check that proper sections are present
        assert 'Professional Summary' in html
        assert 'Core Skills' in html
        assert 'Experience' in html
    
    def test_missing_template_variables_handling(self):
        """Test that missing template variables are handled gracefully."""
        # Content with missing sections
        minimal_content = {
            'summary': 'Minimal summary',
            'skills': {
                'column1': ['Skill1'],
                'column2': ['Skill2'],
                'column3': ['Skill3']
            }
            # Missing experience, education, awards
        }
        
        # Should not raise an exception
        html = self.engine.render_resume(minimal_content)
        
        # Should still produce valid HTML
        assert isinstance(html, str)
        assert len(html) > 100
        assert 'Minimal summary' in html
        assert 'Skill1' in html
    
    def test_fallback_generation(self):
        """Test that fallback HTML generation works when templates fail."""
        # Test with content that should work with fallback
        content_data = {
            'summary': 'Fallback test summary',
            'skills': {
                'column1': ['Skill A', 'Skill B'],
                'column2': ['Skill C', 'Skill D'],
                'column3': ['Skill E', 'Skill F']
            },
            'experience': [
                {
                    'company': 'Fallback Company',
                    'description': 'Test company',
                    'roles': [
                        {
                            'title': 'Test Role',
                            'dates': '2020-2023',
                            'bullets': ['Achievement 1', 'Achievement 2']
                        }
                    ]
                }
            ],
            'education': [{'course': 'Test Degree', 'school': 'Test School'}],
            'awards': [{'title': 'Test Award'}]
        }
        
        # Generate fallback HTML
        fallback_html = self.engine._generate_fallback_resume(content_data)
        
        # Should produce valid HTML
        assert isinstance(fallback_html, str)
        assert '<!DOCTYPE html>' in fallback_html
        assert 'Fallback test summary' in fallback_html
        assert 'Skill A' in fallback_html
        assert 'Fallback Company' in fallback_html
        assert 'Test Role' in fallback_html
        assert 'Achievement 1' in fallback_html
        
        # Test cover letter fallback
        job_data = {'company': 'Test Company'}
        fallback_cover = self.engine._generate_fallback_cover_letter(content_data, job_data)
        
        assert isinstance(fallback_cover, str)
        assert '<!DOCTYPE html>' in fallback_cover
    
    def test_template_validation(self):
        """Test template variable validation."""
        # Valid variables for resume template
        valid_resume_vars = {
            'name': 'Test Name',
            'summary': 'Test Summary',
            'skills': {'column1': [], 'column2': [], 'column3': []},
            'experience': [],
            'education': [],
            'contacts': []
        }
        
        # Should pass validation
        is_valid = self.engine.validate_template_variables('resume.html', valid_resume_vars)
        assert is_valid, "Valid variables should pass validation"
        
        # Invalid variables (missing required fields)
        invalid_vars = {
            'name': 'Test Name'
            # Missing other required fields
        }
        
        # Should fail validation
        is_valid = self.engine.validate_template_variables('resume.html', invalid_vars)
        assert not is_valid, "Invalid variables should fail validation"
    
    @given(
        company_name=st.text(min_size=5, max_size=30),
        paragraphs=st.lists(
            st.text(min_size=20, max_size=100),
            min_size=2, max_size=4
        )
    )
    @settings(max_examples=10)
    def test_cover_letter_content_property(self, company_name, paragraphs):
        """Test that cover letter content is properly rendered."""
        content_data = {
            'cover_letter': {
                'opening': f'Dear {company_name} team,',
                'body_paragraphs': paragraphs,
                'closing': 'Thank you,\\n\\nCandidate Name'
            }
        }
        
        job_data = {'company': company_name}
        
        html = self.engine.render_cover_letter(content_data, job_data)
        
        # Property: All content should appear in HTML
        assert f'Dear {company_name} team,' in html
        for paragraph in paragraphs:
            assert paragraph in html
        assert 'Thank you,' in html
        assert 'Candidate Name' in html
        
        # Property: Should be valid HTML structure
        assert '<!DOCTYPE html>' in html
        assert '<body' in html and '</body>' in html

if __name__ == '__main__':
    pytest.main([__file__, '-v'])