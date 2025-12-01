import 'package:flutter/services.dart';
import 'package:local_auth/local_auth.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_jailbreak_detection/flutter_jailbreak_detection.dart';

class SecurityService {
  final LocalAuthentication _localAuth = LocalAuthentication();
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  Future<bool> isDeviceCompromised() async {
    try {
      bool jailbroken = await FlutterJailbreakDetection.jailbroken;
      bool developerMode = await FlutterJailbreakDetection.developerMode;
      return jailbroken || developerMode;
    } on PlatformException {
      return false;
    }
  }

  Future<bool> authenticateUser() async {
    try {
      bool canCheckBiometrics = await _localAuth.canCheckBiometrics;
      bool isDeviceSupported = await _localAuth.isDeviceSupported();

      if (!canCheckBiometrics || !isDeviceSupported) {
        return true; 
      }

      return await _localAuth.authenticate(
        localizedReason: 'Please authenticate to access Anti-Lust Guardian',
        options: const AuthenticationOptions(
          stickyAuth: true,
          biometricOnly: true,
        ),
      );
    } on PlatformException {
      // Authentication error
      return false;
    }
  }

  Future<void> writeSecure(String key, String value) async {
    await _storage.write(key: key, value: value);
  }

  Future<String?> readSecure(String key) async {
    return await _storage.read(key: key);
  }

  Future<bool> hasUserConsented() async {
    final consent = await _storage.read(key: 'user_consent');
    return consent == 'true';
  }
}
