import os
import re
from pathlib import Path

def strip_comments_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('#') and not stripped.startswith('#!'):
            continue
        cleaned_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    return len(lines) - len(cleaned_lines)

def process_directory(directory):
    total_removed = 0
    files_processed = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                removed = strip_comments_from_file(file_path)
                if removed > 0:
                    print(f"Removed {removed} comment lines from {file}")
                    total_removed += removed
                files_processed += 1
    
    return files_processed, total_removed

if __name__ == "__main__":
    backend_dir = r"e:\Anti-Lust app\backend"
    files_count, comments_removed = process_directory(backend_dir)
    print(f"\nDone: {files_count} files processed, {comments_removed} comment lines removed")
