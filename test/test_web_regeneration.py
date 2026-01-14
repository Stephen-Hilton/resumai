#!/usr/bin/env python3
"""
Test that simulates the exact web app regeneration scenario that was failing.
"""

import sys
import os
from pathlib import Path

def test_web_app_regeneration_import():
    """Test the exact import scenario that happens during web app regeneration."""
    try:
        # Simulate the web app's import setup
        parent_dir = Path(__file__).parent / "src"
        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))
        
        print("Testing web app regeneration import scenario...")
        
        # This is the exact import that was failing in the web app
        import step2_generate
        
        print("✓ step2_generate imported successfully")
        
        # Test that the generate function exists and is callable
        if hasattr(step2_generate, 'generate'):
            print("✓ step2_generate.generate function is available")
            
            # Test that we can access the function without it crashing on import
            generate_func = step2_generate.generate
            print("✓ step2_generate.generate function is accessible")
            
            return True
        else:
            print("✗ step2_generate.generate function not found")
            return False
            
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_logging_setup_import():
    """Test that logging_setup can be imported in web context."""
    try:
        # Reset and set up path like web app
        parent_dir = Path(__file__).parent / "src"
        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))
        
        from utils import logging_setup
        print("✓ logging_setup imported successfully from web context")
        return True
        
    except ImportError as e:
        print(f"✗ logging_setup import failed: {e}")
        return False

def test_version_import():
    """Test that version can be imported in web context."""
    try:
        # Reset and set up path like web app
        parent_dir = Path(__file__).parent / "src"
        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))
        
        from utils.version import get_version
        version = get_version()
        print(f"✓ version imported successfully: {version}")
        return True
        
    except ImportError as e:
        print(f"✗ version import failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Web App Regeneration Fix")
    print("=" * 50)
    
    success = True
    success &= test_logging_setup_import()
    success &= test_version_import()
    success &= test_web_app_regeneration_import()
    
    print("=" * 50)
    if success:
        print("✅ All web app regeneration tests PASSED")
        print("The web app should now be able to regenerate jobs without import errors!")
    else:
        print("❌ Web app regeneration tests FAILED")
    
    sys.exit(0 if success else 1)