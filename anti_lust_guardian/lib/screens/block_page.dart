
import 'package:flutter/material.dart';
import '../ui/cosmic_theme.dart';
import '../ui/particle_background.dart';

class BlockPageScreen extends StatelessWidget {
  const BlockPageScreen({super.key});

  String _getRandomQuote() {
    const quotes = [
      "The only way to do great work is to love what you do. - Steve Jobs",
      "Discipline is choosing between what you want now and what you want most. - Abraham Lincoln",
      "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
      "Your future is created by what you do today, not tomorrow.",
      "Self-control is strength. Right thought is mastery. Calmness is power. - James Allen",
      "The pain of discipline is far less than the pain of regret.",
    ];
    return quotes[DateTime.now().microsecond % quotes.length];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CosmicTheme.deepSpace,
      body: ParticleBackground(
        child: Center(
          child: Container(
            padding: const EdgeInsets.all(32),
            margin: const EdgeInsets.symmetric(horizontal: 24),
            decoration: BoxDecoration(
              color: CosmicTheme.voidBlack.withOpacity(0.8),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: CosmicTheme.alertRed, width: 2),
              boxShadow: [
                BoxShadow(
                  color: CosmicTheme.alertRed.withOpacity(0.4),
                  blurRadius: 30,
                  spreadRadius: 5,
                ),
              ],
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(
                  Icons.gpp_bad,
                  size: 80,
                  color: CosmicTheme.alertRed,
                ),
                const SizedBox(height: 24),
                Text(
                  'ACCESS DENIED',
                  style: CosmicTheme.headerStyle.copyWith(
                    color: CosmicTheme.alertRed,
                    fontSize: 28,
                    shadows: [
                      const BoxShadow(
                        color: CosmicTheme.alertRed,
                        blurRadius: 10,
                        spreadRadius: 2,
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  _getRandomQuote(),
                  style: CosmicTheme.bodyStyle.copyWith(
                    fontStyle: FontStyle.italic,
                    fontSize: 16,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 32),
                ElevatedButton(
                  onPressed: () => Navigator.of(context).pop(),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: CosmicTheme.alertRed.withOpacity(0.2),
                    side: const BorderSide(color: CosmicTheme.alertRed),
                    padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                  ),
                  child: Text(
                    'RETURN TO SAFETY',
                    style: CosmicTheme.hudStyle.copyWith(
                      fontWeight: FontWeight.bold,
                      fontSize: 14,
                      color: CosmicTheme.starlightWhite,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
