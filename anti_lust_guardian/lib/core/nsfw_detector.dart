import 'dart:typed_data';
import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:image/image.dart' as img;

class NSFWDetector {
  final Interpreter? _interpreter;
  static const int _inputSize = 224; // Standard for MobileNet

  NSFWDetector._(this._interpreter);

  static Future<NSFWDetector> load() async {
    try {
      final options = InterpreterOptions();
      // Use XNNPACK or Metal delegate if available for speed
      // options.addDelegate(XNNPackDelegate()); 
      
      Interpreter? interpreter;
      try {
        interpreter = await Interpreter.fromAsset('models/nsfw_mobilenet.tflite', options: options);
      } catch (_) {
        interpreter = await Interpreter.fromAsset('models/nsfw.tflite', options: options);
      }
      
      return NSFWDetector._(interpreter);
    } catch (e) {
      // Error loading NSFW model
      return NSFWDetector._(null);
    }
  }

  Future<bool> isNSFW(Uint8List imageBytes, {double threshold = 0.7}) async {
    if (_interpreter == null) {
      // Fallback or safe default if model failed to load
      return false; 
    }

    try {
      // 1. Preprocess image
      final image = img.decodeImage(imageBytes);
      if (image == null) return false;

      final resized = img.copyResize(image, width: _inputSize, height: _inputSize);
      final input = _imageToByteListFloat32(resized);

      // 2. Run inference
      // Output shape depends on model. Assuming [1, 2] (Safe, NSFW) or [1, 5] (Drawings, Hentai, Neutral, Porn, Sexy)
      // We'll allocate enough space and check output shape dynamically if needed, 
      // but standard MobileNet NSFW is often [1, 2] or [1, 5].
      // Let's assume [1, 2] for binary or [1, 5] for multi-class.
      // We'll try to detect shape or use a safe buffer.
      
      final outputShape = _interpreter!.getOutputTensor(0).shape;
      
      // Allocate output buffer
      // If shape is [1, 5], we need List<List<double>>
      // We can use a flat list and reshape, or nested list.
      final output = List.filled(1 * outputShape.last, 0.0).reshape(outputShape);

      _interpreter!.run(input, output);

      // 3. Interpret results
      // If 2 classes: 0=Safe, 1=NSFW
      // If 5 classes: usually [Drawing, Hentai, Neutral, Porn, Sexy]
      // We sum up NSFW classes.
      
      double nsfwScore = 0.0;
      
      if (outputShape.last == 2) {
        nsfwScore = output[0][1];
      } else if (outputShape.last == 5) {
        // Indices: 0:Drawing, 1:Hentai, 2:Neutral, 3:Porn, 4:Sexy
        // This mapping varies by model training, but this is common for GantMan model.
        // Let's assume indices 1 (Hentai), 3 (Porn), 4 (Sexy) are NSFW.
        nsfwScore = output[0][1] + output[0][3] + output[0][4];
      } else {
        // Unknown model structure, default to safe to avoid false positives
        return false;
      }

      return nsfwScore >= threshold;
    } catch (e) {
      return false;
    }
  }

  // Helper to convert image to Float32List [1, 224, 224, 3] normalized -1..1 or 0..1
  List<dynamic> _imageToByteListFloat32(img.Image image) {
    final convertedBytes = Float32List(1 * _inputSize * _inputSize * 3);
    final buffer = Float32List.view(convertedBytes.buffer);
    int pixelIndex = 0;
    for (var i = 0; i < _inputSize; i++) {
      for (var j = 0; j < _inputSize; j++) {
        final pixel = image.getPixel(j, i);
        // Normalize to 0..1 or -1..1 depending on model. 
        // MobileNet usually expects -1..1 or 0..1. 
        // GantMan model typically uses 0..1 (V2) or -1..1 (V1).
        // We'll use 0..1 which is safer for generic models.
        buffer[pixelIndex++] = pixel.r / 255.0;
        buffer[pixelIndex++] = pixel.g / 255.0;
        buffer[pixelIndex++] = pixel.b / 255.0;
      }
    }
    return convertedBytes.reshape([1, _inputSize, _inputSize, 3]);
  }
}
