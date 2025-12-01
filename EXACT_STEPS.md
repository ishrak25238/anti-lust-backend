# 🎯 EXACT STEPS - Copy & Paste Ready

## Step 1: Open This File in VS Code

```
E:\Anti-Lust app\anti_lust_guardian\lib\core\ai_threat_prediction.dart
```

You already have the API key there! ✅

---

## Step 2: Create a New File (API Service)

**Create**: `E:\Anti-Lust app\anti_lust_guardian\lib\services\backend_service.dart`

**Copy this ENTIRE code**:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/ai_threat_prediction.dart';

class BackendService {
  // Change this based on where you're testing
  static const String baseUrl = 'http://localhost:8000';
  
  // If testing on Android emulator, use this instead:
  // static const String baseUrl = 'http://10.0.2.2:8000';
  
  // If testing on physical device, use your computer's IP:
  // static const String baseUrl = 'http://192.168.2.14:8000';

  /// Check if a URL is threatening
  Future<Map<String, dynamic>> checkUrl(String url) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/ml/threat-url'),
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': AiThreatPrediction.mlApiKey,
        },
        body: jsonEncode({'url': url}),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('API Error: ${response.statusCode}');
      }
    } catch (e) {
      print('Error checking URL: $e');
      rethrow;
    }
  }

  /// Check server health
  Future<bool> isServerHealthy() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/health'),
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
```

---

## Step 3: Use It in Your App

**Example - Where you check if a URL should be blocked**:

```dart
import 'services/backend_service.dart';

// Create the service
final backendService = BackendService();

// Check a URL
Future<void> checkIfBlocked(String url) async {
  try {
    final result = await backendService.checkUrl(url);
    
    print('URL: ${result['url']}');
    print('Threat Score: ${result['threat_score']}');
    print('Is Blocked: ${result['is_blocked']}');
    
    if (result['is_blocked']) {
      // Show block page
      Navigator.push(context, MaterialPageRoute(
        builder: (context) => BlockPage(url: url),
      ));
    }
  } catch (e) {
    print('Failed to check URL: $e');
  }
}
```

---

## Step 4: Add HTTP Package (if not already added)

**Open**: `pubspec.yaml`

**Make sure you have**:
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0  # Add this line if not present
```

**Then run**:
```bash
cd "E:\Anti-Lust app\anti_lust_guardian"
flutter pub get
```

---

## Step 5: Test It!

### A. Make sure backend is running:
**Terminal 1**:
```bash
cd "E:\Anti-Lust app\backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO: ✓ Server ready!
INFO: Uvicorn running on http://0.0.0.0:8000
```

### B. Run your Flutter app:
**Terminal 2**:
```bash
cd "E:\Anti-Lust app\anti_lust_guardian"
flutter run
```

### C. Test the connection:
Add this test button somewhere in your app:

```dart
ElevatedButton(
  onPressed: () async {
    final service = BackendService();
    
    // Test server health
    final healthy = await service.isServerHealthy();
    print('Server healthy: $healthy');
    
    // Test URL check
    final result = await service.checkUrl('https://porn-test.com');
    print('Result: $result');
  },
  child: Text('Test Backend'),
)
```

---

## Step 6: Expected Results

When you click "Test Backend", you should see in console:

```
Server healthy: true
Result: {url: https://porn-test.com, threat_score: 0.3, is_blocked: false}
```

---

## 🔧 Troubleshooting

### ❌ "Connection refused"
**Fix**: Make sure backend is running (Step 5A)

### ❌ "Cannot reach server" (Android emulator)
**Fix**: Change `baseUrl` to `http://10.0.2.2:8000`

### ❌ "Cannot reach server" (Physical device)
**Fix**: Change `baseUrl` to `http://192.168.2.14:8000`

### ❌ Missing http package
**Fix**: 
```bash
flutter pub add http
```

---

## ✅ That's It!

1. ✅ Backend is running
2. ✅ API key is configured
3. ✅ Create `backend_service.dart` (copy code from Step 2)
4. ✅ Use it in your app (example in Step 3)
5. ✅ Test (Step 5)

**You're done! Your Flutter app can now call the backend.** 🚀
