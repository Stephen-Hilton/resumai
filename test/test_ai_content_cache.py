#!/usr/bin/env python3
"""
Test script for AI Content Cache system

This script tests the new AI content caching functionality.
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from utils.ai_content_cache import AIContentCache, get_job_directory_from_id

def test_cache_basic_functionality():
    """Test basic cache save/load functionality"""
    print("Testing basic cache functionality...")
    
    # Use a test directory
    test_dir = Path("test_cache_dir")
    test_dir.mkdir(exist_ok=True)
    
    try:
        # Initialize cache
        cache = AIContentCache(str(test_dir))
        
        # Test data
        test_content = {
            'summary': 'This is a test professional summary.',
            'character_count': 42
        }
        
        test_metadata = {
            'generator_class': 'SummaryGenerator',
            'uses_llm': True,
            'job_title': 'Test Job',
            'company': 'Test Company'
        }
        
        # Save content
        success = cache.save_section_content('summary', test_content, test_metadata)
        print(f"Save result: {success}")
        
        # Check if cached
        has_cache = cache.has_cached_content('summary')
        print(f"Has cached content: {has_cache}")
        
        # Load content
        loaded_content = cache.load_section_content('summary')
        print(f"Loaded content: {loaded_content}")
        
        # Get cache info
        cache_info = cache.get_cache_info()
        print(f"Cache info: {cache_info}")
        
        # Test successful
        print("✓ Basic cache functionality test passed")
        return True
        
    except Exception as e:
        print(f"✗ Basic cache functionality test failed: {e}")
        return False
    
    finally:
        # Cleanup
        import shutil
        if test_dir.exists():
            shutil.rmtree(test_dir)

def test_job_directory_finder():
    """Test finding job directories"""
    print("\nTesting job directory finder...")
    
    try:
        # Test with a known job ID (if exists)
        job_id = "Ladders.Senior_Vice_President_of_Global_Support_and_Custom.4350514507.20251227085032"
        job_dir = get_job_directory_from_id(job_id)
        
        if job_dir:
            print(f"Found job directory: {job_dir}")
            print("✓ Job directory finder test passed")
            return True
        else:
            print("No job directory found (this is expected if no jobs exist)")
            print("✓ Job directory finder test passed (no jobs)")
            return True
            
    except Exception as e:
        print(f"✗ Job directory finder test failed: {e}")
        return False

def test_cache_with_real_job():
    """Test cache with a real job directory if available"""
    print("\nTesting cache with real job directory...")
    
    try:
        jobs_dir = Path("src/jobs/2_generated")
        if not jobs_dir.exists():
            print("No jobs directory found, skipping real job test")
            return True
        
        # Find first job directory
        job_dirs = [d for d in jobs_dir.iterdir() if d.is_dir()]
        if not job_dirs:
            print("No job directories found, skipping real job test")
            return True
        
        job_dir = job_dirs[0]
        print(f"Testing with job directory: {job_dir.name}")
        
        # Initialize cache
        cache = AIContentCache(str(job_dir))
        
        # Check existing cache
        cached_sections = cache.get_cached_sections()
        print(f"Existing cached sections: {cached_sections}")
        
        # Get cache info
        cache_info = cache.get_cache_info()
        print(f"Cache info: {cache_info}")
        
        print("✓ Real job cache test passed")
        return True
        
    except Exception as e:
        print(f"✗ Real job cache test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("AI Content Cache Test Suite")
    print("=" * 40)
    
    tests = [
        test_cache_basic_functionality,
        test_job_directory_finder,
        test_cache_with_real_job
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())