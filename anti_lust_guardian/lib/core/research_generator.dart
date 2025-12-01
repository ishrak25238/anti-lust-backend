import 'package:http/http.dart' as http;
import 'dart:convert';

class ResearchGenerator {
  static const String _backendUrl = 'http://localhost:8000';
  final String _deviceId;

  ResearchGenerator({String? deviceId}) 
    : _deviceId = deviceId ?? DateTime.now().millisecondsSinceEpoch.toString();

  Future<void> generateAndDispatchReport() async {
    // Generating forensic research report
    
    try {
      final response = await http.post(
        Uri.parse('$_backendUrl/api/research/generate-report'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'device_id': _deviceId}),
      );

      if (response.statusCode == 200) {
        // Research report sent successfully to backend
        // Email will be sent to ishrakarafneo@gmail.com
      } else {
        // Failed to send report
      }
    } catch (e) {
      // Backend connection failed
      // Make sure Python backend is running
    }
  }
}
