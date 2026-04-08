# KrishiAI - AI-Powered Farming Assistant

An intelligent farming assistant that uses deep learning models to provide crop recommendations, profit predictions, land analysis, and weather-based optimization.

## Features

### AI Models
- **Crop Recommendation Model**: Suggests optimal crops based on soil conditions, weather, and budget
- **Profit Prediction Model**: Forecasts potential profits based on crop type, duration, and investment
- **Weather Optimization Model**: Recommends crops based on weather conditions
- **Land Analysis CNN**: Analyzes land images to determine soil quality (Note: Large file, not in repo)

### Application Features
- Real-time weather integration
- Land image analysis with AI
- Comprehensive farming plans
- Task scheduling and management
- Market insights and price predictions
- Shopping recommendations for farming supplies

## Setup Instructions

### Prerequisites
- Python 3.8+
- TensorFlow 2.12+
- Streamlit
- Required packages listed in requirements

### Installation

1. Clone the repository with Git LFS:
```bash
git clone https://github.com/ChandanM123456/KrishiAI.git
cd KrishiAI/AGRI-
git lfs install  # Install Git LFS for large model files
```

2. Install dependencies:
```bash
pip install streamlit pandas numpy tensorflow scikit-learn pillow requests
```

3. Train the models (if not already trained):
```bash
python train_model.py
```

4. Run the application:
```bash
streamlit run app.py
```

## Model Files

### Available Models (in repository):
- `models/crop_recommendation_model.h5` (635 KB) - Crop recommendations
- `models/profit_prediction_model.h5` (193 KB) - Profit predictions  
- `models/weather_optimization_model.h5` (80 KB) - Weather optimization

### Large Model (via Git LFS):
- `models/land_analysis_cnn.h5` (324 MB) - Land analysis CNN
  - Stored using Git Large File Storage (LFS)
  - Automatically downloaded when cloning repository
  - Requires Git LFS to be installed: `git lfs install`

## Usage

1. **Start the Application**: Run `streamlit run app.py`
2. **Upload Land Images**: Provide 3 images of your land (far, mid, close views)
3. **Enter Farm Details**: Add location, land area, and other parameters
4. **Get AI Recommendations**: Receive crop suggestions and profit forecasts
5. **Follow Farming Plan**: Get task schedules and shopping recommendations

## Model Training

The models are trained using synthetic data and can be retrained with:
```bash
python train_model.py
```

This will:
- Generate synthetic training data
- Train all 4 deep learning models
- Save models in the `models/` directory
- Provide training metrics and evaluation

## Architecture

- **Frontend**: Streamlit web application
- **Backend**: TensorFlow/Keras deep learning models
- **Data**: Synthetic data generation for training
- **API**: OpenWeatherMap for weather data
- **Storage**: SQLite for user data and farming plans

## Model Performance

- **Crop Recommendation**: High accuracy with confidence scores
- **Profit Prediction**: MSE-based regression model
- **Weather Optimization**: 98% confidence in recommendations
- **Land Analysis**: 83% confidence in soil quality detection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the models and application
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Check the model training logs
- Verify all model files are present
- Ensure TensorFlow is properly installed
- Test with the provided test scripts

---

**Note**: All models are now available in the repository. The land analysis CNN is stored using Git LFS for efficient handling of large files.