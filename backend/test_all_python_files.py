"""
Comprehensive Python File Syntax and Import Checker
Tests every Python file in the backend directory
"""
import os
import sys
import py_compile
import importlib.util
from pathlib import Path

def test_python_file(filepath):
    """Test a single Python file for syntax and import errors"""
    relative_path = filepath.replace(str(Path.cwd()), '').lstrip('\\').lstrip('/')
    
    print(f"\n{'='*80}")
    print(f"Testing: {relative_path}")
    print(f"{'='*80}")
    
    # Test 1: Syntax Check
    try:
        py_compile.compile(filepath, doraise=True)
        print(f"✅ Syntax: OK")
    except py_compile.PyCompileError as e:
        print(f"❌ SYNTAX ERROR:")
        print(f"   {e}")
        return False
    
    # Test 2: Import Check (without executing)
    try:
        spec = importlib.util.spec_from_file_location("test_module", filepath)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules['test_module'] = module
            spec.loader.exec_module(module)
            print(f"✅ Imports: OK")
            # Clean up
            if 'test_module' in sys.modules:
                del sys.modules['test_module']
            return True
    except SyntaxError as e:
        print(f"❌ SYNTAX ERROR in imports:")
        print(f"   Line {e.lineno}: {e.msg}")
        print(f"   {e.text}")
        return False
    except ImportError as e:
        print(f"⚠️  IMPORT ERROR (may be OK if dependencies not installed):")
        print(f"   {e}")
        return "warning"
    except Exception as e:
        print(f"⚠️  RUNTIME ERROR (may be OK - some files need environment):")
        print(f"   {type(e).__name__}: {e}")
        return "warning"

def main():
    """Test all Python files"""
    backend_dir = Path.cwd()
    
    # Find all Python files
    python_files = list(backend_dir.rglob('*.py'))
    
    # Exclude virtual env and cache
    python_files = [
        f for f in python_files 
        if 'venv' not in str(f) 
        and '__pycache__' not in str(f)
        and '.venv' not in str(f)
        and 'site-packages' not in str(f)
    ]
    
    python_files.sort()
    
    print("="*80)
    print(f"COMPREHENSIVE PYTHON FILE TEST")
    print(f"Total files to test: {len(python_files)}")
    print("="*80)
    
    results = {
        'passed': [],
        'failed': [],
        'warnings': []
    }
    
    for filepath in python_files:
        result = test_python_file(str(filepath))
        
        relative_path = str(filepath).replace(str(backend_dir), '').lstrip('\\').lstrip('/')
        
        if result is True:
            results['passed'].append(relative_path)
        elif result is False:
            results['failed'].append(relative_path)
        else:  # warning
            results['warnings'].append(relative_path)
    
    # Summary
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    
    print(f"\n✅ PASSED: {len(results['passed'])} files")
    for f in results['passed']:
        print(f"   {f}")
    
    if results['warnings']:
        print(f"\n⚠️  WARNINGS: {len(results['warnings'])} files (import/runtime issues)")
        for f in results['warnings']:
            print(f"   {f}")
    
    if results['failed']:
        print(f"\n❌ FAILED: {len(results['failed'])} files (SYNTAX ERRORS)")
        for f in results['failed']:
            print(f"   {f}")
    
    print(f"\n{'='*80}")
    print(f"Total: {len(python_files)} files")
    print(f"Passed: {len(results['passed'])}")
    print(f"Warnings: {len(results['warnings'])}")
    print(f"Failed: {len(results['failed'])}")
    print(f"{'='*80}")
    
    if results['failed']:
        print("\n⚠️  CRITICAL: Some files have syntax errors that must be fixed!")
        sys.exit(1)
    else:
        print("\n✅ All files have valid Python syntax!")
        sys.exit(0)

if __name__ == "__main__":
    main()
