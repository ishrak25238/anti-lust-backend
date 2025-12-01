import os
import re
from pathlib import Path

def remove_dart_comments(content):
    lines = content.split('\n')
    new_lines = []
    in_multiline_comment = False
    in_doc_comment = False
    
    for line in lines:
        stripped = line.lstrip()
        
        if stripped.startswith('///'):
            new_lines.append(line)
            continue
        
        if '/*' in line and '*/' in line:
            line = re.sub(r'/\*.*?\*/', '', line)
        elif '/**' in line:
            in_doc_comment = True
            new_lines.append(line)
            continue
        elif '/*' in line:
            in_multiline_comment = True
            line = line.split('/*')[0].rstrip()
            if not line:
                continue
        elif '*/' in line:
            if in_doc_comment:
                new_lines.append(line)
                in_doc_comment = False
            in_multiline_comment = False
            continue
        elif in_multiline_comment:
            if not in_doc_comment:
                continue
            else:
                new_lines.append(line)
                continue
        
        if '//' in line and not in_doc_comment:
            if '"' in line or "'" in line:
                quote_pos = min(
                    line.find('"') if '"' in line else len(line),  
                    line.find("'") if "'" in line else len(line)
                )
                comment_pos = line.find('//')
                if comment_pos < quote_pos:
                    line = line.split('//')[0].rstrip()
            else:
                line = line.split('//')[0].rstrip()
        
        if line or not stripped.startswith('//'):
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def process_dart_files(directory):
    total_removed = 0
    files_processed = 0
    
    for root, dirs, files in os.walk(directory):
        if 'build' in dirs:
            dirs.remove('build')
        if '.dart_tool' in dirs:
            dirs.remove('.dart_tool')
        
        for file in files:
            if file.endswith('.dart'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        original = f.read()
                    
                    new_content = remove_dart_comments(original)
                    
                    if new_content != original:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        removed_lines = len(original.split('\n')) - len(new_content.split('\n'))
                        if removed_lines > 0:
                            print(f"+ {file_path}: Removed {removed_lines} comment lines")
                            total_removed += removed_lines
                    
                    files_processed += 1
                    
                except Exception as e:
                    print(f"x Error processing {file_path}: {e}")
    
    return files_processed, total_removed

if __name__ == "__main__":
    flutter_dir = Path(__file__).parent / "anti_lust_guardian"
    
    if not flutter_dir.exists():
        print(f"Error: Flutter directory not found at {flutter_dir}")
        exit(1)
    
    print("Starting comment removal from Dart/Flutter files...")
    print(f"Processing directory: {flutter_dir}\n")
    
    files, comments = process_dart_files(str(flutter_dir))
    
    print(f"\nComplete!")
    print(f"Files processed: {files}")
    print(f"Comment lines removed: {comments}")
