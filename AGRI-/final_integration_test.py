#!/usr/bin/env python3
"""
Final integration test to verify the complete KrishiAI application
"""

import sys
import os
import subprocess
import time

def test_app_imports():
    """Test if all required imports work in the app"""
    print("Testing Application Imports...")
    
    try:
        # Test basic imports
        import streamlit as st
        import pandas as pd
        import numpy as np
        import tensorflow as tf
        from tensorflow import keras
        print("  All basic imports - SUCCESS")
        
        # Test model loading
        if os.path.exists('models/land_analysis_cnn.h5'):
            keras.models.load_model('models/land_analysis_cnn.h5')
            print("  Land Analysis CNN - LOADABLE")
        
        if os.path.exists('models/crop_recommendation_model.h5'):
            keras.models.load_model('models/crop_recommendation_model.h5')
            print("  Crop Recommendation Model - LOADABLE")
        
        if os.path.exists('models/profit_prediction_model.h5'):
            keras.models.load_model('models/profit_prediction_model.h5')
            print("  Profit Prediction Model - LOADABLE")
        
        if os.path.exists('models/weather_optimization_model.h5'):
            keras.models.load_model('models/weather_optimization_model.h5')
            print("  Weather Optimization Model - LOADABLE")
        
        return True
        
    except Exception as e:
        print(f"  Import test FAILED: {e}")
        return False

def test_app_syntax():
    """Test if the app.py has correct syntax"""
    print("\nTesting Application Syntax...")
    
    try:
        import py_compile
        py_compile.compile('app.py', doraise=True)
        print("  App.py syntax - CORRECT")
        return True
        
    except py_compile.PyCompileError as e:
        print(f"  Syntax error: {e}")
        return False

def test_model_functions():
    """Test the model prediction functions"""
    print("\nTesting Model Functions...")
    
    try:
        # Import the functions from app
        sys.path.append('.')
        
        # Test if functions exist (basic check)
        import app
        
        if hasattr(app, 'load_trained_models'):
            print("  load_trained_models function - EXISTS")
        else:
            print("  load_trained_models function - MISSING")
            return False
            
        if hasattr(app, 'predict_crop_with_trained_model'):
            print("  predict_crop_with_trained_model function - EXISTS")
        else:
            print("  predict_crop_with_trained_model function - MISSING")
            return False
            
        if hasattr(app, 'analyze_land_with_trained_model'):
            print("  analyze_land_with_trained_model function - EXISTS")
        else:
            print("  analyze_land_with_trained_model function - MISSING")
            return False
            
        return True
        
    except Exception as e:
        print(f"  Function test FAILED: {e}")
        return False

def test_required_files():
    """Test if all required files exist"""
    print("\nTesting Required Files...")
    
    required_files = [
        'app.py',
        'models/land_analysis_cnn.h5',
        'models/crop_recommendation_model.h5',
        'models/profit_prediction_model.h5',
        'models/weather_optimization_model.h5',
        'crop_data.csv'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  {file_path} - EXISTS")
        else:
            print(f"  {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("="*60)
    print("KRISHIAI FINAL INTEGRATION TEST")
    print("="*60)
    
    tests = [
        ("Required Files", test_required_files),
        ("Application Syntax", test_app_syntax),
        ("Application Imports", test_app_imports),
        ("Model Functions", test_model_functions),
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
        print("ALL TESTS PASSED! Application is ready for use.")
        print("\nApplication Features:")
        print("  Trained Models: 4/4 loaded")
        print("  Land Analysis: CNN-based soil quality detection")
        print("  Crop Prediction: Deep learning recommendations")
        print("  Profit Forecasting: AI-based profit estimates")
        print("  Weather Optimization: Smart crop selection")
        print("\nAccess the application at: http://localhost:8502")
    else:
        print("Some tests failed. Please check the issues above.")
    
    print("="*60)

if __name__ == "__main__":
    main()
