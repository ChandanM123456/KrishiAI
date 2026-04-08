"""
Simple Weather Optimization Model - No TensorFlow Required
===================================================
"""

import numpy as np
import pandas as pd
from pathlib import Path
import os

class SimpleWeatherOptimizationModel:
    """Simple weather optimization model without TensorFlow dependencies"""
    
    def __init__(self):
        self.model_type = "weather_optimization"
        self.crop_classes = ['Tomato', 'Maize', 'Ragi', 'Wheat', 'Onion', 'Potato', 'Chilli', 'Cabbage']
        
    def optimize_crop_selection(self, features):
        """
        Simple crop selection optimization based on weather conditions
        
        Args:
            features: Dictionary with weather parameters
            
        Returns:
            Dictionary with optimized crop recommendations
        """
        # Extract weather features
        temperature = features.get('temperature', 25)
        rainfall = features.get('rainfall', 100)
        humidity = features.get('humidity', 60)
        season = features.get('season', 'Kharif')
        wind_speed = features.get('wind_speed', 10)
        
        # Simple optimization logic
        recommendations = []
        scores = []
        
        # Temperature-based recommendations
        if 20 <= temperature <= 30:
            recommendations.extend(['Tomato', 'Chilli', 'Cabbage'])
            scores.extend([0.9, 0.85, 0.8])
        elif 30 < temperature <= 35:
            recommendations.extend(['Maize', 'Wheat', 'Onion'])
            scores.extend([0.8, 0.75, 0.7])
        else:
            recommendations.extend(['Ragi', 'Potato'])
            scores.extend([0.6, 0.65, 0.5])
        
        # Rainfall-based adjustments
        if rainfall > 150:
            # Good rainfall - add water-intensive crops
            recommendations.extend(['Rice', 'Sugarcane'])
            scores.extend([0.85, 0.8, 0.75])
        elif rainfall < 50:
            # Low rainfall - add drought-resistant crops
            recommendations.extend(['Ragi', 'Groundnut'])
            scores.extend([0.7, 0.65, 0.6])
        
        # Season-based optimization
        if season == 'Kharif':
            season_bonus = ['Tomato', 'Maize', 'Ragi']
            for i, crop in enumerate(recommendations):
                if crop in season_bonus and i < len(scores):
                    scores[i] += 0.1
        
        # Get top recommendations
        top_crops = []
        top_scores = []
        
        # Sort by score and get top 5
        scored_crops = list(zip(recommendations, scores))
        scored_crops.sort(key=lambda x: x[1], reverse=True)
        
        for crop, score in scored_crops[:5]:
            if crop not in top_crops:
                top_crops.append(crop)
                top_scores.append(score)
        
        results = {
            'optimized_crops': top_crops,
            'confidence_scores': top_scores,
            'weather_conditions': {
                'temperature': temperature,
                'rainfall': rainfall,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'season': season
            },
            'recommendations': {
                'primary': top_crops[0] if top_crops else 'Tomato',
                'secondary': top_crops[1] if len(top_crops) > 1 else 'Maize',
                'alternative': top_crops[2] if len(top_crops) > 2 else 'Ragi'
            },
            'planting_schedule': self._generate_planting_schedule(top_crops, season),
            'irigation_needs': self._calculate_irigation_needs(rainfall, temperature)
        }
        
        return results
    
    def _generate_planting_schedule(self, crops, season):
        """Generate planting schedule based on season"""
        schedule = {}
        
        if season == 'Kharif':
            schedule['june_july'] = crops[:2]  # Early Kharif
            schedule['august_september'] = crops[2:4]  # Main Kharif
            schedule['october_november'] = crops[4:]  # Late Kharif
        else:
            # Rabi season
            schedule['october_december'] = crops[:3]
            schedule['january_february'] = crops[3:6]
            schedule['march_april'] = crops[6:]
        
        return schedule
    
    def _calculate_irigation_needs(self, rainfall, temperature):
        """Calculate irrigation requirements"""
        if rainfall > 100 and temperature > 25:
            return 'High - Regular irrigation needed'
        elif rainfall > 50:
            return 'Medium - Supplemental irrigation'
        else:
            return 'Low - Minimal irrigation'
    
    def get_model_info(self):
        """Get model information"""
        return {
            'model_type': self.model_type,
            'input_features': ['temperature', 'rainfall', 'humidity', 'wind_speed', 'season'],
            'output_classes': self.crop_classes,
            'description': 'Simple rule-based weather optimization model',
            'dependencies': 'numpy, pandas, pathlib, os'
        }
    
    def save_model(self, filepath='models/weather_optimization_simple.h5'):
        """Save model info"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save model metadata
        model_info = self.get_model_info()
        with open(filepath.replace('.h5', '_info.json'), 'w') as f:
            import json
            json.dump(model_info, f, indent=2)
        
        print(f"✅ Simple weather optimization model saved to {filepath}")
        return True

# Initialize model
if __name__ == "__main__":
    print("🌤 Creating Simple Weather Optimization Model...")
    model = SimpleWeatherOptimizationModel()
    model.save_model()
    print("✅ Simple weather optimization model created successfully!")
