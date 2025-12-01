import stripe
import os
from typing import Optional

class PaymentService:
    def __init__(self):
        self.secret_key = os.getenv("STRIPE_SECRET_KEY")
        if self.secret_key:
            stripe.api_key = self.secret_key
    
    def is_configured(self) -> bool:
        return self.secret_key is not None and self.secret_key.startswith("sk_")
    
    async def create_payment_intent(self, amount: int, metadata: dict) -> stripe.PaymentIntent:
        if not self.is_configured():
            raise Exception("Stripe not configured. Set STRIPE_SECRET_KEY in .env")
        
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                automatic_payment_methods={"enabled": True},
                metadata=metadata
            )
            return payment_intent
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    async def create_subscription(self, price_id: str, email: str = None) -> dict:
        if not self.is_configured():
            raise Exception("Stripe not configured")

        try:
            customer = stripe.Customer.create(email=email) if email else stripe.Customer.create()
            
            if price_id == 'monthly_sub':
                price = stripe.Price.create(
                    unit_amount=1000,
                    currency="usd",
                    recurring={"interval": "month"},
                    product_data={"name": "Anti-Lust Guardian Monthly"}
                )
                stripe_price_id = price.id
            else:
                stripe_price_id = price_id

            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": stripe_price_id}],
                trial_period_days=7,
                payment_behavior='default_incomplete',
                payment_settings={'save_default_payment_method': 'on_subscription'},
                expand=['pending_setup_intent']
            )
            
            return {
                "client_secret": subscription.pending_setup_intent.client_secret,
                "subscription_id": subscription.id,
                "type": "setup_intent"
            }
            
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe subscription error: {str(e)}")
    
    async def confirm_payment(self, payment_intent_id: str) -> bool:
        try:
            if payment_intent_id.startswith("pi_"):
                intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                return intent.status == "succeeded"
            elif payment_intent_id.startswith("seti_"):
                intent = stripe.SetupIntent.retrieve(payment_intent_id)
                return intent.status == "succeeded"
            return False
        except stripe.error.StripeError as e:
            raise Exception(f"Payment confirmation failed: {str(e)}")
    
    async def create_subscription_with_user(
        self, 
        price_id: str, 
        firebase_user_id: str,
        customer_email: str = None
    ) -> dict:
        """Create subscription with 7-day trial for monthly plan"""
        if not self.is_configured():
            raise Exception("Stripe not configured")
        
        try:
            # Create or retrieve customer
            customer = stripe.Customer.create(
                email=customer_email,
                metadata={"firebase_user_id": firebase_user_id}
            )
            
            # Determine trial period - 7 days for monthly, 0 for others
            monthly_price_id = os.getenv("STRIPE_MONTHLY_PRICE_ID")
            trial_days = 7 if price_id == monthly_price_id else 0
            
            # Determine plan type
            yearly_price_id = os.getenv("STRIPE_YEARLY_PRICE_ID")
            plan_type = "monthly" if trial_days > 0 else ("yearly" if price_id == yearly_price_id else "lifetime")
            
            # Create subscription
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": price_id}],
                trial_period_days=trial_days if trial_days > 0 else None,
                payment_behavior='default_incomplete',
                payment_settings={'save_default_payment_method': 'on_subscription'},
                expand=['latest_invoice.payment_intent', 'pending_setup_intent'],
                metadata={
                    "firebase_user_id": firebase_user_id,
                    "plan_type": plan_type
                }
            )
            
            # Get client secret
            if subscription.pending_setup_intent:
                client_secret = subscription.pending_setup_intent.client_secret
            elif subscription.latest_invoice and subscription.latest_invoice.payment_intent:
                client_secret = subscription.latest_invoice.payment_intent.client_secret
            else:
                raise Exception("No client secret available")
            
            return {
                "client_secret": client_secret,
                "subscription_id": subscription.id,
                "customer_id": customer.id,
                "trial_end": subscription.trial_end if subscription.trial_end else None,
                "status": subscription.status
            }
            
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe subscription error: {str(e)}")
