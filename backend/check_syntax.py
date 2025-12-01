"""
Quick Syntax Checker - Validates all Python files
"""
import py_compile
import os
from pathlib import Path

print("=" * 60)
print("PYTHON SYNTAX CHECKER")
print("=" * 60)

backend_dir = Path(__file__).parent
errors = []
success = []

# Get all Python files
python_files = list(backend_dir.rglob("*.py"))
python_files = [f for f in python_files if '__pycache__' not in str(f)]

print(f"\nFound {len(python_files)} Python files to check...\n")

for py_file in python_files:
    relative_path = py_file.relative_to(backend_dir)
    try:
        py_compile.compile(str(py_file), doraise=True)
        print(f"✓ {relative_path}")
        success.append(str(relative_path))
    except py_compile.PyCompileError as e:
        print(f"✗ {relative_path}")
        print(f"  Error: {e}")
        errors.append((str(relative_path), str(e)))

print("\n" + "=" * 60)
print(f"RESULTS: {len(success)} passed, {len(errors)} failed")
print("=" * 60)

if errors:
    print("\n❌ SYNTAX ERRORS FOUND:")
    for file, error in errors:
        print(f"\n{file}:")
        print(f"  {error}")
    exit(1)
else:
    print("\n✅ ALL FILES HAVE VALID SYNTAX!")
    exit(0)
