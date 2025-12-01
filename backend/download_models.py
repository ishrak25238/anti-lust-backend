import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_file(url, dest_path):
    if os.path.exists(dest_path):
        logger.info(f"File already exists: {dest_path}")
        return

    logger.info(f"Downloading {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.info(f"Downloaded to {dest_path}")
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)

def main():
    models_dir = os.path.join(os.path.dirname(__file__), 'data', 'models')
    os.makedirs(models_dir, exist_ok=True)

    model_url = "https://github.com/notAI-tech/NudeNet/releases/download/v3.4-weights/640m.onnx"
    model_path = os.path.join(models_dir, "640m.onnx")

    print("[INFO] Downloading High-Precision NudeNet 640m Model...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    if os.path.exists(model_path):
        print(f"[INFO] File already exists: {model_path}")
        return

    try:
        response = requests.get(model_url, stream=True, headers=headers)
        response.raise_for_status()
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[INFO] Downloaded to {model_path}")
    except Exception as e:
        print(f"[ERROR] Failed to download {model_url}: {e}")
        if os.path.exists(model_path):
            os.remove(model_path)
    print("[OK] Download complete. The AI is now ready to use the 640m model.")

if __name__ == "__main__":
    main()
