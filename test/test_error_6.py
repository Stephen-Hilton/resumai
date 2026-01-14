#!/usr/bin/env python3
"""
Test for Error 6: Path Resolution Issues in Web Context
Tests that import paths work correctly when called from web application context.
"""

import sys
import os
from pathlib import Path

# Add project root to path to simulate web context
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_web_context_imports():
    """Test that all modular system imports work from web context."""
    try:
        # Test all the key imports that would be used in web context
        from src.utils.modular_generator import ModularResumeGenerator
        from src.utils.section_generators import SectionManager
        from src.utils.template_engine import TemplateEngine
        from src.utils.content_aggregator import ContentAggregator
        from src.utils.parallel_executor import ParallelExecutor
        from src.utils.ui_feedback_manager import UIFeedbackManager
        
        print("✓ All modular system imports successful from web context")
        return True
        
    except ImportError as e:
        print(f"✗ Import failed in web context: {e}")
        return False

def test_web_context_generation():
    """Test that modular generation works when called from web context."""
    try:
        from src.utils.modular_generator import ModularResumeGenerator
        
        # Simulate web application calling the generator
        generator = ModularResumeGenerator()
        
        # Test data similar to what web app would provide
        resume_data = {
            'name': 'Web Test User',
            'email': 'webtest@example.com',
            'phone': '555-WEB-TEST'
        }
        
        job_data = {
            'description': 'Web context test job',
            'title': 'Web Developer',
            'company': 'Web Test Corp'
        }
        
        # This should work without path resolution issues
        result = generator.generate_resume(resume_data, job_data)
        
        if result and result.get('success'):
            print("✓ Modular generation works correctly from web context")
            return True
        else:
            print("✗ Modular generation failed from web context")
            return False
            
    except Exception as e:
        print(f"✗ Web context generation failed: {e}")
        return False

def test_step2_generate_imports():
    """Test that step2_generate imports work correctly."""
    try:
        # This was one of the problematic imports
        from src.step2_generate import llm_call
        print("✓ step2_generate.llm_call import successful")
        return True
        
    except ImportError as e:
        print(f"✗ step2_generate import failed: {e}")
        return False

def test_cross_module_dependencies():
    """Test that modules can import each other correctly."""
    try:
        # Test the chain of dependencies that was failing
        from src.utils.section_generators import SectionManager, SectionType, SectionConfig
        manager = SectionManager()
        
        # Create a test section config
        test_sections = [
            SectionConfig(
                section_type=SectionType.SUMMARY,
                priority=1,
                required=True
            )
        ]
        
        # This should be able to create generators that use llm_call
        generators = manager.create_section_generators(test_sections)
        if generators:
            print("✓ Cross-module dependencies work correctly")
            return True
        else:
            print("✗ No generators created")
            return False
        
    except Exception as e:
        print(f"✗ Cross-module dependency failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Error 6: Path Resolution Issues in Web Context")
    print("=" * 60)
    
    success = True
    success &= test_web_context_imports()
    success &= test_web_context_generation()
    success &= test_step2_generate_imports()
    success &= test_cross_module_dependencies()
    
    print("=" * 60)
    if success:
        print("✓ All Error 6 tests PASSED")
    else:
        print("✗ Error 6 tests FAILED")
    
    sys.exit(0 if success else 1)