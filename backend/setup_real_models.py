"""
Download and setup real pre-trained models for NSFW detection.
Uses publicly available, safe-to-download models.
"""
import os
import urllib.request
from pathlib import Path

MODELS_DIR = Path("data/models")
MODELS_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Setting up Real Pre-Trained Models")
print("=" * 60)

print("\n[1/2] Setting up NSFW Image Classifier...")
print("Source: Falcons/nsfw_image_detection (HuggingFace)")
print("This model was trained on NSFW datasets but we won't download those.")
print("We'll use the transformers library to auto-download the model weights.")

nsfw_model_info = {
    "name": "Falcons/nsfw_image_detection",
    "type": "image_classification",
    "framework": "transformers"
}

print("[OK] Will use HuggingFace Transformers (auto-download on first use)")

print("\n[2/2] Setting up Text Toxicity Classifier...")
print("Source: unitary/toxic-bert (HuggingFace)")
print("Pre-trained on Wikipedia comments, no NSFW content needed.")

text_model_info = {
    "name": "unitary/toxic-bert",
    "type": "text_classification",
    "framework": "transformers"
}

print("[OK] Will use HuggingFace Transformers (auto-download on first use)")

config = {
    "vision_model": nsfw_model_info,
    "text_model": text_model_info
}

import json
config_path = MODELS_DIR / "model_config.json"
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print(f"\n[OK] Configuration saved to: {config_path}")

print("\n" + "=" * 60)
print("NEXT STEPS:")
print("=" * 60)
print("1. Install dependencies: pip install transformers pillow")
print("2. Models will auto-download on first use (~500MB total)")
print("3. No NSFW content needed - models are pre-trained!")
print("\nRun: python test_real_models.py")
