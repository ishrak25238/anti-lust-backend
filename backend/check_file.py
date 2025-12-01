import os

path = r"E:\Anti-Lust app\backend\data\models\640m.onnx"
print(f"Checking {path}")
if os.path.exists(path):
    print(f"File exists. Size: {os.path.getsize(path)} bytes")
else:
    print("File does not exist")
    print(f"Contents of parent dir: {os.listdir(os.path.dirname(path))}")
