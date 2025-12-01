class AiThreatPrediction {
  static const String mlApiKey = 'MKO4K06joZ9HVaG-znFkW3S_22wvUFsIevu6hyYHjEk';
  
  final List<String> _suspiciousKeywords = [
    'free', 'hack', 'crack', 'xxx', 'porn', 'adult', 'dating', 'gambling',
    'win', 'prize', 'click', 'offer', 'limited', 'sexy', 'nude'
  ];

  Future<double> predictThreat(String url) async {
    final lowerUrl = url.toLowerCase();
    
    double score = 0.0;

    for (final keyword in _suspiciousKeywords) {
      if (lowerUrl.contains(keyword)) {
        score += 0.3;
      }
    }

    if (lowerUrl.endsWith('.xyz') || lowerUrl.endsWith('.top') || lowerUrl.endsWith('.info')) {
      score += 0.2;
    }

    if (score > 1.0) score = 1.0;

    return score;
  }
}

