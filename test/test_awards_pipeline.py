#!/usr/bin/env python3
"""Test the full Awards section pipeline"""

import sys
sys.path.append('src')

def test_full_awards_pipeline():
    """Test Awards section through the entire pipeline"""
    
    try:
        # Test 1: Load actual resume data
        from step2_generate import load_resume_file
        resume_data = load_resume_file('Stephen_Hilton')
        
        print("📋 RESUME DATA:")
        awards_data = resume_data.get('awards_and_keynotes', [])
        print(f"   Awards in resume: {len(awards_data)}")
        for i, award in enumerate(awards_data):
            print(f"   {i+1}. {award.get('award', 'Unknown')}")
        
        # Test 2: Section generation
        from utils.section_generators import SectionManager, AwardsGenerator
        
        sm = SectionManager()
        sections = sm.identify_sections(resume_data)
        awards_sections = [s for s in sections if s.section_type.value == 'awards']
        
        print(f"\n🔧 SECTION GENERATION:")
        print(f"   Awards section identified: {len(awards_sections) > 0}")
        
        if awards_sections:
            awards_gen = AwardsGenerator()
            job_data = {'title': 'Test Job', 'company': 'Test Company'}
            awards_content = awards_gen.generate_content(resume_data, job_data)
            print(f"   Generated awards content: {awards_content}")
        
        # Test 3: Content aggregation
        from utils.content_aggregator import ContentAggregator
        
        aggregator = ContentAggregator()
        
        # Mock section results as they would come from the modular generator
        section_results = {
            'summary': {'status': 'completed', 'content': {'summary': 'Test summary'}},
            'skills': {'status': 'completed', 'content': {'skills': {'technical': ['Python'], 'soft': ['Leadership']}}},
            'highlights': {'status': 'completed', 'content': {'highlights': {'items': ['Test highlight']}}},
            'experience': {'status': 'completed', 'content': {'experience': []}},
            'education': {'status': 'completed', 'content': {'education': []}},
            'awards': {'status': 'completed', 'content': awards_content if 'awards_content' in locals() else {'awards': []}},
            'cover_letter': {'status': 'completed', 'content': {'opening': 'Dear Test', 'body_paragraphs': ['Test'], 'closing': 'Sincerely'}}
        }
        
        aggregated = aggregator.aggregate_sections(section_results, resume_data)
        
        print(f"\n📊 CONTENT AGGREGATION:")
        print(f"   Awards in aggregated content: {len(aggregated.get('awards', []))}")
        for i, award in enumerate(aggregated.get('awards', [])):
            print(f"   {i+1}. {award.get('title', 'Unknown')}")
        
        # Test 4: Template rendering
        from utils.template_engine import TemplateEngine
        
        template_engine = TemplateEngine()
        html_content = template_engine.render_resume(aggregated)
        
        print(f"\n🖼️  TEMPLATE RENDERING:")
        has_awards_section = 'Awards & Recognition' in html_content
        print(f"   Awards section in HTML: {has_awards_section}")
        
        if has_awards_section:
            # Count award items in HTML
            import re
            award_items = re.findall(r'<div class="resume_award_item">(.*?)</div>', html_content)
            print(f"   Award items in HTML: {len(award_items)}")
            for i, item in enumerate(award_items):
                print(f"   {i+1}. {item}")
        
        return len(aggregated.get('awards', [])) > 0 and has_awards_section
        
    except Exception as e:
        print(f"❌ Awards pipeline test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_full_awards_pipeline()
    print(f"\n🎯 AWARDS PIPELINE: {'WORKING' if success else 'BROKEN'}")
    exit(0 if success else 1)