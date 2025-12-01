# 📝 STEP 1: Update Your .env Files

## ✅ What You Need to Do Right Now

### File 1: `anti_lust_guardian\.env`

**Open this file** in your editor and update these 3 lines:

```env
STRIPE_MONTHLY_PRICE_ID=price_1SZDMWAd7fQadcPJ2JJVS1lB
STRIPE_YEARLY_PRICE_ID=price_1SZDNgAd7fQadcPJIvPs9IPI
STRIPE_LIFETIME_PRICE_ID=price_1SZDRBAd7fQadcPJ1it9QjT0
```

**Location:** `e:\Anti-Lust app\anti_lust_guardian\.env`

---

### File 2: `backend\.env`

**Open this file** and add/update these lines:

```env
# Stripe Price IDs
STRIPE_MONTHLY_PRICE_ID=price_1SZDMWAd7fQadcPJ2JJVS1lB
STRIPE_YEARLY_PRICE_ID=price_1SZDNgAd7fQadcPJIvPs9IPI
STRIPE_LIFETIME_PRICE_ID=price_1SZDRBAd7fQadcPJ1it9QjT0
```

**Location:** `e:\Anti-Lust app\backend\.env`

---

## ✅ Checklist

- [ ] Open `anti_lust_guardian\.env` in VS Code
- [ ] Find the lines with `STRIPE_MONTHLY_PRICE_ID`, `STRIPE_YEARLY_PRICE_ID`, `STRIPE_LIFETIME_PRICE_ID`
- [ ] Replace the values with the ones above
- [ ] Save the file (Ctrl+S)
- [ ] Open `backend\.env` in VS Code
- [ ] Add or update the same 3 lines
- [ ] Save the file (Ctrl+S)

---

**Once you've done this, tell me "Done with step 1" and I'll move to the next step!**

This is simple and safe - we're just updating configuration, no code changes yet.
