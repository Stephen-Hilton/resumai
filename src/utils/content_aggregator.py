#!/usr/bin/env python3
"""
Content Aggregator - Combines section results into complete resume data structure

This module handles the aggregation of individual section results into a unified
data structure suitable for template rendering.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ContentAggregator:
    """
    Combines section results into complete resume structure.
    
    Handles missing sections, failed sections, and provides fallback content
    to ensure a complete resume can always be generated.
    """
    
    def __init__(self):
        """Initialize content aggregator."""
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def aggregate_sections(self, section_results: Dict[str, Any], resume_data: dict = None) -> dict:
        """
        Combine section results into complete resume structure.
        
        Args:
            section_results: Dictionary mapping section names to their results
            resume_data: Original resume data from YAML file (for name, contacts, etc.)
            
        Returns:
            Complete resume data structure ready for template rendering
        """
        self.logger.info(f"Aggregating {len(section_results)} section results")
        
        aggregated = {
            'metadata': {
                'generation_timestamp': datetime.now().isoformat(),
                'sections_processed': list(section_results.keys()),
                'successful_sections': [],
                'failed_sections': []
            }
        }
        
        # Include original resume data (name, contacts, etc.)
        if resume_data:
            aggregated.update({
                'name': resume_data.get('name', 'Name Not Provided'),
                'contacts': resume_data.get('contacts', []),
                'location': resume_data.get('location', ''),
                'email': resume_data.get('email', ''),
                'phone': resume_data.get('phone', ''),
                'linkedin': resume_data.get('linkedin', ''),
                'passions': resume_data.get('passions', [])
            })
            self.logger.info(f"Added base resume data for: {aggregated.get('name', 'Unknown')}")
        else:
            # Fallback if no resume data provided
            aggregated.update({
                'name': 'Name Not Provided',
                'contacts': [],
                'location': '',
                'email': '',
                'phone': '',
                'linkedin': '',
                'passions': []
            })
            self.logger.warning("No resume data provided, using fallback values")
        
        # Process each section result
        for section_name, result in section_results.items():
            if result.get('status') == 'completed' and result.get('content'):
                self._add_successful_section(aggregated, section_name, result['content'])
                aggregated['metadata']['successful_sections'].append(section_name)
            else:
                self._handle_failed_section(aggregated, section_name, result)
                aggregated['metadata']['failed_sections'].append({
                    'section': section_name,
                    'status': result.get('status', 'unknown'),
                    'error': result.get('error', 'No error message')
                })
        
        # Ensure all required sections are present
        self._ensure_required_sections(aggregated)
        
        self.logger.info(f"Aggregation complete: {len(aggregated['metadata']['successful_sections'])} successful, "
                        f"{len(aggregated['metadata']['failed_sections'])} failed")
        
        return aggregated
    
    def _add_successful_section(self, aggregated: dict, section_name: str, content: dict):
        """Add successfully generated section content to aggregated result."""
        if section_name == 'summary':
            aggregated['summary'] = content.get('summary', '')
            
        elif section_name == 'skills':
            aggregated['skills'] = {
                'column1': content.get('column1', []),
                'column2': content.get('column2', []),
                'column3': content.get('column3', [])
            }
            
        elif section_name == 'highlights':
            aggregated['highlights'] = content.get('highlights', {})
            
        elif section_name == 'experience':
            aggregated['experience'] = content.get('experience', [])
            
        elif section_name == 'education':
            aggregated['education'] = content.get('education', [])
            
        elif section_name == 'awards':
            aggregated['awards'] = content.get('awards', [])
            
        elif section_name == 'cover_letter':
            aggregated['cover_letter'] = {
                'opening': content.get('opening', ''),
                'body_paragraphs': content.get('body_paragraphs', []),
                'closing': content.get('closing', '')
            }
        
        else:
            # Handle unknown sections
            self.logger.warning(f"Unknown section type: {section_name}")
            aggregated[section_name] = content
    
    def _handle_failed_section(self, aggregated: dict, section_name: str, result: dict):
        """Handle failed section by providing fallback content."""
        self.logger.warning(f"Section '{section_name}' failed: {result.get('error', 'Unknown error')}")
        
        # Provide minimal fallback content
        if section_name == 'summary':
            aggregated['summary'] = "Professional summary not available."
            
        elif section_name == 'skills':
            aggregated['skills'] = {
                'column1': ["Skills", "Not", "Available", "Currently"],
                'column2': ["Please", "Check", "Original", "Resume"],
                'column3': ["For", "Complete", "Skills", "List"]
            }
            
        elif section_name == 'experience':
            aggregated['experience'] = []
            
        elif section_name == 'education':
            aggregated['education'] = []
            
        elif section_name == 'awards':
            aggregated['awards'] = []
            
        elif section_name == 'cover_letter':
            aggregated['cover_letter'] = {
                'opening': "Dear Hiring Team,",
                'body_paragraphs': [
                    "I am writing to express my interest in this position.",
                    "Please refer to my attached resume for detailed information.",
                    "I look forward to hearing from you."
                ],
                'closing': "Thank you,\n\nCandidate"
            }
    
    def _ensure_required_sections(self, aggregated: dict):
        """Ensure all required sections are present with at least fallback content."""
        required_sections = {
            'summary': "Professional summary not available.",
            'skills': {
                'column1': ["Skills", "Not", "Available", "Currently"],
                'column2': ["Please", "Check", "Original", "Resume"],
                'column3': ["For", "Complete", "Skills", "List"]
            },
            'experience': [],
            'education': [],
            'awards': [],
            'cover_letter': {
                'opening': "Dear Hiring Team,",
                'body_paragraphs': [
                    "I am writing to express my interest in this position.",
                    "Please refer to my attached resume for detailed information.",
                    "I look forward to hearing from you."
                ],
                'closing': "Thank you,\n\nCandidate"
            }
        }
        
        for section, default_content in required_sections.items():
            if section not in aggregated:
                aggregated[section] = default_content
                self.logger.info(f"Added default content for missing section: {section}")
    
    def handle_missing_sections(self, resume_data: dict, section_results: Dict[str, Any]) -> dict:
        """
        Fill in missing sections with fallback content from original resume.
        
        Args:
            resume_data: Original resume data from YAML file
            section_results: Results from section generation
            
        Returns:
            Complete resume structure with fallbacks
        """
        self.logger.info("Handling missing sections with original resume data")
        
        # Start with aggregated results
        aggregated = self.aggregate_sections(section_results)
        
        # Fill in missing sections from original resume
        if 'summary' not in aggregated or not aggregated['summary']:
            aggregated['summary'] = resume_data.get('Summary', 'Professional summary not available.')
        
        if 'skills' not in aggregated or not aggregated['skills']:
            original_skills = resume_data.get('skills', [])
            if original_skills:
                # Organize original skills into columns
                skills_per_column = max(1, len(original_skills) // 3)
                aggregated['skills'] = {
                    'column1': original_skills[:skills_per_column],
                    'column2': original_skills[skills_per_column:skills_per_column*2],
                    'column3': original_skills[skills_per_column*2:]
                }
        
        if 'experience' not in aggregated or not aggregated['experience']:
            aggregated['experience'] = resume_data.get('experience', [])
        
        if 'education' not in aggregated or not aggregated['education']:
            original_education = resume_data.get('education', [])
            # Format education without dates
            formatted_education = []
            for edu in original_education:
                formatted_education.append({
                    'course': edu.get('course', 'Unknown Course'),
                    'school': edu.get('school', 'Unknown School')
                })
            aggregated['education'] = formatted_education
        
        if 'awards' not in aggregated or not aggregated['awards']:
            original_awards = resume_data.get('awards_and_keynotes', [])
            # Format awards without dates
            formatted_awards = []
            for award in original_awards:
                formatted_awards.append({
                    'title': award.get('award', 'Unknown Award')
                })
            aggregated['awards'] = formatted_awards
        
        return aggregated
    
    def validate_aggregated_content(self, aggregated: dict) -> bool:
        """
        Validate that aggregated content is suitable for template rendering.
        
        Args:
            aggregated: Aggregated content dictionary
            
        Returns:
            True if content is valid, False otherwise
        """
        required_sections = ['summary', 'skills', 'experience', 'education', 'awards', 'cover_letter']
        
        for section in required_sections:
            if section not in aggregated:
                self.logger.error(f"Missing required section: {section}")
                return False
        
        # Validate skills structure
        skills = aggregated.get('skills', {})
        if not isinstance(skills, dict):
            self.logger.error("Skills section is not a dictionary")
            return False
        
        for col in ['column1', 'column2', 'column3']:
            if col not in skills or not isinstance(skills[col], list):
                self.logger.error(f"Skills {col} is missing or not a list")
                return False
        
        # Validate cover letter structure
        cover_letter = aggregated.get('cover_letter', {})
        if not isinstance(cover_letter, dict):
            self.logger.error("Cover letter section is not a dictionary")
            return False
        
        required_cl_fields = ['opening', 'body_paragraphs', 'closing']
        for field in required_cl_fields:
            if field not in cover_letter:
                self.logger.error(f"Cover letter missing field: {field}")
                return False
        
        self.logger.info("Aggregated content validation passed")
        return True
    
    def get_generation_summary(self, section_results: Dict[str, Any]) -> dict:
        """
        Get summary of generation results for reporting.
        
        Args:
            section_results: Results from section generation
            
        Returns:
            Summary dictionary with statistics
        """
        total_sections = len(section_results)
        successful = sum(1 for r in section_results.values() if r.get('status') == 'completed')
        failed = total_sections - successful
        
        execution_times = []
        for result in section_results.values():
            if result.get('content') and isinstance(result['content'], dict):
                exec_time = result['content'].get('_execution_time')
                if exec_time:
                    execution_times.append(exec_time)
        
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        return {
            'total_sections': total_sections,
            'successful_sections': successful,
            'failed_sections': failed,
            'success_rate': successful / total_sections if total_sections > 0 else 0,
            'average_execution_time': avg_execution_time,
            'section_details': {
                name: {
                    'status': result.get('status', 'unknown'),
                    'generator': result.get('generator', 'unknown'),
                    'error': result.get('error') if result.get('status') != 'completed' else None
                }
                for name, result in section_results.items()
            }
        }