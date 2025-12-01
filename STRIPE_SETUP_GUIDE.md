# 💳 Stripe Payment Setup Guide

Complete guide to integrate Stripe payments into your Anti-Lust Guardian website.

---

## 📋 Quick Setup Checklist

- [ ] Create Stripe account
- [ ] Get API keys
- [ ] Create products & prices
- [ ] Add Publishable key to website
- [ ] Choose integration method
- [ ] Test with test cards
- [ ] Go live!

---

## Step 1: Create Stripe Account

1. Go to https://stripe.com
2. Click "Sign up" or "Start now"
3. Enter your email and create password
4. Complete account setup

---

## Step 2: Get Your API Keys

1. Log in to Stripe Dashboard: https://dashboard.stripe.com
2. Click **"Developers"** (top-right menu)
3. Click **"API keys"** (left sidebar)
4. You'll see two modes:

### 🧪 Test Mode (Start Here!)

```
Publishable key: pk_test_51ABC...
Secret key: sk_test_51XYZ...
```

**Use these for testing!**

### 🚀 Live Mode (After Testing)

```
Publishable key: pk_live_51ABC...
Secret key: sk_live_51XYZ...
```

**Switch to these when ready to accept real payments**

---

## Step 3: Create Products in Stripe

### Create Monthly Subscription

1. In Stripe Dashboard, click **"Products"** → **"Add product"**
2. Fill in:
   - **Name**: Anti-Lust Guardian - Monthly
   - **Description**: Full access to AI protection system
   - **Pricing model**: Recurring
   - **Price**: $17.00 USD
   - **Billing period**: Monthly
3. Click **"Add free trial"**
   - **Trial period**: 7 days
4. Click **"Save product"**
5. **Copy the Price ID** (looks like `price_1ABC...`) - You'll need this!

### Create Lifetime License

1. Click **"Add product"** again
2. Fill in:
   - **Name**: Anti-Lust Guardian - Lifetime
   - **Description**: Lifetime access to all features
   - **Pricing model**: One-time
   - **Price**: $299.00 USD
3. Click **"Save product"**
4. **Copy the Price ID** - You'll need this too!

---

## Step 4: Choose Your Integration Method

### 🎯 OPTION A: Payment Links (EASIEST - Recommended!)

**No coding required!** This is the fastest way to start accepting payments.

#### Create Payment Links:

1. Go to **"Payment links"** in Stripe Dashboard
2. Click **"New"**
3. For Monthly:
   - Select "Anti-Lust Guardian - Monthly" product
   - Click "Create link"
   - **Copy the link** (looks like `https://buy.stripe.com/test_abc123...`)
4. Repeat for Lifetime product

#### Add to Website:

Edit `e:\Anti-Lust app\website\scripts\stripe-payment.js`:

```javascript
const PAYMENT_LINKS = {
    monthly: 'https://buy.stripe.com/YOUR_MONTHLY_LINK_HERE',
    lifetime: 'https://buy.stripe.com/YOUR_LIFETIME_LINK_HERE'
};
```

#### Update Your HTML Buttons:

In `index.html`, find the pricing buttons and update them:

```html
<!-- Monthly Plan Button -->
<a href="javascript:quickCheckoutMonthly()" class="btn btn-primary">START TRIAL</a>

<!-- Lifetime Plan Button -->
<a href="javascript:quickCheckoutLifetime()" class="btn">GET LIFETIME</a>
```

---

### 🔧 OPTION B: Checkout Sessions (Advanced)

**Requires backend server.** More customizable but harder to set up.

This method needs a server to create checkout sessions. Skip this if you're using Payment Links!

---

## Step 5: Add Keys to Your Website

1. Open `e:\Anti-Lust app\website\scripts\stripe-payment.js`

2. Replace the placeholder with your **Publishable key**:

```javascript
// REPLACE THIS:
const STRIPE_PUBLISHABLE_KEY = 'pk_test_YOUR_KEY_HERE';

// WITH YOUR ACTUAL KEY:
const STRIPE_PUBLISHABLE_KEY = 'pk_test_51ABC123...';
```

3. Add your Price IDs (if using Checkout Sessions):

```javascript
const PRICING = {
    monthly: {
        priceId: 'price_1ABC123...', // Your monthly price ID
        // ...
    },
    lifetime: {
        priceId: 'price_1XYZ789...', // Your lifetime price ID
        // ...
    }
};
```

---

## Step 6: Include Script in HTML

Add this line to your `index.html` **before the closing `</body>` tag**:

```html
<script src="scripts/stripe-payment.js"></script>
</body>
</html>
```

---

## Step 7: Test Your Integration

### Use Test Cards:

**Successful Payment:**
```
Card Number: 4242 4242 4242 4242
Expiry: 12/34 (any future date)
CVC: 123 (any 3 digits)
ZIP: 12345 (any 5 digits)
```

**Declined Payment:**
```
Card Number: 4000 0000 0000 0002
```

**3D Secure Authentication:**
```
Card Number: 4000 0025 0000 3155
```

### Testing Steps:

1. Open your website
2. Click on "START TRIAL" or "GET LIFETIME"
3. You'll be redirected to Stripe Checkout
4. Use test card: `4242 4242 4242 4242`
5. Complete the test payment
6. Check Stripe Dashboard → Payments to see the test transaction

---

## Step 8: Go Live!

Once testing is successful:

1. In Stripe Dashboard, toggle from **"Test mode"** to **"Live mode"**
2. Get your **Live API keys** (`pk_live_...` and `sk_live_...`)
3. Update `stripe-payment.js` with your **Live Publishable key**
4. Create **Live Payment Links** (if using Payment Links method)
5. Re-deploy your website

⚠️ **NEVER expose your Secret key in frontend code!**

---

## 🎉 You're Done!

Your website can now accept payments!

### What Happens After Payment:

1. **Customer subscribes/pays** → Stripe processes payment
2. **Stripe sends webhook** → You receive notification
3. **Grant access** → Customer gets activation code/email
4. **Customer uses app** → Full access to Anti-Lust Guardian

---

## 💡 Quick Reference

### Where Everything Is:

- **API Keys**: Stripe Dashboard → Developers → API keys
- **Products**: Stripe Dashboard → Products
- **Payment Links**: Stripe Dashboard → Payment links
- **Payments**: Stripe Dashboard → Payments
- **Test Cards**: https://stripe.com/docs/testing

### Your Files:

- Payment script: `e:\Anti-Lust app\website\scripts\stripe-payment.js`
- Main page: `e:\Anti-Lust app\website\index.html`

---

## 🆘 Common Issues

**"Payment system is loading..."**
- Make sure you added the script tag to your HTML
- Check browser console for errors

**"Invalid API key"**
- Double-check you copied the entire key
- Make sure you're using the Publishable key (pk_test_... or pk_live_...)

**Payment link doesn't work**
- Verify the link is correct
- Test mode links only work in test mode

---

## 📞 Need Help?

- Stripe Docs: https://stripe.com/docs
- Stripe Support: https://support.stripe.com
- Test Cards: https://stripe.com/docs/testing

Good luck with your payments! 💰
