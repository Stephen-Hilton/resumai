#!/usr/bin/env python3
"""
Test script to verify web-based PDF printing functionality.
"""

import sys
import requests
from pathlib import Path

def test_web_pdf_endpoints():
    """Test that the web PDF endpoints are working"""
    
    base_url = "http://127.0.0.1:5001"
    
    # Test that the server is running
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code != 200:
            print(f"❌ Server not responding correctly: {response.status_code}")
            return False
        print("✅ Flask server is running and responding")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to Flask server: {e}")
        print("Make sure the Flask server is running on port 5001")
        return False
    
    # Get the list of jobs to find a test job
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if "Snowflake" in response.text:
            print("✅ Found test job data in main page")
            
            # Test the print endpoints (we can't actually test the print dialog, but we can test the routes)
            test_folder = "Snowflake.Senior_Director_-_Services_Product_&_Strategy.0000017489.20251229140000"
            
            # Test resume print endpoint
            print_resume_url = f"{base_url}/print_file/{test_folder}/resume"
            response = requests.get(print_resume_url, timeout=10)
            
            if response.status_code == 200 and "window.print()" in response.text:
                print("✅ Resume print endpoint working - contains print script")
            else:
                print(f"❌ Resume print endpoint issue: {response.status_code}")
                return False
            
            # Test cover letter print endpoint
            print_cover_url = f"{base_url}/print_file/{test_folder}/coverletter"
            response = requests.get(print_cover_url, timeout=10)
            
            if response.status_code == 200 and "window.print()" in response.text:
                print("✅ Cover letter print endpoint working - contains print script")
            else:
                print(f"❌ Cover letter print endpoint issue: {response.status_code}")
                return False
            
            return True
        else:
            print("❌ No test job data found")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing endpoints: {e}")
        return False

def main():
    print("Testing Web-based PDF Printing Functionality")
    print("=" * 50)
    
    success = test_web_pdf_endpoints()
    
    if success:
        print("\n✅ All tests passed!")
        print("\nHow to use the PDF printing feature:")
        print("1. Open http://127.0.0.1:5001 in your browser")
        print("2. Find a job application card")
        print("3. Click 'Print Resume PDF' or 'Print Cover PDF' buttons")
        print("4. Your browser's print dialog will open automatically")
        print("5. Choose 'Save as PDF' as the destination")
        print("6. The filename will be pre-populated with job details")
        print("\nThis method uses the browser's native PDF engine for perfect rendering!")
    else:
        print("\n❌ Some tests failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())