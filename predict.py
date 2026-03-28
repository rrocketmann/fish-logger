"""
Fish species prediction from images
"""
import torch
from torchvision import transforms
from PIL import Image
import os
import argparse
from model import get_model

class FishPredictor:
    """Class for making predictions on fish images"""
    
    def __init__(self, model_path='./models/best_fish_model.pth'):
        """
        Initialize the predictor
        
        Args:
            model_path: Path to trained model checkpoint
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load checkpoint
        checkpoint = torch.load(model_path, map_location=self.device)
        self.class_names = checkpoint['class_names']
        model_type = checkpoint.get('model_type', 'resnet')
        
        # Initialize model
        self.model = get_model(model_type=model_type, num_classes=len(self.class_names), pretrained=False)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        
        print(f"✓ Model loaded from {model_path}")
        print(f"✓ Device: {self.device}")
        print(f"✓ Classes: {self.class_names}")
    
    def predict(self, image_path, top_k=3):
        """
        Predict fish species from image
        
        Args:
            image_path: Path to image file
            top_k: Number of top predictions to return
        
        Returns:
            List of (class_name, probability) tuples
        """
        # Load and preprocess image
        image = Image.open(image_path).convert('RGB')
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Make prediction
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
        
        # Get top k predictions
        top_probs, top_indices = probabilities.topk(top_k, dim=1)
        
        results = []
        for prob, idx in zip(top_probs[0], top_indices[0]):
            results.append((self.class_names[idx], prob.item()))
        
        return results
    
    def predict_batch(self, image_paths):
        """
        Predict fish species for multiple images
        
        Args:
            image_paths: List of image file paths
        
        Returns:
            List of prediction results
        """
        results = []
        for image_path in image_paths:
            try:
                preds = self.predict(image_path)
                results.append({
                    'image': image_path,
                    'predictions': preds
                })
            except Exception as e:
                results.append({
                    'image': image_path,
                    'error': str(e)
                })
        return results


def main():
    parser = argparse.ArgumentParser(description='Predict fish species from image')
    parser.add_argument('image', type=str, help='Path to image file or directory')
    parser.add_argument('--model', type=str, default='./models/best_fish_model.pth',
                        help='Path to trained model')
    parser.add_argument('--top_k', type=int, default=3,
                        help='Number of top predictions to show')
    
    args = parser.parse_args()
    
    # Initialize predictor
    predictor = FishPredictor(args.model)
    
    # Check if input is directory or file
    if os.path.isdir(args.image):
        # Process all images in directory
        image_files = [os.path.join(args.image, f) for f in os.listdir(args.image)
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        print(f"\nProcessing {len(image_files)} images from {args.image}")
        
        results = predictor.predict_batch(image_files)
        for result in results:
            if 'error' in result:
                print(f"\n✗ {result['image']}: {result['error']}")
            else:
                print(f"\n{result['image']}:")
                for i, (species, prob) in enumerate(result['predictions'], 1):
                    print(f"  {i}. {species}: {prob*100:.2f}%")
    else:
        # Process single image
        results = predictor.predict(args.image, top_k=args.top_k)
        
        print(f"\nPredictions for: {args.image}")
        print("-" * 50)
        for i, (species, prob) in enumerate(results, 1):
            print(f"{i}. {species}: {prob*100:.2f}%")


if __name__ == "__main__":
    main()
