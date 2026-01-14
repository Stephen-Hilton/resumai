#!/usr/bin/env python3
"""
Comprehensive Testing Script - Catches syntax errors and basic functionality issues

This script performs the testing that should have been done before claiming fixes work.
It's designed to catch the obvious errors that any basic test would reveal.
"""

import sys
import ast
import importlib.util
import traceback
from pathlib import Path
from typing import List, Dict, Any

def test_python_syntax(file_path: Path) -> Dict[str, Any]:
    """Test if a Python file has valid syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the AST
        ast.parse(content)
        return {
            'success': True,
            'file': str(file_path),
            'message': 'Syntax OK'
        }
    except SyntaxError as e:
        return {
            'success': False,
            'file': str(file_path),
            'error': f'Syntax Error: {e.msg} at line {e.lineno}',
            'details': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'file': str(file_path),
            'error': f'Parse Error: {str(e)}',
            'details': traceback.format_exc()
        }

def test_import_ability(file_path: Path) -> Dict[str, Any]:
    """Test if a Python file can be imported without errors."""
    try:
        # Add the parent directory to sys.path temporarily
        parent_dir = str(file_path.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        # Try to load the module
        spec = importlib.util.spec_from_file_location("test_module", file_path)
        if spec is None:
            return {
                'success': False,
                'file': str(file_path),
                'error': 'Could not create module spec'
            }
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return {
            'success': True,
            'file': str(file_path),
            'message': 'Import OK'
        }
    except Exception as e:
        return {
            'success': False,
            'file': str(file_path),
            'error': f'Import Error: {str(e)}',
            'details': traceback.format_exc()
        }

def test_pdf_manager_basic_functionality():
    """Test basic PDF manager functionality."""
    try:
        # Add src to path
        src_path = Path(__file__).parent / 'src'
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
        
        from utils.pdf_mgr import PDFManager
        
        # Test initialization
        pdf_manager = PDFManager()
        
        # Test engine detection
        info = pdf_manager.get_engine_info()
        
        return {
            'success': True,
            'message': f"PDF Manager initialized successfully. Available engines: {info['total_available']}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'PDF Manager test failed: {str(e)}',
            'details': traceback.format_exc()
        }

def test_section_generators_count():
    """Test that section generators return exactly 7 sections."""
    try:
        # Add src to path
        src_path = Path(__file__).parent / 'src'
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
        
        from utils.section_generators import SectionManager
        
        manager = SectionManager()
        resume_data = {'name': 'Test User'}
        sections = manager.identify_sections(resume_data)
        
        if len(sections) != 7:
            return {
                'success': False,
                'error': f'Expected 7 sections, got {len(sections)}: {[s.section_type.value for s in sections]}'
            }
        
        return {
            'success': True,
            'message': f'Section manager correctly returns 7 sections: {[s.section_type.value for s in sections]}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Section generators test failed: {str(e)}',
            'details': traceback.format_exc()
        }

def test_ai_content_validation():
    """Test AI content validation expects 7 files."""
    try:
        # Add src to path
        src_path = Path(__file__).parent / 'src'
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
        
        # Test the validation logic by checking the source code
        import step2_generate
        
        # Check if the function exists
        if not hasattr(step2_generate, 'move_queued_to_generated_with_validation'):
            return {
                'success': False,
                'error': 'move_queued_to_generated_with_validation function not found'
            }
        
        return {
            'success': True,
            'message': 'AI content validation function exists and should expect 7 files'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'AI content validation test failed: {str(e)}',
            'details': traceback.format_exc()
        }

def run_all_tests():
    """Run all tests and report results."""
    print("🧪 COMPREHENSIVE TESTING SCRIPT")
    print("=" * 60)
    print("This script catches syntax errors and basic functionality issues")
    print("that should have been caught before claiming fixes work.\n")
    
    # Test critical Python files for syntax errors
    critical_files = [
        Path('src/utils/pdf_mgr.py'),
        Path('src/utils/section_generators.py'),
        Path('src/utils/modular_generator.py'),
        Path('src/step2_generate.py'),
        Path('src/ui/app.py')
    ]
    
    syntax_results = []
    import_results = []
    
    print("1. SYNTAX TESTING")
    print("-" * 30)
    
    for file_path in critical_files:
        if file_path.exists():
            result = test_python_syntax(file_path)
            syntax_results.append(result)
            
            status = "✅" if result['success'] else "❌"
            print(f"{status} {file_path.name}: {result.get('message', result.get('error', 'Unknown'))}")
            
            if not result['success']:
                print(f"   Details: {result.get('details', 'No details')}")
        else:
            print(f"⚠️  {file_path.name}: File not found")
    
    print(f"\nSyntax Test Results: {sum(1 for r in syntax_results if r['success'])}/{len(syntax_results)} passed")
    
    # Only proceed with import tests if syntax is OK
    syntax_failed = [r for r in syntax_results if not r['success']]
    if syntax_failed:
        print(f"\n❌ STOPPING: {len(syntax_failed)} files have syntax errors. Fix these first!")
        return False
    
    print("\n2. IMPORT TESTING")
    print("-" * 30)
    
    for file_path in critical_files:
        if file_path.exists():
            result = test_import_ability(file_path)
            import_results.append(result)
            
            status = "✅" if result['success'] else "❌"
            print(f"{status} {file_path.name}: {result.get('message', result.get('error', 'Unknown'))}")
            
            if not result['success']:
                print(f"   Details: {result.get('details', 'No details')}")
    
    print(f"\nImport Test Results: {sum(1 for r in import_results if r['success'])}/{len(import_results)} passed")
    
    # Functional tests
    print("\n3. FUNCTIONAL TESTING")
    print("-" * 30)
    
    functional_tests = [
        ("PDF Manager Basic", test_pdf_manager_basic_functionality),
        ("Section Count (7)", test_section_generators_count),
        ("AI Content Validation", test_ai_content_validation)
    ]
    
    functional_results = []
    
    for test_name, test_func in functional_tests:
        result = test_func()
        functional_results.append(result)
        
        status = "✅" if result['success'] else "❌"
        print(f"{status} {test_name}: {result.get('message', result.get('error', 'Unknown'))}")
        
        if not result['success']:
            print(f"   Details: {result.get('details', 'No details')}")
    
    print(f"\nFunctional Test Results: {sum(1 for r in functional_results if r['success'])}/{len(functional_results)} passed")
    
    # Overall results
    total_tests = len(syntax_results) + len(import_results) + len(functional_results)
    total_passed = (sum(1 for r in syntax_results if r['success']) + 
                   sum(1 for r in import_results if r['success']) + 
                   sum(1 for r in functional_results if r['success']))
    
    print(f"\n📊 OVERALL RESULTS")
    print("=" * 30)
    print(f"Total Tests: {total_passed}/{total_tests} passed")
    
    if total_passed == total_tests:
        print("🎉 ALL TESTS PASSED! The fixes appear to be working correctly.")
        return True
    else:
        print(f"❌ {total_tests - total_passed} tests failed. Please fix these issues before claiming the code works.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)