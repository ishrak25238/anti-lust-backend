# 🚀 Anti-Lust Guardian - Website Deployment Guide

Complete guide to deploy your website and obtain API keys for payment processing.

---

## 📋 Pre-Deployment Checklist

- ✅ Website files are ready (`index.html`, `features.html`, `dashboard.html`, `api-docs.html`)
- ✅ All CSS and JavaScript files are present in `styles/` and `scripts/` folders
- ✅ Website tested locally and working correctly

---

## 🎯 Deployment Methods (Choose One)

### **Option 1: Netlify Drop** ⚡ (FASTEST - 2 Minutes)

**Best for:** Quick deployment without Git/GitHub

#### Steps:

1. **Visit Netlify Drop**
   - Go to: https://app.netlify.com/drop
   - No account needed initially!

2. **Prepare Your Files**
   - Open File Explorer: `e:\Anti-Lust app\website`
   - Select ALL files and folders (index.html, features.html, dashboard.html, api-docs.html, scripts/, styles/)

3. **Drag & Drop**
   - Drag the selected files directly onto the Netlify Drop page
   - Wait for upload to complete (usually 10-30 seconds)

4. **Get Your URL**
   - Netlify will provide a URL like: `https://random-name-12345.netlify.app`
   - Your site is now LIVE! 🎉

5. **Optional: Sign Up for Custom Domain**
   - Click "Claim this site"
   - Create free account
   - Change domain to something like: `antilust-guardian.netlify.app`

---

### **Option 2: Vercel** 🔥 (RECOMMENDED)

**Best for:** Best performance with edge network & analytics

#### Steps:

1. **Create Vercel Account**
   - Go to: https://vercel.com/signup
   - Sign up with GitHub, GitLab, or Email

2. **Install Vercel CLI** (Optional but easier)
   ```powershell
   npm install -g vercel
   ```

3. **Deploy via CLI**
   ```powershell
   cd "e:\Anti-Lust app\website"
   vercel
   ```
   - Follow the prompts:
     - "Set up and deploy"? → **Yes**
     - "Which scope"? → Select your account
     - "Link to existing project"? → **No**
     - "Project name"? → `antilust-guardian`
     - "Directory"? → Press Enter (current directory)
     - "Auto-detected settings"? → **Yes**

4. **Or Deploy via Web Dashboard**
   - Click "Add New Project"
   - Select "Import Third-Party Git Repository" OR upload files
   - Browse to: `e:\Anti-Lust app\website`
   - Click "Deploy"

5. **Get Your URL**
   - Vercel provides: `https://antilust-guardian.vercel.app`
   - Production ready instantly! 🚀

---

### **Option 3: GitHub Pages** 📦 (Best for Open Source)

**Best for:** Free hosting with version control

#### Steps:

1. **Create GitHub Repository**
   - Go to: https://github.com/new
   - Repository name: `antilust-guardian-website`
   - Make it Public (required for free GitHub Pages)
   - Click "Create repository"

2. **Upload Files to GitHub**
   
   **Option A: Via Web Interface**
   - Click "uploading an existing file"
   - Drag all files from `e:\Anti-Lust app\website`
   - Commit changes

   **Option B: Via Git Command Line**
   ```powershell
   cd "e:\Anti-Lust app\website"
   git init
   git add .
   git commit -m "Initial website deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/antilust-guardian-website.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: Select "main" branch
   - Folder: Select "/ (root)"
   - Click "Save"

4. **Get Your URL**
   - GitHub provides: `https://YOUR_USERNAME.github.io/antilust-guardian-website/`
   - Wait 2-3 minutes for first deployment

---

## 🔑 API Keys to Obtain After Deployment

### 1. **Stripe Payment Integration** (REQUIRED for payments)

#### Get Stripe API Keys:

1. **Create Stripe Account**
   - Go to: https://stripe.com
   - Click "Start now" → Sign up
   - Complete business verification

2. **Get API Keys**
   - Dashboard → Developers → API Keys
   - You'll see two keys:
     - **Publishable key** (starts with `pk_test_...` or `pk_live_...`)
     - **Secret key** (starts with `sk_test_...` or `sk_live_...`)

3. **Test Mode vs Live Mode**
   - Use **Test Mode** keys during development
   - Switch to **Live Mode** keys for production
   - Test cards: https://stripe.com/docs/testing

4. **Add Keys to Website**
   - Open `e:\Anti-Lust app\website\scripts\api.js`
   - Find: `const STRIPE_PUBLISHABLE_KEY = 'YOUR_KEY_HERE';`
   - Replace with your Publishable key
   - Re-deploy the updated file

#### Stripe Setup Checklist:
- [ ] Create Stripe account
- [ ] Activate account (may require business verification)
- [ ] Get Test Mode API keys
- [ ] Create products/prices in Stripe Dashboard:
  - Monthly subscription: $17/month (with 7-day free trial)
  - Lifetime license: $299 one-time
- [ ] Integrate Checkout or Payment Links
- [ ] Test with test card: `4242 4242 4242 4242`
- [ ] Get Live Mode API keys when ready to go live

### 2. **Google Analytics** (Optional - for tracking)

1. **Create GA4 Property**
   - Go to: https://analytics.google.com
   - Create Account → Create Property
   - Get Measurement ID (e.g., `G-XXXXXXXXXX`)

2. **Add to Website**
   - Add this to `<head>` of all HTML files:
   ```html
   <!-- Google Analytics -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-XXXXXXXXXX');
   </script>
   ```

### 3. **Custom Domain** (Optional - Professional branding)

#### Register Domain:
- **Namecheap**: https://www.namecheap.com (~$10/year)
- **Google Domains**: https://domains.google
- **Cloudflare**: https://www.cloudflare.com/products/registrar/

#### Connect to Hosting:

**For Netlify:**
- Netlify Dashboard → Domain Settings → Add custom domain
- Add DNS records provided by Netlify

**For Vercel:**
- Vercel Dashboard → Domains → Add
- Configure DNS as instructed

**For GitHub Pages:**
- Add `CNAME` file to repository root with domain name
- Configure DNS A records to GitHub IPs

---

## ✅ Post-Deployment Verification

1. **Test Website URL**
   - Visit your deployment URL
   - Verify homepage loads with animations

2. **Test All Pages**
   - ✅ Homepage (`index.html`)
   - ✅ Features page (`features.html`)
   - ✅ Dashboard demo (`dashboard.html`)
   - ✅ API docs (`api-docs.html`)

3. **Verify Assets**
   - ✅ Custom cursor appears and works
   - ✅ Starfield background animates
   - ✅ 3D shield animation rotates
   - ✅ Pricing toggle works
   - ✅ Buttons have hover effects

4. **Test on Multiple Devices**
   - Desktop browser
   - Mobile browser
   - Tablet (if available)

---

## 🚨 Troubleshooting

### Issue: CSS/JS Not Loading
- **Fix**: Ensure `styles/` and `scripts/` folders are deployed
- Check browser console (F12) for 404 errors

### Issue: Custom Domain Not Working
- **Fix**: DNS propagation takes 24-48 hours
- Use `nslookup yourdomain.com` to check DNS

### Issue: Stripe Not Working
- **Fix**: Ensure you're using the correct Publishable key (not Secret key)
- Check browser console for errors

---

## 📞 Next Steps

1. **Choose a deployment method** from above (Netlify recommended for speed)
2. **Deploy your website** following the step-by-step guide
3. **Get your live URL** and test it
4. **Sign up for Stripe** to enable payments
5. **Add Stripe API keys** to your website code
6. **Re-deploy** with updated API keys
7. **Start accepting payments!** 💰

---

## 💡 Quick Start Command (Vercel)

If you have npm installed, run:

```powershell
npm install -g vercel
cd "e:\Anti-Lust app\website"
vercel --prod
```

Your website will be live in under 60 seconds! 🚀

---

**Need help?** The deployment process is straightforward, but feel free to ask if you encounter any issues!
