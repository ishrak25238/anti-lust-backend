import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class PayWallScreen extends StatelessWidget {
  const PayWallScreen({super.key});

  Future<void> _launchPaymentUrl() async {
    // Redirect to LOGIN page with plan parameter.
    // This forces the user to log in first. Once logged in, auth.js will see the 'plan' param
    // and automatically redirect them to the Stripe payment page with their user ID attached.
    final Uri url = Uri.parse('https://anti-lust-guardian.web.app/login.html?plan=monthly');
    if (!await launchUrl(url, mode: LaunchMode.externalApplication)) {
      throw Exception('Could not launch $url');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.lock_outline, size: 80, color: Colors.red),
              const SizedBox(height: 24),
              const Text(
                'Subscription Required',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),
              const Text(
                'To access the Anti-Lust Guardian, you must have an active subscription. This is for your own commitment.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey, fontSize: 16),
              ),
              const SizedBox(height: 40),
              ElevatedButton(
                onPressed: _launchPaymentUrl,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                ),
                child: const Text(
                  'Subscribe Now',
                  style: TextStyle(fontSize: 18, color: Colors.white),
                ),
              ),
              const SizedBox(height: 20),
              TextButton(
                onPressed: () {
                  // In a real app, you might want a "Refresh Status" button here
                  // to re-check subscription after they pay.
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Please restart the app after subscribing.')),
                  );
                },
                child: const Text('I have subscribed', style: TextStyle(color: Colors.white70)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
