"""
Download Fish Dataset from Kaggle using kagglehub
This uses the "A Large Scale Fish Dataset" which contains 9000 images across 9 species
"""
import kagglehub
import os
import shutil

def download_fish_dataset():
    """Download the fish dataset from Kaggle"""
    print("Downloading Fish Dataset from Kaggle...")
    print("This may take a few minutes depending on your internet connection...")
    
    try:
        # Download the "A Large Scale Fish Dataset" 
        path = kagglehub.dataset_download("crowww/a-large-scale-fish-dataset")
        
        print(f"\nDataset downloaded to: {path}")
        
        # Create a symlink or copy to a local data directory
        data_dir = "./data/fish_dataset"
        if os.path.exists(data_dir):
            print(f"Removing existing dataset at {data_dir}")
            shutil.rmtree(data_dir)
        
        os.makedirs(os.path.dirname(data_dir), exist_ok=True)
        
        # Create symlink to avoid duplicating large dataset
        if os.name != 'nt':  # Unix-like systems
            os.symlink(path, data_dir, target_is_directory=True)
            print(f"Created symlink: {data_dir} -> {path}")
        else:  # Windows
            shutil.copytree(path, data_dir)
            print(f"Copied dataset to: {data_dir}")
        
        # List the contents
        print("\nDataset structure:")
        for root, dirs, files in os.walk(data_dir):
            level = root.replace(data_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            if level < 2:  # Only show first 2 levels
                subindent = ' ' * 2 * (level + 1)
                for file in files[:5]:  # Show first 5 files
                    print(f'{subindent}{file}')
                if len(files) > 5:
                    print(f'{subindent}... and {len(files) - 5} more files')
        
        return data_dir
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("\nAlternatively, you can manually download from:")
        print("https://www.kaggle.com/datasets/crowww/a-large-scale-fish-dataset")
        return None

if __name__ == "__main__":
    dataset_path = download_fish_dataset()
    if dataset_path:
        print(f"\n✓ Dataset ready at: {dataset_path}")
    else:
        print("\n✗ Failed to download dataset")
