# Production Deployment Guide

## 🚀 Building for Production

### Prerequisites
- Flutter SDK installed
- Platform-specific SDKs (Android Studio, Xcode, Visual Studio, etc.)
- `.env` file configured with production API keys

---

## Android

### Build APK (Direct Distribution)
```bash
cd anti_lust_guardian
flutter build apk --release
```
Output: `build/app/outputs/flutter-apk/app-release.apk`

### Build App Bundle (Google Play Store)
```bash
flutter build appbundle --release
```
Output: `build/app/outputs/bundle/release/app-release.aab`

### Signing (Required for Production)

1. Create keystore:
```bash
keytool -genkey -v -keystore ~/anti-lust-key.jks -keyalg RSA -keysize 2048 - validity 10000 -alias anti-lust-key
```

2. Create `android/key.properties`:
```
storePassword=<your_password>
keyPassword=<your_password>
keyAlias=anti-lust-key
storeFile=<path_to_keystore>/anti-lust-key.jks
```

3. Update `android/app/build.gradle` (add before `android` block):
```gradle
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    ...
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

### Google Play Console
1. Create developer account ($25 one-time fee)
2. Create new app
3. Upload AAB file
4. Fill out store listing, privacy policy, content rating
5. Submit for review

---

## iOS

### Prerequisites
- Mac with Xcode installed
- Apple Developer account ($99/year)
- Signing certificates configured

### Build IPA
```bash
cd anti_lust_guardian
flutter build ios --release
```

### Create Archive (Xcode)
1. Open `ios/Runner.xcworkspace` in Xcode
2. Select "Any iOS Device" as target
3. Product → Archive
4. Distribute App → App Store Connect
5. Upload

### App Store Connect
1. Create new app
2. Fill out app information
3. Upload build via Xcode or Transporter
4. Submit for review

---

## Windows

### Build Windows App
```bash
cd anti_lust_guardian
flutter build windows --release
```
Output: `build/windows/runner/Release/`

### Create Installer (Optional)

**Option 1: MSIX (Microsoft Store)**
1. Add `msix` package to `pubspec.yaml`
2. Configure `msix_config` in pubspec.yaml
3. Run: `flutter pub run msix:create`

**Option 2: Inno Setup**
1. Download Inno Setup
2. Create installer script
3. Point to `build/windows/runner/Release/`

### Microsoft Store
1. Create developer account ($19 one-time)
2. Create app submission
3. Upload MSIX package
4. Submit for certification

---

## macOS

### Build macOS App
```bash
cd anti_lust_guardian
flutter build macos --release
```
Output: `build/macos/Build/Products/Release/anti_lust_guardian.app`

### Code Signing (Required)
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: YOUR NAME" anti_lust_guardian.app
```

### Create DMG Installer
```bash
hdiutil create -volname "Anti-Lust Guardian" -srcfolder anti_lust_guardian.app -ov -format UDZO anti-lust-guardian.dmg
```

### Mac App Store
1. Apple Developer account required
2. Create app in App Store Connect
3. Upload via Xcode or Transporter

---

## Linux

### Build Linux App
```bash
cd anti_lust_guardian
flutter build linux --release
```
Output: `build/linux/x64/release/bundle/`

### Create AppImage
```bash
# Install appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Create AppDir structure
# Package as AppImage
```

### Create .deb Package
```bash
# Create debian control file
# Package using dpkg-deb
```

### Create .rpm Package
```bash
# Use rpmbuild
```

---

## GitHub Actions (Automated Builds)

### Setup

1. Push code to GitHub
2. Workflow file already created: `.github/workflows/build.yml`
3. Create new release with tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

4. GitHub Actions will automatically:
   - Build for all platforms
   - Create artifacts
   - Upload to GitHub Releases

### Manual Trigger
Go to GitHub → Actions → Build and Release → Run workflow

---

## Environment Variables (Production)

### Create `.env` file:
```env
# Supabase (Production)
SUPABASE_URL=https://your-prod-project.supabase.co
SUPABASE_ANON_KEY=your_production_anon_key

# Stripe (Live Keys - IMPORTANT!)
STRIPE_PUBLISHABLE_KEY=pk_live_xxxxx
STRIPE_SECRET_KEY=sk_live_xxxxx

STRIPE_MONTHLY_PRICE_ID=price_live_monthly
STRIPE_YEARLY_PRICE_ID=price_live_yearly
STRIPE_LIFETIME_PRICE_ID=price_live_lifetime

# Google Safe Browsing (Production)
GOOGLE_SAFE_BROWSING_API_KEY=your_production_api_key
```

**⚠️ CRITICAL:**
- Never commit `.env` to git
- Use LIVE Stripe keys, not TEST keys
- Verify Supabase production database

---

## Pre-Launch Checklist

### Technical
- [ ] All `.env` variables set to production
- [ ] Stripe using LIVE keys (not test)
- [ ] Supabase using production database
- [ ] App version incremented in `pubspec.yaml`
- [ ] Icons and splash screens added for all platforms
- [ ] Tested on physical devices (not just emulators)

### Legal
- [ ] Privacy Policy published
- [ ] Terms of Service published
- [ ] COPPA compliance verified
- [ ] GDPR compliance (if EU users)
- [ ] PCI-DSS compliance (Stripe handles this)

### Business
- [ ] Stripe account verified
- [ ] Payment methods tested in LIVE mode
- [ ] Support email configured
- [ ] Analytics/monitoring setup (optional)

### Store Listings
- [ ] App name finalized
- [ ] Description written (compelling!)
- [ ] Screenshots prepared (5-8 per platform)
- [ ] Keywords researched (ASO)
- [ ] Privacy policy URL added
- [ ] Support URL added
- [ ] Age rating determined

---

## Post-Launch

### Monitoring
- Check Stripe dashboard for subscriptions
- Monitor Supabase database usage
- Watch for crash reports
- Review user feedback

### Updates
```bash
# Increment version in pubspec.yaml
version: 1.0.1+2

# Build
flutter build <platform> --release

# Upload to stores
```

---

##  Distribution Summary

| Platform | Distribution Method | Cost | Time to Approve |
|----------|-------------------|------|-----------------|
| **Android** | Google Play Store | $25 (one-time) | 1-7 days |
| **Android** | Direct APK (your website) | FREE | Instant |
| **iOS** | App Store | $99/year | 1-7 days |
| **Windows** | Microsoft Store | $19 (one-time) | 1-3 days |
| **Windows** | Direct Download (GitHub) | FREE | Instant |
| **macOS** | Mac App Store | $99/year | 1-7 days |
| **macOS** | Direct Download (signed) | $99/year | Instant |
| **Linux** | Direct Download (GitHub) | FREE | Instant |

**Recommended Strategy:**
1. **Phase 1:** Direct distribution (Windows, Linux, Android APK) - FREE  
2. **Phase 2:** After getting users, submit to stores

---

## Your App is READY for Production! 🎉

All code is production-ready. Just:
1. Setup production API keys
2. Build for your platforms
3. Submit to stores or distribute directly

**First revenue in < 24 hours possible!**
