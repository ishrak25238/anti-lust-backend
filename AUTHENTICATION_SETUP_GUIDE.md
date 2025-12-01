# 🔐 User Authentication Setup Guide

Complete guide to add Google Login and user management to your Anti-Lust Guardian website.

---

## 🎯 What You Need

**The Problem**: Users need to login before they can pay and access the service.

**The Solution**: Add Google OAuth authentication using Firebase (easiest method).

---

## 📋 Quick Overview

**User Flow**:
1. User visits website → Clicks "START TRIAL"
2. Redirected to login page → Signs in with Google
3. Authenticated → Proceeds to Stripe payment
4. Payment successful → Access granted to dashboard
5. Can now use the service with their subscription

---

## 🚀 Step 1: Set Up Firebase (10 minutes)

### Create Firebase Project

1. Go to: **https://console.firebase.google.com**
2. Click **"Add project"**
3. Enter project name: `anti-lust-guardian`
4. Disable Google Analytics (optional)
5. Click **"Create project"**

### Enable Google Authentication

1. In Firebase Console, click **"Authentication"** (left sidebar)
2. Click **"Get started"**
3. Click **"Sign-in method"** tab
4. Click **"Google"** → Click **"Enable"**
5. Select a support email
6. Click **"Save"**

### Get Your Firebase Config

1. Click the **⚙️ gear icon** → **"Project settings"**
2. Scroll down to **"Your apps"**
3. Click the **</> (Web)** icon
4. Register app name: `Anti-Lust Guardian Web`
5. Click **"Register app"**
6. **COPY** the Firebase config (looks like this):

```javascript
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "anti-lust-guardian.firebaseapp.com",
  projectId: "anti-lust-guardian",
  storageBucket: "anti-lust-guardian...",
  messagingSenderId: "123...",
  appId: "1:123..."
};
```

**SAVE THIS!** You'll need it in the next step.

---

## 🔧 Step 2: Add Authentication Files

I'll create all the necessary files for you. Here's what you need:

### File 1: `scripts/auth.js` (Authentication Logic)

This file handles Google login, logout, and session management.

### File 2: `login.html` (Login Page)

Beautiful login page with Google Sign-In button.

### File 3: Update `index.html` (Protect Pricing Buttons)

Redirect to login if user is not authenticated.

---

## 📝 Step 3: Update Your Firebase Config

Once I create the `auth.js` file, you need to:

1. Open `e:\Anti-Lust app\website\scripts\auth.js`
2. Find this section at the top:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  // ...
};
```

3. **Replace** with your actual Firebase config from Step 1

---

## 💳 Step 4: Link Payments to Users

### Update Stripe Integration

When a user clicks "START TRIAL" or "GET LIFETIME":

1. Check if logged in → If not, redirect to `/login.html`
2. If logged in → Get user email and ID
3. Pass to Stripe with payment
4. Stripe creates customer linked to that user
5. After payment → Save subscription to user profile

### User Profile Structure

Firebase stores user data like this:

```javascript
{
  uid: "abc123...",           // Unique user ID
  email: "user@gmail.com",    // From Google
  displayName: "John Doe",    // From Google
  photoURL: "https://...",    // Profile picture
  
  // Custom data you add:
  subscription: {
    type: "monthly",          // or "lifetime"
    status: "active",         // or "trial", "cancelled"
    stripeCustomerId: "cus_...",
    subscriptionId: "sub_...",
    startedAt: "2025-11-28"
  }
}
```

---

## 🛡️ Step 5: Protect Dashboard

Add this to the top of `dashboard.html`:

```javascript
<script type="module">
  import { auth, onAuthStateChanged } from './scripts/auth.js';
  
  // Check if user is logged in
  onAuthStateChanged(auth, (user) => {
    if (!user) {
      // Not logged in - redirect to login
      window.location.href = '/login.html?redirect=/dashboard.html';
    } else {
      // Logged in - show dashboard
      document.getElementById('userEmail').textContent = user.email;
      loadUserData(user); // Load subscription info
    }
  });
</script>
```

---

## ✅ Step 6: Test Everything

### Test Login Flow

1. Open your website: `http://localhost:8000` (or your deployed URL)
2. Click **"START TRIAL"**
3. Should redirect to `/login.html`
4. Click **"Sign in with Google"**
5. Choose your Google account
6. Should redirect back to payment page

### Test Payment Flow

1. Complete the Stripe test payment
2. Should save subscription to your Firebase user profile
3. Redirect to dashboard
4. Dashboard should show your email and subscription status

### Test Protection

1. Open a new private/incognito window
2. Try to access `/dashboard.html` directly
3. Should redirect to login page ✅

---

## 🔑 Complete Authentication Flow

```
┌─────────────────────────────────────────────────────────┐
│ 1. User visits website (index.html)                     │
│    ↓                                                     │
│ 2. Clicks "START TRIAL" button                          │
│    ↓                                                     │
│ 3. Check: Is user logged in?                            │
│    ├─ NO → Redirect to login.html                       │
│    │   ↓                                                 │
│    │ 4. User clicks "Sign in with Google"               │
│    │   ↓                                                 │
│    │ 5. Google OAuth popup                               │
│    │   ↓                                                 │
│    │ 6. Firebase creates user account                    │
│    │   ↓                                                 │
│    │ 7. Redirect back to payment                         │
│    │                                                      │
│    └─ YES → Continue                                     │
│        ↓                                                  │
│ 8. Redirect to Stripe Checkout                          │
│    - Pass user email and ID to Stripe                   │
│    ↓                                                     │
│ 9. User completes payment                               │
│    ↓                                                     │
│ 10. Payment success webhook                             │
│     - Save subscription to user profile                 │
│     ↓                                                    │
│ 11. Redirect to dashboard.html                          │
│     - Show user email                                    │
│     - Show subscription status                           │
│     - Allow access to service                            │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 What This Gives You

### For Users
- ✅ Easy Google login (no password to remember)
- ✅ Secure authentication
- ✅ Personalized dashboard
- ✅ Subscription management
- ✅ Can access from any device

### For You
- ✅ Know who your users are
- ✅ Track subscriptions
- ✅ Send emails to users
- ✅ Prevent unauthorized access
- ✅ User analytics

---

## 🆘 Common Issues

**"Firebase not defined"**
- Make sure you added the Firebase SDK script tags
- Check browser console for errors

**"Redirect loop"**
- Check your redirect URLs in auth.js
- Make sure login page doesn't redirect to itself

**"Google sign-in popup blocked"**
- Allow popups for your website
- Or use redirect mode instead of popup

---

## 🚀 Ready to Implement?

I can create all the files for you right now:

1. `scripts/auth.js` - Authentication logic
2. `login.html` - Login page
3. Update `index.html` - Add auth checks
4. Update `dashboard.html` - Protect with auth
5. Update `stripe-payment.js` - Link payments to users

**Just let me know and I'll create everything!** 

Then you just need to:
1. Set up Firebase (10 min)
2. Copy your Firebase config into `auth.js`
3. Test it out!

---

**Questions?** Let me know what you'd like me to clarify! 😊
