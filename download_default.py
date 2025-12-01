from nudenet import NudeDetector
import os
import shutil

print("Initializing NudeDetector (this triggers download if missing)...")
try:
    detector = NudeDetector()
    print("NudeDetector initialized successfully.")
except Exception as e:
    print(f"Failed to initialize: {e}")

home = os.path.expanduser("~")
nudenet_dir = os.path.join(home, ".NudeNet")
print(f"Checking {nudenet_dir}")

if os.path.exists(nudenet_dir):
    files = os.listdir(nudenet_dir)
    print(f"Files in .NudeNet: {files}")
    
    dest_dir = r"e:\Anti-Lust app\backend\data\models"
    for f in files:
        if f.endswith(".onnx"):
            src = os.path.join(nudenet_dir, f)
            dst = os.path.join(dest_dir, f)
            print(f"Copying {src} to {dst}")
            shutil.copy2(src, dst)
else:
    print(".NudeNet directory not found.")
