import os

file_path = r"e:\Anti-Lust app\website\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

line_1154 = lines[1153]
line_1349 = lines[1348]

print(f"Line 1154: {line_1154.strip()}")
print(f"Line 1349: {line_1349.strip()}")

if "scale(1.05)" in line_1154 and "scale(1.05)" in line_1349:
    print("Verification successful. Proceeding with slice.")
    
    new_lines = lines[:1154] + lines[1349:]
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"File updated. New line count: {len(new_lines)}")
else:
    print("Verification failed. Aborting.")
