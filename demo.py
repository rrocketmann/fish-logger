#!/usr/bin/env python3
"""
Quick demo script to download data, train model, and make predictions
"""
import os
import sys

def run_demo():
    print("=" * 70)
    print("FISH IDENTIFICATION AI - DEMO")
    print("=" * 70)
    
    # Step 1: Download dataset
    print("\n[Step 1/3] Downloading Fish Dataset...")
    print("-" * 70)
    import download_dataset
    dataset_path = download_dataset.download_fish_dataset()
    
    if not dataset_path:
        print("\n✗ Failed to download dataset. Please check your Kaggle credentials.")
        print("Run: kaggle configure")
        sys.exit(1)
    
    # Step 2: Train model (quick training with fewer epochs)
    print("\n[Step 2/3] Training Model...")
    print("-" * 70)
    print("Training with 10 epochs for quick demo...")
    from train import train_model
    train_model(
        data_dir=dataset_path,
        model_type='resnet',
        num_epochs=10,
        batch_size=32,
        learning_rate=0.001
    )
    
    # Step 3: Test prediction
    print("\n[Step 3/3] Testing Predictions...")
    print("-" * 70)
    from predict import FishPredictor
    
    # Find a test image
    test_image = None
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                test_image = os.path.join(root, file)
                break
        if test_image:
            break
    
    if test_image:
        predictor = FishPredictor('./models/best_fish_model.pth')
        results = predictor.predict(test_image, top_k=3)
        
        print(f"\nTest image: {test_image}")
        print("Predictions:")
        for i, (species, prob) in enumerate(results, 1):
            print(f"  {i}. {species}: {prob*100:.2f}%")
    
    print("\n" + "=" * 70)
    print("✓ DEMO COMPLETE!")
    print("=" * 70)
    print("\nYou can now use the trained model to identify fish:")
    print("  python predict.py <path_to_fish_image>")
    print("\nOr train with more epochs for better accuracy:")
    print("  python train.py --epochs 30")

if __name__ == "__main__":
    run_demo()
