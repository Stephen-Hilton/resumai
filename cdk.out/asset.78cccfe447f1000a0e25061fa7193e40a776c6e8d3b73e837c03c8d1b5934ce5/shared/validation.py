"""
Validation utilities for Lambda functions.

Requirements: 4.4, 12.1
"""
from typing import Dict, List, Tuple, Optional
import re


# Valid job phases
VALID_PHASES = [
    "Search", "Queued", "Generating", "Ready",
    "Applied", "Follow-Up", "Negotiation", "Accepted",
    "Skipped", "Expired", "Errored"
]

# Active phases (for "All Active" filter)
ACTIVE_PHASES = [
    "Search", "Queued", "Generating", "Ready",
    "Applied", "Follow-Up", "Negotiation"
]

# Valid subcomponents
VALID_SUBCOMPONENTS = [
    "contact", "summary", "skills", "highlights",
    "experience", "education", "awards", "coverletter"
]

# Valid generation states
VALID_GENERATION_STATES = ["locked", "ready", "generating", "complete", "error"]

# Valid generation types
VALID_GENERATION_TYPES = ["manual", "ai"]


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username: str) -> Tuple[bool, Optional[str]]:
    """
    Validate username format.
    Returns (is_valid, error_message).
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 30:
        return False, "Username must be at most 30 characters"
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return False, "Username must start with a letter and contain only letters, numbers, and underscores"
    
    return True, None


def validate_job_phase(phase: str) -> bool:
    """Validate job phase is one of the valid values."""
    return phase in VALID_PHASES


def validate_subcomponent(component: str) -> bool:
    """Validate subcomponent name."""
    return component in VALID_SUBCOMPONENTS


def validate_generation_state(state: str) -> bool:
    """Validate generation state."""
    return state in VALID_GENERATION_STATES


def validate_generation_type(gen_type: str) -> bool:
    """Validate generation type."""
    return gen_type in VALID_GENERATION_TYPES


def validate_resume_json(resume_json: Dict) -> Tuple[bool, List[str]]:
    """
    Validate resume JSON against the schema.
    Returns (is_valid, list_of_errors).
    
    Requirements: 4.4
    """
    errors = []
    
    # Required top-level fields
    required_fields = ['contact', 'summary', 'skills', 'highlights', 'experience', 'education', 'awards']
    for field in required_fields:
        if field not in resume_json:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    # Validate contact section
    contact = resume_json.get('contact', {})
    if not isinstance(contact, dict):
        errors.append("contact must be an object")
    else:
        if 'name' not in contact or not contact['name']:
            errors.append("contact.name is required")
        if 'email' not in contact or not contact['email']:
            errors.append("contact.email is required")
        elif not validate_email(contact['email']):
            errors.append("contact.email must be a valid email address")
    
    # Validate summary
    if not isinstance(resume_json.get('summary', ''), str):
        errors.append("summary must be a string")
    
    # Validate skills
    skills = resume_json.get('skills', [])
    if not isinstance(skills, list):
        errors.append("skills must be an array")
    else:
        for i, skill in enumerate(skills):
            if not isinstance(skill, str):
                errors.append(f"skills[{i}] must be a string")
    
    # Validate highlights
    highlights = resume_json.get('highlights', [])
    if not isinstance(highlights, list):
        errors.append("highlights must be an array")
    else:
        for i, highlight in enumerate(highlights):
            if not isinstance(highlight, str):
                errors.append(f"highlights[{i}] must be a string")
    
    # Validate experience
    experience = resume_json.get('experience', [])
    if not isinstance(experience, list):
        errors.append("experience must be an array")
    else:
        for i, exp in enumerate(experience):
            if not isinstance(exp, dict):
                errors.append(f"experience[{i}] must be an object")
            else:
                if 'company' not in exp or not exp['company']:
                    errors.append(f"experience[{i}].company is required")
                if 'title' not in exp or not exp['title']:
                    errors.append(f"experience[{i}].title is required")
                if 'startDate' not in exp or not exp['startDate']:
                    errors.append(f"experience[{i}].startDate is required")
                if 'current' not in exp:
                    errors.append(f"experience[{i}].current is required")
                if 'description' not in exp:
                    errors.append(f"experience[{i}].description is required")
                if 'achievements' not in exp or not isinstance(exp.get('achievements'), list):
                    errors.append(f"experience[{i}].achievements must be an array")
    
    # Validate education
    education = resume_json.get('education', [])
    if not isinstance(education, list):
        errors.append("education must be an array")
    else:
        for i, edu in enumerate(education):
            if not isinstance(edu, dict):
                errors.append(f"education[{i}] must be an object")
            else:
                if 'institution' not in edu or not edu['institution']:
                    errors.append(f"education[{i}].institution is required")
                if 'degree' not in edu or not edu['degree']:
                    errors.append(f"education[{i}].degree is required")
                if 'field' not in edu or not edu['field']:
                    errors.append(f"education[{i}].field is required")
                if 'graduationDate' not in edu or not edu['graduationDate']:
                    errors.append(f"education[{i}].graduationDate is required")
    
    # Validate awards
    awards = resume_json.get('awards', [])
    if not isinstance(awards, list):
        errors.append("awards must be an array")
    else:
        for i, award in enumerate(awards):
            if not isinstance(award, dict):
                errors.append(f"awards[{i}] must be an object")
            else:
                if 'title' not in award or not award['title']:
                    errors.append(f"awards[{i}].title is required")
                if 'issuer' not in award or not award['issuer']:
                    errors.append(f"awards[{i}].issuer is required")
                if 'date' not in award or not award['date']:
                    errors.append(f"awards[{i}].date is required")
    
    return len(errors) == 0, errors


def make_safe_url_segment(text: str) -> str:
    """
    Convert text to a URL-safe segment.
    Used for jobtitlesafe generation.
    """
    # Convert to lowercase
    safe = text.lower()
    # Replace spaces and special chars with hyphens
    safe = re.sub(r'[^a-z0-9]+', '-', safe)
    # Remove leading/trailing hyphens
    safe = safe.strip('-')
    # Collapse multiple hyphens
    safe = re.sub(r'-+', '-', safe)
    # Limit length
    return safe[:50]
