#!/usr/bin/env python3
"""
Comprehensive test of all ResumeAI functions to identify broken ones
"""

import sys
import os
from pathlib import Path

# Set up proper paths
current_dir = Path.cwd()
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing imports...")
    
    try:
        # Change to src directory for imports
        os.chdir(str(src_dir))
        
        # Test step1_queue imports
        import step1_queue
        print("✅ step1_queue imports successfully")
    except Exception as e:
        print(f"❌ step1_queue import failed: {e}")
    
    try:
        # Test step2_generate imports
        import step2_generate
        print("✅ step2_generate imports successfully")
    except Exception as e:
        print(f"❌ step2_generate import failed: {e}")
    
    try:
        # Test Flask app imports
        from ui.app import app
        print("✅ Flask app imports successfully")
        
        # Test route registration
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        critical_routes = [
            '/skip_job/<folder_name>',
            '/mark_applied/<folder_name>',
            '/process_single_job/<folder_name>',
            '/run_step1_queue',
            '/run_step2_generate',
            '/regenerate_html_only/<folder_name>'
        ]
        
        for route in critical_routes:
            if route in routes:
                print(f"✅ Route {route} registered")
            else:
                print(f"❌ Route {route} NOT registered")
                
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
        import traceback
        traceback.print_exc()

def test_directory_structure():
    """Test if required directories exist"""
    print("\n🧪 Testing directory structure...")
    
    required_dirs = [
        'src/jobs/1_queued',
        'src/jobs/2_generated', 
        'src/jobs/3_applied',
        'src/jobs/8_errors',
        'src/jobs/9_skipped',
        'src/utils/logs',
        'src/resources/icons',
        'src/resources/templates'
    ]
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ Directory {dir_path} exists")
        else:
            print(f"❌ Directory {dir_path} missing")

def test_file_existence():
    """Test if critical files exist"""
    print("\n🧪 Testing critical files...")
    
    critical_files = [
        'src/utils/gmail_mgr.py',
        'src/utils/parse_linkedin_emails.py',
        'src/utils/logging_setup.py',
        'src/utils/version.py',
        'src/step1_queue.py',
        'src/step2_generate.py',
        'src/ui/app.py'
    ]
    
    for file_path in critical_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ File {file_path} exists")
        else:
            print(f"❌ File {file_path} missing")

if __name__ == "__main__":
    test_imports()
    test_directory_structure()
    test_file_existence()
    print("\n🎯 Test complete!")