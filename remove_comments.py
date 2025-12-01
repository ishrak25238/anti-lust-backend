import os
import re
import sys
from pathlib import Path

def remove_comments_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    new_lines = []
    in_multiline_string = False
    multiline_delimiter = None
    
    for line in lines:
        stripped = line.lstrip()
        
        if '"""' in line or "'''" in line:
            if '"""' in line:
                delimiter = '"""'
            else:
                delimiter = "'''"
            
            count = line.count(delimiter)
            if count == 2 and not in_multiline_string:
                new_lines.append(line)
                continue
            elif count == 1:
                if not in_multiline_string:
                    in_multiline_string = True
                    multiline_delimiter = delimiter
                elif delimiter == multiline_delimiter:
                    in_multiline_string = False
                    multiline_delimiter = None
            new_lines.append(line)
            continue
        
        if in_multiline_string:
            new_lines.append(line)
            continue
        
        if stripped.startswith('#'):
            continue
        
        if '#' in line and not in_multiline_string:
            before_hash = line.split('#')[0]
            if not any(q in before_hash for q in ['"', "'"]):
                line = before_hash.rstrip() + '\n'
            elif '"#' in line or "'#" in line:
                pass
        
        new_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return len(lines) - len(new_lines)

def process_directory(directory):
    total_removed = 0
    files_processed = 0
    
    for root, dirs, files in os.walk(directory):
        if '__pycache__' in root or '.git' in root:
            continue
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    removed = remove_comments_from_file(file_path)
                    if removed > 0:
                        print(f"+ {file_path}: Removed {removed} comment lines")
                    files_processed += 1
                    total_removed += removed
                except Exception as e:
                    print(f"x Error processing {file_path}: {e}")
    
    return files_processed, total_removed

if __name__ == "__main__":
    backend_dir = Path(__file__).parent / "backend"
    
    if not backend_dir.exists():
        print(f"Error: Backend directory not found at {backend_dir}")
        sys.exit(1)
    
    print("Starting comment removal from Python backend files...")
    print(f"Processing directory: {backend_dir}\n")
    
    files, comments = process_directory(str(backend_dir))
    
    print(f"\nComplete!")
    print(f"Files processed: {files}")
    print(f"Comments removed: {comments}")
