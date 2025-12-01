# 🎉 QUICK START: Authentication Setup

All files have been created! Follow these steps to complete setup:

---

## ✅ What's Been Created

1. **`scripts/auth.js`** - Firebase authentication module
2. **`login.html`** - Beautiful login page with Google sign-in
3. **Updated `index.html`** - Added auth checks and script imports
4. **Updated `stripe-payment.js`** - Links payments to user accounts

---

## 🔥 Step 1: Set Up Firebase (10 minutes)

### Create Project
1. Go to: https://console.firebase.google.com
2. Click "Add project"
3. Project name: `anti-lust-guardian`
4. Click "Create project"

### Enable Google Auth
1. Click "Authentication" → "Get started"
2. Click "Sign-in method" tab
3. Enable "Google"
4. Click "Save"

### Get Your Config
1. Click ⚙️ → "Project settings"
2. Scroll to "Your apps"
3. Click **</>** (Web icon)
4. Register app: `Anti-Lust Guardian`
5. **COPY** the firebaseConfig object

### Add Config to Your Code
Open `e:\Anti-Lust app\website\scripts\auth.js`

Find line 10 and replace:
```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY_HERE",
    // ...
};
```

With your actual config from Firebase!

---

## 💳 Step 2: Set Up Stripe Payment Links

### Create Payment Links (Easiest!)
1. Go to Stripe Dashboard: https://dashboard.stripe.com
2. Click "Payment links" → "New"
3. Create link for **Monthly** product ($17/month)
4. Create link for **Lifetime** product ($299)
5. **COPY** both URLs

### Add Links to Code
Open `e:\Anti-Lust app\website\scripts/stripe-payment.js`

Find line 129 and replace:
```javascript
const PAYMENT_LINKS = {
    monthly: 'https://buy.stripe.com/YOUR_MONTHLY_LINK',
    lifetime: 'https://buy.stripe.com/YOUR_LIFETIME_LINK' 
};
```

---

## 🧪 Step 3: Test It!

1. **Open website**: `file:///e:/Anti-Lust%20app/website/index.html`
2. **Click "START TRIAL"**
   - Should redirect to `/login.html`
3. **Click "Continue with Google"**
   - Sign in with Google
   - Should redirect back to payment
4. **Complete test payment**
   - Use card: `4242 4242 4242 4242`
5. **Check Firestore** 
   - Firebase Console → Firestore Database
   - Should see your user with subscription data!

---

## 📁 File Locations

All your files are ready at:
- `e:\Anti-Lust app\website\scripts\auth.js`
- `e:\Anti-Lust app\website\login.html`
- `e:\Anti-Lust app\website\index.html` (updated)
- `e:\Anti-Lust app\website\scripts\stripe-payment.js` (updated)

---

## 🎯 How It Works

```
User clicks "START TRIAL"
  ↓
Auth check: Logged in?
  ↓ NO
Redirect to /login.html
  ↓
Sign in with Google
  ↓
Redirect to payment
  ↓ YES
Pass user email + ID to Stripe
  ↓
Payment success
  ↓
Save subscription to Firebase
  ↓
Access dashboard
```

---

## 🆘 Need Help?

Check the detailed guide:
`e:\Anti-Lust app\AUTHENTICATION_SETUP_GUIDE.md`

---

**That's it! Two configs and you're done!** 🚀
