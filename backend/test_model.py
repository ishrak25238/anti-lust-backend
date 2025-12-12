"""
Quick test script to verify NudeNet 640m model is working
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("NudeNet 640m Model Test")
print("=" * 60)

# Test 1: Import ultralytics
print("\n1. Testing ultralytics import...")
try:
    from ultralytics import YOLO
    print("   ✅ Ultralytics imported successfully")
except ImportError as e:
    print(f"   ❌ Failed to import ultralytics: {e}")
    sys.exit(1)

# Test 2: Load model
print("\n2. Testing model load...")
model_path = os.path.join(os.path.dirname(__file__), 'data', 'models', '640m.pt')
print(f"   Model path: {model_path}")

if not os.path.exists(model_path):
    print(f"   ❌ Model file not found!")
    sys.exit(1)

file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
print(f"   Model size: {file_size_mb:.1f} MB")

try:
    model = YOLO(model_path)
    print("   ✅ Model loaded successfully!")
except Exception as e:
    print(f"   ❌ Failed to load model: {e}")
    sys.exit(1)

# Test 3: Test ML Core
print("\n3. Testing ML Core integration...")
try:
    from services.ml_core_real import RealNSFWImageClassifier
    classifier = RealNSFWImageClassifier()
    print("   ✅ ML Core initialized successfully")
except Exception as e:
    print(f"   ❌ Failed to initialize ML Core: {e}")
    sys.exit(1)

# Test 4: Test ML Service
print("\n4. Testing ML Service...")
try:
    from services.ml_service_real import RealMLService
    service = RealMLService()
    print("   ✅ ML Service initialized successfully")
except Exception as e:
    print(f"   ❌ Failed to initialize ML Service: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nNudeNet 640m model is ready to use!")
print("\nTo start backend:")
print("  cd backend")
print("  python -m uvicorn main:app --reload")
