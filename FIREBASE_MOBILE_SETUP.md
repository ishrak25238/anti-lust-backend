# Firebase Mobile Setup Guide (Android & iOS)

## 📱 Add Android App to Firebase

### Step 1: Go to Firebase Console
https://console.firebase.google.com/project/anti-lust-guardian/settings/general

### Step 2: Add Android App
1. Click **"Add app"** → Select **Android** icon
2. **Android package name:** `com.antilustguardian.app` (or your package name)
3. **App nickname:** `Anti-Lust Guardian Android`
4. **Debug signing certificate SHA-1:** (optional, get from Android Studio)
5. Click **"Register app"**

### Step 3: Download google-services.json
1. Click **"Download google-services.json"**
2. Save to: `e:\Anti-Lust app\anti_lust_guardian\android\app\google-services.json`

### Step 4: Add Firebase SDK to Android
File: `android/build.gradle`
```gradle
buildscript {
    dependencies {
        classpath 'com.google.gms:google-services:4.4.0'
    }
}
```

File: `android/app/build.gradle`
```gradle
apply plugin: 'com.google.gms.google-services'

dependencies {
    implementation platform('com.google.firebase:firebase-bom:32.7.0')
    implementation 'com.google.firebase:firebase-auth'
    implementation 'com.google.firebase:firebase-firestore'
}
```

---

## 🍎 Add iOS App to Firebase

### Step 1: Add iOS App
1. Same Firebase Console page
2. Click **"Add app"** → Select **iOS** icon
3. **iOS bundle ID:** `com.antilustguardian.app` (or your bundle ID)
4. **App nickname:** `Anti-Lust Guardian iOS`
5. Click **"Register app"**

### Step 2: Download GoogleService-Info.plist
1. Click **"Download GoogleService-Info.plist"**
2. Save to: `e:\Anti-Lust app\anti_lust_guardian\ios\Runner\GoogleService-Info.plist`

### Step 3: Add to Xcode
1. Open Xcode: `ios/Runner.xcworkspace`
2. Drag `GoogleService-Info.plist` into Runner folder
3. Check **"Copy items if needed"**

---

## 🔧 Flutter Configuration

### File: `pubspec.yaml`
```yaml
dependencies:
  firebase_core: ^2.24.2
  firebase_auth: ^4.16.0
  firebase_firestore: ^4.14.0
  google_sign_in: ^6.2.1
```

### File: `lib/main.dart`
```dart
import 'package:firebase_core/firebase_core.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}
```

---

## ✅ Enable Authentication Methods

### Google Sign-In (Already Done for Web)
✅ Already enabled in Firebase Console

### Additional for Mobile:
1. Firebase Console → **Authentication** → **Sign-in method**
2. **Google** → Already enabled ✅
3. **Email/Password** → Enable if you want email login

---

## 🔐 Get Firebase Admin SDK (for Backend)

### Step 1: Generate Private Key
1. Firebase Console → **Project Settings**
2. **Service accounts** tab
3. Click **"Generate new private key"**
4. Download the JSON file

### Step 2: Extract Values
Open the downloaded JSON, copy these to `.env`:

```env
FIREBASE_PROJECT_ID="anti-lust-guardian"
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n[PASTE_KEY_HERE]\n-----END PRIVATE KEY-----"
FIREBASE_CLIENT_EMAIL="firebase-adminsdk-xxxxx@anti-lust-guardian.iam.gserviceaccount.com"
```

---

## 📱 Mobile App Config Files

### Android: `google-services.json`
**Location:** `anti_lust_guardian/android/app/google-services.json`

Example structure:
```json
{
  "project_info": {
    "project_id": "anti-lust-guardian",
    "firebase_url": "https://anti-lust-guardian.firebaseio.com",
    "project_number": "77553493618"
  },
  "client": [
    {
      "client_info": {
        "android_client_info": {
          "package_name": "com.antilustguardian.app"
        }
      }
    }
  ]
}
```

### iOS: `GoogleService-Info.plist`
**Location:** `anti_lust_guardian/ios/Runner/GoogleService-Info.plist`

---

## 🧪 Test Mobile Authentication

### Android Test:
```powershell
cd "e:\Anti-Lust app\anti_lust_guardian"
flutter run -d android
```

### iOS Test:
```powershell
cd "e:\Anti-Lust app\anti_lust_guardian"
flutter run -d ios
```

---

## 🎯 Next Steps

1. [ ] Add Android app to Firebase Console
2. [ ] Download `google-services.json`
3. [ ] Add iOS app to Firebase Console
4. [ ] Download `GoogleService-Info.plist`
5. [ ] Update Flutter dependencies
6. [ ] Generate Firebase Admin SDK key
7. [ ] Update backend `.env` with Firebase credentials
8. [ ] Test authentication on both platforms

---

## ⚠️ Important Notes

- **Package name** must match exactly in Firebase and `android/app/build.gradle`
- **Bundle ID** must match exactly in Firebase and `ios/Runner.xcodeproj`
- Both Android & iOS apps share the **same Firestore database**
- Authentication works across all platforms (web, Android, iOS)
