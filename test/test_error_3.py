#!/usr/bin/env python3
"""
Test for Error 3: HTML Resume Has No Styling
Tests that generated resume HTML contains proper CSS classes and styling.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_template_has_css():
    """Test that the resume template contains CSS styling."""
    try:
        template_path = Path("src/resources/templates/resume.html")
        if not template_path.exists():
            print(f"✗ Template file not found: {template_path}")
            return False
            
        content = template_path.read_text()
        
        # Check for CSS indicators
        css_indicators = [
            "<style>",
            "css",
            "class=",
            "font-family",
            "color:",
            "margin:",
            "padding:"
        ]
        
        found_css = []
        for indicator in css_indicators:
            if indicator in content:
                found_css.append(indicator)
        
        if len(found_css) >= 3:  # At least 3 CSS indicators
            print(f"✓ Template contains CSS styling ({len(found_css)} indicators found)")
            return True
        else:
            print(f"✗ Template lacks proper CSS styling (only {len(found_css)} indicators found)")
            return False
            
    except Exception as e:
        print(f"✗ Failed to check template CSS: {e}")
        return False

def test_template_engine_generates_styled_html():
    """Test that template engine generates HTML with styling."""
    try:
        from src.utils.template_engine import TemplateEngine
        
        engine = TemplateEngine()
        
        # Test data
        test_content = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '555-1234',
            'summary': 'Test summary',
            'skills': ['Python', 'JavaScript'],
            'experience': [
                {
                    'title': 'Software Engineer',
                    'company': 'Test Corp',
                    'duration': '2020-2023',
                    'description': 'Built software'
                }
            ],
            'education': [
                {
                    'degree': 'BS Computer Science',
                    'school': 'Test University',
                    'year': '2020'
                }
            ]
        }
        
        # Generate HTML
        html = engine.render_resume(test_content)
        
        # Check for styling elements
        styling_elements = [
            'class=',
            '<style>',
            'font-family',
            'color:',
            'margin',
            'padding'
        ]
        
        found_styling = []
        for element in styling_elements:
            if element in html:
                found_styling.append(element)
        
        if len(found_styling) >= 3:
            print(f"✓ Generated HTML contains styling ({len(found_styling)} elements found)")
            return True
        else:
            print(f"✗ Generated HTML lacks styling (only {len(found_styling)} elements found)")
            print("First 500 chars of generated HTML:")
            print(html[:500])
            return False
            
    except Exception as e:
        print(f"✗ Failed to test template engine: {e}")
        return False

if __name__ == "__main__":
    print("Testing Error 3: HTML Resume Has No Styling")
    print("=" * 60)
    
    success = True
    success &= test_template_has_css()
    success &= test_template_engine_generates_styled_html()
    
    print("=" * 60)
    if success:
        print("✓ All Error 3 tests PASSED")
    else:
        print("✗ Error 3 tests FAILED")
    
    sys.exit(0 if success else 1)