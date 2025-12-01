import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import torch
import numpy as np
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.ml_service import MLService, ThreatLevel, PredictionResult, EnsemblePrediction

class TestMLService(unittest.TestCase):
    def setUp(self):
        self.ml_service = MLService()
        self.ml_service.nsfw.clip_model = MagicMock()
        self.ml_service.nsfw.clip_processor = MagicMock()
        self.ml_service.nsfw.resnet_model = MagicMock()
        self.ml_service.nsfw.efficientnet_model = MagicMock()
        self.ml_service.text.classifiers = []
        
    def test_initialization(self):
        self.assertFalse(self.ml_service.is_loaded())
        self.assertIsNotNone(self.ml_service.nsfw)
        self.assertIsNotNone(self.ml_service.text)
        self.assertIsNotNone(self.ml_service.url)
        self.assertIsNotNone(self.ml_service.temporal)
        self.assertIsNotNone(self.ml_service.monitor)

    def test_url_analysis(self):
        safe_url = "https://google.com"
        score = self.ml_service.analyze_url(safe_url)
        self.assertLess(score, 0.5)
        
        blocked_url = "https://pornhub.com"
        score = self.ml_service.analyze_url(blocked_url)
        self.assertGreater(score, 0.9)
        
        suspicious_url = "https://example.com/free-download-crack"
        score = self.ml_service.analyze_url(suspicious_url)
        self.assertGreater(score, 0.2)

    @patch('services.ml_service.NSFWDetector.predict')
    def test_nsfw_detection(self, mock_predict):
        mock_result = EnsemblePrediction(
            final_confidence=0.95,
            final_threat_level=ThreatLevel.CRITICAL,
            individual_predictions=[],
            consensus_score=1.0,
            processing_time_ms=100
        )
        mock_predict.return_value = mock_result
        
        dummy_image = "base64string"
        score = self.ml_service.detect_nsfw(dummy_image)
        self.assertEqual(score, 0.95)
        
        self.assertEqual(len(self.ml_service.temporal.history), 1)
        self.assertEqual(self.ml_service.temporal.history[0]['type'], 'nsfw')

    @patch('services.ml_service.TextClassifier.predict')
    def test_text_classification(self, mock_predict):
        mock_result = EnsemblePrediction(
            final_confidence=0.8,
            final_threat_level=ThreatLevel.HIGH,
            individual_predictions=[],
            consensus_score=0.9,
            processing_time_ms=50
        )
        mock_predict.return_value = mock_result
        
        text = "This is a bad text"
        result = self.ml_service.classify_text(text)
        self.assertTrue(result['is_harmful'])
        self.assertEqual(result['confidence'], 0.8)
        self.assertEqual(result['classification'], 'HIGH')

    def test_performance_monitor(self):
        self.ml_service.monitor.record(100, True, "TestModel", 0.5)
        stats = self.ml_service.get_performance()
        self.assertEqual(stats['requests']['total'], 1)
        self.assertEqual(stats['requests']['success'], 1)
        self.assertEqual(stats['latency']['mean_ms'], 100)

if __name__ == '__main__':
    unittest.main()
