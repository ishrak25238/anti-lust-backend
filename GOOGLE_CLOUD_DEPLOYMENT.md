# Google Cloud Run Deployment Guide

## Prerequisites
1. **Google Cloud Account** (Free tier: 2GB RAM, 180,000 vCPU-seconds/month)
2. **Google Cloud SDK** installed

## Step 1: Install Google Cloud SDK

### Windows:
1. Download: https://cloud.google.com/sdk/docs/install
2. Run installer
3. After install, open new PowerShell and run: `gcloud init`

## Step 2: Set Up Google Cloud Project

```powershell
# Login to Google Cloud
gcloud auth login

# Create new project (or use existing)
gcloud projects create anti-lust-backend --name="Anti-Lust Backend"

# Set as active project
gcloud config set project anti-lust-backend

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

## Step 3: Deploy to Cloud Run

```powershell
# Navigate to your project directory
cd "E:\Anti-Lust app"

# Build and deploy in one command
gcloud run deploy anti-lust-backend \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars "DATABASE_URL=your_database_url,STRIPE_SECRET_KEY=your_stripe_key,OPENAI_API_KEY=your_openai_key"
```

## Step 4: Set Environment Variables

After deployment, set your environment variables:

```powershell
gcloud run services update anti-lust-backend \
  --region us-central1 \
  --set-env-vars "\
STRIPE_SECRET_KEY=your_stripe_key,\
STRIPE_PUBLISHABLE_KEY=your_publishable_key,\
OPENAI_API_KEY=your_openai_key,\
SENDGRID_API_KEY=your_sendgrid_key,\
JWT_SECRET_KEY=your_jwt_secret,\
TWILIO_ACCOUNT_SID=your_twilio_sid,\
TWILIO_AUTH_TOKEN=your_twilio_token"
```

## Step 5: Get Your Service URL

```powershell
gcloud run services describe anti-lust-backend --region us-central1 --format 'value(status.url)'
```

## Benefits of Google Cloud Run

✅ **2GB RAM** (vs Render's 512MB free tier)
✅ **Automatic scaling** (0 to 10 instances)
✅ **Pay only for requests** (not 24/7 like Render)
✅ **Perfect for ML models** (torch + transformers work flawlessly)
✅ **300s timeout** (vs 30s on many platforms)
✅ **Free tier**: First 180,000 vCPU-seconds/month FREE

## Costs (After Free Tier)

- **Very cheap**: ~$0.00002400 per vCPU-second
- **2GB RAM**: ~$0.00000250 per GiB-second
- **Typical cost**: $5-20/month for moderate traffic

## Monitoring

View logs:
```powershell
gcloud run services logs read anti-lust-backend --region us-central1
```

## Updating Your Deployment

```powershell
# Just run deploy again
gcloud run deploy anti-lust-backend --source . --region us-central1
```

## Troubleshooting

If build fails:
```powershell
# Check build logs
gcloud builds list --limit=5
gcloud builds log [BUILD_ID]
```

If service doesn't start:
```powershell
# Check service logs
gcloud run services logs read anti-lust-backend --region us-central1 --limit=50
```
