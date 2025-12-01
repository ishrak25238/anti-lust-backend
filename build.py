import os
import subprocess
import sys

def run_command(command):
    print(f"Running: {command}")
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        sys.exit(1)

def main():
    print("--------------------------------------------------")
    print("Starting Custom Build Script (Python)")
    print("--------------------------------------------------")

    # 1. Upgrade build tools
    print("1. Upgrading build tools...")
    run_command(f"{sys.executable} -m pip install --upgrade pip wheel")
    run_command(f"{sys.executable} -m pip install \"setuptools<70.0.0\"")

    # 2. Install PyTorch (CPU)
    print("2. Installing PyTorch (CPU version)...")
    # We use --no-cache-dir to save space and avoid potential cache issues
    run_command(f"{sys.executable} -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --no-cache-dir")

    # 3. Install Transformers
    print("3. Installing Transformers...")
    run_command(f"{sys.executable} -m pip install transformers --no-cache-dir")

    # 4. Install remaining requirements
    print("4. Installing remaining dependencies...")
    run_command(f"{sys.executable} -m pip install --no-build-isolation -r backend/requirements.txt")

    # 5. Verify installation
    print("5. Verifying installation...")
    try:
        import torch
        print(f"SUCCESS: Torch {torch.__version__} is installed at {torch.__file__}")
    except ImportError:
        print("ERROR: Torch failed to import in the build script!")
        sys.exit(1)

    print("--------------------------------------------------")
    print("Build Script Completed Successfully")
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()
