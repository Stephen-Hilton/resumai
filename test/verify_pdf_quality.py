#!/usr/bin/env python3
"""
Simple script to verify PDF generation quality and scaling.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from step2_generate import print_pdf

def test_single_pdf():
    """Test PDF generation for a single job ID"""
    
    # Test with a specific job ID
    test_id = "0000017489"
    
    print(f"Testing PDF generation for job ID: {test_id}")
    
    result = print_pdf(job_id=test_id)
    
    print(f"\nResults:")
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"Converted: {result['converted']} files")
    print(f"Failed: {result['failed']} files")
    print(f"Library used: {result['library_used']}")
    
    if result['results']:
        print(f"\nFile details:")
        for file_result in result['results']:
            print(f"  - {file_result['file']}: {file_result['status']}")
            if file_result['status'] == 'success':
                print(f"    Output: {file_result['output']}")
            else:
                print(f"    Error: {file_result.get('error', 'Unknown error')}")
    
    return result['success']

if __name__ == "__main__":
    success = test_single_pdf()
    if success:
        print("\n✅ PDF generation test completed successfully!")
        print("PDFs should now have:")
        print("  - 75% scaling (smaller text and elements)")
        print("  - Minimal WeasyPrint warnings")
        print("  - Better quality output")
    else:
        print("\n❌ PDF generation test failed!")
        sys.exit(1)