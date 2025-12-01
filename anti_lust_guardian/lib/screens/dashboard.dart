
import 'package:flutter/material.dart';
import '../core/url_monitor.dart';
import 'block_page.dart';
import 'focus_horizon.dart';
import 'package:image_picker/image_picker.dart';
import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';
import '../core/text_recognizer_service.dart';

import '../services/subscription_service.dart';
import 'pay_wall.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final UrlMonitor _urlMonitor = UrlMonitor();
  final TextRecognizerService _textRecognizerService = TextRecognizerService();
  final SubscriptionService _subscriptionService = SubscriptionService();
  final TextEditingController _urlController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _checkSubscription();
  }

  Future<void> _checkSubscription() async {
    // Check if user has active subscription
    final hasSub = await _subscriptionService.currentUserHasActiveSubscription();
    if (!hasSub) {
      if (!mounted) return;
      // Redirect to PayWall
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const PayWallScreen()),
      );
    }
  }

  final bool _isProtectionActive = true;
  final int _streak = 42;
  bool _isCheckingUrl = false;

  void _checkUrl() async {
    final url = _urlController.text.trim();
    if (url.isEmpty) {
      return;
    }

    setState(() {
      _isCheckingUrl = true;
    });

    final isThreat = await _urlMonitor.isThreat(url);

    setState(() {
      _isCheckingUrl = false;
    });

    if (isThreat) {
      if (!mounted) return;
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => const BlockPageScreen()),
      );
    } else {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('URL is safe!')),
      );
    }
  }

  Future<void> _testOcr() async {
    final ImagePicker picker = ImagePicker();
    final XFile? image = await picker.pickImage(source: ImageSource.gallery);
    
    if (image == null) return;

    final inputImage = InputImage.fromFilePath(image.path);
    final isThreat = await _textRecognizerService.scanAndDetect(inputImage);

    if (!mounted) return;

    if (isThreat) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('THREAT DETECTED in image!'), backgroundColor: Colors.red),
      );
    } else {
      final text = await _textRecognizerService.extractText(inputImage);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Safe. Extracted: ${text.length > 20 ? "${text.substring(0, 20)}..." : text}')),
      );
    }
  }

  @override
  void dispose() {
    _urlController.dispose();
    _textRecognizerService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'Protection Status: ${_isProtectionActive ? 'Active' : 'Inactive'}',
              style: TextStyle(
                fontSize: 20.0,
                color: _isProtectionActive ? Colors.green : Colors.red,
              ),
            ),
            const SizedBox(height: 20.0),
            Text(
              'Current Streak: $_streak days',
              style: const TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 40.0),
            TextField(
              controller: _urlController,
              decoration: const InputDecoration(
                labelText: 'Enter a URL to check',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 10.0),
            _isCheckingUrl
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _checkUrl,
                    child: const Text('Check URL'),
                  ),
            const SizedBox(height: 40.0),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const FocusHorizonScreen()),
                );
              },
              child: const Text('View Focus Horizon'),
            ),
            const SizedBox(height: 20.0),
            ElevatedButton(
              onPressed: _testOcr,
              style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
              child: const Text('Test Screen OCR (Pick Image)'),
            ),
          ],
        ),
      ),
    );
  }
}
