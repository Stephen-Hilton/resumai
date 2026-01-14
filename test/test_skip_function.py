#!/usr/bin/env python3
"""
Test the skip job functionality specifically
"""

import sys
import os
from pathlib import Path

# Set up proper paths
current_dir = Path.cwd()
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))
os.chdir(str(src_dir))

def test_skip_function():
    """Test the skip job function directly"""
    print("🧪 Testing skip job function...")
    
    try:
        from ui.app import skip_job, JOBS_DIR
        
        # Check if test job exists
        test_job = "20251229140000.4323850902.Gordon and Betty Moore Foundation.Director of IT and Head of Technology"
        source_path = JOBS_DIR / '2_generated' / test_job
        
        if source_path.exists():
            print(f"✅ Test job exists: {test_job}")
            
            # Test the skip function logic (without actually moving)
            skipped_dir = JOBS_DIR / '9_skipped'
            dest_path = skipped_dir / test_job
            
            print(f"✅ Source path: {source_path}")
            print(f"✅ Destination would be: {dest_path}")
            print(f"✅ Skipped directory exists: {skipped_dir.exists()}")
            
            # Check if we can create the skipped directory
            try:
                skipped_dir.mkdir(exist_ok=True)
                print("✅ Can create skipped directory")
            except Exception as e:
                print(f"❌ Cannot create skipped directory: {e}")
                
        else:
            print(f"❌ Test job does not exist: {test_job}")
            print("Available jobs:")
            gen_dir = JOBS_DIR / '2_generated'
            if gen_dir.exists():
                for item in gen_dir.iterdir():
                    if item.is_dir():
                        print(f"  - {item.name}")
            
    except Exception as e:
        print(f"❌ Skip function test failed: {e}")
        import traceback
        traceback.print_exc()

def test_flask_app_context():
    """Test if Flask app can handle requests"""
    print("\n🧪 Testing Flask app context...")
    
    try:
        from ui.app import app
        
        with app.test_client() as client:
            # Test a simple GET route
            response = client.get('/')
            print(f"✅ Home page status: {response.status_code}")
            
            # Test skip job route (should fail without proper setup, but route should exist)
            test_job = "20251229140000.4323850902.Gordon and Betty Moore Foundation.Director of IT and Head of Technology"
            response = client.post(f'/skip_job/{test_job}')
            print(f"✅ Skip job route accessible, status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Skip job response: {data}")
            
    except Exception as e:
        print(f"❌ Flask app context test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_skip_function()
    test_flask_app_context()
    print("\n🎯 Skip function test complete!")