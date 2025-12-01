# API Keys Location Guide

## 🔐 Stripe API Keys

### **1. Frontend (Website) - PUBLIC KEY**

**File:** `e:\Anti-Lust app\website\scripts\stripe-payment.js`

**Line 7:**
```javascript
const STRIPE_PUBLISHABLE_KEY = 'pk_live_51SYnV2Ad7fQadcPJaPUgRQB9VibztUYclFwaqbHyh0tRvJ7CZtjqmKcjrFpHwITkVrir37405e8ojpl1iLiHeAJN00EdyoYywJ';
```

✅ **Already set to your public key**

---

### **2. Backend (Firebase Functions) - SECRET KEY**

**File:** `e:\Anti-Lust app\backend\functions\.env.anti-lust-guardian`

This file was auto-created during deployment. Add/update:

```env
STRIPE_SECRET_KEY=sk_live_YOUR_SECRET_KEY_HERE
STRIPE_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET_HERE
```

**How to update:**

1. Open: `e:\Anti-Lust app\backend\functions\.env.anti-lust-guardian`
2. Replace the values
3. Redeploy:
   ```powershell
   cd "e:\Anti-Lust app\backend"
   firebase deploy --only functions
   ```

---

### **3. Mobile App (Flutter) - If Using Stripe**

**File:** `e:\Anti-Lust app\anti_lust_guardian\lib\core\payment_gate.dart`

Search for any Stripe key references and update with your publishable key.

---

## 🤖 ChatGPT / OpenAI API Key

### **1. Backend Python Files**

**File:** `e:\Anti-Lust app\backend\.env`

Add this line:
```env
OPENAI_API_KEY=sk-proj-YOUR_OPENAI_KEY_HERE
```

**Usage in code:** Check these files:
- `e:\Anti-Lust app\backend\services\email_service.py` (line ~114)
- Any other ML/AI service files

**Example in Python:**
```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
```

---

### **2. If Using in Firebase Functions**

**File:** `e:\Anti-Lust app\backend\functions\.env.anti-lust-guardian`

Add:
```env
OPENAI_API_KEY=sk-proj-YOUR_OPENAI_KEY_HERE
```

**Usage in Node.js:**
```javascript
const { defineString } = require('firebase-functions/params');
const openaiKey = defineString('OPENAI_API_KEY');
```

---

## 📋 Complete Checklist

### Stripe Keys:
- [ ] **Public key** in `website/scripts/stripe-payment.js` (line 7)
- [ ] **Secret key** in `backend/functions/.env.anti-lust-guardian`
- [ ] **Webhook secret** in `backend/functions/.env.anti-lust-guardian`

### OpenAI Keys:
- [ ] **API key** in `backend/.env`
- [ ] **API key** in `backend/functions/.env.anti-lust-guardian` (if using in functions)

---

## 🔒 Security Best Practices

### ✅ DO:
- Store secret keys in `.env` files
- Add `.env` to `.gitignore`
- Use environment variables
- Never commit secrets to Git

### ❌ DON'T:
- Hardcode keys in code files
- Commit `.env` files
- Share secret keys publicly
- Use production keys in test code

---

## 🚀 After Updating Keys

### For Stripe:
```powershell
cd "e:\Anti-Lust app\backend"
firebase deploy --only functions
```

### For OpenAI (Backend):
Just restart your backend server - no redeployment needed.

---

## 📂 File Locations Summary

| Key Type | File Location | Status |
|----------|---------------|--------|
| Stripe Public | `website/scripts/stripe-payment.js` | ✅ Set |
| Stripe Secret | `backend/functions/.env.anti-lust-guardian` | ⚠️ Check |
| Webhook Secret | `backend/functions/.env.anti-lust-guardian` | ✅ Set |
| OpenAI | `backend/.env` | ❓ Need to add |
| FirebaseConfig | `website/scripts/auth.js` | ✅ Set |

---

## 🔍 How to Find Your Keys

### Stripe:
1. **Public key:** https://dashboard.stripe.com/apikeys (starts with `pk_live_`)
2. **Secret key:** Same page (starts with `sk_live_`)
3. **Webhook secret:** https://dashboard.stripe.com/webhooks → Click your webhook (starts with `whsec_`)

### OpenAI:
1. Go to: https://platform.openai.com/api-keys
2. Create new key or copy existing
3. Starts with: `sk-proj-` or `sk-`

---

## ⚠️ Important Notes

1. **Never share your secret keys** - they give full access to your accounts
2. **Use test keys during development** (`sk_test_`, `pk_test_`)
3. **Switch to live keys only when ready** (`sk_live_`, `pk_live_`)
4. **Set billing alerts** in both Stripe and OpenAI dashboards
