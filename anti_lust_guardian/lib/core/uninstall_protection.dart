import 'package:flutter/services.dart';
import 'package:flutter/foundation.dart';

/// Uninstall Protection using Device Admin
class UninstallProtection {
  static const MethodChannel _channel = MethodChannel('anti_lust/device_admin');
  
  /// Request Device Admin permissions
  Future<void> requestDeviceAdmin() async {
    try {
      await _channel.invokeMethod('requestDeviceAdmin');
    } catch (e) {
      debugPrint('Failed to request device admin: $e');
      rethrow;
    }
  }
  
  /// Check if app is Device Admin
  Future<bool> isDeviceAdmin() async {
    try {
      return await _channel.invokeMethod<bool>('isDeviceAdmin') ?? false;
    } catch (e) {
      return false;
    }
  }
  
  /// Send uninstall alert to backend
  Future<void> sendUninstallAlert() async {
    try {
      await _channel.invokeMethod('sendUninstallAlert');
    } catch (e) {
      debugPrint('Failed to send uninstall alert: $e');
    }
  }
  
  /// Prevent uninstall (requires Device Admin)
  Future<bool> preventUninstall() async {
    final isAdmin = await isDeviceAdmin();
    if (!isAdmin) {
      await requestDeviceAdmin();
      return await isDeviceAdmin();
    }
    return true;
  }
}
