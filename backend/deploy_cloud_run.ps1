#!/usr/bin/env pwsh
# Cloud Run Deployment Script for Anti-Lust Backend
# Run this from the backend directory

# Configuration
$PROJECT_ID = "anti-lust-guardian"
$SERVICE_NAME = "anti-lust-backend"
$REGION = "us-central1"

Write-Host "Deploying Anti-Lust Backend to Cloud Run..." -ForegroundColor Cyan
Write-Host ""

# Check if gcloud is installed
if (!(Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "Error: gcloud CLI not found. Please install Google Cloud SDK first." -ForegroundColor Red
    Write-Host "   Download from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Set project
Write-Host "Setting GCP project to: $PROJECT_ID" -ForegroundColor Yellow
gcloud config set project $PROJECT_ID

# Deploy to Cloud Run
Write-Host "Building and deploying to Cloud Run..." -ForegroundColor Yellow
Write-Host ""

gcloud run deploy $SERVICE_NAME `
    --source . `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --timeout 300 `
    --memory 2Gi `
    --cpu 2 `
    --min-instances 0 `
    --max-instances 10 `
    --port 8080

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Deployment successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "   1. Go to Cloud Run console: https://console.cloud.google.com/run" -ForegroundColor White
    Write-Host "   2. Select '$SERVICE_NAME' service" -ForegroundColor White
    Write-Host "   3. Click 'EDIT & DEPLOY NEW REVISION'" -ForegroundColor White
    Write-Host "   4. Add environment variables from .env.example" -ForegroundColor White
    Write-Host "   5. Deploy the new revision" -ForegroundColor White
    Write-Host ""
    Write-Host "IMPORTANT: Set these required environment variables:" -ForegroundColor Yellow
    Write-Host "   - STRIPE_SECRET_KEY" -ForegroundColor White
    Write-Host "   - API_SECRET_KEY" -ForegroundColor White
    Write-Host "   - JWT_SECRET_KEY" -ForegroundColor White
    Write-Host "   - SMTP_USERNAME and SMTP_PASSWORD" -ForegroundColor White
    Write-Host "   - ML_API_KEYS" -ForegroundColor White
    Write-Host "   - ALLOWED_ORIGINS" -ForegroundColor White
    Write-Host ""
}
else {
    Write-Host ""
    Write-Host "Deployment failed. Check the error messages above." -ForegroundColor Red
    Write-Host "   Reviewing deployment logs..." -ForegroundColor Yellow
    gcloud run services describe $SERVICE_NAME --region $REGION
    exit 1
}
