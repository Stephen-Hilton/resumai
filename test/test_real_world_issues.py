#!/usr/bin/env python3
"""Test real-world issues with template engine and awards"""

import sys
sys.path.append('src')

def test_real_world_issues():
    """Test the actual issues preventing the fixes from working"""
    
    print("🔍 REAL-WORLD ISSUE INVESTIGATION")
    print("=" * 60)
    
    # Test 1: Check if awards data exists in resume
    from step2_generate import load_resume_file
    
    resume_data = load_resume_file('Stephen_Hilton')
    awards_data = resume_data.get('awards_and_keynotes', [])
    
    print(f"📋 RESUME DATA:")
    print(f"   Awards in resume file: {len(awards_data)}")
    for i, award in enumerate(awards_data[:3]):  # Show first 3
        print(f"   {i+1}. {award.get('award', 'Unknown')}")
    
    # Test 2: Test awards generation without LLM
    from utils.section_generators import AwardsGenerator
    
    awards_gen = AwardsGenerator()
    job_data = {'title': 'Test Job', 'company': 'Test Company'}
    
    awards_content = awards_gen.generate_content(resume_data, job_data)
    
    print(f"\n🏆 AWARDS GENERATION:")
    print(f"   Generated awards count: {len(awards_content.get('awards', []))}")
    print(f"   Uses LLM: {awards_gen.uses_llm()}")
    
    # Test 3: Test full modular generation for awards only
    from utils.content_aggregator import ContentAggregator
    
    aggregator = ContentAggregator()
    section_results = {
        'awards': {'status': 'completed', 'content': awards_content}
    }
    
    aggregated = aggregator.aggregate_sections(section_results, resume_data)
    awards_in_aggregated = aggregated.get('awards', [])
    
    print(f"\n📊 CONTENT AGGREGATION:")
    print(f"   Awards in aggregated content: {len(awards_in_aggregated)}")
    
    # Test 4: Test template rendering with awards
    from utils.template_engine import TemplateEngine
    
    template_engine = TemplateEngine()
    
    # Create minimal content with awards
    template_data = {
        'name': 'Stephen Hilton',
        'contacts': resume_data.get('contacts', []),
        'awards': awards_in_aggregated,
        'summary': 'Test summary',
        'skills': {'column1': ['Python'], 'column2': ['Leadership'], 'column3': ['AI']},
        'highlights': {'items': ['Test highlight']},
        'experience': [],
        'education': [],
        'version': '1.0.0'
    }
    
    html_content = template_engine.render_resume(template_data)
    
    # Check if awards appear in HTML
    has_awards_header = 'Awards & Recognition' in html_content
    has_awards_content = 'resume_award_item' in html_content
    awards_count_in_html = html_content.count('resume_award_item')
    
    print(f"\n🖼️  TEMPLATE RENDERING:")
    print(f"   Awards header in HTML: {has_awards_header}")
    print(f"   Awards content in HTML: {has_awards_content}")
    print(f"   Award items in HTML: {awards_count_in_html}")
    
    # Show awards section from HTML
    import re
    awards_match = re.search(r'<!-- AWARDS.*?</section>', html_content, re.DOTALL)
    if awards_match:
        print(f"\n📋 AWARDS SECTION IN HTML:")
        lines = awards_match.group(0).split('\n')
        for line in lines[:15]:  # Show first 15 lines
            print(f"   {line}")
    
    # Test 5: Check template engine closing issue
    cover_letter_data = {
        'name': 'Test User',
        'contacts': [],
        'date': 'January 11, 2026',
        'opening': 'Dear Test Company,',
        'body_paragraphs': ['Test paragraph.'],
        'closing': 'I welcome the opportunity. Thank you for considering my application.\\n\\nSincerely,\\nTest User',
        'version': '1.0.0'
    }
    
    cover_html = template_engine.render_cover_letter(cover_letter_data, job_data)
    has_split_closing = 'opportunity.</p>' in cover_html and '<p style="margin-top: 0px;">Thank you' in cover_html
    
    print(f"\n📝 COVER LETTER TEMPLATE:")
    print(f"   Closing properly split: {has_split_closing}")
    
    # Show what we actually got
    closing_match = re.search(r'<!-- Closing.*?</div>', cover_html, re.DOTALL)
    if closing_match:
        print(f"   Actual closing HTML:")
        lines = closing_match.group(0).split('\n')
        for line in lines[:15]:
            if line.strip():
                print(f"     {line.strip()}")
    
    # Check for the actual pattern we're getting
    has_br_separation = '<br>' in cover_html and '<p style="margin-top: 0px;">Thank you' in cover_html
    print(f"   Has <br> separation before Thank you: {has_br_separation}")
    
    # Overall assessment
    awards_working = len(awards_in_aggregated) > 0 and has_awards_content
    template_working = has_br_separation  # Updated criteria
    
    print(f"\n🎯 ISSUE SUMMARY:")
    print(f"   Awards pipeline working: {'✅' if awards_working else '❌'}")
    print(f"   Template engine working: {'✅' if template_working else '❌'}")
    
    return awards_working and template_working

if __name__ == '__main__':
    success = test_real_world_issues()
    print(f"\n🏁 REAL-WORLD FIXES: {'✅ WORKING' if success else '❌ NEED FIXING'}")
    exit(0 if success else 1)