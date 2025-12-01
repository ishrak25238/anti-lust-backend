# 🔑 Supabase Keys - What to Copy Where

## Where to Find Your Keys in Supabase Dashboard

When you're on the Supabase Settings → API page, you'll see this layout:

---

## 📍 SECTION 1: Project URL (At the Top)

```
┌─────────────────────────────────────────────┐
│  Configuration                               │
│                                              │
│  Project URL                                 │
│  https://xxxxxxxxxxxxx.supabase.co          │
│  [Copy button]                               │
└─────────────────────────────────────────────┘
```

**THIS IS YOUR `SUPABASE_URL`** ⬅️ Copy this entire URL

---

## 📍 SECTION 2: Project API Keys (Below the URL)

```
┌─────────────────────────────────────────────┐
│  Project API keys                            │
│                                              │
│  anon public                                 │
│  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...   │
│  [Copy button]                               │
│                                              │
│  service_role secret                         │
│  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...   │
│  [Copy button]                               │
└─────────────────────────────────────────────┘
```

**USE THIS ONE:** `anon public` ⬅️ This is your `SUPABASE_ANON_KEY`  
**IGNORE THIS:** `service_role` ❌ Don't use this one (it's for backend only)

---

## ✅ What You Need to Copy

| Supabase Label | Your .env Variable | Example |
|----------------|-------------------|---------|
| **Project URL** | `SUPABASE_URL` | `https://abcdefgh.supabase.co` |
| **anon public** | `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2MzI...` |

---

## 🚫 What to IGNORE

- ❌ **service_role** - This is for admin/backend, NOT for your mobile app
- ❌ Don't use any "secret" keys in your Flutter app

---

## 📝 Where You're Confused

You mentioned seeing:
- ✅ **anon public** - YES, use this!
- ❌ **publishable** - This is from STRIPE, not Supabase
- ❌ **secret api** - This is from STRIPE, not Supabase
- ❌ **service role** - Ignore this (Supabase admin key)

You're probably looking at multiple tabs/dashboards at once!

---

## 🎯 Step-by-Step Instructions

### Step 1: Make Sure You're in Supabase
- URL should be: `app.supabase.com/project/...`
- Top left should say "Supabase"

### Step 2: Click Settings (Gear Icon)
- In the left sidebar
- Should be near the bottom

### Step 3: Click "API"
- Under Settings menu
- Second option usually

### Step 4: Scroll to Top
- You'll see "Project URL" first
- Copy the whole URL starting with `https://`

### Step 5: Scroll Down Slightly
- Look for "Project API keys" section
- Find the one labeled "anon public"
- Click the copy button
- It's a LONG string starting with `eyJ`

---

## 🖼️ Visual Reference

**Top of the page:**
```
Project URL
┌────────────────────────────────────────┐
│ https://xxxxx.supabase.co              │ ← COPY THIS (SUPABASE_URL)
└────────────────────────────────────────┘
```

**Middle of the page:**
```
Project API keys

anon
public
┌────────────────────────────────────────┐
│ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC... │ ← COPY THIS (SUPABASE_ANON_KEY)
└────────────────────────────────────────┘

service_role    ⚠️ DO NOT USE THIS ONE
secret
┌────────────────────────────────────────┐
│ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC... │ ← IGNORE THIS
└────────────────────────────────────────┘
```

---

## ✅ Final Result in Your .env

After copying, your `.env` file should look like:

```env
SUPABASE_URL=https://abcdefgh.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2MzIxNDcwNjAsImV4cCI6MTk0NzcyMzA2MH0.abcdefghijklmnopqrstuvwxyz
```

Both should be REAL values, not the words "YOUR_SUPABASE_URL"!

---

## 🆘 Still Can't Find It?

Take a screenshot of your Supabase Settings → API page and I can point out exactly where to look!

Or just tell me: "I'm on the API settings page but I don't see Project URL"
