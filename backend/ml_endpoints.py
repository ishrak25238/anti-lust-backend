"""
Additional ML API Endpoints for Integration Tests
Add these to main.py to provide standardized API endpoints
"""

# Add these imports at the top of main.py if not present
from fastapi import File, UploadFile
import base64

# Add these routes to main.py

@app.get("/api/ml/health")
async def ml_health_check():
    """ML service health check for integration tests"""
    try:
        health = ml_service.get_health()
        return {
            "status": "operational" if health.get('loaded') else "degraded",
            "models": health.get('models', {}),
            "loaded": health.get('loaded', False)
        }
    except Exception as e:
        logger.error(f"ML health check failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

@app.post("/api/ml/scan-image")
async def scan_image_simple(image: UploadFile = File(...)):
    """Simplified image scanning endpoint for integration tests"""
    try:
        # Read image bytes
        image_bytes = await image.read()
        
        # Use ML service's scan_image method
        result = await ml_service.scan_image(image_bytes)
        
        return {
            "is_safe": result.is_safe,
            "score": result.score,
            "flags": result.flags,
            "latency_ms": result.latency_ms
        }
    except Exception as e:
        logger.error(f"Image scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class TextScanRequest(BaseModel):
    text: str

@app.post("/api/ml/scan-text")
async def scan_text_simple(request: TextScanRequest):
    """Simplified text scanning endpoint for integration tests"""
    try:
        result = await ml_service.scan_text(request.text)
        
        return {
            "is_safe": result.is_safe,
            "score": result.score,
            "flags": result.flags
        }
    except Exception as e:
        logger.error(f"Text scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class URLScanRequest(BaseModel):
    url: str

@app.post("/api/ml/scan-url")
async def scan_url_simple(request: URLScanRequest):
    """Simplified URL scanning endpoint for integration tests"""
    try:
        result = await ml_service.scan_url(request.url)
        
        return {
            "is_safe": result.is_safe,
            "score": result.score,
            "flags": result.flags
        }
    except Exception as e:
        logger.error(f"URL scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
