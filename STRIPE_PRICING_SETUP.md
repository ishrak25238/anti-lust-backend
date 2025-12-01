# 💳 Stripe Setup Guide - Your Pricing Plan

**Your Pricing:**
- 💚 Monthly: $4.99/month (7-day free trial)
- 💙 Yearly: $49.99/year (save 17%)
- 💎 Lifetime: $149.99 (one-time)

---

## 🚀 Step-by-Step: Create Your Products in Stripe

### STEP 1: Go to Stripe Dashboard
1. Open: https://dashboard.stripe.com/
2. **Make sure TEST MODE is ON** (toggle in top right)

---

### STEP 2: Create Monthly Subscription ($4.99 with Trial)

1. Click **"Products"** in left sidebar
2. Click **"+ Add product"** button

**Fill in the form:**

```
Product details
┌────────────────────────────────────────┐
│ Name                                   │
│ Anti-Lust Guardian - Monthly          │
│                                        │
│ Description (optional)                 │
│ Monthly subscription with 7-day trial │
└────────────────────────────────────────┘

Pricing
┌────────────────────────────────────────┐
│ Pricing model                          │
│ ● Standard pricing                     │ ← Select this
│                                        │
│ Price                                  │
│ $ 4.99                                │ ← Enter 4.99
│                                        │
│ Billing period                         │
│ ● Recurring                           │ ← Select this
│   [Monthly ▼]                         │ ← Select Monthly
│                                        │
│ Free trial                            │
│ ☑ Offer customers a free trial       │ ← CHECK THIS BOX!
│   Duration: [7] days                  │ ← Enter 7
└────────────────────────────────────────┘

[Save product]                           ← Click this
```

3. **After saving, COPY the Price ID**
   - It looks like: `price_1AbCdEfGhIjKlMnO`
   - **WRITE IT DOWN:** This is your `STRIPE_MONTHLY_PRICE_ID`

---

### STEP 3: Create Yearly Subscription ($49.99)

1. Click **"+ Add product"** again

**Fill in the form:**

```
Product details
┌────────────────────────────────────────┐
│ Name                                   │
│ Anti-Lust Guardian - Yearly           │
│                                        │
│ Description (optional)                 │
│ Annual subscription - Save 17%        │
└────────────────────────────────────────┘

Pricing
┌────────────────────────────────────────┐
│ Pricing model                          │
│ ● Standard pricing                     │
│                                        │
│ Price                                  │
│ $ 49.99                               │ ← Enter 49.99
│                                        │
│ Billing period                         │
│ ● Recurring                           │
│   [Yearly ▼]                          │ ← Select Yearly
│                                        │
│ Free trial                            │
│ ☐ Offer customers a free trial       │ ← Leave unchecked
└────────────────────────────────────────┘

[Save product]                           ← Click this
```

2. **COPY the Price ID** → This is your `STRIPE_YEARLY_PRICE_ID`

---

### STEP 4: Create Lifetime Access ($149.99)

1. Click **"+ Add product"** again

**Fill in the form:**

```
Product details
┌────────────────────────────────────────┐
│ Name                                   │
│ Anti-Lust Guardian - Lifetime         │
│                                        │
│ Description (optional)                 │
│ One-time payment for lifetime access  │
└────────────────────────────────────────┘

Pricing
┌────────────────────────────────────────┐
│ Pricing model                          │
│ ● Standard pricing                     │
│                                        │
│ Price                                  │
│ $ 149.99                              │ ← Enter 149.99
│                                        │
│ Billing period                         │
│ ● One time                            │ ← Select this!
└────────────────────────────────────────┘

[Save product]                           ← Click this
```

2. **COPY the Price ID** → This is your `STRIPE_LIFETIME_PRICE_ID`

---

## 📋 Summary - What You Should Have:

After creating all 3 products, you should have:

| Plan | Price | Type | Trial | Price ID |
|------|-------|------|-------|----------|
| Monthly | $4.99 | Recurring/Monthly | 7 days | `price_xxxxx` |
| Yearly | $49.99 | Recurring/Yearly | None | `price_xxxxx` |
| Lifetime | $149.99 | One-time | None | `price_xxxxx` |

---

## 🔑 Update Your .env File

Now open your `.env` file and update these lines:

```env
# Stripe Price IDs
STRIPE_MONTHLY_PRICE_ID=price_1AbCdEfGhIjKlMnO    ← Paste your monthly price ID
STRIPE_YEARLY_PRICE_ID=price_2PqRsTuVwXyZaBcD     ← Paste your yearly price ID
STRIPE_LIFETIME_PRICE_ID=price_3EfGhIjKlMnOpQrS   ← Paste your lifetime price ID

# App Configuration
TRIAL_DAYS=7                                       ← Already set correctly
REQUIRE_PAYMENT_METHOD_FOR_TRIAL=true             ← Keep this
```

**Save the file!**

---

## 🎯 Important Settings for Trial

### How the 7-Day Trial Works:

When a user subscribes to Monthly plan:
1. They enter their payment info
2. They get **7 days FREE** access
3. On day 8, Stripe automatically charges $4.99
4. Then $4.99 every month after that

### Should You Require Payment Method?

**YES (Recommended)** - `REQUIRE_PAYMENT_METHOD_FOR_TRIAL=true`

**Why?**
- ✅ Prevents abuse (people creating infinite trials)
- ✅ Higher conversion rate (they already entered card)
- ✅ Automatic billing after trial ends
- ⚠️ Some users may hesitate to enter card info

**Alternative:** Set to `false` if you want trial without card
- ⚠️ But then they'd need to come back and pay later
- ⚠️ Lower conversion rates

**I recommend keeping it `true`** ✅

---

## 🧪 Testing Your Prices

After setup, test with Stripe test cards:

**Test Card Number:** `4242 4242 4242 4242`
- Any future expiry date (e.g., 12/25)
- Any 3-digit CVC (e.g., 123)
- Any ZIP code

This simulates a successful payment without charging real money!

---

## ✅ Checklist

- [ ] Create Monthly product ($4.99, recurring, 7-day trial)
- [ ] Copy Monthly price ID
- [ ] Create Yearly product ($49.99, recurring, no trial)
- [ ] Copy Yearly price ID
- [ ] Create Lifetime product ($149.99, one-time, no trial)
- [ ] Copy Lifetime price ID
- [ ] Paste all 3 price IDs into `.env` file
- [ ] Save `.env` file

---

## 💡 Pro Tips

1. **Product Names:** You can edit them later if needed
2. **Descriptions:** Show in Stripe Checkout - make them appealing
3. **Test Mode:** Always test first before going live
4. **Trial Cancellation:** Users can cancel during trial without being charged

---

## 🎉 Value Proposition

Your pricing is smart:
- **Monthly $4.99** - Low barrier to entry, trial reduces risk
- **Yearly $49.99** - Saves $10 vs monthly ($59.88/year)
- **Lifetime $149.99** - 2.5 years worth, great for committed users

**Go ahead and create those products in Stripe now!** 🚀
