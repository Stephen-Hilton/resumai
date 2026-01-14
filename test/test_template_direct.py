#!/usr/bin/env python3
"""Test template directly"""

import sys
sys.path.append('src')

def test_template_direct():
    """Test the template engine directly with our closing content"""
    
    from pathlib import Path
    
    # Read the actual template file
    template_path = Path('src/resources/templates/cover_letter.html')
    template_content = template_path.read_text()
    
    print("🔍 TEMPLATE ANALYSIS:")
    print("=" * 50)
    
    # Check if our logic is in the template
    has_thank_you_logic = '. Thank you' in template_content
    print(f"✅ Template has '. Thank you' logic: {has_thank_you_logic}")
    
    # Check for the specific patterns
    has_split_logic = 'closing_clean.split' in template_content
    print(f"✅ Template has split logic: {has_split_logic}")
    
    # Show the closing section
    import re
    closing_section = re.search(r'<!-- One newline before thank you.*?{% endif %}', template_content, re.DOTALL)
    if closing_section:
        print(f"\n📋 TEMPLATE CLOSING SECTION:")
        lines = closing_section.group(0).split('\n')
        for i, line in enumerate(lines[:20]):  # Show first 20 lines
            print(f"   {i+1:2d}: {line}")
    
    # Test with Jinja2 directly
    from jinja2 import Template
    
    # Extract just the closing logic from our template
    closing_template = '''
    {% set closing_clean = closing|replace('\\\\n', ' ')|replace('  ', ' ') %}
    {% if '. Thank you' in closing_clean %}
      {% set parts = closing_clean.split('. Thank you') %}
      <p style="margin-top: 15px;">{{ parts[0] }}.</p>
      <br>
      <p style="margin-top: 0px;">Thank you{{ parts[1] }}</p>
    {% else %}
      <p style="margin-top: 15px;">{{ closing|replace('\\\\n', '<br>')|safe }}</p>
    {% endif %}
    '''
    
    template = Template(closing_template)
    
    test_closing = 'I welcome the opportunity to bring my experience to your organization and partner with leadership to achieve your goals. Thank you for considering my application—I look forward to hearing from you.\\n\\nSincerely,\\nTest User'
    
    result = template.render(closing=test_closing)
    
    print(f"\n🧪 DIRECT TEMPLATE TEST:")
    print("=" * 30)
    print(result)
    
    # Check if it worked
    has_goals_para = 'achieve your goals.</p>' in result
    has_thank_you_para = '<p style="margin-top: 0px;">Thank you for considering' in result
    
    print(f"\n📊 RESULTS:")
    print(f"   Goals paragraph: {'✅' if has_goals_para else '❌'}")
    print(f"   Thank you paragraph: {'✅' if has_thank_you_para else '❌'}")
    
    return has_goals_para and has_thank_you_para

if __name__ == '__main__':
    success = test_template_direct()
    print(f"\n🎯 TEMPLATE LOGIC: {'✅ WORKING' if success else '❌ BROKEN'}")
    exit(0 if success else 1)