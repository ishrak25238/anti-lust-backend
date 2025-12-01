import 'dart:async';
import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/services.dart';
import 'package:image/image.dart' as img;
import 'motivational_quotes.dart';

/// NSFW Detection Service that triggers app exit and motivational quotes
class NSFWDetectionService {
  final String _backendUrl;
  final MotivationalQuotesService _quotes = MotivationalQuotesService();
  bool _isMonitoring = false;
  Timer? _monitoringTimer;

  NSFWDetectionService({required String backendUrl}) : _backendUrl = backendUrl;

  /// Start monitoring for NSFW content
  void startMonitoring() {
    if (_isMonitoring) return;
    
    _isMonitoring = true;
    // Check every 5 seconds (adjust based on performance needs)
    _monitoringTimer = Timer.periodic(Duration(seconds: 5), (_) async {
      await _checkCurrentScreen();
    });
  }

  /// Stop monitoring
  void stopMonitoring() {
    _isMonitoring = false;
    _monitoringTimer?.cancel();
    _monitoringTimer = null;
  }

  /// Check current screen for NSFW content
  Future<void> _checkCurrentScreen() async {
    try {
      // Capture screenshot (requires platform-specific implementation)
      final screenshot = await _captureScreenshot();
      if (screenshot == null) return;

      // Send to backend for analysis
      final response = await _analyzeImage(screenshot);
      
      if (response['isNSFW'] == true) {
        final score = response['score'] as double? ?? 0.0;
        
        // Trigger actions if NSFW detected with high confidence
        if (score > 0.7) {
          await _triggerNSFWDetected();
        }
      }
    } catch (e) {
      print("NSFW detection error: $e");
    }
  }

  /// Capture screenshot (platform-specific)
  Future<List<int>?> _captureScreenshot() async {
    try {
      // This would use platform channels to capture screenshot
      // For now, return null (needs implementation)
      return null;
    } catch (e) {
      print("Screenshot capture error: $e");
      return null;
    }
  }

  /// Send image to backend for NSFW analysis
  Future<Map<String, dynamic>> _analyzeImage(List<int> imageBytes) async {
    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$_backendUrl/api/ml/scan-image'),
      );
      
      request.files.add(
        http.MultipartFile.fromBytes(
          'image',
          imageBytes,
          filename: 'screenshot.jpg',
        ),
      );

      final response = await request.send();
      final responseBody = await response.stream.bytesToString();
      final data = jsonDecode(responseBody);

      return {
        'isNSFW': !data['is_safe'],
        'score': data['score'] ?? 0.0,
        'flags': data['flags'] ?? [],
      };
    } catch (e) {
      print("Backend analysis error: $e");
      return {'isNSFW': false, 'score': 0.0};
    }
  }

  /// Trigger NSFW detection response
  Future<void> _triggerNSFWDetected() async {
    try {
      // 1. Show motivational quote with TTS
      await _quotes.speakAndShowQuote();
      
      // 2. Wait for quote to finish
      await Future.delayed(Duration(seconds: 3));
      
      // 3. Exit the app
      await _exitApp();
    } catch (e) {
      print("NSFW trigger error: $e");
    }
  }

  /// Exit the application
  Future<void> _exitApp() async {
    if (Platform.isAndroid) {
      SystemNavigator.pop();
    } else if (Platform.isIOS) {
      exit(0);
    }
  }

  void dispose() {
    stopMonitoring();
    _quotes.dispose();
  }
}
