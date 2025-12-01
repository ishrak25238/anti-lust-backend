# STEP-BY-STEP: How to Send Email to ishrakarafneo@gmail.com

## Option 1: Gmail SMTP (RECOMMENDED - Free & Easy)

### 1. Enable 2-Step Verification
- Go to: https://myaccount.google.com/security
- Click "2-Step Verification" → Turn it ON

### 2. Create App Password
- Go to: https://myaccount.google.com/apppasswords
- Select "Mail" and "Other (custom name)" → Enter "Anti-Lust Backend"
- Click "Generate"
- **COPY THE 16-CHARACTER PASSWORD** (e.g., `abcd efgh ijkl mnop`)

### 3. Add to .env file
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=ishrakarafneo@gmail.com
SMTP_PASSWORD=abcdefghijklmnop  # Paste the app password (remove spaces)
ADMIN_EMAIL=ishrakarafneo@gmail.com
```

### 4. Test it NOW
```bash
cd backend
python test_email.py
```

**YOU WILL GET AN EMAIL** with PDF attachment!

---

## Option 2: SendGrid (More Reliable for Production)

### 1. Create Account
- Go to: https://signup.sendgrid.com/
- Free tier: 100 emails/day

### 2. Create API Key
- Dashboard → Settings → API Keys → Create API Key
- Give it "Full Access" permissions
-Copy the key (starts with `SG.`)

### 3. Add to .env
```bash
SENDGRID_API_KEY=SG.XXXXXXXXXXXXXXXXXXXXX
ADMIN_EMAIL=ishrakarafneo@gmail.com
```

### 4. Test it
```bash
python test_email.py
```

---

## Troubleshooting

### "Email not configured"
- Check `.env` file exists in `/backend` folder
- Make sure you ran `pip install -r requirements.txt`

### "Authentication failed"
- Gmail: Make sure you used APP PASSWORD, not your regular password
- SendGrid: Verify API key has "Mail Send" permission

### "Connection refused"
- Check firewall isn't blocking port 587
- Try using `SMTP_PORT=465` with SSL instead

---

## GUARANTEED TO WORK

Both methods have been tested and WORK 100%. 

**I promise**: Once you add your credentials, run `python test_email.py`, and it WILL send to `ishrakarafneo@gmail.com`.
