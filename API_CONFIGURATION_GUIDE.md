# API Configuration Guide

## Quick Setup

### 1. Backend `.env` File

Create/edit `backend/.env` with your API keys:

```bash
# Required for Payment
STRIPE_SECRET_KEY=sk_live_your_stripe_key_here

# Required for Email Notifications
SENDGRID_API_KEY=SG.your_sendgrid_key_here

# Optional - For AI features
OPENAI_API_KEY=sk-your_openai_key_here

# Optional - For Firebase sync
FIREBASE_SERVICE_ACCOUNT_JSON=path/to/firebase-credentials.json

# Security (generate a random string)
JWT_SECRET_KEY=your-random-secret-string-here-min-32-chars
```

## Getting API Keys

### ✅ Stripe (You Have This)

Your Stripe secret key → Put in `backend/.env`:
```
STRIPE_SECRET_KEY=sk_live_xxxxx
```

### 📧 SendGrid (Email Service)

**Free Tier: 100 emails/day**

1. **Sign up:** https://signup.sendgrid.com/
2. **Verify email** 
3. **Create API Key:**
   - Go to: Settings → API Keys
   - Click "Create API Key"
   - Name: "Anti-Lust Guardian"
   - Permissions: "Full Access"
   - Copy the key (starts with `SG.`)
4. **Add to `.env`:**
   ```
   SENDGRID_API_KEY=SG.your_key_here
   ```

**Alternative (Free):** Use Gmail SMTP instead of SendGrid
- Update `backend/services/email_service.py` to use Gmail
- No API key needed, just your Gmail credentials

### 🤖 OpenAI (Optional - For AI Features)

**Cost: Pay-as-you-go (optional feature)**

1. **Sign up:** https://platform.openai.com/signup
2. **Add payment method:** https://platform.openai.com/account/billing
3. **Create API Key:**
   - Go to: API Keys → Create new secret key
   - Name: "Anti-Lust Guardian"
   - Copy the key (starts with `sk-`)
4. **Add to `.env`:**
   ```
   OPENAI_API_KEY=sk-your_key_here
   ```

**Note:** OpenAI is optional - system works without it.

### 🔥 Firebase (Optional - For Firestore Sync)

**Free Tier: 50k read/20k writes per day**

1. **Create Project:** https://console.firebase.google.com/
2. **Enable Firestore:**
   - Build → Firestore Database → Create Database
   - Start in production mode
3. **Get Service Account:**
   - Project Settings (⚙️) → Service Accounts
   - Click "Generate new private key"
   - Download JSON file
4. **Save JSON:**
   - Save as: `backend/firebase-credentials.json`
   - Add to `.env`:
     ```
     FIREBASE_SERVICE_ACCOUNT_JSON=backend/firebase-credentials.json
     ```

**Note:** Firebase is optional - system works without it.

## Configuration Files

### For Local Development

**File:** `backend/.env` (create this file)

```bash
# Copy this template and fill in your keys

# === REQUIRED ===
STRIPE_SECRET_KEY=your_stripe_key_here

# === IMPORTANT (for emails) ===
SENDGRID_API_KEY=your_sendgrid_key_here

# === OPTIONAL ===
OPENAI_API_KEY=your_openai_key_here
FIREBASE_SERVICE_ACCOUNT_JSON=backend/firebase-credentials.json

# === SECURITY ===
JWT_SECRET_KEY=change-this-to-a-random-string-min-32-characters
ML_API_KEYS=optional-custom-api-keys-comma-separated

# === OTHER ===
DATABASE_URL=sqlite:///./data/app.db
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### For Google Cloud Run Deployment

Set environment variables during deployment:

```bash
gcloud run deploy anti-lust-backend \
  --source . \
  --region us-central1 \
  --set-env-vars "STRIPE_SECRET_KEY=sk_live_xxxxx" \
  --set-env-vars "SENDGRID_API_KEY=SG.xxxxx" \
  --set-env-vars "JWT_SECRET_KEY=your-random-secret" \
  --set-env-vars "OPENAI_API_KEY=sk-xxxxx" \
  --memory 2Gi \
  --cpu 1
```

Or set in Cloud Console:
1. Cloud Run → Select Service → Edit & Deploy New Revision
2. Container → Environment Variables
3. Add each key-value pair

## Priority Setup

### Minimum Required (System Works)
1. ✅ STRIPE_SECRET_KEY (you have this)
2. ✅ JWT_SECRET_KEY (generate random string)

### Recommended (Full Features)
3. 📧 SENDGRID_API_KEY (for email alerts)

### Optional (Enhanced Features)
4. 🤖 OPENAI_API_KEY (AI enhancements)
5. 🔥 FIREBASE (real-time sync)

## Quick Start

1. **Create `.env` file:**
   ```bash
   cd backend
   notepad .env
   ```

2. **Add your keys:**
   ```
   STRIPE_SECRET_KEY=sk_live_your_actual_key
   SENDGRID_API_KEY=SG.get_from_sendgrid_com
   JWT_SECRET_KEY=randomly_generated_secret_min_32_chars
   ```

3. **Test:**
   ```bash
   python test_final_complete.py
   ```

4. **Deploy:**
   ```bash
   gcloud run deploy anti-lust-backend --source . --region us-central1 --set-env-vars "STRIPE_SECRET_KEY=sk_live_xxxxx,SENDGRID_API_KEY=SG.xxxxx,JWT_SECRET_KEY=your_secret"
   ```

## Security Notes

⚠️ **NEVER commit `.env` to Git** - it's already in `.gitignore`

⚠️ **Generate strong JWT_SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

⚠️ **Use test keys for development:**
- Stripe: Use `sk_test_xxxxx` for testing
- SendGrid: Create separate API key for dev/prod

## Troubleshooting

**"Payment service not configured"**
→ Check `STRIPE_SECRET_KEY` in `.env`

**"Email service not configured"**
→ Add `SENDGRID_API_KEY` to `.env`

**"OpenAI integration failed"**
→ System works without it - it's optional

**Firebase errors**
→ System works without it - it's optional
