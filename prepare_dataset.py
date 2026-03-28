#!/usr/bin/env python3
"""
Prepare the fish dataset for training by creating a clean directory structure.
The original dataset has nested folders (Species/Species/images and Species/Species GT/masks).
This script creates a flat structure with just Species/images for training.
"""
import os
import shutil
from pathlib import Path

def prepare_dataset(source_dir='./data/fish_dataset', target_dir='./data/fish_train'):
    """
    Reorganize dataset from nested structure to flat structure
    
    Original: Species/Species/image.png and Species/Species GT/mask.png
    Target:   Species/image.png
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    if not source_path.exists():
        print(f"❌ Source directory not found: {source_dir}")
        print("Please run: python download_dataset.py")
        return None
    
    # Remove existing target if it exists
    if target_path.exists():
        print(f"Removing existing directory: {target_path}")
        shutil.rmtree(target_path)
    
    target_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Preparing dataset from {source_path}")
    print(f"📁 Creating clean structure at {target_path}\n")
    
    # List of fish species (folders in the dataset)
    species_folders = [d for d in source_path.iterdir() 
                      if d.is_dir() and not d.name.startswith('.')]
    
    total_images = 0
    species_count = 0
    
    for species_folder in sorted(species_folders):
        species_name = species_folder.name
        
        # Skip non-species folders
        if species_name in ['license.txt', 'README.txt', 'Segmentation_example_script.m']:
            continue
        
        # Look for the nested image folder (Species/Species/)
        image_folder = species_folder / species_name
        
        if not image_folder.exists():
            print(f"⚠️  Skipping {species_name}: image folder not found")
            continue
        
        # Create target species folder
        target_species = target_path / species_name
        target_species.mkdir(exist_ok=True)
        
        # Copy/symlink images
        image_files = list(image_folder.glob('*.png')) + list(image_folder.glob('*.jpg'))
        
        print(f"📸 {species_name}: {len(image_files)} images")
        
        for image_file in image_files:
            target_file = target_species / image_file.name
            # Create symlink to save space (or copy if on Windows)
            if os.name != 'nt':
                os.symlink(image_file.absolute(), target_file)
            else:
                shutil.copy2(image_file, target_file)
        
        total_images += len(image_files)
        species_count += 1
    
    print(f"\n✅ Dataset prepared!")
    print(f"   Species: {species_count}")
    print(f"   Total images: {total_images}")
    print(f"   Location: {target_path.absolute()}")
    
    return str(target_path.absolute())


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Prepare fish dataset for training')
    parser.add_argument('--source', type=str, default='./data/fish_dataset',
                        help='Source dataset directory')
    parser.add_argument('--target', type=str, default='./data/fish_train',
                        help='Target directory for prepared dataset')
    
    args = parser.parse_args()
    
    result = prepare_dataset(args.source, args.target)
    
    if result:
        print(f"\n💡 Now you can train the model with:")
        print(f"   python train.py --data_dir {result}")
