# GitHub Auto-Deploy Setup

## Push to GitHub = Automatic Builds

### Step 1: Push Your Code

```bash
cd "e:\Anti-Lust app"
git init
git add .
git commit -m "Production ready"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/anti-lust-guardian.git
git push -u origin main
```

### Step 2: Create a Release Tag

```bash
git tag v1.0.0
git push origin v1.0.0
```

**DONE!** GitHub Actions automatically builds:
- Android APK
- Android AAB (Play Store)
- Windows EXE
- Linux binary
- macOS app

### Download Links

After 15-20 minutes, go to:
`https://github.com/YOUR_USERNAME/anti-lust-guardian/releases`

You'll see downloadable files for ALL platforms.

## Manual Build (If Needed)

```bash
cd "e:\Anti-Lust app\anti_lust_guardian"

flutter build apk
flutter build windows
flutter build linux
flutter build macos
```

## Website Deploy (2 Minutes)

```bash
cd "e:\Anti-Lust app\website"
netlify deploy --prod
```

Or push to GitHub and enable GitHub Pages.

## Backend Deploy

### Docker:
```bash
cd "e:\Anti-Lust app\backend"
docker build -t anti-lust-api .
docker run -p 8000:8000 anti-lust-api
```

### Heroku:
```bash
heroku create anti-lust-api
git subtree push --prefix backend heroku main
```

## Stripe Payment

1. Get keys: stripe.com/dashboard
2. Update `.env` files with your keys
3. Done - payment works

## That's It

Push code → Get downloads automatically.

No build servers needed. No manual compilation.

GitHub Actions does everything.
