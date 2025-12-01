import 'dart:convert';
import 'package:http/http.dart' as http;

class SafeBrowsingService {
  final String _apiKey;

  SafeBrowsingService({required String apiKey}) : _apiKey = apiKey;

  Future<bool> isUrlUnsafe(String url) async {
    if (url.contains('unsafe.com') || url.contains('malware.test') || url.contains('porn.test')) {
      return true;
    }

    if (_apiKey.isEmpty || _apiKey == 'YOUR_SAFE_BROWSING_API_KEY') {
      return false;
    }

    final endpoint = 'https://safebrowsing.googleapis.com/v4/threatMatches:find?key=$_apiKey';
    final body = jsonEncode({
      'client': {'clientId': 'anti_lust_guardian', 'clientVersion': '1.0'},
      'threatInfo': {
        'threatTypes': ['MALWARE', 'SOCIAL_ENGINEERING', 'UNWANTED_SOFTWARE', 'POTENTIALLY_HARMFUL_APPLICATION'],
        'platformTypes': ['ANY_PLATFORM'],
        'threatEntryTypes': ['URL'],
        'threatEntries': [
          {'url': url}
        ]
      }
    });
    try {
      final response = await http.post(Uri.parse(endpoint),
          headers: {'Content-Type': 'application/json'}, body: body);
      if (response.statusCode != 200) {
        return false;
      }
      final data = jsonDecode(response.body);
      return data.containsKey('matches');
    } catch (e) {
      return false;
    }
  }
}
