# 🚀 YOUR ACTION PLAN - Step by Step

**Goal:** Get the Anti-Lust Guardian app running on Android

**Time Needed:** 1-2 hours (if you already have accounts)

---

## 📋 PHASE 1: Get Your API Keys (30-60 minutes)

### STEP 1: Get Supabase Credentials

**What:** Database and authentication backend

**How:**
1. Go to: https://supabase.com/dashboard
2. Sign in (or create free account)
3. Create a new project OR select existing "anti-lust-guardian" project
4. Click **Settings** (gear icon on left sidebar)
5. Click **API** section
6. **COPY these two values:**
   - `Project URL` → This is your `SUPABASE_URL`
   - `anon public` key → This is your `SUPABASE_ANON_KEY`

**Write them down temporarily:**
```
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxx...
```

---

### STEP 2: Get Stripe Keys

**What:** Payment processing for subscriptions

**How:**
1. Go to: https://dashboard.stripe.com/
2. Sign in (or create account)
3. Make sure you're in **TEST MODE** (toggle in top right)
4. Click **Developers** in top nav
5. Click **API keys**
6. **COPY these:**
   - `Publishable key` (starts with `pk_test_`)
   - `Secret key` (click "Reveal" first, starts with `sk_test_`)

**Write them down:**
```
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxx
```

---

### STEP 3: Create Stripe Products & Prices

**Still in Stripe Dashboard:**

1. Click **Products** in left sidebar
2. Click **+ Add product**
3. Create three products:

**Product 1: Monthly Subscription**
- Name: `Anti-Lust Guardian Monthly`
- Price: `$9.99`
- Billing: `Recurring` → `Monthly`
- Click **Save**
- **COPY the Price ID** (starts with `price_`)

**Product 2: Yearly Subscription**
- Name: `Anti-Lust Guardian Yearly`
- Price: `$99.99`
- Billing: `Recurring` → `Yearly`
- Click **Save**
- **COPY the Price ID**

**Product 3: Lifetime Access**
- Name: `Anti-Lust Guardian Lifetime`
- Price: `$299.99`
- Billing: `One time`
- Click **Save**
- **COPY the Price ID**

**Write them down:**
```
STRIPE_MONTHLY_PRICE_ID=price_xxxxxxxxxxxxxx
STRIPE_YEARLY_PRICE_ID=price_xxxxxxxxxxxxxx
STRIPE_LIFETIME_PRICE_ID=price_xxxxxxxxxxxxxx
```

---

### STEP 4: Get Google Safe Browsing API Key

**What:** Checks URLs against Google's malware/phishing database

**How:**
1. Go to: https://console.cloud.google.com/
2. Sign in with Google account
3. Create new project OR select existing
4. Click **APIs & Services** → **Library**
5. Search: `Safe Browsing API`
6. Click it, then click **ENABLE**
7. Go to **Credentials** (left sidebar)
8. Click **+ CREATE CREDENTIALS** → **API Key**
9. **COPY the API key** (starts with `AIza`)

**Optional but recommended:**
- Click the key name to edit
- Under "API restrictions" → Select APIs
- Choose "Safe Browsing API"
- Click **Save**

**Write it down:**
```
GOOGLE_SAFE_BROWSING_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 📝 PHASE 2: Update Your Code (10 minutes)

### STEP 5: Edit the .env File

1. Open File Explorer
2. Navigate to: `e:\Anti-Lust app\anti_lust_guardian\`
3. Find the file named `.env`
4. Open it with Notepad or VS Code
5. **Replace ALL the placeholder values** with your real keys:

```env
# Supabase Configuration
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxx

# Stripe Configuration (Test Keys)
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxx

# Stripe Price IDs
STRIPE_MONTHLY_PRICE_ID=price_xxxxxxxxxxxxxx
STRIPE_YEARLY_PRICE_ID=price_xxxxxxxxxxxxxx
STRIPE_LIFETIME_PRICE_ID=price_xxxxxxxxxxxxxx

# Google Safe Browsing API
GOOGLE_SAFE_BROWSING_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxx

# App Configuration
TRIAL_DAYS=7
REQUIRE_PAYMENT_METHOD_FOR_TRIAL=true
```

6. **Save the file** (Ctrl+S)

---

### STEP 6: Update main.dart to Use Environment Variables

**YOU DON'T NEED TO DO THIS - I'LL DO IT FOR YOU IN NEXT STEP**

Just so you know what needs to happen:
- Replace hardcoded `'YOUR_SUPABASE_URL'` with code that reads from `.env`
- Same for `'YOUR_SUPABASE_ANON_KEY'`

---

### STEP 7: Update url_monitor.dart

**YOU DON'T NEED TO DO THIS - I'LL DO IT FOR YOU IN NEXT STEP**

Same thing - replace hardcoded API key with environment variable.

---

## 🧪 PHASE 3: Test the App (10 minutes)

### STEP 8: Load Environment Variables

After I fix the code files, you'll run:

```powershell
cd "e:\Anti-Lust app\anti_lust_guardian"
flutter pub get
```

---

### STEP 9: Connect Android Device or Start Emulator

**Option A: Real Android Phone**
1. Enable Developer Options on your phone
2. Enable USB Debugging
3. Connect via USB
4. Check connection: `flutter devices`

**Option B: Android Emulator**
1. Open Android Studio
2. Click AVD Manager
3. Create/start an emulator
4. Check it shows up: `flutter devices`

---

### STEP 10: Run the App

```powershell
flutter run
```

Watch for:
- ✅ "Successfully initialized Firebase Core"
- ✅ Supabase connection successful
- ✅ App UI loads

---

## 🎯 QUICK CHECKLIST

Before you start, make sure you have accounts at:
- [ ] Supabase (free tier is fine)
- [ ] Stripe (test mode is fine)
- [ ] Google Cloud Console (free tier)

---

## ⏱️ TIME BREAKDOWN

| Task | Time |
|------|------|
| Create accounts (if needed) | 15-30 min |
| Get Supabase keys | 5 min |
| Get Stripe keys | 5 min |
| Create Stripe products | 10 min |
| Get Google API key | 10 min |
| Update .env file | 5 min |
| Wait for me to fix code | 5 min |
| Test run | 5 min |
| **TOTAL** | **60-90 min** |

---

## 🚨 IMPORTANT NOTES

1. **Keep your keys SECRET**
   - Never share them
   - Never commit to GitHub
   - .env is already gitignored ✅

2. **Use TEST mode for Stripe**
   - Don't use live keys yet
   - Test cards: 4242 4242 4242 4242

3. **Free tiers are enough**
   - Supabase: Free tier works
   - Google Cloud: Free tier works
   - Stripe: Free for test mode

---

## ❓ WHAT IF YOU GET STUCK?

### "I don't have a Supabase account"
→ Create one at supabase.com (free)

### "I can't find my API keys"
→ Follow screenshots in each service's documentation

### "Stripe won't give me an API key"
→ Make sure you're in TEST mode (toggle in top right)

### "Google Cloud is confusing"
→ Just need: Enable API → Create API Key → Copy it

### "The app crashes on startup"
→ Check console output for error messages
→ Make sure all keys are correctly copied

---

## 🎉 WHAT HAPPENS NEXT?

Once you:
1. ✅ Get all your API keys
2. ✅ Put them in `.env`
3. ✅ Tell me you're done

I will:
1. Fix `main.dart` to read from `.env`
2. Fix `url_monitor.dart` to use the API key
3. Test that the code compiles
4. Give you the command to run

Then YOU will:
1. Run `flutter run`
2. See your app working!
3. Test features

---

## 📞 YOUR IMMEDIATE ACTION

**RIGHT NOW, DO THIS:**

1. Open 3 browser tabs:
   - Tab 1: https://supabase.com/dashboard
   - Tab 2: https://dashboard.stripe.com/
   - Tab 3: https://console.cloud.google.com/

2. Sign into all three

3. Get your keys following STEP 1-4 above

4. Write them ALL down in a temporary text file

5. **Tell me:** "I have all the keys ready"

Then I'll help you update the code!

---

**BOTTOM LINE:** You need to gather API keys from 3 services. That's it. Then I'll handle the code changes.
