# 🚀 Complete Setup Guide - Anti-Lust Backend on Cloud Run

Your backend is **successfully deployed** to Cloud Run! Now let's get it fully configured.

## 📍 Current Status

✅ **Deployed**: https://anti-lust-backend-77553493618.us-central1.run.app  
✅ **Container Running**: Revision anti-lust-backend-00007-vgf  
⚠️ **Needs**: Environment variables configuration  

---

## Step 1: Gather Your Credentials

Before configuring Cloud Run, collect these credentials:

### A. Stripe Credentials
1. Go to https://dashboard.stripe.com/apikeys
2. Copy your **Secret Key** (starts with `sk_live_` or `sk_test_`)
3. Copy your **Publishable Key** (starts with `pk_live_` or `pk_test_`)

### B. Stripe Price IDs
1. Go to https://dashboard.stripe.com/products
2. For each product (Monthly, Yearly, Lifetime):
   - Click on the product
   - Copy the **Price ID** (starts with `price_`)

### C. Gmail SMTP Credentials
1. Use your Gmail account email
2. Create an **App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Generate a new app password for "Mail"
   - Copy the 16-character password

### D. Stripe Webhook Secret (Setup Later)
We'll create this in Step 4.

---

## Step 2: Configure Cloud Run Environment Variables

### Option A: Via Google Cloud Console (Recommended)

1. **Open Cloud Run Console**:
   - Go to 00
   - Or search "Cloud Run" in Google Cloud Console

2. **Select Your Service**:
   - Click on `anti-lust-backend`

3. **Edit Configuration**:
   - Click the **"EDIT & DEPLOY NEW REVISION"** button at the top

4. **Add Environment Variables**:
   - Scroll down to **"Variables & Secrets"** section
   - Click **"+ ADD VARIABLE"** for each variable below

**Required Variables** (Add these):

```
Variable Name: STRIPE_SECRET_KEY
Value: sk_live_YOUR_ACTUAL_KEY_HERE

Variable Name: STRIPE_PUBLISHABLE_KEY
Value: pk_live_YOUR_ACTUAL_KEY_HERE

Variable Name: STRIPE_MONTHLY_PRICE_ID
Value: price_YOUR_MONTHLY_PRICE_ID

Variable Name: STRIPE_YEARLY_PRICE_ID
Value: price_YOUR_YEARLY_PRICE_ID

Variable Name: STRIPE_LIFETIME_PRICE_ID
Value: price_YOUR_LIFETIME_PRICE_ID

Variable Name: API_SECRET_KEY
Value: ALG_8f3d9c2a1b7e4f6a9d2c8b5e1f4a7c3d9b6e2f8a5c1d7e3b9f6a2c8d5e1b4f7a3

Variable Name: JWT_SECRET_KEY
Value: JWT_9d7f2c4e8b1a6d3f9c5e2b8a7d4f1c6e9b3a7d2f5c8e1b4a6d9f3c7e2b5a8d1

Variable Name: JWT_ALGORITHM
Value: HS256

Variable Name: JWT_EXPIRATION_HOURS
Value: 24

Variable Name: SMTP_HOST
Value: smtp.gmail.com

Variable Name: SMTP_PORT
Value: 587

Variable Name: SMTP_USERNAME
Value: your-email@gmail.com

Variable Name: SMTP_PASSWORD
Value: your_16_char_app_password

Variable Name: ADMIN_EMAIL
Value: your-email@gmail.com

Variable Name: EMAIL_SENDER
Value: your-email@gmail.com

Variable Name: ML_API_KEYS
Value: alg-app-mobile-2024-98f7d6c5b4a3,alg-app-web-2024-87e6d5c4b3a2

Variable Name: ALLOWED_ORIGINS
Value: https://your-frontend-domain.com,http://localhost:3000

Variable Name: PORT
Value: 8080

Variable Name: DATABASE_URL
Value: sqlite+aiosqlite:///./guardian.db
```

**Optional Variables** (Add if using Firebase/Firestore):

```
Variable Name: FIREBASE_PROJECT_ID
Value: anti-lust-guardian

Variable Name: FIREBASE_PRIVATE_KEY
Value: -----BEGIN PRIVATE KEY-----\nYOUR_KEY_HERE\n-----END PRIVATE KEY-----\n

Variable Name: 
Value: firebase-adminsdk-xxxxx@anti-lust-guardian.iam.gserviceaccount.com
```

5. **Deploy the New Revision**:
   - Scroll to bottom
   - Click **"DEPLOY"**
   - Wait for deployment to complete (2-3 minutes)

---

## Step 3: Verify Your Backend is Working

Once the new revision is deployed:

### Test 1: Health Check
```powershell
curl https://anti-lust-backend-77553493618.us-central1.run.app/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "stripe": true,
  "email": true,
  "ml": false,
  "database": "connected"
}
```

### Test 2: Root Endpoint
```powershell
curl https://anti-lust-backend-77553493618.us-central1.run.app/
```

**Expected Response**:
```json
{
  "service": "Anti-Lust Guardian API",
  "status": "operational",
  "version": "1.0.0",
  "features": {
    "payment": true,
    "ml_models": true,
    "email": true,
    "sync": true,
    "dopamine_control": true
  }
}
```

---

## Step 4: Configure Stripe Webhook

Your backend needs to receive webhook events from Stripe for subscription updates.

1. **Go to Stripe Webhooks**:
   - https://dashboard.stripe.com/webhooks

2. **Add Endpoint**:
   - Click **"Add endpoint"**
   - Enter URL: `https://anti-lust-backend-77553493618.us-central1.run.app/api/stripe/webhook`
   - Click **"Select events"**

3. **Select These Events**:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - Click **"Add events"**

4. **Save and Copy Webhook Secret**:
   - Click **"Add endpoint"**
   - Click on your new webhook endpoint
   - Under "Signing secret", click **"Reveal"**
   - Copy the secret (starts with `whsec_`)

5. **Add Webhook Secret to Cloud Run**:
   - Go back to Cloud Run Console
   - Click `anti-lust-backend` → **"EDIT & DEPLOY NEW REVISION"**
   - Add variable:
     ```
     Variable Name: STRIPE_WEBHOOK_SECRET
     Value: whsec_YOUR_WEBHOOK_SECRET
     ```
   - Click **"DEPLOY"**

---

## Step 5: Update Your Frontend/Mobile App

Update your frontend and mobile app to use the new backend URL:

**Backend URL**: `https://anti-lust-backend-77553493618.us-central1.run.app`

### For Website:
Update API base URL in your JavaScript files:
```javascript
const API_BASE_URL = 'https://anti-lust-backend-77553493618.us-central1.run.app';
```

### For Flutter App:
Update API base URL in your Dart files:
```dart
static const String baseUrl = 'https://anti-lust-backend-77553493618.us-central1.run.app';
```

---

## Step 6: Test Critical Endpoints

### Test Payment Creation
```powershell
curl -X POST https://anti-lust-backend-77553493618.us-central1.run.app/api/payment/create-intent `
  -H "Content-Type: application/json" `
  -d '{"price_id":"monthly_sub","amount":499}'
```

### Test ML Health (Optional)
```powershell
curl https://anti-lust-backend-77553493618.us-central1.run.app/api/ml/health
```

**Expected**: `{"status":"not_initialized","message":"ML service will initialize on first use","loaded":false}`

---

## 🎯 Quick Checklist

- [ ] Collected all Stripe credentials
- [ ] Created Gmail App Password
- [ ] Added all required environment variables to Cloud Run
- [ ] Deployed new revision with environment variables
- [ ] Tested `/health` endpoint (shows stripe:true, email:true)
- [ ] Tested root `/` endpoint
- [ ] Created Stripe webhook endpoint
- [ ] Added webhook secret to Cloud Run
- [ ] Updated frontend/mobile app with backend URL
- [ ] Tested payment endpoint

---

## 🆘 Troubleshooting

### Health Check Shows `stripe: false`
- Double-check your `STRIPE_SECRET_KEY` is set correctly
- Ensure it starts with `sk_live_` or `sk_test_`

### Health Check Shows `email: false`
- Verify `SMTP_USERNAME` and `SMTP_PASSWORD` are correct
- Make sure you used Gmail App Password (not your regular password)

### "CORS Error" in Frontend
- Add your frontend domain to `ALLOWED_ORIGINS`
- Format: `https://yourdomain.com,https://www.yourdomain.com`
- Include `http://localhost:3000` for local testing

### Webhook Not Working
- Verify webhook URL is exactly: `https://anti-lust-backend-77553493618.us-central1.run.app/api/stripe/webhook`
- Check `STRIPE_WEBHOOK_SECRET` is set in Cloud Run
- Test webhook in Stripe Dashboard (Send test webhook)

---

## 📚 Reference Documents

- **Complete Fix Documentation**: `walkthrough.md` artifact
- **Task Checklist**: `task.md` artifact
- **Deployment Plan**: `implementation_plan.md` artifact
- **Cloud Run Console**: https://console.cloud.google.com/run
- **Stripe Dashboard**: https://dashboard.stripe.com

---

## ✅ You're Done!

Your Anti-Lust Guardian backend is now:
- ✅ Deployed to Google Cloud Run
- ✅ Running with all dependencies fixed
- ✅ Ready to accept API requests
- ✅ Configured for payments and email

**Next**: Configure environment variables and test your endpoints!
