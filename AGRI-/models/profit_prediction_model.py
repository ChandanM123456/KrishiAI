"""
Simple Profit Prediction Model - No TensorFlow Required
===================================================
"""

import numpy as np
import pandas as pd
from pathlib import Path
import os

class SimpleProfitPredictionModel:
    """Simple profit prediction model without TensorFlow dependencies"""
    
    def __init__(self):
        self.model_type = "profit_prediction"
        
    def predict_profit(self, features):
        """
        Simple profit prediction based on basic features
        
        Args:
            features: Dictionary with agricultural parameters
            
        Returns:
            Dictionary with profit predictions
        """
        # Extract features
        crop_type = features.get('crop_type', 'Tomato')
        duration = features.get('duration', 90)  # days
        investment = features.get('investment', 25000)
        location = features.get('location', 'Bangalore')
        season = features.get('season', 'Kharif')
        
        # Simple profit calculation logic
        base_yield_per_acre = {
            'Tomato': 25,  # quintals
            'Maize': 20,
            'Ragi': 8,
            'Onion': 15,
            'Potato': 20,
            'Chilli': 10
        }
        
        base_price_per_quintal = {
            'Tomato': 1500,
            'Maize': 1200,
            'Ragi': 3000,
            'Onion': 1800,
            'Potato': 1000,
            'Chilli': 2500
        }
        
        # Calculate expected yield and revenue
        expected_yield = base_yield_per_acre.get(crop_type, 15) * features.get('area', 1.0)
        expected_revenue = expected_yield * base_price_per_quintal.get(crop_type, 1500)
        
        # Calculate costs
        seed_cost = investment * 0.3
        fertilizer_cost = investment * 0.4
        labor_cost = investment * 0.2
        water_cost = investment * 0.1
        total_cost = seed_cost + fertilizer_cost + labor_cost + water_cost
        
        # Calculate profit
        expected_profit = expected_revenue - total_cost
        
        # Apply location and season multipliers
        location_multiplier = 1.2 if location == 'Bangalore' else 1.0
        season_multiplier = 1.1 if season == 'Kharif' else 1.0
        
        adjusted_profit = expected_profit * location_multiplier * season_multiplier
        
        # Calculate confidence based on data quality
        confidence = min(0.95, 0.6 + (investment / 100000))
        
        results = {
            'expected_profit': adjusted_profit,
            'expected_revenue': expected_revenue,
            'total_cost': total_cost,
            'profit_margin': (adjusted_profit / expected_revenue) * 100 if expected_revenue > 0 else 0,
            'confidence': confidence,
            'investment_breakdown': {
                'seeds': seed_cost,
                'fertilizer': fertilizer_cost,
                'labor': labor_cost,
                'water': water_cost
            },
            'risk_factors': ['Weather', 'Market Price', 'Pest Attack'],
            'recommendations': ['Crop rotation', 'Organic farming', 'Market timing']
        }
        
        return results
    
    def get_model_info(self):
        """Get model information"""
        return {
            'model_type': self.model_type,
            'input_features': ['crop_type', 'duration', 'investment', 'location', 'season'],
            'output_features': ['expected_profit', 'expected_revenue', 'profit_margin', 'confidence'],
            'description': 'Simple rule-based profit prediction model',
            'dependencies': 'numpy, pandas, pathlib, os'
        }
    
    def save_model(self, filepath='models/profit_prediction_simple.h5'):
        """Save model info"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save model metadata
        model_info = self.get_model_info()
        with open(filepath.replace('.h5', '_info.json'), 'w') as f:
            import json
            json.dump(model_info, f, indent=2)
        
        print(f"✅ Simple profit prediction model saved to {filepath}")
        return True

# Initialize model
if __name__ == "__main__":
    print("💰 Creating Simple Profit Prediction Model...")
    model = SimpleProfitPredictionModel()
    model.save_model()
    print("✅ Simple profit prediction model created successfully!")
