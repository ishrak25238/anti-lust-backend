# Flutter Install Guide (Windows)

## Step 1: Download Flutter SDK

1. Go to https://docs.flutter.dev/get-started/install/windows
2. Download the latest stable release (Flutter SDK .zip file)
3. Extract to `C:\flutter` (create folder if needed)

## Step 2: Update PATH

**Option A: Using System Properties**
1. Open Start Menu → Search "Environment Variables"
2. Click "Edit the system environment variables"
3. Click "Environment Variables" button
4. Under "User variables", find "Path", click "Edit"
5. Click "New" and add: `C:\flutter\bin`
6. Click "OK" on all dialogs

**Option B: Using PowerShell (Admin)**
```powershell
[System.Environment]::SetEnvironmentVariable('Path', $env:Path + ';C:\flutter\bin', 'User')
```

## Step 3: Verify Installation

Open **NEW** PowerShell window (important - to reload PATH):

```powershell
flutter --version
flutter doctor
```

You should see Flutter version info and a diagnostic report.

## Step 4: Install Dependencies

Run `flutter doctor` and install missing dependencies:

**Android Studio (for Android development):**
1. Download from https://developer.android.com/studio
2. Install with default settings
3. Run `flutter doctor --android-licenses` and accept all

**Visual Studio (for Windows desktop):**
1. Download from https://visualstudio.microsoft.com/downloads/
2. Install "Desktop development with C++" workload
3. Restart after installation

**Chrome (for web development):**
- Install Google Chrome if not already installed

## Step 5: Verify All Platforms

```powershell
flutter doctor -v
```

You should see checkmarks (✓) for:
- Flutter (Channel stable)
- Windows Version
- Android toolchain
- Chrome
- Visual Studio

## Step 6: Test Flutter

```powershell
flutter create test_app
cd test_app
flutter run -d windows
```

A sample Flutter app should launch!

---

## Quick Reference

**Check Flutter version:**
```powershell
flutter --version
```

**Update Flutter:**
```powershell
flutter upgrade
```

**See available devices:**
```powershell
flutter devices
```

**Run on specific platform:**
```powershell
flutter run -d windows     # Windows desktop
flutter run -d chrome      # Web (Chrome)
flutter run -d android     # Android (if emulator running)
```

---

## Troubleshooting

**"flutter is not recognized":**
- Make sure you added `C:\flutter\bin` to PATH
- Restart PowerShell/Terminal
- Check PATH: `echo $env:Path`

**Android licenses not accepted:**
```powershell
flutter doctor --android-licenses
```
Type 'y' for each prompt

**Visual Studio errors:**
- Make sure "Desktop development with C++" is installed
- Restart after installation

---

## Next Steps for Anti-Lust Guardian

Once Flutter is installed:

```powershell
cd "e:\Anti-Lust app\anti_lust_guardian"
flutter pub get
# Setup .env file with your API keys
flutter run -d windows
```

Your app will launch with:
- Cosmic UI design
- Payment-required paywall
- Protection engine ready to test!
