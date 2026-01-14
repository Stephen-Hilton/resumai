#!/usr/bin/env python3
"""Test Awards section generation and display"""

import sys
sys.path.append('src')

def test_awards_section():
    """Test that Awards section is properly generated and displayed"""
    
    try:
        from utils.section_generators import SectionManager, AwardsGenerator
        
        # Test 1: Check if AwardsGenerator exists and works
        awards_gen = AwardsGenerator()
        
        # Mock resume data with awards
        resume_data = {
            'name': 'Test User',
            'awards_and_keynotes': [
                {'award': 'Best Developer Award'},
                {'award': 'Innovation Excellence'}
            ]
        }
        
        job_data = {'title': 'Test Job', 'company': 'Test Company'}
        
        # Generate awards content
        awards_content = awards_gen.generate_content(resume_data, job_data)
        print(f"✅ Awards Generator works: {awards_content}")
        
        # Test 2: Check section manager includes awards
        sm = SectionManager()
        sections = sm.identify_sections(resume_data)
        awards_sections = [s for s in sections if s.section_type.value == 'awards']
        
        print(f"✅ Awards section identified: {len(awards_sections) > 0}")
        print(f"   Awards section details: {awards_sections[0].section_type.value if awards_sections else 'None'}")
        
        # Test 3: Check template engine
        from utils.template_engine import TemplateEngine
        template_engine = TemplateEngine()
        
        # Mock aggregated content
        aggregated_content = {
            'name': 'Test User',
            'awards': [
                {'title': 'Best Developer Award'},
                {'title': 'Innovation Excellence'}
            ]
        }
        
        # Check if template renders awards
        html_content = template_engine.render_resume(aggregated_content)
        has_awards_section = 'Awards & Recognition' in html_content
        has_awards_content = 'Best Developer Award' in html_content
        
        print(f"✅ Template includes Awards section: {has_awards_section}")
        print(f"✅ Template includes Awards content: {has_awards_content}")
        
        # Test 4: Check for duplicate awards line in template engine
        from pathlib import Path
        template_engine_path = Path('src/utils/template_engine.py')
        content = template_engine_path.read_text()
        awards_lines = [line for line in content.split('\n') if "'awards':" in line]
        
        print(f"⚠️  Awards lines in template_engine.py: {len(awards_lines)}")
        for i, line in enumerate(awards_lines):
            print(f"   {i+1}: {line.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Awards section test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_awards_section()
    exit(0 if success else 1)