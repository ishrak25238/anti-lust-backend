# Firebase Setup - SIMPLE VERSION (Parts 2-5)

## ✅ Part 1: DONE! 
You already added your Firebase config to auth.js.

---

## 📝 Part 2: Turn On Google Login (2 clicks)

### What to do:
1. Open Firebase Console: https://console.firebase.google.com
2. Click your project: **"anti-lust-guardian"**
3. Left sidebar → Click **"Authentication"**
4. Click **"Get started"** button
5. Click the **"Sign-in method"** tab (at top)
6. You'll see a list → Find **"Google"**
7. Click on **"Google"** row
8. Toggle switch to **ON** (blue)
9. Choose support email: **your email**
10. Click **"Save"**

**Done!** Google Sign-In is now enabled.

---

## 💾 Part 3: Create Database (3 clicks)

### What to do:
1. Still in Firebase Console
2. Left sidebar → Click **"Firestore Database"**
3. Click **"Create database"** button
4. Choose **"Start in test mode"** (radio button)
5. Click **"Next"**
6. Location: **"nam5 (us-central)"** (or your nearest)
7. Click **"Enable"**

Wait 30 seconds... database is creating...

8. When it loads, click **"+ Start collection"**
9. Collection ID: Type `users`
10. Click **"Next"**
11. Document ID: Leave as **"Auto-ID"**
12. Click **"Save"** (don't add fields, just save empty)

**Done!** Database is ready.

---

## 🚀 Part 4: Deploy Webhook (Copy/Paste Commands)

**What this does:** Creates a server that Stripe talks to after payment.

### Step 1: Install Firebase Tools
Open PowerShell and run:
```powershell
npm install -g firebase-tools
```
Wait for it to finish... (1-2 minutes)

### Step 2: Login
```powershell
firebase login
```
- Browser opens
- Click **"Allow"**
- Close browser

### Step 3: Go to Backend Folder
```powershell
cd "e:\Anti-Lust app\backend"
```

### Step 4: Initialize
```powershell
firebase init functions
```

**Answer these questions:**
- **Project:** Use arrow keys → select **"anti-lust-guardian"** → Press Enter
- **Language:** JavaScript
- **ESLint:** n (No)
- **Install dependencies:** Y (Yes)

Wait for installation... (2-3 minutes)

### Step 5: Edit Webhook File
1. Open this file: `e:\Anti-Lust app\backend\functions\index.js`
2. **Delete everything** in that file
3. **Copy this entire code** and paste it:

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

4. **Save** the file (Ctrl+S)

### Step 6: Install Stripe
Back to PowerShell:
```powershell
cd "e:\Anti-Lust app\backend\functions"
npm install stripe
```

### Step 7: Configure Stripe Key
Go to Stripe Dashboard: https://dashboard.stripe.com/apikeys
- Copy your **"Secret key"** (starts with `sk_live_` or `sk_test_`)

Back to PowerShell:
```powershell
firebase functions:config:set stripe.secret_key="PASTE_YOUR_KEY_HERE"
```
(Replace PASTE_YOUR_KEY_HERE with actual key)

For now, set webhook secret to temp:
```powershell
firebase functions:config:set stripe.webhook_secret="temp123"
```

### Step 8: Deploy
```powershell
cd ..
firebase deploy --only functions
```

Wait 2-3 minutes...

**When done**, you'll see:
```
✔ functions[stripeWebhook]: https://us-central1-anti-lust-guardian.cloudfunctions.net/stripeWebhook
```

**📋 COPY THAT URL!** You need it for Part 5.

---

## 🔗 Part 5: Connect Stripe to Firebase

### Step 1: Add Webhook
1. Go to Stripe: https://dashboard.stripe.com/webhooks
2. Click **"+ Add endpoint"** button
3. **Endpoint URL:** Paste the URL you copied from Part 4
4. Click **"+ Select events"**
5. Search for: `checkout.session.completed`
6. Check the box ✅
7. Search for: `customer.subscription.deleted`
8. Check the box ✅
9. Click **"Add events"**
10. Click **"Add endpoint"**

### Step 2: Get Webhook Secret
1. You'll see your new webhook listed
2. Click on it
3. Find **"Signing secret"** section
4. Click **"Reveal"**
5. Copy the secret (starts with `whsec_`)

### Step 3: Update Firebase Config
Back to PowerShell:
```powershell
firebase functions:config:set stripe.webhook_secret="PASTE_WHSEC_HERE"
```
(Replace with your actual whsec_ value)

### Step 4: Redeploy
```powershell
firebase deploy --only functions
```

Wait 1-2 minutes...

---

## 🎉 ALL DONE!

**Test it:**
1. Go to your website
2. Click pricing
3. Sign in with Google
4. You should see Stripe checkout with email filled!

---

## Need Help?

**Stuck on PowerShell commands?**
→ Just copy/paste exactly as shown

**Don't see "functions" folder?**
→ Part 4, Step 4 creates it

**Stripe key not working?**
→ Make sure you copied the SECRET key, not publishable

Let me know which part you're on! 🚀
