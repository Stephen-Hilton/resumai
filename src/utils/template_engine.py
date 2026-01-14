#!/usr/bin/env python3
"""
Template Engine - Merges structured content into HTML templates

This module handles loading HTML templates and rendering them with structured
content from the modular generation system.
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
from datetime import datetime

logger = logging.getLogger(__name__)

class TemplateEngine:
    """
    Merges structured content into HTML templates from src/resources/templates/.
    
    Handles template loading, variable mapping, and HTML generation for both
    resume and cover letter content.
    """
    
    def __init__(self, template_dir: str = None):
        """
        Initialize template engine with template directory.
        
        Args:
            template_dir: Path to template directory (defaults to src/resources/templates relative to this file)
        """
        if template_dir is None:
            # Get absolute path relative to this file's location
            current_file = Path(__file__).parent
            template_dir = current_file.parent / "resources" / "templates"
        
        self.template_dir = Path(template_dir)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Initialize Jinja2 environment
        if self.template_dir.exists():
            self.env = Environment(
                loader=FileSystemLoader(str(self.template_dir)),
                autoescape=True,
                trim_blocks=True,
                lstrip_blocks=True,
                cache_size=0  # Disable template caching
            )
            self.logger.info(f"Template engine initialized with directory: {self.template_dir}")
        else:
            self.logger.warning(f"Template directory does not exist: {self.template_dir}")
            self.env = None
    
    def render_resume(self, content_data: dict, template_name: str = "resume.html") -> str:
        """
        Render structured content into HTML resume.
        
        Args:
            content_data: Aggregated content from ContentAggregator
            template_name: Name of resume template file
            
        Returns:
            Rendered HTML string
        """
        self.logger.info(f"Rendering resume with template: {template_name}")
        
        try:
            template = self.load_template(template_name)
            
            # Prepare template variables
            template_vars = self._prepare_resume_variables(content_data)
            
            # Render template
            html_content = template.render(**template_vars)
            
            self.logger.info("Resume template rendered successfully")
            return html_content
            
        except Exception as e:
            self.logger.error(f"Error rendering resume template: {str(e)}", exc_info=True)
            return self._generate_fallback_resume(content_data)
    
    def render_cover_letter(self, content_data: dict, job_data: dict, 
                          template_name: str = "cover_letter.html") -> str:
        """
        Render cover letter using structured content.
        
        Args:
            content_data: Aggregated content from ContentAggregator
            job_data: Job information for personalization
            template_name: Name of cover letter template file
            
        Returns:
            Rendered HTML string
        """
        self.logger.info(f"Rendering cover letter with template: {template_name}")
        
        try:
            template = self.load_template(template_name)
            
            # Prepare template variables
            template_vars = self._prepare_cover_letter_variables(content_data, job_data)
            
            # Render template
            html_content = template.render(**template_vars)
            
            self.logger.info("Cover letter template rendered successfully")
            return html_content
            
        except Exception as e:
            self.logger.error(f"Error rendering cover letter template: {str(e)}", exc_info=True)
            return self._generate_fallback_cover_letter(content_data, job_data)
    
    def load_template(self, template_name: str) -> Template:
        """
        Load HTML template from src/resources/templates/.
        
        Args:
            template_name: Name of template file
            
        Returns:
            Jinja2 Template object
        """
        if not self.env:
            raise TemplateNotFound(f"Template environment not initialized")
        
        try:
            template = self.env.get_template(template_name)
            self.logger.debug(f"Loaded template: {template_name}")
            return template
            
        except TemplateNotFound:
            self.logger.error(f"Template not found: {template_name}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading template {template_name}: {str(e)}")
            raise
    
    def _prepare_resume_variables(self, content_data: dict) -> dict:
        """Prepare variables for resume template rendering."""
        # Use dynamic contact information from content_data
        contacts = content_data.get('contacts', [])
        
        # If no contacts provided, create from individual fields
        if not contacts:
            contacts = []
            if content_data.get('email'):
                contacts.append({'name': 'email', 'label': content_data['email'], 'icon': 'mail'})
            if content_data.get('phone'):
                contacts.append({'name': 'phone', 'label': content_data['phone'], 'icon': 'mobile'})
            if content_data.get('location'):
                contacts.append({'name': 'location', 'label': content_data['location'], 'icon': 'home_pin'})
            if content_data.get('linkedin'):
                contacts.append({'name': 'linkedin', 'label': content_data['linkedin'], 'icon': 'linkedin.svg'})
        
        return {
            'name': content_data.get('name', 'Name Not Provided'),
            'summary': content_data.get('summary', ''),
            'skills': content_data.get('skills', {}),
            'highlights': content_data.get('highlights', {}),
            'experience': content_data.get('experience', []),
            'education': content_data.get('education', []),
            'awards': content_data.get('awards', []),
            'contacts': contacts,
            'generation_date': datetime.now().strftime('%B %d, %Y'),
            'version': self._get_version()
        }
    
    def _prepare_cover_letter_variables(self, content_data: dict, job_data: dict) -> dict:
        """Prepare variables for cover letter template rendering."""
        cover_letter = content_data.get('cover_letter', {})
        
        # Use dynamic contact information from content_data
        contacts = content_data.get('contacts', [])
        
        # If no contacts provided, create from individual fields
        if not contacts:
            contacts = []
            if content_data.get('email'):
                contacts.append({'name': 'email', 'label': content_data['email'], 'icon': 'mail'})
            if content_data.get('phone'):
                contacts.append({'name': 'phone', 'label': content_data['phone'], 'icon': 'mobile'})
            if content_data.get('location'):
                contacts.append({'name': 'location', 'label': content_data['location'], 'icon': 'home_pin'})
            if content_data.get('linkedin'):
                contacts.append({'name': 'linkedin', 'label': content_data['linkedin'], 'icon': 'linkedin.svg'})
        
        return {
            'name': content_data.get('name', 'Name Not Provided'),
            'contacts': contacts,
            'date': datetime.now().strftime('%B %d, %Y'),
            'company': job_data.get('company', 'Hiring Team'),
            'opening': cover_letter.get('opening', 'Dear Hiring Team,'),
            'body_paragraphs': cover_letter.get('body_paragraphs', []),
            'closing': cover_letter.get('closing', f'Thank you,\n\n{content_data.get("name", "Name Not Provided")}'),
            'version': self._get_version()
        }
    
    def _get_version(self) -> str:
        """Get version string for footer."""
        try:
            from src.utils.version import get_version
            return get_version()
        except ImportError:
            return "1.0.0"
    
    def _generate_fallback_resume(self, content_data: dict) -> str:
        """Generate basic HTML resume when template fails."""
        self.logger.info("Generating fallback resume HTML")
        
        skills = content_data.get('skills', {})
        all_skills = []
        for col in ['column1', 'column2', 'column3']:
            all_skills.extend(skills.get(col, []))
        
        # Use dynamic contact info
        name = content_data.get('name', 'Name Not Provided')
        email = content_data.get('email', 'email@example.com')
        phone = content_data.get('phone', '(555) 000-0000')
        location = content_data.get('location', 'Location Not Provided')
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Resume - {name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .section {{ margin-bottom: 25px; }}
        .section h2 {{ color: #2c5aa0; border-bottom: 1px solid #ccc; }}
        .skills {{ display: flex; flex-wrap: wrap; }}
        .skill {{ margin: 5px; padding: 5px 10px; background: #f0f0f0; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{name}</h1>
        <p>{email} | {phone} | {location}</p>
    </div>
    
    <div class="section">
        <h2>Professional Summary</h2>
        <p>{content_data.get('summary', 'Professional summary not available.')}</p>
    </div>
    
    <div class="section">
        <h2>Core Skills</h2>
        <div class="skills">
            {' '.join(f'<span class="skill">{skill}</span>' for skill in all_skills)}
        </div>
    </div>
    
    <div class="section">
        <h2>Experience</h2>
        {''.join(self._format_experience_fallback(exp) for exp in content_data.get('experience', []))}
    </div>
    
    <div class="section">
        <h2>Education</h2>
        {''.join(f'<p><strong>{edu.get("course", "")}</strong> - {edu.get("school", "")}</p>' 
                 for edu in content_data.get('education', []))}
    </div>
    
    <div class="section">
        <h2>Awards & Recognition</h2>
        {''.join(f'<p>{award.get("title", "")}</p>' for award in content_data.get('awards', []))}
    </div>
    
    <footer style="text-align: center; margin-top: 40px; font-size: 8pt; color: #666;">
        ResumeAI v{self._get_version()}
    </footer>
</body>
</html>
"""
        return html
    
    def _format_experience_fallback(self, exp: dict) -> str:
        """Format experience entry for fallback HTML."""
        html = f"<div><h3>{exp.get('company', 'Unknown Company')}</h3>"
        if exp.get('description'):
            html += f"<p><em>{exp['description']}</em></p>"
        
        for role in exp.get('roles', []):
            html += f"<h4>{role.get('title', 'Unknown Role')} ({role.get('dates', 'Unknown dates')})</h4>"
            html += "<ul>"
            for bullet in role.get('bullets', []):
                html += f"<li>{bullet}</li>"
            html += "</ul>"
        
        html += "</div>"
        return html
    
    def _generate_fallback_cover_letter(self, content_data: dict, job_data: dict) -> str:
        """Generate basic HTML cover letter when template fails."""
        self.logger.info("Generating fallback cover letter HTML")
        
        cover_letter = content_data.get('cover_letter', {})
        name = content_data.get('name', 'Name Not Provided')
        email = content_data.get('email', 'email@example.com')
        phone = content_data.get('phone', '(555) 000-0000')
        location = content_data.get('location', 'Location Not Provided')
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Cover Letter - {name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .letter-body {{ margin: 30px 0; }}
        .paragraph {{ margin-bottom: 15px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{name}</h1>
        <p>{email} | {phone} | {location}</p>
    </div>
    
    <div class="letter-body">
        <p>{datetime.now().strftime('%B %d, %Y')}</p>
        
        <p>{cover_letter.get('opening', 'Dear Hiring Team,')}</p>
        
        {''.join(f'<p class="paragraph">{para}</p>' for para in cover_letter.get('body_paragraphs', []))}
        
        <p>{cover_letter.get('closing', f'Thank you,<br><br>{name}')}</p>
    </div>
    
    <footer style="text-align: center; margin-top: 40px; font-size: 8pt; color: #666;">
        ResumeAI v{self._get_version()}
    </footer>
</body>
</html>
"""
        return html
    
    def validate_template_variables(self, template_name: str, variables: dict) -> bool:
        """
        Validate that all required template variables are present.
        
        Args:
            template_name: Name of template to validate against
            variables: Variables to validate
            
        Returns:
            True if all required variables are present
        """
        try:
            template = self.load_template(template_name)
            
            # Get template source to analyze required variables
            # This is a simplified validation - in practice, you might want
            # to use more sophisticated template analysis
            
            required_vars = {
                'resume.html': ['name', 'summary', 'skills', 'experience', 'education', 'contacts'],
                'cover_letter.html': ['name', 'contacts', 'date', 'opening', 'body_paragraphs', 'closing']
            }
            
            required = required_vars.get(template_name, [])
            
            for var in required:
                if var not in variables:
                    self.logger.error(f"Missing required template variable: {var}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating template variables: {str(e)}")
            return False