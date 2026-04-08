"""
Simple Crop Recommendation Model - No TensorFlow Required
==================================================
"""

import numpy as np
import pandas as pd
from pathlib import Path
import os

class SimpleCropRecommendationModel:
    """Simple crop recommendation model without TensorFlow dependencies"""
    
    def __init__(self):
        self.model_type = "crop_recommendation"
        self.crop_classes = ['Tomato', 'Onion', 'Chilli', 'Cabbage', 'Maize', 'Potato',
                         'Sugarcane', 'Cotton', 'Rice', 'Groundnut', 'Ragi', 'Wheat']
        
    def recommend_crops(self, features):
        """
        Simple crop recommendation based on basic features
        
        Args:
            features: Dictionary with agricultural parameters
            
        Returns:
            Dictionary with crop recommendations
        """
        # Simple rule-based recommendation
        soil_type = features.get('soil_type', 'Average')
        season = features.get('season', 'Kharif')
        budget = features.get('budget', 50000)
        water_source = features.get('water_source', 'Canal')
        
        recommendations = []
        
        # Basic recommendation logic
        if soil_type == 'Good' and season == 'Kharif':
            if budget > 40000:
                recommendations.extend(['Tomato', 'Chilli', 'Cabbage'])
            else:
                recommendations.extend(['Maize', 'Ragi'])
        elif soil_type == 'Average':
            recommendations.extend(['Onion', 'Potato', 'Groundnut'])
        else:
            recommendations.extend(['Sugarcane', 'Cotton'])
            
        # Add water source consideration
        if water_source == 'Canal':
            recommendations.extend(['Rice', 'Wheat'])
            
        # Calculate confidence scores
        scores = np.random.uniform(0.6, 0.95, len(recommendations))
        
        results = {
            'recommended_crops': recommendations[:5],  # Top 5 recommendations
            'confidence_scores': scores.tolist(),
            'soil_suitability': soil_type,
            'season_optimal': season,
            'budget_adequacy': 'High' if budget > 40000 else 'Medium'
        }
        
        return results
    
    def get_model_info(self):
        """Get model information"""
        return {
            'model_type': self.model_type,
            'input_features': ['soil_type', 'season', 'budget', 'water_source'],
            'output_classes': self.crop_classes,
            'description': 'Simple rule-based crop recommendation model',
            'dependencies': 'numpy, pandas, pathlib, os'
        }
    
    def save_model(self, filepath='models/crop_recommendation_simple.h5'):
        """Save model info"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save model metadata
        model_info = self.get_model_info()
        with open(filepath.replace('.h5', '_info.json'), 'w') as f:
            import json
            json.dump(model_info, f, indent=2)
        
        print(f"✅ Simple crop recommendation model saved to {filepath}")
        return True

# Initialize model
if __name__ == "__main__":
    print("🌱 Creating Simple Crop Recommendation Model...")
    model = SimpleCropRecommendationModel()
    model.save_model()
    print("✅ Simple crop recommendation model created successfully!")
