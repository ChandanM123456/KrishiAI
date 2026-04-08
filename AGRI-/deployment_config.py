#!/usr/bin/env python3
"""
Deployment Configuration for KrishiAI Application
Contains all settings and configurations for production deployment
"""

import os
from pathlib import Path

# Deployment Settings
DEPLOYMENT_CONFIG = {
    "app_name": "KrishiAI Pro",
    "version": "2.0.0",
    "description": "Advanced AI-powered Agricultural Assistant",
    "author": "KrishiAI Team",
    
    # Server Configuration
    "server": {
        "host": "0.0.0.0",
        "port": 8501,
        "headless": False,
        "gather_usage_stats": False,
        "max_upload_size": 200,  # MB
        "enable_cors": True,
        "enable_xsrf": True
    },
    
    # Database Configuration
    "database": {
        "type": "SQLite",
        "path": "farmers.db",
        "backup_enabled": True,
        "backup_interval": "daily",
        "max_backups": 7
    },
    
    # Security Settings
    "security": {
        "enable_authentication": True,
        "session_timeout": 3600,  # 1 hour
        "max_login_attempts": 5,
        "password_min_length": 8,
        "enable_2fa": False
    },
    
    # Performance Settings
    "performance": {
        "enable_caching": True,
        "cache_ttl": 300,  # 5 minutes
        "max_concurrent_users": 100,
        "enable_compression": True
    },
    
    # Model Settings
    "models": {
        "land_analysis": "models/land_analysis_cnn.h5",
        "crop_recommendation": "models/crop_recommendation_model.h5",
        "profit_prediction": "models/profit_prediction_model.h5",
        "weather_optimization": "models/weather_optimization_model.h5",
        "model_cache_enabled": True
    },
    
    # Data Settings
    "data": {
        "datasets_path": "datasets/",
        "land_analysis_dataset": "datasets/land_analysis/",
        "crop_data": "crop_data.csv",
        "market_data": "market_data.csv",
        "auto_backup": True
    },
    
    # Monitoring Settings
    "monitoring": {
        "enable_logging": True,
        "log_level": "INFO",
        "log_file": "krishiai.log",
        "enable_metrics": True,
        "health_check_endpoint": "/health"
    }
}

# Production URLs
PRODUCTION_URLS = {
    "main_app": "https://krishiai.example.com",
    "api_docs": "https://krishiai.example.com/docs",
    "admin_panel": "https://krishiai.example.com/admin"
}

# Environment Variables
ENVIRONMENT_VARS = {
    "STREAMLIT_SERVER_PORT": "8501",
    "STREAMLIT_SERVER_ADDRESS": "0.0.0.0",
    "STREAMLIT_SERVER_HEADLESS": "true",
    "DATABASE_URL": "sqlite:///farmers.db"
}

# Docker Configuration
DOCKER_CONFIG = """
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for data and models
RUN mkdir -p datasets models logs

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8501/health || exit 1

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""

# Kubernetes Configuration
KUBERNETES_CONFIG = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: krishiai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: krishiai
  template:
    metadata:
      labels:
        app: krishiai
    spec:
      containers:
      - name: krishiai
        image: krishiai:latest
        ports:
        - containerPort: 8501
        env:
        - name: STREAMLIT_SERVER_PORT
          value: "8501"
        - name: STREAMLIT_SERVER_ADDRESS
          value: "0.0.0.0"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
"""

# Deployment Scripts
def create_dockerfile():
    """Create Dockerfile for deployment"""
    dockerfile_path = Path("Dockerfile")
    with open(dockerfile_path, 'w') as f:
        f.write(DOCKER_CONFIG)
    print(f"Dockerfile created at {dockerfile_path}")

def create_kubernetes_manifest():
    """Create Kubernetes manifest for deployment"""
    k8s_path = Path("k8s-deployment.yaml")
    with open(k8s_path, 'w') as f:
        f.write(KUBERNETES_CONFIG)
    print(f"Kubernetes manifest created at {k8s_path}")

def create_requirements_file():
    """Create requirements.txt for deployment"""
    requirements = [
        "streamlit>=1.35.0",
        "pandas>=2.1.0",
        "numpy>=1.22.0",
        "tensorflow>=2.12.0",
        "scikit-learn>=1.4.0",
        "Pillow>=9.0.0",
        "requests>=2.28.0",
        "sqlite3"
    ]
    
    req_path = Path("requirements.txt")
    with open(req_path, 'w') as f:
        for req in requirements:
            f.write(f"{req}\n")
    print(f"Requirements file created at {req_path}")

def setup_production_environment():
    """Setup production environment"""
    print("Setting up production environment...")
    
    # Create necessary directories
    directories = ["datasets", "models", "logs", "backups"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    # Create configuration files
    create_requirements_file()
    create_dockerfile()
    create_kubernetes_manifest()
    
    print("Production environment setup complete!")

if __name__ == "__main__":
    setup_production_environment()
