"""
Command-line interface for fish species prediction.
"""
import argparse
import json
import os
import sys
from predict import FishPredictor

def main():
    """
    CLI for predicting fish species from an image.
    Outputs prediction results as a JSON string.
    """
    # Suppress model loading print statements for cleaner JSON output
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    
    parser = argparse.ArgumentParser(description='Predict fish species from an image.')
    parser.add_argument('image_path', help='Path to the image file.')
    args = parser.parse_args()

    # Restore stdout
    sys.stdout.close()
    sys.stdout = original_stdout

    if not os.path.exists(args.image_path):
        print(json.dumps({'error': f'Image not found at {args.image_path}'}))
        return

    try:
        # Construct the model path relative to this script's location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, 'models', 'best_fish_model.pth')

        if not os.path.exists(model_path):
             print(json.dumps({'error': f'Model not found at {model_path}'}))
             return

        predictor = FishPredictor(model_path)
        # Get only the top prediction
        predictions = predictor.predict(args.image_path, top_k=1)
        
        if predictions:
            species, confidence = predictions[0]
            result = {
                'species': species,
                'confidence': confidence
            }
            print(json.dumps(result))
        else:
            print(json.dumps({'error': 'Prediction failed.'}))

    except Exception as e:
        print(json.dumps({'error': str(e)}))

if __name__ == '__main__':
    main()
