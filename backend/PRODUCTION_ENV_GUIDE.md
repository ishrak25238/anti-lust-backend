# Production .env Configuration Guide

## 🔴 REMOVE FOR PRODUCTION

**Remove this line entirely:**
```
PARENT_ALERT_EMAIL="neoishrakaraf@gmail.com"
```

**Why?** In production, parent emails are stored in the database for each user. This environment variable was only for testing purposes.

## ✅ REQUIRED CHANGES

### 1. Email Configuration

**Option A: Use a dedicated Gmail account for the app**
```env
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USERNAME="anti-lust-guardian@gmail.com"  # Create a new dedicated account
SMTP_PASSWORD="your_app_password_here"
EMAIL_SENDER="Anti-Lust Guardian <noreply@anti-lust-guardian.com>"
ADMIN_EMAIL="admin@yourdomain.com"
```

**Option B: Use a professional email service (Recommended)**
For production, consider using:
- **SendGrid** (Free tier: 100 emails/day)
- **Amazon SES** (Very cheap, pay-as-you-go)
- **Mailgun** (Free tier: 5,000 emails/month)
- **Postmark** (Professional email delivery)

### 2. Database Configuration

For production, upgrade from SQLite to PostgreSQL:
```env
DATABASE_URL="postgresql+asyncpg://username:password@host:5432/guardian_db"
```

Or use a managed database service:
- **Supabase** (PostgreSQL - free tier available)
- **Render PostgreSQL** (free tier available)
- **Railway** (PostgreSQL)

### 3. API Keys Security

**IMPORTANT:** Your current `.env` contains real API keys that should be kept secret!

For production deployment:
1. Never commit `.env` to Git (it's already in `.gitignore`)
2. Use environment variables in your hosting platform
3. Rotate all keys if they were ever exposed publicly

## 📋 Production Deployment Checklist

- [ ] Remove `PARENT_ALERT_EMAIL` from `.env`
- [ ] Create dedicated email account for the app
- [ ] Update `EMAIL_SENDER` to professional address
- [ ] Upgrade to PostgreSQL database (from SQLite)
- [ ] Set all environment variables in hosting platform (Render, Railway, etc.)
- [ ] Verify `ALLOWED_ORIGINS` includes your production domain
- [ ] Test email sending with real Gmail SMTP
- [ ] Ensure all Stripe keys are LIVE mode (not test mode)
- [ ] Set secure `JWT_SECRET_KEY` and `API_SECRET_KEY`
- [ ] Configure `STRIPE_WEBHOOK_SECRET` from Stripe dashboard

## 🔒 Security Best Practices

1. **Never hardcode personal emails** - Always use database-stored emails
2. **Use environment variables** - Never commit secrets to Git
3. **Rotate keys periodically** - Especially API keys and JWT secrets
4. **Monitor email quota** - Gmail has sending limits (500/day for free accounts)
5. **Use separate accounts** - Don't use personal email for app services

## 📧 How Parent Emails Work in Production

```python
# Parent emails come from the database, NOT from .env
user = await db.get(User, child_id)
parent_email = user.parent_email  # Stored when parent links to child

# Notification is sent to database-stored parent email
await notifier.send_critical_alert(
    parent_email=user.parent_email,  # From database
    ...
)
```

The `PARENT_ALERT_EMAIL` in `.env` was only used in the test script. In actual production code, the system uses the `parent_email` field from the User table in the database.

## ✅ Final .env Structure for Production

```env
# Stripe (LIVE mode keys)
STRIPE_SECRET_KEY="sk_live_..."
STRIPE_PUBLISHABLE_KEY="pk_live_..."
STRIPE_MONTHLY_PRICE_ID="price_..."
STRIPE_YEARLY_PRICE_ID="price_..."
STRIPE_LIFETIME_PRICE_ID="price_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

# Email (Dedicated app account)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USERNAME="app-dedicated@gmail.com"
SMTP_PASSWORD="app_password"
EMAIL_SENDER="Anti-Lust Guardian <noreply@yourdomain.com>"
ADMIN_EMAIL="admin@yourdomain.com"

# Database (PostgreSQL recommended)
DATABASE_URL="postgresql+asyncpg://user:pass@host/db"

# Security
API_SECRET_KEY="generate_new_random_key_256_bit"
JWT_SECRET_KEY="generate_new_random_key_256_bit"
JWT_ALGORITHM="HS256"
JWT_EXPIRATION_HOURS="24"

# AI/ML
OPENAI_API_KEY="sk-proj-..."
ML_API_KEYS="alg-app-mobile-2024-...,alg-app-web-2024-..."

# Server
ALLOWED_ORIGINS="https://your-production-domain.com"
RATE_LIMIT_PER_MINUTE="100"
MAX_IMAGE_SIZE_MB="10"
MAX_TEXT_LENGTH="10000"
```

**Note:** No `PARENT_ALERT_EMAIL` in production! 🎯
