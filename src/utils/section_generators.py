#!/usr/bin/env python3
"""
Section Generators - Individual content generators for resume sections

This module provides the base classes and specific implementations for generating
structured content for different resume sections (summary, skills, experience, etc.).
"""

import logging
import yaml
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
from .ai_content_cache import AIContentCache

logger = logging.getLogger(__name__)

class SectionType(Enum):
    """Enumeration of supported resume sections."""
    SUMMARY = "summary"
    SKILLS = "skills"
    HIGHLIGHTS = "highlights"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    AWARDS = "awards"
    COVER_LETTER = "cover_letter"

@dataclass
class SectionConfig:
    """Configuration for a resume section."""
    section_type: SectionType
    priority: int = 1
    required: bool = True
    timeout_seconds: int = 30
    max_retries: int = 2
    character_limits: Optional[Dict[str, int]] = None

class SectionGenerator(ABC):
    """
    Abstract base class for all section generators.
    
    Each section generator is responsible for creating structured content
    for a specific resume section using LLM calls.
    """
    
    def __init__(self, section_name: str, config: Optional[Dict] = None, cache: Optional[AIContentCache] = None):
        """
        Initialize section generator.
        
        Args:
            section_name: Name of the section (e.g., "summary", "skills")
            config: Optional configuration dictionary
            cache: Optional AIContentCache instance for saving/loading content
        """
        self.section_name = section_name
        self.config = config or {}
        self.cache = cache
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    def generate_content(self, resume_data: dict, job_data: dict) -> dict:
        """
        Generate structured content for this section.
        
        Args:
            resume_data: Resume information from YAML file
            job_data: Job description and requirements
            
        Returns:
            Dictionary containing structured content for this section
        """
        pass
    
    @abstractmethod
    def get_prompt_template(self) -> str:
        """
        Get LLM prompt template for this section.
        
        Returns:
            String template for LLM prompt
        """
        pass
    
    def uses_llm(self) -> bool:
        """
        Check if this generator makes LLM calls.
        
        Returns:
            True if generator makes LLM calls, False for simple reformatting
        """
        template = self.get_prompt_template()
        return template is not None and template.strip() != ""
    
    def validate_content(self, content: dict) -> bool:
        """
        Validate generated content structure.
        
        Args:
            content: Generated content dictionary
            
        Returns:
            True if content is valid, False otherwise
        """
        if not isinstance(content, dict):
            self.logger.error(f"Content is not a dictionary: {type(content)}")
            return False
        
        if not content:
            self.logger.error("Content is empty")
            return False
        
        return True
    
    def generate_with_cache(self, resume_data: dict, job_data: dict, force_regenerate: bool = False) -> dict:
        """
        Generate content with caching support.
        
        Args:
            resume_data: Resume information from YAML file
            job_data: Job description and requirements
            force_regenerate: If True, skip cache and regenerate content
            
        Returns:
            Dictionary containing structured content for this section
        """
        # Try to load from cache first (unless forced to regenerate)
        if not force_regenerate and self.cache and self.cache.has_cached_content(self.section_name):
            cached_content = self.cache.load_section_content(self.section_name)
            if cached_content:
                self.logger.info(f"Using cached content for section '{self.section_name}'")
                return cached_content
        
        # Generate new content
        self.logger.info(f"Generating new content for section '{self.section_name}'")
        content = self.generate_content(resume_data, job_data)
        
        # Save to cache if available
        if self.cache and content:
            metadata = {
                'generator_class': self.__class__.__name__,
                'uses_llm': self.uses_llm(),
                'job_title': job_data.get('title', ''),
                'company': job_data.get('company', '')
            }
            self.cache.save_section_content(self.section_name, content, metadata)
        
        return content
    
    def _make_llm_call(self, prompt: str, system_prompt: str = None) -> str:
        """
        Make LLM call for content generation.
        
        Args:
            prompt: User prompt for LLM
            system_prompt: Optional system prompt
            
        Returns:
            LLM response string
        """
        try:
            # Import LLM function - handle different contexts
            try:
                from src.step2_generate import llm_call
            except ImportError:
                # Try alternative import path for web context
                import sys
                from pathlib import Path
                
                # Add project root to path if not already there
                project_root = str(Path(__file__).parent.parent.parent)
                if project_root not in sys.path:
                    sys.path.insert(0, project_root)
                
                from src.step2_generate import llm_call
            
            # Use structured output system prompt
            if not system_prompt:
                system_prompt = """
                You are a professional resume writer who creates structured content in YAML format.
                Return ONLY valid YAML content without explanations, code fences, or additional text.
                Focus on content quality and relevance to the job description.
                Ensure all character limits are respected.
                """
            
            response = llm_call(sys_prompt=system_prompt, user_prompt=prompt, section_name=self.section_name)
            return response.strip()
            
        except Exception as e:
            self.logger.error(f"LLM call failed for {self.section_name}: {str(e)}")
            raise
    
    def _parse_yaml_response(self, response: str) -> dict:
        """
        Parse YAML response from LLM.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed dictionary
        """
        try:
            # Clean up response (remove code fences if present)
            cleaned_response = response.strip()
            if cleaned_response.startswith('```yaml'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            
            # Clean up each line: strip trailing whitespace and normalize indentation
            lines = cleaned_response.strip().split('\n')
            cleaned_lines = []
            
            # First pass: strip trailing whitespace from all lines
            for line in lines:
                cleaned_lines.append(line.rstrip())
            
            # Second pass: find minimum indentation of non-empty lines
            non_empty_lines = [line for line in cleaned_lines if line.strip()]
            
            if non_empty_lines:
                # Find minimum indentation
                min_indent = min(len(line) - len(line.lstrip()) for line in non_empty_lines)
                
                # Remove minimum indentation from all lines
                if min_indent > 0:
                    final_lines = []
                    for line in cleaned_lines:
                        if line.strip():  # Non-empty line
                            final_lines.append(line[min_indent:])
                        else:  # Empty line
                            final_lines.append('')
                    cleaned_response = '\n'.join(final_lines)
                else:
                    cleaned_response = '\n'.join(cleaned_lines)
            else:
                cleaned_response = '\n'.join(cleaned_lines)
            
            # Parse YAML
            content = yaml.safe_load(cleaned_response.strip())
            
            if not isinstance(content, dict):
                raise ValueError(f"Parsed content is not a dictionary: {type(content)}")
            
            return content
            
        except yaml.YAMLError as e:
            self.logger.error(f"YAML parsing error for {self.section_name}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error parsing response for {self.section_name}: {str(e)}")
            raise

class SummaryGenerator(SectionGenerator):
    """Generator for professional summary section."""
    
    def __init__(self, config: Optional[Dict] = None, cache: Optional[AIContentCache] = None):
        super().__init__("summary", config, cache)
        self.character_limit = (580, 630)  # Min, Max characters
    
    def generate_content(self, resume_data: dict, job_data: dict) -> dict:
        """Generate professional summary tailored to job."""
        prompt = self.get_prompt_template().format(
            resume_summary=resume_data.get('Summary', ''),
            job_title=job_data.get('title', ''),
            job_description=job_data.get('description', ''),
            company=job_data.get('company', ''),
            min_chars=self.character_limit[0],
            max_chars=self.character_limit[1]
        )
        
        response = self._make_llm_call(prompt)
        content = self._parse_yaml_response(response)
        
        # Validate character count
        summary_text = content.get('summary', '')
        char_count = len(summary_text)
        
        if char_count < self.character_limit[0] or char_count > self.character_limit[1]:
            self.logger.warning(f"Summary character count {char_count} outside limits {self.character_limit}")
        
        return content
    
    def get_prompt_template(self) -> str:
        return """
Create a professional summary for this resume tailored to the specific job opportunity.

REQUIREMENTS:
- Length: {min_chars}-{max_chars} characters (including spaces)
- Focus on relevance to the job description
- Maintain factual accuracy based on resume content
- Use professional, impactful language

CURRENT RESUME SUMMARY:
{resume_summary}

JOB OPPORTUNITY:
Title: {job_title}
Company: {company}
Description: {job_description}

Return ONLY this YAML structure:
summary: "Your tailored professional summary here (must be {min_chars}-{max_chars} characters)"
character_count: [actual character count]
"""

class SkillsGenerator(SectionGenerator):
    """Generator for core skills section."""
    
    def __init__(self, config: Optional[Dict] = None, cache: Optional[AIContentCache] = None):
        super().__init__("skills", config, cache)
        self.skills_count = 12
        self.columns = 3
        self.skill_char_limit = (20, 36)
    
    def generate_content(self, resume_data: dict, job_data: dict) -> dict:
        """Generate 12 most relevant skills in 3 columns with strict validation and retry."""
        current_skills = resume_data.get('skills', [])
        
        prompt = self.get_prompt_template().format(
            current_skills=', '.join(current_skills),
            job_title=job_data.get('title', ''),
            job_description=job_data.get('description', ''),
            skills_count=self.skills_count,
            min_chars=self.skill_char_limit[0],
            max_chars=self.skill_char_limit[1]
        )
        
        # Retry logic for validation failures
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Skills generation attempt {attempt + 1}/{max_retries}")
                response = self._make_llm_call(prompt)
                content = self._parse_yaml_response(response)
                
                # Strict validation - will raise ValueError if invalid
                self._validate_skills_content(content)
                
                self.logger.info(f"Skills validation passed on attempt {attempt + 1}")
                return content
                
            except ValueError as e:
                self.logger.warning(f"Skills validation failed on attempt {attempt + 1}: {str(e)}")
                if attempt == max_retries - 1:
                    self.logger.error(f"Skills generation failed after {max_retries} attempts")
                    raise
                else:
                    self.logger.info(f"Retrying skills generation (attempt {attempt + 2}/{max_retries})")
                    # Add emphasis to prompt for retry
                    prompt += f"\n\nRETRY #{attempt + 2}: Previous attempt failed validation. ENSURE each skill is exactly {self.skill_char_limit[0]}-{self.skill_char_limit[1]} characters and based ONLY on existing skills."
    
    def _validate_skills_content(self, content: dict):
        """Validate skills content structure and character limits with STRICT enforcement."""
        validation_errors = []
        
        for col_num in range(1, 4):
            col_key = f"column{col_num}"
            if col_key not in content:
                validation_errors.append(f"Missing {col_key} in skills content")
                continue
            
            skills = content[col_key]
            if not isinstance(skills, list) or len(skills) != 4:
                validation_errors.append(f"{col_key} must contain exactly 4 skills")
                continue
            
            for skill in skills:
                char_count = len(skill)
                if char_count < self.skill_char_limit[0] or char_count > self.skill_char_limit[1]:
                    validation_errors.append(f"Skill '{skill}' has {char_count} characters, must be {self.skill_char_limit[0]}-{self.skill_char_limit[1]}")
        
        if validation_errors:
            error_msg = "SKILLS VALIDATION FAILED - REGENERATING: " + "; ".join(validation_errors)
            self.logger.error(error_msg)
            raise ValueError(error_msg)
    
    def get_prompt_template(self) -> str:
        return """
CRITICAL: Select and organize the {skills_count} most relevant skills for this job opportunity.

🚨 ABSOLUTE REQUIREMENTS - FAILURE TO COMPLY WILL RESULT IN REGENERATION:
1. NEVER FABRICATE OR INVENT NEW SKILLS - Only use skills from the current skills list or logical combinations/expansions of existing skills
2. Each skill MUST be exactly {min_chars}-{max_chars} characters (count spaces and punctuation)
3. Organize into exactly 3 columns of exactly 4 skills each
4. Only select skills that actually exist in the candidate's background

CURRENT SKILLS (DO NOT ADD SKILLS NOT LISTED HERE):
{current_skills}

JOB OPPORTUNITY:
Title: {job_title}
Description: {job_description}

INSTRUCTIONS:
- Choose ONLY from existing skills or combine/expand existing short skills
- Example: "AWS" → "AWS cloud services" (if AWS is in current skills)
- Example: "SQL" → "SQL database management" (if SQL is in current skills)
- NEVER add completely new skills not represented in the current skills list
- Each skill must be {min_chars}-{max_chars} characters exactly
- Prioritize job relevance from existing skills only

Return ONLY this YAML structure:
column1:
  - "Existing skill 1 expanded ({min_chars}-{max_chars} chars)"
  - "Existing skill 2 expanded ({min_chars}-{max_chars} chars)"
  - "Existing skill 3 expanded ({min_chars}-{max_chars} chars)"
  - "Existing skill 4 expanded ({min_chars}-{max_chars} chars)"
column2:
  - "Existing skill 5 expanded ({min_chars}-{max_chars} chars)"
  - "Existing skill 6 expanded ({min_chars}-{max_chars} chars)"
  - "Existing skill 7 expanded ({min_chars}-{max_chars} chars)"
  - "Existing skill 8 expanded ({min_chars}-{max_chars} chars)"
column3:
  - "Existing skill 9 expanded ({min_chars}-{max_chars} chars)"
  - "Existing skill 10 expanded ({min_chars}-{max_chars} chars)"
  - "Existing skill 11 expanded ({min_chars}-{max_chars} chars)"
  - "Existing skill 12 expanded ({min_chars}-{max_chars} chars)"
"""

class HighlightsGenerator(SectionGenerator):
    """Generator for selected achievements/highlights section."""
    
    def __init__(self, config: Optional[Dict] = None, cache: Optional[AIContentCache] = None):
        super().__init__("highlights", config, cache)
        self.highlights_count = 5
        self.highlight_char_limit = (300, 350)
    
    def generate_content(self, resume_data: dict, job_data: dict) -> dict:
        """Generate 5 achievement highlights tailored to the job."""
        prompt = self.get_prompt_template().format(
            resume_summary=resume_data.get('Summary', ''),
            experience_data=yaml.dump(resume_data.get('experience', []), default_flow_style=False),
            job_title=job_data.get('title', ''),
            job_description=job_data.get('description', ''),
            company=job_data.get('company', ''),
            highlights_count=self.highlights_count,
            min_chars=self.highlight_char_limit[0],
            max_chars=self.highlight_char_limit[1]
        )
        
        response = self._make_llm_call(prompt)
        content = self._parse_yaml_response(response)
        
        # Validate character counts
        highlights = content.get('highlights', [])
        for i, highlight in enumerate(highlights):
            char_count = len(highlight)
            if char_count < self.highlight_char_limit[0] or char_count > self.highlight_char_limit[1]:
                self.logger.warning(f"Highlight {i+1} character count {char_count} outside limits {self.highlight_char_limit}")
        
        return content
    
    def get_prompt_template(self) -> str:
        return """
Create {highlights_count} selected achievements/highlights tailored to this specific job opportunity.

REQUIREMENTS:
- Each highlight must be {min_chars}-{max_chars} characters (including spaces)
- Focus on accomplishments that directly relate to the job requirements
- Use quantifiable results when possible (numbers, percentages, dollar amounts)
- Maintain factual accuracy based on resume content
- NEVER fabricate achievements not present in the resume

CURRENT RESUME SUMMARY:
{resume_summary}

EXPERIENCE DATA:
{experience_data}

JOB OPPORTUNITY:
Title: {job_title}
Company: {company}
Description: {job_description}

Return ONLY this YAML structure:
highlights:
  - "First achievement highlighting most relevant accomplishment ({min_chars}-{max_chars} chars)"
  - "Second achievement with quantifiable results ({min_chars}-{max_chars} chars)"
  - "Third achievement demonstrating relevant skills ({min_chars}-{max_chars} chars)"
  - "Fourth achievement showing leadership/impact ({min_chars}-{max_chars} chars)"
  - "Fifth achievement relevant to job requirements ({min_chars}-{max_chars} chars)"
company_name: "{company}"
"""

class ExperienceGenerator(SectionGenerator):
    """Generator for work experience section."""
    
    def __init__(self, config: Optional[Dict] = None, cache: Optional[AIContentCache] = None):
        super().__init__("experience", config, cache)
        self.bullet_limits = [(90, 115), (180, 240)]  # Short or long bullets
    
    def generate_content(self, resume_data: dict, job_data: dict) -> dict:
        """Generate work experience with optimized bullets."""
        experience = resume_data.get('experience', [])
        
        prompt = self.get_prompt_template().format(
            experience_data=yaml.dump(experience, default_flow_style=False),
            job_title=job_data.get('title', ''),
            job_description=job_data.get('description', ''),
            short_min=self.bullet_limits[0][0],
            short_max=self.bullet_limits[0][1],
            long_min=self.bullet_limits[1][0],
            long_max=self.bullet_limits[1][1]
        )
        
        response = self._make_llm_call(prompt)
        content = self._parse_yaml_response(response)
        
        # Validate bullet character counts
        self._validate_experience_content(content)
        
        return content
    
    def _validate_experience_content(self, content: dict):
        """Validate experience bullet character counts."""
        experience = content.get('experience', [])
        
        for exp in experience:
            roles = exp.get('roles', [])
            for role in roles:
                bullets = role.get('bullets', [])
                for bullet in bullets:
                    char_count = len(bullet)
                    
                    # Check if bullet fits allowed ranges (allow 1-5 character buffer)
                    valid_short = (self.bullet_limits[0][0] - 5) <= char_count <= (self.bullet_limits[0][1] + 5)
                    valid_long = (self.bullet_limits[1][0] - 5) <= char_count <= (self.bullet_limits[1][1] + 5)
                    
                    if not (valid_short or valid_long):
                        self.logger.warning(f"Bullet character count {char_count} outside allowed ranges: {self.bullet_limits}")
                    else:
                        self.logger.debug(f"Bullet character count {char_count} within acceptable range")
    
    def get_prompt_template(self) -> str:
        return """
Optimize work experience for this job opportunity while maintaining factual accuracy.

REQUIREMENTS:
- Reorder bullets within each role to prioritize job-relevant accomplishments
- Each bullet must be {short_min}-{short_max} OR {long_min}-{long_max} characters
- Company descriptions should be brief without "Company:" prefix
- Maintain original company and role order from resume

CURRENT EXPERIENCE:
{experience_data}

JOB OPPORTUNITY:
Title: {job_title}
Description: {job_description}

Return ONLY this YAML structure:
experience:
  - company: "Company Name Only"
    description: "Brief company description"
    roles:
      - title: "Role Title"
        dates: "Date Range"
        bullets:
          - "Bullet 1 ({short_min}-{short_max} or {long_min}-{long_max} chars)"
          - "Bullet 2 ({short_min}-{short_max} or {long_min}-{long_max} chars)"
"""

class EducationGenerator(SectionGenerator):
    """Generator for education section."""
    
    def __init__(self, config: Optional[Dict] = None, cache: Optional[AIContentCache] = None):
        super().__init__("education", config, cache)
    
    def generate_content(self, resume_data: dict, job_data: dict) -> dict:
        """Generate education entries without dates (no LLM needed)."""
        education = resume_data.get('education', [])
        
        # Simple reformatting without LLM call - just remove dates
        formatted_education = []
        for edu in education:
            formatted_education.append({
                'course': edu.get('course', 'Unknown Course'),
                'school': edu.get('school', 'Unknown School')
            })
        
        return {'education': formatted_education}
    
    def get_prompt_template(self) -> str:
        # Education doesn't need LLM generation, just reformatting
        return ""

class AwardsGenerator(SectionGenerator):
    """Generator for awards and keynotes section."""
    
    def __init__(self, config: Optional[Dict] = None, cache: Optional[AIContentCache] = None):
        super().__init__("awards", config, cache)
    
    def generate_content(self, resume_data: dict, job_data: dict) -> dict:
        """Generate awards entries without dates."""
        awards = resume_data.get('awards_and_keynotes', [])
        
        # For awards, we just reformat without dates
        formatted_awards = []
        for award in awards:
            formatted_awards.append({
                'title': award.get('award', 'Unknown Award')
            })
        
        return {'awards': formatted_awards}
    
    def get_prompt_template(self) -> str:
        # Awards don't need LLM generation, just reformatting
        return ""

class CoverLetterGenerator(SectionGenerator):
    """Generator for cover letter content."""
    
    def __init__(self, config: Optional[Dict] = None, cache: Optional[AIContentCache] = None):
        super().__init__("cover_letter", config, cache)
        self.max_words = 350
    
    def generate_content(self, resume_data: dict, job_data: dict) -> dict:
        """Generate professional cover letter content."""
        prompt = self.get_prompt_template().format(
            candidate_name=resume_data.get('name', 'Candidate'),
            job_title=job_data.get('title', ''),
            company=job_data.get('company', ''),
            job_description=job_data.get('description', ''),
            resume_summary=resume_data.get('Summary', ''),
            max_words=self.max_words
        )
        
        response = self._make_llm_call(prompt)
        content = self._parse_yaml_response(response)
        
        # Validate word count
        body_text = ' '.join(content.get('body_paragraphs', []))
        word_count = len(body_text.split())
        
        if word_count > self.max_words:
            self.logger.warning(f"Cover letter word count {word_count} exceeds limit {self.max_words}")
        
        return content
    
    def get_prompt_template(self) -> str:
        return """
Create professional cover letter content tailored to this job opportunity.

REQUIREMENTS:
- Maximum {max_words} words for body content
- Professional and engaging tone
- Highlight relevant experience and fit for role
- Structure with opening, body paragraphs, and closing

CANDIDATE INFO:
Name: {candidate_name}
Summary: {resume_summary}

JOB OPPORTUNITY:
Title: {job_title}
Company: {company}
Description: {job_description}

Return ONLY this YAML structure:
opening: "Dear {company} hiring team,"
body_paragraphs:
  - "First paragraph focusing on role fit and interest"
  - "Second paragraph highlighting relevant achievements"
  - "Third paragraph with call to action"
closing: "Thank you,\\n\\n{candidate_name}"
word_count: [actual word count of body paragraphs]
"""

class SectionManager:
    """
    Manages section identification and generator creation.
    
    Determines which sections to generate based on resume data
    and creates appropriate generators for each section.
    """
    
    def __init__(self):
        self.generator_classes = {
            SectionType.SUMMARY: SummaryGenerator,
            SectionType.SKILLS: SkillsGenerator,
            SectionType.HIGHLIGHTS: HighlightsGenerator,
            SectionType.EXPERIENCE: ExperienceGenerator,
            SectionType.EDUCATION: EducationGenerator,
            SectionType.AWARDS: AwardsGenerator,
            SectionType.COVER_LETTER: CoverLetterGenerator
        }
    
    def identify_sections(self, resume_data: dict) -> List[SectionConfig]:
        """
        Identify sections to generate based on resume data.
        
        Args:
            resume_data: Resume information from YAML file
            
        Returns:
            List of SectionConfig objects (exactly 7 core sections)
        """
        sections = []
        
        # Always generate these 7 core sections
        sections.append(SectionConfig(SectionType.SUMMARY, priority=1, required=True))
        sections.append(SectionConfig(SectionType.SKILLS, priority=2, required=True))
        sections.append(SectionConfig(SectionType.HIGHLIGHTS, priority=3, required=True))
        sections.append(SectionConfig(SectionType.EXPERIENCE, priority=4, required=True))
        sections.append(SectionConfig(SectionType.EDUCATION, priority=5, required=True))
        sections.append(SectionConfig(SectionType.AWARDS, priority=6, required=True))
        sections.append(SectionConfig(SectionType.COVER_LETTER, priority=7, required=True))
        
        # Note: Awards are handled within the template, not as a separate generator
        
        # Sort by priority
        sections.sort(key=lambda x: x.priority)
        
        return sections
    
    def create_section_generators(self, sections: List[SectionConfig], cache: Optional[AIContentCache] = None) -> List[SectionGenerator]:
        """
        Create appropriate generators for each section.
        
        Args:
            sections: List of SectionConfig objects
            cache: Optional AIContentCache instance for saving/loading content
            
        Returns:
            List of SectionGenerator instances
        """
        generators = []
        
        for section_config in sections:
            generator_class = self.generator_classes.get(section_config.section_type)
            if generator_class:
                generator = generator_class(cache=cache)
                generators.append(generator)
            else:
                logger.warning(f"No generator found for section type: {section_config.section_type}")
        
        return generators