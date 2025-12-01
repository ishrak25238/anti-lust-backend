import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'dart:math';

class ParentalLinkService {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  
  static const String _roleKey = 'user_role'; // 'parent' or 'child'
  static const String _pairingCodeKey = 'pairing_code';
  static const String _linkedDeviceIdKey = 'linked_device_id';
  static const String _childNameKey = 'child_name';

  Future<String?> getUserRole() async {
    return await _storage.read(key: _roleKey);
  }

  Future<void> setUserRole(String role) async {
    await _storage.write(key: _roleKey, value: role);
  }

  Future<String> generatePairingCode() async {
    final code = (100000 + Random().nextInt(900000)).toString();
    await _storage.write(key: _pairingCodeKey, value: code);
    return code;
  }

  Future<String?> getPairingCode() async {
    return await _storage.read(key: _pairingCodeKey);
  }

  Future<bool> linkChildAccount(String code, String childName) async {
    if (code.length == 6) {
      await _storage.write(key: _linkedDeviceIdKey, value: 'child_device_$code');
      await _storage.write(key: _childNameKey, value: childName);
      return true;
    }
    return false;
  }

  Future<bool> isLinked() async {
    final linkedId = await _storage.read(key: _linkedDeviceIdKey);
    return linkedId != null;
  }

  Future<String?> getChildName() async {
    return await _storage.read(key: _childNameKey);
  }

  Future<List<Map<String, dynamic>>> fetchChildLogs() async {
    await Future.delayed(const Duration(seconds: 1));
    
    return [
      {
        'timestamp': DateTime.now().subtract(const Duration(minutes: 10)).toString(),
        'activity': 'Blocked Attempt: "Adult Content"',
        'status': 'BLOCKED',
      },
      {
        'timestamp': DateTime.now().subtract(const Duration(hours: 1)).toString(),
        'activity': 'App Usage: "Instagram" (Dopamine Trap)',
        'status': 'WARNING',
      },
      {
        'timestamp': DateTime.now().subtract(const Duration(hours: 5)).toString(),
        'activity': 'Screen Shield: Screenshot Prevented',
        'status': 'SECURED',
      },
    ];
  }
}
