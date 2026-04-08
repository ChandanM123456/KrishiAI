import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
import base64

# Import essential functions for cloud deployment
def get_translated_text(key, language):
    """Simple translation function for cloud deployment"""
    translations = {
        'english': {
            'dashboard': 'Dashboard',
            'upload': 'Upload Land',
            'results': 'Crop Recommendations',
            'schedule': 'Farming Schedule',
            'shopping': 'Shopping Requirements',
            'marketing': 'Marketing & Selling',
            'market': 'Market Insights',
            'selling_strategy': 'Selling Strategy',
            'government_subsidy': 'Government Subsidies',
            'profile': 'Profile'
        }
    }
    return translations.get(language, {}).get(key, key)

def get_mock_weather_data():
    """Mock weather data for cloud deployment"""
    return {
        'temperature': 28,
        'humidity': 65,
        'rainfall': 120,
        'forecast': 'Sunny conditions expected'
    }

def get_mock_crop_recommendations():
    """Mock crop recommendations for cloud deployment"""
    return [
        {'name': 'Tomato', 'yield': '25-35 q/ha', 'profit': '₹50k-₹80k'},
        {'name': 'Maize', 'yield': '20-30 q/ha', 'profit': '₹40k-₹60k'},
        {'name': 'Ragi', 'yield': '8-12 q/ha', 'profit': '₹30k-₹45k'},
        {'name': 'Okra', 'yield': '15-25 q/ha', 'profit': '₹35k-₹55k'}
    ]

def get_mock_shopping_requirements(crop, area):
    """Mock shopping requirements for cloud deployment"""
    return {
        'seeds': {'name': f'{crop} Seeds', 'quantity': f'{area * 2} kg', 'price': 500},
        'fertilizer': {'name': 'NPK Fertilizer', 'quantity': f'{area * 3} bags', 'price': 1500},
        'tools': {'name': 'Farming Tools', 'quantity': '1 set', 'price': 2000}
    }

def get_mock_market_prices():
    """Mock market prices for cloud deployment"""
    return {
        'Tomato': {'min': 20, 'max': 35, 'avg': 28, 'demand': 'High'},
        'Maize': {'min': 18, 'max': 25, 'avg': 22, 'demand': 'Medium'},
        'Ragi': {'min': 25, 'max': 40, 'avg': 33, 'demand': 'High'},
        'Okra': {'min': 30, 'max': 45, 'avg': 38, 'demand': 'High'}
    }

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'language' not in st.session_state:
    st.session_state.language = 'english'
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'crop' not in st.session_state:
    st.session_state.crop = None
if 'farming_plan' not in st.session_state:
    st.session_state.farming_plan = None

# Database initialization
conn = sqlite3.connect(":memory:", check_same_thread=False)
c = conn.cursor()

# Streamlit Community Cloud App
def main():
    # Custom CSS for professional appearance
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
            color: #1e3a8a;
        }
        h1, h2, h3 {
            color: #1e3a8a;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #1e3a8a;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .stButton button {
            background: linear-gradient(45deg, #3b82f6, #2563eb);
            color: white;
            border-radius: 10px;
            padding: 12px 24px;
            border: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background: linear-gradient(45deg, #2563eb, #1d4ed8);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
        }
        .shopping-title {
            color: #3b82f6 !important;
            font-weight: 600;
        }
        .marketing-title {
            color: #3b82f6 !important;
            font-weight: 600;
        }
        .section-header {
            color: #2563eb !important;
            font-weight: 600;
        }
        .shopping-item-title {
            color: #1e40af !important;
            font-weight: 600;
        }
        .marketing-item-title {
            color: #1e40af !important;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🌾 KrishiAI Pro")
        st.markdown("---")
        
        # Navigation
        if st.button("🏠 Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        
        if st.button("📤 Upload Land"):
            st.session_state.page = "upload"
            st.rerun()
        
        if st.button("🌱 Crop Recommendations"):
            st.session_state.page = "results"
            st.rerun()
        
        if st.button("📅 Farming Schedule"):
            st.session_state.page = "schedule"
            st.rerun()
        
        if st.button("🛒 Shopping"):
            st.session_state.page = "shopping"
            st.rerun()
        
        if st.button("🏪 Marketing"):
            st.session_state.page = "marketing"
            st.rerun()
        
        if st.button("📈 Market Insights"):
            st.session_state.page = "market"
            st.rerun()
        
        if st.button("💼 Selling Strategy"):
            st.session_state.page = "selling_strategy"
            st.rerun()
        
        if st.button("🏛️ Government Subsidies"):
            st.session_state.page = "government_subsidy"
            st.rerun()
        
        if st.button("📰 Profile"):
            st.session_state.page = "profile"
            st.rerun()
        
        st.markdown("---")
        
        # Language selector
        language = st.selectbox("🌍 Language", ["english", "हिंदी", "తెలుగు", "ಕನ್ನ"])
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()
    
    # Main content based on page
    if st.session_state.page == "dashboard":
        st.markdown('<h1 class="marketing-title">🏠 Farming Dashboard</h1>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">Welcome to KrishiAI Pro - Your Intelligent Farming Assistant</p>', unsafe_allow_html=True)
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div class="card">
                <h3>🌾 Active Crops</h3>
                <h2>4</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card">
                <h3>📅 Farm Days</h3>
                <h2>45</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="card">
                <h3>💰 Revenue</h3>
                <h2>₹2.5L</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="card">
                <h3>📈 Success Rate</h3>
                <h2>87%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<h2 class="section-header">🌟 Quick Actions</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📤 New Analysis", use_container_width=True):
                st.session_state.page = "upload"
                st.rerun()
        
        with col2:
            if st.button("🛒 Shop Supplies", use_container_width=True):
                st.session_state.page = "shopping"
                st.rerun()
        
        with col3:
            if st.button("🏪 Sell Crops", use_container_width=True):
                st.session_state.page = "marketing"
                st.rerun()
    
    elif st.session_state.page == "upload":
        st.markdown('<h1 class="marketing-title">📤 Land Analysis</h1>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("📁 Upload your land image", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded land image", use_column_width=True)
            
            if st.button("🔍 Analyze Land", use_container_width=True):
                # Mock analysis
                st.session_state.crop = "Tomato"
                st.session_state.farming_plan = {"area": 2.5, "city": "Bangalore"}
                st.success("✅ Land analyzed successfully!")
                st.info("🍅 Recommended crop: Tomato for this region")
                st.rerun()
    
    elif st.session_state.page == "results":
        st.markdown('<h1 class="marketing-title">🌱 Crop Recommendations</h1>', unsafe_allow_html=True)
        
        # Mock recommendations
        recommendations = get_mock_crop_recommendations()
        
        df = pd.DataFrame(recommendations)
        st.dataframe(df, use_container_width=True)
        
        if st.button("📅 Create Farming Plan", use_container_width=True):
            st.session_state.page = "schedule"
            st.rerun()
    
    elif st.session_state.page == "schedule":
        st.markdown('<h1 class="marketing-title">📅 Farming Schedule</h1>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">Plan your farming activities for optimal results</p>', unsafe_allow_html=True)
        
        # Calendar view
        calendar_data = []
        base_date = datetime.now()
        
        for i in range(30):
            date = base_date + timedelta(days=i)
            calendar_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "day": date.day,
                "task": f"Day {i+1} farming activity",
                "completed": i < 15  # Mock completed tasks
            })
        
        df = pd.DataFrame(calendar_data)
        st.dataframe(df, use_container_width=True)
    
    elif st.session_state.page == "shopping":
        st.markdown('<h1 class="shopping-title">🛒 Shopping Requirements</h1>', unsafe_allow_html=True)
        
        if st.session_state.farming_plan:
            crop = st.session_state.crop
            area = st.session_state.farming_plan.get('area', 1.0)
            
            requirements = get_mock_shopping_requirements(crop, area)
            
            st.markdown('<h2 class="section-header">📋 Purchase Checklist</h2>', unsafe_allow_html=True)
            
            for category, item in requirements.items():
                st.markdown(f'<h3 class="shopping-item-title">{category.title()}</h3>', unsafe_allow_html=True)
                st.markdown(f"- {item['name']}: ₹{item['price']}")
    
    elif st.session_state.page == "marketing":
        st.markdown('<h1 class="marketing-title">🏪 Marketing & Selling</h1>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">Maximize your profits with intelligent selling strategies</p>', unsafe_allow_html=True)
        
        if st.session_state.crop:
            # Market prices
            market_data = get_mock_market_prices()
            crop_data = market_data.get(st.session_state.crop, {})
            
            if crop_data:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <h3>💰 Min Price</h3>
                        <h2>₹{crop_data['min']}/kg</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="card">
                        <h3>💵 Avg Price</h3>
                        <h2>₹{crop_data['avg']}/kg</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="card">
                        <h3>💸 Max Price</h3>
                        <h2>₹{crop_data['max']}/kg</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="card">
                        <h3>📊 Demand</h3>
                        <h2>{crop_data['demand']}</h2>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif st.session_state.page == "market":
        st.markdown('<h1 class="marketing-title">📈 Market Insights</h1>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">Real-time market intelligence for better decisions</p>', unsafe_allow_html=True)
        
        # Market trends chart
        dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="M")
        prices = np.random.normal(25, 5, len(dates))  # Mock price data
        
        fig = px.line(x=dates, y=prices, title=f"{st.session_state.crop} Price Trends")
        st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.page == "selling_strategy":
        st.markdown('<h1 class="marketing-title">💼 Selling Strategy</h1>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">Advanced strategies for maximum profit</p>', unsafe_allow_html=True)
        
        st.info("📋 Comprehensive selling strategies including market timing, storage recommendations, and value addition options")
    
    else:
        st.markdown('<h1 class="marketing-title">🏠 Welcome to KrishiAI Pro</h1>', unsafe_allow_html=True)
        st.markdown('<p class="section-header">Your Intelligent Farming Assistant</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Start Analysis", use_container_width=True):
                st.session_state.page = "upload"
                st.rerun()
        
        with col2:
            if st.button("📊 View Demo", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()

if __name__ == "__main__":
    main()
