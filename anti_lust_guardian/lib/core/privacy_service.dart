import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';

class PrivacyService {
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();
  
  static const String _incognitoKey = 'is_incognito_mode';
  static const String _lastIncinerationKey = 'last_incineration_timestamp';

  Future<bool> isIncognitoMode() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_incognitoKey) ?? false;
  }

  Future<void> setIncognitoMode(bool enabled) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_incognitoKey, enabled);
  }

  Future<void> incinerateData() async {
    await _secureStorage.deleteAll();

    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();

    
    await prefs.setString(_lastIncinerationKey, DateTime.now().toIso8601String());
  }

  Future<String> getDataFootprint() async {
    final allData = await _secureStorage.readAll();
    int bytes = 0;
    allData.forEach((key, value) {
      bytes += key.length + value.length;
    });
    
    if (bytes < 1024) return '$bytes B';
    if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(1)} KB';
    return '${(bytes / (1024 * 1024)).toStringAsFixed(1)} MB';
  }

  Future<void> enforceRetentionPolicy() async {
  }
}
