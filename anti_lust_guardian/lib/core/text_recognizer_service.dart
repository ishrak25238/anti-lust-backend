import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';
import 'package:flutter/foundation.dart';

class TextRecognizerService {
  final TextRecognizer _textRecognizer = TextRecognizer(script: TextRecognitionScript.latin);
  List<String> _blockedKeywords = [];

  TextRecognizerService() {
    _loadThreatList();
  }

  Future<void> _loadThreatList() async {
    try {
      final String response = await rootBundle.loadString('assets/threat_list.json');
      final data = json.decode(response);
      if (data['keywords'] != null) {
        _blockedKeywords = List<String>.from(data['keywords']);
      }
    } catch (e) {
      debugPrint('Error loading threat list for OCR: $e');
    }
  }

  Future<bool> scanAndDetect(InputImage inputImage) async {
    try {
      final RecognizedText recognizedText = await _textRecognizer.processImage(inputImage);
      String fullText = recognizedText.text.toLowerCase();

      for (String keyword in _blockedKeywords) {
        if (fullText.contains(keyword.toLowerCase())) {
          return true; // Threat detected
        }
      }
      return false;
    } catch (e) {
      debugPrint('OCR Error: $e');
      return false;
    }
  }

  Future<String> extractText(InputImage inputImage) async {
    try {
      final RecognizedText recognizedText = await _textRecognizer.processImage(inputImage);
      return recognizedText.text;
    } catch (e) {
      return 'Error extracting text: $e';
    }
  }

  void dispose() {
    _textRecognizer.close();
  }
}
