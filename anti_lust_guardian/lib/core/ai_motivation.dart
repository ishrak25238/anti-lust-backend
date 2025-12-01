import 'dart:math';

class AiMotivation {
  final Random _random = Random();

  final List<String> _earlyStageQuotes = [
    "The journey of a thousand miles begins with a single step.",
    "Don't watch the clock; do what it does. Keep going.",
    "You are stronger than you think.",
    "Every moment is a fresh beginning.",
    "Believe you can and you're halfway there."
  ];

  final List<String> _midStageQuotes = [
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "Hardships often prepare ordinary people for an extraordinary destiny.",
    "It always seems impossible until it's done.",
    "Your discipline is paying off. Keep pushing.",
    "You are building a new version of yourself."
  ];

  final List<String> _advancedStageQuotes = [
    "We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
    "The only way to do great work is to love what you do.",
    "You have mastered your impulses. Now master your destiny.",
    "Your strength is an inspiration to others.",
    "Limitless potential lies ahead."
  ];

  Future<String> getMotivation(int streakDays) async {
    await Future.delayed(const Duration(milliseconds: 500));

    List<String> pool;
    if (streakDays < 7) {
      pool = _earlyStageQuotes;
    } else if (streakDays < 30) {
      pool = _midStageQuotes;
    } else {
      pool = _advancedStageQuotes;
    }

    return pool[_random.nextInt(pool.length)];
  }
}
