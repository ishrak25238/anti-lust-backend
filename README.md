# Anti-Lust Guardian

**YOUR** cross-platform digital discipline guardian with mandatory payment protection.

## Features
- ✅ **Mandatory Subscription** - Users must pay before accessing protection
- ✅ **Cross-Platform** - Android, iOS, Windows, macOS, Linux
- ✅ **AI-Powered Filtering** - URL blocking, intent detection
- ✅ **Stripe Integration** - Secure payment processing
- ✅ **Focus Features** - Streak tracking, purpose pathways

## Tech Stack
- **Flutter** (Dart) - Cross-platform UI
- **Supabase** - FREE backend (auth, database, real-time sync)
- **Stripe** - Payment processing (only charges 2.9% + $0.30 per transaction)
- **TensorFlow Lite** - On-device AI filtering
- **Google Safe Browsing API** - Real-time threat detection

## Setup Instructions

### 1. Install Flutter

**Windows:**
```bash
# Download Flutter SDK from https://docs.flutter.dev/get-started/install/windows
# Extract to C:\flutter
# Add to PATH: C:\flutter\bin
```

**Verify installation:**
```bash
flutter doctor
```

### 2. Install Dependencies
```bash
cd anti_lust_guardian
flutter pub get
```

### 3. Setup Supabase

1. Go to https://supabase.com
2. Create new project (FREE tier)
3. Get your project URL and anon key
4. Copy `.env.example` to `.env.local`
5. Add your Supabase credentials

### 4. Setup Stripe

1. Go to https://stripe.com
2. Create account (FREE - no monthly fees)
3. Get your publishable and secret keys
4. Create subscription products:
   - **Monthly Pro**: $9.99/month
   - **Yearly Pro**: $99/year
   - **Lifetime**: $299 one-time
5. Add keys to `.env.local`

### 5. Run the App

**Android:**
```bash
flutter run -d android
```

**iOS:**
```bash
flutter run -d ios
```

**Windows:**
```bash
flutter run -d windows
```

**macOS:**
```bash
flutter run -d macos
```

**Linux:**
```bash
flutter run -d linux
```

## Build for Production

**Android APK:**
```bash
flutter build apk --release
```

**iOS:**
```bash
flutter build ios --release
```

**Windows:**
```bash
flutter build windows --release
```

**macOS:**
```bash
flutter build macos --release
```

**Linux:**
```bash
flutter build linux --release
```

## Monetization Strategy

✅ **Payment Required Before Use**
- No free tier - users MUST subscribe to access protection
- 7-day trial with payment method required upfront
- Automatic billing after trial

**Pricing:**
- Monthly: $9.99/mo
- Yearly: $99/year (save 17%)
- Lifetime: $299 (one-time)

**Revenue Calculator:**
- 100 users = ~$999/month
- 1,000 users = ~$9,990/month
- 10,000 users = ~$99,900/month

Less Stripe fees (2.9% + $0.30)

## Project Structure

```
anti_lust_guardian/
├── lib/
│   ├── main.dart                    # App entry
│   ├── app.dart                     # App configuration
│   ├── core/
│   │   ├── payment_gate.dart        # Payment requirement enforcement
│   │   ├── url_monitor.dart         # URL filtering
│   │   ├── ai_classifier.dart       # TensorFlow Lite
│   │   └── threat_db.dart           # Local threat database
│   ├── services/
│   │   ├── supabase_service.dart    # Backend API
│   │   ├── stripe_service.dart      # Payment processing
│   │   └── safe_browsing.dart       # Google API
│   ├── screens/
│   │   ├── paywall_screen.dart      # Payment required screen
│   │   ├── auth/                    # Login, signup
│   │   ├── dashboard.dart           # Main app
│   │   ├── focus_horizon.dart       # Streak tracking
│   │   └── block_page.dart          # Intervention screen
│   └── widgets/                     # Reusable components
├── assets/
│   ├── models/                      # TensorFlow models
│   └── threat_list.json             # Initial threats
├── android/                         # Android config
├── ios/                             # iOS config
├── windows/                         # Windows config
├── macos/                           # macOS config
├── linux/                           # Linux config
└── pubspec.yaml                     # Dependencies
```

## License

Proprietary - All rights reserved.
