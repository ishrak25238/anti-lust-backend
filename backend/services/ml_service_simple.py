"""
Simple ML Service - Fallback when torch is not available
Uses basic keyword matching and heuristics
"""
import logging
import asyncio
from typing import Dict, List
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SimpleMLService")


@dataclass
class ScanResult:
    is_safe: bool
    score: float
    uncertainty: float
    flags: List[str]
    details: Dict
    latency_ms: float


class SimpleMLService:
    """
    Fallback ML Service using keyword-based detection.
    Used when torch/transformers are not available.
    """
    def __init__(self):
        logger.warning("Using SimpleMLService (keyword-based fallback)")
        logger.warning("For production use, install torch and transformers for AI-powered detection")
        
        # Basic NSFW keywords
        self.nsfw_keywords = {
            'porn', 'sex', 'xxx', 'adult', 'nsfw', 'nude', 'naked',
            'explicit', 'erotic', 'hentai', 'xxx', 'xvideos', 'pornhub'
        }
        
        # Toxic keywords
        self.toxic_keywords = {
            'hate', 'kill', 'die', 'stupid', 'idiot', 'fuck', 'shit',
            'damn', 'hell', 'bastard', 'bitch', 'ass', 'cunt'
        }
        
        # Blocked domains
        self.blocked_domains = {
            'pornhub.com', 'xvideos.com', 'xnxx.com', 'redtube.com',
            'xhamster.com', 'youporn.com', 'tube8.com', 'porn.com'
        }

    async def scan_text(self, text: str) -> ScanResult:
        """Basic text scanning using keyword matching."""
        import time
        start_time = time.time()
        
        text_lower = text.lower()
        matched_keywords = []
        
        for keyword in self.toxic_keywords:
            if keyword in text_lower:
                matched_keywords.append(keyword)
        
        score = min(1.0, len(matched_keywords) * 0.3)
        is_safe = score < 0.5
        
        return ScanResult(
            is_safe=is_safe,
            score=score,
            uncertainty=0.5,  # High uncertainty for keyword-based
            flags=["keywords_detected"] if matched_keywords else [],
            details={'matched_keywords': matched_keywords},
            latency_ms=(time.time() - start_time) * 1000
        )

    async def scan_image(self, image_bytes: bytes) -> ScanResult:
        """Placeholder image scanning - always returns safe."""
        import time
        start_time = time.time()
        
        # Without ML models, we can't actually scan images
        # Return safe with high uncertainty
        return ScanResult(
            is_safe=True,
            score=0.0,
            uncertainty=1.0,  # Maximum uncertainty
            flags=["no_ml_available"],
            details={'message': 'Image scanning requires ML models'},
            latency_ms=(time.time() - start_time) * 1000
        )

    async def scan_url(self, url: str) -> ScanResult:
        """Basic URL scanning using domain blocklist."""
        import time
        start_time = time.time()
        
        from urllib.parse import urlparse
        try:
            domain = urlparse(url).netloc.lower()
        except:
            domain = ""
        
        is_blocked = domain in self.blocked_domains
        
        return ScanResult(
            is_safe=not is_blocked,
            score=1.0 if is_blocked else 0.0,
            uncertainty=0.2,
            flags=["domain_blocklist"] if is_blocked else [],
            details={'domain': domain},
            latency_ms=(time.time() - start_time) * 1000
        )
