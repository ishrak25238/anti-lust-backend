# 🚀 Final Deployment Instructions

## 1. Backend Deployment (Google Cloud Run)

**Prerequisite:** You need the Google Cloud CLI.
1. Download & Install: https://cloud.google.com/sdk/docs/install
2. Open a new terminal (PowerShell)
3. Login:
   ```powershell
   gcloud auth login
   ```

**Deploy Command:**
Run this exact command in the `e:\Anti-Lust app` folder:

```powershell
gcloud run deploy anti-lust-backend `
  --source . `
  --region us-central1 `
  --memory 2Gi `
  --cpu 1 `
  --allow-unauthenticated `
  --set-env-vars "STRIPE_SECRET_KEY=sk_live_YOUR_KEY,SENDGRID_API_KEY=SG.YOUR_KEY,JWT_SECRET_KEY=YOUR_SECRET"
```

*Replace `YOUR_KEY` with your actual keys from `backend/.env`.*

## 2. Mobile App Build (Android)

1. Open terminal in `e:\Anti-Lust app\anti_lust_guardian`
2. Run:
   ```powershell
   flutter build apk --release
   ```
3. **Get the APK:**
   - Location: `build\app\outputs\flutter-apk\app-release.apk`
   - Send this file to your phone to install!

## 3. Website Deployment (Optional)

You can host the `website` folder for free on Netlify or Vercel.
1. Drag and drop the `website` folder to https://app.netlify.com/drop

## ✅ Verification

After deployment:
1. **Backend:** Visit the URL provided by Google Cloud (e.g., `https://anti-lust-backend-xyz.run.app/docs`)
   - You should see the API documentation.
2. **Mobile App:** Open the app.
   - It should connect to the backend (update the URL in the app if needed).

**Congratulations! Your Anti-Lust Guardian is live.**
