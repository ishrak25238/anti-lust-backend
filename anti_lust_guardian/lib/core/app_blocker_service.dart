import 'dart:async';
import 'package:flutter/services.dart';
import 'content_scraper.dart';
import 'dopamine_scheduler.dart';
import 'threat_intelligence_service.dart';

class AppBlockerService {
  final ContentScraper _scraper = ContentScraper();
  final DopamineScheduler _scheduler = DopamineScheduler();
  final ThreatIntelligenceService _threatService = ThreatIntelligenceService();
  
  final _interventionController = StreamController<String>.broadcast();
  Stream<String> get interventionStream => _interventionController.stream;

  Timer? _monitorTimer;
  bool _isRunning = false;

  void startMonitoring() {
    if (_isRunning) return;
    _isRunning = true;
    _monitorTimer = Timer.periodic(const Duration(seconds: 2), (timer) async {
      await _checkScreen();
    });
  }

  void stopMonitoring() {
    _monitorTimer?.cancel();
    _isRunning = false;
  }

  Future<void> _checkScreen() async {
    final isDetoxTime = await _scheduler.isScrollBlocked();
    
    final detectedKeywords = await _scraper.scanScreen();

    if (detectedKeywords.isEmpty) return;

    bool shouldBlock = false;
    String reason = '';

    for (final keyword in detectedKeywords) {
      if (_isAdultKeyword(keyword)) {
        shouldBlock = true;
        reason = 'Harmful content detected ($keyword).';
        break;
      }

      if (isDetoxTime && _isDopamineKeyword(keyword)) {
        shouldBlock = true;
        reason = 'Dopamine Detox Active. No scrolling allowed.';
        break;
      }
    }

    if (shouldBlock) {
      await _triggerBlock(reason, detectedKeywords.first);
    }
  }

  bool _isAdultKeyword(String keyword) {
    const adult = ['porn', 'xxx', 'nude', 'sex', 'adult', 'hentai', 'onlyfans'];
    return adult.contains(keyword.toLowerCase());
  }

  bool _isDopamineKeyword(String keyword) {
    const dopamine = ['reels', 'shorts', 'tiktok', 'foryou', 'trending', 'instagram', 'facebook'];
    return dopamine.contains(keyword.toLowerCase());
  }

  Future<void> _triggerBlock(String reason, String sourceKeyword) async {
    try {
      await SystemChannels.platform.invokeMethod('SystemNavigator.pop');
    } catch (e) {
      // Failed to close app
    }

    await _threatService.logThreatEvent(
      source: sourceKeyword,
      reason: reason,
      context: 'App Blocked via ContentScraper',
    );

    _interventionController.add(reason);
  }
}
