"""
Real ML Service - Using actual pre-trained models
"""
import logging
import asyncio
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from services.ml_core_real import (
    ModelFactory, EnsembleVoter
)
from services.ml_data import (
    DomainDatabase, KeywordDatabase
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RealMLService")


@dataclass
class ScanResult:
    is_safe: bool
    score: float
    uncertainty: float
    flags: List[str]
    details: Dict
    latency_ms: float


class RealMLService:
    """
    Production ML Service using real pre-trained models.
    """
    def __init__(self):
        logger.info("Initializing Real ML Service...")
        
        self.domain_db = DomainDatabase()
        self.keyword_db = KeywordDatabase()
        
        self.vision_model = ModelFactory.get_vision_model()
        self.text_model = ModelFactory.get_text_model()
        
        self.ensemble = EnsembleVoter()
        
        logger.info("Real ML Service Initialized Successfully.")

    async def scan_text(self, text: str) -> ScanResult:
        """
        Scans text using REAL toxicity detection.
        """
        start_time = time.time()
        
        kw_weight, keywords = self.keyword_db.analyze_text(text)
        
        model_score = self.text_model.predict(text)
        
        final_score, uncertainty = self.ensemble.vote({
            'text': model_score,
            'metadata': kw_weight
        })
        
        is_safe = final_score < 0.5
        flags = []
        if not is_safe:
            flags.append("toxic_text")
        if keywords:
            flags.append("keywords_detected")
            
        return ScanResult(
            is_safe=is_safe,
            score=final_score,
            uncertainty=uncertainty,
            flags=flags,
            details={
                'keywords': keywords,
                'model_score': model_score,
                'keyword_weight': kw_weight
            },
            latency_ms=(time.time() - start_time) * 1000
        )

    async def scan_image(self, image_bytes: bytes) -> ScanResult:
        """
        Scans image using REAL NSFW detection.
        """
        start_time = time.time()
        
        try:
            score = self.vision_model.predict(image_bytes)
            
            final_score, uncertainty = self.ensemble.vote({'vision': score})
            
            is_safe = final_score < 0.5
            flags = ["nsfw_image"] if not is_safe else []
            
            return ScanResult(
                is_safe=is_safe,
                score=final_score,
                uncertainty=uncertainty,
                flags=flags,
                details={'vision_score': score},
                latency_ms=(time.time() - start_time) * 1000
            )
        except Exception as e:
            logger.error(f"Image scan error: {e}")
            return ScanResult(
                is_safe=True,
                score=0.0,
                uncertainty=1.0,
                flags=["error"],
                details={'error': str(e)},
                latency_ms=(time.time() - start_time) * 1000
            )

    async def scan_url(self, url: str) -> ScanResult:
        """
        Scans URL (domain check only for now - no fetching).
        """
        start_time = time.time()
        
        from urllib.parse import urlparse
        try:
            domain = urlparse(url).netloc
        except:
            domain = ""
        
        if self.domain_db.is_blocked(domain):
            return ScanResult(
                is_safe=False,
                score=1.0,
                uncertainty=0.0,
                flags=["domain_blocklist"],
                details={'domain': domain},
                latency_ms=(time.time() - start_time) * 1000
            )
        
        return ScanResult(
            is_safe=True,
            score=0.0,
            uncertainty=0.1,
            flags=[],
            details={'domain': domain},
            latency_ms=(time.time() - start_time) * 1000
        )
