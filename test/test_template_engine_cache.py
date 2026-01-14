#!/usr/bin/env python3
"""Test if template engine has caching issues"""

import sys
sys.path.append('src')

def test_template_engine_cache():
    """Test template engine to see if it's using updated template"""
    
    from utils.template_engine import TemplateEngine
    
    # Create template engine
    template_engine = TemplateEngine()
    
    # Test data
    cover_letter_data = {
        'name': 'Test User',
        'contacts': [],
        'date': 'January 11, 2026',
        'opening': 'Dear Test Company hiring team,',
        'body_paragraphs': [
            'First paragraph of cover letter content.',
            'Second paragraph with more details.',
            'Third paragraph building the case.'
        ],
        'closing': 'I welcome the opportunity to bring my experience to your organization and partner with leadership to achieve your goals. Thank you for considering my application—I look forward to hearing from you.\\n\\nSincerely,\\nTest User',
        'version': '1.0.0'
    }
    
    job_data = {'title': 'Test Job', 'company': 'Test Company'}
    
    print("🔍 TEMPLATE ENGINE TEST:")
    print("=" * 50)
    
    # Create template engine (force new instance to avoid caching)
    template_engine = TemplateEngine()
    
    # Force Jinja2 to reload templates by clearing cache if it exists
    if hasattr(template_engine.env, 'cache') and template_engine.env.cache:
        template_engine.env.cache.clear()
    
    # Render with template engine
    html_content = template_engine.render_cover_letter(cover_letter_data, job_data)
    
    print(f"📋 Raw closing in data: '{cover_letter_data['closing']}'")
    
    # Check what we got
    has_goals_para = 'achieve your goals.</p>' in html_content
    has_thank_you_para = '<p style="margin-top: 0px;">Thank you for considering' in html_content
    br_count = html_content.count('<br>')
    
    print(f"✅ Goals paragraph found: {has_goals_para}")
    print(f"✅ Thank you paragraph found: {has_thank_you_para}")
    print(f"✅ Total <br> tags: {br_count}")
    
    # Show the closing section
    import re
    closing_match = re.search(r'<!-- One newline before thank you.*?</div>', html_content, re.DOTALL)
    if closing_match:
        closing_html = closing_match.group(0)
        print(f"\n📋 RENDERED CLOSING SECTION:")
        lines = closing_html.split('\n')
        for line in lines:
            if '<p' in line or '<br>' in line or 'Thank you' in line or 'goals' in line:
                print(f"   {line.strip()}")
    else:
        # Look for any closing content
        print(f"\n📋 SEARCHING FOR CLOSING CONTENT:")
        lines = html_content.split('\n')
        for i, line in enumerate(lines):
            if 'closing' in line.lower() or 'thank you' in line.lower():
                print(f"   Line {i}: {line.strip()}")
    
    return has_goals_para and has_thank_you_para

if __name__ == '__main__':
    success = test_template_engine_cache()
    print(f"\n🎯 TEMPLATE ENGINE: {'✅ WORKING' if success else '❌ BROKEN'}")
    exit(0 if success else 1)