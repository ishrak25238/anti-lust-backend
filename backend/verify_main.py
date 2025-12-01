import sys
import os

sys.path.append(os.getcwd())

print("Attempting to import main...")
try:
    from main import app
    print("Successfully imported app from main")
except Exception as e:
    print(f"Failed to import main: {e}")
    import traceback
    traceback.print_exc()
