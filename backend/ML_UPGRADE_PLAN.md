# Phase 5: ML System Enhancement - Implementation Plan

## Goal
Enable full ML capabilities by switching from degraded mode to real ML models (already installed).

## Changes Needed

### 1. Update main.py
**Line 14**: Change from `from services.ml_service import MLService` to `from services.ml_service_real import RealMLService`
**Line 63**: Change `ml_service = MLService()` to `ml_service = RealMLService()`

### 2. Add Adapter Layer
Create `services/ml_adapter.py` to maintain API compatibility:
- Wraps RealMLService
- Converts ScanResult to old dict format
- Provides: detect_nsfw(), classify_text(), analyze_url()

## What's Already Working
✅ Real NSFW detection model installed (Falconsai/nsfw_image_detection)
✅ Real text toxicity model installed (unitary/toxic-bert)
✅ Models cached in HuggingFace cache
✅ Test file verified working (test_real_models.py)

## Testing Steps
1. Load real service: `python -c "from services.ml_service_real import RealMLService; ml = RealMLService()"`
2. Run test file: `python test_real_models.py`
3. Start server: `uvicorn main:app --reload`
4. Test endpoint: POST to /api/ml/classify-text

## No New Packages Needed
All ML packages already installed - just need to switch the import!
