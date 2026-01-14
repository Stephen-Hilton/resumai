#!/usr/bin/env python3
"""Test that newline is added before the last sentence in cover letter closing"""

import sys
sys.path.append('src')

def test_last_sentence_newline():
    """Test that cover letter template adds newline before last sentence"""
    
    try:
        from utils.template_engine import TemplateEngine
        
        # Mock cover letter data with multi-sentence closing
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
        
        # Render template
        template_engine = TemplateEngine()
        html_content = template_engine.render_cover_letter(cover_letter_data, {})
        
        print("📝 LAST SENTENCE NEWLINE TEST:")
        print("=" * 50)
        
        # Check for sentence splitting logic
        has_sentence_split = 'closing_parts = closing.split' in open('src/resources/templates/cover_letter.html').read()
        print(f"✅ Template has sentence splitting logic: {has_sentence_split}")
        
        # Debug: Show the actual closing content
        print(f"📋 Raw closing content: '{cover_letter_data['closing']}'")
        
        # Check for multiple <br> tags (should have more now)
        br_count = html_content.count('<br>')
        print(f"✅ Total <br> tags in rendered HTML: {br_count}")
        
        # Look for the pattern where closing is split
        has_split_closing = 'Thank you for considering' in html_content
        print(f"✅ Closing content rendered: {has_split_closing}")
        
        # Check if there are separate paragraph tags for closing parts
        closing_paragraphs = html_content.count('<p style="margin-top: 0px;">')
        print(f"✅ Last sentence paragraphs: {closing_paragraphs}")
        
        # Check for the specific pattern we expect
        has_goals_paragraph = 'achieve your goals.</p>' in html_content
        has_thank_you_paragraph = '<p style="margin-top: 0px;">Thank you for considering' in html_content
        
        print(f"✅ Goals paragraph found: {has_goals_paragraph}")
        print(f"✅ Thank you paragraph found: {has_thank_you_paragraph}")
        
        # Extract the closing section for inspection
        import re
        closing_section = re.search(r'<!-- Closing.*?</div>', html_content, re.DOTALL)
        if closing_section:
            closing_html = closing_section.group(0)
            print(f"\n📋 CLOSING SECTION HTML:")
            # Show just the key parts
            lines = closing_html.split('\n')
            for line in lines:
                if '<p' in line or '<br>' in line or 'Thank you' in line:
                    print(f"   {line.strip()}")
        
        # Success if we have proper sentence splitting with newline before "Thank you"
        success = has_goals_paragraph and has_thank_you_paragraph and closing_paragraphs >= 1
        
        print(f"\n🎯 LAST SENTENCE NEWLINE: {'✅ WORKING' if success else '❌ BROKEN'}")
        return success
        
    except Exception as e:
        print(f"❌ Last sentence newline test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_last_sentence_newline()
    exit(0 if success else 1)