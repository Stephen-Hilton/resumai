#!/usr/bin/env python3
"""
Run all error tests to verify all issues are fixed.
"""

import subprocess
import sys
from pathlib import Path

def run_test(test_file):
    """Run a single test file and return success status."""
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=300)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Test timed out after 5 minutes"

def main():
    print("Running All Error Tests")
    print("=" * 60)
    
    tests = [
        ("Error 1: Import Error in Section Generators", "test_error_1.py"),
        ("Error 2: Missing pdf_mgr Module", "test_error_2.py"),
        ("Error 3: HTML Resume Has No Styling", "test_error_3.py"),
        ("Error 4: Template Engine Not Using Dynamic Content", "test_error_4.py"),
        ("Error 5: Section Generator Failures Cascade", "test_error_5.py"),
        ("Error 6: Path Resolution Issues in Web Context", "test_error_6.py"),
    ]
    
    all_passed = True
    results = []
    
    for description, test_file in tests:
        print(f"\nRunning {description}...")
        if not Path(test_file).exists():
            print(f"✗ Test file {test_file} not found")
            all_passed = False
            results.append((description, False, "Test file not found"))
            continue
            
        success, stdout, stderr = run_test(test_file)
        
        if success:
            print(f"✓ {description} PASSED")
            results.append((description, True, ""))
        else:
            print(f"✗ {description} FAILED")
            all_passed = False
            results.append((description, False, stderr or "Unknown error"))
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    
    for description, passed, error in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {description}")
        if not passed and error:
            print(f"      Error: {error[:100]}...")
    
    print("=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! All errors have been fixed.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())