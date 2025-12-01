from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request
import time
from typing import Optional
import logging

logger = logging.getLogger(__name__)

request_count = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint']
)

active_requests = Gauge(
    'api_active_requests',
    'Number of active requests'
)

ml_predictions = Counter(
    'ml_predictions_total',
    'Total ML predictions',
    ['model_type', 'threat_level']
)

ml_prediction_duration = Histogram(
    'ml_prediction_duration_seconds',
    'ML prediction duration in seconds',
    ['model_type']
)

authentication_failures = Counter(
    'authentication_failures_total',
    'Total authentication failures',
    ['reason']
)

rate_limit_hits = Counter(
    'rate_limit_hits_total',
    'Total rate limit violations',
    ['endpoint']
)

async def track_request_metrics(request: Request, call_next):
    active_requests.inc()
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        request_count.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        request_duration.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        response.headers["X-Process-Time"] = f"{duration:.4f}"
        
        return response
    finally:
        active_requests.dec()

def track_ml_prediction(model_type: str, threat_level: str, duration: float):
    ml_predictions.labels(
        model_type=model_type,
        threat_level=threat_level
    ).inc()
    
    ml_prediction_duration.labels(
        model_type=model_type
    ).observe(duration)

def track_auth_failure(reason: str):
    authentication_failures.labels(reason=reason).inc()
    logger.warning(f"Authentication failure: {reason}")

def track_rate_limit_hit(endpoint: str):
    rate_limit_hits.labels(endpoint=endpoint).inc()
    logger.warning(f"Rate limit hit: {endpoint}")

def get_metrics():
    return generate_latest()
