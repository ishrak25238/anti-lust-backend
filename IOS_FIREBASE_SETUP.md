# iOS Firebase Setup Guide (For Windows Users)

## 🚨 Important: Xcode Limitation

**Xcode only runs on macOS.** Since you're on Windows, you have two options:

### Option 1: Configure Now, Build Later (Recommended)
- ✅ I've already configured the iOS files for you using **CocoaPods**
- ⏳ You'll need access to a Mac later to actually build the iOS app
- 📱 This setup will work when you eventually build on macOS

### Option 2: Skip iOS for Now
- Focus only on Android development
- Add iOS support later when you have Mac access

---

## ✅ What I've Already Done for You

### Created Podfile with Firebase Dependencies

I've created [`ios/Podfile`](file:///e:/Anti-Lust%20app/anti_lust_guardian/ios/Podfile) with:
- Firebase Core
- Firebase Auth
- Cloud Firestore
- Google Sign-In

This is **equivalent** to using Swift Package Manager in Xcode, but configured via CocoaPods instead.

---

## 📋 Steps to Complete (When You Have Mac Access)

### 1. Add iOS App to Firebase Console

> [!IMPORTANT]
> You need to do this **right now** from Windows to download the config file!

1. Open Firebase Console: https://console.firebase.google.com/project/anti-lust-guardian/settings/general
2. Click **"Add app"** → Select **iOS** icon (🍎)
3. **iOS bundle ID:** `com.antilustguardian.app`
4. **App nickname:** `Anti-Lust Guardian iOS`
5. Click **"Register app"**
6. **Download `GoogleService-Info.plist`**
7. Save it to: `e:\Anti-Lust app\anti_lust_guardian\ios\Runner\GoogleService-Info.plist`

### 2. When on Mac: Install CocoaPods Dependencies

```bash
cd ios
pod install
```

This will download and install all Firebase libraries.

### 3. When on Mac: Open in Xcode

```bash
# Open the WORKSPACE, not the project!
open Runner.xcworkspace
```

### 4. Verify GoogleService-Info.plist is Included

In Xcode's file navigator, make sure `GoogleService-Info.plist` is in the `Runner` folder with a checkmark next to your target.

---

## 🔄 Alternative: Swift Package Manager (Mac Only)

If you prefer Swift Package Manager over CocoaPods when you get Mac access:

1. **Remove Podfile**: Delete `ios/Podfile`
2. **Open Xcode**: `open ios/Runner.xcworkspace`
3. **Add Package**: File → Add Packages
4. **Firebase SDK URL**: `https://github.com/firebase/firebase-ios-sdk`
5. **Select Products**:
   - FirebaseAuth
   - FirebaseFirestore
   - FirebaseAnalytics (or FirebaseAnalyticsWithoutAdId)
   - GoogleSignIn (separate repo: https://github.com/google/GoogleSignIn-iOS)

However, **CocoaPods is already configured** for you, so you're ready to go!

---

## 📱 Current iOS Configuration Status

| Task | Status |
|------|--------|
| Create Podfile with Firebase | ✅ Complete |
| Register iOS app in Firebase | ⏳ **YOU NEED TO DO THIS** |
| Download GoogleService-Info.plist | ⏳ **YOU NEED TO DO THIS** |
| Place GoogleService-Info.plist | ⏳ Waiting on download |
| Install pods (Mac required) | ⏳ Requires Mac |
| Build in Xcode (Mac required) | ⏳ Requires Mac |

---

## 🎯 Next Action Items

### Right Now (From Windows):

1. **Register iOS App** in Firebase Console
2. **Download `GoogleService-Info.plist`**
3. **Place it at**: `e:\Anti-Lust app\anti_lust_guardian\ios\Runner\GoogleService-Info.plist`

### Later (When You Have Mac):

1. Open Terminal in project folder
2. Run:
   ```bash
   cd ios
   pod install
   ```
3. Open `Runner.xcworkspace` in Xcode
4. Build and run on iOS simulator or device

---

## ⚠️ Important Notes

- **Bundle ID**: Set to `com.antilustguardian.app` (matches Android)
- **Minimum iOS Version**: iOS 12.0+
- **CocoaPods vs SPM**: Both work, but CocoaPods is already configured
- **Workspace**: Always open `.xcworkspace`, never `.xcodeproj` after pod install
- **GoogleService-Info.plist**: Must be added to Firebase Console first, then downloaded

---

## 🚀 Testing iOS (Requires Mac)

Once you have Mac access and complete the setup:

```bash
# Run on iOS simulator
flutter run -d ios

# Or in Xcode
open ios/Runner.xcworkspace
# Then click the Play button
```

---

## 📖 Summary

**What's Ready:**
- ✅ iOS Podfile configured with Firebase
- ✅ Flutter packages support iOS
- ✅ main.dart initialized Firebase

**What You Need:**
- ⏳ Register iOS app in Firebase Console (can do now from Windows)
- ⏳ Download GoogleService-Info.plist (can do now)
- ⏳ Mac to actually build the iOS app (later)
