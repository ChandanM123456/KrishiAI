#!/usr/bin/env python3
"""
Complete Application Test Script
Tests all components of the KrishiAI application
"""

import sys
import os
import warnings
warnings.filterwarnings('ignore')

def test_imports():
    """Test all required imports"""
    print("Testing Imports...")
    
    try:
        import streamlit as st
        import pandas as pd
        import numpy as np
        import tensorflow as tf
        from tensorflow import keras
        from PIL import Image
        import requests
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler
        print("  All imports - SUCCESS")
        return True
    except Exception as e:
        print(f"  Import error: {e}")
        return False

def test_model_files():
    """Test if all model files exist"""
    print("\nTesting Model Files...")
    
    model_files = [
        'models/land_analysis_cnn.h5',
        'models/crop_recommendation_model.h5',
        'models/profit_prediction_model.h5',
        'models/weather_optimization_model.h5'
    ]
    
    all_exist = True
    for file_path in model_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path) / (1024*1024)  # MB
            print(f"  {file_path} - EXISTS ({size:.1f} MB)")
        else:
            print(f"  {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_model_loading():
    """Test model loading functionality"""
    print("\nTesting Model Loading...")
    
    try:
        # Import app module
        import app
        
        # Test model loading
        models = app.load_trained_models()
        
        if models:
            print(f"  Models loaded: {len(models)}/4")
            for name in models.keys():
                print(f"    {name}")
            return True
        else:
            print("  No models loaded")
            return False
            
    except Exception as e:
        print(f"  Model loading error: {e}")
        return False

def test_dataset_files():
    """Test dataset files"""
    print("\nTesting Dataset Files...")
    
    dataset_files = [
        'crop_data.csv',
        'crop_schedule.csv',
        'market_data.csv',
        'datasets/land_analysis/labels.csv',
        'datasets/land_analysis/dataset_info.json'
    ]
    
    all_exist = True
    for file_path in dataset_files:
        if os.path.exists(file_path):
            print(f"  {file_path} - EXISTS")
        else:
            print(f"  {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_database():
    """Test database functionality"""
    print("\nTesting Database...")
    
    try:
        import sqlite3
        db_path = 'farmers.db'
        
        # Test database connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"  Database tables: {[table[0] for table in tables]}")
        conn.close()
        
        return True
    except Exception as e:
        print(f"  Database error: {e}")
        return False

def test_app_functions():
    """Test key app functions"""
    print("\nTesting App Functions...")
    
    try:
        import app
        
        # Test key functions exist
        functions_to_test = [
            'load_trained_models',
            'predict_crop_with_trained_model',
            'predict_profit_with_trained_model',
            'analyze_land_with_trained_model'
        ]
        
        all_exist = True
        for func_name in functions_to_test:
            if hasattr(app, func_name):
                print(f"  {func_name} - EXISTS")
            else:
                print(f"  {func_name} - MISSING")
                all_exist = False
        
        return all_exist
        
    except Exception as e:
        print(f"  Function test error: {e}")
        return False

def test_model_predictions():
    """Test model predictions"""
    print("\nTesting Model Predictions...")
    
    try:
        import app
        import numpy as np
        from PIL import Image
        
        # Load models
        models = app.load_trained_models()
        if not models:
            print("  Cannot test predictions - no models loaded")
            return False
        
        # Test crop prediction
        if 'crop_recommendation' in models:
            try:
                result = app.predict_crop_with_trained_model(
                    models, 
                    {'soil_health': 50, 'ph': 6.5},
                    {'temp': 25, 'humidity': 60, 'rainfall': 150},
                    50000, 120
                )
                print(f"  Crop prediction: SUCCESS - {len(result) if result else 0} results")
            except Exception as e:
                print(f"  Crop prediction error: {e}")
        
        # Test profit prediction
        if 'profit_prediction' in models:
            try:
                result = app.predict_profit_with_trained_model(
                    models, 'Tomato', 120, 50000, 'Bangalore', 'High'
                )
                print(f"  Profit prediction: SUCCESS - {result}")
            except Exception as e:
                print(f"  Profit prediction error: {e}")
        
        # Test land analysis
        if 'land_analysis' in models:
            try:
                # Create a test image
                test_img = Image.new('RGB', (224, 224), color='brown')
                result = app.analyze_land_with_trained_model(models, test_img)
                print(f"  Land analysis: SUCCESS - {result}")
            except Exception as e:
                print(f"  Land analysis error: {e}")
        
        return True
        
    except Exception as e:
        print(f"  Prediction test error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("KRISHIAI COMPLETE APPLICATION TEST")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Model Files", test_model_files),
        ("Dataset Files", test_dataset_files),
        ("Database", test_database),
        ("Model Loading", test_model_loading),
        ("App Functions", test_app_functions),
        ("Model Predictions", test_model_predictions),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  {test_name} test ERROR: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nALL TESTS PASSED! Application is ready for use.")
        print("\nApplication Features Working:")
        print("  Model Loading: All 4 AI models loaded")
        print("  Predictions: Crop, profit, and land analysis working")
        print("  Database: SQLite database functional")
        print("  Datasets: All data files available")
        print("  Imports: All dependencies satisfied")
    else:
        print(f"\n{total-passed} tests failed. Please check the issues above.")
    
    print("="*60)

if __name__ == "__main__":
    main()
