# AI Models Directory

This directory contains trained machine learning models for KrishiAI Pro.

## Model Files:
- `land_analysis_cnn.h5` - CNN model for land analysis
- `crop_recommendation_model.h5` - ML model for crop recommendations  
- `profit_prediction_model.h5` - Model for profit forecasting
- `weather_optimization_model.h5` - Model for weather-based optimization

## Training:
Run `python train_model.py` to train these models with your agricultural data.

## Deployment:
Models are automatically loaded when TensorFlow is available.
If TensorFlow is not available, the app gracefully degrades to core functionality.
