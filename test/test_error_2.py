#!/usr/bin/env python3
"""
Test for Error 2: Missing pdf_mgr Module
Tests that print_pdf function can be imported and called.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_pdf_mgr_import():
    """Test that pdf_mgr can be imported."""
    try:
        from src.utils.pdf_mgr import print_pdf
        print("✓ Successfully imported print_pdf from pdf_mgr")
        return True
    except ImportError as e:
        print(f"✗ Failed to import print_pdf: {e}")
        return False

def test_print_pdf_function():
    """Test that print_pdf function can be called."""
    try:
        from src.utils.pdf_mgr import print_pdf
        
        # Call with no arguments (should handle gracefully)
        result = print_pdf()
        print(f"✓ print_pdf() returned: {result}")
        return True
    except Exception as e:
        print(f"✗ print_pdf() failed: {e}")
        return False

def test_step2_generate_import():
    """Test that step2_generate can import print_pdf correctly."""
    try:
        # This simulates the import that was failing
        from src.utils.pdf_mgr import print_pdf as pdf_print_pdf
        print("✓ step2_generate style import works")
        return True
    except ImportError as e:
        print(f"✗ step2_generate style import failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Error 2: Missing pdf_mgr Module")
    print("=" * 60)
    
    success = True
    success &= test_pdf_mgr_import()
    success &= test_print_pdf_function()
    success &= test_step2_generate_import()
    
    print("=" * 60)
    if success:
        print("✓ All Error 2 tests PASSED")
    else:
        print("✗ Error 2 tests FAILED")
    
    sys.exit(0 if success else 1)