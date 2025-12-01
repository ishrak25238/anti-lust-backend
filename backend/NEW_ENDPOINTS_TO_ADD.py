# NEW SUBSCRIPTION AND WEBHOOK ENDPOINTS - Add to main.py after line 148

# Add these endpoints after @app.post("/api/payment/confirm")

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
        raise HTTPException(status_code=500, detail=str(e))

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
        logger.warning("Stripe webhook secret not configured - skipping verification")
        return {"success": True, "message": "Webhook secret not configured"}
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle subscription events
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
                logger.info(f"Subscription created via webhook for user {user_id}")
        
        elif event['type'] == 'customer.subscription.updated':
            subscription = event['data']['object']
            user_id = subscription['metadata'].get('firebase_user_id')
            if user_id:
                await subscription_service.update_subscription_status(
                    user_id, subscription['status']
                )
                logger.info(f"Subscription updated via webhook for user {user_id}: {subscription['status']}")
        
        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            user_id = subscription['metadata'].get('firebase_user_id')
            if user_id:
                await subscription_service.update_subscription_status(
                    user_id, 'cancelled'
                )
                logger.info(f"Subscription cancelled via webhook for user {user_id}")
        
        return {"success": True}
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        # Don't raise error - return 200 to Stripe
        return {"success": False, "error": str(e)}
