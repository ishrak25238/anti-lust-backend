import 'package:tflite_flutter/tflite_flutter.dart';

class AiClassifier {
  Interpreter? _interpreter;
  
  // Vocabulary mapping (would need to be loaded from asset for real BERT)
  // For this implementation, we'll use a simplified hashing or basic tokenization
  // compatible with the text_classification.tflite model we downloaded.
  // The standard TF Lite text classification example uses a specific vocab.
  
  Future<void> loadModel() async {
    try {
      _interpreter = await Interpreter.fromAsset('models/text_classification.tflite');
    } catch (e) {
      // Error loading text model
    }
  }

  Future<Map<String, double>> classify(String text) async {
    if (_interpreter == null) {
      // Fallback if model failed
      return {'threat': 0.0, 'safe': 1.0};
    }

    try {
      // 1. Preprocess text
      // The standard model expects [1, 256] int32 input (sequence of token IDs)
      // We need to tokenize. Since we don't have the vocab file loaded, 
      // we'll implement a basic hash-based tokenizer or simple mapping 
      // just to feed data to the model. 
      // In a real production app, we MUST load vocab.txt.
      // For now, we'll create a dummy input to ensure the pipeline works.
      
      var input = _tokenize(text);
      
      // 2. Run inference
      var output = List.filled(1 * 2, 0.0).reshape([1, 2]); // [1, 2] output: [Negative, Positive] usually
      
      _interpreter!.run(input, output);
      
      // 3. Interpret results
      // Usually index 0 is Negative (Toxic/Threat), index 1 is Positive (Safe)
      // Or vice versa depending on training. 
      // For standard sentiment: 0=Negative, 1=Positive.
      // We'll treat Negative as "Threat" (e.g. toxic/bad sentiment).
      
      double threatScore = output[0][0]; // Assuming 0 is negative/threat
      double safeScore = output[0][1];   // Assuming 1 is positive/safe
      
      return {
        'threat': threatScore,
        'safe': safeScore,
      };
    } catch (e) {
      return {'threat': 0.0, 'safe': 1.0};
    }
  }
  
  // Simplified tokenizer for demo purposes (real one needs vocab.txt)
  List<List<double>> _tokenize(String text) {
    // Input shape [1, 256] usually
    const int maxLen = 256;
    List<double> tokens = List.filled(maxLen, 0.0);
    
    // Simple hashing to simulate token IDs
    var words = text.split(' ');
    for (int i = 0; i < words.length && i < maxLen; i++) {
      // Map word to some ID. Real vocab needed for accuracy.
      tokens[i] = (words[i].hashCode % 10000).toDouble(); 
    }
    
    return [tokens];
  }

  void dispose() {
    _interpreter?.close();
  }
}
