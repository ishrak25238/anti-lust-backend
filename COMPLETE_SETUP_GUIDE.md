# 🔑 COMPLETE SETUP GUIDE - All Keys & Payment

## 📍 EXACT FILE LOCATIONS

### Backend Configuration File
**File**: `E:\Anti-Lust app\backend\.env`

This file contains ALL your API keys and secrets.

---

## 🎯 WHAT YOU NEED TO GET

### 1️⃣ Stripe Keys (For Payments) 💳

#### How to Get:
1. Go to: https://dashboard.stripe.com/register
2. Create account (free)
3. Verify your email
4. Go to: https://dashboard.stripe.com/test/apikeys
5. Copy these keys:
   - **Publishable key** (starts with `pk_test_`)
   - **Secret key** (starts with `sk_test_`)

#### Where to Put:
**File**: `E:\Anti-Lust app\backend\.env`

**Add these lines** (replace with your actual keys):
```
STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
```

**File**: `E:\Anti-Lust app\anti_lust_guardian\lib\core\payment_gate.dart`

Find this line (around line 14):
```dart
static const String _stripePublishableKey = 'YOUR_PUBLISHABLE_KEY';
```

Replace with:
```dart
static const String _stripePublishableKey = 'pk_test_YOUR_KEY_HERE';
```

---

### 2️⃣ Email Configuration (For Notifications) 📧

#### Option A: Gmail (Easier)

**How to Get Gmail App Password**:
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification (required)
3. Go to: https://myaccount.google.com/apppasswords
4. Select "Mail" and "Other (Custom name)"
5. Name it "Anti-Lust Guardian"
6. Click "Generate"
7. Copy the 16-character password (no spaces)

**Where to Put**:
**File**: `E:\Anti-Lust app\backend\.env`

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # The 16-char password (remove spaces)
ADMIN_EMAIL=your-email@gmail.com
```

#### Option B: SendGrid (More Professional)

**How to Get**:
1. Go to: https://signup.sendgrid.com/
2. Create free account (100 emails/day free)
3. Verify your email
4. Go to: https://app.sendgrid.com/settings/api_keys
5. Click "Create API Key"
6. Choose "Full Access"
7. Copy the key (starts with `SG.`)

**Where to Put**:
**File**: `E:\Anti-Lust app\backend\.env`

```
SENDGRID_API_KEY=SG.YOUR_KEY_HERE
```

---

### 3️⃣ ML API Keys (Already Done!) ✅

**Already configured in**:
- Backend: `E:\Anti-Lust app\backend\.env` ✅
- Flutter: `E:\Anti-Lust app\anti_lust_guardian\lib\core\ai_threat_prediction.dart` ✅

**Your API Key**:
```
MKO4K06joZ9HVaG-znFkW3S_22wvUFsIevu6hyYHjEk
```

**No action needed - this is done!**

---

## 📝 COMPLETE .env FILE EXAMPLE

**File**: `E:\Anti-Lust app\backend\.env`

**Open this file and make sure it looks like this** (with your actual keys):

```
# Stripe Keys (Get from https://dashboard.stripe.com/test/apikeys)
STRIPE_SECRET_KEY=sk_test_51JAbCdEfGhIjKlMnOpQrStUvWxYz1234567890
STRIPE_PUBLISHABLE_KEY=pk_test_51JAbCdEfGhIjKlMnOpQrStUvWxYz1234567890

# Email Configuration - Gmail
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=yourname@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
ADMIN_EMAIL=yourname@gmail.com

# Database (Already correct - don't change)
DATABASE_URL=sqlite+aiosqlite:///./guardian.db

# Security Keys (Already configured - don't change)
API_SECRET_KEY=XwmIvN3M8GG5rGTYOjvPLoqVDdNitsPxAo8n71vmFtw
JWT_SECRET_KEY=Sxnv9rw17YQ0Qbchtm2G3iMlpr_g7rsL8wM-eRNPU1s
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# ML API Keys (Already configured - don't change)
ML_API_KEYS=MKO4K06joZ9HVaG-znFkW3S_22wvUFsIevu6hyYHjEk,BoFDIA1VwcIS_ZRDThONRM5r_kRk53gIwN1_TBnfnn4,geD13Hsj1gNLPWymlDLbd-o3l7sMMH0raHSG_NQPv4M

# CORS (Already correct - don't change)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost:*

# Rate Limiting (Already correct - don't change)
RATE_LIMIT_PER_MINUTE=100
MAX_IMAGE_SIZE_MB=10
MAX_TEXT_LENGTH=10000

# Monitoring (Optional - leave empty for now)
SENTRY_DSN=
PROMETHEUS_PORT=9090
```

---

## 💳 PAYMENT SETUP - EXACT STEPS

### Step 1: Get Stripe Keys (as shown above)

### Step 2: Add to Backend
**File**: `E:\Anti-Lust app\backend\.env`
```
STRIPE_SECRET_KEY=sk_test_YOUR_KEY
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY
```

### Step 3: Add to Flutter App
**File**: `E:\Anti-Lust app\anti_lust_guardian\lib\core\payment_gate.dart`

Around line 14, change:
```dart
static const String _stripePublishableKey = 'YOUR_PUBLISHABLE_KEY';
```

To:
```dart
static const String _stripePublishableKey = 'pk_test_YOUR_ACTUAL_KEY_HERE';
```

### Step 4: Test Payment

**In your Flutter app**, when user clicks "Subscribe" or "Pay":

```dart
import 'core/payment_gate.dart';

final paymentGate = PaymentGate();

// Create payment
final result = await paymentGate.createPaymentIntent(
  amount: 999, // $9.99 in cents
  priceId: 'premium_monthly',
);

// If successful, result contains payment details
if (result['status'] == 'succeeded') {
  print('Payment successful!');
}
```

### Step 5: Stripe Dashboard
- Test payments: https://dashboard.stripe.com/test/payments
- See customers: https://dashboard.stripe.com/test/customers
- Set up products: https://dashboard.stripe.com/test/products

---

## 🚀 STARTUP CHECKLIST

### Before Running Your App:

**1. Backend Configuration** ✅
- [ ] Open `E:\Anti-Lust app\backend\.env`
- [ ] Add Stripe keys (from https://dashboard.stripe.com/test/apikeys)
- [ ] Add Gmail app password (from https://myaccount.google.com/apppasswords)
- [ ] Save file

**2. Flutter Configuration** ✅
- [ ] Open `payment_gate.dart`
- [ ] Add Stripe publishable key
- [ ] Save file

**3. Start Backend** ✅
```bash
cd "E:\Anti-Lust app\backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**4. Run Flutter App** ✅
```bash
cd "E:\Anti-Lust app\anti_lust_guardian"
flutter run
```

---

## 🔍 HOW TO VERIFY EVERYTHING WORKS

### Test 1: Backend is Running
Open browser: http://localhost:8000

Should see:
```json
{"service":"Anti-Lust Guardian API","status":"operational"}
```

### Test 2: Stripe is Configured
Backend logs should show:
```
Stripe configured: True
```

### Test 3: Email is Configured
Backend logs should show:
```
Email configured: True
```

### Test 4: Make Test Payment
In Stripe test mode, use:
- Card: `4242 4242 4242 4242`
- Date: Any future date
- CVC: Any 3 digits
- ZIP: Any 5 digits

---

## 📞 QUICK REFERENCE

| What | Get From | Put In |
|------|----------|---------|
| Stripe Secret | https://dashboard.stripe.com/test/apikeys | `backend\.env` |
| Stripe Publishable | https://dashboard.stripe.com/test/apikeys | `backend\.env` + `payment_gate.dart` |
| Gmail Password | https://myaccount.google.com/apppasswords | `backend\.env` |
| ML API Key | Already done! ✅ | Already configured ✅ |

---

## ⚠️ COMMON MISTAKES

❌ **Using live keys in test mode**
✅ Use test keys (start with `sk_test_` and `pk_test_`)

❌ **Gmail password instead of app password**
✅ Must use 16-character app password from Google

❌ **Spaces in app password**
✅ Remove all spaces: `abcd efgh ijkl mnop` → `abcdefghijklmnop`

❌ **Not saving .env file**
✅ Save and restart backend after changes

---

## 🎯 NEXT STEPS

1. **Get Stripe keys** (5 minutes)
   - Go to: https://dashboard.stripe.com/register
   - Get test API keys
   - Add to `.env` and `payment_gate.dart`

2. **Get Gmail app password** (5 minutes)
   - Go to: https://myaccount.google.com/apppasswords
   - Generate password
   - Add to `.env`

3. **Test everything**
   - Start backend
   - Run Flutter app
   - Try making a test payment

**That's it! You're done!** 🚀
