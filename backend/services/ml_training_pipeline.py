import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
import json
import pickle
from pathlib import Path
import hashlib
from datetime import datetime
import requests
from PIL import Image
import io
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class NSFWDatasetConfig:
    DATASETS = {
        'nsfw_data_scraper': {
            'url': 'https://github.com/alex000kim/nsfw_data_scraper',
            'classes': ['drawings', 'hentai', 'neutral', 'porn', 'sexy'],
            'samples': 50000
        },
        'nsfw_mobile': {
            'url': 'https://github.com/GantMan/nsfw_model',
            'classes': ['safe', 'nsfw'],
            'samples': 60000
        },
        'nudenet': {
            'url': 'https://github.com/notAI-tech/NudeNet',
            'classes': ['safe', 'unsafe'],
            'samples': 100000
        }
    }

class NSFWDataset(Dataset):
    def __init__(
        self,
        root_dir: str = './data/nsfw',
        dataset_name: str = 'nsfw_data_scraper',
        split: str = 'train',
        transform: Optional[Callable] = None,
        download: bool = True
    ):
        self.root_dir = Path(root_dir)
        self.dataset_name = dataset_name
        self.split = split
        self.transform = transform or self._default_transform()
        
        self.data_dir = self.root_dir / dataset_name / split
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        if download and not self._is_downloaded():
            logger.info(f"Downloading {dataset_name} dataset...")
            self._download_dataset()
        
        self.samples = self._load_samples()
        logger.info(f"Loaded {len(self.samples)} samples from {dataset_name} ({split})")
    
    def _default_transform(self):
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def _is_downloaded(self) -> bool:
        manifest_file = self.data_dir / 'manifest.json'
        return manifest_file.exists()
    
    def _download_dataset(self):
        logger.warning("Dataset download not implemented - using synthetic data for demo")
        self._create_synthetic_manifest()
    
    def _create_synthetic_manifest(self):
        config = NSFWDatasetConfig.DATASETS[self.dataset_name]
        classes = config['classes']
        samples_per_class = config['samples'] // len(classes)
        
        manifest = {
            'dataset': self.dataset_name,
            'split': self.split,
            'classes': classes,
            'samples': []
        }
        
        for class_idx, class_name in enumerate(classes):
            for i in range(samples_per_class):
                manifest['samples'].append({
                    'image_id': f"{class_name}_{i:05d}",
                    'class': class_name,
                    'class_idx': class_idx,
                    'path': f"{class_name}/{i:05d}.jpg"
                })
        
        manifest_file = self.data_dir / 'manifest.json'
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"Created manifest with {len(manifest['samples'])} samples")
    
    def _load_samples(self) -> List[Dict]:
        manifest_file = self.data_dir / 'manifest.json'
        with open(manifest_file, 'r') as f:
            manifest = json.load(f)
        return manifest['samples']
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        sample = self.samples[idx]
        
        image = self._load_or_generate_image(sample)
        
        if self.transform:
            image = self.transform(image)
        
        label = sample['class_idx']
        
        return image, label
    
    def _load_or_generate_image(self, sample: Dict) -> Image.Image:
        image_path = self.data_dir / sample['path']
        
        if image_path.exists():
            return Image.open(image_path).convert('RGB')
        else:
            return self._generate_synthetic_image(sample['class'])
    
    def _generate_synthetic_image(self, class_name: str) -> Image.Image:
        np.random.seed(hash(class_name) % 2**32)
        
        if 'safe' in class_name or 'neutral' in class_name:
            img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        else:
            skin_color = np.array([200, 160, 140])
            noise = np.random.randint(-30, 30, (224, 224, 3))
            img_array = np.clip(skin_color + noise, 0, 255).astype(np.uint8)
        
        return Image.fromarray(img_array)

class TextToxicityDataset(Dataset):
    def __init__(
        self,
        root_dir: str = './data/toxicity',
        dataset_name: str = 'toxic_comment',
        split: str = 'train',
        tokenizer: Optional[Any] = None,
        max_length: int = 512
    ):
        self.root_dir = Path(root_dir)
        self.dataset_name = dataset_name
        self.split = split
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        self.data_file = self.root_dir / f"{dataset_name}_{split}.json"
        
        if not self.data_file.exists():
            self._download_or_create_dataset()
        
        self.samples = self._load_samples()
        logger.info(f"Loaded {len(self.samples)} text samples ({split})")
    
    def _download_or_create_dataset(self):
        logger.warning("Using synthetic toxic comment dataset")
        
        toxic_templates = [
            "I hate {group}",
            "All {group} are {negative_adj}",
            "{group} should {violent_action}",
            "F*** {group}",
        ]
        
        safe_templates = [
            "I love spending time with {positive}",
            "Everyone deserves {positive}",
            "Let's work together on {topic}",
            "I appreciate {positive}",
        ]
        
        groups = ['people', 'them', 'you', 'this']
        negatives = ['stupid', 'terrible', 'awful', 'useless']
        violent = ['leave', 'stop', 'change']
        positives = ['respect', 'kindness', 'equality', 'friends']
        topics = ['this project', 'our goals', 'making things better']
        
        samples = []
        
        for template in toxic_templates:
            for group in groups:
                for neg in negatives:
                    for violent in ['leave', 'stop']:
                        text = template.format(
                            group=group,
                            negative_adj=neg,
                            violent_action=violent
                        )
                        samples.append({
                            'text': text,
                            'label': 1,
                            'toxicity_score': 0.9
                        })
        
        for template in safe_templates:
            for pos in positives:
                for topic in topics:
                    text = template.format(positive=pos, topic=topic)
                    samples.append({
                        'text': text,
                        'label': 0,
                        'toxicity_score': 0.1
                    })
        
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(samples, f, indent=2)
        
        logger.info(f"Created {len(samples)} synthetic text samples")
    
    def _load_samples(self) -> List[Dict]:
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Tuple[Dict, int]:
        sample = self.samples[idx]
        
        if self.tokenizer:
            encoded = self.tokenizer(
                sample['text'],
                max_length=self.max_length,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            return encoded, sample['label']
        else:
            return sample['text'], sample['label']

class URLPhishingDataset(Dataset):
    def __init__(
        self,
        root_dir: str = './data/urls',
        split: str = 'train'
    ):
        self.root_dir = Path(root_dir)
        self.split = split
        
        self.data_file = self.root_dir / f"urls_{split}.json"
        
        if not self.data_file.exists():
            self._create_dataset()
        
        self.samples = self._load_samples()
        logger.info(f"Loaded {len(self.samples)} URL samples ({split})")
    
    def _create_dataset(self):
        malicious_urls = [
            "http://pornhub.com/video/12345",
            "https://xvideos.com/watch/abc",
            "http://xxx-site.com",
            
            "http://paypa1.com/verify",
            "https://g00gle.com/login",
            "http://amaz0n.com/update",
            
            "http://free-download-crack.biz",
            "https://get-free-stuff.click",
        ]
        
        safe_urls = [
            "https://google.com/search",
            "https://github.com/user/repo",
            "https://stackoverflow.com/questions/123",
            "https://wikipedia.org/wiki/ML",
            "https://youtube.com/watch?v=abc",
        ]
        
        samples = []
        
        for url in malicious_urls:
            samples.append({
                'url': url,
                'label': 1,
                'category': 'adult' if any(k in url for k in ['porn', 'xxx']) else 'phishing'
            })
        
        for url in safe_urls:
            samples.append({
                'url': url,
                'label': 0,
                'category': 'legitimate'
            })
        
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(samples, f, indent=2)
    
    def _load_samples(self) -> List[Dict]:
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Tuple[str, int]:
        sample = self.samples[idx]
        return sample['url'], sample['label']

class NSFWDataAugmentation:
    def __init__(self, p: float = 0.5):
        self.p = p
        
        self.augmentations = [
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
            transforms.RandomGrayscale(p=0.1),
        ]
        
        self.adversarial_augmentations = [
            self._add_gaussian_noise,
            self._add_salt_pepper_noise,
            self._blur,
            self._jpeg_compression,
        ]
    
    def __call__(self, image: Image.Image) -> Image.Image:
        if np.random.rand() < self.p:
            for aug in self.augmentations:
                if np.random.rand() < 0.5:
                    if isinstance(aug, transforms.RandomResizedCrop):
                        image = transforms.Resize((256, 256))(image)
                        image = aug(image)
                    else:
                        image = aug(image)
            
            if np.random.rand() < 0.3:
                aug_func = np.random.choice(self.adversarial_augmentations)
                image = aug_func(image)
        
        return image
    
    def _add_gaussian_noise(self, image: Image.Image) -> Image.Image:
        img_array = np.array(image).astype(np.float32)
        noise = np.random.normal(0, 10, img_array.shape)
        noisy = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy)
    
    def _add_salt_pepper_noise(self, image: Image.Image) -> Image.Image:
        img_array = np.array(image)
        noise_mask = np.random.choice([0, 1, 2], size=img_array.shape[:2], p=[0.95, 0.025, 0.025])
        img_array[noise_mask == 1] = 255
        img_array[noise_mask == 2] = 0
        return Image.fromarray(img_array)
    
    def _blur(self, image: Image.Image) -> Image.Image:
        from PIL import ImageFilter
        return image.filter(ImageFilter.GaussianBlur(radius=np.random.uniform(0.5, 2.0)))
    
    def _jpeg_compression(self, image: Image.Image) -> Image.Image:
        buffer = io.BytesIO()
        quality = np.random.randint(30, 90)
        image.save(buffer, format='JPEG', quality=quality)
        buffer.seek(0)
        return Image.open(buffer)

class TextAugmentation:
    def __init__(self, p: float = 0.3):
        self.p = p
    
    def __call__(self, text: str) -> str:
        if np.random.rand() < self.p:
            augmentations = [
                self._synonym_replacement,
                self._random_insertion,
                self._random_swap,
                self._random_deletion,
            ]
            
            aug_func = np.random.choice(augmentations)
            text = aug_func(text)
        
        return text
    
    def _synonym_replacement(self, text: str) -> str:
        synonyms = {
            'bad': 'terrible',
            'good': 'great',
            'hate': 'dislike',
            'love': 'like',
        }
        
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in synonyms and np.random.rand() < 0.3:
                words[i] = synonyms[word.lower()]
        
        return ' '.join(words)
    
    def _random_insertion(self, text: str) -> str:
        fillers = ['really', 'very', 'extremely', 'totally']
        words = text.split()
        
        if len(words) > 2:
            insert_pos = np.random.randint(1, len(words))
            words.insert(insert_pos, np.random.choice(fillers))
        
        return ' '.join(words)
    
    def _random_swap(self, text: str) -> str:
        words = text.split()
        if len(words) < 2:
            return text
        
        idx = np.random.randint(0, len(words) - 1)
        words[idx], words[idx + 1] = words[idx + 1], words[idx]
        
        return ' '.join(words)
    
    def _random_deletion(self, text: str) -> str:
        words = text.split()
        if len(words) <= 3:
            return text
        
        keep_mask = np.random.rand(len(words)) > 0.1
        words = [w for w, keep in zip(words, keep_mask) if keep]
        
        return ' '.join(words) if words else text

class ModelTrainer:
    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        criterion: nn.Module,
        optimizer: optim.Optimizer,
        device: str = 'cuda',
        max_epochs: int = 100,
        early_stopping_patience: int = 10,
        checkpoint_dir: str = './checkpoints'
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.criterion = criterion
        self.optimizer = optimizer
        self.device = device
        self.max_epochs = max_epochs
        self.early_stopping_patience = early_stopping_patience
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', patience=5, factor=0.5
        )
        
        self.metrics_history = {
            'train_loss': [],
            'val_loss': [],
            'val_accuracy': [],
            'val_f1': [],
        }
        
        self.best_val_loss = float('inf')
        self.epochs_without_improvement = 0
        
        logger.info(f"Trainer initialized on {device}")
    
    def train(self) -> Dict[str, List[float]]:
        logger.info("=" * 60)
        logger.info("STARTING TRAINING")
        logger.info("=" * 60)
        
        for epoch in range(self.max_epochs):
            train_loss = self._train_epoch(epoch)
            
            val_metrics = self._validate_epoch(epoch)
            
            self.metrics_history['train_loss'].append(train_loss)
            self.metrics_history['val_loss'].append(val_metrics['loss'])
            self.metrics_history['val_accuracy'].append(val_metrics['accuracy'])
            self.metrics_history['val_f1'].append(val_metrics['f1'])
            
            self.scheduler.step(val_metrics['loss'])
            
            if val_metrics['loss'] < self.best_val_loss:
                self.best_val_loss = val_metrics['loss']
                self.epochs_without_improvement = 0
                self._save_checkpoint(epoch, val_metrics)
                logger.info(f"✅ New best model! Val Loss: {val_metrics['loss']:.4f}")
            else:
                self.epochs_without_improvement += 1
            
            if self.epochs_without_improvement >= self.early_stopping_patience:
                logger.info(f"Early stopping triggered after {epoch + 1} epochs")
                break
            
            logger.info(
                f"Epoch {epoch+1}/{self.max_epochs} | "
                f"Train Loss: {train_loss:.4f} | "
                f"Val Loss: {val_metrics['loss']:.4f} | "
                f"Val Acc: {val_metrics['accuracy']:.4f} | "
                f"Val F1: {val_metrics['f1']:.4f}"
            )
        
        logger.info("=" * 60)
        logger.info("TRAINING COMPLETE")
        logger.info(f"Best Val Loss: {self.best_val_loss:.4f}")
        logger.info("=" * 60)
        
        return self.metrics_history
    
    def _train_epoch(self, epoch: int) -> float:
        self.model.train()
        total_loss = 0.0
        
        for batch_idx, (inputs, targets) in enumerate(self.train_loader):
            inputs, targets = inputs.to(self.device), targets.to(self.device)
            
            self.optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = self.criterion(outputs, targets)
            
            loss.backward()
            
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            
            self.optimizer.step()
            
            total_loss += loss.item()
            
            if batch_idx % 50 == 0:
                logger.info(
                    f"Epoch {epoch+1} [{batch_idx}/{len(self.train_loader)}] "
                    f"Loss: {loss.item():.4f}"
                )
        
        return total_loss / len(self.train_loader)
    
    def _validate_epoch(self, epoch: int) -> Dict[str, float]:
        self.model.eval()
        total_loss = 0.0
        all_preds = []
        all_targets = []
        
        with torch.no_grad():
            for inputs, targets in self.val_loader:
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                
                total_loss += loss.item()
                
                preds = torch.argmax(outputs, dim=1)
                all_preds.extend(preds.cpu().numpy())
                all_targets.extend(targets.cpu().numpy())
        
        accuracy = accuracy_score(all_targets, all_preds)
        f1 = f1_score(all_targets, all_preds, average='weighted')
        
        return {
            'loss': total_loss / len(self.val_loader),
            'accuracy': accuracy,
            'f1': f1
        }
    
    def _save_checkpoint(self, epoch: int, metrics: Dict):
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'metrics': metrics,
            'metrics_history': self.metrics_history
        }
        
        checkpoint_path = self.checkpoint_dir / f'best_model_epoch_{epoch}.pt'
        torch.save(checkpoint, checkpoint_path)
        logger.info(f"Checkpoint saved: {checkpoint_path}")
