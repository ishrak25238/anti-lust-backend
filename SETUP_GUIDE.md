# Anti-Lust Guardian - Setup Guide

## 🚀 Quick Start

### 1. Install Flutter

**Download & Install:**
- Go to https://docs.flutter.dev/get-started/install
- Download Flutter SDK for Windows
- Extract to `C:\flutter`
- Add to PATH: `C:\flutter\bin`

**Verify:**
```powershell
flutter doctor
```

### 2. Clone & Setup Project

```powershell
cd "e:\Anti-Lust app\anti_lust_guardian"
flutter pub get
```

### 3. Setup Supabase (FREE Backend)

1. Go to https://supabase.com
2. Click "Start your project"
3. Create new organization (FREE)
4. Create new project:
   - Name: `anti-lust-guardian`
   - Database Password: (choose strong password)
   - Region: (closest to you)
5. Wait for project to deploy (~2 minutes)
6. Go to **Settings** → **API**
7. Copy:
   - Project URL
   - `anon` `public` key

8. **Run SQL Schema:**
   - Go to **SQL Editor**
   - Click "New query"
   - Paste contents of `supabase_schema.sql`
   - Click "Run"

### 4. Setup Stripe (FREE Payment Processing)

1. Go to https://stripe.com
2. Create account (no credit card needed)
3. Go to **Developers** → **API keys**
4. Copy:
   - Publishable key (starts with `pk_test_`)
   - Secret key (starts with `sk_test_`)

5. **Create Products:**
   - Go to **Products**
   - Click "+ Add product"
   
   **Product 1: Monthly Pro**
   - Name: Monthly Pro
   - Price: $9.99 USD
   - Billing period: Monthly
   - Copy the Price ID (starts with `price_`)
   
   **Product 2: Yearly Pro**
   - Name: Yearly Pro
   - Price: $99.00 USD
   - Billing period: Yearly
   - Copy the Price ID
   
   **Product 3: Lifetime Access**
   - Name: Lifetime Access
   - Price: $299.00 USD
   - Billing period: One-time
   - Copy the Price ID

### 5. Configure Environment

Create `.env` file in `anti_lust_guardian/` folder:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key

STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key

STRIPE_MONTHLY_PRICE_ID=price_monthly_xxxx
STRIPE_YEARLY_PRICE_ID=price_yearly_xxxx
STRIPE_LIFETIME_PRICE_ID=price_lifetime_xxxx

GOOGLE_SAFE_BROWSING_API_KEY=your_api_key_here
```

### 6. Run the App

**Android (requires Android Studio):**
```powershell
flutter run -d android
```

**Windows:**
```powershell
flutter run -d windows
```

**Web (for testing):**
```powershell
flutter run -d chrome
```

---

## 💰 Monetization

**Payment Required Model:**
- Users MUST subscribe before accessing protection
- No free tier
- 3 pricing options:
  - Monthly: $9.99/mo
  - Yearly: $99/year (17% discount)
  - Lifetime: $299 (one-time)

**Stripe Fees:**
- 2.9% + $0.30 per transaction
- Example: $9.99 charge = $0.59 fee = $9.40 profit

**Revenue Projections:**
- 100 users (avg $9.99/mo) = $999/mo → ~$940 after Stripe fees
- 1,000 users = $9,990/mo → ~$9,400 after fees
- 10,000 users = $99,900/mo → ~$94,000 after fees

---

## 🔧 Features Implemented

✅ **Payment System**
- Mandatory subscription (no free access)
- Stripe integration
- 3 pricing tiers
- Beautiful paywall screen

✅ **Authentication**
- Supabase auth (email/password)
- Secure user management
- Password reset

✅ **Database**
- User profiles
- Subscription tracking
- Device management
- Threat intelligence

✅ **Cross-Platform**
- Android, iOS, Windows, macOS, Linux support
- Single codebase

---

## 📋 Next Steps (Day 2-3)

Will add:
- URL monitoring & blocking
- AI content filtering (TensorFlow Lite)
- Google Safe Browsing API integration
- Streak tracking & gamification
- Focus features
- Production builds

---

## 🆘 Troubleshooting

**Flutter not found:**
- Make sure `C:\flutter\bin` is in your PATH
- Restart terminal after adding to PATH

**Supabase connection error:**
- Double-check URL and anon key in `.env`
- Make sure SQL schema was run successfully

**Stripe payment not working:**
- Verify you're using TEST keys (not live keys)
- Check that Price IDs match the products you created

---

**Your app enforces payment BEFORE granting access.** Users can't bypass - they MUST pay to use protection features!
