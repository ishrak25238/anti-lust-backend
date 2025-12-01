
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import '../core/payment_gate.dart';
import 'dashboard.dart';
import 'auth/login_screen.dart';
import 'auth/signup_screen.dart';

class PaywallScreen extends StatefulWidget {
  const PaywallScreen({super.key});

  @override
  _PaywallScreenState createState() => _PaywallScreenState();
}

enum SubscriptionPlan { monthly, yearly, lifetime }

class _PaywallScreenState extends State<PaywallScreen> {
  final PaymentGate _paymentGate = PaymentGate();
  SubscriptionPlan _selectedPlan = SubscriptionPlan.yearly;

  void _subscribe() async {
    try {
      String priceId;
      switch (_selectedPlan) {
        case SubscriptionPlan.monthly:
          priceId = dotenv.env['STRIPE_MONTHLY_PRICE_ID'] ?? '';
          break;
        case SubscriptionPlan.yearly:
          priceId = dotenv.env['STRIPE_YEARLY_PRICE_ID'] ?? '';
          break;
        case SubscriptionPlan.lifetime:
          priceId = dotenv.env['STRIPE_LIFETIME_PRICE_ID'] ?? '';
          break;
      }

      if (priceId.isEmpty) {
        throw Exception('Price ID not configured for selected plan');
      }

      await _paymentGate.startPayment(priceId: priceId);
      
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const DashboardScreen()),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Payment failed: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Unlock Your Guardian'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            const Text(
              'Choose Your Plan',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 30.0),
            _buildPlanSelector(
              plan: SubscriptionPlan.monthly,
              title: 'Monthly Plan',
              price: '\$4.99/month',
              subtitle: '7-day FREE trial',
              features: const [
                '✅ All core protection features',
                '✅ AI content filtering',
                '✅ URL monitoring & blocking',
                '✅ Parental controls',
                '✅ Streak tracking',
                '✅ Email support',
              ],
              isPopular: false,
            ),
            const SizedBox(height: 12.0),
            _buildPlanSelector(
              plan: SubscriptionPlan.yearly,
              title: 'Yearly Plan',
              price: '\$49.99/year',
              subtitle: 'Save \$10 - Best Value!',
              features: const [
                '✅ Everything in Monthly',
                '🎯 Priority email support',
                '📊 Annual progress report',
                '📥 Data export feature',
                '💰 Save \$10 per year',
              ],
              isPopular: true,
            ),
            const SizedBox(height: 12.0),
            _buildPlanSelector(
              plan: SubscriptionPlan.lifetime,
              title: 'Lifetime Access',
              price: '\$149.99 once',
              subtitle: 'Pay once, use forever',
              features: const [
                '✅ Everything in Yearly',
                '🚀 Premium priority support',
                '🔬 Research paper generator',
                '📈 Advanced analytics',
                '⚡ Early beta access',
                '♾️ Lifetime updates',
              ],
            ),
            const SizedBox(height: 40.0),
            ElevatedButton(
              onPressed: _subscribe,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16.0),
              ),
              child: const Text('Subscribe Now', style: TextStyle(fontSize: 18)),
            ),
            const SizedBox(height: 20.0),
            TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const LoginScreen()),
                );
              },
              child: const Text('Already have an account? Log In'),
            ),
            TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const SignUpScreen()),
                );
              },
              child: const Text('New user? Sign Up'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPlanSelector({
    required SubscriptionPlan plan,
    required String title,
    required String price,
    String? subtitle,
    List<String> features = const [],
    bool isPopular = false,
  }) {
    final bool isSelected = _selectedPlan == plan;
    return GestureDetector(
      onTap: () {
        setState(() {
          _selectedPlan = plan;
        });
      },
      child: Container(
        padding: const EdgeInsets.all(16.0),
        decoration: BoxDecoration(
          color: isSelected ? Colors.blue.withOpacity(0.1) : Colors.grey[200],
          borderRadius: BorderRadius.circular(8.0),
          border: Border.all(
            color: isSelected ? Colors.blue : Colors.transparent,
            width: 2.0,
          ),
        ),
        child: Stack(
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(fontSize: 18.0, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 5.0),
                Text(
                  price,
                  style: const TextStyle(fontSize: 16.0, fontWeight: FontWeight.w600),
                ),
                if (subtitle != null) ...[
                  const SizedBox(height: 3.0),
                  Text(
                    subtitle,
                    style: TextStyle(fontSize: 14.0, color: Colors.grey[600]),
                  ),
                ],
                if (features.isNotEmpty) ...[
                  const SizedBox(height: 12.0),
                  const Divider(height: 1),
                  const SizedBox(height: 8.0),
                  ...features.map((feature) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 2.0),
                    child: Text(
                      feature,
                      style: const TextStyle(fontSize: 13.0, height: 1.4),
                    ),
                  )),
                ],
              ],
            ),
            if (isPopular)
              Positioned(
                top: -8,
                right: -8,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
                  decoration: BoxDecoration(
                    color: Colors.green,
                    borderRadius: BorderRadius.circular(4.0),
                  ),
                  child: const Text(
                    'POPULAR',
                    style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
