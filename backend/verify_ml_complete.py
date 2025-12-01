import asyncio
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("MLSystemTest")

async def test_1_imports():
    logger.info("="*60)
    logger.info("TEST 1: Import All Components")
    logger.info("="*60)
    try:
        from services.ml_core_real import RealNSFWImageClassifier, RealTextToxicityClassifier
        from services.ml_data import DomainDatabase, KeywordDatabase
        from services.ml_service_real import RealMLService
        logger.info("[OK] All imports successful")
        return True
    except Exception as e:
        logger.error(f"[FAIL] Import error: {e}")
        return False

async def test_2_data_structures():
    logger.info("\n" + "="*60)
    logger.info("TEST 2: Data Structures (Bloom Filter, Trie)")
    logger.info("="*60)
    try:
        from services.ml_data import DomainDatabase, KeywordDatabase
        ddb = DomainDatabase()
        kdb = KeywordDatabase()
        
        assert ddb.is_blocked("pornhub.com"), "Failed to block pornhub.com"
        assert not ddb.is_blocked("google.com"), "False positive on google.com"
        logger.info("[OK] Domain blocking works")
        
        score, kws = kdb.analyze_text("xxx porn sex")
        assert score > 0.5, "Failed to detect keywords"
        assert "porn" in kws or "sex" in kws, "Failed to extract keywords"
        logger.info(f"[OK] Keyword detection works (score: {score:.2f})")
        return True
    except Exception as e:
        logger.error(f"[FAIL] Data structure error: {e}")
        return False

async def test_3_ml_models():
    logger.info("\n" + "="*60)
    logger.info("TEST 3: ML Models Load")
    logger.info("="*60)
    try:
        from services.ml_service_real import RealMLService
        service = RealMLService()
        logger.info("[OK] ML Service initialized")
        logger.info("[INFO] Models loaded:")
        logger.info("  - Image: AdamCodd/vit-base-nsfw-detector (328 MB)")
        logger.info("  - Text: s-nlp/roberta_toxicity_classifier (479 MB)")
        return True, service
    except Exception as e:
        logger.error(f"[FAIL] ML model load error: {e}")
        import traceback
        traceback.print_exc()
        return False, None

async def test_4_text_detection(service):
    logger.info("\n" + "="*60)
    logger.info("TEST 4: Text Detection")
    logger.info("="*60)
    try:
        result = await service.scan_text("Hello world")
        assert result.is_safe, "Safe text marked as unsafe"
        logger.info(f"[OK] Safe text: score={result.score:.3f}")
        
        result = await service.scan_text("xxx hardcore porn sex video")
        assert not result.is_safe, "NSFW text marked as safe"
        logger.info(f"[OK] NSFW text: score={result.score:.3f}")
        return True
    except Exception as e:
        logger.error(f"[FAIL] Text detection error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_5_image_detection(service):
    logger.info("\n" + "="*60)
    logger.info("TEST 5: Image Detection")
    logger.info("="*60)
    try:
        from PIL import Image
        import io
        
        img = Image.new('RGB', (640, 640), color='white')
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        
        result = await service.scan_image(buf.getvalue())
        logger.info(f"[OK] Image scan completed: score={result.score:.3f}, latency={result.latency_ms:.1f}ms")
        return True
    except Exception as e:
        logger.error(f"[FAIL] Image detection error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_6_url_check(service):
    logger.info("\n" + "="*60)
    logger.info("TEST 6: URL Domain Check")
    logger.info("="*60)
    try:
        result = await service.scan_url("https://google.com")
        assert result.is_safe, "Google.com blocked incorrectly"
        logger.info("[OK] Safe URL allowed")
        
        result = await service.scan_url("https://pornhub.com")
        assert not result.is_safe, "Pornhub.com not blocked"
        logger.info("[OK] Blocked URL detected")
        return True
    except Exception as e:
        logger.error(f"[FAIL] URL check error: {e}")
        return False

async def main():
    logger.info("\n" + "="*60)
    logger.info("COMPLETE ML SYSTEM VERIFICATION")
    logger.info("="*60)
    
    results = []
    
    if not await test_1_imports():
        logger.error("\nFATAL: Import test failed. Aborting.")
        return False
    results.append(True)
    
    if not await test_2_data_structures():
        logger.error("\nWARNING: Data structure test failed")
        results.append(False)
    else:
        results.append(True)
    
    success, service = await test_3_ml_models()
    if not success:
        logger.error("\nFATAL: ML models failed to load. Aborting.")
        return False
    results.append(True)
    
    if not await test_4_text_detection(service):
        results.append(False)
    else:
        results.append(True)
    
    if not await test_5_image_detection(service):
        results.append(False)
    else:
        results.append(True)
    
    if not await test_6_url_check(service):
        results.append(False)
    else:
        results.append(True)
    
    logger.info("\n" + "="*60)
    logger.info("FINAL RESULTS")
    logger.info("="*60)
    passed = sum(results)
    total = len(results)
    logger.info(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        logger.info("\n[SUCCESS] ALL TESTS PASSED")
        logger.info("ML System is FULLY FUNCTIONAL")
        return True
    else:
        logger.error(f"\n[FAILURE] {total-passed} test(s) failed")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
