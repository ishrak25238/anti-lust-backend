# Backend Environment Variables

## ✅ Safe Browsing API
Your Safe Browsing API is correctly configured!
- **Flutter side:** `lib/core/url_monitor.dart` line 21 reads from `.env` ✅
- **Location:** Add to `anti_lust_guardian/.env`:
  ```
  GOOGLE_SAFE_BROWSING_API_KEY=your_key_here
  ```

## ⚠️ Backend .env File

I cannot view `backend/.env` (blocked by gitignore), but here's what it MUST contain:

```env
# Stripe Keys
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Price IDs
STRIPE_MONTHLY_PRICE_ID=price_1SZDMWAd7fQadcPJ2JJVS1lB
STRIPE_YEARLY_PRICE_ID=price_1SZDNgAd7fQadcPJIvPs9IPI
STRIPE_LIFETIME_PRICE_ID=price_1SZDRBAd7fQadcPJ1it9QjT0

# Firebase Admin (for Firestore backend access)
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com

# Trial Settings
TRIAL_DAYS=7
REQUIRE_PAYMENT_METHOD_FOR_TRIAL=false
```

**Status:** Please confirm you have these in `backend/.env`!
