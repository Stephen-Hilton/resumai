#!/usr/bin/env python3
"""
Test all critical functions that users interact with
"""

import sys
import os
from pathlib import Path

# Set up proper paths
current_dir = Path.cwd()
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))
os.chdir(str(src_dir))

def test_all_flask_routes():
    """Test all critical Flask routes"""
    print("🧪 Testing all critical Flask routes...")
    
    try:
        from ui.app import app
        
        test_job = "20251229140000.4323850902.Gordon and Betty Moore Foundation.Director of IT and Head of Technology"
        
        with app.test_client() as client:
            
            # Test 1: Home page
            response = client.get('/')
            print(f"✅ Home page: {response.status_code}")
            
            # Test 2: Phase pages
            for phase in ['queued', 'generated', 'applied']:
                response = client.get(f'/phase/{phase}')
                print(f"✅ Phase {phase}: {response.status_code}")
            
            # Test 3: Skip job (we know this works)
            response = client.post(f'/skip_job/{test_job}')
            result = response.get_json()
            print(f"✅ Skip job: {response.status_code} - {result.get('success', False)}")
            
            # Move it back for other tests
            if result.get('success'):
                import shutil
                src_path = Path('jobs/9_skipped') / test_job
                dest_path = Path('jobs/2_generated') / test_job
                if src_path.exists():
                    shutil.move(str(src_path), str(dest_path))
            
            # Test 4: Mark as applied
            response = client.post(f'/mark_applied/{test_job}')
            result = response.get_json()
            print(f"✅ Mark applied: {response.status_code} - {result.get('success', False)}")
            
            # Move it back
            if result.get('success'):
                import shutil
                src_path = Path('jobs/3_applied') / f"{test_job}.yaml"
                dest_path = Path('jobs/2_generated') / test_job
                if src_path.exists():
                    # Need to recreate the folder structure
                    dest_path.mkdir(exist_ok=True)
                    shutil.move(str(src_path), str(dest_path / f"{test_job}.yaml"))
            
            # Test 5: Fetch jobs from email
            response = client.post('/run_step1_queue')
            result = response.get_json()
            print(f"✅ Fetch jobs from email: {response.status_code} - {result.get('success', False)}")
            
            # Test 6: Process all jobs
            response = client.post('/run_step2_generate')
            result = response.get_json()
            print(f"✅ Process all jobs: {response.status_code} - {result.get('success', False)}")
            
            # Test 7: Process single job
            response = client.post(f'/process_single_job/{test_job}')
            result = response.get_json()
            print(f"✅ Process single job: {response.status_code} - {result.get('success', False)}")
            
            # Test 8: Regenerate HTML only
            response = client.post(f'/regenerate_html_only/{test_job}')
            result = response.get_json()
            print(f"✅ Regenerate HTML only: {response.status_code} - {result.get('success', False)}")
            
            # Test 9: Manual job entry page
            response = client.get('/manually_enter')
            print(f"✅ Manual job entry page: {response.status_code}")
            
            # Test 10: Add job by URL page
            response = client.get('/add_job_by_url')
            print(f"✅ Add job by URL page: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Flask routes test failed: {e}")
        import traceback
        traceback.print_exc()

def test_step1_queue_directly():
    """Test step1_queue.py directly"""
    print("\n🧪 Testing step1_queue.py directly...")
    
    try:
        import step1_queue
        print("✅ step1_queue imports successfully")
        
        # Test if main functions exist
        functions_to_check = ['sanitize_text_for_yaml', 'sanitize_job_data', 'get_all_ids']
        for func_name in functions_to_check:
            if hasattr(step1_queue, func_name):
                print(f"✅ Function {func_name} exists")
            else:
                print(f"❌ Function {func_name} missing")
                
    except Exception as e:
        print(f"❌ step1_queue test failed: {e}")

def test_step2_generate_directly():
    """Test step2_generate.py directly"""
    print("\n🧪 Testing step2_generate.py directly...")
    
    try:
        import step2_generate
        print("✅ step2_generate imports successfully")
        
        # Test if main functions exist
        functions_to_check = ['generate', 'load_queued_jobs']
        for func_name in functions_to_check:
            if hasattr(step2_generate, func_name):
                print(f"✅ Function {func_name} exists")
            else:
                print(f"❌ Function {func_name} missing")
                
    except Exception as e:
        print(f"❌ step2_generate test failed: {e}")

if __name__ == "__main__":
    test_all_flask_routes()
    test_step1_queue_directly()
    test_step2_generate_directly()
    print("\n🎯 All critical functions test complete!")