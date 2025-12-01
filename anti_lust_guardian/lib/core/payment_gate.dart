import 'package:flutter_stripe/flutter_stripe.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PaymentGate {
  static const String _subscriptionKey = 'has_active_subscription';
  static const String _backendUrl = 'http://localhost:8000';

  Future<bool> hasActiveSubscription() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_subscriptionKey) ?? false;
  }

  Future<void> _setSubscription(bool active) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_subscriptionKey, active);
  }

  Future<void> startPayment({
    required String priceId,
    bool debugMode = false,
  }) async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) {
      throw Exception('User must be logged in to subscribe');
    }
    
    if (debugMode) {
      await Future.delayed(const Duration(seconds: 2));
      await _setSubscription(true);
      return;
    }

    final clientSecret = await _createSubscription(
      priceId: priceId,
      userId: user.uid,
      userEmail: user.email ?? '',
    );

    await Stripe.instance.initPaymentSheet(
      paymentSheetParameters: SetupPaymentSheetParameters(
        paymentIntentClientSecret: clientSecret,
        merchantDisplayName: 'Anti‑Lust Guardian',
      ),
    );

    await Stripe.instance.presentPaymentSheet();
    await _setSubscription(true);
  }

  Future<String> _createSubscription({
    required String priceId,
    required String userId,
    required String userEmail,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_backendUrl/api/subscription/create'),
       headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'price_id': priceId,
          'firebase_user_id': userId,
          'customer_email': userEmail,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['client_secret'];
      } else {
        throw Exception('Subscription creation failed: ${response.body}');
      }
    } catch (e) {
      throw Exception('Backend connection failed: $e');
    }
  }

  Future<void> subscribe() async => _setSubscription(true);
}
