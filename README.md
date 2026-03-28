# Fish Identifier AI 🐟🤖

A deep learning system that identifies fish species from images using PyTorch and convolutional neural networks.

## Features

- **Large Dataset**: Uses the "A Large Scale Fish Dataset" from Kaggle with 9,000+ images across 9 fish species
- **Two Model Architectures**: 
  - Custom CNN built from scratch
  - ResNet-18 with transfer learning (recommended)
- **High Accuracy**: Achieves 90%+ validation accuracy after training
- **Easy to Use**: Simple command-line interface for training and prediction
- **Data Augmentation**: Robust training with random flips, rotations, and color jittering

## Dataset

The system uses the ["A Large Scale Fish Dataset"](https://www.kaggle.com/datasets/crowww/a-large-scale-fish-dataset) containing **9,000 images** of 9 common fish species (1,000 images each):

1. Black Sea Sprat
2. Gilt-Head Bream
3. Hourse Mackerel
4. Red Mullet
5. Red Sea Bream
6. Sea Bass
7. Shrimp
8. Striped Red Mullet
9. Trout

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd fish-logger
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Kaggle API** (for dataset download):
   - Go to https://www.kaggle.com/settings/account
   - Create a new API token (downloads `kaggle.json`)
   - Place `kaggle.json` in `~/.kaggle/` (Unix) or `%USERPROFILE%/.kaggle/` (Windows)
   - Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

## Quick Start

### Option 1: Run the Complete Demo
```bash
python demo.py
```
This will download the dataset, train the model, and test predictions automatically.

### Option 2: Step-by-Step

#### 1. Download the Dataset
```bash
python download_dataset.py
python prepare_dataset.py  # Organize dataset for training
```

#### 2. Train the Model
```bash
# Train with ResNet (recommended)
python train.py --model_type resnet --epochs 20

# Or train custom CNN
python train.py --model_type cnn --epochs 30
```

**Training Options**:
- `--data_dir`: Path to dataset (default: `./data/fish_train`)
- `--model_type`: `resnet` or `cnn` (default: `resnet`)
- `--epochs`: Number of training epochs (default: 20)
- `--batch_size`: Batch size (default: 32)
- `--lr`: Learning rate (default: 0.001)
- `--save_dir`: Directory to save models (default: `./models`)

#### 3. Make Predictions
```bash
# Predict single image
python predict.py path/to/fish_image.jpg

# Predict all images in a directory
python predict.py path/to/fish_images_folder/

# Specify model and top-k predictions
python predict.py my_fish.jpg --model ./models/best_fish_model.pth --top_k 5
```

## Model Architecture

### ResNet-18 (Transfer Learning)
- Pre-trained on ImageNet
- Modified final layer for 9-class classification
- Dropout for regularization
- ~11M parameters

### Custom CNN
- 5 convolutional blocks with batch normalization
- MaxPooling and dropout
- 3 fully connected layers
- ~25M parameters

## Training Results

After 20 epochs with ResNet-18:
- Training Accuracy: ~95%
- Validation Accuracy: ~92%
- Training Time: ~30-45 minutes (GPU) / 2-3 hours (CPU)

Training history plots are saved in `./models/training_history.png`

## Project Structure

```
fish-logger/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── download_dataset.py          # Dataset download script
├── model.py                     # CNN and ResNet model definitions
├── train.py                     # Training script
├── predict.py                   # Prediction script
├── demo.py                      # Complete demo workflow
├── data/                        # Dataset directory (created after download)
│   └── fish_dataset/
└── models/                      # Trained models (created during training)
    ├── best_fish_model.pth      # Best model checkpoint
    ├── final_fish_model.pth     # Final model
    ├── training_history.json    # Training metrics
    └── training_history.png     # Training plots
```

## Usage Examples

### Python API

```python
from predict import FishPredictor

# Initialize predictor
predictor = FishPredictor('./models/best_fish_model.pth')

# Predict single image
results = predictor.predict('my_fish.jpg', top_k=3)
for species, probability in results:
    print(f"{species}: {probability*100:.2f}%")

# Batch prediction
image_list = ['fish1.jpg', 'fish2.jpg', 'fish3.jpg']
batch_results = predictor.predict_batch(image_list)
```

### Custom Training

```python
from train import train_model

train_model(
    data_dir='./data/fish_dataset/Fish_Dataset/Fish_Dataset',
    model_type='resnet',
    num_epochs=25,
    batch_size=64,
    learning_rate=0.0001,
    save_dir='./my_models'
)
```

## Requirements

- Python 3.8+
- PyTorch 2.0+
- torchvision
- PIL (Pillow)
- NumPy
- Matplotlib
- scikit-learn
- kagglehub
- tqdm

See `requirements.txt` for specific versions.

## Performance Tips

1. **Use GPU**: Training is much faster with CUDA-enabled GPU
2. **Batch Size**: Increase if you have more GPU memory (try 64 or 128)
3. **Learning Rate**: Use learning rate scheduling (already implemented)
4. **Data Augmentation**: Already includes flips, rotations, and color jittering
5. **Transfer Learning**: ResNet with pre-trained weights converges faster

## Troubleshooting

**Dataset download fails**:
- Ensure Kaggle API credentials are set up correctly
- Check internet connection
- Manually download from Kaggle website if needed

**Out of memory during training**:
- Reduce batch size: `--batch_size 16`
- Use CPU: Model will automatically use CPU if GPU unavailable

**Low accuracy**:
- Train for more epochs: `--epochs 30`
- Check if dataset downloaded correctly
- Ensure images are not corrupted

## License

See LICENSE file.

## Acknowledgments

- Dataset: ["A Large Scale Fish Dataset"](https://www.kaggle.com/datasets/crowww/a-large-scale-fish-dataset) by Oğuzhan Ulucan
- ResNet architecture: He et al., "Deep Residual Learning for Image Recognition"
- PyTorch framework: Facebook AI Research