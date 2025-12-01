# 🚀 DEPLOYMENT INSTRUCTIONS

## What I Need From You

Now that the security hardening and ML enhancements are complete, here's what you need to do to make it operational:

---

## 1. Generate Security Keys

Run these commands and save the output:

```bash
# Generate API Secret Key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT Secret Key  
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ML API Key 1
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ML API Key 2
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ML API Key 3
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 2. Create `.env` File

Create `backend/.env` with the generated keys:

```bash
# Stripe Keys (from your Stripe dashboard)
STRIPE_SECRET_KEY=sk_test_YOUR_ACTUAL_STRIPE_KEY
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_ACTUAL_STRIPE_KEY

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-actual-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
ADMIN_EMAIL=your-actual-email@gmail.com

# Database
DATABASE_URL=sqlite+aiosqlite:///./guardian.db

# Security - PASTE GENERATED KEYS HERE
API_SECRET_KEY=<paste-key-1-here>
JWT_SECRET_KEY=<paste-key-2-here>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# ML API Keys - PASTE KEYS HERE (comma-separated, no spaces)
ML_API_KEYS=<paste-key-3-here>,<paste-key-4-here>,<paste-key-5-here>

# CORS Configuration (your Flutter app URLs)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100

# Request Size Limits
MAX_IMAGE_SIZE_MB=10
MAX_TEXT_LENGTH=10000

# Monitoring (Optional - leave empty for now)
SENTRY_DSN=
PROMETHEUS_PORT=9090
```

---

## 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 4. Initialize Database

```bash
python migrations/add_security_tables.py
```

You should see:
```
✅ All security and pattern analysis tables created successfully!

Created tables:
  - api_keys (API key management)
  - user_sessions (JWT session tracking)
  - audit_logs (Security event logging)
  - pattern_events (ML pattern storage)
  ... (and 4 more)
```

---

## 5. Start the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`

---

## 6. Test Security

Open a new terminal and run:

```bash
# Test 1: Health check (no auth needed)
curl http://localhost:8000/health

# Test 2: Try ML endpoint without API key (should fail with 401)
curl -X POST http://localhost:8000/api/ml/nsfw-check \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "test"}'

# Should return: {"detail":"API key required. Include X-API-Key header."}

# Test 3: Check security headers
curl -I http://localhost:8000/health

# Should see headers like:
# x-content-type-options: nosniff
# x-frame-options: DENY
# strict-transport-security: max-age=31536000
```

---

## 7. Update Flutter App

In your Flutter app, add the API key to ML requests:

### Where to Add

Look for these files in your Flutter app:
- `anti_lust_guardian/lib/core/ai_threat_prediction.dart`
- Any file making HTTP requests to `api/ml/` endpoints

### What to Change

**Before**:
```dart
final response = await http.post(
  Uri.parse('http://localhost:8000/api/ml/nsfw-check'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({'image_base64': imageBase64}),
);
```

**After**:
```dart
final response = await http.post(
  Uri.parse('http://localhost:8000/api/ml/nsfw-check'),
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'YOUR_ML_API_KEY_HERE',  // Add this line
  },
  body: jsonEncode({'image_base64': imageBase64}),
);
```

**Important**: Use one of the ML API keys from your `.env` file (one of the 3 you generated)

---

## 8. Git Security

Make sure `.env` is NOT committed:

```bash
# Check if .env is ignored
git status

# If you see .env listed, it's NOT ignored yet
# Add it to .gitignore:
echo ".env" >> backend/.gitignore
echo ".env.openai" >> backend/.gitignore

# Remove from git if already committed
git rm --cached backend/.env
git rm --cached backend/.env.openai

# Commit
git add backend/.gitignore
git commit -m "Secure: Add .env files to gitignore"
```

---

## ✅ Verification Checklist

Before marking as complete, verify:

- [ ] `.env` file created with all generated keys
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database initialized (ran migration script)
- [ ] Server starts without errors
- [ ] Health endpoint works (`curl http://localhost:8000/health`)
- [ ] ML endpoint rejects requests without API key
- [ ] Security headers present (`curl -I http://localhost:8000/health`)
- [ ] `.env` is in `.gitignore`
- [ ] `.env` is NOT in git (`git status` doesn't show it)

---

## 🚨 Common Issues

### "ModuleNotFoundError: No module named 'slowapi'"
**Solution**: Run `pip install -r requirements.txt`

### "No such file or directory: '.env'"
**Solution**: Create the `.env` file as shown in step 2

### "Table pattern_events already exists"
**Solution**: Database already initialized, you're good to go!

### "Invalid API key"
**Solution**: Check that:
1. You set `ML_API_KEYS` in `.env`
2. You're using the correct key in your Flutter app
3. There are no extra spaces in the `.env` file

---

## 📞 When You're Done

After completing all steps, tell me:

1. ✅ ".env file created with generated keys"
2. ✅ "Server started successfully"
3. ✅ "Security tests passed"

Then I'll guide you on integrating with your Flutter app and deploying to production.

---

## 🔐 Security Reminder

**NEVER commit these files to git:**
- `.env` (contains all secrets)
- `.env.openai` (contains OpenAI API key)
- `guardian.db` (contains user data)

They should all be in `.gitignore` (which I already created for you).
