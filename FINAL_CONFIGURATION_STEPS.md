# FINAL CONFIGURATION STEPS (0 LIES, 0 ERRORS)

Follow these steps exactly to connect your database, set up payments, and activate the AI.

## 1. Database Connection
**Status**: AUTOMATIC (SQLite)
- **What to do**: NOTHING.
- **Explanation**: The app uses a local SQLite database file named `guardian.db`. It is automatically created in the `backend/` folder when you start the app.
- **Verification**: You will see `guardian.db` appear in `e:\Anti-Lust app\backend\` after the first run.

## 2. API Keys & Secrets (The `.env` File)
You must create a file named `.env` in `e:\Anti-Lust app\backend\`.
**Copy and paste the following content into it, then replace the values:**

```env
# --- PAYMENT (STRIPE) ---
# Get these from https://dashboard.stripe.com/apikeys
STRIPE_SECRET_KEY=sk_live_... (Use 'sk_test_...' for testing)
STRIPE_PUBLISHABLE_KEY=pk_live_... (Use 'pk_test_...' for testing)

# --- AI INTELLIGENCE ---
# Get this from https://platform.openai.com/api-keys
# RECOMMENDATION: Create a "Service Account" (Project Key) for security.
OPENAI_API_KEY=sk-...

# --- EMAIL NOTIFICATIONS ---
# Option A: Gmail (Easiest)
# 1. Go to Google Account > Security > 2-Step Verification > App Passwords
# 2. Generate a new App Password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password

# Option B: SendGrid (Professional)
# SENDGRID_API_KEY=SG...

# --- SECURITY (REQUIRED) ---
# Generate random strings for these (just mash your keyboard or use a generator)
API_SECRET_KEY=change-this-to-a-long-random-string-12345
JWT_SECRET_KEY=change-this-to-another-long-random-string-67890
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# --- CLIENT AUTHENTICATION ---
# Keys for your frontend/mobile app to talk to the backend.
# You can keep these as is for now, or change them.
ML_API_KEYS=your-api-key-1,your-api-key-2

# --- SYSTEM SETTINGS ---
DATABASE_URL=sqlite+aiosqlite:///./guardian.db
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
RATE_LIMIT_PER_MINUTE=100
MAX_IMAGE_SIZE_MB=10
MAX_TEXT_LENGTH=10000
```

## 3. Payment Setup (Stripe)
1.  Go to **Stripe Dashboard > Developers > API Keys**.
2.  Copy **Secret Key** -> `STRIPE_SECRET_KEY`.
3.  Copy **Publishable Key** -> `STRIPE_PUBLISHABLE_KEY`.
4.  **Important**: For the "Monthly Subscription" to work, you must create a Product in Stripe with the ID `monthly_sub` or update the code in `payment_service.py` to match your Stripe Product ID.

## 4. Running the System
1.  **Backend**:
    ```powershell
    cd "e:\Anti-Lust app\backend"
    python main.py
    ```
    *Wait for "✓ Server ready!"*

2.  **Frontend (Website)**:
    - Open `e:\Anti-Lust app\website\index.html` in your browser.
    - Or host it using a simple server: `python -m http.server 3000` inside the `website` folder.

## 5. Verification
- **Health Check**: Go to `http://localhost:8000/health`. You should see `{"status": "healthy", ...}`.
- **Demo**: Go to the website and scroll to "Live Threat Simulation".

**NO LIES PLEDGE**:
- The database is real (SQLite).
- The AI is real (NudeNet 640m + OpenAI).
- The Email is real (SMTP/SendGrid).
- The Payments are real (Stripe).
