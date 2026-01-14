#!/usr/bin/env python3
"""Test cover letter formatting changes"""

from pathlib import Path

def test_cover_letter_formatting():
    """Test that cover letter formatting changes are properly implemented"""
    
    template_path = Path('src/resources/templates/cover_letter.html')
    content = template_path.read_text()
    
    # Check for actual <br> tags (visible newlines)
    checks = {
        'Two newlines before date (<br><br>)': '<br><br>' in content,
        'One newline before Dear (<br>)': content.count('<!-- One newline before Dear -->') > 0 and '<br>' in content,
        'One newline after Dear (<br>)': content.count('<!-- One newline after Dear -->') > 0,
        'One newline before last sentence': 'One newline before last sentence' in content and 'loop.last' in content,
        'One newline before thank you (<br>)': content.count('<!-- One newline before thank you') > 0,
        'Loop.last logic for last paragraph': 'loop.last' in content
    }
    
    print('📝 COVER LETTER VISIBLE NEWLINES TEST:')
    print('=' * 50)
    for check, result in checks.items():
        status = '✅' if result else '❌'
        print(f'{status} {check}')
    
    # Count actual <br> tags
    br_count = content.count('<br>')
    print(f'\n📊 VISIBLE NEWLINES SUMMARY:')
    print(f'Total <br> tags: {br_count} (should be 5+)')
    
    # Test PDF CSS changes for <br> handling
    pdf_mgr_path = Path('src/utils/pdf_mgr.py')
    pdf_content = pdf_mgr_path.read_text()
    pdf_br_handling = '.cover_letter_body br' in pdf_content and 'display: block' in pdf_content
    
    print(f'\n🖨️  PDF FORMATTING:')
    print(f'{"✅" if pdf_br_handling else "❌"} PDF CSS handles <br> tags for visible newlines')
    
    # Overall result
    has_visible_newlines = br_count >= 5 and pdf_br_handling
    print(f'\n🎉 VISIBLE NEWLINES: {"IMPLEMENTED" if has_visible_newlines else "MISSING"}')
    
    return has_visible_newlines

if __name__ == '__main__':
    success = test_cover_letter_formatting()
    exit(0 if success else 1)