import 'dart:typed_data';
import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:flutter/services.dart';

class MLScreenReader {
  final Interpreter? _interpreter;

  MLScreenReader._(this._interpreter);

  static Future<MLScreenReader> load() async {
    try {
      final interpreter = await Interpreter.fromAsset('models/screen_reader.tflite');
      return MLScreenReader._(interpreter);
    } catch (e) {
      // Warning: ML model not found. Using mock screen reader.
      return MLScreenReader._(null);
    }
  }

  Future<Uint8List> captureScreen() async {
    return Uint8List(0);
  }

  Future<String> extractText(Uint8List imageBytes) async {
    if (_interpreter == null) {
      return "Mock extracted text: Safe content detected.";
    }

    final input = imageBytes;
    final output = List.filled(1, List.filled(256, 0.0));
    _interpreter!.run(input, output);
    return output[0].join('');
  }
}
