from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
import stripe
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import logging

from services.payment_service import PaymentService
from services.email_service import EmailService
from services.ml_adapter import MLServiceAdapter as MLService
from services.sync_service import SyncService
from services.pattern_storage import PatternStorage
from services.notification_service import NotificationService
from services.audit_logger import AuditLogger
from database import engine, Base

from middleware.security import (
    verify_api_key, verify_jwt_token, limiter, add_security_headers,
    validate_image_size, validate_text_length, sanitize_input,
    api_key_header, SecurityConfig
)
from middleware.monitoring import (
    track_request_metrics, track_ml_prediction, track_auth_failure, get_metrics
)
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Anti-Lust Guardian API",
    description="Backend services for content filtering and parental controls",
    version="1.0.0"
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
)

app.middleware("http")(add_security_headers)

app.middleware("http")(track_request_metrics)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from services.dopamine_service import DopamineService
from services.subscription_service import SubscriptionService

payment_service = PaymentService()
email_service = EmailService()
ml_service = MLService()
sync_service = SyncService()
pattern_storage = PatternStorage()
notification_service = NotificationService()
audit_logger = AuditLogger()
dopamine_service = DopamineService()
security_config = SecurityConfig()
subscription_service = SubscriptionService()

class PaymentIntentRequest(BaseModel):
    price_id: str
    amount: int

class PaymentIntentResponse(BaseModel):
    client_secret: str
    payment_intent_id: str

class PairingRequest(BaseModel):
    parent_email: EmailStr
    child_code: str
    child_name: str

class ThreatLog(BaseModel):
    device_id: str
    source: str
    reason: str
    context: str
    timestamp: str

class NSFWCheckRequest(BaseModel):
    image_base64: str
    device_id: Optional[str] = None
    parent_email: Optional[str] = None

class TextClassificationRequest(BaseModel):
    text: str
    device_id: Optional[str] = None

class URLThreatRequest(BaseModel):
    url: str
    device_id: Optional[str] = None

class DopamineLimitRequest(BaseModel):
    device_id: str
    category: str
    minutes: int

class UsageReportRequest(BaseModel):
    device_id: str
    category: str
    minutes_delta: float
    parent_email: Optional[str] = None

@app.post("/api/payment/create-intent", response_model=PaymentIntentResponse)
async def create_payment_intent(request: PaymentIntentRequest):
    try:
        if request.price_id == 'monthly_sub' or request.price_id == '2week_trial':
            result = await payment_service.create_subscription(
                price_id='monthly_sub',
                email=None
            )
            return PaymentIntentResponse(
                client_secret=result['client_secret'],
                payment_intent_id=result['subscription_id']
            )
        else:
            payment_intent = await payment_service.create_payment_intent(
                amount=request.amount,
                metadata={"price_id": request.price_id}
            )
            return PaymentIntentResponse(
                client_secret=payment_intent.client_secret,
                payment_intent_id=payment_intent.id
            )
    except Exception as e:
        logger.error(f"Payment intent creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/payment/confirm")
async def confirm_payment(payment_intent_id: str):
    try:
        result = await payment_service.confirm_payment(payment_intent_id)
        return {"success": True, "subscription_active": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/subscription/create")
async def create_subscription_endpoint(
    price_id: str,
    firebase_user_id: str,
    customer_email: str
):
    """Create subscription for authenticated user with 7-day trial"""
    try:
        result = await payment_service.create_subscription_with_user(
            price_id=price_id,
            firebase_user_id=firebase_user_id,
            customer_email=customer_email
        )
        
        # Store in Firestore
        await subscription_service.store_subscription(
            user_id=firebase_user_id,
            subscription_id=result['subscription_id'],
            customer_id=result['customer_id'],
            price_id=price_id,
            status=result['status'],
            trial_end=result.get('trial_end')
        )
        
        return result
    except Exception as e:
        logger.error(f"Subscription creation failed: {e}")
        raise HTTPException(status_code=500,detail=str(e))

@app.get("/api/subscription/status/{user_id}")
async def get_subscription_status_endpoint(user_id: str):
    """Get user's subscription status"""
    try:
        subscription = await subscription_service.get_subscription(user_id)
        if not subscription:
            return {"hasSubscription": False}
        
        return {
            "hasSubscription": True,
            "status": subscription.get('status'),
            "plan": subscription.get('plan'),
            "trialEnd": subscription.get('trialEnd')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stripe/webhook")
async def stripe_webhook_endpoint(request: Request):
    """Handle Stripe webhooks for subscription events"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    if not webhook_secret:
        logger.warning("Stripe webhook secret not configured")
        return {"success": True, "message": "Webhook secret not configured"}
    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    try:
        if event['type'] == 'customer.subscription.created':
            subscription = event['data']['object']
            user_id = subscription['metadata'].get('firebase_user_id')
            if user_id:
                await subscription_service.store_subscription(
                    user_id=user_id,
                    subscription_id=subscription['id'],
                    customer_id=subscription['customer'],
                    price_id=subscription['items']['data'][0]['price']['id'],
                    status=subscription['status'],
                    trial_end=subscription.get('trial_end')
                )
        
        elif event['type'] == 'customer.subscription.updated':
            subscription = event['data']['object']
            user_id = subscription['metadata'].get('firebase_user_id')
            if user_id:
                await subscription_service.update_subscription_status(user_id, subscription['status'])
        
        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            user_id = subscription['metadata'].get('firebase_user_id')
            if user_id:
                await subscription_service.update_subscription_status(user_id, 'cancelled')
        
        return {"success": True}
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/pairing/link")
async def link_parent_child(request: PairingRequest):
    try:
        result = await sync_service.link_accounts(
            parent_email=request.parent_email,
            child_code=request.child_code,
            child_name=request.child_name
        )
        return {"success": True, "link_id": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/logs/push")
async def push_child_logs(logs: List[ThreatLog]):
    try:
        await sync_service.store_logs(logs)
        return {"success": True, "count": len(logs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs/fetch/{parent_email}")
async def fetch_child_logs(parent_email: str):
    try:
        logs = await sync_service.get_logs_for_parent(parent_email)
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dopamine/limit")
async def set_dopamine_limit(
    request: DopamineLimitRequest,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    try:
        await dopamine_service.set_limit(
            device_id=request.device_id,
            category=request.category,
            minutes=request.minutes
        )
        return {"success": True, "message": f"Limit set for {request.category}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dopamine/report")
async def report_usage(
    request: UsageReportRequest,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    try:
        status = await dopamine_service.report_usage(
            device_id=request.device_id,
            category=request.category,
            minutes_delta=request.minutes_delta
        )
        
        if not status['allowed'] and request.parent_email:
             await notification_service.send_time_limit_alert(
                 device_id=request.device_id,
                 parent_email=request.parent_email,
                 category=request.category,
                 limit=status['limit']
             )
        
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dopamine/status/{device_id}")
async def get_dopamine_status(device_id: str, api_key: str = Depends(api_key_header)):
    await verify_api_key(api_key)
    try:
        return await dopamine_service.get_status(device_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ml/nsfw-check")
@limiter.limit("100/minute")
async def check_nsfw(
    request: Request,
    nsfw_request: NSFWCheckRequest,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    
    validate_image_size(nsfw_request.image_base64, max_mb=security_config.max_image_size_mb)
    
    try:
        score = await ml_service.detect_nsfw(nsfw_request.image_base64)
        
        if hasattr(nsfw_request, 'device_id') and nsfw_request.device_id:
            device_id = nsfw_request.device_id
            threat_level = 4 if score > 0.8 else 3 if score > 0.6 else 2 if score > 0.4 else 1
            
            await pattern_storage.store_event(
                device_id=device_id,
                event_type='nsfw',
                confidence=score,
                threat_level=threat_level,
                threat_score=score,
                context={'source': 'image_check'}
            )
            
            if score > 0.8 and hasattr(nsfw_request, 'parent_email'):
                await notification_service.send_critical_alert(
                    device_id=device_id,
                    parent_email=nsfw_request.parent_email,
                    event_type='NSFW',
                    threat_level='CRITICAL',
                    confidence=score,
                    context={'source': 'image_check'}
                )
        
        return {
            "is_nsfw": score > 0.7,
            "confidence": score,
            "threshold": 0.7
        }
    except Exception as e:
        logger.error(f"NSFW detection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ml/classify-text")
@limiter.limit("100/minute")
async def classify_text(
    request: Request,
    text_request: TextClassificationRequest,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    
    validate_text_length(text_request.text, max_length=security_config.max_text_length)
    
    sanitized_text = sanitize_input(text_request.text)
    
    try:
        result = await ml_service.classify_text(sanitized_text)
        
        if hasattr(text_request, 'device_id') and text_request.device_id:
            device_id = text_request.device_id
            await pattern_storage.store_event(
                device_id=device_id,
                event_type='text',
                confidence=result['confidence'],
                threat_level=3 if result['is_harmful'] else 0,
                threat_score=result['confidence'],
                context={'classification': result['classification']}
            )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ml/threat-url")
@limiter.limit("100/minute")
async def analyze_url(
    request: Request,
    url_request: URLThreatRequest,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    
    try:
        threat_score = await ml_service.analyze_url(url_request.url)
        
        if hasattr(url_request, 'device_id') and url_request.device_id:
            device_id = url_request.device_id
            threat_level = 4 if threat_score > 0.8 else 3 if threat_score > 0.6 else 2 if threat_score > 0.4 else 1
            
            await pattern_storage.store_event(
                device_id=device_id,
                event_type='url',
                confidence=threat_score,
                threat_level=threat_level,
                threat_score=threat_score,
                context={'url': url_request.url}
            )
        
        return {
            "url": url_request.url,
            "threat_score": threat_score,
            "is_blocked": threat_score > 0.7
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patterns/analysis/{device_id}")
@limiter.limit("50/minute")
async def get_pattern_analysis(
    request: Request,
    device_id: str,
    days: int = 7,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    
    try:
        patterns = await pattern_storage.analyze_temporal_patterns(device_id, days=days)
        recommendations = await pattern_storage.generate_recommendations(device_id)
        profile = await pattern_storage.get_behavioral_profile(device_id)
        
        return {
            "patterns": patterns,
            "recommendations": recommendations,
            "profile": profile
        }
    except Exception as e:
        logger.error(f"Pattern analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/patterns/false-positive")
@limiter.limit("20/minute")
async def report_false_positive(
    request: Request,
    event_id: int,
    device_id: str,
    reason: str,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    
    try:
        report_id = await pattern_storage.report_false_positive(event_id, device_id, reason)
        return {"success": True, "report_id": report_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def prometheus_metrics():
    from prometheus_client import generate_latest
    return Response(content=generate_latest(), media_type="text/plain")

@app.get("/api/stats/ml")
@limiter.limit("20/minute")
async def ml_statistics(request: Request):
    try:
        return ml_service.get_health()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/research/generate-report")
async def generate_research_report(
    device_id: str,
    background_tasks: BackgroundTasks
):
    try:
        logs = await sync_service.get_logs_by_device(device_id)
        
        background_tasks.add_task(
            email_service.send_research_report,
            logs=logs,
            device_id=device_id
        )
        
        return {
            "success": True,
            "message": "Report generation started",
            "log_count": len(logs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "service": "Anti-Lust Guardian API",
        "status": "operational",
        "version": "1.0.0",
        "features": {
            "payment": True,
            "ml_models": True,
            "email": True,
            "sync": True,
            "dopamine_control": True
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "stripe": payment_service.is_configured(),
        "email": email_service.is_configured(),
        "ml": ml_service.is_loaded(),
        "database": "connected"
    }

@app.on_event("startup")
async def startup():
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Loading ML models...")
    if hasattr(ml_service, 'load_models') and callable(getattr(ml_service, 'load_models')):
        try:
            ml_service.load_models()
            logger.info("✓ ML models loaded successfully")
        except Exception as e:
            logger.warning(f"ML model loading failed (degraded mode): {e}")
    else:
        logger.warning("ML service in degraded mode - models not available")
    
    logger.info("✓ Server ready!")

from services.ml_training import ModelTrainer

model_trainer = ModelTrainer()

@app.post("/api/ml/train")
async def train_models(
    background_tasks: BackgroundTasks,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    try:
        result = await model_trainer.train_on_feedback()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class TrainFileRequest(BaseModel):
    file_path: str
    data_type: str

@app.post("/api/ml/train-file")
async def train_from_file(
    request: TrainFileRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    try:
        if not os.path.exists(request.file_path):
             raise HTTPException(status_code=404, detail=f"File not found: {request.file_path}")

        result = await model_trainer.train_from_file(request.file_path, request.data_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from services.parent_child_service import ParentChildService
from pydantic import BaseModel

class CreatePinRequest(BaseModel):
    parent_id: int
    pin: str
    phone_number: Optional[str] = None

class VerifyPinRequest(BaseModel):
    parent_id: int
    pin: str

class AppPermissionRequest(BaseModel):
    child_id: int
    app_package: str
    allowed: bool

class UninstallProtectionRequest(BaseModel):
    child_id: int
    enabled: bool

class RemoteLockRequest(BaseModel):
    child_id: int
    duration_minutes: int
    reason: str = "Parent initiated"

class UninstallAttemptRequest(BaseModel):
    child_id: int
    pin: str

@app.post("/api/parent/create-pin")
async def create_parent_pin(
    request: CreatePinRequest,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    parent_service = ParentChildService(None)
    
    if request.phone_number:
        from database import User, async_session
        async with async_session() as db:
            parent = await db.get(User, request.parent_id)
            if parent:
                parent.parent_phone_number = request.phone_number
                await db.commit()
    
    success = await parent_service.create_parent_pin(request.parent_id, request.pin)
    
    if success:
        return {"success": True, "message": "PIN created successfully"}
    return {"success": False, "message": "Invalid PIN format or parent not found"}

@app.post("/api/parent/verify-pin")
async def verify_parent_pin(
    request: VerifyPinRequest,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    parent_service = ParentChildService(None)
    valid = await parent_service.verify_parent_pin(request.parent_id, request.pin)
    return {"valid": valid}

@app.post("/api/parent/app-permission")
async def set_app_permission(
    request: AppPermissionRequest,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    parent_service = ParentChildService(None)
    success = await parent_service.set_app_permission(
        request.child_id,
        request.app_package,
        request.allowed
    )
    return {"success": success}

@app.get("/api/parent/app-permissions/{child_id}")
async def get_app_permissions(
    child_id: int,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    parent_service = ParentChildService(None)
    permissions = await parent_service.get_app_permissions(child_id)
    return permissions

@app.post("/api/parent/uninstall-protection")
async def set_uninstall_protection(
    request: UninstallProtectionRequest,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    parent_service = ParentChildService(None)
    success = await parent_service.enable_uninstall_protection(
        request.child_id,
        request.enabled
    )
    return {"success": success}

@app.post("/api/parent/remote-lock")
async def remote_lock_device(
    request: RemoteLockRequest,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    parent_service = ParentChildService(None)
    result = await parent_service.send_remote_lock_command(
        request.child_id,
        request.duration_minutes,
        request.reason
    )
    return result

@app.get("/api/parent/lock-status/{child_id}")
async def get_lock_status(
    child_id: int,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    parent_service = ParentChildService(None)
    status = await parent_service.check_remote_lock_status(child_id)
    return status

@app.post("/api/parent/unlock")
async def unlock_device(
    child_id: int,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    parent_service = ParentChildService(None)
    success = await parent_service.unlock_child_device(child_id)
    return {"success": success}

@app.post("/api/device/attempt-uninstall")
async def attempt_app_uninstall(
    request: UninstallAttemptRequest
):
    parent_service = ParentChildService(None)
    result = await parent_service.attempt_uninstall(request.child_id, request.pin)
    return result

class UpdatePhoneRequest(BaseModel):
    parent_id: int
    phone_number: str

@app.post("/api/parent/update-phone")
async def update_parent_phone(
    request: UpdatePhoneRequest,
    api_key: str = Depends(api_key_header)
):
    await verify_api_key(api_key)
    from database import User, async_session
    
    async with async_session() as db:
        parent = await db.get(User, request.parent_id)
        if not parent:
            return {"success": False, "message": "Parent not found"}
        
        parent.parent_phone_number = request.phone_number
        await db.commit()
        return {"success": True, "message": "Phone number updated"}
