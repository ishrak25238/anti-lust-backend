import os
import sys
import logging
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

def download_nudenet():
    print("\n[1] Downloading NudeNet (Object Detection)...")
    try:
        # Re-use the existing logic or script
        subprocess.check_call([sys.executable, "backend/download_models.py"])
        print("[OK] NudeNet 640m Ready.")
    except Exception as e:
        print(f"[ERROR] NudeNet Error: {e}")

def download_falconsai():
    print("\n[2] Downloading FalconsAI (NSFW Classification)...")
    try:
        from transformers import AutoModelForImageClassification, AutoImageProcessor
        
        # Define local path
        local_path = os.path.join("backend", "data", "models", "falconsai")
        
        if os.path.exists(local_path):
            print(f"   (FalconsAI already exists at {local_path})")
            return

        print(f"   Saving to: {local_path}")
        
        # Download and Save Locally
        processor = AutoImageProcessor.from_pretrained("Falconsai/nsfw_image_detection")
        model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
        
        processor.save_pretrained(local_path)
        model.save_pretrained(local_path)
        
        print("[OK] FalconsAI Model Saved Locally.")
    except ImportError:
        print("[ERROR] Error: Transformers not installed. Run 'pip install transformers'")
    except Exception as e:
        print(f"[ERROR] FalconsAI Error: {e}")

def download_clip():
    print("\n[3] Downloading OpenAI CLIP (Context Brain)...")
    try:
        from transformers import CLIPProcessor, CLIPModel
        
        # Define local path
        local_path = os.path.join("backend", "data", "models", "clip")
        
        if os.path.exists(local_path):
            print(f"   (CLIP already exists at {local_path})")
            return

        print(f"   Saving to: {local_path}")
        
        # Download and Save Locally
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
        model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
        
        processor.save_pretrained(local_path)
        model.save_pretrained(local_path)
        
        print("[OK] CLIP Model Saved Locally.")
    except Exception as e:
        print(f"[ERROR] CLIP Error: {e}")

def main():
    print("="*50)
    print("ANTI-LUST GUARDIAN: BRAIN DOWNLOADER")
    print("="*50)
    print("This script will download all pre-trained models now.")
    print("You do NOT need to visit any websites.")
    
    # Ensure we are in root
    if not os.path.exists("backend"):
        print("[ERROR] Please run this from the 'Anti-Lust app' root folder.")
        return

    download_nudenet()
    download_falconsai()
    download_clip()
    
    print("\n" + "="*50)
    print("[OK] ALL BRAINS ACQUIRED.")
    print("You can now run the app without internet access for ML.")
    print("="*50)

if __name__ == "__main__":
    main()
