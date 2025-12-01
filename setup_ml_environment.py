import os
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def install_dependencies():
    logger.info("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
        logger.info("✅ Dependencies installed.")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def create_directories():
    logger.info("wd Creating data directories...")
    base_dir = os.path.join("backend", "data")
    dirs = [
        "models",
        "blacklists"
    ]
    
    for d in dirs:
        path = os.path.join(base_dir, d)
        os.makedirs(path, exist_ok=True)
        logger.info(f"  -> Created: {path}")
    
    logger.info("✅ Directories ready.")

def download_models():
    logger.info("⬇️ Downloading High-Precision Models...")
    try:
        # Run the master downloader
        subprocess.check_call([sys.executable, "download_all_brains.py"])
        logger.info("✅ Models downloaded.")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to download models: {e}")

def main():
    print("\n🛡️ Anti-Lust Guardian: ML Environment Setup 🛡️\n")
    
    # Ensure we are in the root directory
    if not os.path.exists("backend"):
        logger.error("Please run this script from the project root (E:\\Anti-Lust app)")
        sys.exit(1)

    install_dependencies()
    create_directories()
    download_models()
    
    print("\n" + "="*50)
    print("✅ SETUP COMPLETE! The Code and Brain are ready.")
    print("="*50)
    print("\n👉 YOUR FINAL MISSION (Safe Mode):")
    print("1. Run 'uvicorn main:app --reload'")
    print("2. Wait for the system to auto-download FalconsAI & CLIP models (approx 2GB)")
    print("3. The system will be fully operational with pre-trained military-grade AI.")
    print("\nGood luck, Guardian.")

if __name__ == "__main__":
    main()
