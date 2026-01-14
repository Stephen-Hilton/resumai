#!/usr/bin/env python3
"""
Quick test to regenerate HTML with updated templates
"""

import sys
sys.path.append('src')

from utils.template_engine import TemplateEngine

# Test the template engine with sample data
template_engine = TemplateEngine()

# Sample content (you can load from YAML instead)
content_data = {
    'name': 'Stephen Hilton',
    'summary': 'Test summary',
    'skills': {'column1': ['Skill 1'], 'column2': ['Skill 2'], 'column3': ['Skill 3']},
    'experience': [],
    'education': [],
    'awards': [],
    'cover_letter': {
        'opening': 'Dear Hiring Team,',
        'body_paragraphs': ['Test paragraph 1', 'Test paragraph 2'],
        'closing': 'Thank you,\n\nStephen Hilton'
    }
}

job_data = {'company': 'Test Company'}

# Generate cover letter with new spacing
cover_letter_html = template_engine.render_cover_letter(content_data, job_data)

# Save test file
with open('test_cover_letter_new_spacing.html', 'w') as f:
    f.write(cover_letter_html)

print("✅ Test cover letter generated: test_cover_letter_new_spacing.html")
print("💡 Open this file in browser to see new spacing")