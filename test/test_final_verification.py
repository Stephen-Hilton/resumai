#!/usr/bin/env python3
"""Final verification test for cover letter formatting and awards section"""

import sys
sys.path.append('src')

def test_cover_letter_newlines():
    """Test that cover letter has visible newlines"""
    from pathlib import Path
    
    template_path = Path('src/resources/templates/cover_letter.html')
    content = template_path.read_text()
    
    br_count = content.count('<br>')
    has_double_br = '<br><br>' in content
    
    print(f"📝 COVER LETTER NEWLINES:")
    print(f"   Total <br> tags: {br_count}")
    print(f"   Has double newlines: {has_double_br}")
    
    return br_count >= 5 and has_double_br

def test_awards_section():
    """Test that awards section works end-to-end"""
    from step2_generate import load_resume_file
    from utils.section_generators import AwardsGenerator
    from utils.content_aggregator import ContentAggregator
    from utils.template_engine import TemplateEngine
    
    # Load resume with awards
    resume_data = load_resume_file('Stephen_Hilton')
    awards_count = len(resume_data.get('awards_and_keynotes', []))
    
    # Generate awards content
    awards_gen = AwardsGenerator()
    job_data = {'title': 'Test Job', 'company': 'Test Company'}
    awards_content = awards_gen.generate_content(resume_data, job_data)
    
    # Aggregate content
    aggregator = ContentAggregator()
    section_results = {
        'awards': {'status': 'completed', 'content': awards_content}
    }
    aggregated = aggregator.aggregate_sections(section_results, resume_data)
    
    # Render template
    template_engine = TemplateEngine()
    html_content = template_engine.render_resume(aggregated)
    
    has_awards_section = 'Awards & Recognition' in html_content
    awards_in_html = len([line for line in html_content.split('\n') if 'resume_award_item' in line])
    
    print(f"\n🏆 AWARDS SECTION:")
    print(f"   Awards in resume data: {awards_count}")
    print(f"   Awards section in HTML: {has_awards_section}")
    print(f"   Award items rendered: {awards_in_html}")
    
    return awards_count > 0 and has_awards_section and awards_in_html > 0

def main():
    """Run final verification tests"""
    print("🧪 FINAL VERIFICATION TEST")
    print("=" * 50)
    
    cover_letter_ok = test_cover_letter_newlines()
    awards_ok = test_awards_section()
    
    print(f"\n📊 RESULTS:")
    print(f"   Cover letter newlines: {'✅ WORKING' if cover_letter_ok else '❌ BROKEN'}")
    print(f"   Awards section: {'✅ WORKING' if awards_ok else '❌ BROKEN'}")
    
    overall_success = cover_letter_ok and awards_ok
    print(f"\n🎯 OVERALL: {'✅ ALL ISSUES FIXED' if overall_success else '❌ ISSUES REMAIN'}")
    
    return overall_success

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)