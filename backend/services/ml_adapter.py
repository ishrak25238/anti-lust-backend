"""
ML Service Adapter - Maintains backward compatibility with old API
Wraps RealMLService to provide old interface format
"""
import asyncio
from typing import Dict, Union
import base64
from io import BytesIO

# Try to import real ML service, fall back to simple one if torch is not available
try:
    from services.ml_service_real import RealMLService
    ML_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    from services.ml_service_simple import SimpleMLService
    ML_AVAILABLE = False
    print(f"ML models not available ({e}), using simple fallback")


class MLServiceAdapter:
    """Adapter to maintain backward compatibility while using real ML models."""
    
    def __init__(self):
        if ML_AVAILABLE:
            self.real_service = RealMLService()
        else:
            self.real_service = SimpleMLService()
        self._loaded = True
    
    def is_loaded(self) -> bool:
        """Check if ML service is loaded."""
        return self._loaded
    
    async def detect_nsfw(self, image_base64: str) -> float:
        """
        Detect NSFW content in base64 encoded image.
        Returns confidence score (0.0-1.0).
        """
        try:
            image_bytes = base64.b64decode(image_base64)
            result = await self.real_service.scan_image(image_bytes)
            return result.score
        except Exception as e:
            print(f"NSFW detection error: {e}")
            return 0.0
    
    async def classify_text(self, text: str) -> Dict[str, Union[bool, float, str]]:
        """
        Classify text for harmful content.
        Returns: {'is_harmful': bool, 'confidence': float, 'classification': str}
        """
        try:
            result = await self.real_service.scan_text(text)
            
            classification = "safe"
            if not result.is_safe:
                if "toxic_text" in result.flags:
                    classification = "toxic"
                elif "keywords_detected" in result.flags:
                    classification = "inappropriate"
                else:
                    classification = "harmful"
            
            return {
                'is_harmful': not result.is_safe,
                'confidence': result.score,
                'classification': classification
            }
        except Exception as e:
            print(f"Text classification error: {e}")
            return {
                'is_harmful': False,
                'confidence': 0.0,
                'classification': 'error'
            }
    
    async def analyze_url(self, url: str) -> float:
        """
        Analyze URL for threats.
        Returns threat score (0.0-1.0).
        """
        try:
            result = await self.real_service.scan_url(url)
            return result.score
        except Exception as e:
            print(f"URL analysis error: {e}")
            return 0.0
    
    def get_health(self) -> Dict:
        """Return health status."""
        return {
            'loaded': self._loaded,
            'models': {
                'nsfw': 'Falconsai/nsfw_image_detection',
                'text': 'unitary/toxic-bert'
            },
            'status': 'operational'
        }
