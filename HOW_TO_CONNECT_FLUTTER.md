# 📱 How to Connect Flutter App to Backend

## Step 1: The API Key is Already Configured! ✅

I already added it to your Flutter app at:  
**File**: `anti_lust_guardian\lib\core\ai_threat_prediction.dart` (line 20)

```dart
static const String mlApiKey = 'MKO4K06joZ9HVaG-znFkW3S_22wvUFsIevu6hyYHjEk';
```

---

## Step 2: Make HTTP Requests from Flutter

### Example: Analyze a URL

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>> analyzeUrl(String url) async {
  // Your backend URL
  final baseUrl = 'http://localhost:8000';  // or use your IP address
  
  // Make the request
  final response = await http.post(
    Uri.parse('$baseUrl/api/ml/threat-url'),
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': AiThreatPrediction.mlApiKey,  // Use the static key
    },
    body: jsonEncode({
      'url': url,
    }),
  );

  if (response.statusCode == 200) {
    return jsonDecode(response.body);
  } else {
    throw Exception('Failed to analyze URL: ${response.body}');
  }
}

// Usage
void checkUrl() async {
  try {
    final result = await analyzeUrl('https://example.com');
    print('Threat score: ${result['threat_score']}');
    print('Is blocked: ${result['is_blocked']}');
  } catch (e) {
    print('Error: $e');
  }
}
```

---

## Step 3: Find Your Backend URL

### If running on the same computer:
```dart
final baseUrl = 'http://localhost:8000';
```

### If running on a physical device or emulator:
Find your computer's IP address:

**Windows (PowerShell)**:
```bash
ipconfig
# Look for "IPv4 Address" (e.g., 192.168.1.100)
```

Then use:
```dart
final baseUrl = 'http://192.168.1.100:8000';  // Replace with your IP
```

---

## Step 4: Update Your App Configuration

Create a config file: `lib/config/api_config.dart`

```dart
class ApiConfig {
  // Change this to your computer's IP when testing on device
  static const String baseUrl = 'http://localhost:8000';
  
  // Or use environment-specific URLs
  static String get apiUrl {
    // During development on physical device
    // return 'http://192.168.1.100:8000';
    
    // During development on emulator
    return 'http://10.0.2.2:8000';  // Android emulator special IP
    
    // In production
    // return 'https://your-production-url.com';
  }
}
```

---

## Step 5: Make Requests in Your App

### Example: Update your threat checking code

**File**: Wherever you're checking URLs (e.g., `lib/services/threat_service.dart`)

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../core/ai_threat_prediction.dart';
import '../config/api_config.dart';

class ThreatService {
  Future<bool> isUrlBlocked(String url) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.apiUrl}/api/ml/threat-url'),
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': AiThreatPrediction.mlApiKey,
        },
        body: jsonEncode({'url': url}),
      );

      if (response.statusCode == 200) {
        final result = jsonDecode(response.body);
        return result['is_blocked'] ?? false;
      }
      
      return false; // Fail open if API is down
    } catch (e) {
      print('Error checking URL: $e');
      return false; // Fail open
    }
  }
}
```

---

## Step 6: Test It!

### Start the backend:
```bash
cd "E:\Anti-Lust app\backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Run your Flutter app:
```bash
cd "E:\Anti-Lust app\anti_lust_guardian"
flutter run
```

### Test in your app:
```dart
final threatService = ThreatService();
final isBlocked = await threatService.isUrlBlocked('https://porn-site.com');
print('URL blocked: $isBlocked'); // Should detect it
```

---

## Common Issues & Solutions

### ❌ "Connection refused"
**Problem**: Can't reach the backend  
**Fix**: Make sure backend is running (`python -m uvicorn main:app --host 0.0.0.0 --port 8000`)

### ❌ "API key required"
**Problem**: Header not sent  
**Fix**: Make sure you're including the `X-API-Key` header

### ❌ "Network error" on Android emulator
**Problem**: `localhost` doesn't work on Android emulator  
**Fix**: Use `http://10.0.2.2:8000` instead of `http://localhost:8000`

### ❌ "Network error" on physical device
**Problem**: Device can't reach your computer  
**Fix**: 
1. Get your computer's IP address (`ipconfig`)
2. Use that IP: `http://192.168.1.100:8000`
3. Make sure Windows Firewall allows Python/uvicorn

---

## Quick Reference

| Scenario | Backend URL |
|----------|-------------|
| Flutter Desktop (same computer) | `http://localhost:8000` |
| Android Emulator | `http://10.0.2.2:8000` |
| iOS Simulator | `http://localhost:8000` |
| Physical Device (same WiFi) | `http://YOUR_IP:8000` |
| Production | `https://your-domain.com` |

---

## API Key (Already Configured)
```
MKO4K06joZ9HVaG-znFkW3S_22wvUFsIevu6hyYHjEk
```

**Everything is already set up! Just use the examples above.** ✅
