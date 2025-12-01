import os
import subprocess
import sys

print("=" * 60)
print("CUSTOM BUILD SCRIPT STARTED")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print("=" * 60)

def run_command(command, description=""):
    if description:
        print(f"\n>>> {description}")
    print(f"    Command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(f"    Output: {result.stdout[:500]}")
    if result.stderr:
        print(f"    Stderr: {result.stderr[:500]}")
    
    if result.returncode != 0:
        print(f"    ERROR: Command failed with exit code {result.returncode}")
        sys.exit(1)
    
    print(f"    ✓ Success")
    return result

def main():
    # 1. Show environment
    print("\n" + "=" * 60)
    print("ENVIRONMENT INFO")
    print("=" * 60)
    run_command("pip --version", "Checking pip version")
    run_command("which python", "Python location")
    
    # 2. Upgrade pip and setuptools
    print("\n" + "=" * 60)
    print("UPGRADING BUILD TOOLS")
    print("=" * 60)
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    run_command(f"{sys.executable} -m pip install wheel", "Installing wheel")
    run_command(f'{sys.executable} -m pip install "setuptools<70.0.0"', "Pinning setuptools")

    # 3. Install PyTorch
    print("\n" + "=" * 60)
    print("INSTALLING PYTORCH (CPU)")
    print("=" * 60)
    torch_cmd = f"{sys.executable} -m pip install torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu --no-cache-dir"
    run_command(torch_cmd, "Installing PyTorch CPU")

    # 4. Verify torch immediately
    print("\n" + "=" * 60)
    print("VERIFYING PYTORCH INSTALLATION")
    print("=" * 60)
    verify_result = subprocess.run(
        [sys.executable, "-c", "import torch; print(f'Torch {torch.__version__} at {torch.__file__}')"],
        capture_output=True,
        text=True
    )
    if verify_result.returncode == 0:
        print(f"    ✓ {verify_result.stdout.strip()}")
    else:
        print(f"    ✗ FAILED TO IMPORT TORCH")
        print(f"    Error: {verify_result.stderr}")
        sys.exit(1)

    # 5. Install transformers
    print("\n" + "=" * 60)
    print("INSTALLING TRANSFORMERS")
    print("=" * 60)
    run_command(f"{sys.executable} -m pip install transformers --no-cache-dir", "Installing transformers")

    # 6. Install remaining requirements
    print("\n" + "=" * 60)
    print("INSTALLING REMAINING DEPENDENCIES")
    print("=" * 60)
    run_command(f"{sys.executable} -m pip install --no-build-isolation -r backend/requirements.txt", "Installing from requirements.txt")

    # 7. Final verification
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION")
    print("=" * 60)
    run_command("pip list | grep -i torch", "Listing torch packages")
    
    # Final torch check
    final_check = subprocess.run(
        [sys.executable, "-c", "import torch; import transformers; print('✓ All ML libraries loaded successfully')"],
        capture_output=True,
        text=True
    )
    if final_check.returncode == 0:
        print(f"\n{final_check.stdout.strip()}")
    else:
        print(f"\n✗ ML libraries failed to load: {final_check.stderr}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n{'=' * 60}")
        print(f"BUILD FAILED WITH EXCEPTION:")
        print(f"{'=' * 60}")
        print(str(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)
