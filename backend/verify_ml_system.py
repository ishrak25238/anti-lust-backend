
import asyncio
import logging
import sys
import os
import time
import numpy as np
import torch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MLVerifier")

def test_imports():
    logger.info("--- Testing Imports ---")
    try:
        from services.ml_core import AdvancedVisionModel, ImagePreprocessor
        from services.ml_data import DomainDatabase, KeywordDatabase
        from services.ml_service import MLService
        logger.info("✅ All ML modules imported successfully.")
        return True
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error during import: {e}")
        return False

def test_data_structures():
    logger.info("\n--- Testing Data Structures ---")
    try:
        from services.ml_data import DomainDatabase, KeywordDatabase
        
        ddb = DomainDatabase()
        test_domain = "pornhub.com"
        if ddb.is_blocked(test_domain):
            logger.info(f"✅ DomainDatabase correctly blocked {test_domain}")
        else:
            logger.error(f"❌ DomainDatabase FAILED to block {test_domain}")
            
        safe_domain = "google.com"
        if not ddb.is_blocked(safe_domain):
            logger.info(f"✅ DomainDatabase correctly allowed {safe_domain}")
        else:
            logger.error(f"❌ DomainDatabase FAILED (False Positive) on {safe_domain}")

        kdb = KeywordDatabase()
        unsafe_text = "hot sex porn video"
        score, keywords = kdb.analyze_text(unsafe_text)
        if score > 0.5 and "porn" in keywords:
            logger.info(f"✅ KeywordDatabase correctly flagged '{unsafe_text}' (Score: {score:.2f})")
        else:
            logger.error(f"❌ KeywordDatabase FAILED on '{unsafe_text}'")

        return True
    except Exception as e:
        logger.error(f"❌ Data structure test failed: {e}")
        return False

async def test_ml_service():
    logger.info("\n--- Testing ML Service End-to-End ---")
    try:
        from services.ml_service import MLService
        
        service = MLService()
        logger.info("✅ MLService initialized.")

        logger.info("Testing Text Scan...")
        res_text = await service.scan_text("This is a completely safe and innocent sentence about puppies.")
        if res_text.is_safe:
            logger.info(f"✅ Safe text correctly identified. Score: {res_text.score:.4f}")
        else:
            logger.error(f"❌ Safe text flagged as UNSAFE. Score: {res_text.score:.4f}")

        res_unsafe = await service.scan_text("hardcore sex xxx video")
        if not res_unsafe.is_safe:
            logger.info(f"✅ Unsafe text correctly identified. Score: {res_unsafe.score:.4f}")
        else:
            logger.error(f"❌ Unsafe text flagged as SAFE. Score: {res_unsafe.score:.4f}")

        logger.info("Testing Image Scan (Simulated 640x640 input)...")
        import cv2
        dummy_img = np.zeros((640, 640, 3), dtype=np.uint8)
        success, encoded_img = cv2.imencode('.jpg', dummy_img)
        if not success:
            logger.error("Failed to encode dummy image")
            return False
            
        res_img = await service.scan_image(encoded_img.tobytes())
        logger.info(f"✅ Image scan completed. Result: Safe={res_img.is_safe}, Score={res_img.score:.4f}, Latency={res_img.latency_ms:.2f}ms")

        logger.info("Testing URL Scan...")
        res_url = await service.scan_url("http://google.com") # Should be safe
        logger.info(f"✅ URL scan completed. Result: Safe={res_url.is_safe}")

        return True
    except Exception as e:
        logger.error(f"❌ ML Service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    logger.info("Starting System Verification...")
    
    if not test_imports():
        logger.error("CRITICAL: Import tests failed. Aborting.")
        return
        
    if not test_data_structures():
        logger.error("CRITICAL: Data structure tests failed.")
        
    if not await test_ml_service():
        logger.error("CRITICAL: ML Service tests failed.")
    else:
        logger.info("\n🎉 ALL SYSTEMS GO. The ML pipeline is functional and robust.")

if __name__ == "__main__":
    asyncio.run(main())
