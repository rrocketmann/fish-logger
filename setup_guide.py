#!/usr/bin/env python3
"""
Interactive setup and usage guide for Fish Identifier AI
"""
import os
import sys
import subprocess

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_step(number, text):
    """Print a formatted step"""
    print(f"\n[Step {number}] {text}")
    print("-" * 70)

def check_kaggle_setup():
    """Check if Kaggle API is configured"""
    kaggle_config = os.path.expanduser("~/.kaggle/kaggle.json")
    return os.path.exists(kaggle_config)

def main():
    print_header("🐟 Fish Identifier AI - Interactive Setup & Guide 🤖")
    
    print("""
This AI system identifies fish species from images using deep learning.

What this system does:
  • Downloads a dataset of 9,000+ fish images (9 species)
  • Trains a neural network to recognize fish species
  • Makes predictions on new fish images with confidence scores
  • Visualizes predictions with charts
    """)
    
    # Check environment
    print_step("1/4", "Environment Check")
    
    venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not venv_active:
        print("⚠️  Virtual environment not activated!")
        print("\nPlease run:")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("  pip install -r requirements.txt")
        print("\nThen run this script again.")
        return
    else:
        print("✓ Virtual environment is active")
    
    # Check dependencies
    try:
        import torch
        print(f"✓ PyTorch {torch.__version__} installed")
        if torch.cuda.is_available():
            print(f"✓ GPU available: {torch.cuda.get_device_name(0)}")
        else:
            print("ℹ️  Using CPU (training will be slower)")
    except ImportError:
        print("✗ PyTorch not installed")
        print("Run: pip install -r requirements.txt")
        return
    
    # Check Kaggle
    print_step("2/4", "Kaggle API Setup")
    
    if check_kaggle_setup():
        print("✓ Kaggle API configured")
    else:
        print("⚠️  Kaggle API not configured (required for dataset download)")
        print("\nTo set up Kaggle API:")
        print("  1. Go to https://www.kaggle.com/settings/account")
        print("  2. Scroll to 'API' section")
        print("  3. Click 'Create New Token' (downloads kaggle.json)")
        print("  4. Move kaggle.json to ~/.kaggle/")
        print("  5. Set permissions: chmod 600 ~/.kaggle/kaggle.json")
        print("\nYou can also manually download the dataset from:")
        print("  https://www.kaggle.com/datasets/crowww/a-large-scale-fish-dataset")
    
    # Usage options
    print_step("3/4", "Choose Your Option")
    
    print("""
A) Quick Demo (Recommended for first-time users)
   └─ Downloads data, trains model, tests prediction
   └─ Command: python demo.py
   └─ Time: ~30-45 minutes with GPU, 2-3 hours with CPU

B) Manual Training (For customization)
   └─ Step 1: python download_dataset.py
   └─ Step 2: python train.py --epochs 20
   └─ Step 3: python predict.py <image.jpg>

C) Quick Prediction (If model already trained)
   └─ python predict.py path/to/fish_image.jpg
   └─ python visualize.py path/to/fish_image.jpg

D) Batch Processing (Multiple images)
   └─ python predict.py path/to/image_folder/
   └─ python visualize.py path/to/image_folder/
    """)
    
    print_step("4/4", "Training Tips")
    
    print("""
For best results:
  • Use GPU if available (10x faster training)
  • Start with ResNet-18 (default, better accuracy)
  • Train for at least 20 epochs
  • Use batch size 32-64 depending on GPU memory
  • Monitor validation accuracy (saved in models/)

Advanced options:
  python train.py --help        # See all training options
  python predict.py --help      # See prediction options
  python visualize.py --help    # See visualization options
    """)
    
    print_header("Ready to Start!")
    
    print("""
Quick start commands:

  # Full demo (all-in-one)
  python demo.py

  # Or step by step:
  python download_dataset.py           # Download fish dataset
  python train.py --epochs 20          # Train the AI model
  python predict.py my_fish.jpg        # Identify a fish
  python visualize.py my_fish.jpg      # See prediction chart

For detailed documentation, see README.md
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
