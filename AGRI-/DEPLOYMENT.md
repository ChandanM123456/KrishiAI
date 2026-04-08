# 🚀 KrishiAI Pro - Deployment Guide

## 📋 Overview

KrishiAI Pro is an advanced AI-powered agricultural assistant that helps farmers with:
- 🌱 Land analysis using CNN models
- 🌾 Crop recommendations with ML predictions  
- 💰 Profit forecasting and market insights
- 📊 Advanced selling strategies and marketing insights
- 📅 Farming schedule management
- 🛒 Shopping recommendations and market locations

## 🌐 Streamlit Cloud Deployment

### Quick Start (Recommended)

**For Streamlit Cloud deployment without TensorFlow dependencies:**

```bash
# Clone the repository
git clone https://github.com/ChandanM123456/KrishiAI.git
cd KrishiAI/AGRI-

# Deploy to Streamlit Cloud (uses packages.txt by default)
streamlit deploy
```

### With TensorFlow AI Features

**If you want full AI features in Streamlit Cloud:**

1. **Install TensorFlow locally first:**
```bash
pip install tensorflow>=2.10.0 keras>=2.10.0
```

2. **Then deploy with full requirements:**
```bash
# Copy full requirements to packages.txt
cp requirements.txt packages.txt
streamlit deploy
```

### Requirements Files

- **`packages.txt`**: Core dependencies only (for Streamlit Cloud)
- **`requirements.txt`**: All dependencies including TensorFlow (for local/full deployment)
- **`requirements-cloud.txt`**: Cloud-specific without TensorFlow (alternative)

### TensorFlow Handling

The application gracefully handles TensorFlow absence:
- ✅ **Core Features**: Shopping, marketing, calendar all work perfectly
- ✅ **Beautiful Design**: Professional backgrounds and text colors
- ✅ **No Crashes**: Graceful degradation when TensorFlow unavailable
- ✅ **User Warnings**: Clear messages about disabled AI features

## 🐳 Docker Deployment

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/ChandanM123456/KrishiAI.git
cd KrishiAI/AGRI-

# Build and run with Docker
docker build -t krishiai-pro .
docker run -p 8501:8501 -v $(pwd)/datasets:/app/datasets krishiai-pro
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  krishiai:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./datasets:/app/datasets
      - ./models:/app/models
      - ./farmers.db:/app/farmers.db
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## ☸️ Kubernetes Deployment

### Deploy to Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s-deployment.yaml

# Check deployment status
kubectl get pods -l app=krishiai

# Get service URL
kubectl get service krishiai
```

### Kubernetes Manifest

The application includes a pre-configured Kubernetes manifest with:
- **3 replicas** for high availability
- **Resource limits** (512Mi memory, 250m CPU requests)
- **Health checks** for automatic restarts
- **Environment variables** for configuration

## 🌐 Cloud Deployment Options

### 1. Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### 2. Heroku

```bash
# Install Heroku CLI
heroku login

# Create app
heroku create krishiai-pro

# Set buildpack
heroku buildpacks:set heroku/python

# Deploy
git subtree push --prefix AGRI- heroku main
```

### 3. AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p "Python 3.9"

# Deploy
eb create krishiai-pro-production
```

### 4. Google Cloud Platform

```bash
# Install gcloud CLI
gcloud init

# Deploy to Cloud Run
gcloud run deploy krishiai-pro --source . --platform python
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STREAMLIT_SERVER_PORT` | 8501 | Application port |
| `STREAMLIT_SERVER_ADDRESS` | 0.0.0.0 | Server address |
| `STREAMLIT_SERVER_HEADLESS` | true | Run in headless mode |
| `DATABASE_URL` | sqlite:///farmers.db | Database connection |

### Model Configuration

Ensure these model files are present:
- `models/land_analysis_cnn.h5` (324 MB)
- `models/crop_recommendation_model.h5` (12 MB)
- `models/profit_prediction_model.h5` (8 MB)
- `models/weather_optimization_model.h5` (6 MB)

### Dataset Requirements

Required datasets:
- `datasets/land_analysis/` (450 labeled images)
- `crop_data.csv` (Crop information)
- `market_data.csv` (Market prices)
- `crop_schedule.csv` (Farming schedules)

## 🔒 Security Configuration

### Production Security

1. **Enable Authentication**
   - User registration and login
   - Session management
   - Password requirements (min 8 characters)

2. **Data Protection**
   - HTTPS enforcement
   - SQL injection prevention
   - Input validation and sanitization

3. **Access Control**
   - Rate limiting
   - CORS configuration
   - File upload restrictions

### SSL/HTTPS Setup

#### Nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoring & Logging

### Application Monitoring

1. **Health Check Endpoint**
   - URL: `/health`
   - Returns application status
   - Monitors model loading and database connectivity

2. **Logging Configuration**
   - Log level: INFO
   - Log file: `krishiai.log`
   - Log rotation: Daily

3. **Performance Metrics**
   - Response time monitoring
   - Error rate tracking
   - User activity analytics

### Monitoring Stack

```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  krishiai:
    build: .
    ports:
      - "8501:8501"
  
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy KrishiAI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r AGRI-/requirements.txt
      - name: Run tests
        run: |
          cd AGRI-
          python test_complete_app.py
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          # Add your deployment commands here
          echo "Deploying to production..."
```

## 📱 Mobile App Deployment

### Progressive Web App (PWA)

The application can be deployed as a PWA:
- Offline functionality support
- Mobile-optimized interface
- App-like experience
- Push notifications for price alerts

### React Native Integration

```bash
# Create React Native app
npx react-native init KrishiAI-Mobile

# Integrate with backend API
npm install axios
npm install @react-navigation/native
```

## 🌍 Multi-Region Deployment

### India Region
- **Primary**: Mumbai, Delhi, Bangalore
- **CDN**: CloudFlare India
- **Database**: Mumbai region

### Global Deployment
- **Asia**: Singapore, Tokyo
- **Europe**: Frankfurt, London
- **US**: Virginia, Oregon

## 💰 Pricing & Monetization

### Freemium Model
- **Free**: Basic land analysis, 3 predictions/month
- **Premium**: ₹299/month - Unlimited predictions, advanced insights
- **Enterprise**: ₹999/month - API access, custom models

### API Integration
```python
# Example API usage
import requests

response = requests.post('https://api.krishiai.com/v1/analyze-land', {
    'api_key': 'your-api-key',
    'image_url': 'https://example.com/field.jpg'
})
```

## 🔧 Troubleshooting

### Common Issues

1. **Model Loading Errors**
   ```bash
   # Check model files
   ls -la models/
   # Verify Git LFS
   git lfs pull
   ```

2. **Database Connection Issues**
   ```bash
   # Check database permissions
   ls -la farmers.db
   # Test connection
   sqlite3 farmers.db ".tables"
   ```

3. **Memory Issues**
   ```bash
   # Monitor memory usage
   docker stats krishiai
   # Increase memory limit
   docker run --memory=2g krishiai-pro
   ```

### Performance Optimization

1. **Model Caching**
   - Enable model caching in production
   - Pre-load models at startup
   - Use GPU acceleration if available

2. **Database Optimization**
   - Add indexes to frequently queried columns
   - Implement connection pooling
   - Regular database maintenance

3. **Frontend Optimization**
   - Lazy loading for large datasets
   - Image optimization and compression
   - Minimize CSS and JavaScript

## 📞 Support

### Documentation
- **User Guide**: [Link to documentation]
- **API Docs**: [Link to API documentation]
- **Video Tutorials**: [Link to YouTube channel]

### Community Support
- **GitHub Issues**: [Link to issues page]
- **Discord Community**: [Link to Discord server]
- **WhatsApp Support**: +91-XXXXXXXXXX

---

## 🎯 Quick Deployment Commands

```bash
# 1. Clone and setup
git clone https://github.com/ChandanM123456/KrishiAI.git
cd KrishiAI/AGRI-
git lfs install
git lfs pull

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run locally (for testing)
streamlit run app.py

# 4. Deploy with Docker
docker build -t krishiai-pro .
docker run -p 8501:8501 krishiai-pro

# 5. Access application
# Open browser to http://localhost:8501
```

**🌾 Happy Farming with KrishiAI Pro!**

---

*Last Updated: April 2026*
*Version: 2.0.0*
