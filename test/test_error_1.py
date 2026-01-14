#!/usr/bin/env python3
"""
Test for Error 1: Import Error in Section Generators
Tests that section generators can be imported and used from web context.
"""

import sys
import os
from pathlib import Path

# Add project root to path to simulate web context
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_section_generators_import():
    """Test that section generators can be imported from web context."""
    try:
        from src.utils.section_generators import SectionManager
        print("✓ Successfully imported SectionManager")
        return True
    except ImportError as e:
        print(f"✗ Failed to import SectionManager: {e}")
        return False

def test_llm_call_import():
    """Test that LLM call can be imported through section generators."""
    try:
        from src.utils.section_generators import SectionManager
        
        # Create instance and try to call a method that uses llm_call
        manager = SectionManager()
        
        # Test with minimal data to see if import works
        test_data = {
            'name': 'Test User',
            'email': 'test@example.com'
        }
        
        # This should not fail on import, even if LLM call fails
        try:
            generator = manager.get_generator('summary')
            result = generator.generate(test_data, "Test job description")
            print("✓ LLM import through section generators works")
            return True
        except Exception as e:
            if "llm_call" in str(e) or "ModuleNotFoundError" in str(e):
                print(f"✗ LLM import failed: {e}")
                return False
            else:
                # Other errors are OK for this test - we just care about imports
                print("✓ LLM import works (other error occurred but not import-related)")
                return True
                
    except ImportError as e:
        print(f"✗ Failed to test LLM import: {e}")
        return False

if __name__ == "__main__":
    print("Testing Error 1: Import Error in Section Generators")
    print("=" * 60)
    
    success = True
    success &= test_section_generators_import()
    success &= test_llm_call_import()
    
    print("=" * 60)
    if success:
        print("✓ All Error 1 tests PASSED")
    else:
        print("✗ Error 1 tests FAILED")
    
    sys.exit(0 if success else 1)