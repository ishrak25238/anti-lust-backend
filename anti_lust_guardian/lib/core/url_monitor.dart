import 'ai_classifier.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:anti_lust_guardian/services/safe_browsing.dart';
import 'package:anti_lust_guardian/core/ai_threat_prediction.dart';
import 'package:anti_lust_guardian/core/privacy_service.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'threat_db.dart';
import 'threat_intelligence_service.dart';

class UrlMonitor {
  final ThreatDb _threatDb = ThreatDb();
  final AiClassifier _aiClassifier = AiClassifier();
  late final SafeBrowsingService _safeBrowsing;
  final AiThreatPrediction _aiThreatPrediction = AiThreatPrediction();
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  final PrivacyService _privacyService = PrivacyService();
  final ThreatIntelligenceService _threatService = ThreatIntelligenceService();

  Future<void> init() async {
    await _aiClassifier.loadModel();
    _safeBrowsing = SafeBrowsingService(apiKey: dotenv.env['GOOGLE_SAFE_BROWSING_API_KEY'] ?? '');
  }

  Future<bool> isThreat(String url) async {
    await _logUrl(url);
    bool isBlocked = false;
    String blockReason = '';

    if (_threatDb.blockedUrls.contains(url)) {
      isBlocked = true;
      blockReason = 'Known Malicious URL';
    } else {
      for (final keyword in _threatDb.blockedKeywords) {
        if (url.contains(keyword)) {
          isBlocked = true;
          blockReason = 'Blocked Keyword ($keyword)';
          break;
        }
      }
    }

    if (!isBlocked && await _safeBrowsing.isUrlUnsafe(url)) {
      isBlocked = true;
      blockReason = 'Google Safe Browsing';
    }

    /* 
    // BROKEN COMPONENT: Disabling until we have a real vocab.txt
    if (!isBlocked) {
      final classification = await _aiClassifier.classify(url);
      final threatScore = classification['threat'] ?? 0.0;
      if (threatScore > 0.8) {
        isBlocked = true;
        blockReason = 'AI Classifier (Score: $threatScore)';
      }
    }
    */

    if (!isBlocked) {
      final heuristicScore = await _aiThreatPrediction.predictThreat(url);
      if (heuristicScore > 0.7) {
        isBlocked = true;
        blockReason = 'Heuristic Threat Prediction';
      }
    }

    if (isBlocked) {
      await _threatService.logThreatEvent(
        source: url,
        reason: blockReason,
        context: 'UrlMonitor Block',
      );
      return true;
    }
    return false;
  }

  void dispose() {
    _aiClassifier.dispose();
  }

  Future<void> _logUrl(String url) async {
    if (await _privacyService.isIncognitoMode()) {
      return;
    }
    final timestamp = DateTime.now().toIso8601String();
    await _storage.write(key: 'log_$timestamp', value: url);
  }
}
