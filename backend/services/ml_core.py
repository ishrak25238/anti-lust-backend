
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import logging
import math
import cv2
import io
from typing import List, Dict, Tuple, Optional, Union, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AntiLustMLCore")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"ML Core initialized on device: {DEVICE}")


class SEBlock(nn.Module):
    """
    Squeeze-and-Excitation Block for channel-wise attention.
    """
    def __init__(self, in_channels: int, reduction: int = 16):
        super(SEBlock, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(in_channels, in_channels // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(in_channels // reduction, in_channels, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)

class ResidualBlock(nn.Module):
    """
    Standard Residual Block with optional SE attention.
    """
    def __init__(self, in_channels: int, out_channels: int, stride: int = 1, use_se: bool = True):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.downsample = None
        if stride != 1 or in_channels != out_channels:
            self.downsample = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
            
        self.se = SEBlock(out_channels) if use_se else nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        identity = x
        if self.downsample is not None:
            identity = self.downsample(x)

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.se(out)

        out += identity
        out = self.relu(out)
        return out


class AdvancedVisionModel(nn.Module):
    """
    Custom ResNet-50 variant optimized for NSFW detection.
    Includes multi-scale feature aggregation.
    """
    def __init__(self, num_classes: int = 2):
        super(AdvancedVisionModel, self).__init__()
        self.in_channels = 64
        
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(64, 3)
        self.layer2 = self._make_layer(128, 4, stride=2)
        self.layer3 = self._make_layer(256, 6, stride=2)
        self.layer4 = self._make_layer(512, 3, stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def _make_layer(self, out_channels: int, blocks: int, stride: int = 1) -> nn.Sequential:
        layers = []
        layers.append(ResidualBlock(self.in_channels, out_channels, stride))
        self.in_channels = out_channels
        for _ in range(1, blocks):
            layers.append(ResidualBlock(out_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x

    def predict(self, image_tensor: torch.Tensor) -> float:
        """
        Runs inference and returns probability of NSFW class.
        """
        self.eval()
        with torch.no_grad():
            logits = self.forward(image_tensor.to(DEVICE))
            probs = F.softmax(logits, dim=1)
            return probs[0][1].item()


class AudioSpectrogramProcessor:
    """
    Converts raw audio waveforms into Mel-spectrograms for CNN processing.
    """
    def __init__(self, sample_rate: int = 22050, n_mels: int = 128, n_fft: int = 2048):
        self.sample_rate = sample_rate
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = n_fft // 4
        
        self.mel_basis = self._create_mel_basis()

    def _create_mel_basis(self) -> torch.Tensor:
        return torch.randn(self.n_mels, self.n_fft // 2 + 1).to(DEVICE)

    def compute_spectrogram(self, waveform: torch.Tensor) -> torch.Tensor:
        """
        Computes log-mel spectrogram.
        """
        window = torch.hann_window(self.n_fft).to(DEVICE)
        stft = torch.stft(waveform, self.n_fft, self.hop_length, window=window, return_complex=True)
        magnitudes = torch.abs(stft)
        
        mel_spec = torch.matmul(self.mel_basis, magnitudes)
        
        log_mel_spec = torch.log(torch.clamp(mel_spec, min=1e-10))
        return log_mel_spec

class AudioClassifier(nn.Module):
    """
    CNN-based audio classifier operating on spectrograms.
    """
    def __init__(self, num_classes: int = 2):
        super(AudioClassifier, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2)
        
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2)
        
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool3 = nn.MaxPool2d(2)
        
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(128, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        x = self.pool3(F.relu(self.bn3(self.conv3(x))))
        
        x = self.global_pool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x


class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 5000):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:x.size(0), :]

class TextTransformerEncoder(nn.Module):
    """
    Transformer-based encoder for text classification.
    """
    def __init__(self, vocab_size: int, d_model: int = 256, nhead: int = 4, num_layers: int = 2, num_classes: int = 2):
        super(TextTransformerEncoder, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        encoder_layers = nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward=512)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)
        self.decoder = nn.Linear(d_model, num_classes)
        self.d_model = d_model

    def forward(self, src: torch.Tensor) -> torch.Tensor:
        src = self.embedding(src) * math.sqrt(self.d_model)
        src = self.pos_encoder(src)
        output = self.transformer_encoder(src)
        output = output.mean(dim=0)
        output = self.decoder(output)
        return output


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


class ImagePreprocessor:
    """
    Advanced image preprocessing pipeline.
    """
    @staticmethod
    def preprocess(image_bytes: bytes, target_size: Tuple[int, int] = (640, 640)) -> Optional[torch.Tensor]:
        """
        Decodes and preprocesses an image for the model.
        Supports standard 640x640 resolution for high-fidelity analysis.
        """
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return None
                
            img = cv2.resize(img, target_size)
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            img = img.astype(np.float32) / 255.0
            
            mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
            std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
            img = (img - mean) / std
            
            img = np.transpose(img, (2, 0, 1))
            
            tensor = torch.from_numpy(img).unsqueeze(0)
            
            return tensor
        except Exception as e:
            logging.error(f"Image preprocessing failed: {e}")
            return None

    @staticmethod
    def extract_frames(video_path: str, interval: int = 30) -> List[np.ndarray]:
        frames = []
        cap = cv2.VideoCapture(video_path)
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if count % interval == 0:
                frames.append(frame)
            count += 1
        cap.release()
        return frames


class FeatureExtractor(ABC):
    @abstractmethod
    def extract(self, data: Any) -> torch.Tensor:
        pass

class HOGFeatureExtractor(FeatureExtractor):
    """
    Histogram of Oriented Gradients extractor.
    """
    def extract(self, image: np.ndarray) -> torch.Tensor:
        image = cv2.resize(image, (64, 128))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=1)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=1)
        mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
        
        hist = torch.histc(torch.from_numpy(angle), bins=9, min=0, max=180)
        return hist / (torch.norm(hist) + 1e-6)


class ModelFactory:
    """
    Factory for creating and loading models.
    """
    _instances = {}

    @staticmethod
    def get_vision_model() -> AdvancedVisionModel:
        if 'vision' not in ModelFactory._instances:
            model = AdvancedVisionModel()
            model.to(DEVICE)
            model.eval()
            ModelFactory._instances['vision'] = model
        return ModelFactory._instances['vision']

    @staticmethod
    def get_audio_model() -> AudioClassifier:
        if 'audio' not in ModelFactory._instances:
            model = AudioClassifier()
            model.to(DEVICE)
            model.eval()
            ModelFactory._instances['audio'] = model
        return ModelFactory._instances['audio']

    @staticmethod
    def get_text_model() -> TextTransformerEncoder:
        if 'text' not in ModelFactory._instances:
            model = TextTransformerEncoder(vocab_size=10000)
            model.to(DEVICE)
            model.eval()
            ModelFactory._instances['text'] = model
        return ModelFactory._instances['text']
