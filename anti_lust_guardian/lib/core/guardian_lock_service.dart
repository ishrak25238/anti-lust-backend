import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'privacy_service.dart';

class GuardianLockService {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  final PrivacyService _privacyService = PrivacyService();
  
  static const String _pinKey = 'guardian_pin';
  static const String _recoveryEmailKey = 'guardian_recovery_email';
  static const String _failedAttemptsKey = 'guardian_failed_attempts';
  static const int _maxAttempts = 5;

  Future<bool> isPinSet() async {
    final pin = await _storage.read(key: _pinKey);
    return pin != null && pin.isNotEmpty;
  }

  Future<void> setPin(String pin) async {
    if (pin.length < 4 || pin.length > 6) {
      throw Exception('PIN must be 4-6 digits');
    }
    await _storage.write(key: _pinKey, value: pin);
    await _resetFailedAttempts();
  }

  Future<bool> validatePin(String enteredPin) async {
    final storedPin = await _storage.read(key: _pinKey);
    
    if (storedPin == enteredPin) {
      await _resetFailedAttempts();
      return true;
    } else {
      await _incrementFailedAttempts();
      return false;
    }
  }

  Future<void> _incrementFailedAttempts() async {
    final currentStr = await _storage.read(key: _failedAttemptsKey);
    int current = int.tryParse(currentStr ?? '0') ?? 0;
    current++;
    
    if (current >= _maxAttempts) {
      await _privacyService.incinerateData();
    } else {
      await _storage.write(key: _failedAttemptsKey, value: current.toString());
    }
  }

  Future<void> _resetFailedAttempts() async {
    await _storage.delete(key: _failedAttemptsKey);
  }

  Future<void> setRecoveryEmail(String email) async {
    await _storage.write(key: _recoveryEmailKey, value: email);
  }

  Future<void> removePin() async {
    await _storage.delete(key: _pinKey);
  }
}
