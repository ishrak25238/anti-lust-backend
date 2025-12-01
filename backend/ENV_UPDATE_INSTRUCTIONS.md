# Updated .env File - Copy This Content

## ✅ What I've Done:
1. **Generated secure random keys** for API_SECRET_KEY and JWT_SECRET_KEY
2. **Organized** all configuration with clear sections
3. **Added Firebase mobile** configuration placeholders

---

## 📋 Copy This to Your `.env` File:

Open: `e:\Anti-Lust app\backend\.env` and replace **EVERYTHING** with:

```env
# ============================================
# STRIPE PAYMENT INTEGRATION
# ============================================
STRIPE_SECRET_KEY="sk_live_YOUR_STRIPE_SECRET_KEY_HERE"
STRIPE_PUBLISHABLE_KEY="pk_live_YOUR_STRIPE_PUBLISHABLE_KEY_HERE"

# ============================================
# EMAIL NOTIFICATIONS (Gmail SMTP)
# ============================================
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USERNAME=""  # YOUR_EMAIL@gmail.com
SMTP_PASSWORD=""  # Generate at: https://myaccount.google.com/apppasswords
ADMIN_EMAIL=""    # admin@yourdomain.com

# ============================================
# DATABASE
# ============================================
DATABASE_URL="sqlite+aiosqlite:///./guardian.db"

# ============================================
# SECURITY (AUTO-GENERATED SECURE KEYS) ✅
# ============================================
API_SECRET_KEY="U5OCdve88VC5BrxCqJZosy9HHvn/kaI/Y4GyfCyEF8w="
JWT_SECRET_KEY="k1jpNbAGGZtdcxnGwYdIP2UuVGWo74TJRVZZA1IwN34="
JWT_ALGORITHM="HS256"
JWT_EXPIRATION_HOURS="24"

# ============================================
# AI SERVICES
# ============================================
OPENAI_API_KEY="sk-YOUR_OPENAI_API_KEY_HERE"

# ============================================
# FIREBASE (For Mobile Apps)
# ============================================
FIREBASE_PROJECT_ID="anti-lust-guardian"
# Get these from: Firebase Console > Project Settings > Service Accounts > Generate New Private Key
# FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_KEY_HERE\n-----END PRIVATE KEY-----"
# FIREBASE_CLIENT_EMAIL="firebase-adminsdk-xxxxx@anti-lust-guardian.iam.gserviceaccount.com"

# ============================================
# API CONFIGURATION
# ============================================
ML_API_KEYS="client-app-key-1"
ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8080,https://yourdomain.com"
RATE_LIMIT_PER_MINUTE="100"
MAX_IMAGE_SIZE_MB="10"
MAX_TEXT_LENGTH="10000"

# ============================================
# OPTIONAL SERVICES (Uncomment & add keys when ready)
# ============================================

# VPN/Proxy Detection
# IPHUB_API_KEY="your-iphub-key"  # Get from: https://iphub.info/

# Email Service (Alternative to SMTP)
# SENDGRID_API_KEY="SG.xxxxxxxxx"  # Get from: https://sendgrid.com/
# SENDGRID_FROM_EMAIL="noreply@yourdomain.com"

# SMS Notifications
# TWILIO_API_KEY="ACxxxxxxxxxx"  # Get from: https://twilio.com/
# TWILIO_API_SECRET="your-secret"
# TWILIO_SENDER_ID="+1234567890"

# Push Notifications (Firebase Cloud Messaging)
# FCM_SERVER_KEY="your-fcm-server-key"  # Get from: Firebase Console > Project Settings > Cloud Messaging
```

---

## 🔐 What Changed:

✅ **API_SECRET_KEY** = `U5OCdve88VC5BrxCqJZosy9HHvn/kaI/Y4GyfCyEF8w=` (secure random)  
✅ **JWT_SECRET_KEY** = `k1jpNbAGGZtdcxnGwYdIP2UuVGWo74TJRVZZA1IwN34=` (secure random)  
✅ **Added Firebase** configuration section  
✅ **Organized** all services with clear headers
