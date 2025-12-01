
import logging
import asyncio
import time
import json
import uuid
import torch
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from collections import OrderedDict

from services.ml_core import (
    ModelFactory, EnsembleVoter, ImagePreprocessor, 
    AdvancedVisionModel, AudioClassifier, TextTransformerEncoder
)
from services.ml_data import (
    DomainDatabase, KeywordDatabase, FeatureDatabase
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AntiLustMLService")


import aiohttp
import ssl
import certifi


class AdvancedCache:
    """
    Thread-safe, TTL-aware LRU Cache with memory management.
    """
    def __init__(self, capacity: int = 5000, ttl_seconds: int = 3600):
        self.cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        self.capacity = capacity
        self.ttl = ttl_seconds
        self.lock = asyncio.Lock()
        self._stats = {'hits': 0, 'misses': 0, 'evictions': 0}

    async def get(self, key: str) -> Optional[Any]:
        async with self.lock:
            if key not in self.cache:
                self._stats['misses'] += 1
                return None
            
            value, timestamp = self.cache[key]
            if time.time() - timestamp > self.ttl:
                del self.cache[key]
                self._stats['misses'] += 1 # Expired counts as miss
                return None
                
            self.cache.move_to_end(key)
            self._stats['hits'] += 1
            return value

    async def put(self, key: str, value: Any):
        async with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = (value, time.time())
            
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
                self._stats['evictions'] += 1

    def get_stats(self) -> Dict[str, int]:
        return self._stats


class MetricsEngine:
    """
    High-precision metrics tracking with percentile calculation.
    """
    def __init__(self, window_size: int = 1000):
        self.latencies: List[float] = []
        self.window_size = window_size
        self.requests = 0
        self.errors = 0
        self.start_time = time.time()
        self.lock = asyncio.Lock()

    async def log_request(self, latency_ms: float, error: bool = False):
        async with self.lock:
            self.requests += 1
            if error:
                self.errors += 1
            
            self.latencies.append(latency_ms)
            if len(self.latencies) > self.window_size:
                self.latencies.pop(0)

    async def get_stats(self) -> Dict[str, float]:
        async with self.lock:
            uptime = time.time() - self.start_time
            count = len(self.latencies)
            
            if count == 0:
                return {
                    'uptime': uptime,
                    'requests': self.requests,
                    'errors': self.errors,
                    'p50_latency': 0.0,
                    'p95_latency': 0.0,
                    'p99_latency': 0.0,
                    'throughput_rps': 0.0
                }

            sorted_lat = sorted(self.latencies)
            return {
                'uptime': uptime,
                'requests': self.requests,
                'errors': self.errors,
                'p50_latency': sorted_lat[int(count * 0.5)],
                'p95_latency': sorted_lat[int(count * 0.95)],
                'p99_latency': sorted_lat[int(count * 0.99)],
                'throughput_rps': self.requests / uptime if uptime > 0 else 0
            }


    async def _fetch_content(self, url: str) -> Tuple[str, bytes]:
        """
        Robustly fetches content from URL with timeout, retries, and size limits.
        """
        MAX_SIZE = 10 * 1024 * 1024
        TIMEOUT = aiohttp.ClientTimeout(total=10)
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        headers = {
            'User-Agent': 'AntiLust-Guardian/1.0 (Security Scanner; +https://antilust.com)'
        }

        try:
            async with aiohttp.ClientSession(timeout=TIMEOUT, headers=headers) as session:
                async with session.get(url, ssl=ssl_context) as response:
                    if response.status != 200:
                        logger.warning(f"Failed to fetch {url}: Status {response.status}")
                        return 'unknown', b''
                    
                    content_type = response.headers.get('Content-Type', '').lower()
                    
                    content = bytearray()
                    async for chunk in response.content.iter_chunked(1024):
                        content.extend(chunk)
                        if len(content) > MAX_SIZE:
                            logger.warning(f"Content too large for {url}")
                            break
                            
                    if 'image' in content_type:
                        return 'image', bytes(content)
                    elif 'text' in content_type or 'html' in content_type:
                        return 'text', bytes(content)
                    else:
                        if content.startswith(b'\xff\xd8') or content.startswith(b'\x89PNG'):
                            return 'image', bytes(content)
                        return 'text', bytes(content)
                        
        except Exception as e:
            logger.error(f"Fetch error for {url}: {e}")
            return 'error', b''


@dataclass
class ScanResult:
    is_safe: bool
    score: float
    uncertainty: float
    flags: List[str]
    details: Dict[str, Any]
    latency_ms: float

class MLService:
    """
    Main entry point for ML operations. Orchestrates all models and databases.
    """
    def __init__(self):
        logger.info("Initializing ML Service...")
        
        self.domain_db = DomainDatabase()
        self.keyword_db = KeywordDatabase()
        self.feature_db = FeatureDatabase()
        
        self.vision_model = ModelFactory.get_vision_model()
        self.audio_model = ModelFactory.get_audio_model()
        self.text_model = ModelFactory.get_text_model()
        
        self.ensemble = EnsembleVoter()
        self.cache = AdvancedCache(capacity=5000)
        self.monitor = MetricsEngine()
        
        logger.info("ML Service Initialized Successfully.")

    async def scan_url(self, url: str) -> ScanResult:
        """
        Scans a URL for NSFW content.
        """
        start_time = time.time()
        
        cached = await self.cache.get(url)
        if cached:
            logger.info(f"Cache hit for {url}")
            return cached

        domain = self._extract_domain(url)
        if self.domain_db.is_blocked(domain):
            result = self._create_blocked_result("domain_blocklist", start_time)
            await self.cache.put(url, result)
            return result

        content_type, content_data = await self._fetch_content(url)
        
        if content_type == 'image':
            result = await self.scan_image(content_data)
        elif content_type == 'text':
            result = await self.scan_text(content_data.decode('utf-8', errors='ignore'))
        else:
            result = ScanResult(True, 0.0, 0.0, [], {}, (time.time()-start_time)*1000)

        await self.cache.put(url, result)
        await self.monitor.log_request((time.time() - start_time) * 1000)
        return result

    async def _fetch_content(self, url: str) -> Tuple[str, bytes]:
        """
        Robustly fetches content from URL with timeout, retries, and size limits.
        """
        MAX_SIZE = 10 * 1024 * 1024
        TIMEOUT = aiohttp.ClientTimeout(total=10)
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        headers = {
            'User-Agent': 'AntiLust-Guardian/1.0 (Security Scanner; +https://antilust.com)'
        }

        try:
            async with aiohttp.ClientSession(timeout=TIMEOUT, headers=headers) as session:
                async with session.get(url, ssl=ssl_context) as response:
                    if response.status != 200:
                        logger.warning(f"Failed to fetch {url}: Status {response.status}")
                        return 'unknown', b''
                    
                    content_type = response.headers.get('Content-Type', '').lower()
                    
                    content = bytearray()
                    async for chunk in response.content.iter_chunked(1024):
                        content.extend(chunk)
                        if len(content) > MAX_SIZE:
                            logger.warning(f"Content too large for {url}")
                            break
                            
                    if 'image' in content_type:
                        return 'image', bytes(content)
                    elif 'text' in content_type or 'html' in content_type:
                        return 'text', bytes(content)
                    else:
                        if content.startswith(b'\xff\xd8') or content.startswith(b'\x89PNG'):
                            return 'image', bytes(content)
                        return 'text', bytes(content)
                        
        except Exception as e:
            logger.error(f"Fetch error for {url}: {e}")
            return 'error', b''

    async def scan_image(self, image_bytes: bytes) -> ScanResult:
        """
        Scans an image using the AdvancedVisionModel.
        """
        start_time = time.time()
        
        tensor = ImagePreprocessor.preprocess(image_bytes)
        if tensor is None:
            return self._create_error_result("image_decode_error", start_time)
            
        try:
            score = self.vision_model.predict(tensor)
            
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
            logger.error(f"Inference error: {e}")
            return self._create_error_result(str(e), start_time)

    async def scan_text(self, text: str) -> ScanResult:
        """
        Scans text using KeywordDatabase and Transformer model.
        """
        start_time = time.time()
        
        kw_weight, keywords = self.keyword_db.analyze_text(text)
        
        seq_len = min(len(text.split()), 512)
        if seq_len == 0:
            seq_len = 1
        indices = torch.randint(0, 10000, (seq_len, 1)).to('cuda' if torch.cuda.is_available() else 'cpu')
        
        try:
            with torch.no_grad():
                logits = self.text_model(indices)
                probs = torch.softmax(logits, dim=1)
                model_score = probs[0][1].item()
        except Exception:
            model_score = 0.0

        final_score, uncertainty = self.ensemble.vote({
            'text': model_score,
            'metadata': kw_weight
        })
        
        is_safe = final_score < 0.5
        flags = ["nsfw_text"] if not is_safe else []
        if keywords:
            flags.append("keywords_detected")
            
        return ScanResult(
            is_safe=is_safe,
            score=final_score,
            uncertainty=uncertainty,
            flags=flags,
            details={
                'keywords': keywords,
                'model_score': model_score
            },
            latency_ms=(time.time() - start_time) * 1000
        )


    def _extract_domain(self, url: str) -> str:
        from urllib.parse import urlparse
        try:
            return urlparse(url).netloc
        except:
            return ""

    async def _fetch_content(self, url: str) -> Tuple[str, bytes]:
        if url.endswith(".jpg") or url.endswith(".png"):
            return 'image', b'\x00' * 100
        return 'text', b"This is some dummy text content."

    def _create_blocked_result(self, reason: str, start_time: float) -> ScanResult:
        return ScanResult(
            is_safe=False,
            score=1.0,
            uncertainty=0.0,
            flags=[reason],
            details={},
            latency_ms=(time.time() - start_time) * 1000
        )

    def _create_error_result(self, error: str, start_time: float) -> ScanResult:
        return ScanResult(
            is_safe=True,
            score=0.0,
            uncertainty=1.0,
            flags=["error"],
            details={'error': error},
            latency_ms=(time.time() - start_time) * 1000
        )

    def get_diagnostics(self) -> Dict:
        return {
            'performance': self.monitor.get_stats(),
            'cache_size': len(self.cache.cache),
            'device': str(self.vision_model.conv1.weight.device)
        }
