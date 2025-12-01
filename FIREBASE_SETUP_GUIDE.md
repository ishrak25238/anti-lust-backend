# Firebase Setup - Step by Step Guide

## Part 1: Get Your Firebase Config (5 minutes)

### Step 1: Create/Access Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click **"Add project"** (or select existing project)
3. Name it: `Anti-Lust Guardian` (or your choice)
4. Enable Google Analytics: **Optional**
5. Click **"Create project"**

### Step 2: Get Your Config Keys
1. In Firebase Console → Click ⚙️ (Settings) → **Project settings**
2. Scroll down to "Your apps"
3. Click the **Web icon** (`</>`) → "Add app"
4. App nickname: `Anti-Lust Web`
5. Click **"Register app"**
6. **Copy the config object** (looks like this):
   ```javascript
   const firebaseConfig = {
     apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXX",
     authDomain: "your-project.firebaseapp.com",
     projectId: "your-project-id",
     storageBucket: "your-project.appspot.com",
     messagingSenderId: "123456789",
     appId: "1:123456789:web:xxxxx"
   };
   ```

### Step 3: Update auth.js
1. Open: `e:\Anti-Lust app\website\scripts\auth.js`
2. Find lines 6-14
3. **Replace** the placeholder config with your actual config
4. Save the file

---

## Part 2: Enable Authentication (3 minutes)

### Step 4: Enable Google Sign-In
1. In Firebase Console → **Authentication** (left sidebar)
2. Click **"Get started"**
3. Go to **"Sign-in method"** tab
4. Click **"Google"**
5. Toggle **"Enable"**
6. Select a **support email**
7. Click **"Save"**

### Step 5: Enable Email/Password (Optional)
1. Still in "Sign-in method"
2. Click **"Email/Password"**
3. Toggle **"Enable"**
4. Click **"Save"**

---

## Part 3: Set Up Firestore Database (3 minutes)

### Step 6: Create Firestore
1. In Firebase Console → **Firestore Database** (left sidebar)
2. Click **"Create database"**
3. Choose **"Start in test mode"** (for now)
4. Select location: **us-central** (or nearest to you)
5. Click **"Enable"**

### Step 7: Create Collection
1. Click **"+ Start collection"**
2. Collection ID: `users`
3. Click **"Next"**
4. Document ID: **Auto-ID**
5. Add field:
   - Field: `email`
   - Type: `string`
   - Value: `test@example.com`
6. Click **"Save"**

---

## Part 4: Deploy Firebase Functions (10 minutes)

### Step 8: Install Firebase CLI
Open PowerShell/Terminal:
```powershell
npm install -g firebase-tools
```

Verify installation:
```powershell
firebase --version
```

### Step 9: Login to Firebase
```powershell
firebase login
```
- Opens browser → Sign in with Google
- Click **"Allow"**

### Step 10: Initialize Functions
```powershell
cd "e:\Anti-Lust app\backend"
firebase init functions
```

Answer the prompts:
- **Select project**: Choose your Firebase project
- **Language**: JavaScript
- **ESLint**: No
- **Install dependencies**: Yes

### Step 11: Copy Webhook Code
1. Open: `e:\Anti-Lust app\backend\functions\index.js`
2. **Replace entire content** with:
   ```javascript
   const functions = require('firebase-functions');
   const admin = require('firebase-admin');
   const stripe = require('stripe')(functions.config().stripe.secret_key);

   admin.initializeApp();

   exports.stripeWebhook = functions.https.onRequest(async (req, res) => {
       const sig = req.headers['stripe-signature'];
       const webhookSecret = functions.config().stripe.webhook_secret;

       let event;
       try {
           event = stripe.webhooks.constructEvent(req.rawBody, sig, webhookSecret);
       } catch (err) {
           console.error('Webhook error:', err.message);
           return res.status(400).send(`Webhook Error: ${err.message}`);
       }

       if (event.type === 'checkout.session.completed') {
           const session = event.data.object;
           const uid = session.client_reference_id;
           
           if (!uid) {
               return res.status(400).send('No user ID');
           }

           const lineItems = await stripe.checkout.sessions.listLineItems(session.id);
           const amount = lineItems.data[0].amount_total;
           const plan = amount >= 15000 ? 'lifetime' : 'monthly';

           await admin.firestore().collection('users').doc(uid).update({
               subscription: {
                   status: 'active',
                   plan: plan,
                   stripeCustomerId: session.customer,
                   amount: amount / 100,
                   startDate: admin.firestore.FieldValue.serverTimestamp()
               }
           });

           console.log('✅ Subscription updated:', uid, plan);
       }

       res.json({ received: true });
   });
   ```

### Step 12: Install Stripe Package
```powershell
cd "e:\Anti-Lust app\backend\functions"
npm install stripe
```

### Step 13: Set Stripe Secrets
Get your Stripe **Secret Key** from [Stripe Dashboard](https://dashboard.stripe.com/apikeys):

```powershell
firebase functions:config:set stripe.secret_key="sk_live_YOUR_KEY_HERE"
```

Set webhook secret (we'll get this in next step):
```powershell
firebase functions:config:set stripe.webhook_secret="TEMP_VALUE"
```

### Step 14: Deploy Function
```powershell
cd "e:\Anti-Lust app\backend"
firebase deploy --only functions
```

Wait for deployment... (2-3 minutes)

Copy the **Function URL** from output:
```
✔ functions[stripeWebhook(us-central1)]: 
  https://us-central1-YOUR-PROJECT.cloudfunctions.net/stripeWebhook
```

---

## Part 5: Configure Stripe Webhook (5 minutes)

### Step 15: Add Webhook Endpoint
1. Go to [Stripe Dashboard](https://dashboard.stripe.com/webhooks)
2. Click **"+ Add endpoint"**
3. Paste your function URL
4. Click **"Select events"**
5. Check these events:
   - ✅ `checkout.session.completed`
   - ✅ `customer.subscription.deleted`
6. Click **"Add events"**
7. Click **"Add endpoint"**

### Step 16: Get Webhook Secret
1. Click on your newly created webhook
2. Click **"Signing secret"** → **"Reveal"**
3. Copy the secret (starts with `whsec_`)

### Step 17: Update Firebase Config
```powershell
firebase functions:config:set stripe.webhook_secret="whsec_YOUR_SECRET_HERE"
```

### Step 18: Redeploy
```powershell
firebase deploy --only functions
```

---

## 🎉 Done! Test Your Setup

### Quick Test:
1. Visit your website
2. Click a pricing plan
3. Sign in with Google
4. Should redirect to Stripe checkout with email pre-filled!

---

## ✅ Checklist

- [ ] Firebase project created
- [ ] Config copied to auth.js
- [ ] Google Sign-In enabled
- [ ] Firestore database created
- [ ] Firebase CLI installed
- [ ] Functions initialized
- [ ] Webhook code added
- [ ] Stripe package installed
- [ ] Secrets configured
- [ ] Functions deployed
- [ ] Stripe webhook added
- [ ] Webhook secret updated
- [ ] Functions redeployed

---

## 🆘 Common Issues

**Error: "Firebase CLI not found"**
→ Restart PowerShell after installing

**Error: "Not authorized"**
→ Run `firebase login` again

**Error: "stripe is not defined"**
→ Run `npm install stripe` in functions folder

**Webhook not firing**
→ Check Stripe Dashboard → Webhooks → Logs

Let me know when you're ready to start! 🚀
