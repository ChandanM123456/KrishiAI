import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error
import os
import warnings
from PIL import Image
warnings.filterwarnings('ignore')

print("🌾 Starting Model Training for KrishiAI...")

# Import model classes
from land_analysis_model import (
    LandAnalysisCNN, 
    CropRecommendationModel, 
    ProfitPredictionModel, 
    WeatherCropOptimizationModel
)

# ============================================================
# DATA PREPARATION
# ============================================================

def prepare_crop_data():
    """Prepare crop recommendation data"""
    print("\n📊 Preparing Crop Recommendation Data...")
    
    # Load crop data
    try:
        df = pd.read_csv('crop_data.csv')
        print(f"  ✅ Loaded {len(df)} records from crop_data.csv")
    except:
        print("  ⚠️ No crop_data.csv found, generating synthetic data...")
        df = generate_synthetic_crop_data()
    
    # Define valid crops (matching the model's crop_classes)
    valid_crops = ['Tomato', 'Onion', 'Chilli', 'Cabbage', 'Maize', 'Potato',
                   'Sugarcane', 'Cotton', 'Rice', 'Groundnut', 'Ragi', 'Wheat']
    
    # Filter data to only include valid crops
    df = df[df['crop'].isin(valid_crops)].copy()
    print(f"  📈 Filtered to {len(df)} records with valid crops")
    
    # If no valid crops, generate synthetic data
    if len(df) < 10:
        print("  ⚠️ Not enough valid crop data, generating synthetic data...")
        df = generate_synthetic_crop_data()
    
    # Encode categorical variables
    le_soil = LabelEncoder()
    le_water = LabelEncoder()
    le_location = LabelEncoder()
    le_crop = LabelEncoder()
    
    df['soil_encoded'] = le_soil.fit_transform(df['soil'])
    df['water_encoded'] = le_water.fit_transform(df['water'])
    df['location_encoded'] = le_location.fit_transform(df['location'])
    df['crop_encoded'] = le_crop.fit_transform(df['crop'])
    
    # Prepare features - need 10 features to match model input shape
    features = ['location_encoded', 'soil_encoded', 'water_encoded', 'budget', 'duration_days']
    X = df[features].values
    
    # Add 5 more features to reach 10 (using synthetic data for missing features)
    additional_features = np.random.rand(len(X), 5)  # Random values for missing features
    X = np.hstack([X, additional_features])
    
    y = keras.utils.to_categorical(df['crop_encoded'], num_classes=12)
    
    # Normalize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    return train_test_split(X, y, test_size=0.2, random_state=42), (le_soil, le_water, le_location, le_crop, scaler)

def generate_synthetic_crop_data():
    """Generate synthetic crop data for training"""
    np.random.seed(42)
    
    locations = ['Bangalore', 'Mysore', 'Tumkur', 'Mandya', 'Hassan', 'Hubli', 'Belgaum']
    soils = ['Poor', 'Average', 'Good']
    waters = ['Low', 'Medium', 'High']
    crops = ['Tomato', 'Onion', 'Chilli', 'Cabbage', 'Maize', 'Potato', 'Sugarcane', 'Cotton', 'Rice', 'Groundnut', 'Ragi', 'Wheat']
    
    data = []
    for _ in range(500):
        location = np.random.choice(locations)
        soil = np.random.choice(soils)
        water = np.random.choice(waters)
        crop = np.random.choice(crops)
        budget = np.random.randint(10000, 80000)
        duration = np.random.randint(60, 300)
        profit = int(budget * np.random.uniform(0.5, 1.5))
        demand = np.random.choice(['Low', 'Medium', 'High'])
        yield_per_acre = np.random.randint(1000, 50000)
        
        data.append([location, soil, water, budget, crop, duration, profit, demand, yield_per_acre])
    
    return pd.DataFrame(data, columns=['location', 'soil', 'water', 'budget', 'crop', 'duration_days', 'profit', 'demand', 'yield_per_acre'])

def prepare_profit_data():
    """Prepare profit prediction data"""
    print("\n💰 Preparing Profit Prediction Data...")
    
    try:
        df = pd.read_csv('crop_data.csv')
    except:
        df = generate_synthetic_crop_data()
    
    # Encode categorical variables
    le_crop = LabelEncoder()
    le_location = LabelEncoder()
    le_demand = LabelEncoder()
    
    df['crop_encoded'] = le_crop.fit_transform(df['crop'])
    df['location_encoded'] = le_location.fit_transform(df['location'])
    df['demand_encoded'] = le_demand.fit_transform(df['demand'])
    
    # Prepare features - need 8 features to match model input shape
    features = ['crop_encoded', 'duration_days', 'budget', 'location_encoded', 'demand_encoded', 'yield_per_acre']
    X = df[features].values
    
    # Add 2 more features to reach 8 (using synthetic data for missing features)
    additional_features = np.random.rand(len(X), 2)  # Random values for missing features
    X = np.hstack([X, additional_features])
    
    y = df['profit'].values
    
    # Normalize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    return train_test_split(X, y, test_size=0.2, random_state=42), (le_crop, le_location, le_demand, scaler)

def prepare_weather_data():
    """Prepare weather optimization data"""
    print("\n🌤️ Preparing Weather Optimization Data...")
    
    # Generate synthetic weather data
    np.random.seed(42)
    n_samples = 300
    
    # Weather features: rainfall, temperature, humidity, wind_speed, season, soil_moisture
    rainfall = np.random.uniform(50, 300, n_samples)  # mm
    temperature = np.random.uniform(15, 35, n_samples)  # Celsius
    humidity = np.random.uniform(30, 90, n_samples)  # %
    wind_speed = np.random.uniform(5, 25, n_samples)  # km/h
    season = np.random.randint(1, 4, n_samples)  # 1=Summer, 2=Monsoon, 3=Winter
    soil_moisture = np.random.uniform(20, 80, n_samples)  # %
    
    # Crop recommendations based on weather conditions
    crops = ['Tomato', 'Onion', 'Chilli', 'Cabbage', 'Maize', 'Potato', 'Sugarcane', 'Cotton', 'Rice', 'Groundnut', 'Ragi', 'Wheat']
    crop_labels = []
    
    for i in range(n_samples):
        if rainfall > 200 and temperature < 25:
            crop_labels.append('Rice')  # Water-loving crops
        elif temperature > 30 and rainfall < 100:
            crop_labels.append('Cotton')  # Heat-tolerant crops
        elif season == 2:  # Monsoon
            crop_labels.append(np.random.choice(['Maize', 'Sugarcane', 'Groundnut']))
        elif season == 3:  # Winter
            crop_labels.append(np.random.choice(['Wheat', 'Potato', 'Onion']))
        else:  # Summer
            crop_labels.append(np.random.choice(['Tomato', 'Chilli', 'Cabbage']))
    
    # Create DataFrame
    df = pd.DataFrame({
        'rainfall': rainfall,
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'season': season,
        'soil_moisture': soil_moisture,
        'crop': crop_labels
    })
    
    # Encode crop labels
    le_crop = LabelEncoder()
    df['crop_encoded'] = le_crop.fit_transform(df['crop'])
    
    # Prepare features
    features = ['rainfall', 'temperature', 'humidity', 'wind_speed', 'season', 'soil_moisture']
    X = df[features].values
    y = keras.utils.to_categorical(df['crop_encoded'], num_classes=12)
    
    # Normalize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    return train_test_split(X, y, test_size=0.2, random_state=42), (le_crop, scaler)

# ============================================================
# MODEL TRAINING FUNCTIONS
# ============================================================

def train_land_analysis_model():
    """Train the Land Analysis CNN model"""
    print("\n🔍 Training Land Analysis CNN Model...")
    
    # Check if dataset exists
    dataset_path = "datasets/land_analysis"
    if os.path.exists(dataset_path):
        print(f"  📁 Using dataset from: {dataset_path}")
        
        # Load dataset
        labels_file = os.path.join(dataset_path, "labels.csv")
        if os.path.exists(labels_file):
            labels_df = pd.read_csv(labels_file)
            print(f"  📊 Loaded {len(labels_df)} labeled images")
            
            # Prepare training data
            X_train = []
            y_train = []
            
            # Load training images
            train_labels = labels_df[labels_df['split'] == 'train']
            for _, row in train_labels.iterrows():
                img_path = os.path.join(dataset_path, "images", "train", row['soil_class'], row['filename'])
                if os.path.exists(img_path):
                    # Load and preprocess image
                    img = Image.open(img_path)
                    img = img.resize((224, 224))
                    img_array = np.array(img) / 255.0
                    X_train.append(img_array)
                    
                    # Convert soil class to numeric
                    class_map = {'poor': 0, 'average': 1, 'good': 2}
                    y_train.append(class_map[row['soil_class']])
            
            if len(X_train) == 0:
                print("  ⚠️ No training images found, falling back to synthetic data")
                use_synthetic = True
            else:
                print(f"  ✅ Loaded {len(X_train)} training images")
                X_train = np.array(X_train)
                y_train = keras.utils.to_categorical(y_train, num_classes=3)
                use_synthetic = False
        else:
            print("  ⚠️ Labels file not found, using synthetic data")
            use_synthetic = True
    else:
        print("  ⚠️ Dataset not found, using synthetic data")
        use_synthetic = True
    
    # Use synthetic data if no real data available
    if use_synthetic:
        print("  📸 Generating synthetic land image data...")
        X_train = np.random.rand(100, 224, 224, 3)  # 100 synthetic land images
        y_train = keras.utils.to_categorical(np.random.randint(0, 3, 100), num_classes=3)  # 3 soil quality classes
    
    # Create model
    model = LandAnalysisCNN()
    
    # Train model
    print("  🏋️ Training model...")
    history = model.model.fit(
        X_train, y_train,
        epochs=10,
        batch_size=16,
        validation_split=0.2,
        verbose=1
    )
    
    # Save model
    model.save_model()
    print("  ✅ Land Analysis CNN model trained and saved!")
    
    return model

def train_crop_recommendation_model():
    """Train the Crop Recommendation model"""
    print("\n🌱 Training Crop Recommendation Model...")
    
    # Prepare data
    (X_train, X_test, y_train, y_test), encoders = prepare_crop_data()
    
    # Create and train model
    model = CropRecommendationModel()
    
    print("  Training model...")
    history = model.model.fit(
        X_train, y_train,
        epochs=20,
        batch_size=16,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # Evaluate model
    y_pred = model.model.predict(X_test)
    accuracy = accuracy_score(np.argmax(y_test, axis=1), np.argmax(y_pred, axis=1))
    print(f"  Model Accuracy: {accuracy:.4f}")
    
    # Save model
    model.save_model()
    print("  Crop Recommendation model trained and saved!")
    
    return model, encoders

def train_profit_prediction_model():
    """Train the Profit Prediction model"""
    print("\n Training Profit Prediction Model...")
    
    # Prepare data
    (X_train, X_test, y_train, y_test), encoders = prepare_profit_data()
    
    # Create and train model
    model = ProfitPredictionModel()
    
    print("  Training model...")
    history = model.model.fit(
        X_train, y_train,
        epochs=20,
        batch_size=16,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # Evaluate model
    y_pred = model.model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"  Model MSE: {mse:.2f}")
    
    # Save model
    model.save_model()
    print("  Profit Prediction model trained and saved!")
    
    return model, encoders

def train_weather_optimization_model():
    """Train the Weather Optimization model"""
    print("\n Training Weather Optimization Model...")
    
    # Prepare data
    (X_train, X_test, y_train, y_test), encoders = prepare_weather_data()
    
    # Create and train model
    model = WeatherCropOptimizationModel()
    
    print("  Training model...")
    history = model.model.fit(
        X_train, y_train,
        epochs=20,
        batch_size=16,
        validation_data=(X_test, y_test),
        verbose=1
    )
    
    # Evaluate model
    y_pred = model.model.predict(X_test)
    accuracy = accuracy_score(np.argmax(y_test, axis=1), np.argmax(y_pred, axis=1))
    print(f"  Model Accuracy: {accuracy:.4f}")
    
    # Save model
    model.save_model()
    print("  ✅ Weather Optimization model trained and saved!")
    
    return model, encoders

# ============================================================
# MAIN TRAINING FUNCTION
# ============================================================

def main():
    """Main training function"""
    print("="*70)
    print("🌾 KRISHIAI MODEL TRAINING STARTED")
    print("="*70)
    
    try:
        # Train all models
        land_model = train_land_analysis_model()
        crop_model, crop_encoders = train_crop_recommendation_model()
        profit_model, profit_encoders = train_profit_prediction_model()
        weather_model, weather_encoders = train_weather_optimization_model()
        
        print("\n" + "="*70)
        print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
        print("="*70)
        print("\n📁 Models saved in 'models/' directory:")
        print("  🔹 land_analysis_cnn.h5")
        print("  🔹 crop_recommendation_model.h5")
        print("  🔹 profit_prediction_model.h5")
        print("  🔹 weather_optimization_model.h5")
        print("\n🎉 Training completed! Models are ready for use.")
        
    except Exception as e:
        print(f"\n❌ Error during training: {str(e)}")
        print("Please check the error and try again.")

if __name__ == "__main__":
    main()