import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'cosmic_theme.dart';
import '../core/legal_terms.dart';

class ConsentScreen extends StatefulWidget {
  final Widget nextScreen;

  const ConsentScreen({super.key, required this.nextScreen});

  @override
  _ConsentScreenState createState() => _ConsentScreenState();
}

class _ConsentScreenState extends State<ConsentScreen> {
  final _storage = const FlutterSecureStorage();
  final ScrollController _scrollController = ScrollController();
  bool _hasScrolledToBottom = false;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
  }

  @override
  void dispose() {
    _scrollController.removeListener(_onScroll);
    _scrollController.dispose();
    super.dispose();
  }

  void _onScroll() {
    if (_scrollController.position.pixels >= _scrollController.position.maxScrollExtent - 50) {
      if (!_hasScrolledToBottom) {
        setState(() {
          _hasScrolledToBottom = true;
        });
      }
    }
  }

  Future<void> _accept() async {
    if (!_hasScrolledToBottom) return;
    await _storage.write(key: 'user_consent', value: 'true');
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => widget.nextScreen),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CosmicTheme.deepSpace,
      body: SafeArea(
        child: Container(
          padding: const EdgeInsets.all(24),
          child: Column(
            children: [
              const SizedBox(height: 20),
              Text(
                'LEGAL AGREEMENT',
                style: CosmicTheme.headerStyle.copyWith(
                  color: CosmicTheme.neonCyan,
                  fontSize: 24,
                ),
              ),
              const SizedBox(height: 20),
              Container(
                height: 2,
                width: double.infinity,
                decoration: const BoxDecoration(
                  gradient: CosmicTheme.primaryGradient,
                ),
              ),
              const SizedBox(height: 20),
              Expanded(
                child: Container(
                  decoration: BoxDecoration(
                    color: CosmicTheme.voidBlack.withOpacity(0.5),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: CosmicTheme.plasmaPurple.withOpacity(0.3)),
                  ),
                  padding: const EdgeInsets.all(16),
                  child: Scrollbar(
                    controller: _scrollController,
                    thumbVisibility: true,
                    child: SingleChildScrollView(
                      controller: _scrollController,
                      child: Text(
                        LegalTerms.termsAndConditions,
                        style: CosmicTheme.bodyStyle.copyWith(fontSize: 14),
                        textAlign: TextAlign.left,
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 20),
              if (!_hasScrolledToBottom)
                Text(
                  'Please scroll to the bottom to accept.',
                  style: CosmicTheme.hudStyle.copyWith(color: CosmicTheme.alertRed),
                ),
              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _hasScrolledToBottom ? _accept : null,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: _hasScrolledToBottom 
                        ? CosmicTheme.neonCyan.withOpacity(0.2) 
                        : Colors.grey.withOpacity(0.1),
                    side: BorderSide(
                        color: _hasScrolledToBottom ? CosmicTheme.neonCyan : Colors.grey),
                  ),
                  child: Text(
                    'I AGREE & ACCEPT',
                    style: CosmicTheme.hudStyle.copyWith(
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                        color: _hasScrolledToBottom ? CosmicTheme.neonCyan : Colors.grey),
                  ),
                ),
              ),
              const SizedBox(height: 10),
              TextButton(
                onPressed: () {
                },
                child: Text(
                  'DECLINE & EXIT',
                  style: CosmicTheme.hudStyle.copyWith(color: CosmicTheme.alertRed),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
