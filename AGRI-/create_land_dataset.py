#!/usr/bin/env python3
"""
Create Land Analysis Dataset
Generates and manages a structured land image dataset for training the CNN model
"""

import os
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import json
import shutil
from datetime import datetime

class LandDatasetCreator:
    def __init__(self, base_dir="datasets/land_analysis"):
        self.base_dir = base_dir
        self.images_dir = os.path.join(base_dir, "images")
        self.labels_file = os.path.join(base_dir, "labels.csv")
        
        # Soil quality classes
        self.soil_classes = {
            'poor': {
                'color_range': [(139, 90, 43), (160, 110, 60)],  # Brown shades
                'texture': 'rough',
                'vegetation': (0, 100, 0),  # Low vegetation
                'moisture': (0.2, 0.4),  # Low moisture
                'ph_range': (4.5, 6.0),
                'nitrogen_range': (20, 40),
                'phosphorus_range': (10, 25),
                'potassium_range': (15, 30)
            },
            'average': {
                'color_range': [(101, 67, 33), (139, 90, 43)],  # Medium brown
                'texture': 'medium',
                'vegetation': (0, 150, 0),  # Medium vegetation
                'moisture': (0.4, 0.6),  # Medium moisture
                'ph_range': (6.0, 7.0),
                'nitrogen_range': (40, 70),
                'phosphorus_range': (25, 40),
                'potassium_range': (30, 50)
            },
            'good': {
                'color_range': [(46, 125, 50), (76, 175, 80)],  # Dark green-brown
                'texture': 'smooth',
                'vegetation': (0, 200, 0),  # High vegetation
                'moisture': (0.6, 0.8),  # High moisture
                'ph_range': (6.5, 7.5),
                'nitrogen_range': (70, 100),
                'phosphorus_range': (40, 60),
                'potassium_range': (50, 80)
            }
        }
        
        # Image variations
        self.conditions = ['sunny', 'cloudy', 'dawn', 'dusk']
        self.seasons = ['summer', 'monsoon', 'winter', 'spring']
        
    def create_directories(self):
        """Create dataset directory structure"""
        print("Creating dataset directories...")
        
        dirs = [
            self.base_dir,
            self.images_dir,
            os.path.join(self.images_dir, 'train'),
            os.path.join(self.images_dir, 'val'),
            os.path.join(self.images_dir, 'test')
        ]
        
        for split in ['train', 'val', 'test']:
            for soil_class in self.soil_classes.keys():
                dirs.append(os.path.join(self.images_dir, split, soil_class))
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
            print(f"  Created: {dir_path}")
    
    def generate_land_image(self, soil_class, width=224, height=224, condition='sunny', season='summer'):
        """Generate a synthetic land image based on soil quality"""
        
        class_props = self.soil_classes[soil_class]
        
        # Create base image
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Generate soil color variations
        base_color = class_props['color_range'][0]
        variation = class_props['color_range'][1]
        
        # Create soil texture
        for y in range(height):
            for x in range(width):
                # Add noise and variation
                noise = np.random.normal(0, 10)
                color_variation = [
                    int(min(255, max(0, base_color[i] + noise + np.random.randint(-20, 20))))
                    for i in range(3)
                ]
                
                # Add texture patterns
                if class_props['texture'] == 'rough':
                    if np.random.random() > 0.7:
                        color_variation = [int(min(255, c - 30)) for c in color_variation]
                elif class_props['texture'] == 'smooth':
                    if np.random.random() > 0.9:
                        color_variation = [int(min(255, c + 10)) for c in color_variation]
                
                draw.point((x, y), fill=tuple(color_variation))
        
        # Add vegetation patches
        vegetation_density = class_props['vegetation'][1] / 255.0
        for _ in range(int(vegetation_density * 50)):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            size = np.random.randint(5, 15)
            
            veg_color = (
                int(np.random.randint(0, class_props['vegetation'][1])),
                int(np.random.randint(max(0, class_props['vegetation'][1] - 50), min(255, class_props['vegetation'][1] + 50))),
                0
            )
            
            draw.ellipse([x-size, y-size, x+size, y+size], fill=veg_color)
        
        # Apply lighting conditions
        if condition == 'cloudy':
            img = img.point(lambda p: int(p * 0.8))
        elif condition == 'dawn':
            img = img.point(lambda p: int(p * 0.6))
            # Add reddish tint
            img = Image.blend(img, Image.new('RGB', (width, height), (255, 200, 200)), 0.2)
        elif condition == 'dusk':
            img = img.point(lambda p: int(p * 0.7))
            # Add orange tint
            img = Image.blend(img, Image.new('RGB', (width, height), (255, 200, 100)), 0.3)
        
        # Apply seasonal effects
        if season == 'monsoon':
            img = img.point(lambda p: int(p * 0.9))
            # Add wetness effect
            img = img.filter(ImageFilter.BLUR)
        elif season == 'winter':
            img = img.point(lambda p: int(p * 0.85))
        elif season == 'spring':
            # Add more green
            img = Image.blend(img, Image.new('RGB', (width, height), (200, 255, 200)), 0.1)
        
        # Add some random noise for realism
        noise = np.random.normal(0, 5, (height, width, 3))
        img_array = np.array(img)
        img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(img_array)
        
        return img
    
    def generate_dataset(self, samples_per_class=100):
        """Generate complete dataset with labels"""
        print(f"Generating dataset with {samples_per_class} samples per class...")
        
        labels = []
        dataset_info = {
            'created_at': datetime.now().isoformat(),
            'total_samples': samples_per_class * len(self.soil_classes),
            'classes': list(self.soil_classes.keys()),
            'image_size': (224, 224),
            'conditions': self.conditions,
            'seasons': self.seasons
        }
        
        # Split ratios
        train_ratio = 0.7
        val_ratio = 0.2
        test_ratio = 0.1
        
        sample_id = 0
        
        for soil_class, properties in self.soil_classes.items():
            print(f"\nGenerating {soil_class} soil images...")
            
            # Calculate splits
            total_samples = samples_per_class
            train_samples = int(total_samples * train_ratio)
            val_samples = int(total_samples * val_ratio)
            test_samples = total_samples - train_samples - val_samples
            
            # Generate training images
            for i in range(train_samples):
                condition = np.random.choice(self.conditions)
                season = np.random.choice(self.seasons)
                
                img = self.generate_land_image(soil_class, condition=condition, season=season)
                
                filename = f"{soil_class}_{sample_id:04d}_{condition}_{season}.jpg"
                filepath = os.path.join(self.images_dir, 'train', soil_class, filename)
                img.save(filepath)
                
                # Create label
                label = {
                    'filename': filename,
                    'soil_class': soil_class,
                    'split': 'train',
                    'condition': condition,
                    'season': season,
                    'ph': np.random.uniform(*properties['ph_range']),
                    'nitrogen': np.random.uniform(*properties['nitrogen_range']),
                    'phosphorus': np.random.uniform(*properties['phosphorus_range']),
                    'potassium': np.random.uniform(*properties['potassium_range']),
                    'moisture': np.random.uniform(*properties['moisture']),
                    'texture': properties['texture']
                }
                labels.append(label)
                sample_id += 1
            
            # Generate validation images
            for i in range(val_samples):
                condition = np.random.choice(self.conditions)
                season = np.random.choice(self.seasons)
                
                img = self.generate_land_image(soil_class, condition=condition, season=season)
                
                filename = f"{soil_class}_{sample_id:04d}_{condition}_{season}.jpg"
                filepath = os.path.join(self.images_dir, 'val', soil_class, filename)
                img.save(filepath)
                
                label = {
                    'filename': filename,
                    'soil_class': soil_class,
                    'split': 'val',
                    'condition': condition,
                    'season': season,
                    'ph': np.random.uniform(*properties['ph_range']),
                    'nitrogen': np.random.uniform(*properties['nitrogen_range']),
                    'phosphorus': np.random.uniform(*properties['phosphorus_range']),
                    'potassium': np.random.uniform(*properties['potassium_range']),
                    'moisture': np.random.uniform(*properties['moisture']),
                    'texture': properties['texture']
                }
                labels.append(label)
                sample_id += 1
            
            # Generate test images
            for i in range(test_samples):
                condition = np.random.choice(self.conditions)
                season = np.random.choice(self.seasons)
                
                img = self.generate_land_image(soil_class, condition=condition, season=season)
                
                filename = f"{soil_class}_{sample_id:04d}_{condition}_{season}.jpg"
                filepath = os.path.join(self.images_dir, 'test', soil_class, filename)
                img.save(filepath)
                
                label = {
                    'filename': filename,
                    'soil_class': soil_class,
                    'split': 'test',
                    'condition': condition,
                    'season': season,
                    'ph': np.random.uniform(*properties['ph_range']),
                    'nitrogen': np.random.uniform(*properties['nitrogen_range']),
                    'phosphorus': np.random.uniform(*properties['phosphorus_range']),
                    'potassium': np.random.uniform(*properties['potassium_range']),
                    'moisture': np.random.uniform(*properties['moisture']),
                    'texture': properties['texture']
                }
                labels.append(label)
                sample_id += 1
        
        # Save labels CSV
        df = pd.DataFrame(labels)
        df.to_csv(self.labels_file, index=False)
        print(f"  Saved labels to: {self.labels_file}")
        
        # Save dataset info
        info_file = os.path.join(self.base_dir, 'dataset_info.json')
        with open(info_file, 'w') as f:
            json.dump(dataset_info, f, indent=2)
        print(f"  Saved dataset info to: {info_file}")
        
        return labels, dataset_info
    
    def create_real_samples_template(self):
        """Create template for collecting real land images"""
        template_dir = os.path.join(self.base_dir, "real_samples")
        os.makedirs(template_dir, exist_ok=True)
        
        # Create collection guide
        guide = {
            'purpose': 'Collect real land images for better model training',
            'instructions': [
                'Take photos of actual agricultural land',
                'Include different soil qualities (poor, average, good)',
                'Capture various lighting conditions',
                'Include different seasons if possible',
                'Ensure images are clear and focused on soil',
                'Avoid shadows and obstructions'
            ],
            'image_requirements': {
                'size': 'Minimum 224x224 pixels',
                'format': 'JPG or PNG',
                'focus': 'Soil and land surface',
                'lighting': 'Natural daylight preferred'
            },
            'labeling_format': {
                'filename': 'soil_quality_location_date.jpg',
                'required_labels': [
                    'soil_quality',
                    'location',
                    'date',
                    'ph_level',
                    'nitrogen_content',
                    'phosphorus_content',
                    'potassium_content',
                    'moisture_level',
                    'notes'
                ]
            }
        }
        
        guide_file = os.path.join(template_dir, 'collection_guide.json')
        with open(guide_file, 'w') as f:
            json.dump(guide, f, indent=2)
        
        # Create labeling template
        template_data = []
        template_file = os.path.join(template_dir, 'real_labels_template.csv')
        
        columns = [
            'filename', 'soil_quality', 'location', 'date', 'ph_level',
            'nitrogen_content', 'phosphorus_content', 'potassium_content',
            'moisture_level', 'texture', 'vegetation_cover', 'notes'
        ]
        
        df_template = pd.DataFrame(columns=columns)
        df_template.to_csv(template_file, index=False)
        
        print(f"Created real samples template in: {template_dir}")
        return template_dir

def main():
    """Main function to create land analysis dataset"""
    print("="*60)
    print("LAND ANALYSIS DATASET CREATOR")
    print("="*60)
    
    creator = LandDatasetCreator()
    
    # Create directory structure
    creator.create_directories()
    
    # Generate synthetic dataset
    labels, info = creator.generate_dataset(samples_per_class=150)
    
    # Create real samples template
    template_dir = creator.create_real_samples_template()
    
    print("\n" + "="*60)
    print("DATASET CREATION COMPLETE!")
    print("="*60)
    print(f"Total images created: {info['total_samples']}")
    print(f"Classes: {', '.join(info['classes'])}")
    print(f"Image size: {info['image_size']}")
    print(f"Conditions: {', '.join(info['conditions'])}")
    print(f"Seasons: {', '.join(info['seasons'])}")
    print(f"\nDataset structure:")
    print(f"  {creator.base_dir}/")
    print(f"  |-- images/")
    print(f"  |   |-- train/")
    print(f"  |   |-- val/")
    print(f"  |   |-- test/")
    print(f"  |-- labels.csv")
    print(f"  |-- dataset_info.json")
    print(f"  |-- real_samples/ (for collecting real images)")
    print(f"\nNext steps:")
    print(f"1. Use this dataset to train the land analysis CNN")
    print(f"2. Collect real land images using the template")
    print(f"3. Combine synthetic and real data for better performance")

if __name__ == "__main__":
    main()
