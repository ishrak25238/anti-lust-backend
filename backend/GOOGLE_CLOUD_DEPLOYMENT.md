# Google Cloud Platform Deployment Guide
## Anti-Lust Guardian Backend

### Table of Contents
1. [Prerequisites](#prerequisites)
2. [Option 1: Cloud Run (Recommended - Easiest)](#option-1-cloud-run-recommended)
3. [Option 2: App Engine](#option-2-app-engine)
4. [Option 3: Compute Engine VM](#option-3-compute-engine)
5. [Database Setup (Cloud SQL)](#database-setup)
6. [Environment Variables](#environment-variables)
7. [Cost Estimates](#cost-estimates)

---

## Prerequisites

### 1. Create Google Cloud Account
1. Go to https://console.cloud.google.com
2. Sign up with your Gmail account
3. **Free tier**: $300 credit for 90 days + Always Free tier

### 2. Install Google Cloud CLI
Download from: https://cloud.google.com/sdk/docs/install

**Windows:**
```powershell
# Download and run installer
# After installation, run:
gcloud init
```

### 3. Create a New Project
```powershell
# Create project
gcloud projects create anti-lust-guardian --name="Anti-Lust Guardian"

# Set as active project
gcloud config set project anti-lust-guardian

# Enable billing (required)
# Go to: https://console.cloud.google.com/billing
```

### 4. Enable Required APIs
```powershell
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Cloud SQL API
gcloud services enable sql-component.googleapis.com
gcloud services enable sqladmin.googleapis.com

# Enable Container Registry
gcloud services enable containerregistry.googleapis.com

# Enable Secret Manager
gcloud services enable secretmanager.googleapis.com
```

---

## Option 1: Cloud Run (Recommended - Easiest)

**Why Cloud Run?**
- ✅ Automatic scaling (0 to millions)
- ✅ Pay only for what you use
- ✅ Easy deployment
- ✅ Free tier: 2 million requests/month
- ✅ Perfect for FastAPI

### Step 1: Create Dockerfile

Create `Dockerfile` in your backend directory:

```dockerfile
# Use official Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy ML models
COPY data/models /app/data/models

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Step 2: Create .dockerignore

Create `.dockerignore` file:

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.git
.gitignore
*.db
*.log
.vscode/
.idea/
*.md
tests/
```

### Step 3: Build and Deploy

```powershell
# Set your project ID
$PROJECT_ID = "anti-lust-guardian"

# Build the container
gcloud builds submit --tag gcr.io/$PROJECT_ID/backend

# Deploy to Cloud Run
gcloud run deploy anti-lust-backend `
  --image gcr.io/$PROJECT_ID/backend `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 2Gi `
  --cpu 2 `
  --timeout 300 `
  --max-instances 10 `
  --set-env-vars "ENVIRONMENT=production"
```

### Step 4: Set Environment Variables

```powershell
# You'll be prompted to set environment variables
# Or use Cloud Console > Cloud Run > Edit & Deploy New Revision > Variables & Secrets

# Set secrets using Secret Manager (more secure)
echo -n "your-stripe-secret-key" | gcloud secrets create stripe-secret-key --data-file=-
echo -n "your-jwt-secret" | gcloud secrets create jwt-secret-key --data-file=-
echo -n "your-openai-key" | gcloud secrets create openai-api-key --data-file=-

# Grant Cloud Run access to secrets
gcloud secrets add-iam-policy-binding stripe-secret-key `
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" `
  --role="roles/secretmanager.secretAccessor"
```

### Step 5: Get Your URL

```powershell
# After deployment, you'll get a URL like:
# https://anti-lust-backend-xxxxx-uc.a.run.app

# Test it:
curl https://anti-lust-backend-xxxxx-uc.a.run.app/health
```

---

## Option 2: App Engine

**Good for:** Traditional deployment, simpler than Cloud Run

### Step 1: Create app.yaml

```yaml
runtime: python311

instance_class: F2

env_variables:
  ENVIRONMENT: "production"
  
automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
  
handlers:
- url: /.*
  script: auto
  secure: always
```

### Step 2: Create requirements.txt (if not exists)

```powershell
pip freeze > requirements.txt
```

### Step 3: Deploy

```powershell
# Deploy to App Engine
gcloud app deploy

# View logs
gcloud app logs tail -s default

# Open in browser
gcloud app browse
```

---

## Option 3: Compute Engine (Full Control)

**Good for:** Maximum control, complex setups

### Step 1: Create VM Instance

```powershell
# Create VM
gcloud compute instances create anti-lust-vm `
  --zone=us-central1-a `
  --machine-type=e2-medium `
  --image-family=debian-11 `
  --image-project=debian-cloud `
  --boot-disk-size=50GB `
  --tags=http-server,https-server

# Configure firewall
gcloud compute firewall-rules create allow-http `
  --allow tcp:80,tcp:443,tcp:8000 `
  --target-tags http-server
```

### Step 2: SSH into VM

```powershell
# Connect to VM
gcloud compute ssh anti-lust-vm --zone=us-central1-a
```

### Step 3: Setup on VM

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3.11
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# Install Git
sudo apt-get install -y git

# Clone your repository (or upload files)
git clone https://github.com/your-repo/anti-lust-backend.git
cd anti-lust-backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Nginx
sudo apt-get install -y nginx

# Install Supervisor (to keep app running)
sudo apt-get install -y supervisor
```

### Step 4: Configure Nginx

```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/anti-lust
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/anti-lust /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: Configure Supervisor

```bash
sudo nano /etc/supervisor/conf.d/anti-lust.conf
```

Add:
```ini
[program:anti-lust]
directory=/home/YOUR_USER/anti-lust-backend
command=/home/YOUR_USER/anti-lust-backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
user=YOUR_USER
autostart=true
autorestart=true
stderr_logfile=/var/log/anti-lust/err.log
stdout_logfile=/var/log/anti-lust/out.log
```

```bash
# Create log directory
sudo mkdir /var/log/anti-lust

# Start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start anti-lust
```

---

## Database Setup (Cloud SQL)

### Step 1: Create PostgreSQL Instance

```powershell
# Create Cloud SQL PostgreSQL instance
gcloud sql instances create anti-lust-db `
  --database-version=POSTGRES_15 `
  --tier=db-f1-micro `
  --region=us-central1 `
  --root-password=YOUR_SECURE_PASSWORD

# Create database
gcloud sql databases create guardian_db --instance=anti-lust-db

# Create user
gcloud sql users create backend_user `
  --instance=anti-lust-db `
  --password=YOUR_USER_PASSWORD
```

### Step 2: Connect from Cloud Run

```powershell
# Get connection name
gcloud sql instances describe anti-lust-db --format="value(connectionName)"
# Output: PROJECT_ID:REGION:INSTANCE_NAME

# Deploy with Cloud SQL connection
gcloud run deploy anti-lust-backend `
  --image gcr.io/$PROJECT_ID/backend `
  --add-cloudsql-instances PROJECT_ID:REGION:anti-lust-db `
  --set-env-vars "DATABASE_URL=postgresql+asyncpg://backend_user:PASSWORD@/guardian_db?host=/cloudsql/PROJECT_ID:REGION:anti-lust-db"
```

### Step 3: Alternative - Use Supabase (Easier & Free)

```powershell
# Instead of Cloud SQL, use Supabase (free PostgreSQL)
# 1. Go to https://supabase.com
# 2. Create project
# 3. Get connection string
# 4. Set as environment variable

# Example DATABASE_URL:
# postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

---

## Environment Variables

### Set All Required Variables

```powershell
# For Cloud Run
gcloud run services update anti-lust-backend `
  --update-env-vars `
    STRIPE_SECRET_KEY=sk_live_xxxxx `
    STRIPE_PUBLISHABLE_KEY=pk_live_xxxxx `
    STRIPE_MONTHLY_PRICE_ID=price_xxxxx `
    STRIPE_YEARLY_PRICE_ID=price_xxxxx `
    STRIPE_LIFETIME_PRICE_ID=price_xxxxx `
    STRIPE_WEBHOOK_SECRET=whsec_xxxxx `
    SMTP_HOST=smtp.gmail.com `
    SMTP_PORT=587 `
    SMTP_USERNAME=your-email@gmail.com `
    SMTP_PASSWORD=your-app-password `
    EMAIL_SENDER=noreply@yourdomain.com `
    ADMIN_EMAIL=admin@yourdomain.com `
    DATABASE_URL=postgresql://user:pass@host/db `
    API_SECRET_KEY=your-api-key `
    JWT_SECRET_KEY=your-jwt-key `
    JWT_ALGORITHM=HS256 `
    JWT_EXPIRATION_HOURS=24 `
    OPENAI_API_KEY=sk-proj-xxxxx `
    ML_API_KEYS=key1,key2 `
    ALLOWED_ORIGINS=https://yourdomain.com `
    RATE_LIMIT_PER_MINUTE=100 `
    MAX_IMAGE_SIZE_MB=10 `
    MAX_TEXT_LENGTH=10000
```

---

## Cost Estimates (Monthly)

### Cloud Run (Recommended)
- **Free Tier**: 2M requests, 360,000 GB-seconds, 180,000 vCPU-seconds
- **Low Traffic** (10k requests/month): **$0** (within free tier)
- **Medium Traffic** (100k requests/month): **~$5-10**
- **High Traffic** (1M requests/month): **~$20-40**

### Cloud SQL PostgreSQL
- **db-f1-micro** (shared CPU, 614 MB): **$7.67/month**
- **db-g1-small** (1 vCPU, 1.7 GB): **$25/month**
- **Alternative**: Supabase Free (500 MB): **$0**

### Cloud Storage (for files)
- **5 GB**: **$0.10/month**
- **First 5 GB downloads/month**: Free

### Total Estimated Cost
- **Minimal setup**: **$0-10/month** (Cloud Run + Supabase)
- **Small production**: **$15-25/month** (Cloud Run + Cloud SQL micro)
- **Medium production**: **$30-60/month** (Cloud Run + Cloud SQL small)

---

## Post-Deployment Checklist

### ✅ Testing
```powershell
# Test health endpoint
curl https://your-url.run.app/health

# Test ML endpoint
curl -X POST https://your-url.run.app/api/ml/analyze `
  -H "Content-Type: application/json" `
  -d '{"text":"test"}'
```

### ✅ Monitoring
- Go to Cloud Console > Cloud Run > your-service
- Check **Logs** tab
- Check **Metrics** tab
- Set up **Alerts**

### ✅ Custom Domain (Optional)
```powershell
# Map custom domain
gcloud run services add-iam-policy-binding anti-lust-backend `
  --member="allUsers" `
  --role="roles/run.invoker"

gcloud run domain-mappings create `
  --service anti-lust-backend `
  --domain api.yourdomain.com
```

### ✅ SSL Certificate
- Cloud Run automatically provides HTTPS
- Custom domains get automatic SSL from Google

### ✅ Update Frontend
Update your website/mobile app to use new backend URL:
```javascript
// In your frontend
const API_URL = 'https://anti-lust-backend-xxxxx-uc.a.run.app';
```

---

## Troubleshooting

### Issue: Container fails to start
```powershell
# View logs
gcloud run services logs read anti-lust-backend --limit=50

# Common fix: Check PORT environment variable
# Cloud Run expects port 8080
```

### Issue: Out of memory
```powershell
# Increase memory
gcloud run services update anti-lust-backend --memory 4Gi
```

### Issue: Cold starts
```powershell
# Keep minimum instances
gcloud run services update anti-lust-backend --min-instances 1
```

### Issue: Database connection fails
```powershell
# Check Cloud SQL connection name
# Verify DATABASE_URL format
# Ensure Cloud SQL API is enabled
```

---

## Quick Deploy Script

Save as `deploy.ps1`:

```powershell
# Google Cloud Deploy Script
$PROJECT_ID = "anti-lust-guardian"
$REGION = "us-central1"
$SERVICE_NAME = "anti-lust-backend"

# Build and deploy
Write-Host "Building container..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/backend

Write-Host "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/backend `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --memory 2Gi `
  --cpu 2 `
  --max-instances 10

Write-Host "Deployment complete!"
gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)"
```

Run:
```powershell
.\deploy.ps1
```

---

## My Recommendation

**For Anti-Lust Guardian, I recommend:**

1. **Use Cloud Run** (easiest, cheapest, scales automatically)
2. **Use Supabase for database** (free, managed PostgreSQL)
3. **Start with free tier** (test everything)
4. **Upgrade as you grow**

**Total cost to start: $0/month** (within free tiers)

---

**Your backend is ready. This guide is honest and complete. You can do this!** 🚀
