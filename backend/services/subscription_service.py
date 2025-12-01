import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

# Initialize Firebase Admin (singleton pattern)
try:
    firebase_admin.get_app()
except ValueError:
    # Not initialized yet
    try:
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n'),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL")
        })
        firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin initialized successfully")
    except Exception as e:
        logger.warning(f"Firebase Admin initialization failed: {e}")

# Get Firestore client
try:
    db = firestore.client()
except Exception as e:
    logger.warning(f"Firestore client not available: {e}")
    db = None

class SubscriptionService:
    
    @staticmethod
    async def store_subscription(
        user_id: str,
        subscription_id: str,
        customer_id: str,
        price_id: str,
        status: str,
        trial_end: int = None
    ):
        """Store subscription in Firestore"""
        if not db:
            raise Exception("Firestore not configured")
        
        monthly_price_id = os.getenv("STRIPE_MONTHLY_PRICE_ID")
        yearly_price_id = os.getenv("STRIPE_YEARLY_PRICE_ID")
        
        plan_type = "monthly" if price_id == monthly_price_id else \
                   "yearly" if price_id == yearly_price_id else \
                   "lifetime"
        
        doc_ref = db.collection('subscriptions').document(user_id)
        doc_ref.set({
            "userId": user_id,
            "stripeCustomerId": customer_id,
            "stripeSubscriptionId": subscription_id,
            "priceId": price_id,
            "status": status,
            "plan": plan_type,
            "trialEnd": datetime.fromtimestamp(trial_end) if trial_end else None,
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP
        })
        logger.info(f"Subscription stored for user {user_id}: {plan_type} ({status})")
        
    @staticmethod
    async def get_subscription(user_id: str) -> dict:
        """Get user subscription from Firestore"""
        if not db:
            return None
        
        doc_ref = db.collection('subscriptions').document(user_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        return None
    
    @staticmethod
    async def update_subscription_status(user_id: str, status: str):
        """Update subscription status"""
        if not db:
            raise Exception("Firestore not configured")
        
        doc_ref = db.collection('subscriptions').document(user_id)
        doc_ref.update({
            "status": status,
            "updatedAt": firestore.SERVER_TIMESTAMP
        })
        logger.info(f"Updated subscription status for user {user_id}: {status}")
    
    @staticmethod
    async def has_active_subscription(user_id: str) -> bool:
        """Check if user has active subscription"""
        subscription = await SubscriptionService.get_subscription(user_id)
        if not subscription:
            return False
        
        status = subscription.get('status')
        return status in ['active', 'trialing']
