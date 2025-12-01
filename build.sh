#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "--------------------------------------------------"
echo "Starting Custom Build Script"
echo "--------------------------------------------------"

echo "1. Upgrading build tools (forcing setuptools<70.0.0)..."
pip install --upgrade pip wheel
pip install "setuptools<70.0.0"

echo "2. Installing PyTorch (CPU version)..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

echo "3. Installing Transformers..."
pip install transformers

echo "4. Installing remaining dependencies from requirements.txt..."
pip install --no-build-isolation -r backend/requirements.txt

echo "5. Verifying installation..."
pip list
python -c "import torch; print(f'SUCCESS: Torch {torch.__version__} is installed!')"

echo "--------------------------------------------------"
echo "Build Script Completed Successfully"
echo "--------------------------------------------------"
