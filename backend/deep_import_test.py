"""
Deep Import Test for All Python Files
Actually imports each module to catch runtime errors
"""
import os
import sys
import importlib.util
from pathlib import Path
import traceback

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def test_import_file(filepath, module_name):
    """Attempt to import a Python file"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # Clean up
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            return True, None
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        tb = traceback.format_exc()
        return False, (error_msg, tb)

def main():
    backend_dir = Path.cwd()
    
    # Get all Python files
    python_files = list(backend_dir.rglob('*.py'))
    python_files = [
        f for f in python_files 
        if 'venv' not in str(f) 
        and '__pycache__' not in str(f)
        and '.venv' not in str(f)
        and 'site-packages' not in str(f)
    ]
    python_files.sort()
    
    print("="*100)
    print(f"DEEP IMPORT TEST - Testing {len(python_files)} Python files")
    print("="*100)
    
    # Core service files to test first
    priority_files = [
        'services/ml_core.py',
        'services/ml_service.py',
        'services/ml_evaluation.py',
        'services/ml_training.py',
        'services/notification_service.py',
        'services/parent_child_service.py',
        'services/security_service.py',
        'database.py',
        'main.py',
    ]
    
    results = {
        'success': [],
        'errors': []
    }
    
    # Test each file
    for i, filepath in enumerate(python_files, 1):
        relative_path = str(filepath).replace(str(backend_dir) + '\\', '')
        module_name = f"test_module_{i}"
        
        print(f"\n[{i}/{len(python_files)}] Testing: {relative_path}")
        
        success, error_info = test_import_file(str(filepath), module_name)
        
        if success:
            print(f"  [OK] PASSED")
            results['success'].append(relative_path)
        else:
            print(f"  [ERROR] FAILED")
            print(f"  Error: {error_info[0]}")
            results['errors'].append({
                'file': relative_path,
                'error': error_info[0],
                'traceback': error_info[1]
            })
    
    # Print detailed summary
    print("\n" + "="*100)
    print("DETAILED ERROR REPORT")
    print("="*100)
    
    if results['errors']:
        for err in results['errors']:
            print(f"\n[FAIL] {err['file']}")
            print(f"   {err['error']}")
            print(f"\n   Full traceback:")
            for line in err['traceback'].split('\n')[:20]:  # First 20 lines
                print(f"   {line}")
    else:
        print("\n[SUCCESS] No import errors found!")
    
    # Summary
    print("\n" + "="*100)
    print("SUMMARY")
    print("="*100)
    print(f"Total files tested: {len(python_files)}")
    print(f"[PASS] Successful imports: {len(results['success'])}")
    print(f"[FAIL] Failed imports: {len(results['errors'])}")
    
    if results['errors']:
        print(f"\nFiles with errors:")
        for err in results['errors']:
            print(f"  - {err['file']}")
        sys.exit(1)
    else:
        print(f"\n[SUCCESS] ALL FILES IMPORTED SUCCESSFULLY!")
        sys.exit(0)

if __name__ == "__main__":
    main()

