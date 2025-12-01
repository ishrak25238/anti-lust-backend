import os
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def check_directory(path, name):
    if not os.path.exists(path):
        logger.warning(f"❌ {name} NOT FOUND at: {path}")
        return False
    
    files = os.listdir(path)
    if not files:
        logger.warning(f"⚠️ {name} directory is EMPTY: {path}")
        return False
        
    logger.info(f"✅ {name} FOUND: {len(files)} files/folders in {path}")
    return True

def check_file(path, name):
    if not os.path.exists(path):
        logger.warning(f"❌ {name} NOT FOUND at: {path}")
        return False
    
    size_mb = os.path.getsize(path) / (1024 * 1024)
    logger.info(f"✅ {name} FOUND: {size_mb:.2f} MB at {path}")
    return True

def main():
    print("\n🔍 Verifying Training Data Status...\n")
    
    base_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    print("--- Vision System (Images) ---")
    nudenet_path = os.path.join(base_dir, 'nudenet')
    has_nudenet = check_directory(nudenet_path, "NudeNet Dataset")
    
    raw_images_path = os.path.join(base_dir, 'raw_images')
    has_raw = check_directory(raw_images_path, "Raw Images Dataset")
    
    if not has_nudenet and not has_raw:
        print("  -> ❗ ACTION REQUIRED: Download images as per TRAINING_GUIDE.md")

    print("\n--- Language Brain (Text) ---")
    jigsaw_path = os.path.join(base_dir, 'train.csv')
    has_jigsaw = check_file(jigsaw_path, "Jigsaw Toxic Comments")
    
    civil_path = os.path.join(base_dir, 'civil_comments.csv')
    has_civil = check_file(civil_path, "Civil Comments")
    
    if not has_jigsaw and not has_civil:
        print("  -> ❗ ACTION REQUIRED: Download CSVs as per TRAINING_GUIDE.md")

    print("\n--- Web Guardian (URLs) ---")
    urlhaus_path = os.path.join(base_dir, 'urlhaus.csv')
    has_urlhaus = check_file(urlhaus_path, "URLHaus Database")
    
    if not has_urlhaus:
        print("  -> ❗ ACTION REQUIRED: Download URLHaus CSV as per TRAINING_GUIDE.md")

    print("\n---------------------------------------------------")
    print("Summary: Run this script again after downloading files.")
    print("See backend/TRAINING_GUIDE.md for download links.")

if __name__ == "__main__":
    main()
