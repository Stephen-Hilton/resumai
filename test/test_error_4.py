#!/usr/bin/env python3
"""
Test for Error 4: Template Engine Not Using Dynamic Content
Tests that templates use dynamic content instead of hardcoded values.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_template_engine_dynamic_content():
    """Test that template engine uses dynamic content properly."""
    try:
        from src.utils.template_engine import TemplateEngine
        
        engine = TemplateEngine()
        
        # Test with specific unique values in the correct format
        test_content = {
            'name': 'UNIQUE_TEST_NAME_12345',
            'email': 'unique.test@example.com',
            'phone': '555-UNIQUE-TEST',
            'summary': 'This is a unique test summary that should appear in output',
            'skills': {
                'column1': ['UniqueSkill1', 'UniqueSkill2'],
                'column2': ['UniqueSkill3'],
                'column3': []
            },
            'experience': [
                {
                    'company': 'Unique Test Corp',
                    'description': 'A unique test company description',
                    'roles': [
                        {
                            'title': 'Unique Test Engineer',
                            'dates': '2023-2024',
                            'bullets': ['Built unique test software with unique features']
                        }
                    ]
                }
            ],
            'education': [
                {
                    'course': 'BS Unique Testing',
                    'school': 'Unique Test University'
                }
            ]
        }
        
        # Generate HTML
        html = engine.render_resume(test_content)
        
        # Check that our unique values appear in the output
        unique_values = [
            'UNIQUE_TEST_NAME_12345',
            'unique.test@example.com',
            '555-UNIQUE-TEST',
            'unique test summary',  # Case insensitive
            'UniqueSkill1',
            'Unique Test Engineer',
            'Unique Test Corp',
            'BS Unique Testing'
        ]
        
        found_values = []
        missing_values = []
        
        for value in unique_values:
            if value.lower() in html.lower():
                found_values.append(value)
            else:
                missing_values.append(value)
        
        if len(found_values) >= 6:  # At least 6 out of 8 unique values should be found
            print(f"✓ Template uses dynamic content ({len(found_values)}/{len(unique_values)} unique values found)")
            return True
        else:
            print(f"✗ Template not using dynamic content properly ({len(found_values)}/{len(unique_values)} unique values found)")
            print(f"Missing values: {missing_values}")
            print("First 1000 chars of generated HTML:")
            print(html[:1000])
            return False
            
    except Exception as e:
        print(f"✗ Failed to test template engine dynamic content: {e}")
        return False

def test_no_hardcoded_placeholders():
    """Test that output doesn't contain hardcoded placeholder values."""
    try:
        from src.utils.template_engine import TemplateEngine
        
        engine = TemplateEngine()
        
        test_content = {
            'name': 'Real Name',
            'email': 'real@email.com',
            'summary': 'Real summary content'
        }
        
        html = engine.render_resume(test_content)
        
        # Common hardcoded placeholders that shouldn't appear
        bad_placeholders = [
            'John Doe',
            'jane.doe@email.com',
            'Your Name Here',
            'Sample Company',
            'Lorem ipsum',
            'placeholder',
            'PLACEHOLDER',
            'TODO',
            'FIXME'
        ]
        
        found_placeholders = []
        for placeholder in bad_placeholders:
            if placeholder.lower() in html.lower():
                found_placeholders.append(placeholder)
        
        if len(found_placeholders) == 0:
            print("✓ No hardcoded placeholders found in output")
            return True
        else:
            print(f"✗ Found hardcoded placeholders: {found_placeholders}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to test for hardcoded placeholders: {e}")
        return False

if __name__ == "__main__":
    print("Testing Error 4: Template Engine Not Using Dynamic Content")
    print("=" * 60)
    
    success = True
    success &= test_template_engine_dynamic_content()
    success &= test_no_hardcoded_placeholders()
    
    print("=" * 60)
    if success:
        print("✓ All Error 4 tests PASSED")
    else:
        print("✗ Error 4 tests FAILED")
    
    sys.exit(0 if success else 1)