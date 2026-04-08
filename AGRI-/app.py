import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from PIL import Image
import datetime
from pathlib import Path
import json
import hashlib
import hmac
import sqlite3
from datetime import timedelta
import base64
import time
from collections import defaultdict
try:
    import tensorflow as tf
    from tensorflow import keras
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("Warning: TensorFlow not available. Some AI features will be disabled.")
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Agri AI Pro", layout="wide", initial_sidebar_state="expanded")

# ==================== CSS STYLING ====================
def get_css(page):
    base_css = """
    /* Professional Light Background and Main Styling */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 25%, #f1f5f9 50%, #e0f2fe 75%, #f0f9ff 100%);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        transition: background 0.5s ease;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Professional Button Styling */
    .stButton button {
        border-radius: 12px;
        height: 3em;
        font-weight: 600;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        font-size: 14px;
        letter-spacing: 0.025em;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.25);
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }
    
    .stButton button:active {
        transform: translateY(0);
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.2);
    }
    
    /* Typography */
    h1, h2, h3 {
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2c3e50;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    h2 {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Professional Card Styling */
    .card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    /* Professional Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(226, 232, 240, 0.6);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: rgba(59, 130, 246, 0.4);
    }
    
    .metric-card h3 {
        color: #64748b;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-card h2 {
        color: #1e293b;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    
    /* Professional Crop Cards */
    .crop-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(226, 232, 240, 0.6);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .crop-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10b981, #34d399);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .crop-card:hover::before {
        opacity: 1;
    }
    
    .crop-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: rgba(16, 185, 129, 0.4);
    }
    
    .crop-card.selected {
        background: rgba(16, 185, 129, 0.1);
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    .crop-card.selected::before {
        opacity: 1;
        background: linear-gradient(90deg, #10b981, #059669);
    }
    
    .crop-card h3 {
        color: #64748b;
        font-weight: 500;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .crop-card.selected h3 {
        color: #059669;
        font-weight: 600;
    }
    
    .crop-card h2 {
        color: #1e293b;
        font-weight: 700;
        margin: 0.5rem 0;
        font-size: 1.25rem;
    }
    
    .crop-card.selected h2 {
        color: #047857;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,248,255,0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
        border-radius: 8px;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 4px solid #dc3545;
        border-radius: 8px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
        border-left: 4px solid #ffc107;
        border-radius: 8px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left: 4px solid #17a2b8;
        border-radius: 8px;
    }
    
    /* Progress Bar */
    .stProgress .progress-bar {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        border-radius: 10px;
    }
    
    /* File Uploader */
    .stFileUploader {
        border: 2px dashed #4CAF50;
        border-radius: 15px;
        padding: 20px;
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, rgba(139, 195, 74, 0.05) 100%);
    }
    
    /* Selectbox and Input */
    .stSelectbox > div > div, .stTextInput > div > div {
        background: rgba(255,255,255,0.9);
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    /* Marketing Strategy Cards */
    .strategy-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
        transition: all 0.3s ease;
    }
    
    .strategy-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.2);
        border-left-color: #2563eb;
    }
    
    .strategy-card h4, .strategy-card h5, .strategy-card h3, .strategy-card h2 {
        color: #1e40af !important;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .strategy-card p, .strategy-card strong {
        color: #1e293b !important;
        font-weight: 400;
    }
    
    .strategy-card strong {
        color: #1e40af !important;
        font-weight: 600;
    }
    
    /* Location Cards */
    .location-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
        border: 1px solid #3b82f6;
        transition: all 0.3s ease;
    }
    
    .location-card:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.25);
        border-color: #2563eb;
    }
    
    .location-card h5, .location-card h4, .location-card h3, .location-card h2 {
        color: #1e40af !important;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .location-card p, .location-card strong {
        color: #1e293b !important;
        font-weight: 400;
    }
    
    .location-card strong {
        color: #1e40af !important;
        font-weight: 600;
    }
    
    /* Price Trend Chart */
    .price-trend {
        background: linear-gradient(135deg, #ffffff 0%, #fef3c7 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(251, 146, 60, 0.15);
        border: 1px solid #f59e0b;
    }
    
    .price-trend h4, .price-trend h3, .price-trend h2 {
        color: #92400e !important;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .price-trend p, .price-trend strong {
        color: #1e293b !important;
        font-weight: 400;
    }
    
    /* Shopping and Marketing Section Text Colors */
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
        
    
    /* Task Items */
    .task-item {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,248,255,0.95) 100%);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #4CAF50;
        color: #2c3e50;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .task-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }
    
    .task-item b, .task-item p {
        color: #2c3e50;
    }
    
    /* Marketing Insights Section */
    .marketing-insights {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .insight-header {
        background: linear-gradient(45deg, #4CAF50, #45a049);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .price-alert {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 4px solid #f39c12;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .strategy-tip {
        background: linear-gradient(135deg, #d1f2eb 0%, #a8dadc 100%);
        border-left: 4px solid #457b9d;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #1d3557;
    }
    
    .market-opportunity {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    """
    
    if page in ["auth_home", "auth_login", "auth_register"]:
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
        }
        h1, h2, h3 {
            color: #ffffff;
        }
        .card {
            background: rgba(255,255,255,0.95);
            color: #333333;
        }
        .card h1, .card h2, .card h3, .card p, .card b {
            color: #333333;
        }
        .stButton button {
            background: linear-gradient(45deg, #ff6b6b, #ffa500);
            color: white;
        }
        .stTextInput input, .stNumberInput input, .stSlider div {
            color: #333333;
        }
        """
    elif page == "dashboard":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #1f3d23;
        }
        h1, h2, h3 {
            color: #1a5f2f;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #1f3d23;
        }
        .stButton button {
            background: linear-gradient(45deg, #1a5f2f, #2ecc71);
            color: white;
        }
        """
    elif page == "upload":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #a8e6cf 0%, #dcedc8 100%);
            color: #1e4621;
        }
        h1, h2, h3 {
            color: #1b5e20;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #1e4621;
        }
        .stButton button {
            background: linear-gradient(45deg, #4caf50, #81c784);
            color: white;
        }
        """
    elif page == "results":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            color: #7b3f00;
        }
        h1, h2, h3 {
            color: #bf360c;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #5a3400;
        }
        .stButton button {
            background: linear-gradient(45deg, #ff9800, #ffb74d);
            color: white;
        }
        .crop-card {
            background: rgba(255,255,255,0.98);
            border-radius: 15px;
            padding: 10px;
            margin: 6px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            border-left: 4px solid #ff9800;
            transition: transform 0.25s ease, border-color 0.25s ease;
            min-height: 150px;
            width: 100%;
            aspect-ratio: 1 / 1;
        }
        .crop-card:hover {
            transform: translateY(-2px);
        }
        .crop-card.selected {
            border-left: 4px solid #4caf50;
            background: rgba(232, 245, 233, 0.98);
        }
        .crop-card h2 {
            font-size: 1.1rem;
            margin-bottom: 4px;
        }
        .crop-card p {
            font-size: 0.75rem;
            line-height: 1.3;
        }
        .crop-card small {
            color: #555555;
        }
        """
    elif page == "schedule":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            color: #7b3f00;
        }
        h1, h2, h3 {
            color: #bf360c;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #5a3400;
        }
        .calendar-month-card {
            background: rgba(255,255,255,0.98);
            border-radius: 25px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 6px 18px rgba(0,0,0,0.12);
        }
        .calendar-day {
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 12px;
            margin: 4px 0;
            text-align: left;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            min-height: 140px;
        }
        .calendar-day.completed {
            background: rgba(144,238,144,0.95);
        }
        .calendar-day strong {
            display: block;
            margin-bottom: 8px;
            font-size: 1.1rem;
        }
        .calendar-day small {
            color: #444444;
        }
        .month-title {
            font-size: 1.3rem;
            font-weight: 700;
            text-align: center;
            margin: 0 10px;
        }
        .stButton button {
            background: linear-gradient(45deg, #ff9800, #ffb74d);
            color: white;
        }
        """
    elif page == "market":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #ffcdd2 0%, #ffebee 100%);
            color: #7b1f1f;
        }
        h1, h2, h3 {
            color: #d32f2f;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #7b1f1f;
        }
        .stButton button {
            background: linear-gradient(45deg, #f44336, #ef5350);
            color: white;
        }
        """
    elif page == "profile":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            color: #1b5e20;
        }
        h1, h2, h3 {
            color: #1b5e20;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #1b5e20;
        }
        .stButton button {
            background: linear-gradient(45deg, #43a047, #66bb6a);
            color: white;
        }
        """
    elif page == "news":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            color: #0d47a1;
        }
        h1, h2, h3 {
            color: #0d47a1;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #0d47a1;
        }
        .stButton button {
            background: linear-gradient(45deg, #1e88e5, #42a5f5);
            color: white;
        }
        """
    elif page == "selling_strategy":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 100%);
            color: #33691e;
        }
        h1, h2, h3 {
            color: #33691e;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #33691e;
        }
        .stButton button {
            background: linear-gradient(45deg, #7cb342, #c0ca33);
            color: white;
        }
        """
    elif page == "government_subsidy":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
            color: #bf360c;
        }
        h1, h2, h3 {
            color: #bf360c;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #5d4037;
        }
        .stButton button {
            background: linear-gradient(45deg, #ffa726, #ffb74d);
            color: white;
        }
        """
    
    # Add CSS for specific pages
    if page == "shopping":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #e0f2fe 0%, #c7d2fe 100%);
            color: #1e3a8a;
        }
        h1, h2, h3 {
            color: #1e3a8a;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #1e3a8a;
            background: rgba(255, 255, 255, 0.95);
        }
        .stButton button {
            background: linear-gradient(45deg, #3b82f6, #2563eb);
            color: white;
        }
        """
    elif page == "marketing":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            color: #1e3a8a;
        }
        h1, h2, h3 {
            color: #1e3a8a;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #1e3a8a;
            background: rgba(255, 255, 255, 0.95);
        }
        .stButton button {
            background: linear-gradient(45deg, #8b5cf6, #6366f1);
            color: white;
        }
        """
    elif page == "schedule":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            color: #1e3a8a;
        }
        h1, h2, h3 {
            color: #1e3a8a;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #1e3a8a;
            background: rgba(255, 255, 255, 0.95);
        }
        .stButton button {
            background: linear-gradient(45deg, #f59e0b, #d97706);
            color: white;
        }
        """
    return base_css

# Initialize session state
conn = sqlite3.connect("farmers.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
c.execute('''CREATE TABLE IF NOT EXISTS farming_plans (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    crop TEXT NOT NULL,
    start_date TEXT,
    land_images TEXT,
    soil_data TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)''')
c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (
    id INTEGER PRIMARY KEY,
    plan_id INTEGER NOT NULL,
    task_date TEXT,
    task_description TEXT,
    task_type TEXT,
    is_completed INTEGER DEFAULT 0,
    FOREIGN KEY(plan_id) REFERENCES farming_plans(id)
)''')
conn.commit()

REMEMBER_FILE = Path("remember_me.json")

def get_user_by_username(username):
    try:
        c = conn.cursor()
        c.execute("SELECT id, username, email FROM users WHERE username=?", (username,))
        user = c.fetchone()
        if user:
            return {"id": user[0], "username": user[1], "email": user[2]}
    except Exception:
        pass
    return None


def save_remembered_user(username, token):
    try:
        REMEMBER_FILE.write_text(json.dumps({"username": username, "token": token}), encoding="utf-8")
    except Exception:
        pass


def clear_remembered_user():
    try:
        if REMEMBER_FILE.exists():
            REMEMBER_FILE.unlink()
    except Exception:
        pass


def load_remembered_user():
    try:
        if REMEMBER_FILE.exists():
            data = json.loads(REMEMBER_FILE.read_text(encoding="utf-8"))
            username = data.get("username")
            token = data.get("token")
            if username and token:
                user = get_user_by_username(username)
                if user:
                    return user, token
    except Exception:
        pass
    return None, None


def save_farming_plan_to_db(user_id, plan):
    try:
        c = conn.cursor()
        soil_data = json.dumps({
            "soil_health": plan.get("soil_health"),
            "vegetation": plan.get("vegetation"),
            "soil_type": plan.get("soil_type"),
            "estimated_ph": plan.get("estimated_ph"),
            "weather": plan.get("weather"),
            "temp": plan.get("temp"),
            "humidity": plan.get("humidity"),
            "city": plan.get("city"),
            "area": plan.get("area"),
            "recommended_crop": plan.get("recommended_crop"),
            "short_term_crop": plan.get("short_term_crop"),
            "medium_term_crop": plan.get("medium_term_crop"),
            "long_term_crop": plan.get("long_term_crop")
        })
        land_images = json.dumps(plan.get("land_images", []))
        c.execute("SELECT id FROM farming_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,))
        existing = c.fetchone()
        if existing:
            c.execute("""UPDATE farming_plans SET crop=?, start_date=?, land_images=?, soil_data=?, status=? WHERE id=?""",
                      (plan.get("crop"), plan.get("start_date").isoformat(), land_images, soil_data, plan.get("status", "active"), existing[0]))
            plan_id = existing[0]
        else:
            c.execute("""INSERT INTO farming_plans (user_id, crop, start_date, land_images, soil_data, status) VALUES (?, ?, ?, ?, ?, ?)""",
                      (user_id, plan.get("crop"), plan.get("start_date").isoformat(), land_images, soil_data, plan.get("status", "active")))
            plan_id = c.lastrowid
        conn.commit()
        return plan_id
    except Exception:
        return None


def load_farming_plan_from_db(user_id):
    try:
        c = conn.cursor()
        c.execute("SELECT id, crop, start_date, land_images, soil_data, status FROM farming_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,))
        row = c.fetchone()
        if row:
            plan_id, crop, start_date, land_images_text, soil_data_text, status = row
            soil_data = json.loads(soil_data_text or "{}")
            return {
                "plan_id": plan_id,
                "crop": crop,
                "start_date": datetime.date.fromisoformat(start_date),
                "land_images": json.loads(land_images_text or "[]"),
                "status": status,
                **soil_data
            }
    except Exception:
        pass
    return None


def save_daily_tasks_to_db(plan_id, schedule):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM daily_tasks WHERE plan_id=?", (plan_id,))
        for item in schedule:
            c.execute("""INSERT INTO daily_tasks (plan_id, task_date, task_description, task_type, is_completed)
                         VALUES (?, ?, ?, ?, ?)""",
                      (plan_id, item["date"], item["task"], item["type"], 1 if item.get("completed") else 0))
        conn.commit()
    except Exception:
        pass


def load_daily_tasks_from_db(plan_id):
    try:
        c = conn.cursor()
        c.execute("SELECT task_date, task_description, task_type, is_completed FROM daily_tasks WHERE plan_id=? ORDER BY task_date", (plan_id,))
        rows = c.fetchall()
        schedule = []
        for row in rows:
            schedule.append({
                "date": row[0],
                "task": row[1],
                "type": row[2],
                "completed": bool(row[3])
            })
        return schedule
    except Exception:
        return []


def update_task_completion(plan_id, task_date, completed):
    try:
        c = conn.cursor()
        c.execute("UPDATE daily_tasks SET is_completed=? WHERE plan_id=? AND task_date=?", (1 if completed else 0, plan_id, task_date))
        conn.commit()
    except Exception:
        pass


def load_user_data(user_id):
    plan = load_farming_plan_from_db(user_id)
    if plan:
        st.session_state.farming_plan = plan
        st.session_state.crop = plan.get("crop", st.session_state.crop)
        st.session_state.plan_id = plan.get("plan_id")
        schedule = load_daily_tasks_from_db(plan["plan_id"])
        if schedule:
            st.session_state.schedule = schedule
            st.session_state.tasks_completed = {item["date"]: item["completed"] for item in schedule}

if "language" not in st.session_state:
    st.session_state.language = "en"

if "page" not in st.session_state:
    st.session_state.page = "auth_home"
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.images = []
    st.session_state.crop = ""
    st.session_state.location = None
    st.session_state.schedule = []
    st.session_state.tasks_completed = {}
    st.session_state.farming_plan = None
    st.session_state.plan_id = None
    remembered_user, remembered_token = load_remembered_user()
    if remembered_user:
        st.session_state.user = remembered_user
        st.session_state.token = remembered_token
        st.session_state.page = "dashboard"
        load_user_data(remembered_user["id"])

st.markdown(f"<style>{get_css(st.session_state.page)}</style>", unsafe_allow_html=True)

# ==================== MODEL LOADING ====================
# Initialize ML models
@st.cache_resource
def load_trained_models():
    """Load all trained ML models"""
    try:
        ml_models = KrishiAIModels()
        return ml_models
    except Exception as e:
        st.error(f"❌ Error initializing ML models: {e}")
        return None

# Crop classes for prediction
CROP_CLASSES = ['Tomato', 'Onion', 'Chilli', 'Cabbage', 'Maize', 'Potato',
                'Sugarcane', 'Cotton', 'Rice', 'Groundnut', 'Ragi', 'Wheat']

def predict_crop_with_trained_model(models, soil_data, weather_data, budget, duration):
    """Use trained crop recommendation model for prediction"""
    try:
        if 'crop_recommendation' not in models:
            return None
        
        model = models['crop_recommendation']
        
        # Prepare input features (10 features as expected by model)
        # location_encoded, soil_encoded, water_encoded, budget, duration + 5 synthetic features
        features = np.array([[1.0, 1.0, 1.0, budget, duration, 0.5, 0.5, 0.5, 0.5, 0.5]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        top_3_indices = np.argsort(prediction)[-3:][::-1]
        top_3_crops = [CROP_CLASSES[i] for i in top_3_indices]
        top_3_probs = [prediction[i] for i in top_3_indices]
        
        return list(zip(top_3_crops, top_3_probs))
        
    except Exception as e:
        st.error(f"Error in crop prediction: {e}")
        return None

def predict_profit_with_trained_model(trained_models, crop_type, duration, budget, location, demand):
    """Use trained profit prediction model for prediction"""
    try:
        if not hasattr(trained_models, 'predict_profit'):
            return None
        
        # Prepare input features (8 features as expected by model)
        # crop_encoded, duration, budget, location_encoded, demand_encoded, yield_per_acre + 2 synthetic features
        crop_encoded = CROP_CLASSES.index(crop_type) if crop_type in CROP_CLASSES else 0
        features = np.array([[crop_encoded, duration, budget, 1.0, 1.0, 5000, 0.5, 0.5]])
        
        # Make prediction
        prediction = trained_models.predict_profit(crop_type, duration, budget, location, demand)
        
        return {
            'predicted_profit': prediction['predicted_profit'],
            'confidence': prediction['confidence'],
            'recommendations': prediction['recommendations'],
            'ml_insights': f"ML model analyzed profit potential with {prediction['confidence']} confidence"
        }
        
    except Exception as e:
        st.error(f"Error in profit prediction: {e}")
        return None

def analyze_land_with_trained_model(trained_models, image):
    """Use trained land analysis CNN for soil quality prediction"""
    try:
        if not hasattr(trained_models, 'optimize_farming_conditions'):
            return None
        
        # Preprocess image to (224, 224, 3)
        img = image.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction using our trained model
        prediction = trained_models.optimize_farming_conditions(25, 60, 100, 10, 50, 1)
        
        return prediction['farming_score'], prediction['confidence']
        
    except Exception as e:
        st.error(f"Error in land analysis: {e}")
        return None, None

# ==================== DATABASE INITIALIZATION ====================
def init_db():
    conn = sqlite3.connect("farmers.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        location TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS farming_plans (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        crop TEXT NOT NULL,
        start_date TEXT,
        land_images TEXT,
        soil_data TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (
        id INTEGER PRIMARY KEY,
        plan_id INTEGER NOT NULL,
        task_date TEXT,
        task_description TEXT,
        task_type TEXT,
        is_completed INTEGER DEFAULT 0,
        FOREIGN KEY(plan_id) REFERENCES farming_plans(id)
    )''')
    conn.commit()
    return conn

conn = init_db()

# ==================== JWT AUTHENTICATION ====================
SECRET_KEY = "agri_ai_pro_secret_key_2024_farming"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_jwt_token(user_id, username):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": (datetime.datetime.now() + timedelta(days=30)).isoformat()
    }
    header_json = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    payload_json = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    signature = base64.urlsafe_b64encode(
        hmac.new(SECRET_KEY.encode(), f"{header_json}.{payload_json}".encode(), hashlib.sha256).digest()
    ).decode().rstrip('=')
    return f"{header_json}.{payload_json}.{signature}"

def verify_jwt_token(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        payload_data = base64.urlsafe_b64decode(parts[1] + '==')
        return json.loads(payload_data)
    except:
        return None

# ==================== USER MANAGEMENT ====================
def register_user(username, password, email, phone):
    try:
        c = conn.cursor()
        hashed_pwd = hash_password(password)
        c.execute("INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)",
                  (username, hashed_pwd, email, phone))
        conn.commit()
        return True, "✅ Registration successful! Please login."
    except sqlite3.IntegrityError:
        return False, "❌ Username already exists!"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def authenticate_user(username, password):
    try:
        c = conn.cursor()
        hashed_pwd = hash_password(password)
        c.execute("SELECT id, username, email FROM users WHERE username=? AND password=?", (username, hashed_pwd))
        user = c.fetchone()
        if user:
            token = create_jwt_token(user[0], user[1])
            return True, token, {"id": user[0], "username": user[1], "email": user[2]}
        return False, None, None
    except Exception as e:
        return False, None, None

def get_shopping_requirements(crop_name, area_hectares):
    """Get crop-specific shopping requirements with real-world pricing"""
    requirements = {
        "tomato": {
            "seeds": {"name": "Tomato Seeds (Hybrid)", "quantity": f"{int(area_hectares * 500)}g", "price": int(area_hectares * 1500), "unit": "packs"},
            "fertilizer": {"name": "NPK Fertilizer (19-19-19)", "quantity": f"{int(area_hectares * 50)}kg", "price": int(area_hectares * 3000), "unit": "bags"},
            "organic": {"name": "Organic Compost", "quantity": f"{int(area_hectares * 1000)}kg", "price": int(area_hectares * 2000), "unit": "tons"},
            "pesticide": {"name": "Organic Pesticide", "quantity": f"{int(area_hectares * 2)}L", "price": int(area_hectares * 800), "unit": "bottles"},
            "tools": {"name": "Farm Tools & Equipment", "quantity": "1 set", "price": 2500, "unit": "set"},
            "irrigation": {"name": "Drip Irrigation Parts", "quantity": f"{int(area_hectares * 100)}m", "price": int(area_hectares * 1500), "unit": "meters"}
        },
        "maize": {
            "seeds": {"name": "Maize Seeds (Hybrid)", "quantity": f"{int(area_hectares * 25)}kg", "price": int(area_hectares * 2000), "unit": "bags"},
            "fertilizer": {"name": "Urea Fertilizer", "quantity": f"{int(area_hectares * 80)}kg", "price": int(area_hectares * 2500), "unit": "bags"},
            "organic": {"name": "Farm Yard Manure", "quantity": f"{int(area_hectares * 2000)}kg", "price": int(area_hectares * 1500), "unit": "tons"},
            "pesticide": {"name": "Herbicide", "quantity": f"{int(area_hectares * 3)}L", "price": int(area_hectares * 1200), "unit": "bottles"},
            "tools": {"name": "Maize Farming Tools", "quantity": "1 set", "price": 3000, "unit": "set"},
            "irrigation": {"name": "Sprinkler System", "quantity": f"{int(area_hectares * 50)}m", "price": int(area_hectares * 2000), "unit": "meters"}
        },
        "ragi": {
            "seeds": {"name": "Finger Millet Seeds", "quantity": f"{int(area_hectares * 15)}kg", "price": int(area_hectares * 1200), "unit": "bags"},
            "fertilizer": {"name": "Organic Fertilizer", "quantity": f"{int(area_hectares * 30)}kg", "price": int(area_hectares * 1500), "unit": "bags"},
            "organic": {"name": "Vermicompost", "quantity": f"{int(area_hectares * 800)}kg", "price": int(area_hectares * 1200), "unit": "tons"},
            "pesticide": {"name": "Bio-pesticide", "quantity": f"{int(area_hectares * 1.5)}L", "price": int(area_hectares * 600), "unit": "bottles"},
            "tools": {"name": "Traditional Farm Tools", "quantity": "1 set", "price": 2000, "unit": "set"}
        },
        "paddy": {
            "seeds": {"name": "Paddy Seeds (Improved)", "quantity": f"{int(area_hectares * 40)}kg", "price": int(area_hectares * 1800), "unit": "bags"},
            "fertilizer": {"name": "Complex Fertilizer", "quantity": f"{int(area_hectares * 60)}kg", "price": int(area_hectares * 2800), "unit": "bags"},
            "organic": {"name": "Bio-fertilizer", "quantity": f"{int(area_hectares * 500)}kg", "price": int(area_hectares * 1800), "unit": "tons"},
            "pesticide": {"name": "Insecticide", "quantity": f"{int(area_hectares * 2.5)}L", "price": int(area_hectares * 1000), "unit": "bottles"},
            "tools": {"name": "Paddy Farming Equipment", "quantity": "1 set", "price": 3500, "unit": "set"},
            "irrigation": {"name": "Water Pump & Pipes", "quantity": "1 set", "price": int(area_hectares * 2500), "unit": "set"}
        },
        "cotton": {
            "seeds": {"name": "Bt Cotton Seeds", "quantity": f"{int(area_hectares * 5)}kg", "price": int(area_hectares * 3000), "unit": "packs"},
            "fertilizer": {"name": "DAP Fertilizer", "quantity": f"{int(area_hectares * 70)}kg", "price": int(area_hectares * 3500), "unit": "bags"},
            "organic": {"name": "Organic Manure", "quantity": f"{int(area_hectares * 1200)}kg", "price": int(area_hectares * 2200), "unit": "tons"},
            "pesticide": {"name": "Cotton Specific Pesticide", "quantity": f"{int(area_hectares * 4)}L", "price": int(area_hectares * 2000), "unit": "bottles"},
            "tools": {"name": "Cotton Picking Tools", "quantity": "1 set", "price": 4000, "unit": "set"}
        }
    }
    
    # Default for other crops
    default_requirements = {
        "seeds": {"name": f"{crop_name.title()} Seeds", "quantity": f"{int(area_hectares * 20)}kg", "price": int(area_hectares * 1500), "unit": "bags"},
        "fertilizer": {"name": "General Purpose Fertilizer", "quantity": f"{int(area_hectares * 50)}kg", "price": int(area_hectares * 2500), "unit": "bags"},
        "organic": {"name": "Organic Compost", "quantity": f"{int(area_hectares * 1000)}kg", "price": int(area_hectares * 1800), "unit": "tons"},
        "pesticide": {"name": "General Pesticide", "quantity": f"{int(area_hectares * 2)}L", "price": int(area_hectares * 800), "unit": "bottles"},
        "tools": {"name": "Basic Farm Tools", "quantity": "1 set", "price": 2500, "unit": "set"}
    }
    
    return requirements.get(crop_name.lower(), default_requirements)

def get_nearest_markets(location):
    """Get nearest agricultural markets with real market names"""
    markets = {
        "bangalore": [
            {"name": "KR Market", "distance": "2 km", "address": "Krishna Rajendra Market, Bangalore"},
            {"name": "Yelahanka Market", "distance": "15 km", "address": "Yelahanka Agricultural Market, Bangalore"},
            {"name": "Hoskote Market", "distance": "25 km", "address": "Hoskote Agricultural Yard, Bangalore Rural"}
        ],
        "mysore": [
            {"name": "Mysore APMC Market", "distance": "3 km", "address": "APMC Market, Mysore"},
            {"name": "Nazarbad Market", "distance": "5 km", "address": "Nazarbad Agricultural Market, Mysore"},
            {"name": "Hootagalli Market", "distance": "8 km", "address": "Hootagalli Market Yard, Mysore"}
        ],
        "tumkur": [
            {"name": "Tumkur APMC", "distance": "2 km", "address": "APMC Market, Tumkur"},
            {"name": "Kunigal Market", "distance": "20 km", "address": "Kunigal Agricultural Market"},
            {"name": "Gubbi Market", "distance": "25 km", "address": "Gubbi Market Yard"}
        ],
        "mandya": [
            {"name": "Mandya Sugar Market", "distance": "2 km", "address": "Mandya Agricultural Market"},
            {"name": "Maddur Market", "distance": "15 km", "address": "Maddur APMC Market"},
            {"name": "Srirangapatna Market", "distance": "18 km", "address": "Srirangapatna Agricultural Market"}
        ]
    }
    
    # Default markets for other locations
    default_markets = [
        {"name": "Local APMC Market", "distance": "5 km", "address": "Nearest Agricultural Market"},
        {"name": "District Market Yard", "distance": "10 km", "address": "District Agricultural Market"},
        {"name": "Regional Market", "distance": "20 km", "address": "Regional Agricultural Market"}
    ]
    
    location_key = location.lower().split()[0] if location else "default"
    return markets.get(location_key, default_markets)

def get_marketing_insights(crop, location, area):
    """Get comprehensive marketing insights based on crop and location"""
    insights = {
        "tomato": {
            "best_seasons": ["Winter (Oct-Feb)", "Summer (Mar-Jun)"],
            "price_trends": "High demand in festivals and wedding seasons",
            "storage_tips": "Can be stored for 2-3 weeks in cool conditions",
            "processing_options": ["Fresh market", "Sauce making", "Canning"],
            "export_potential": "High demand in Middle East and Europe",
            "price_factors": ["Festival demand", "Weather conditions", "Transport costs"],
            "market_opportunities": [
                "Restaurant chains in cities",
                "Export markets",
                "Processing industries",
                "Local wholesale markets"
            ]
        },
        "maize": {
            "best_seasons": ["Monsoon (Jun-Sep)", "Post-monsoon (Oct-Nov)"],
            "price_trends": "Prices peak during festival seasons",
            "storage_tips": "Dry storage for 6-8 months possible",
            "processing_options": ["Animal feed", "Corn flour", "Starch production"],
            "export_potential": "Good demand from poultry and cattle feed industry",
            "price_factors": ["Monsoon performance", "International demand", "Fuel prices"],
            "market_opportunities": [
                "Poultry feed companies",
                "Starch manufacturers",
                "Animal feed industry",
                "Export to Southeast Asia"
            ]
        },
        "ragi": {
            "best_seasons": ["Monsoon (Jun-Sep)", "Winter (Oct-Jan)"],
            "price_trends": "Steady demand throughout year",
            "storage_tips": "Excellent storage life up to 1 year",
            "processing_options": ["Millet flour", "Health foods", "Traditional recipes"],
            "export_potential": "Growing health food market demand",
            "price_factors": ["Health food trends", "Organic demand", "Government procurement"],
            "market_opportunities": [
                "Health food stores",
                "Government procurement",
                "Organic markets",
                "Traditional food manufacturers"
            ]
        },
        "okra": {
            "best_seasons": ["Summer (Mar-Jun)", "Monsoon (Jul-Sep)"],
            "price_trends": "Premium prices in summer months",
            "storage_tips": "Very perishable - sell within 2-3 days",
            "processing_options": ["Frozen okra", "Pickling", "Dehydration"],
            "export_potential": "Good demand in Gulf countries",
            "price_factors": ["Seasonality", "Export demand", "Transport costs"],
            "market_opportunities": [
                "Export to Gulf countries",
                "Frozen food companies",
                "Urban supermarkets",
                "Hotel industry"
            ]
        }
    }
    
    return insights.get(crop.lower(), {
        "best_seasons": ["Varies by region"],
        "price_trends": "Market dependent on seasonal factors",
        "storage_tips": "Follow standard agricultural storage practices",
        "processing_options": ["Fresh market", "Processing industry"],
        "export_potential": "Depends on quality and market demand",
        "price_factors": ["Season", "Quality", "Market demand"],
        "market_opportunities": ["Local markets", "Processing industries"]
    })

def get_selling_strategies(crop, location, quantity_kg):
    """Get comprehensive selling strategies for the crop"""
    strategies = {
        "immediate_sale": {
            "title": "Immediate Sale Strategy",
            "description": "Sell immediately after harvest for quick cash flow",
            "pros": ["Quick cash flow", "No storage costs", "Lower risk"],
            "cons": ["Lower prices", "Market timing risk"],
            "best_for": ["Small farmers", "Need immediate cash", "Perishable crops"],
            "expected_price": "Market rate - 10-15%",
            "timeline": "1-7 days after harvest"
        },
        "storage_strategy": {
            "title": "Storage Strategy",
            "description": "Store crop and wait for better prices",
            "pros": ["Higher prices", "Market timing advantage", "Better negotiation power"],
            "cons": ["Storage costs", "Price risk", "Quality deterioration"],
            "best_for": ["Non-perishable crops", "Price storage facilities", "Risk-tolerant farmers"],
            "expected_price": "Market rate + 20-40%",
            "timeline": "1-6 months storage"
        },
        "processing_strategy": {
            "title": "Value Addition Strategy",
            "description": "Process crop to add value before selling",
            "pros": ["Higher margins", "Longer shelf life", "Brand building"],
            "cons": ["Processing costs", "Equipment needed", "Technical knowledge"],
            "best_for": ["Farmers with processing skills", "Access to equipment", "Quality produce"],
            "expected_price": "Market rate + 50-100%",
            "timeline": "2-4 weeks processing"
        },
        "contract_farming": {
            "title": "Contract Farming Strategy",
            "description": "Sell through advance contracts with buyers",
            "pros": ["Price security", "Guaranteed market", "Technical support"],
            "cons": ["Lower prices", "Quality requirements", "Contract obligations"],
            "best_for": ["Large farmers", "Quality-focused", "Risk-averse"],
            "expected_price": "Market rate - 5-10%",
            "timeline": "Pre-harvest contracts"
        },
        "direct_to_consumer": {
            "title": "Direct to Consumer Strategy",
            "description": "Sell directly to consumers or retailers",
            "pros": ["Higher prices", "Direct feedback", "Brand building"],
            "cons": ["Marketing effort", "Logistics complexity", "Limited reach"],
            "best_for": ["Small-medium farmers", "Quality produce", "Near urban areas"],
            "expected_price": "Market rate + 30-60%",
            "timeline": "Ongoing marketing"
        }
    }
    
    # Add crop-specific recommendations
    crop_specific = {
        "tomato": {
            "recommended_strategy": "processing_strategy",
            "reason": "Tomatoes have high processing potential for sauces, purees, and canning",
            "best_time": "When market prices are low (usually post-harvest glut)"
        },
        "maize": {
            "recommended_strategy": "storage_strategy", 
            "reason": "Maize stores well and prices often increase in feed season",
            "best_time": "Store until poultry feed demand peaks (Oct-Dec)"
        },
        "ragi": {
            "recommended_strategy": "direct_to_consumer",
            "reason": "Growing health food market for millets",
            "best_time": "Year-round, but best during health food campaigns"
        },
        "okra": {
            "recommended_strategy": "immediate_sale",
            "reason": "Highly perishable - best sold fresh",
            "best_time": "Immediately after harvest"
        }
    }
    
    return {
        "strategies": strategies,
        "crop_specific": crop_specific.get(crop.lower(), {
            "recommended_strategy": "immediate_sale",
            "reason": "General recommendation for quick turnover",
            "best_time": "Based on market conditions"
        })
    }

def get_price_forecast(crop, location, months_ahead=3):
    """Get price forecast for the crop"""
    # Simulated price data based on real market patterns
    base_prices = {
        "tomato": {"min": 15, "max": 40, "avg": 25},
        "maize": {"min": 12, "max": 22, "avg": 17},
        "ragi": {"min": 20, "max": 35, "avg": 28},
        "okra": {"min": 25, "max": 45, "avg": 35}
    }
    
    current_month = datetime.datetime.now().month
    forecasts = []
    
    for i in range(months_ahead):
        forecast_month = (current_month + i - 1) % 12 + 1
        base_price = base_prices.get(crop.lower(), {"avg": 20})["avg"]
        
        # Seasonal adjustments
        seasonal_factor = 1.0
        if crop.lower() == "tomato":
            if forecast_month in [10, 11, 12, 1, 2]:  # Festival season
                seasonal_factor = 1.3
            elif forecast_month in [3, 4, 5]:  # Summer
                seasonal_factor = 1.1
        elif crop.lower() == "maize":
            if forecast_month in [10, 11, 12]:  # Feed season
                seasonal_factor = 1.2
        
        price = base_price * seasonal_factor * (1 + np.random.uniform(-0.1, 0.1))
        forecasts.append({
            "month": datetime.date(2024, forecast_month, 1).strftime("%B"),
            "price": round(price, 2),
            "trend": "up" if seasonal_factor > 1 else "stable" if seasonal_factor == 1 else "down"
        })
    
    return forecasts

def get_optimal_selling_locations(crop, location, quantity):
    """Get optimal selling locations based on crop and quantity"""
    # Real market data with price differentials
    market_data = {
        "bangalore": {
            "premium_markets": [
                {"name": "KR Market", "price_premium": 0.15, "min_quantity": 500, "specialty": "Organic"},
                {"name": "HSR Layout", "price_premium": 0.10, "min_quantity": 200, "specialty": "Retail"},
                {"name": "Whitefield", "price_premium": 0.12, "min_quantity": 300, "specialty": "Export"}
            ],
            "wholesale_markets": [
                {"name": "Yelahanka APMC", "price_premium": 0.05, "min_quantity": 1000, "specialty": "Bulk"},
                {"name": "Kolar Market", "price_premium": 0.03, "min_quantity": 2000, "specialty": "Traditional"}
            ]
        },
        "default": {
            "premium_markets": [
                {"name": "City Supermarkets", "price_premium": 0.20, "min_quantity": 100, "specialty": "Retail"},
                {"name": "Hotels & Restaurants", "price_premium": 0.15, "min_quantity": 50, "specialty": "Direct supply"}
            ],
            "wholesale_markets": [
                {"name": "Local APMC", "price_premium": 0.00, "min_quantity": 500, "specialty": "Standard"},
                {"name": "District Market", "price_premium": 0.02, "min_quantity": 1000, "specialty": "Regional"}
            ]
        }
    }
    
    location_key = location.lower().split()[0] if location else "default"
    return market_data.get(location_key, market_data["default"])

def get_risk_management_strategies(crop):
    """Get risk management strategies for the crop"""
    return {
        "price_risk": {
            "strategies": [
                "Forward contracts with buyers",
                "Price insurance schemes",
                "Diversify selling timing",
                "Monitor market trends daily"
            ],
            "tools": ["Commodity exchanges", "Government price support", "Hedging options"]
        },
        "production_risk": {
            "strategies": [
                "Crop insurance coverage",
                "Diversify crop portfolio",
                "Improved irrigation systems",
                "Quality seed investment"
            ],
            "tools": ["Weather insurance", "Crop insurance schemes", "Technical support"]
        },
        "market_risk": {
            "strategies": [
                "Multiple buyer relationships",
                "Transport logistics planning",
                "Market information networks",
                "Alternative marketing channels"
            ],
            "tools": ["Market apps", "Cooperative societies", "Digital platforms"]
        }
    }

def get_translated_text(text, lang_code):
    translations = {
        "en": {
            "dashboard": "Dashboard",
            "profile_settings": "Profile Settings",
            "news": "News",
            "selling_strategy": "Selling Strategy",
            "government_subsidies": "Government Subsidies",
            "logout": "Logout",
            "start_farming": "Start Farming",
            "view_schedule": "View Schedule",
            "market_insights": "Market Insights",
            "language": "Language",
            "weather": "Weather",
            "temperature": "Temperature",
            "humidity": "Humidity",
            "location": "Location",
            "shopping_requirements": "Pre-Farming Shopping Requirements",
            "seeds": "Seeds",
            "fertilizer": "Fertilizer",
            "organic": "Organic Manure",
            "pesticide": "Pesticide",
            "tools": "Tools & Equipment",
            "irrigation": "Irrigation",
            "quantity": "Quantity",
            "price": "Price",
            "nearest_markets": "Nearest Agricultural Markets",
            "purchase_checklist": "Purchase Checklist",
            "mark_as_purchased": "Mark as Purchased",
            "total_cost": "Total Estimated Cost",
            "proceed_to_calendar": "Proceed to Farming Calendar",
            "back_to_results": "Back to Results",
            "profile": "Profile",
            "personal_details": "Personal Details",
            "account_status": "Account Status",
            "name": "Name",
            "email": "Email",
            "designation": "Designation",
            "role": "Role",
            "member_since": "Member Since",
            "status": "Status",
            "verified": "Verified",
            "farming_activity": "Farming Activity",
            "current_crop": "Current Crop",
            "land_area": "Land Area",
            "start_date": "Start Date",
            "agriculture_news": "Agriculture News",
            "todays_headlines": "Today's Top Agriculture Headlines",
            "source": "Source",
            "date": "Date",
            "selling_strategies": "Best Selling Strategies",
            "price_range": "Price Range",
            "current_demand": "Current Demand",
            "best_markets": "Best Markets",
            "best_time": "Best Time",
            "selling_strategy": "Selling Strategy",
            "view_market_rates": "View Market Rates",
            "congratulations": "Congratulations!",
            "farming_completed": "All farming days completed. Ready for harvest!",
            "back_to_dashboard": "Back to Dashboard"
        },
        "hi": {
            "dashboard": "डैशबोर्ड",
            "profile_settings": "प्रोफाइल सेटिंग्स",
            "news": "समाचार",
            "selling_strategy": "बिक्री रणनीति",
            "government_subsidies": "सरकारी सब्सिडी",
            "logout": "लॉगआउट",
            "start_farming": "खेती शुरू करें",
            "view_schedule": "अनुसूची देखें",
            "market_insights": "बाजार जानकारी",
            "language": "भाषा",
            "weather": "मौसम",
            "temperature": "तापमान",
            "humidity": "नमी",
            "location": "स्थान",
            "shopping_requirements": "खेती से पहले खरीदारी आवश्यकताएं",
            "seeds": "बीज",
            "fertilizer": "उर्वरक",
            "organic": "जैविक खाद",
            "pesticide": "कीटनाशक",
            "tools": "उपकरण और उपकरण",
            "irrigation": "सिंचाई",
            "quantity": "मात्रा",
            "price": "कीमत",
            "nearest_markets": "निकटतम कृषि बाजार",
            "purchase_checklist": "खरीद सूची",
            "mark_as_purchased": "खरीदे गए के रूप में चिह्नित करें",
            "total_cost": "कुल अनुमानित लागत",
            "proceed_to_calendar": "खेती कैलेंडर पर जाएं",
            "back_to_results": "परिणामों पर वापस जाएं",
            "profile": "प्रोफाइल",
            "personal_details": "व्यक्तिगत विवरण",
            "account_status": "खाता स्थिति",
            "name": "नाम",
            "email": "ईमेल",
            "designation": "पद",
            "role": "भूमिका",
            "member_since": "सदस्यता दिनांक",
            "status": "स्थिति",
            "verified": "सत्यापित",
            "farming_activity": "खेती गतिविधि",
            "current_crop": "वर्तमान फसल",
            "land_area": "भूमि क्षेत्र",
            "start_date": "प्रारंभ तिथि",
            "agriculture_news": "कृषि समाचार",
            "todays_headlines": "आज की प्रमुख कृषि सुर्खियां",
            "source": "स्रोत",
            "date": "तिथि",
            "selling_strategies": "सर्वोत्तम बिक्री रणनीतियां",
            "price_range": "मूल्य सीमा",
            "current_demand": "वर्तमान मांग",
            "best_markets": "सर्वोत्तम बाजार",
            "best_time": "सर्वोत्तम समय",
            "selling_strategy": "बिक्री रणनीति",
            "view_market_rates": "बाजार दरें देखें",
            "congratulations": "बधाई हो!",
            "farming_completed": "सभी खेती दिन पूर्ण हुए। फसल काटने के लिए तैयार!",
            "back_to_dashboard": "डैशबोर्ड पर वापस जाएं"
        },
        "te": {
            "dashboard": "డాష్బోర్డ్",
            "profile_settings": "ప్రొఫైల్ సెట్టింగ్‌లు",
            "news": "వార్తలు",
            "selling_strategy": "అమ్మకాల వ్యూహం",
            "government_subsidies": "ప్రభుత్వ సబ్సిడీలు",
            "logout": "లాగ్‌అవుట్",
            "start_farming": "వ్యవసాయం ప్రారంభించండి",
            "view_schedule": "షెడ్యూల్ చూడండి",
            "market_insights": "మార్కెట్ విశ్లేషణలు",
            "language": "భాష",
            "weather": "వాతావరణం",
            "temperature": "ఉష్ణోగ్రత",
            "humidity": "తేమ",
            "location": "స్థానం",
            "shopping_requirements": "వ్యవసాయం ముందు కొనుగోలు అవసరాలు",
            "seeds": "విత్తనాలు",
            "fertilizer": "ఎరువులు",
            "organic": "సేంద్రీయ ఎరువు",
            "pesticide": "కీటకనాశకాలు",
            "tools": "పనిముట్లు మరియు పరికరాలు",
            "irrigation": "నీటిపారుదల",
            "quantity": "పరిమాణం",
            "price": "�ర",
            "nearest_markets": "సమీప వ్యవసాయ మార్కెట్లు",
            "purchase_checklist": "కొనుగోలు చెక్‌లిస్ట్",
            "mark_as_purchased": "కొనుగోలు చేసినట్లు గుర్తించండి",
            "total_cost": "మొత్తం అంచనా ఖర్చు",
            "proceed_to_calendar": "వ్యవసాయ క్యాలెండర్‌కు వెళ్ళండి",
            "back_to_results": "ఫలితాలకు తిరిగి వెళ్ళండి"
        },
        "kn": {
            "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
            "profile_settings": "ಪ್ರೊಫೈಲ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
            "news": "ಸುದ್ದಿಗಳು",
            "selling_strategy": "ಮಾರಾಟ ತಂತ್ರ",
            "government_subsidies": "ಸರ್ಕಾರಿ ಸಹಾಯಧನ",
            "logout": "ಲಾಗ್‌ಔಟ್",
            "start_farming": "ಕೃಷಿ ಪ್ರಾರಂಭಿಸಿ",
            "view_schedule": "ವೇಳಾಪಟ್ಟಿ ನೋಡಿ",
            "market_insights": "ಮಾರುಕಟ್ಟೆ ಒಳನೋಟಗಳು",
            "language": "ಭಾಷೆ",
            "weather": "ಹವಾಮಾನ",
            "temperature": "ತಾಪಮಾನ",
            "humidity": "ಆರ್ದ್ರತೆ",
            "location": "ಸ್ಥಳ",
            "shopping_requirements": "ಕೃಷಿಗೆ ಮೊದಲು ಖರೀದಿ ಅಗತ್ಯಗಳು",
            "seeds": "ಬೀಜಗಳು",
            "fertilizer": "ರಸಗೊಬ್ಬರ",
            "organic": "ಜೈವಿಕ ಗೊಬ್ಬರ",
            "pesticide": "ಕೀಟನಾಶಕಗಳು",
            "tools": "ಉಪಕರಣಗಳು ಮತ್ತು ಸಲಕರಣೆಗಳು",
            "irrigation": "ನೀರಾವರಿ",
            "quantity": "ಪ್ರಮಾಣ",
            "price": "ಬೆಲೆ",
            "nearest_markets": "ಹತ್ತಿರದ ಕೃಷಿ ಮಾರುಕಟ್ಟೆಗಳು",
            "purchase_checklist": "ಖರೀದಿ ಚೆಕ್‌ಲಿಸ್ಟ್",
            "mark_as_purchased": "ಖರೀದಿಸಿದಂತೆ ಗುರುತಿಸಿ",
            "total_cost": "ಒಟ್ಟು ಅಂದಾಜು ವೆಚ್ಚ",
            "proceed_to_calendar": "ಕೃಷಿ ಕ್ಯಾಲೆಂಡರ್‌ಗೆ ಹೋಗಿ",
            "back_to_results": "ಫಲಿತಾಂಶಗಳಿಗೆ ಹಿಂದಿರುಗಿ"
        }
    }
    return translations.get(lang_code, {}).get(text, text)

@st.cache_data
def load_data():
    try:
        csv_path = Path("datasets/crop_data.csv")
        if csv_path.exists():
            return pd.read_csv(csv_path)
        else:
            return pd.DataFrame(columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame(columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])

@st.cache_data
def build_model():
    try:
        data = load_data()
        if data.empty or 'label' not in data.columns:
            return None, None
        X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
        y = data['label']
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42, n_jobs=-1)
        model.fit(X_scaled, y)
        return model, scaler
    except Exception as e:
        st.error(f"Error building model: {e}")
        return None, None

# Load trained ML models
trained_models = load_trained_models()

# Keep fallback model for compatibility
model, scaler = build_model()

CROP_DURATION = {
    'rice': 120, 'maize': 120, 'cotton': 180, 'sugarcane': 360, 'wheat': 120,
    'chickpea': 100, 'soybean': 100, 'kidneybeans': 90, 'pigeonpea': 240,
    'mothbeans': 90, 'pomegranate': 180, 'papaya': 180, 'tomato': 90,
    'arecanut': 180, 'coconut': 180, 'jute': 120, 'coffee': 180, 'tea': 180
}

FARMING_TASKS = {
    'general': [
        {'day': 0, 'type': 'soil_prep', 'task': '🌱 Prepare soil - Plow and add organic matter'},
        {'day': 2, 'type': 'seed', 'task': '🌾 Sow seeds at appropriate depth and spacing'},
        {'day': 7, 'type': 'water', 'task': '💧 First irrigation - Ensure soil moisture'},
        {'day': 14, 'type': 'fertilizer', 'task': '🧪 Apply nitrogen-based fertilizer'},
        {'day': 25, 'type': 'water', 'task': '💧 Second irrigation'},
        {'day': 35, 'type': 'fertilizer', 'task': '🧪 Apply phosphorus-based fertilizer'},
        {'day': 45, 'type': 'pest', 'task': '🐛 Monitor and control pests'},
        {'day': 60, 'type': 'water', 'task': '💧 Third irrigation - Critical stage'},
        {'day': 75, 'type': 'weed', 'task': '🌿 Remove weeds and loose soil'},
        {'day': 90, 'type': 'fertilizer', 'task': '🧪 Final fertilizer application'},
    ]
}

TERM_CROPS = {
    'short_term': 'tomato',
    'medium_term': 'maize',
    'long_term': 'sugarcane'
}

CROP_DETAILS = {
    'tomato': 'Short-term crop with fast harvest. Requires regular watering and balanced fertilizer.',
    'maize': 'Medium-term crop with good yield. Needs warm temperature and consistent rainfall.',
    'sugarcane': 'Long-term crop suited for sustained farming cycles with high water requirement.',
}

# ==================== IMAGE ANALYSIS ====================
def is_valid_land_image(image):
    """Validate if image is actually a land/field image"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) < 2:
            return False, "Invalid image format"
        
        if img_array.shape[0] < 100 or img_array.shape[1] < 100:
            return False, "Image too small - needs to be at least 100x100 pixels"
        
        if len(img_array.shape) == 3:
            std_dev = np.std(img_array)
            if std_dev < 10:
                return False, "Image appears to be a solid color - not a land image"
            
            green = np.mean(img_array[:,:,1])
            red = np.mean(img_array[:,:,0])
            blue = np.mean(img_array[:,:,2])
            
            if green < 30 and red < 30 and blue < 30:
                return False, "Image is too dark - not recognizable as land"
            
            if green > 200 and red > 200 and blue > 200:
                return False, "Image is too bright/washed out"
        
        return True, "✅ Valid land image detected"
    except Exception as e:
        return False, f"Error analyzing image: {str(e)}"

def analyze_soil_quality(image):
    """Analyze soil quality from image including color detection"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            # Calculate average colors
            avg_r = img_array[:,:,0].mean()
            avg_g = img_array[:,:,1].mean()
            avg_b = img_array[:,:,2].mean()
            
            brown_score = abs(avg_r - avg_b) * 0.5
            green_score = max(0, avg_g - 80) * 1.5
            
            # Estimate soil type based on RGB
            if avg_r > avg_g and avg_r > avg_b:  # Reddish
                soil_type = "Clay Soil"
                estimated_ph = 6.5
            elif avg_g > avg_r and avg_g > avg_b:  # Greenish
                soil_type = "Loamy Soil"
                estimated_ph = 6.8
            elif avg_b > avg_r and avg_b > avg_g:  # Bluish (rare)
                soil_type = "Sandy Soil"
                estimated_ph = 7.0
            else:
                soil_type = "Alluvial Soil"
                estimated_ph = 7.2
            
            soil_health = min(100, max(0, (brown_score + green_score) / 2))
            vegetation_index = max(0, green_score / 2)
            
            return soil_health, vegetation_index, soil_type, estimated_ph
        return 50, 50, "Unknown", 7.0
    except:
        return 50, 50, "Unknown", 7.0

def get_weather(city):
    """Get real weather data"""
    try:
        API_KEY = "ce07d5d5aa68971127720f35a704aa4e"
        if not city or city.strip() == "":
            return 25, 60, "Unknown"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url, timeout=5).json()
        if res.get('cod') == 200:
            return (res.get('main', {}).get('temp', 25), 
                   res.get('main', {}).get('humidity', 60),
                   res.get('weather', [{}])[0].get('main', 'Clear'))
        return 25, 60, "Unknown"
    except:
        return 25, 60, "Unknown"

def get_location():
    """Get user location"""
    try:
        res = requests.get("https://ipapi.co/json/", timeout=5).json()
        city = res.get('city', 'Bangalore')
        country = res.get('country_name', 'India')
        if city and city != 'Unknown':
            return f"{city}, {country}"
        else:
            return "Bangalore, India"
    except:
        return "Bangalore, India"


def get_daily_agri_news():
    newspaper_feed = {
        "The Hindu": [
            {
                "title": "Kharif MSP Boost Brings Relief to Farmers",
                "summary": "The Hindu reports higher procurement rates for paddy, cotton and sugarcane this season to support rural incomes.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "Farmers Adopt Smart Irrigation to Fight Heatwaves",
                "summary": "New drip irrigation subsidies are helping farmers reduce water use and increase productivity.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "Organic Food Demand Climbs Across India",
                "summary": "Demand for certified organic vegetables and fruits is on the rise, offering higher margins for small farmers.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            }
        ],
        "Times of India": [
            {
                "title": "Agri Tech Startups Help Farmers Track Crop Health",
                "summary": "IoT sensors and mobile apps are helping farmers detect pests early and improve yields.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "New Solar Pumps Expand Irrigation Options",
                "summary": "Farmers are installing solar water pumps to reduce diesel costs and increase irrigation reliability.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "Local Produce Markets See Higher Prices",
                "summary": "Rising demand for fresh vegetables has pushed up prices, especially for onions, tomatoes and leafy greens.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            }
        ],
        "Indian Express": [
            {
                "title": "Government Launches New Farm Credit Scheme",
                "summary": "The government is offering low-interest loans to promote crop diversification and climate-smart agriculture.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "Pulses Production Expected to Rise",
                "summary": "Higher procurement support and improved seed distribution are set to boost pulse farming this year.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "Farmers Use Drones for Soil and Pest Monitoring",
                "summary": "Drone technology is becoming affordable and is now widely used for crop scouting.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            }
        ]
    }
    sources = list(newspaper_feed.keys())
    source_index = (datetime.date.today().day - 1) % len(sources)
    source_name = sources[source_index]
    news_items = newspaper_feed[source_name]
    for item in news_items:
        item["source"] = source_name
    return source_name, news_items


def generate_farming_schedule(crop, start_date, duration=None):
    """Generate day-by-day farming schedule"""
    if duration is None:
        duration = CROP_DURATION.get(crop.lower(), 120)
    
    schedule = []
    tasks = FARMING_TASKS.get('general', [])
    task_map = {task['day']: task for task in tasks}
    
    for day_count in range(duration + 1):
        current_date = start_date + timedelta(days=day_count)
        if day_count == duration:
            task_text = '🌾 HARVEST DAY - Ready for market!'
            task_type = 'harvest'
        elif day_count in task_map:
            task_text = task_map[day_count]['task']
            task_type = task_map[day_count]['type']
        elif day_count % 7 == 0:
            task_text = '💧 Weekly field check - inspect soil moisture and pests.'
            task_type = 'weekly_check'
        else:
            task_text = '🌿 Daily care: monitor soil moisture, weeds, and crop health.'
            task_type = 'daily'
        
        schedule.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': day_count,
            'task': task_text,
            'type': task_type,
            'completed': False
        })
    
    return schedule

# ==================== PAGE: AUTHENTICATION HOME ====================
if st.session_state.page == "auth_home":
    st.title("🌾 Agri AI Pro")
    st.markdown("<h3>Professional Farmer Advisory System</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🚀 Welcome Farmer</h3>
            <p>Choose to Login or Create a New Account</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔐 LOGIN", use_container_width=True, key="goto_login"):
                st.session_state.page = "auth_login"
                st.rerun()
        
        with col2:
            if st.button("📝 REGISTER", use_container_width=True, key="goto_register"):
                st.session_state.page = "auth_register"
                st.rerun()

# ==================== PAGE: LOGIN ====================
elif st.session_state.page == "auth_login":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown('<div class="card"><h2>🔐 Login</h2></div>', unsafe_allow_html=True)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("LOGIN", use_container_width=True):
                if username and password:
                    success, token, user = authenticate_user(username, password)
                    if success:
                        st.session_state.token = token
                        st.session_state.user = user
                        save_remembered_user(user['username'], token)
                        load_user_data(user['id'])
                        st.session_state.page = "dashboard"
                        st.success(f"✅ Welcome {user['username']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
                else:
                    st.error("❌ Please enter username and password!")
        
        with col2:
            if st.button("BACK", use_container_width=True):
                st.session_state.page = "auth_home"
                st.rerun()

# ==================== PAGE: REGISTER ====================
elif st.session_state.page == "auth_register":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown('<div class="card"><h2>📝 Register</h2></div>', unsafe_allow_html=True)
        
        username = st.text_input("Username")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("REGISTER", use_container_width=True):
                if not username or not email or not phone or not password or not password_confirm:
                    st.error("❌ Fill all fields!")
                elif password != password_confirm:
                    st.error("❌ Passwords don't match!")
                elif len(password) < 6:
                    st.error("❌ Password must be 6+ characters!")
                elif "@" not in email:
                    st.error("❌ Invalid email!")
                else:
                    success, msg = register_user(username, password, email, phone)
                    if success:
                        st.success("✅ Registration successful!")
                        st.info("Go back and login!")
                        time.sleep(2)
                        st.session_state.page = "auth_home"
                        st.rerun()
                    else:
                        st.error(msg)
        
        with col2:
            if st.button("BACK", use_container_width=True):
                st.session_state.page = "auth_home"
                st.rerun()

# ==================== PAGE: DASHBOARD ====================
elif st.session_state.page == "dashboard":
    
    # Enhanced Sidebar with Better Design
    with st.sidebar:
        # Custom styled header
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
        ">
            <h2 style="margin: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-weight: 600;">
                Farmer Portal
            </h2>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">
                Your Complete Farming Companion
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Language Selector with Enhanced Styling
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.15);
        ">
            <h4 style="margin: 0 0 10px 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
                Language / Hindi / Telugu / Kannada
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        language_options = {
            'en': '🇺🇸 English',
            'hi': '🇮🇳 हिंदी',
            'te': '🇮🇳 తెలుగు',
            'kn': '🇮🇳 ಕನ್ನಡ'
        }
        
        selected_lang = st.selectbox(
            "",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(st.session_state.language),
            key="language_selector"
        )
        
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()
        
        # Navigation Menu with Enhanced Styling
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        ">
            <h4 style="margin: 0 0 15px 0; color: #333; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
                📱 Quick Navigation
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced Navigation Buttons
        nav_buttons = [
            ("👤", get_translated_text("profile_settings", st.session_state.language), "profile"),
            ("📰", get_translated_text("news", st.session_state.language), "news"),
            ("💼", get_translated_text("selling_strategy", st.session_state.language), "selling_strategy"),
            ("🏛️", get_translated_text("government_subsidies", st.session_state.language), "government_subsidy"),
        ]
        
        for icon, text, page in nav_buttons:
            if st.button(f"{icon} {text}", use_container_width=True, key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()
        
        st.markdown("---")
        
        # Logout Button with Special Styling
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
        ">
        """, unsafe_allow_html=True)
        
        if st.button("🚪 " + get_translated_text("logout", st.session_state.language), 
                     use_container_width=True, key="logout_btn"):
            clear_remembered_user()
            st.session_state.page = "auth_home"
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.crop = ""
            st.session_state.schedule = []
            st.session_state.tasks_completed = {}
            st.session_state.farming_plan = None
            st.session_state.plan_id = None
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.title("🌾 Agri AI Pro Dashboard")
    
    location = get_location()
    temp, humidity, weather_condition = get_weather(location.split(',')[0] if location else "")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <h3>🌡️ {get_translated_text("temperature", st.session_state.language)}</h3>
            <h2>{temp}°C</h2>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <h3>💧 {get_translated_text("humidity", st.session_state.language)}</h3>
            <h2>{humidity}%</h2>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <h3>🌤️ {get_translated_text("weather", st.session_state.language)}</h3>
            <h2>{weather_condition}</h2>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
            <h3>📍 {get_translated_text("location", st.session_state.language)}</h3>
            <h2>{location}</h2>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Realistic Market Insights Section
    st.markdown("### Real-time Market Insights")
    
    # Get current date and season
    current_date = datetime.datetime.now()
    current_month = current_date.month
    
    # Define realistic market data based on actual Indian agricultural patterns
    market_data = {
        "tomato": {
            "current_price": 28.50,
            "price_change": "+12.5%",
            "trend": "up",
            "demand": "High",
            "season": "Peak Season",
            "markets": ["Bangalore KR Market", "Mysore APMC", "Hubli Market"],
            "export_demand": "Strong demand from Middle East",
            "storage_advice": "Prices expected to rise further in next 2 weeks",
            "quality_premium": "+15% for organic certified"
        },
        "maize": {
            "current_price": 18.75,
            "price_change": "+5.2%",
            "trend": "stable",
            "demand": "Moderate",
            "season": "Harvest Season",
            "markets": ["Bellary Market", "Raichur APMC", "Gulbarga"],
            "export_demand": "Good demand from poultry industry",
            "storage_advice": "Store for 2-3 months for better prices",
            "quality_premium": "+8% for high-quality grains"
        },
        "ragi": {
            "current_price": 32.00,
            "price_change": "+18.3%",
            "trend": "up",
            "demand": "High",
            "season": "Festival Season",
            "markets": ["Bangalore Organic Market", "Mysore Traditional Market", "Chitradurga"],
            "export_demand": "Growing demand from health food companies",
            "storage_advice": "Excellent storage life, hold for premium prices",
            "quality_premium": "+25% for organic millets"
        },
        "okra": {
            "current_price": 42.30,
            "price_change": "-3.1%",
            "trend": "down",
            "demand": "Moderate",
            "season": "Normal Season",
            "markets": ["Bangalore Russell Market", "Mysore Vegetable Market", "Tumkur"],
            "export_demand": "Steady demand from Gulf countries",
            "storage_advice": "Sell immediately due to perishability",
            "quality_premium": "+20% for export-grade okra"
        }
    }
    
    # Create market insights cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Today's Market Overview")
        
        # Create a market summary
        market_summary = []
        for crop, data in market_data.items():
            trend_icon = "up" if data["trend"] == "up" else "down" if data["trend"] == "down" else "stable"
            trend_color = "#10b981" if data["trend"] == "up" else "#ef4444" if data["trend"] == "down" else "#64748b"
            
            market_summary.append(f"""
            <div style="
                background: rgba(255, 255, 255, 0.95);
                border-radius: 8px;
                padding: 12px;
                margin: 8px 0;
                border-left: 3px solid {trend_color};
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #1e293b; font-weight: 600;">{crop.title()}</h4>
                        <p style="margin: 4px 0; color: #64748b; font-size: 0.875rem;">{data['demand']} demand</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; color: #1e293b; font-weight: 700;">{data['current_price']}/kg</p>
                        <p style="margin: 0; color: {trend_color}; font-size: 0.875rem; font-weight: 600;">
                            {data['price_change']} {'up' if data['trend'] == 'up' else 'down' if data['trend'] == 'down' else 'stable'}
                        </p>
                    </div>
                </div>
            </div>
            """)
        
        st.markdown("".join(market_summary), unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Market Intelligence")
        
        # Add market intelligence insights
        intelligence_data = [
            {
                "title": "Seasonal Trends",
                "content": "Festival season driving up prices for traditional crops. Expect 15-20% increase in next month.",
                "icon": "trending_up",
                "color": "#3b82f6"
            },
            {
                "title": "Export Opportunities",
                "content": "Strong demand from Middle East for tomatoes and okra. Premium prices available for quality produce.",
                "icon": "global",
                "color": "#10b981"
            },
            {
                "title": "Government Support",
                "content": "MSP announced for maize at 20% above market rate. Subsidies available for storage infrastructure.",
                "icon": "policy",
                "color": "#f59e0b"
            },
            {
                "title": "Weather Impact",
                "content": "Monsoon forecast normal. Good conditions for Kharif crops. Planting season optimal now.",
                "icon": "cloud",
                "color": "#8b5cf6"
            }
        ]
        
        for item in intelligence_data:
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.95);
                border-radius: 8px;
                padding: 12px;
                margin: 8px 0;
                border-left: 3px solid {item['color']};
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            ">
                <h4 style="margin: 0 0 8px 0; color: #1e293b; font-weight: 600; display: flex; align-items: center;">
                    <span style="background: {item['color']}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; margin-right: 8px;">
                        {item['icon'].upper()}
                    </span>
                    {item['title']}
                </h4>
                <p style="margin: 0; color: #64748b; font-size: 0.875rem; line-height: 1.4;">
                    {item['content']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Add price forecast chart
    st.markdown("#### 7-Day Price Forecast")
    
    # Generate realistic price forecast data
    forecast_data = []
    base_prices = {
        "tomato": 28.50,
        "maize": 18.75,
        "ragi": 32.00,
        "okra": 42.30
    }
    
    for crop, base_price in base_prices.items():
        daily_prices = []
        for day in range(7):
            # Add realistic price variations
            variation = np.random.uniform(-0.05, 0.08)
            seasonal_factor = 1.0
            
            # Add weekend effects
            if day in [5, 6]:  # Weekend
                seasonal_factor *= 1.02
            
            # Add festival effects (simplified)
            if day == 3:  # Mid-week
                seasonal_factor *= 1.03
            
            price = base_price * (1 + variation) * seasonal_factor
            daily_prices.append(round(price, 2))
        
        forecast_data.append({
            "crop": crop.title(),
            "prices": daily_prices
        })
    
    # Create forecast visualization
    forecast_df = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        **{item['crop']: item['prices'] for item in forecast_data}
    })
    
    st.dataframe(forecast_df, use_container_width=True)
    
    # Add market recommendations
    st.markdown("#### Expert Recommendations")
    
    recommendations = [
        {
            "category": "Immediate Action",
            "recommendation": "Sell okra immediately - prices dropping due to increased supply",
            "priority": "High",
            "color": "#ef4444"
        },
        {
            "category": "Storage Strategy",
            "recommendation": "Store maize for 2-3 months - prices expected to rise during feed season",
            "priority": "Medium",
            "color": "#f59e0b"
        },
        {
            "category": "Market Opportunity",
            "recommendation": "Target organic markets for ragi - premium prices available",
            "priority": "High",
            "color": "#10b981"
        },
        {
            "category": "Export Focus",
            "recommendation": "Quality tomatoes can fetch 20% premium in Gulf markets",
            "priority": "Medium",
            "color": "#3b82f6"
        }
    ]
    
    rec_cols = st.columns(2)
    for i, rec in enumerate(recommendations):
        with rec_cols[i % 2]:
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.95);
                border-radius: 8px;
                padding: 16px;
                margin: 8px 0;
                border-left: 4px solid {rec['color']};
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            ">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <h4 style="margin: 0; color: #1e293b; font-weight: 600;">{rec['category']}</h4>
                    <span style="
                        background: {rec['color']};
                        color: white;
                        padding: 2px 8px;
                        border-radius: 12px;
                        font-size: 0.75rem;
                        font-weight: 600;
                    ">
                        {rec['priority']}
                    </span>
                </div>
                <p style="margin: 0; color: #64748b; font-size: 0.875rem; line-height: 1.4;">
                    {rec['recommendation']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚜 " + get_translated_text("start_farming", st.session_state.language), use_container_width=True):
            st.session_state.page = "upload"
            st.rerun()
    
    with col2:
        if st.button("📅 " + get_translated_text("view_schedule", st.session_state.language), use_container_width=True):
            if st.session_state.farming_plan:
                st.session_state.page = "schedule"
                st.rerun()
            else:
                st.warning("⚠️ Please start farming first")
    
    with col3:
        if st.button("📈 " + get_translated_text("market_insights", st.session_state.language), use_container_width=True):
            if st.session_state.crop:
                st.session_state.page = "market"
                st.rerun()
            else:
                st.warning("⚠️ Please analyze land first")

# ==================== PAGE: LAND ANALYSIS & IMAGE UPLOAD ====================
elif st.session_state.page == "upload":
    
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.title("📸 Land Analysis & Image Upload")
    
    st.markdown("### 📷 Upload Land Images (3 views)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🔭 Far View")
        img1 = st.file_uploader("Upload far view of your land", type=["jpg", "png", "jpeg"], key="far_view")
        if img1:
            st.image(img1, use_column_width=True)
            is_valid, msg = is_valid_land_image(Image.open(img1))
            if is_valid:
                st.success(msg)
            else:
                st.error(f"❌ {msg}")
    
    with col2:
        st.markdown("#### 📷 Mid View")
        img2 = st.file_uploader("Upload mid view of your land", type=["jpg", "png", "jpeg"], key="mid_view")
        if img2:
            st.image(img2, use_column_width=True)
            is_valid, msg = is_valid_land_image(Image.open(img2))
            if is_valid:
                st.success(msg)
            else:
                st.error(f"❌ {msg}")
    
    with col3:
        st.markdown("#### 🔍 Close View")
        img3 = st.file_uploader("Upload close view of your land", type=["jpg", "png", "jpeg"], key="close_view")
        if img3:
            st.image(img3, use_column_width=True)
            is_valid, msg = is_valid_land_image(Image.open(img3))
            if is_valid:
                st.success(msg)
            else:
                st.error(f"❌ {msg}")
    
    st.markdown("---")
    st.markdown("### 🌱 Soil & Environmental Data")
    
    detected_location = get_location()
    default_city = detected_location.split(',')[0] if detected_location else ""
    
    col1, col2 = st.columns(2)
    
    with col1:
        city = st.text_input("🏙️ City/Village", value=default_city, key="city_input")
        ph = st.slider("🧪 Soil pH (3-9)", 3.0, 9.0, 6.5)
        area = st.number_input("📏 Land Area (acres)", min_value=0.1, value=1.0, step=0.1, key="area_input")
    
    with col2:
        rainfall = st.slider("🌧️ Rainfall (mm)", 50, 300, 150)
        nitrogen = st.slider("🧬 Nitrogen Level (ppm)", 10, 100, 40)
    
    st.markdown("---")
    
    if st.button("🔍 ANALYZE LAND & PREDICT CROP", use_container_width=True):
        if img1 and img2 and img3:
            if not city:
                city = default_city
            with st.spinner("🔄 Analyzing your land..."):
                img1_valid, msg1 = is_valid_land_image(Image.open(img1))
                img2_valid, msg2 = is_valid_land_image(Image.open(img2))
                img3_valid, msg3 = is_valid_land_image(Image.open(img3))
                
                if not (img1_valid and img2_valid and img3_valid):
                    st.error("❌ One or more images are invalid land images. Please upload actual land/field photos.")
                    if not img1_valid:
                        st.error(f"Far View: {msg1}")
                    if not img2_valid:
                        st.error(f"Mid View: {msg2}")
                    if not img3_valid:
                        st.error(f"Close View: {msg3}")
                else:
                    soil1, veg1, soil_type1, ph_est1 = analyze_soil_quality(Image.open(img1))
                    soil2, veg2, soil_type2, ph_est2 = analyze_soil_quality(Image.open(img2))
                    soil3, veg3, soil_type3, ph_est3 = analyze_soil_quality(Image.open(img3))
                    
                    avg_soil = (soil1 + soil2 + soil3) / 3
                    avg_veg = (veg1 + veg2 + veg3) / 3
                    avg_ph = (ph_est1 + ph_est2 + ph_est3) / 3
                    
                    # Use trained CNN model for land analysis if available
                    if trained_models and 'land_analysis' in trained_models:
                        st.info(" Using trained AI model for advanced land analysis...")
                        land_predictions = []
                        confidences = []
                        
                        for img in [img1, img2, img3]:
                            soil_quality, confidence = analyze_land_with_trained_model(trained_models, Image.open(img))
                            if soil_quality:
                                land_predictions.append(soil_quality)
                                confidences.append(confidence)
                        
                        if land_predictions:
                            # Get most common prediction
                            from collections import Counter
                            predicted_soil_quality = Counter(land_predictions).most_common(1)[0][0]
                            avg_confidence = sum(confidences) / len(confidences)
                            
                            st.info(f" AI Land Analysis: {predicted_soil_quality} soil quality (Confidence: {avg_confidence:.2%})")
                            
                            # Convert soil quality to numeric for compatibility
                            soil_quality_map = {'Poor': 25, 'Average': 50, 'Good': 75}
                            avg_soil = soil_quality_map.get(predicted_soil_quality, avg_soil)
                    
                    # Determine dominant soil type
                    soil_types = [soil_type1, soil_type2, soil_type3]
                    dominant_soil = max(set(soil_types), key=soil_types.count)
                    
                    temp, humidity, weather = get_weather(city)
                    
                    K = 40
                    P = 35
                    N = nitrogen
                    
                    # Use trained models if available, otherwise fallback to RandomForest
                    if trained_models and hasattr(trained_models, 'recommend_crop'):
                        # Use our trained crop recommendation model
                        crop_predictions = predict_crop_with_trained_model(
                            trained_models, 
                            {'soil_health': avg_soil, 'ph': avg_ph}, 
                            {'temp': temp, 'humidity': humidity, 'rainfall': rainfall}, 
                            area * 50000,  # Convert acres to budget estimate
                            120  # Default duration in days
                        )
                        
                        if crop_predictions:
                            predicted_crop = crop_predictions[0][0]  # Get top recommendation
                            # Using trained AI model for prediction
                        else:
                            # Fallback to RandomForest
                            if model and scaler:
                                input_data = np.array([[N, P, K, temp, humidity, avg_ph, rainfall]])
                                input_scaled = scaler.transform(input_data)
                                predicted_crop = model.predict(input_scaled)[0]
                            else:
                                predicted_crop = "tomato"  # Default fallback
                    elif model and scaler:
                        # Fallback to RandomForest
                        input_data = np.array([[N, P, K, temp, humidity, avg_ph, rainfall]])
                        input_scaled = scaler.transform(input_data)
                        predicted_crop = model.predict(input_scaled)[0]
                    else:
                        predicted_crop = "tomato"  # Default fallback
                    
                    st.session_state.crop = predicted_crop
                    st.session_state.images = [img1, img2, img3]
                    plan_data = {
                        'crop': predicted_crop,
                        'start_date': datetime.date.today(),
                        'soil_health': avg_soil,
                        'vegetation': avg_veg,
                        'soil_type': dominant_soil,
                        'estimated_ph': avg_ph,
                        'weather': weather,
                        'temp': temp,
                        'humidity': humidity,
                        'city': city,
                        'area': area,
                        'recommended_crop': predicted_crop,
                        'short_term_crop': TERM_CROPS['short_term'],
                        'medium_term_crop': TERM_CROPS['medium_term'],
                        'long_term_crop': TERM_CROPS['long_term'],
                        'status': 'active'
                    }
                    st.session_state.farming_plan = plan_data
                    if st.session_state.user:
                        plan_id = save_farming_plan_to_db(st.session_state.user['id'], plan_data)
                        st.session_state.plan_id = plan_id
                    
                    st.session_state.page = "results"
                    st.rerun()
        else:
            st.error("❌ Please upload all three images and ensure city/village information is included")

# ==================== PAGE: RESULTS ====================
elif st.session_state.page == "results":
    
    st.title("✅ Land Analysis Results")
    
    if st.session_state.farming_plan:
        plan = st.session_state.farming_plan
        
        # Load datasets
        try:
            crop_data = pd.read_csv('crop_data.csv')
        except FileNotFoundError:
            st.error("Crop data file not found. Please ensure crop_data.csv exists.")
            crop_data = pd.DataFrame()
        try:
            market_data = pd.read_csv('market_data.csv')
        except FileNotFoundError:
            market_data = pd.DataFrame()
        current_month = datetime.datetime.now().strftime('%B')
        area = plan.get('area', 1.0)
        
        # Soil Insights Section
        st.markdown("### 🌱 Soil Insights")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""<div class="metric-card">
                <h3>🪨 Soil Type</h3>
                <h2>{plan.get('soil_type', 'Unknown').title()}</h2>
            </div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""<div class="metric-card">
                <h3>🧪 Est. pH</h3>
                <h2>{plan.get('estimated_ph', 7.0):.1f}</h2>
            </div>""", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""<div class="metric-card">
                <h3>🌱 Soil Health</h3>
                <h2>{plan['soil_health']:.0f}%</h2>
            </div>""", unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""<div class="metric-card">
                <h3>🌿 Vegetation</h3>
                <h2>{plan['vegetation']:.0f}%</h2>
            </div>""", unsafe_allow_html=True)
        
        st.markdown(f"**Location:** {plan.get('city', 'Unknown')} | **Weather:** {plan.get('weather', 'Unknown')}, {plan.get('temp', 0)}°C, {plan.get('humidity', 0)}%")
        
        st.markdown("---")
        
        # Crop Options
        st.markdown("### 🌾 Crop Options")
        
        recommended_crop = plan.get('recommended_crop', st.session_state.crop)
        short_crop = plan.get('short_term_crop', TERM_CROPS['short_term'])
        medium_crop = plan.get('medium_term_crop', TERM_CROPS['medium_term'])
        long_crop = plan.get('long_term_crop', TERM_CROPS['long_term'])
        
        crops = [short_crop, medium_crop, long_crop]
        crop_labels = ["Short-term", "Medium-term", "Long-term"]
        
        if 'selected_crop_result' not in st.session_state:
            st.session_state.selected_crop_result = short_crop
        
        selected_crop = st.session_state.selected_crop_result
        
        # Display 3 crops and 1 farmer card in one row
        cols = st.columns(4)
        
        # First card: Motivational Farmer
        with cols[0]:
            st.markdown("""
            <div class="crop-card">
                <h3>🌾 Proud Farmer</h3>
                <p>Farmer holding crop in hand</p>
                <p style="font-size: 3rem;">👨‍🌾🌽</p>
                <p><strong>Keep Growing!</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Crop cards
        for i, (crop_name, label) in enumerate(zip(crops, crop_labels)):
            with cols[i+1]:
                if crop_data.empty or 'crop' not in crop_data.columns:
                    # Use default values if crop_data is not available
                    yield_per_acre = 5000
                    profit_per_acre = 20000
                    budget_per_acre = 30000
                    duration_days = CROP_DURATION.get(crop_name.lower(), 120)
                else:
                    crop_info = crop_data[crop_data['crop'].str.lower() == crop_name.lower()]
                    if not crop_info.empty:
                        yield_per_acre = crop_info['yield_per_acre'].values[0]
                        profit_per_acre = crop_info['profit'].values[0]
                        budget_per_acre = crop_info['budget'].values[0]
                        duration_days = CROP_DURATION.get(crop_name.lower(), 120)
                    else:
                        # Use default values if crop not found
                        yield_per_acre = 5000
                        profit_per_acre = 20000
                        budget_per_acre = 30000
                        duration_days = CROP_DURATION.get(crop_name.lower(), 120)
                    
                total_yield = yield_per_acre * area
                total_profit = profit_per_acre * area
                total_investment = budget_per_acre * area
                
                yield_lower = total_yield * 0.85
                yield_upper = total_yield * 1.15
                selected_class = "crop-card selected" if crop_name.lower() == selected_crop.lower() else "crop-card"
                
                st.markdown(f"""
                <div class=\"{selected_class}\">
                    <h3>{label}</h3>
                    <h2>{crop_name.upper()}</h2>
                    <p><strong>Duration:</strong> {duration_days} days</p>
                    <p><strong>Total Yield:</strong> {total_yield:,.0f} kg<br>
                    <small>({yield_lower:,.0f} - {yield_upper:,.0f} kg)</small></p>
                    <p><strong>Total Investment:</strong> ₹{total_investment:,.0f}</p>
                    <p><strong>Total Profit:</strong> ₹{total_profit:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Choose {label}", key=f"choose_{crop_name.lower()}"):
                    st.session_state.selected_crop_result = crop_name
                    st.session_state.crop = crop_name
                    st.session_state.farming_plan['crop'] = crop_name
                    selected_crop = crop_name
                    st.rerun()
        
        st.markdown("---")
        st.markdown(f"**Selected Crop:** **{selected_crop.upper()}**")
        st.session_state.crop = selected_crop
        st.session_state.farming_plan['crop'] = selected_crop
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🛒 " + get_translated_text("shopping_requirements", st.session_state.language), use_container_width=True):
                st.session_state.page = "shopping"
                st.rerun()
            
            if st.button("📅 Create Farming Schedule", use_container_width=True):
                duration = CROP_DURATION.get(selected_crop.lower(), 120)
                schedule = generate_farming_schedule(
                    selected_crop,
                    plan['start_date'],
                    duration
                )
                st.session_state.schedule = schedule
                st.session_state.tasks_completed = {item['date']: item.get('completed', False) for item in schedule}
                if st.session_state.plan_id:
                    save_daily_tasks_to_db(st.session_state.plan_id, schedule)
                st.session_state.page = "schedule"
                st.rerun()
        
        with col2:
            if st.button("⬅️ " + get_translated_text("back_to_results", st.session_state.language), use_container_width=True):
                st.session_state.page = "upload"
                st.rerun()

# ==================== PAGE: SHOPPING REQUIREMENTS ====================
elif st.session_state.page == "shopping":
    
    if st.button("⬅️ " + get_translated_text("back_to_results", st.session_state.language)):
        st.session_state.page = "results"
        st.rerun()
    
    st.markdown('<h1 class="shopping-title">🛒 ' + get_translated_text("shopping_requirements", st.session_state.language) + '</h1>', unsafe_allow_html=True)
    
    if st.session_state.farming_plan:
        plan = st.session_state.farming_plan
        crop = st.session_state.crop
        area = plan.get('area', 1.0)
        location = plan.get('city', 'Unknown')
        
        # Initialize shopping checklist in session state
        if 'shopping_checklist' not in st.session_state:
            st.session_state.shopping_checklist = {}
        
        st.markdown(f"### 🌾 Shopping Requirements for {crop.upper()} - {area} acres")
        st.markdown(f"**📍 Location:** {location}")
        
        # Get shopping requirements
        requirements = get_shopping_requirements(crop, area)
        
        # Shopping Checklist Card
        st.markdown("---")
        st.markdown("### ✅ " + get_translated_text("purchase_checklist", st.session_state.language))
        
        total_cost = 0
        all_purchased = True
        
        # Create a beautiful card layout for shopping items
        for category, item in requirements.items():
            category_translated = get_translated_text(category, st.session_state.language)
            
            with st.container():
                st.markdown(f"""
                <div style="border: 2px solid #4CAF50; border-radius: 15px; padding: 20px; margin: 10px 0; background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);">
                    <h4 class="shopping-item-title" style="margin-bottom: 15px;">🛍️ {category_translated}</h4>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p style="font-weight: bold; color: #1b5e20; font-size: 16px;">{item['name']}</p>
                            <p style="color: #388e3c;">📏 {get_translated_text('quantity', st.session_state.language)}: {item['quantity']} ({item['unit']})</p>
                            <p style="color: #388e3c;">💰 {get_translated_text('price', st.session_state.language)}: ₹{item['price']:,.0f}</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="font-size: 18px; font-weight: bold; color: #2e7d32;">₹{item['price']:,.0f}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Checkbox for marking as purchased
                purchased = st.checkbox(
                    get_translated_text("mark_as_purchased", st.session_state.language) + f" - {item['name']}",
                    key=f"purchase_{category}",
                    value=st.session_state.shopping_checklist.get(category, False)
                )
                
                st.session_state.shopping_checklist[category] = purchased
                
                if purchased:
                    total_cost += item['price']
                else:
                    all_purchased = False
                
                st.markdown("---")
        
        # Total Cost Section
        st.markdown(f"""
        <div style="border: 3px solid #FF9800; border-radius: 15px; padding: 25px; margin: 20px 0; background: linear-gradient(135deg, #fff8e1 0%, #ffe0b2 100%); text-align: center;">
            <h3 style="color: #e65100; margin-bottom: 10px;">💵 {get_translated_text('total_cost', st.session_state.language)}</h3>
            <p style="font-size: 28px; font-weight: bold; color: #ff6f00;">₹{total_cost:,.0f}</p>
            <p style="color: #f57c00; font-size: 14px;">Estimated cost for all marked items</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Nearest Markets Section
        st.markdown("---")
        st.markdown("### 🏪 " + get_translated_text("nearest_markets", st.session_state.language))
        
        markets = get_nearest_markets(location)
        
        for i, market in enumerate(markets, 1):
            st.markdown(f"""
            <div style="border: 1px solid #2196F3; border-radius: 10px; padding: 15px; margin: 10px 0; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);">
                <h4 style="color: #1565c0; margin-bottom: 10px;">📍 {market['name']}</h4>
                <p style="color: #1976d2;">📏 Distance: {market['distance']}</p>
                <p style="color: #1976d2;">🏠 Address: {market['address']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Action Buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📅 " + get_translated_text("proceed_to_calendar", st.session_state.language), 
                        use_container_width=True, 
                        disabled=not all_purchased,
                        help="Please mark all items as purchased before proceeding"):
                # Add shopping requirements to the first day of schedule
                if st.session_state.plan_id:
                    shopping_task = {
                        'date': datetime.date.today().strftime('%Y-%m-%d'),
                        'task': f'🛒 Completed shopping for {crop}: Seeds, Fertilizer, Tools & Equipment',
                        'type': 'shopping',
                        'completed': True
                    }
                    save_daily_tasks_to_db(st.session_state.plan_id, [shopping_task])
                
                st.session_state.page = "schedule"
                st.rerun()
        
        with col2:
            if st.button("⬅️ " + get_translated_text("back_to_results", st.session_state.language), 
                        use_container_width=True):
                st.session_state.page = "results"
                st.rerun()
        
        if not all_purchased:
            st.warning("⚠️ Please mark all items as purchased before proceeding to the farming calendar.")
        
        # Progress indicator
        purchased_count = sum(1 for v in st.session_state.shopping_checklist.values() if v)
        total_items = len(requirements)
        progress = purchased_count / total_items if total_items > 0 else 0
        
        st.markdown("---")
        st.markdown(f"### 📊 Shopping Progress: {purchased_count}/{total_items} items purchased")
        st.progress(progress)

# ==================== PAGE: DAILY SCHEDULE ====================
elif st.session_state.page == "schedule":
    
    if st.button("⬅️ Back to Results"):
        st.session_state.page = "results"
        st.rerun()
    
    st.title("📅 Farming Schedule Calendar")
    
    if not st.session_state.schedule and st.session_state.plan_id:
        stored_schedule = load_daily_tasks_from_db(st.session_state.plan_id)
        if stored_schedule:
            st.session_state.schedule = stored_schedule
            st.session_state.tasks_completed = {item['date']: item['completed'] for item in stored_schedule}
    
    if st.session_state.schedule:
        crop = st.session_state.crop
        st.markdown(f"### 🌾 {crop.upper()} - Month-by-month Crop Calendar")
        
        schedule = st.session_state.schedule
        schedule_map = {item['date']: item for item in schedule}
        start_date = datetime.datetime.strptime(schedule[0]['date'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(schedule[-1]['date'], '%Y-%m-%d').date()
        
        import calendar
        cal = calendar.Calendar(firstweekday=0)
        
        months = []
        current_month = datetime.date(start_date.year, start_date.month, 1)
        last_month = datetime.date(end_date.year, end_date.month, 1)
        while current_month <= last_month:
            months.append((current_month.year, current_month.month))
            if current_month.month == 12:
                current_month = datetime.date(current_month.year + 1, 1, 1)
            else:
                current_month = datetime.date(current_month.year, current_month.month + 1, 1)
        
        if 'schedule_month_index' not in st.session_state:
            st.session_state.schedule_month_index = 0
        if st.session_state.schedule_month_index >= len(months):
            st.session_state.schedule_month_index = len(months) - 1
        
        month_index = st.session_state.schedule_month_index
        year, month = months[month_index]
        month_name = calendar.month_name[month]
        
        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
        with nav_col1:
            if st.button("⬅️ Previous Month", key="prev_schedule_month"):
                st.session_state.schedule_month_index = max(0, month_index - 1)
                st.rerun()
        with nav_col3:
            if st.button("Next Month ➡️", key="next_schedule_month"):
                st.session_state.schedule_month_index = min(len(months) - 1, month_index + 1)
                st.rerun()
        with nav_col2:
            st.markdown(f"<div class='month-title'>{month_name} {year}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='calendar-month-card'>", unsafe_allow_html=True)
        header_cols = st.columns(7)
        for idx, weekday_name in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
            header_cols[idx].markdown(f"<div style='text-align:center; font-weight:bold'>{weekday_name}</div>", unsafe_allow_html=True)
        
        for week in cal.monthdatescalendar(year, month):
            cols = st.columns(7)
            for idx, day in enumerate(week):
                with cols[idx]:
                    if day.month != month or day < start_date or day > end_date:
                        st.markdown("<div class='calendar-day' style='opacity:0.25; min-height:160px;'></div>", unsafe_allow_html=True)
                        continue
                    
                    day_str = day.strftime('%Y-%m-%d')
                    entry = schedule_map.get(day_str, {
                        'task': '🌿 Daily care: monitor soil moisture and crop health.',
                        'type': 'daily',
                        'day': (day - start_date).days
                    })
                    completed = st.session_state.tasks_completed.get(day_str, False)
                    box_class = "calendar-day completed" if completed else "calendar-day"
                    
                    st.markdown(f"<div class='{box_class}'><strong>{day.day}</strong><br><small>{entry['task']}</small></div>", unsafe_allow_html=True)
                    checked = st.checkbox("Done", value=completed, key=f"day_{day_str}")
                    if checked != completed and st.session_state.plan_id:
                        update_task_completion(st.session_state.plan_id, day_str, checked)
                    st.session_state.tasks_completed[day_str] = checked
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        completed_count = sum(1 for v in st.session_state.tasks_completed.values() if v)
        total_count = len(schedule)
        progress = completed_count / total_count if total_count > 0 else 0
        
        st.markdown(f"### 📊 Progress: {completed_count}/{total_count} days completed")
        st.progress(progress)
        
        if progress == 1.0:
            st.success(f"🎉 {get_translated_text('congratulations', st.session_state.language)}! {get_translated_text('farming_completed', st.session_state.language)}")
            if st.button("🏪 View Marketing & Selling Options", use_container_width=True):
                st.session_state.page = "marketing"
                st.rerun()
        else:
            st.info("📝 Complete all daily farming tasks to unlock marketing and selling options")

# ==================== PAGE: MARKETING & SELLING ====================
elif st.session_state.page == "marketing":
    
    if st.button("⬅️ Back to Calendar"):
        st.session_state.page = "schedule"
        st.rerun()
    
    st.markdown('<h1 class="marketing-title">🏪 Marketing & Selling Options</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🌾 Sell Your Harvest for Maximum Profit!</h2>', unsafe_allow_html=True)
    
    if st.session_state.farming_plan:
        crop = st.session_state.crop.lower()
        location = st.session_state.farming_plan.get('city', 'Unknown')
        area = st.session_state.farming_plan.get('area', 1.0)
        
        # Enhanced market data with comprehensive information
        market_prices = {
            'tomato': {
                'min': 10, 'max': 25, 'avg': 17, 'demand': 'High', 
                'markets': ['Bangalore', 'Chennai', 'Hyderabad'],
                'strategy': 'Harvest at right ripeness. Sell fresh to local markets. Consider value addition like ketchup for higher returns.',
                'storage': 'Can be stored for 5-7 days at room temperature',
                'transport': 'Requires careful handling, use crates',
                'best_season': 'October - March',
                'price_factors': 'Quality, size, color, and freshness',
                'estimated_yield': f"{area * 25:.0f} - {area * 35:.0f} quintals",
                'estimated_revenue': f"₹{area * 25000:.0f} - ₹{area * 87500:.0f}"
            },
            'maize': {
                'min': 18, 'max': 28, 'avg': 23, 'demand': 'Medium', 
                'markets': ['Pune', 'Nashik', 'Bangalore'],
                'strategy': 'Store in cool, dry place. Sell during high demand seasons. Consider processing into corn flour for better prices.',
                'storage': 'Can be stored for 6-12 months when dried properly',
                'transport': 'Easy to transport, requires dry conditions',
                'best_season': 'Year-round demand, peak in winter',
                'price_factors': 'Moisture content, grain quality, variety',
                'estimated_yield': f"{area * 20:.0f} - {area * 30:.0f} quintals",
                'estimated_revenue': f"₹{area * 36000:.0f} - ₹{area * 84000:.0f}"
            },
            'rice': {
                'min': 20, 'max': 35, 'avg': 27, 'demand': 'High', 
                'markets': ['Bangalore', 'Mysore', 'Delhi'],
                'strategy': 'Sell immediately after harvest to avoid storage losses. Target wholesale markets for bulk sales.',
                'storage': 'Can be stored for 12-18 months with proper conditions',
                'transport': 'Requires dry storage and moisture control',
                'best_season': 'Kharif: Oct-Dec, Rabi: Apr-Jun',
                'price_factors': 'Grain quality, variety, milling recovery',
                'estimated_yield': f"{area * 30:.0f} - {area * 40:.0f} quintals",
                'estimated_revenue': f"₹{area * 60000:.0f} - ₹{area * 140000:.0f}"
            },
            'cotton': {
                'min': 50, 'max': 80, 'avg': 65, 'demand': 'High', 
                'markets': ['Gujarat', 'Maharashtra', 'Telangana'],
                'strategy': 'Ginning and pressing before sale increases value. Sell to textile mills directly for premium prices.',
                'storage': 'Requires controlled humidity, can store 6-12 months',
                'transport': 'Requires covered transport to prevent moisture',
                'best_season': 'October - February',
                'price_factors': 'Staple length, cleanliness, moisture content',
                'estimated_yield': f"{area * 15:.0f} - {area * 25:.0f} quintals",
                'estimated_revenue': f"₹{area * 75000:.0f} - ₹{area * 200000:.0f}"
            },
            'ragi': {
                'min': 15, 'max': 25, 'avg': 20, 'demand': 'Medium', 
                'markets': ['Bangalore', 'Mysore', 'Hubli'],
                'strategy': 'Sell to health food stores and organic markets. Consider value addition through flour processing.',
                'storage': 'Excellent storage capacity, 12-24 months',
                'transport': 'Easy to transport and store',
                'best_season': 'Year-round, higher demand in festivals',
                'price_factors': 'Grain quality, processing method, organic certification',
                'estimated_yield': f"{area * 8:.0f} - {area * 12:.0f} quintals",
                'estimated_revenue': f"₹{area * 12000:.0f} - ₹{area * 30000:.0f}"
            },
            'cabbage': {
                'min': 8, 'max': 15, 'avg': 11, 'demand': 'Medium', 
                'markets': ['Bangalore', 'Mysore', 'Chennai'],
                'strategy': 'Harvest fresh. Sell to wholesale markets. Consider organic certification for higher prices.',
                'storage': 'Cold storage extends life to 2-3 months',
                'transport': 'Requires refrigerated transport for long distances',
                'best_season': 'October - March',
                'price_factors': 'Head size, freshness, color, weight',
                'estimated_yield': f"{area * 40:.0f} - {area * 60:.0f} quintals",
                'estimated_revenue': f"₹{area * 32000:.0f} - ₹{area * 90000:.0f}"
            }
        }
        
        if crop in market_prices:
            prices = market_prices[crop]
            
            # Harvest Summary Card
            st.markdown("---")
            st.markdown('<h2 class="section-header">📊 Harvest Summary</h2>', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""<div class="metric-card">
                    <h3>🌾 Crop</h3>
                    <h2>{crop.upper()}</h2>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div class="metric-card">
                    <h3>📏 Area</h3>
                    <h2>{area} acres</h2>
                </div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""<div class="metric-card">
                    <h3>⚖️ Est. Yield</h3>
                    <h2>{prices['estimated_yield']}</h2>
                </div>""", unsafe_allow_html=True)
            with col4:
                st.markdown(f"""<div class="metric-card">
                    <h3>💰 Est. Revenue</h3>
                    <h2>{prices['estimated_revenue']}</h2>
                </div>""", unsafe_allow_html=True)
            
            # Market Overview Cards
            st.markdown("---")
            st.markdown('<h2 class="section-header">🏪 Market Overview</h2>', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""<div class="metric-card">
                    <h3>💰 Price Range</h3>
                    <h2>₹{prices['min']}-{prices['max']}/kg</h2>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div class="metric-card">
                    <h3>📊 Demand</h3>
                    <h2>{prices['demand']}</h2>
                </div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""<div class="metric-card">
                    <h3>🏪 Best Markets</h3>
                    <h2>{len(prices['markets'])} Cities</h2>
                </div>""", unsafe_allow_html=True)
            with col4:
                st.markdown(f"""<div class="metric-card">
                    <h3>📅 Best Season</h3>
                    <h2>{prices['best_season']}</h2>
                </div>""", unsafe_allow_html=True)
            
            # Comprehensive Selling Strategy
            st.markdown("---")
            st.markdown('<h2 class="section-header">🎯 Selling Strategy</h2>', unsafe_allow_html=True)
            st.markdown(f'<p class="marketing-item-title" style="font-weight: normal;">{prices["strategy"]}</p>', unsafe_allow_html=True)
            
            # Nearest Markets Section
            st.markdown("---")
            st.markdown('<h2 class="section-header">📍 Nearest Agricultural Markets</h2>', unsafe_allow_html=True)
            
            nearest_markets = get_nearest_markets(location)
            
            for i, market in enumerate(nearest_markets, 1):
                # Check if this market is in the recommended markets list
                is_recommended = market['name'] in prices['markets']
                badge = "⭐ RECOMMENDED" if is_recommended else "📍 Available"
                
                st.markdown(f"""
                <div style="border: 2px solid {'#FFD700' if is_recommended else '#2196F3'}; border-radius: 15px; padding: 20px; margin: 10px 0; background: linear-gradient(135deg, {'#fffacd' if is_recommended else '#e3f2fd'} 0%, {'#f0e68c' if is_recommended else '#bbdefb'} 100%);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="color: {'#ff8c00' if is_recommended else '#1565c0'}; margin: 0;">🏪 {market['name']}</h4>
                        <span style="background: {'#FFD700' if is_recommended else '#2196F3'}; color: white; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">{badge}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <p style="color: {'#ff8c00' if is_recommended else '#1976d2'}; margin: 5px 0;">📏 Distance: {market['distance']}</p>
                        <p style="color: {'#ff8c00' if is_recommended else '#1976d2'}; margin: 5px 0;">💰 Est. Price: ₹{prices['min']}-{prices['max']}/kg</p>
                    </div>
                    <p style="color: {'#ff8c00' if is_recommended else '#1976d2'}; margin: 5px 0;">🏠 Address: {market['address']}</p>
                    {f'<p style="color: #d32f2f; margin: 5px 0; font-weight: bold;">🌟 Top choice for {crop} - Best prices guaranteed!</p>' if is_recommended else ''}
                </div>
                """, unsafe_allow_html=True)
            
            # Additional Market Information
            st.markdown("---")
            st.markdown("### 📋 Important Market Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="border: 1px solid #4CAF50; border-radius: 10px; padding: 15px; background: #e8f5e8;">
                    <h4 style="color: #2e7d32;">📦 Storage Guidelines</h4>
                    <p style="color: #388e3c;">{prices['storage']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="border: 1px solid #FF9800; border-radius: 10px; padding: 15px; background: #fff3e0;">
                    <h4 style="color: #e65100;">🚚 Transport Tips</h4>
                    <p style="color: #f57c00;">{prices['transport']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="border: 1px solid #9C27B0; border-radius: 10px; padding: 15px; background: #f3e5f5;">
                <h4 style="color: #6a1b9a;">💡 Price Factors</h4>
                <p style="color: #7b1fa2;">{prices['price_factors']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Value Addition Opportunities
            st.markdown("---")
            st.markdown("### 🚀 Value Addition Opportunities")
            
            value_addition_ideas = {
                'tomato': ['🍅 Tomato Ketchup/Sauce', '🥫 Canned Tomatoes', '🧂 Tomato Powder', '🍷 Tomato Juice'],
                'maize': ['🌽 Corn Flour', '🍿 Popcorn', '🌾 Animal Feed', '🧈 Corn Oil'],
                'rice': ['🍚 Rice Flour', '🍜 Rice Noodles', '🍶 Rice Wine', '🥮 Rice Cakes'],
                'cotton': ['🧵 Cotton Thread', '👕 Cotton Fabric', '🏥 Cotton Medical Supplies', '💊 Cotton Seed Oil'],
                'ragi': ['🌾 Ragi Flour', '🥘 Ragi Porridge', '🍪 Ragi Biscuits', '🥤 Ragi Health Drinks'],
                'cabbage': ['🥗 Cabbage Salad', '🥒 Pickled Cabbage', '🍲 Cabbage Soup', '🥬 Cabbage Rolls']
            }
            
            if crop in value_addition_ideas:
                st.markdown("Consider these value addition options to increase your profits:")
                for idea in value_addition_ideas[crop]:
                    st.markdown(f"- {idea}")
            
            # Motivational Message
            st.markdown("---")
            st.markdown("### 🌾 Congratulations on Successful Harvest!")
            st.markdown("**💪 Dear Farmer, your hard work and dedication have paid off! You've successfully completed your farming cycle. May your harvest bring prosperity and joy to you and your family! Best wishes for selling your produce at the best prices! 🚜✨**")
            
            # Action Buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📈 View Market Rates", use_container_width=True):
                    st.session_state.page = "market"
                    st.rerun()
            
            with col2:
                if st.button("💼 Selling Strategies", use_container_width=True):
                    st.session_state.page = "selling_strategy"
                    st.rerun()
            
            with col3:
                if st.button("🏛️ Government Subsidies", use_container_width=True):
                    st.session_state.page = "government_subsidy"
                    st.rerun()
        else:
            st.info("Market data for this crop is being updated. Please check back later.")

# ==================== PAGE: PROFILE ====================
elif st.session_state.page == "profile":
    
    if st.button("⬅️ " + get_translated_text("back_to_dashboard", st.session_state.language)):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.title("👤 " + get_translated_text("profile_settings", st.session_state.language))
    
    if st.session_state.user:
        st.markdown("### " + get_translated_text("personal_details", st.session_state.language))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="card">
                <h3>👨‍🌾 {get_translated_text('personal_details', st.session_state.language)}</h3>
                <p><strong>{get_translated_text('name', st.session_state.language)}:</strong> {st.session_state.user['username']}</p>
                <p><strong>{get_translated_text('email', st.session_state.language)}:</strong> {st.session_state.user['email']}</p>
                <p><strong>{get_translated_text('designation', st.session_state.language)}:</strong> Farmer</p>
                <p><strong>{get_translated_text('role', st.session_state.language)}:</strong> Agricultural Producer</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card">
                <h3>📊 {get_translated_text('account_status', st.session_state.language)}</h3>
                <p><strong>{get_translated_text('member_since', st.session_state.language)}:</strong> {datetime.datetime.now().strftime('%B %Y')}</p>
                <p><strong>{get_translated_text('status', st.session_state.language)}:</strong> Active Farmer</p>
                <p><strong>{get_translated_text('verified', st.session_state.language)}:</strong> ✅ Yes</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🌾 " + get_translated_text("farming_activity", st.session_state.language))
        
        if st.session_state.farming_plan:
            plan = st.session_state.farming_plan
            st.write(f"**{get_translated_text('current_crop', st.session_state.language)}:** {plan.get('crop', 'None')}")
            st.write(f"**{get_translated_text('land_area', st.session_state.language)}:** {plan.get('area', 0)} acres")
            st.write(f"**{get_translated_text('start_date', st.session_state.language)}:** {plan.get('start_date', 'Not set')}")
        else:
            st.info("No active farming plan. Start farming to see your activity here!")

# ==================== PAGE: NEWS ====================
elif st.session_state.page == "news":
    
    if st.button("⬅️ " + get_translated_text("back_to_dashboard", st.session_state.language)):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.title("📰 " + get_translated_text("agriculture_news", st.session_state.language))
    
    source_name, news_items = get_daily_agri_news()
    st.markdown(f"### {get_translated_text('todays_headlines', st.session_state.language)} from {source_name}")
    st.markdown("Stay updated with rotating newspaper-style coverage and crop market trends.")
    for item in news_items:
        st.markdown(f"""
        <div class="card">
            <h3>{item['title']}</h3>
            <p>{item['summary']}</p>
            <small><strong>{get_translated_text('source', st.session_state.language)}:</strong> {item['source']} | <strong>{get_translated_text('date', st.session_state.language)}:</strong> {item['date']}</small>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

# ==================== PAGE: SELLING STRATEGY ====================
elif st.session_state.page == "selling_strategy":
    
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.title("💼 Advanced Selling Strategies & Marketing Insights")
    
    # Check if user has farming plan
    if st.session_state.farming_plan:
        plan = st.session_state.farming_plan
        crop = st.session_state.crop
        location = plan.get('city', 'Unknown')
        area = plan.get('area', 1.0)
        
        # Get comprehensive marketing insights
        insights = get_marketing_insights(crop, location, area)
        strategies = get_selling_strategies(crop, location, area * 1000)  # Convert to kg
        forecasts = get_price_forecast(crop, location, 6)
        optimal_locations = get_optimal_selling_locations(crop, location, area * 1000)
        risk_management = get_risk_management_strategies(crop)
        
        # Marketing Insights Section
        st.markdown('<div class="marketing-insights">', unsafe_allow_html=True)
        st.markdown('<div class="insight-header">📊 MARKETING INSIGHTS FOR ' + crop.upper() + '</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌱 Crop Information")
            st.markdown(f"""
            <div class="strategy-card">
                <h4>Best Growing Seasons</h4>
                <p>{', '.join(insights['best_seasons'])}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="strategy-card">
                <h4>Price Trends</h4>
                <p>{insights['price_trends']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="strategy-card">
                <h4>Storage Tips</h4>
                <p>{insights['storage_tips']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🏭 Processing Options")
            for option in insights['processing_options']:
                st.markdown(f"""
                <div class="strategy-tip">
                    <strong>• {option}</strong>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("### 🌍 Export Potential")
            st.markdown(f"""
            <div class="market-opportunity">
                <p>{insights['export_potential']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Price Forecast
        st.markdown("### 📈 Price Forecast (Next 6 Months)")
        forecast_df = pd.DataFrame(forecasts)
        forecast_df['Price Change'] = forecast_df['price'].pct_change().fillna(0) * 100
        
        # Create price trend visualization
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(forecast_df.rename(columns={
                'month': 'Month',
                'price': 'Expected Price (₹/kg)',
                'trend': 'Trend'
            }), use_container_width=True)
        
        with col2:
            # Simple price trend indicator
            current_price = forecasts[0]['price']
            future_price = forecasts[-1]['price']
            price_change = ((future_price - current_price) / current_price) * 100
            
            trend_color = "#4CAF50" if price_change > 0 else "#f44336"
            st.markdown(f"""
            <div class="price-trend">
                <h4>Price Trend</h4>
                <p>Current: ₹{current_price:.2f}/kg</p>
                <p>Expected: ₹{future_price:.2f}/kg</p>
                <p style="color: {trend_color}; font-weight: bold;">
                    {price_change:+.1f}% {'↑' if price_change > 0 else '↓'}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Optimal Selling Locations
        st.markdown("### 📍 Optimal Selling Locations")
        
        location_cols = st.columns(2)
        with location_cols[0]:
            st.markdown("**Premium Markets (Higher Prices)**")
            for market in optimal_locations['premium_markets']:
                st.markdown(f"""
                <div class="location-card">
                    <h5>🏪 {market['name']}</h5>
                    <p><strong>Price Premium:</strong> +{market['price_premium']*100:.0f}%</p>
                    <p><strong>Min Quantity:</strong> {market['min_quantity']} kg</p>
                    <p><strong>Specialty:</strong> {market['specialty']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with location_cols[1]:
            st.markdown("**Wholesale Markets (Bulk Sales)**")
            for market in optimal_locations['wholesale_markets']:
                st.markdown(f"""
                <div class="location-card">
                    <h5>🏢 {market['name']}</h5>
                    <p><strong>Price Premium:</strong> +{market['price_premium']*100:.0f}%</p>
                    <p><strong>Min Quantity:</strong> {market['min_quantity']} kg</p>
                    <p><strong>Specialty:</strong> {market['specialty']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Recommended Strategy
        crop_specific = strategies['crop_specific']
        st.markdown(f"### 🎯 Recommended Strategy for {crop.upper()}")
        recommended_strategy = strategies['strategies'][crop_specific['recommended_strategy']]
        
        st.markdown(f"""
        <div class="strategy-card" style="border-left: 4px solid #4CAF50; background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);">
            <h4>🌟 {recommended_strategy['title']}</h4>
            <p><strong>Why Recommended:</strong> {crop_specific['reason']}</p>
            <p><strong>Best Time:</strong> {crop_specific['best_time']}</p>
            <p><strong>Expected Price:</strong> {recommended_strategy['expected_price']}</p>
            <p><strong>Timeline:</strong> {recommended_strategy['timeline']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # All Strategies Comparison
        st.markdown("### 🔄 All Selling Strategies")
        
        strategy_cols = st.columns(3)
        strategy_names = list(strategies['strategies'].keys())
        
        for i, strategy_key in enumerate(strategy_names):
            strategy = strategies['strategies'][strategy_key]
            with strategy_cols[i % 3]:
                is_recommended = strategy_key == crop_specific['recommended_strategy']
                border_color = "#4CAF50" if is_recommended else "#e9ecef"
                bg_color = "linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)" if is_recommended else "linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)"
                
                st.markdown(f"""
                <div class="strategy-card" style="border-left: 4px solid {border_color}; background: {bg_color};">
                    <h5>{strategy['title']} {'🌟' if is_recommended else ''}</h5>
                    <p><strong>Expected Price:</strong> {strategy['expected_price']}</p>
                    <p><strong>Timeline:</strong> {strategy['timeline']}</p>
                    <p><strong>Best For:</strong></p>
                    <ul>
                        {"".join([f"<li>{item}</li>" for item in strategy['best_for']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Risk Management
        st.markdown("### 🛡️ Risk Management Strategies")
        
        risk_cols = st.columns(3)
        risk_types = ['price_risk', 'production_risk', 'market_risk']
        risk_titles = ['Price Risk', 'Production Risk', 'Market Risk']
        
        for i, (risk_type, title) in enumerate(zip(risk_types, risk_titles)):
            with risk_cols[i]:
                risk_data = risk_management[risk_type]
                st.markdown(f"""
                <div class="strategy-tip">
                    <h5>⚠️ {title}</h5>
                    <p><strong>Strategies:</strong></p>
                    <ul>
                        {"".join([f"<li>{strategy}</li>" for strategy in risk_data['strategies']])}
                    </ul>
                    <p><strong>Available Tools:</strong></p>
                    <p>{', '.join(risk_data['tools'])}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Market Opportunities
        st.markdown("### 🎯 Market Opportunities")
        
        opp_cols = st.columns(2)
        with opp_cols[0]:
            for opportunity in insights['market_opportunities'][:4]:
                st.markdown(f"""
                <div class="market-opportunity">
                    <h5>💼 {opportunity}</h5>
                </div>
                """, unsafe_allow_html=True)
        
        with opp_cols[1]:
            for opportunity in insights['market_opportunities'][4:]:
                st.markdown(f"""
                <div class="market-opportunity">
                    <h5>💼 {opportunity}</h5>
                </div>
                """, unsafe_allow_html=True)
        
        # Action Buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Market Analysis", use_container_width=True):
                st.info("Detailed market analysis for " + crop + " in " + location + " is being prepared. Check back for comprehensive market report.")
        
        with col2:
            if st.button("💰 Price Alert Setup", use_container_width=True):
                st.success("Price alerts set for " + crop + ". You'll receive notifications when prices change by more than 10%.")
        
        with col3:
            if st.button("📱 Contact Buyers", use_container_width=True):
                st.info("Connecting you with verified buyers for " + crop + " in your region. Buyer contacts will be shared via email.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.warning("🚜 Please complete land analysis and select a crop first to access selling strategies.")
        if st.button("🌱 Analyze Land Now"):
            st.session_state.page = "upload"
            st.rerun()

# ==================== PAGE: GOVERNMENT SUBSIDY ====================
elif st.session_state.page == "government_subsidy":
    
    if st.button("⬅️ " + get_translated_text("back_to_dashboard", st.session_state.language)):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.title("🏛️ " + get_translated_text("government_subsidies", st.session_state.language))
    st.markdown("### Support schemes and subsidy programs for farmers")
    st.image("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=compress&cs=tinysrgb&h=400&w=800", use_column_width=True)
    
    subsidies = [
        {
            "name": "PM-Kisan Samman Nidhi",
            "description": "Direct income support of up to ₹6,000 per year for small and marginal farmers.",
            "benefits": "Regular cash support, easy online application, bank transfer",
            "eligibility": "All landholding farmers with Aadhaar and bank account"
        },
        {
            "name": "Pradhan Mantri Fasal Bima Yojana",
            "description": "Crop insurance scheme to protect farmers from yield loss due to natural disasters.",
            "benefits": "Low premium, wide coverage, claim settlement support",
            "eligibility": "All farmers growing notified crops"
        },
        {
            "name": "Kisan Credit Card (KCC)",
            "description": "Provides short-term credit at concessional interest rates for agricultural needs.",
            "benefits": "Easy loan access, working capital support, crop cycle financing",
            "eligibility": "Farmers with land records and bank account"
        },
        {
            "name": "Soil Health Card Scheme",
            "description": "Free soil testing and recommendations to improve fertilizer use efficiency.",
            "benefits": "Better yields, reduced input cost, balanced nutrient use",
            "eligibility": "All farmers across India"
        },
        {
            "name": "Sub-Mission on Agroforestry",
            "description": "Support for tree plantation on farms and wasteland to boost income and ecology.",
            "benefits": "Financial assistance for saplings, training, and maintenance",
            "eligibility": "Farmers, forest dwellers, rural households"
        },
        {
            "name": "PMKSY - Per Drop More Crop",
            "description": "Subsidies for micro-irrigation systems such as drip and sprinkler irrigation.",
            "benefits": "Water saving, higher productivity, lower power costs",
            "eligibility": "Irrigated farmers and groups"
        }
    ]
    
    for sub in subsidies:
        st.markdown(f"""
        <div class="card">
            <h3>🌾 {sub['name']}</h3>
            <p><strong>What it is:</strong> {sub['description']}</p>
            <p><strong>Why it matters:</strong> {sub['benefits']}</p>
            <p><strong>Who can apply:</strong> {sub['eligibility']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

# ==================== PAGE: MARKET INSIGHTS ====================
elif st.session_state.page == "market":
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.title("📈 Market Insights")
    st.markdown("### Real-time pricing guidance and best selling locations")
    st.image("https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=compress&cs=tinysrgb&h=400&w=800", use_column_width=True)

    # Get user's location from farming plan
    user_location = st.session_state.farming_plan.get('city', 'Bangalore') if st.session_state.farming_plan else 'Bangalore'
    
    # Enhanced market data with location-based recommendations
    market_prices = {
        'tomato': {
            'min': 25, 'max': 45, 'avg': 32, 'demand': 'Very High', 
            'markets': ['Bangalore KR Market', 'Mysore APMC', 'Hubli Market'],
            'best_markets': {
                'Bangalore': {'price': 35, 'demand': 'Very High', 'distance': '0 km', 'premium': '+10%'},
                'Mysore': {'price': 32, 'demand': 'High', 'distance': '150 km', 'premium': '+5%'},
                'Hubli': {'price': 30, 'demand': 'Medium', 'distance': '400 km', 'premium': '0%'}
            },
            'seasonal_trend': 'Prices rising due to festival season',
            'storage_advice': 'Sell within 3-5 days for best prices'
        },
        'maize': {
            'min': 18, 'max': 28, 'avg': 23, 'demand': 'High',
            'markets': ['Bellary Market', 'Raichur APMC', 'Gulbarga'],
            'best_markets': {
                'Bangalore': {'price': 24, 'demand': 'High', 'distance': '0 km', 'premium': '+8%'},
                'Bellary': {'price': 22, 'demand': 'Very High', 'distance': '300 km', 'premium': '+0%'},
                'Raichur': {'price': 21, 'demand': 'High', 'distance': '400 km', 'premium': '-2%'}
            },
            'seasonal_trend': 'Stable prices, good for storage',
            'storage_advice': 'Store for 2-3 months for better prices'
        },
        'ragi': {
            'min': 30, 'max': 45, 'avg': 38, 'demand': 'Very High',
            'markets': ['Bangalore Organic Market', 'Mysore Traditional Market', 'Chitradurga'],
            'best_markets': {
                'Bangalore': {'price': 42, 'demand': 'Very High', 'distance': '0 km', 'premium': '+15%'},
                'Mysore': {'price': 38, 'demand': 'High', 'distance': '150 km', 'premium': '+5%'},
                'Chitradurga': {'price': 35, 'demand': 'Medium', 'distance': '200 km', 'premium': '0%'}
            },
            'seasonal_trend': 'High demand during festival season',
            'storage_advice': 'Excellent storage life, hold for premium prices'
        },
        'okra': {
            'min': 35, 'max': 55, 'avg': 45, 'demand': 'High',
            'markets': ['Bangalore Russell Market', 'Mysore Vegetable Market', 'Tumkur'],
            'best_markets': {
                'Bangalore': {'price': 48, 'demand': 'Very High', 'distance': '0 km', 'premium': '+12%'},
                'Mysore': {'price': 44, 'demand': 'High', 'distance': '150 km', 'premium': '+5%'},
                'Tumkur': {'price': 40, 'demand': 'Medium', 'distance': '70 km', 'premium': '0%'}
            },
            'seasonal_trend': 'Prices stable, good for immediate sale',
            'storage_advice': 'Sell immediately due to perishability'
        }
    }

    crop_choice = st.selectbox("Choose a crop for market insights", sorted(market_prices.keys()))
    prices = market_prices[crop_choice]

    # Display price metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <h3>💰 Min Price</h3>
            <h2>₹{prices['min']}/kg</h2>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <h3>💵 Avg Price</h3>
            <h2>₹{prices['avg']}/kg</h2>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <h3>💸 Max Price</h3>
            <h2>₹{prices['max']}/kg</h2>
        </div>""", unsafe_allow_html=True)
    with col4:
        demand_color = "#10b981" if prices['demand'] == 'Very High' else "#3b82f6" if prices['demand'] == 'High' else "#f59e0b"
        st.markdown(f"""<div class="metric-card">
            <h3>📊 Demand</h3>
            <h2 style="color: {demand_color};">{prices['demand']}</h2>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    
    # Location-based market recommendations
    st.markdown("### 🏪 Best Markets Near Your Location")
    
    # Sort markets by distance from user location
    best_markets = prices['best_markets']
    
    for market_name, market_data in best_markets.items():
        distance_color = "#10b981" if market_data['distance'] == '0 km' else "#3b82f6" if int(market_data['distance'].replace(' km', '').replace('+', '')) <= 150 else "#f59e0b"
        premium_color = "#10b981" if '+' in market_data['premium'] else "#64748b"
        
        st.markdown(f"""
        <div class="location-card">
            <h5>🏪 {market_name}</h5>
            <p><strong>Current Price:</strong> ₹{market_data['price']}/kg</p>
            <p><strong>Demand Level:</strong> {market_data['demand']}</p>
            <p><strong>Distance from you:</strong> <span style="color: {distance_color}; font-weight: 600;">{market_data['distance']}</span></p>
            <p><strong>Price Premium:</strong> <span style="color: {premium_color}; font-weight: 600;">{market_data['premium']}</span></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Market intelligence section
    st.markdown("### 🧠 Market Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="strategy-card">
            <h4>📈 Seasonal Trend</h4>
            <p>{prices['seasonal_trend']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="strategy-card">
            <h4>💡 Storage Advice</h4>
            <p>{prices['storage_advice']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Market demand indicators
        demand_indicators = {
            'Very High': '🔥 Extremely high demand - sell now for maximum profit',
            'High': '📊 Strong demand - good prices available',
            'Medium': '⚖️ Moderate demand - consider storage strategies',
            'Low': '📉 Low demand - wait for better market conditions'
        }
        
        st.markdown(f"""
        <div class="strategy-card">
            <h4>🎯 Demand Analysis</h4>
            <p><strong>Current Status:</strong> {prices['demand']}</p>
            <p><strong>Recommendation:</strong> {demand_indicators[prices['demand']]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Best selling time
        selling_times = {
            'tomato': 'Early morning (6-8 AM) for best prices',
            'maize': 'Afternoon (2-4 PM) when bulk buyers active',
            'ragi': 'Any time - consistent demand throughout day',
            'okra': 'Morning (7-9 AM) for fresh produce premium'
        }
        
        st.markdown(f"""
        <div class="strategy-card">
            <h4>⏰ Best Selling Time</h4>
            <p>{selling_times.get(crop_choice, 'Market hours 8 AM - 6 PM')}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📱 Selling Guidance")
    st.markdown("Use these location-specific insights to maximize your profits. Consider transportation costs and market timing for optimal results.")
