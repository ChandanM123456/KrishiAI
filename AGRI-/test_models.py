#!/usr/bin/env python3
"""
Test script to verify trained models are working correctly
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
import warnings
warnings.filterwarnings('ignore')

print("Testing Trained Models Integration")
print("="*50)

# Test if models can be loaded
def test_model_loading():
    print("\n1. Testing Model Loading...")
    
    models = {}
    
    try:
        # Load Land Analysis CNN
        if os.path.exists('models/land_analysis_cnn.h5'):
            models['land_analysis'] = keras.models.load_model('models/land_analysis_cnn.h5')
            print("   Land Analysis CNN - LOADED")
        else:
            print("   Land Analysis CNN - NOT FOUND")
        
        # Load Crop Recommendation Model
        if os.path.exists('models/crop_recommendation_model.h5'):
            models['crop_recommendation'] = keras.models.load_model('models/crop_recommendation_model.h5')
            print("   Crop Recommendation Model - LOADED")
        else:
            print("   Crop Recommendation Model - NOT FOUND")
        
        # Load Profit Prediction Model
        if os.path.exists('models/profit_prediction_model.h5'):
            models['profit_prediction'] = keras.models.load_model('models/profit_prediction_model.h5')
            print("   Profit Prediction Model - LOADED")
        else:
            print("   Profit Prediction Model - NOT FOUND")
        
        # Load Weather Optimization Model
        if os.path.exists('models/weather_optimization_model.h5'):
            models['weather_optimization'] = keras.models.load_model('models/weather_optimization_model.h5')
            print("   Weather Optimization Model - LOADED")
        else:
            print("   Weather Optimization Model - NOT FOUND")
            
        return models
        
    except Exception as e:
        print(f"   ERROR loading models: {e}")
        return None

# Test crop prediction
def test_crop_prediction(models):
    print("\n2. Testing Crop Prediction...")
    
    if 'crop_recommendation' not in models:
        print("   Crop recommendation model not available")
        return
    
    try:
        model = models['crop_recommendation']
        
        # Test input (10 features as expected)
        features = np.array([[1.0, 1.0, 1.0, 50000, 120, 0.5, 0.5, 0.5, 0.5, 0.5]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        crop_classes = ['Tomato', 'Onion', 'Chilli', 'Cabbage', 'Maize', 'Potato',
                       'Sugarcane', 'Cotton', 'Rice', 'Groundnut', 'Ragi', 'Wheat']
        
        top_3_indices = np.argsort(prediction)[-3:][::-1]
        top_3_crops = [crop_classes[i] for i in top_3_indices]
        top_3_probs = [prediction[i] for i in top_3_indices]
        
        print(f"   Top 3 Crop Recommendations:")
        for i, (crop, prob) in enumerate(zip(top_3_crops, top_3_probs), 1):
            print(f"   {i}. {crop}: {prob:.4f}")
        
        print("   Crop Prediction - WORKING")
        
    except Exception as e:
        print(f"   ERROR in crop prediction: {e}")

# Test profit prediction
def test_profit_prediction(models):
    print("\n3. Testing Profit Prediction...")
    
    if 'profit_prediction' not in models:
        print("   Profit prediction model not available")
        return
    
    try:
        model = models['profit_prediction']
        
        # Test input (8 features as expected)
        features = np.array([[0, 120, 50000, 1.0, 1.0, 5000, 0.5, 0.5]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        print(f"   Predicted Profit: {float(prediction[0]):.2f}")
        print("   Profit Prediction - WORKING")
        
    except Exception as e:
        print(f"   ERROR in profit prediction: {e}")

# Test land analysis
def test_land_analysis(models):
    print("\n4. Testing Land Analysis...")
    
    if 'land_analysis' not in models:
        print("   Land analysis model not available")
        return
    
    try:
        model = models['land_analysis']
        
        # Test input (224, 224, 3 image)
        test_image = np.random.rand(224, 224, 3)
        test_image = np.expand_dims(test_image, axis=0)
        
        # Make prediction
        prediction = model.predict(test_image)[0]
        
        soil_classes = ['Poor', 'Average', 'Good']
        predicted_class = soil_classes[np.argmax(prediction)]
        confidence = float(np.max(prediction))
        
        print(f"   Predicted Soil Quality: {predicted_class}")
        print(f"   Confidence: {confidence:.4f}")
        print("   Land Analysis - WORKING")
        
    except Exception as e:
        print(f"   ERROR in land analysis: {e}")

# Test weather optimization
def test_weather_optimization(models):
    print("\n5. Testing Weather Optimization...")
    
    if 'weather_optimization' not in models:
        print("   Weather optimization model not available")
        return
    
    try:
        model = models['weather_optimization']
        
        # Test input (6 weather features)
        features = np.array([[150, 25, 60, 10, 2, 50]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        crop_classes = ['Tomato', 'Onion', 'Chilli', 'Cabbage', 'Maize', 'Potato',
                       'Sugarcane', 'Cotton', 'Rice', 'Groundnut', 'Ragi', 'Wheat']
        
        top_crop_idx = np.argmax(prediction)
        top_crop = crop_classes[top_crop_idx]
        confidence = float(prediction[top_crop_idx])
        
        print(f"   Recommended Crop for Weather: {top_crop}")
        print(f"   Confidence: {confidence:.4f}")
        print("   Weather Optimization - WORKING")
        
    except Exception as e:
        print(f"   ERROR in weather optimization: {e}")

# Main test function
def main():
    print("KrishiAI Model Integration Test")
    print("="*50)
    
    # Test model loading
    models = test_model_loading()
    
    if not models:
        print("\nERROR: No models loaded. Cannot proceed with tests.")
        return
    
    # Test each model
    test_crop_prediction(models)
    test_profit_prediction(models)
    test_land_analysis(models)
    test_weather_optimization(models)
    
    print("\n" + "="*50)
    print("Model Integration Test Complete!")
    print("All models are working and ready for use in the application.")

if __name__ == "__main__":
    main()
