import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter/material.dart';

/// Password Service for parent verification - Strong password required
class PasswordService {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  static const String _passwordKey = 'parent_password';
  static const String _passwordSetKey = 'password_is_set';
  
  /// Password requirements
  static const int minLength = 8;
  
  /// Validate password strength
  /// Returns null if valid, error message if invalid
  static String? validatePassword(String password) {
    if (password.length < minLength) {
      return 'Password must be at least $minLength characters';
    }
    if (!password.contains(RegExp(r'[A-Z]'))) {
      return 'Password must contain at least one uppercase letter';
    }
    if (!password.contains(RegExp(r'[a-z]'))) {
      return 'Password must contain at least one lowercase letter';
    }
    if (!password.contains(RegExp(r'[0-9]'))) {
      return 'Password must contain at least one number';
    }
    if (!password.contains(RegExp(r'[!@#$%^&*(),.?":{}|<>]'))) {
      return 'Password must contain at least one special character (!@#\$%^&*...)';
    }
    return null; // Valid
  }
  
  /// Check if password meets all requirements
  static bool isStrongPassword(String password) {
    return validatePassword(password) == null;
  }
  
  /// Verify if entered password matches stored password
  Future<bool> verifyPassword(String password) async {
    try {
      final storedPassword = await _storage.read(key: _passwordKey);
      if (storedPassword == null) {
        return false; // No password set, must set one first
      }
      return password == storedPassword;
    } catch (e) {
      return false;
    }
  }
  
  /// Set new parent password (validates strength first)
  Future<void> setPassword(String password) async {
    final error = validatePassword(password);
    if (error != null) {
      throw Exception(error);
    }
    await _storage.write(key: _passwordKey, value: password);
    await _storage.write(key: _passwordSetKey, value: 'true');
  }
  
  /// Check if password has been set
  Future<bool> hasPasswordSet() async {
    final isSet = await _storage.read(key: _passwordSetKey);
    return isSet == 'true';
  }
  
  /// Check if this is first time (needs password setup)
  Future<bool> needsPasswordSetup() async {
    return !(await hasPasswordSet());
  }
  
  /// Show password verification dialog
  static Future<bool> showPasswordDialog(BuildContext context, {String title = 'Enter Parent Password'}) async {
    String enteredPassword = '';
    final passwordService = PasswordService();
    
    return await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext dialogContext) {
        return AlertDialog(
          title: Text(title),
          content: StatefulBuilder(
            builder: (BuildContext context, StateSetter setState) {
              return Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  TextField(
                    obscureText: true,
                    onChanged: (value) {
                      enteredPassword = value;
                    },
                    decoration: const InputDecoration(
                      labelText: 'Password',
                      hintText: 'Enter your parent password',
                    ),
                  ),
                ],
              );
            },
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(dialogContext).pop(false),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                final isValid = await passwordService.verifyPassword(enteredPassword);
                if (dialogContext.mounted) {
                  if (isValid) {
                    Navigator.of(dialogContext).pop(true);
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Incorrect password')),
                    );
                  }
                }
              },
              child: const Text('Verify'),
            ),
          ],
        );
      },
    ) ?? false;
  }
  
  /// Show password setup dialog (for first-time setup)
  static Future<bool> showPasswordSetupDialog(BuildContext context) async {
    String newPassword = '';
    String confirmPassword = '';
    String? errorMessage;
    final passwordService = PasswordService();
    
    return await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext dialogContext) {
        return StatefulBuilder(
          builder: (context, setState) {
            return AlertDialog(
              title: const Text('Create Parent Password'),
              content: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Password Requirements:',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    const Text('• At least 8 characters'),
                    const Text('• At least one uppercase letter (A-Z)'),
                    const Text('• At least one lowercase letter (a-z)'),
                    const Text('• At least one number (0-9)'),
                    const Text('• At least one special character (!@#\$%^&*...)'),
                    const SizedBox(height: 16),
                    TextField(
                      obscureText: true,
                      onChanged: (value) {
                        newPassword = value;
                        setState(() {
                          errorMessage = validatePassword(value);
                        });
                      },
                      decoration: const InputDecoration(
                        labelText: 'New Password',
                        hintText: 'Create a strong password',
                      ),
                    ),
                    const SizedBox(height: 8),
                    TextField(
                      obscureText: true,
                      onChanged: (value) {
                        confirmPassword = value;
                      },
                      decoration: const InputDecoration(
                        labelText: 'Confirm Password',
                        hintText: 'Re-enter password',
                      ),
                    ),
                    if (errorMessage != null) ...[
                      const SizedBox(height: 8),
                      Text(
                        errorMessage!,
                        style: const TextStyle(color: Colors.red, fontSize: 12),
                      ),
                    ],
                  ],
                ),
              ),
              actions: [
                ElevatedButton(
                  onPressed: () async {
                    if (newPassword != confirmPassword) {
                      setState(() {
                        errorMessage = 'Passwords do not match';
                      });
                      return;
                    }
                    
                    final validationError = validatePassword(newPassword);
                    if (validationError != null) {
                      setState(() {
                        errorMessage = validationError;
                      });
                      return;
                    }
                    
                    try {
                      await passwordService.setPassword(newPassword);
                      if (dialogContext.mounted) {
                        Navigator.of(dialogContext).pop(true);
                      }
                    } catch (e) {
                      if (context.mounted) { // Ensure context is valid for setState
                        setState(() {
                          errorMessage = e.toString();
                        });
                      }
                    }
                  },
                  child: const Text('Create Password'),
                ),
              ],
            );
          },
        );
      },
    ) ?? false;
  }
}

/// Backwards compatibility - PinService now wraps PasswordService
/// @deprecated Use PasswordService instead
class PinService {
  final PasswordService _passwordService = PasswordService();
  
  Future<bool> verifyPin(String pin) => _passwordService.verifyPassword(pin);
  Future<void> setPin(String pin) => _passwordService.setPassword(pin);
  Future<bool> hasPinSet() => _passwordService.hasPasswordSet();
  
  static Future<bool> showPinDialog(BuildContext context, {String title = 'Enter Parent Password'}) {
    return PasswordService.showPasswordDialog(context, title: title);
  }
}
