import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:intl/intl.dart';
import 'dart:convert';
import 'research_generator.dart';

class ThreatIntelligenceService {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  final ResearchGenerator _researchGenerator = ResearchGenerator();
  
  static const String _forensicLogKey = 'forensic_logs';

  Future<void> logThreatEvent({
    required String source,
    required String reason,
    String context = 'Standard',
  }) async {
    final timestamp = DateFormat('yyyy-MM-dd HH:mm:ss').format(DateTime.now());
    
    final logEntry = {
      'timestamp': timestamp,
      'source': source,
      'reason': reason,
      'context': context,
      'action': 'BLOCKED',
    };

    await _appendLog(logEntry);
    
    // Threat Intelligence: Learned pattern from source

    if (reason.contains('Illegal') || reason.contains('Dark Web') || reason.contains('Child')) {
      await _researchGenerator.generateAndDispatchReport();
    }
  }

  Future<void> _appendLog(Map<String, dynamic> entry) async {
    final currentLogsStr = await _storage.read(key: _forensicLogKey);
    List<dynamic> logs = [];
    if (currentLogsStr != null) {
      try {
        logs = jsonDecode(currentLogsStr);
      } catch (e) {
        logs = [];
      }
    }
    logs.add(entry);
    await _storage.write(key: _forensicLogKey, value: jsonEncode(logs));
  }

  Future<List<Map<String, dynamic>>> getForensicLogs() async {
    final currentLogsStr = await _storage.read(key: _forensicLogKey);
    if (currentLogsStr == null) return [];
    try {
      final List<dynamic> decoded = jsonDecode(currentLogsStr);
      return decoded.cast<Map<String, dynamic>>();
    } catch (e) {
      return [];
    }
  }
}
