"""
Real ML Core - Using NudeNet ONNX Model for Images + Keyword-based Text
Best accuracy for NSFW images, simple keyword matching for text
NO TensorFlow dependencies = NO conflicts
"""
import logging
import numpy as np
from typing import Optional, Dict, Tuple, Any, List
from PIL import Image
import io
import os
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RealMLCore")


class RealNSFWImageClassifier:
    """
    Real NSFW image classifier using NudeNet 640m ONNX model.
    This is the BEST model for NSFW detection with 99%+ accuracy.
    """
    def __init__(self):
        try:
            import onnxruntime as ort
            import cv2
            
            model_path = os.path.join(os.path.dirname(__file__), '../data/models/640m.onnx')
            model_path = os.path.abspath(model_path)
            logger.info(f"Loading NudeNet 640m ONNX model from {model_path}...")
            
            # Create ONNX inference session
            self.session = ort.InferenceSession(
                model_path,
                providers=['CPUExecutionProvider']
            )
            
            # Get model input details
            self.input_name = self.session.get_inputs()[0].name
            self.input_shape = self.session.get_inputs()[0].shape
            
            # NSFW class labels for NudeNet
            self.labels = [
                'FEMALE_GENITALIA_EXPOSED',
                'FEMALE_BREAST_EXPOSED', 
                'BUTTOCKS_EXPOSED',
                'ANUS_EXPOSED',
                'MALE_GENITALIA_EXPOSED'
            ]
            
            logger.info("[OK] NudeNet 640m model loaded successfully (BEST accuracy)")
        except Exception as e:
            logger.error(f"Failed to load NudeNet model: {e}")
            logger.info("Make sure 640m.onnx is in data/models/ directory")
            raise

    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """Preprocess image for NudeNet model"""
        import cv2
        
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Resize to model input size (640x640 for 640m model)
        img = cv2.resize(img, (640, 640))
        
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Normalize to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Transpose to (C, H, W) format
        img = np.transpose(img, (2, 0, 1))
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img

    def predict(self, image_bytes: bytes) -> float:
        """
        Returns NSFW probability (0.0 = safe, 1.0 = NSFW)
        """
        try:
            # Preprocess image
            input_data = self.preprocess_image(image_bytes)
            
            # Run inference
            outputs = self.session.run(None, {self.input_name: input_data})
            
            # Get detections (boxes, scores, classes)
            boxes = outputs[0]  # Bounding boxes
            scores = outputs[1]  # Confidence scores
            classes = outputs[2]  # Class indices
            
            # Check if any NSFW content detected with high confidence
            nsfw_score = 0.0
            threshold = 0.3  # Detection threshold
            
            if len(scores) > 0 and len(scores[0]) > 0:
                for i, score in enumerate(scores[0]):
                    if score > threshold:
                        # Any detection above threshold indicates NSFW
                        nsfw_score = max(nsfw_score, float(score))
            
            return nsfw_score
            
        except Exception as e:
            logger.error(f"Image prediction error: {e}")
            return 0.0


class SimpleTextToxicityClassifier:
    """
    Simple keyword-based text toxicity classifier.
    Fast, no external dependencies, works immediately.
    """
    def __init__(self):
        # Comprehensive toxic keyword list
        self.toxic_keywords = {
            'fuck', 'shit', 'damn', 'hell', 'ass', 'bitch', 'bastard', 'cunt',
            'dick', 'cock', 'pussy', 'whore', 'slut', 'fag', 'nigger', 'retard',
            'idiot', 'stupid', 'moron', 'imbecile', 'kill', 'die', 'hate', 'destroy',
            'porn', 'sex', 'xxx', 'nsfw', 'nude', 'naked', 'explicit', 'hentai'
        }
        logger.info(f"[OK] Simple text classifier loaded ({len(self.toxic_keywords)} keywords)")
    
    def predict(self, text: str) -> float:
        """
        Returns toxicity probability (0.0 = safe, 1.0 = toxic)
        """
        try:
            text_lower = text.lower()
            
            # Count toxic keywords
            matches = 0
            for keyword in self.toxic_keywords:
                # Use word boundaries to avoid partial matches
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    matches += 1
            
            # Convert to score (cap at 1.0)
            score = min(1.0, matches * 0.3)
            
            return score
                
        except Exception as e:
            logger.error(f"Text prediction error: {e}")
            return 0.0


class EnsembleVoter:
    """
    Weighted voting mechanism for multi-modal analysis.
    """
    def __init__(self):
        self.weights = {
            'vision': 0.5,
            'audio': 0.2,
            'text': 0.3,
            'metadata': 0.1
        }

    def vote(self, scores: Dict[str, float]) -> Tuple[float, float]:
        """
        Returns (weighted_score, uncertainty).
        """
        total_weight = 0.0
        weighted_sum = 0.0
        variances = []

        for modality, score in scores.items():
            if modality in self.weights:
                w = self.weights[modality]
                weighted_sum += score * w
                total_weight += w
                variances.append(score)

        if total_weight == 0:
            return 0.0, 1.0

        final_score = weighted_sum / total_weight
        
        if len(variances) > 1:
            variance = np.var(variances)
            uncertainty = min(1.0, variance * 2)
        else:
            uncertainty = 0.1

        return final_score, uncertainty


class ModelFactory:
    """
    Factory for creating and loading REAL pre-trained models.
    """
    _instances = {}

    @staticmethod
    def get_vision_model() -> RealNSFWImageClassifier:
        if 'vision' not in ModelFactory._instances:
            model = RealNSFWImageClassifier()
            ModelFactory._instances['vision'] = model
        return ModelFactory._instances['vision']

    @staticmethod
    def get_text_model() -> SimpleTextToxicityClassifier:
        if 'text' not in ModelFactory._instances:
            model = SimpleTextToxicityClassifier()
            ModelFactory._instances['text'] = model
        return ModelFactory._instances['text']


class RealMLCore:
    """
    Main entry point for Real ML operations.
    Orchestrates Vision and Text analysis.
    """
    def __init__(self):
        self.vision_model = ModelFactory.get_vision_model()
        self.text_model = ModelFactory.get_text_model()
        self.voter = EnsembleVoter()
        logger.info("RealMLCore Orchestrator initialized")

    def analyze_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes content (image, text, etc.) and returns threat assessment.
        """
        scores = {}
        
        if 'image_bytes' in content and content['image_bytes']:
            try:
                scores['vision'] = self.vision_model.predict(content['image_bytes'])
            except Exception as e:
                logger.error(f"Vision analysis failed: {e}")
                scores['vision'] = 0.0

        if 'text' in content and content['text']:
            try:
                scores['text'] = self.text_model.predict(content['text'])
            except Exception as e:
                logger.error(f"Text analysis failed: {e}")
                scores['text'] = 0.0

        final_score, uncertainty = self.voter.vote(scores)
        
        return {
            'is_threat': final_score > 0.7,
            'threat_score': final_score,
            'uncertainty': uncertainty,
            'details': scores
        }
