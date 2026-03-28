"""
Visualize model predictions with image display
"""
import torch
import matplotlib.pyplot as plt
from PIL import Image
import argparse
import os
from predict import FishPredictor

def visualize_prediction(image_path, model_path='./models/best_fish_model.pth', save_path=None):
    """
    Visualize fish image with top predictions
    
    Args:
        image_path: Path to image file
        model_path: Path to trained model
        save_path: Optional path to save visualization
    """
    # Load predictor
    predictor = FishPredictor(model_path)
    
    # Make prediction
    results = predictor.predict(image_path, top_k=5)
    
    # Load image
    image = Image.open(image_path).convert('RGB')
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Display image
    ax1.imshow(image)
    ax1.axis('off')
    ax1.set_title('Input Image', fontsize=14, fontweight='bold')
    
    # Display predictions as horizontal bar chart
    species = [r[0] for r in results]
    probs = [r[1] * 100 for r in results]
    colors = plt.cm.viridis([p/100 for p in probs])
    
    y_pos = range(len(species))
    ax2.barh(y_pos, probs, color=colors)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(species)
    ax2.set_xlabel('Confidence (%)', fontsize=12)
    ax2.set_title('Top 5 Predictions', fontsize=14, fontweight='bold')
    ax2.set_xlim(0, 100)
    ax2.invert_yaxis()
    
    # Add percentage labels
    for i, prob in enumerate(probs):
        ax2.text(prob + 2, i, f'{prob:.1f}%', va='center')
    
    plt.tight_layout()
    
    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Visualization saved to: {save_path}")
    else:
        plt.show()


def visualize_batch(image_dir, model_path='./models/best_fish_model.pth', save_dir='./visualizations'):
    """
    Create visualizations for all images in a directory
    
    Args:
        image_dir: Directory containing images
        model_path: Path to trained model
        save_dir: Directory to save visualizations
    """
    os.makedirs(save_dir, exist_ok=True)
    
    # Get all image files
    image_files = [f for f in os.listdir(image_dir) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Processing {len(image_files)} images...")
    
    for i, filename in enumerate(image_files, 1):
        image_path = os.path.join(image_dir, filename)
        save_path = os.path.join(save_dir, f'prediction_{i}_{filename}')
        
        print(f"[{i}/{len(image_files)}] {filename}")
        visualize_prediction(image_path, model_path, save_path)
    
    print(f"\n✓ All visualizations saved to: {save_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visualize fish predictions')
    parser.add_argument('input', type=str, help='Image file or directory')
    parser.add_argument('--model', type=str, default='./models/best_fish_model.pth',
                        help='Path to trained model')
    parser.add_argument('--save', type=str, help='Path to save visualization')
    parser.add_argument('--save_dir', type=str, default='./visualizations',
                        help='Directory to save batch visualizations')
    
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        visualize_batch(args.input, args.model, args.save_dir)
    else:
        visualize_prediction(args.input, args.model, args.save)
