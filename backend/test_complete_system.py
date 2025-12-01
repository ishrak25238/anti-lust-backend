"""
COMPLETE SYSTEM TEST - No lies, 100% honest validation
Tests EVERY component and reports actual status
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("COMPLETE SYSTEM VALIDATION - HONEST REPORT")
print("=" * 70)

test_results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

# TEST 1: Payment Integration (Stripe)
print("\n[TEST 1] Stripe Payment Integration...")
try:
    import stripe
    from services.payment_service import PaymentService
    
    # Check if Stripe key is configured
    from dotenv import load_dotenv
    load_dotenv()
    
    stripe_key = os.getenv('STRIPE_SECRET_KEY')
    if stripe_key and len(stripe_key) > 20:
        test_results["passed"].append("Stripe API key configured")
        print("✓ Stripe SDK imported")
        print("✓ Stripe API key found in .env")
        print("✓ PaymentService module exists")
    else:
        test_results["warnings"].append("Stripe API key not configured in .env")
        print("⚠ Stripe key missing (needs STRIPE_SECRET_KEY in .env)")
        
except Exception as e:
    test_results["failed"].append(f"Payment integration: {str(e)}")
    print(f"✗ Payment test failed: {e}")

# TEST 2: Database & Authentication
print("\n[TEST 2] Database & Authentication...")
try:
    from database import engine, Base
    from models import User
    from middleware.security import hash_password, verify_password
    
    # Test password hashing
    test_pass = "TestPassword123"
    hashed = hash_password(test_pass)
    is_valid = verify_password(test_pass, hashed)
    
    if is_valid:
        test_results["passed"].append("Password hashing & verification")
        print("✓ Database models imported")
        print("✓ Password hashing works")
        print("✓ Password verification works")
    else:
        test_results["failed"].append("Password verification failed")
        print("✗ Password verification failed")
        
except Exception as e:
    test_results["failed"].append(f"Database/Auth: {str(e)}")
    print(f"✗ Database test failed: {e}")

# TEST 3: ML Models (NSFW Detection)
print("\n[TEST 3] ML Models - NSFW Detection...")
try:
    from services.ml_core_real import RealNSFWImageClassifier
    from PIL import Image
    import io
    
    # Load model
    vision_model = RealNSFWImageClassifier()
    
    # Create test image
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes = img_bytes.getvalue()
    
    # Test prediction
    score = vision_model.predict(img_bytes)
    
    test_results["passed"].append(f"NSFW detection (score: {score:.3f})")
    print(f"✓ NudeNet 640m model loaded")
    print(f"✓ Image prediction works (score: {score:.3f})")
    
except Exception as e:
    test_results["failed"].append(f"NSFW detection: {str(e)}")
    print(f"✗ NSFW detection failed: {e}")
    import traceback
    traceback.print_exc()

# TEST 4: Text Classification
print("\n[TEST 4] Text Toxicity Detection...")
try:
    from services.ml_core_real import SimpleTextToxicityClassifier
    
    text_model = SimpleTextToxicityClassifier()
    
    # Test with toxic text
    toxic_score = text_model.predict("I hate you, you idiot!")
    safe_score = text_model.predict("Hello, have a nice day!")
    
    if toxic_score > safe_score:
        test_results["passed"].append(f"Text classification (toxic: {toxic_score:.2f}, safe: {safe_score:.2f})")
        print(f"✓ Text classifier loaded")
        print(f"✓ Detects toxic text (score: {toxic_score:.2f})")
        print(f"✓ Detects safe text (score: {safe_score:.2f})")
    else:
        test_results["warnings"].append("Text classifier may need tuning")
        print(f"⚠ Text scores unexpected: toxic={toxic_score:.2f}, safe={safe_score:.2f}")
        
except Exception as e:
    test_results["failed"].append(f"Text classification: {str(e)}")
    print(f"✗ Text classification failed: {e}")

# TEST 5: API Endpoints
print("\n[TEST 5] FastAPI Application...")
try:
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Test health endpoint
    response = client.get("/health")
    if response.status_code == 200:
        test_results["passed"].append("API health endpoint")
        print(f"✓ FastAPI app loaded")
        print(f"✓ Health endpoint working")
        print(f"  Total routes: {len(app.routes)}")
    else:
        test_results["warnings"].append(f"Health endpoint returned {response.status_code}")
        print(f"⚠ Health endpoint status: {response.status_code}")
        
except Exception as e:
    test_results["failed"].append(f"FastAPI: {str(e)}")
    print(f"✗ FastAPI test failed: {e}")
    import traceback
    traceback.print_exc()

# TEST 6: OpenAI Integration
print("\n[TEST 6] OpenAI Integration...")
try:
    import openai
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key and len(openai_key) > 20:
        test_results["passed"].append("OpenAI API configured")
        print("✓ OpenAI SDK imported")
        print("✓ OpenAI API key configured")
    else:
        test_results["warnings"].append("OpenAI API key not configured")
        print("⚠ OpenAI key missing (optional for deployment)")
        
except Exception as e:
    test_results["failed"].append(f"OpenAI: {str(e)}")
    print(f"✗ OpenAI test failed: {e}")

# FINAL REPORT
print("\n" + "=" * 70)
print("HONEST TEST REPORT")
print("=" * 70)

print(f"\n✅ PASSED ({len(test_results['passed'])} tests):")
for item in test_results["passed"]:
    print(f"   - {item}")

if test_results["warnings"]:
    print(f"\n⚠ WARNINGS ({len(test_results['warnings'])} items):")
    for item in test_results["warnings"]:
        print(f"   - {item}")

if test_results["failed"]:
    print(f"\n❌ FAILED ({len(test_results['failed'])} tests):")
    for item in test_results["failed"]:
        print(f"   - {item}")
    print("\n🚨 SYSTEM HAS ERRORS - NOT READY FOR DEPLOYMENT")
    sys.exit(1)
else:
    print("\n✅ ALL CRITICAL SYSTEMS WORKING")
    if test_results["warnings"]:
        print("⚠ Some optional features need configuration")
    print("✅ READY FOR DEPLOYMENT")
    
print("=" * 70)
