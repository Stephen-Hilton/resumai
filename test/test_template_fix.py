#!/usr/bin/env python3
"""
Test script to verify template engine works with embedded CSS
"""

import sys
import os
sys.path.append('src')

from utils.template_engine import TemplateEngine

def test_template_rendering():
    """Test that templates render with embedded CSS"""
    
    # Initialize template engine
    engine = TemplateEngine()
    
    # Sample content data
    content_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '(555) 123-4567',
        'location': 'San Francisco, CA',
        'summary': 'Experienced software engineer with expertise in Python and web development.',
        'skills': {
            'column1': ['Python', 'JavaScript', 'React', 'Node.js'],
            'column2': ['PostgreSQL', 'MongoDB', 'Redis', 'Docker'],
            'column3': ['AWS', 'Git', 'Linux', 'CI/CD']
        },
        'experience': [
            {
                'company': 'Tech Corp',
                'description': 'Leading technology company',
                'roles': [
                    {
                        'title': 'Senior Software Engineer',
                        'dates': '2020 - Present',
                        'bullets': [
                            'Led development of microservices architecture',
                            'Improved system performance by 40%',
                            'Mentored junior developers'
                        ]
                    }
                ]
            }
        ],
        'education': [
            {
                'course': 'Bachelor of Science in Computer Science',
                'school': 'University of California'
            }
        ],
        'awards': [
            {
                'title': 'Employee of the Year 2023'
            }
        ]
    }
    
    job_data = {
        'company': 'Example Corp',
        'title': 'Software Engineer'
    }
    
    print("Testing resume template rendering...")
    try:
        resume_html = engine.render_resume(content_data)
        
        # Check that CSS is embedded
        if '<style>' in resume_html and '.both_body' in resume_html:
            print("✅ Resume template rendered successfully with embedded CSS")
            
            # Save to file for manual inspection
            with open('test_resume_output.html', 'w') as f:
                f.write(resume_html)
            print("✅ Resume HTML saved to test_resume_output.html")
        else:
            print("❌ Resume template missing embedded CSS")
            return False
            
    except Exception as e:
        print(f"❌ Resume template rendering failed: {e}")
        return False
    
    print("\nTesting cover letter template rendering...")
    try:
        # Add cover letter content
        content_data['cover_letter'] = {
            'opening': 'Dear Hiring Manager,',
            'body_paragraphs': [
                'I am writing to express my interest in the Software Engineer position.',
                'My experience in Python and web development makes me a strong candidate.',
                'I look forward to discussing how I can contribute to your team.'
            ],
            'closing': 'Sincerely,\n\nJohn Doe'
        }
        
        cover_letter_html = engine.render_cover_letter(content_data, job_data)
        
        # Check that CSS is embedded
        if '<style>' in cover_letter_html and '.both_body' in cover_letter_html:
            print("✅ Cover letter template rendered successfully with embedded CSS")
            
            # Save to file for manual inspection
            with open('test_cover_letter_output.html', 'w') as f:
                f.write(cover_letter_html)
            print("✅ Cover letter HTML saved to test_cover_letter_output.html")
        else:
            print("❌ Cover letter template missing embedded CSS")
            return False
            
    except Exception as e:
        print(f"❌ Cover letter template rendering failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_template_rendering()
    if success:
        print("\n🎉 All template tests passed! HTML files should now display with proper formatting.")
    else:
        print("\n💥 Template tests failed!")
    
    sys.exit(0 if success else 1)