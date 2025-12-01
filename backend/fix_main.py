"""
Quick script to fix corrupted main.py
"""
import re

with open('main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Original file: {len(lines)} lines")

good_lines = []
for i, line in enumerate(lines):
    if i < 443:
        good_lines.append(line)
    elif '# Initialize database on startup' in line:
        good_lines.extend(lines[i:])
        break

fixed_content = ''.join(good_lines)

fixed_content = fixed_content.replace(
    '''    return {
        "status": "healthy",
        "stripe": payment_service.is_configured(),
        "email": email_service.is_configured(),
        "ml": ml_service.is_loaded(),
        "database": "connected"
    """''',
    '''    return {
        "status": "healthy",
        "stripe": payment_service.is_configured(),
        "email": email_service.is_configured(),
        "ml": ml_service.is_loaded(),
        "database": "connected"
    }'''
)

with open('main_fixed.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print(f"Fixed file written to main_fixed.py")
print(f"Lines: {len(fixed_content.splitlines())}")
