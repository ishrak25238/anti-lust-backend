import os
import re
from pathlib import Path

def remove_html_comments(content):
    content = re.sub(r'\u003c!--.*?--\u003e', '', content, flags=re.DOTALL)
    return content

def remove_js_comments(content):
    lines = content.split('\n')
    new_lines = []
    in_multiline_comment = False
    
    for line in lines:
        if '/*' in line and '*/' in line:
            line = re.sub(r'/\*.*?\*/', '', line)
        elif '/*' in line:
            in_multiline_comment = True
            line = line.split('/*')[0]
        elif '*/' in line:
            in_multiline_comment = False
            line = line.split('*/')[1]
            continue
        elif in_multiline_comment:
            continue
        
        if not in_multiline_comment and '//' in line:
            if '"' in line or "'" in line:
                pass
            else:
                line = line.split('//')[0].rstrip()
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def remove_css_comments(content):
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return content

def process_web_files(directory):
    total_removed = 0
    files_processed = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    original = f.read()
                
                new_content = original
                
                if file.endswith('.html'):
                    new_content = remove_html_comments(original)
                elif file.endswith('.js'):
                    new_content = remove_js_comments(original)
                elif file.endswith('.css'):
                    new_content = remove_css_comments(original)
                else:
                    continue
                
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
    website_dir = Path(__file__).parent / "website"
    
    if not website_dir.exists():
        print(f"Error: Website directory not found at {website_dir}")
        exit(1)
    
    print("Starting comment removal from website files...")
    print(f"Processing directory: {website_dir}\n")
    
    files, comments = process_web_files(str(website_dir))
    
    print(f"\nComplete!")
    print(f"Files processed: {files}")
    print(f"Comment lines removed: {comments}")
