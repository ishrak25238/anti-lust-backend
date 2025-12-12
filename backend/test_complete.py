"""
COMPREHENSIVE SYSTEM TEST - NO LIES, ONLY TRUTH
Tests every single component of the ML system
"""
import sys
import os
import json
import time
from pathlib import Path

# Test results tracker
results = {
    'passed': [],
    'failed': [],
    'warnings': []
}

def test(name, func):
    """Run a test and track results"""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)
    try:
        result = func()
        if result:
            results['passed'].append(name)
            print(f"✅ PASS: {name}")
            return True
        else:
            results['failed'].append(name)
            print(f"❌ FAIL: {name}")
            return False
    except Exception as e:
        results['failed'].append(name)
        print(f"❌ FAIL: {name}")
        print(f"   Error: {e}")
        return False

def print_summary():
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"✅ Passed: {len(results['passed'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"⚠️  Warnings: {len(results['warnings'])}")
    
    if results['failed']:
        print("\n❌ Failed Tests:")
        for test in results['failed']:
            print(f"   - {test}")
    
    if results['warnings']:
        print("\n⚠️  Warnings:")
        for warning in results['warnings']:
            print(f"   - {warning}")
    
    print("="*60)
    return len(results['failed']) == 0

# ============================================================
# FILE EXISTENCE TESTS
# ============================================================

def test_model_file_exists():
    """Verify 640m.pt file exists"""
    model_path = Path(__file__).parent / 'data' / 'models' / '640m.pt'
    exists = model_path.exists()
    if exists:
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"   File: {model_path}")
        print(f"   Size: {size_mb:.1f} MB")
        if size_mb < 40:
            results['warnings'].append(f"640m.pt seems small ({size_mb:.1f} MB, expected ~50 MB)")
    else:
        print(f"   File not found: {model_path}")
    return exists

def test_config_file_exists():
    """Verify model_config.json exists and is valid"""
    config_path = Path(__file__).parent / 'data' / 'models' / 'model_config.json'
    if not config_path.exists():
        print(f"   File not found: {config_path}")
        return False
    
    with open(config_path) as f:
        config = json.load(f)
    
    print(f"   Config loaded successfully")
    print(f"   Vision model: {config.get('vision_model', {}).get('name')}")
    print(f"   Model path: {config.get('vision_model', {}).get('path')}")
    
    return config.get('vision_model', {}).get('path') == '640m.pt'

def test_ml_service_files_exist():
    """Verify all ML service files exist"""
    files = [
        'services/ml_core_real.py',
        'services/ml_service_real.py',
        'services/ml_adapter.py',
        'services/ml_data.py'
    ]
    
    missing = []
    for file in files:
        file_path = Path(__file__).parent / file
        if file_path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NOT FOUND")
            missing.append(file)
    
    return len(missing) == 0

# ============================================================
# IMPORT TESTS
# ============================================================

def test_import_ultralytics():
    """Test ultralytics import"""
    try:
        from ultralytics import YOLO
        print(f"   ✅ Ultralytics imported")
        print(f"   Version: {YOLO.__module__}")
        return True
    except ImportError as e:
        print(f"   ❌ Failed to import ultralytics: {e}")
        return False

def test_import_torch():
    """Test torch import"""
    try:
        import torch
        print(f"   ✅ PyTorch imported")
        print(f"   Version: {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
        return True
    except ImportError as e:
        print(f"   ❌ Failed to import torch: {e}")
        return False

def test_import_cv2():
    """Test OpenCV import"""
    try:
        import cv2
        print(f"   ✅ OpenCV imported")
        print(f"   Version: {cv2.__version__}")
        return True
    except ImportError as e:
        print(f"   ❌ Failed to import cv2: {e}")
        return False

def test_import_numpy():
    """Test NumPy import"""
    try:
        import numpy as np
        print(f"   ✅ NumPy imported")
        print(f"   Version: {np.__version__}")
        return True
    except ImportError as e:
        print(f"   ❌ Failed to import numpy: {e}")
        return False

# ============================================================
# MODEL LOADING TESTS
# ============================================================

def test_load_yolo_model():
    """Test loading 640m.pt with YOLO"""
    try:
        from ultralytics import YOLO
        model_path = Path(__file__).parent / 'data' / 'models' / '640m.pt'
        
        print(f"   Loading model from: {model_path}")
        start_time = time.time()
        
        model = YOLO(str(model_path))
        
        load_time = time.time() - start_time
        print(f"   ✅ Model loaded in {load_time:.2f} seconds")
        print(f"   Model type: {type(model)}")
        
        # Try to get model info
        try:
            print(f"   Model has {len(model.names)} classes")
            print(f"   Classes: {list(model.names.values())}")
        except:
            pass
        
        return True
    except Exception as e:
        print(f"   ❌ Failed to load model: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================
# SERVICE INITIALIZATION TESTS
# ============================================================

def test_ml_core_init():
    """Test RealNSFWImageClassifier initialization"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from services.ml_core_real import RealNSFWImageClassifier
        
        print(f"   Initializing RealNSFWImageClassifier...")
        classifier = RealNSFWImageClassifier()
        
        print(f"   ✅ Classifier initialized")
        print(f"   Model type: {type(classifier.model)}")
        print(f"   Labels: {list(classifier.labels.values())}")
        
        return True
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ml_service_init():
    """Test RealMLService initialization"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from services.ml_service_real import RealMLService
        
        print(f"   Initializing RealMLService...")
        service = RealMLService()
        
        print(f"   ✅ Service initialized")
        print(f"   Vision model loaded: {service.vision_model is not None}")
        print(f"   Text model loaded: {service.text_model is not None}")
        
        return True
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ml_adapter_init():
    """Test MLServiceAdapter initialization"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from services.ml_adapter import MLServiceAdapter
        
        print(f"   Initializing MLServiceAdapter...")
        adapter = MLServiceAdapter()
        
        print(f"   ✅ Adapter initialized")
        print(f"   Loaded: {adapter.is_loaded()}")
        
        health = adapter.get_health()
        print(f"   Health status:")
        print(f"      Status: {health.get('status')}")
        print(f"      NSFW Model: {health.get('models', {}).get('nsfw')}")
        print(f"      Text Model: {health.get('models', {}).get('text')}")
        
        return adapter.is_loaded()
    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================
# INFERENCE TESTS
# ============================================================

def test_create_dummy_image():
    """Create a test image"""
    try:
        import numpy as np
        import cv2
        
        # Create a simple test image (100x100 red square)
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :] = (0, 0, 255)  # Red in BGR
        
        # Encode to JPEG bytes
        success, buffer = cv2.imencode('.jpg', img)
        if not success:
            print(f"   ❌ Failed to encode image")
            return None
        
        image_bytes = buffer.tobytes()
        print(f"   ✅ Created test image ({len(image_bytes)} bytes)")
        
        return image_bytes
    except Exception as e:
        print(f"   ❌ Failed to create test image: {e}")
        return None

def test_inference_with_classifier():
    """Test actual inference with RealNSFWImageClassifier"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from services.ml_core_real import RealNSFWImageClassifier
        
        classifier = RealNSFWImageClassifier()
        
        # Create test image
        image_bytes = test_create_dummy_image()
        if not image_bytes:
            return False
        
        print(f"   Running inference...")
        start_time = time.time()
        
        score = classifier.predict(image_bytes)
        
        inference_time = time.time() - start_time
        
        print(f"   ✅ Inference completed in {inference_time:.3f} seconds")
        print(f"   Score: {score:.4f}")
        print(f"   Is NSFW: {score > 0.5}")
        
        return True
    except Exception as e:
        print(f"   ❌ Inference failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_inference_with_service():
    """Test async inference with RealMLService"""
    try:
        import asyncio
        sys.path.insert(0, str(Path(__file__).parent))
        from services.ml_service_real import RealMLService
        
        service = RealMLService()
        
        # Create test image
        image_bytes = test_create_dummy_image()
        if not image_bytes:
            return False
        
        print(f"   Running async inference...")
        
        async def run_test():
            start_time = time.time()
            result = await service.scan_image(image_bytes)
            inference_time = time.time() - start_time
            
            print(f"   ✅ Async inference completed in {inference_time:.3f} seconds")
            print(f"   Is safe: {result.is_safe}")
            print(f"   Score: {result.score:.4f}")
            print(f"   Flags: {result.flags}")
            print(f"   Latency: {result.latency_ms:.1f} ms")
            
            return True
        
        return asyncio.run(run_test())
    except Exception as e:
        print(f"   ❌ Async inference failed: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================
# RUN ALL TESTS
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("COMPREHENSIVE SYSTEM TEST")
    print("Testing NudeNet 640m Integration")
    print("="*60)
    
    # File existence tests
    test("Model file (640m.pt) exists", test_model_file_exists)
    test("Config file exists and valid", test_config_file_exists)
    test("ML service files exist", test_ml_service_files_exist)
    
    # Import tests
    test("Import ultralytics", test_import_ultralytics)
    test("Import torch", test_import_torch)
    test("Import OpenCV", test_import_cv2)
    test("Import NumPy", test_import_numpy)
    
    # Model loading tests
    test("Load YOLO model directly", test_load_yolo_model)
    
    # Service initialization tests
    test("Initialize RealNSFWImageClassifier", test_ml_core_init)
    test("Initialize RealMLService", test_ml_service_init)
    test("Initialize MLServiceAdapter", test_ml_adapter_init)
    
    # Inference tests
    test("Run inference with classifier", test_inference_with_classifier)
    test("Run async inference with service", test_inference_with_service)
    
    # Print summary
    success = print_summary()
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("System is ready for production use.")
        sys.exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED!")
        print("Review failed tests above.")
        sys.exit(1)
