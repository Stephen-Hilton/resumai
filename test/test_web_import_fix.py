#!/usr/bin/env python3
"""
Test that step2_generate can be imported from web app context.
This simulates the exact import scenario that was failing in the web app.
"""

import sys
from pathlib import Path

def test_web_app_import_scenario():
    """Test the exact import scenario used by the web app."""
    try:
        # Simulate what the web app does - add parent directory to path
        parent_dir = Path(__file__).parent / "src"
        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))
        
        # Now try to import step2_generate like the web app does
        import step2_generate
        
        print("✓ step2_generate imported successfully from web app context")
        
        # Test that we can access a function from it
        if hasattr(step2_generate, 'generate'):
            print("✓ step2_generate.generate function is accessible")
            return True
        else:
            print("✗ step2_generate.generate function not found")
            return False
            
    except ImportError as e:
        print(f"✗ Failed to import step2_generate from web app context: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_direct_import():
    """Test direct import of step2_generate."""
    try:
        # Reset sys.path to clean state
        original_path = sys.path.copy()
        
        # Add src to path like our tests do
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        from src import step2_generate
        print("✓ Direct import of src.step2_generate works")
        
        # Restore original path
        sys.path = original_path
        return True
        
    except ImportError as e:
        print(f"✗ Direct import failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Web App Import Fix")
    print("=" * 50)
    
    success = True
    success &= test_web_app_import_scenario()
    success &= test_direct_import()
    
    print("=" * 50)
    if success:
        print("✓ All web import tests PASSED")
    else:
        print("✗ Web import tests FAILED")
    
    sys.exit(0 if success else 1)