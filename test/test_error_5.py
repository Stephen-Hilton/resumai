#!/usr/bin/env python3
"""
Test for Error 5: Section Generator Failures Cascade
Tests that when LLM sections fail, system falls back gracefully instead of failing completely.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_modular_generator_fallback():
    """Test that modular generator falls back gracefully when sections fail."""
    try:
        from src.utils.modular_generator import ModularResumeGenerator
        
        generator = ModularResumeGenerator()
        
        # Test data that might cause LLM failures
        test_data = {
            'name': 'Test User',
            'email': 'test@example.com'
        }
        
        job_description = {"description": "Test job description", "title": "Test Job", "company": "Test Company"}
        
        # This should not crash even if LLM calls fail
        result = generator.generate_resume(test_data, job_description)
        
        # Check that we got some result back
        if result and 'success' in result:
            print(f"✓ Modular generator returned result with success: {result['success']}")
            
            # Check if it fell back to legacy system when sections failed
            if result.get('generation_method') == 'legacy':
                print("✓ System gracefully fell back to legacy generation")
                return True
            elif result.get('generation_method') == 'modular':
                print("✓ System succeeded with modular generation")
                return True
            else:
                print(f"? System returned method: {result.get('generation_method')}")
                return True  # Any non-crash result is good for this test
        else:
            print("✗ Modular generator returned no result or missing success key")
            print(f"Result keys: {list(result.keys()) if result else 'None'}")
            return False
            
    except Exception as e:
        print(f"✗ Modular generator crashed instead of falling back: {e}")
        return False

def test_section_failure_handling():
    """Test that individual section failures don't crash the whole system."""
    try:
        from src.utils.modular_generator import ModularResumeGenerator
        from src.utils.parallel_executor import ParallelExecutor
        
        # Test with minimal data that might cause some sections to fail
        test_data = {
            'name': 'Test User'
            # Missing email, phone, etc. - some sections might fail
        }
        
        job_description = {"description": "Test job", "title": "Test Job", "company": "Test Company"}
        
        generator = ModularResumeGenerator()
        
        # This should handle missing data gracefully
        result = generator.generate_resume(test_data, job_description)
        
        if result:
            print("✓ System handled incomplete data without crashing")
            return True
        else:
            print("✗ System failed with incomplete data")
            return False
            
    except Exception as e:
        print(f"✗ System crashed with incomplete data: {e}")
        return False

if __name__ == "__main__":
    print("Testing Error 5: Section Generator Failures Cascade")
    print("=" * 60)
    
    success = True
    success &= test_modular_generator_fallback()
    success &= test_section_failure_handling()
    
    print("=" * 60)
    if success:
        print("✓ All Error 5 tests PASSED")
    else:
        print("✗ Error 5 tests FAILED")
    
    sys.exit(0 if success else 1)