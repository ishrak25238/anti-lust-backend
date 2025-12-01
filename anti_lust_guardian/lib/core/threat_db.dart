
import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class ThreatDb {
  static final ThreatDb _instance = ThreatDb._internal();
  factory ThreatDb() => _instance;
  ThreatDb._internal();

  List<String> _blockedUrls = [];
  List<String> _blockedKeywords = [];

  List<String> get blockedUrls => _blockedUrls;
  List<String> get blockedKeywords => _blockedKeywords;

  Future<void> init() async {
    try {
      final String response = await rootBundle.loadString('assets/threat_list.json');
      final data = await json.decode(response);
      _blockedUrls = List<String>.from(data['urls']);
      _blockedKeywords = List<String>.from(data['keywords']);
    } catch (e) {
      // Error loading threat database
    }
  }
}
