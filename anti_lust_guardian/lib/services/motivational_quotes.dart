import 'package:flutter_tts/flutter_tts.dart';

/// Motivational quotes service for encouraging users
class MotivationalQuotesService {
  final FlutterTts _tts = FlutterTts();
  
  // Curated motivational quotes for recovery
  static const List<String> quotes = [
    "You are stronger than your urges. One day at a time.",
    "Every moment of resistance is a victory.",
    "Your future self will thank you for staying strong today.",
    "True strength is choosing discipline over desire.",
    "You're not alone in this journey. Keep fighting.",
    "The pain of discipline is nothing compared to the pain of regret.",
    "Your mind is powerful. You control it, not the other way around.",
    "Progress, not perfection. Keep moving forward.",
    "You deserve better than fleeting pleasure. Choose lasting fulfillment.",
    "Champions are made when nobody is watching. Stay strong.",
    "Your streak is precious. Don't throw it away for temporary pleasure.",
    "Remember why you started. Your goals are worth it.",
    "Relapse is not failure. Getting back up is what matters.",
    "You are reclaiming your power. Don't give it away.",
    "This urge will pass. You are in control.",
    "Think about who you want to become. Act like that person now.",
    "Your brain is healing. Give it time and patience.",
    "Today's decision shapes tomorrow's reality.",
    "You're rewriting your story. Make it a good one.",
    "Freedom is on the other side of resistance."
  ];

  String getRandomQuote() {
    final index = DateTime.now().millisecondsSinceEpoch % quotes.length;
    return quotes[index];
  }

  Future<void> speakQuote(String quote) async {
    try {
      await _tts.setLanguage("en-US");
      await _tts.setSpeechRate(0.5);
      await _tts.setVolume(1.0);
      await _tts.setPitch(1.0);
      await _tts.speak(quote);
    } catch (e) {
      // TTS not available
    }
  }

  Future<void> speakAndShowQuote() async {
    final quote = getRandomQuote();
    await speakQuote(quote);
  }

  void dispose() {
    _tts.stop();
  }
}
