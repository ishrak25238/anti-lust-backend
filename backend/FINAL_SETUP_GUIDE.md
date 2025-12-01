# 🚀 Anti-Lust Guardian - Production Setup Guide

This guide details exactly how to set up the **production-ready** backend with zero mocks and full ML capabilities.

## 1. Prerequisites

You must have the following installed:
- **Python 3.10+** (Required for PyTorch/TensorFlow)
- **PostgreSQL** (Recommended) or SQLite (Default)
- **Redis** (Optional, for caching if scaling)

## 2. Install Dependencies

The backend now uses **REAL** Machine Learning models (PyTorch, Transformers, CLIP). You must install the heavy dependencies.

```bash
cd backend
pip install -r requirements.txt
```

**Note:** This will install ~2GB of ML libraries. Ensure you have a good internet connection.

## 3. Environment Configuration

Create a `.env` file in the `backend/` directory with your **REAL** keys.

```ini
# --- Security ---
SECRET_KEY=your_super_secret_jwt_key_here_make_it_long
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# --- Database ---
# Default is SQLite (easiest):
DATABASE_URL=sqlite+aiosqlite:///./guardian.db
# For Production PostgreSQL:
# DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname

# --- Stripe Payments (REQUIRED) ---
STRIPE_SECRET_KEY=sk_test_...  # Get this from Stripe Dashboard
STRIPE_WEBHOOK_SECRET=whsec_...

# --- Email Service (REQUIRED) ---
# Option 1: SendGrid (Recommended)
SENDGRID_API_KEY=SG.your_key_here
ADMIN_EMAIL=your_email@example.com

# Option 2: SMTP (Gmail/Outlook)
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=your_email@gmail.com
# SMTP_PASSWORD=your_app_password

# --- OpenAI (Optional but Recommended) ---
# Used for "Hardcore" forensic analysis reports
OPENAI_API_KEY=sk-...
```

## 4. Stripe Setup (Critical)

You must configure Stripe for the pricing logic to work:

1.  Go to **Stripe Dashboard > Products**.
2.  Create **Product 1**: "Anti-Lust Guardian Monthly"
    *   Price: **$17.00** / month
    *   **IMPORTANT:** Add a **7-day free trial** to this price in Stripe (or the backend handles it via code, but it's good practice).
    *   Copy the Price ID (e.g., `price_123...`).
3.  Create **Product 2**: "Anti-Lust Guardian Lifetime"
    *   Price: **$299.00** (One-time)
    *   Copy the Price ID.
4.  **Update Code:**
    *   In `backend/services/payment_service.py`, you can optionally hardcode these IDs if you want strict mapping, but the current code handles dynamic IDs passed from the frontend.

## 5. Running the Server

Start the server. It will take 10-20 seconds to load the ML models (CLIP, BERT, ResNet) into memory.

```bash
uvicorn main:app --reload
```

**Verify it works:**
- Go to `http://localhost:8000/health`
- You should see `"ml": true` and `"stripe": true`.

## 6. Flutter App Connection

Ensure your Flutter app is pointing to this backend.
In `lib/core/api_config.dart` (or equivalent):

```dart
static const String baseUrl = 'http://YOUR_PC_IP:8000';
```

**Do not use `localhost`** on Android Emulator (use `10.0.2.2`) or Physical Device (use PC's IP).

---

## 🛡️ What's "Under the Hood"?

- **No Mocks:** Every service (Payment, Email, ML) executes real logic.
- **ML Engine:** Uses OpenAI's CLIP model for image analysis and BERT for text classification.
- **Forensics:** Generates PDF reports using `reportlab` and emails them via SendGrid/SMTP.
- **Database:** Stores all threat logs and behavioral profiles in SQLite/Postgres.

**You are now running a professional-grade protection system.**
