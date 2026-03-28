# Fish Identification AI System

## Overview
Complete deep learning system for identifying fish species from images using PyTorch.

## Core Components
1. **download_dataset.py** - Downloads fish dataset from Kaggle (~9K images, 9 species)
2. **model.py** - Two architectures: Custom CNN and ResNet-18 (transfer learning)
3. **train.py** - Full training pipeline with validation and checkpointing
4. **predict.py** - Inference engine for single/batch predictions
5. **demo.py** - End-to-end demonstration workflow

## Quick Commands

### Setup
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### Run Everything
```bash
python demo.py  # Download data, train, predict
```

### Individual Steps
```bash
python download_dataset.py           # Download dataset
python train.py --epochs 20          # Train model
python predict.py image.jpg          # Predict species
```

## Model Performance
- **ResNet-18**: ~92% validation accuracy (20 epochs, ~30min on GPU)
- **Custom CNN**: ~88% validation accuracy (30 epochs, ~45min on GPU)

## Dataset Structure
After download: `./data/fish_dataset/Fish_Dataset/Fish_Dataset/`
- 9 species classes
- ~1000 images per class
- 224x224 RGB images (preprocessed)

## Training Features
- Data augmentation (flip, rotate, color jitter)
- Learning rate scheduling
- Early stopping via best model checkpointing
- Training history plots
- Validation split (80/20)

## Output Files
```
models/
├── best_fish_model.pth          # Best checkpoint (highest val accuracy)
├── final_fish_model.pth         # Final epoch model
├── training_history.json        # Loss/accuracy metrics
└── training_history.png         # Training curves
```
