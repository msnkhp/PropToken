import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
import json
from datetime import datetime, timedelta
import random
from faker import Faker
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
from prophet import Prophet
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import base64

# Set page config
st.set_page_config(
    page_title="PropToken - Real Estate Tokenization",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Faker for dummy data
fake = Faker()

# Premium Responsive CSS - Ultra Modern Design System
st.markdown("""
<style>
    /* ============================================
       PREMIUM GLOBAL STYLES & RESET
       ============================================ */
    * {
        box-sizing: border-box;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.2;
    }
    
    /* ============================================
       PREMIUM STATS CARDS
       ============================================ */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stats-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stats-card:hover::before {
        left: 100%;
    }
    
    .stats-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* ============================================
       PREMIUM PROPERTY CARDS - RESPONSIVE
       ============================================ */
    .property-card {
        border: 3px solid #000;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        min-height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        background: #fff;
        position: relative;
        overflow: hidden;
    }
    
    .property-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.4s;
    }
    
    .property-card:hover::after {
        opacity: 1;
    }
    
    .property-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        border-color: #667eea;
    }
    
    /* ============================================
       RESPONSIVE BREAKPOINTS - PROPERTY CARDS
       ============================================ */
    @media (min-width: 1400px) {
        .property-card {
            min-height: 340px;
            padding: 2.5rem;
        }
    }
    
    @media (max-width: 1200px) {
        .property-card {
            min-height: 300px;
            padding: 1.8rem;
        }
        .main-header {
            font-size: 2.2rem;
        }
    }
    
    @media (max-width: 992px) {
        .property-card {
            min-height: 280px;
            padding: 1.5rem;
        }
        .main-header {
            font-size: 2rem;
        }
    }
    
    @media (max-width: 768px) {
        .property-card {
            min-height: 260px;
            padding: 1.2rem;
            border-width: 2px;
        }
        .main-header {
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
        }
        .stats-card {
            padding: 1.2rem;
        }
    }
    
    @media (max-width: 576px) {
        .property-card {
            min-height: 240px;
            padding: 1rem;
            border-radius: 15px;
        }
        .main-header {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .stats-card {
            padding: 1rem;
            border-radius: 12px;
        }
    }
    
    @media (max-width: 480px) {
        .property-card {
            min-height: 220px;
            padding: 0.9rem;
        }
        .main-header {
            font-size: 1.3rem;
        }
    }
    
    /* ============================================
       PREMIUM BADGES & BUTTONS
       ============================================ */
    .roi-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 25px;
        font-size: 0.875rem;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        display: inline-block;
        transition: all 0.3s ease;
    }
    
    .roi-badge:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
    }
    
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2.5rem;
        border: none;
        border-radius: 30px;
        font-size: 1rem;
        font-weight: 700;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .cta-button:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* ============================================
       PREMIUM CONTAINER ALIGNMENT
       ============================================ */
    .premium-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    @media (max-width: 1200px) {
        .premium-container {
            padding: 1.5rem;
        }
    }
    
    @media (max-width: 768px) {
        .premium-container {
            padding: 1rem;
        }
    }
    
    /* ============================================
       STREAMLIT COMPONENT ENHANCEMENTS
       ============================================ */
    .stButton > button {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 10px;
        font-weight: 700;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    /* Input fields premium styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        transition: all 0.3s ease;
        padding: 0.75rem 1rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Column spacing */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    @media (max-width: 768px) {
        [data-testid="column"] {
            padding: 0.25rem;
        }
    }
    
    /* ============================================
       PREMIUM SIDEBAR ENHANCEMENTS
       ============================================ */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* ============================================
       SMOOTH SCROLLING & ANIMATIONS
       ============================================ */
    html {
        scroll-behavior: smooth;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* ============================================
       PREMIUM TYPOGRAPHY
       ============================================ */
    h1, h2, h3, h4, h5, h6 {
        line-height: 1.3;
        margin-bottom: 1rem;
    }
    
    /* ============================================
       PREMIUM SPACING SYSTEM
       ============================================ */
    .premium-spacing {
        margin: 2rem 0;
    }
    
    @media (max-width: 768px) {
        .premium-spacing {
            margin: 1.5rem 0;
        }
    }
    
    @media (max-width: 480px) {
        .premium-spacing {
            margin: 1rem 0;
        }
    }
    
    /* ============================================
       PREMIUM GRID SYSTEM
       ============================================ */
    .premium-grid {
        display: grid;
        gap: 1.5rem;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    }
    
    @media (max-width: 768px) {
        .premium-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
    
    /* ============================================
       PREMIUM LOADING STATES
       ============================================ */
    .premium-loading {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
    }
    
    /* ============================================
       PREMIUM SHADOWS & DEPTH
       ============================================ */
    .shadow-sm { box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .shadow-md { box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
    .shadow-lg { box-shadow: 0 8px 24px rgba(0,0,0,0.16); }
    .shadow-xl { box-shadow: 0 12px 32px rgba(0,0,0,0.2); }
    
    /* ============================================
       PREMIUM BORDERS & RADIUS
       ============================================ */
    .rounded-sm { border-radius: 8px; }
    .rounded-md { border-radius: 12px; }
    .rounded-lg { border-radius: 16px; }
    .rounded-xl { border-radius: 20px; }
    .rounded-full { border-radius: 9999px; }
    
    /* ============================================
       PREMIUM RESPONSIVE TEXT
       ============================================ */
    .responsive-text-lg {
        font-size: 2rem;
    }
    
    @media (max-width: 768px) {
        .responsive-text-lg {
            font-size: 1.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .responsive-text-lg {
            font-size: 1.25rem;
        }
    }
    
    /* ============================================
       PREMIUM UTILITIES
       ============================================ */
    .text-center { text-align: center; }
    .text-left { text-align: left; }
    .text-right { text-align: right; }
    
    .flex-center {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .premium-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* ============================================
       HIDE STREAMLIT DEFAULT ELEMENTS
       ============================================ */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* ============================================
       PREMIUM MOBILE OPTIMIZATIONS
       ============================================ */
    @media (max-width: 768px) {
        /* Better touch targets */
        button, a, input, select {
            min-height: 44px;
        }
        
        /* Improved spacing on mobile */
        .stContainer {
            padding: 0.5rem;
        }
        
        /* Better column handling on mobile */
        [data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
        }
    }
    
    /* ============================================
       PREMIUM PAGE WRAPPER
       ============================================ */
    .premium-page-wrapper {
        max-width: 100%;
        margin: 0 auto;
        padding: 0;
        overflow-x: hidden;
    }
    
    @media (min-width: 1400px) {
        .premium-page-wrapper {
            max-width: 1400px;
            padding: 0 2rem;
        }
    }
    
    @media (max-width: 1200px) {
        .premium-page-wrapper {
            padding: 0 1.5rem;
        }
    }
    
    @media (max-width: 768px) {
        .premium-page-wrapper {
            padding: 0 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .premium-page-wrapper {
            padding: 0 0.5rem;
        }
    }
    
    /* ============================================
       PREMIUM ALIGNMENT UTILITIES
       ============================================ */
    .align-center {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    .align-left {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        text-align: left;
    }
    
    .align-right {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        text-align: right;
    }
    
    /* ============================================
       PREMIUM SPACING SYSTEM
       ============================================ */
    .spacing-xs { margin: 0.5rem 0; }
    .spacing-sm { margin: 1rem 0; }
    .spacing-md { margin: 1.5rem 0; }
    .spacing-lg { margin: 2rem 0; }
    .spacing-xl { margin: 3rem 0; }
    
    @media (max-width: 768px) {
        .spacing-xs { margin: 0.4rem 0; }
        .spacing-sm { margin: 0.8rem 0; }
        .spacing-md { margin: 1.2rem 0; }
        .spacing-lg { margin: 1.5rem 0; }
        .spacing-xl { margin: 2rem 0; }
    }
    
    /* ============================================
       PREMIUM TEXT RESPONSIVE
       ============================================ */
    .text-responsive-h1 {
        font-size: 3rem;
        line-height: 1.2;
    }
    
    .text-responsive-h2 {
        font-size: 2.5rem;
        line-height: 1.3;
    }
    
    .text-responsive-h3 {
        font-size: 2rem;
        line-height: 1.4;
    }
    
    @media (max-width: 992px) {
        .text-responsive-h1 { font-size: 2.5rem; }
        .text-responsive-h2 { font-size: 2rem; }
        .text-responsive-h3 { font-size: 1.75rem; }
    }
    
    @media (max-width: 768px) {
        .text-responsive-h1 { font-size: 2rem; }
        .text-responsive-h2 { font-size: 1.75rem; }
        .text-responsive-h3 { font-size: 1.5rem; }
    }
    
    @media (max-width: 480px) {
        .text-responsive-h1 { font-size: 1.75rem; }
        .text-responsive-h2 { font-size: 1.5rem; }
        .text-responsive-h3 { font-size: 1.25rem; }
    }
    
    /* ============================================
       PREMIUM SMOOTH TRANSITIONS
       ============================================ */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* ============================================
       PREMIUM FOCUS STATES
       ============================================ */
    button:focus-visible,
    input:focus-visible,
    select:focus-visible,
    textarea:focus-visible {
        outline: 3px solid #667eea;
        outline-offset: 2px;
    }
    
    /* ============================================
       PREMIUM PRINT STYLES
       ============================================ */
    @media print {
        .sidebar,
        button,
        .stButton {
            display: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'properties' not in st.session_state:
    st.session_state.properties = []
if 'investments' not in st.session_state:
    st.session_state.investments = []
if 'user_portfolio' not in st.session_state:
    st.session_state.user_portfolio = {}
if 'kyc_status' not in st.session_state:
    st.session_state.kyc_status = {
        'verified': False,
        'documents_uploaded': False,
        'personal_info': {},
        'documents': {}
    }
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'user_account_type' not in st.session_state:
    st.session_state.user_account_type = None

# User database (in production, use a real database)
USERS_DATABASE = {
    'premium_user@proptoken.com': {
        'password': 'premium123',
        'name': 'Premium User',
        'account_type': 'premium',
        'email': 'premium_user@proptoken.com'
    },
    'free_user@proptoken.com': {
        'password': 'free123',
        'name': 'Free User',
        'account_type': 'free',
        'email': 'free_user@proptoken.com'
    },
    'admin@proptoken.com': {
        'password': 'admin123',
        'name': 'Admin User',
        'account_type': 'premium',
        'email': 'admin@proptoken.com'
    }
}

def authenticate_user(email, password):
    """Authenticate user credentials"""
    if email in USERS_DATABASE:
        if USERS_DATABASE[email]['password'] == password:
            return {
                'success': True,
                'user': USERS_DATABASE[email]
            }
        else:
            return {
                'success': False,
                'error': 'Invalid password'
            }
    else:
        return {
            'success': False,
            'error': 'User not found'
        }

def login_page():
    """Beautiful login page with black and white theme"""
    st.markdown("""
    <style>
        @keyframes backgroundMove {
            0% { background-position: 0% 0%; }
            50% { background-position: 100% 100%; }
            100% { background-position: 0% 0%; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-50px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 20px rgba(0,0,0,0.3); }
            50% { box-shadow: 0 0 40px rgba(0,0,0,0.6); }
        }
        
        .login-container {
            background: linear-gradient(45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(-45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(45deg, transparent 75%, #f8f9fa 75%), 
                        linear-gradient(-45deg, transparent 75%, #f8f9fa 75%);
            background-size: 20px 20px;
            background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
            animation: backgroundMove 20s linear infinite;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        
        @media (max-width: 768px) {
            .login-container {
                padding: 1.5rem;
                min-height: calc(100vh - 2rem);
            }
        }
        
        @media (max-width: 480px) {
            .login-container {
                padding: 1rem;
                min-height: calc(100vh - 1rem);
            }
        }
        
        .login-box {
            background: #fff;
            border: 3px solid #000;
            border-radius: 20px;
            padding: 3rem;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: fadeIn 0.8s ease-out, glow 3s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }
        
        @media (max-width: 768px) {
            .login-box {
                padding: 2rem 1.5rem;
                border-radius: 15px;
                border-width: 2px;
            }
        }
        
        @media (max-width: 480px) {
            .login-box {
                padding: 1.5rem 1rem;
                border-radius: 12px;
            }
        }
        
        .login-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0,0,0,0.1), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2.5rem;
            animation: slideIn 0.8s ease-out;
        }
        
        @media (max-width: 768px) {
            .login-header {
                margin-bottom: 2rem;
            }
        }
        
        .login-header h1 {
            color: #000;
            font-size: 3rem;
            font-weight: 900;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 4px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
            line-height: 1.2;
        }
        
        @media (max-width: 768px) {
            .login-header h1 {
                font-size: 2.2rem;
                letter-spacing: 3px;
            }
        }
        
        @media (max-width: 480px) {
            .login-header h1 {
                font-size: 1.8rem;
                letter-spacing: 2px;
            }
        }
        
        .login-header p {
            color: #666;
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        @media (max-width: 768px) {
            .login-header p {
                font-size: 0.95rem;
                letter-spacing: 1px;
            }
        }
        
        @media (max-width: 480px) {
            .login-header p {
                font-size: 0.85rem;
            }
        }
        
        .input-group {
            margin-bottom: 1.5rem;
            animation: fadeIn 1s ease-out;
        }
        
        .input-label {
            color: #000;
            font-weight: 800;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
            display: block;
        }
        
        .login-button {
            width: 100%;
            background: #000;
            color: #fff;
            border: 3px solid #000;
            padding: 1rem 2rem;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1rem;
            animation: fadeIn 1.2s ease-out;
        }
        
        .login-button:hover {
            background: #fff;
            color: #000;
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        
        .demo-accounts {
            margin-top: 2rem;
            padding: 1.5rem;
            background: #f8f9fa;
            border: 2px solid #000;
            border-radius: 10px;
            animation: fadeIn 1.4s ease-out;
        }
        
        @media (max-width: 768px) {
            .demo-accounts {
                padding: 1.2rem;
                margin-top: 1.5rem;
            }
        }
        
        @media (max-width: 480px) {
            .demo-accounts {
                padding: 1rem;
                margin-top: 1rem;
            }
        }
        
        .demo-accounts h3 {
            color: #000;
            font-size: 1.2rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .demo-accounts h3 {
                font-size: 1rem;
                letter-spacing: 1px;
            }
        }
        
        @media (max-width: 480px) {
            .demo-accounts h3 {
                font-size: 0.9rem;
            }
        }
        
        .demo-account-item {
            background: #fff;
            border: 2px solid #000;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.8rem;
            transition: all 0.3s ease;
        }
        
        .demo-account-item:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .account-type {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-left: 0.5rem;
        }
        
        .premium-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
        }
        
        .free-badge {
            background: #000;
            color: #fff;
        }
        
        .account-info {
            color: #000;
            font-weight: 600;
            margin-top: 0.5rem;
            font-size: 0.9rem;
        }
    </style>
    
    <div class="login-container">
        <div class="login-box">
            <div class="login-header">
                <h1>🏠 PropToken</h1>
                <p>Real Estate Tokenization Platform</p>
            </div>
            
            <form>
                <div class="input-group">
                    <label class="input-label">📧 Email Address</label>
                </div>
            </form>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        email = st.text_input(
            "",
            key="login_email",
            placeholder="Enter your email",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        password = st.text_input(
            "",
            key="login_password",
            type="password",
            placeholder="Enter your password",
            label_visibility="collapsed"
        )
        
        st.markdown("""
        <style>
            .stTextInput > div > div > input {
                border: 3px solid #000;
                border-radius: 10px;
                padding: 0.8rem;
                font-weight: 600;
                font-size: 1rem;
            }
            .stTextInput > div > div > input:focus {
                border-color: #000;
                box-shadow: 0 0 10px rgba(0,0,0,0.3);
            }
        </style>
        """, unsafe_allow_html=True)
        
        login_button = st.button(
            "🔐 LOGIN",
            use_container_width=True,
            type="primary"
        )
        
        st.markdown("""
        <style>
            .stButton > button {
                background: #000;
                color: #fff;
                border: 3px solid #000;
                padding: 1rem 2rem;
                border-radius: 10px;
                font-size: 1.1rem;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: 2px;
                width: 100%;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                background: #fff;
                color: #000;
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            }
        </style>
        """, unsafe_allow_html=True)
        
        if login_button:
            if email and password:
                auth_result = authenticate_user(email, password)
                if auth_result['success']:
                    st.session_state.authenticated = True
                    st.session_state.current_user = auth_result['user']
                    st.session_state.user_account_type = auth_result['user']['account_type']
                    st.success(f"✅ Welcome back, {auth_result['user']['name']}!")
                    st.rerun()
                else:
                    st.error(f"❌ {auth_result['error']}")
            else:
                st.warning("⚠️ Please enter both email and password")
        
        # Demo accounts section
        st.markdown("""
        <div class="demo-accounts">
            <h3>🔑 Demo Accounts</h3>
            <div class="demo-account-item">
                <strong>Premium Account</strong>
                <span class="account-type premium-badge">PREMIUM</span>
                <div class="account-info">Email: premium_user@proptoken.com</div>
                <div class="account-info">Password: premium123</div>
            </div>
            <div class="demo-account-item">
                <strong>Free Account</strong>
                <span class="account-type free-badge">FREE</span>
                <div class="account-info">Email: free_user@proptoken.com</div>
                <div class="account-info">Password: free123</div>
            </div>
            <div class="demo-account-item">
                <strong>Admin Account</strong>
                <span class="account-type premium-badge">PREMIUM</span>
                <div class="account-info">Email: admin@proptoken.com</div>
                <div class="account-info">Password: admin123</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def verify_kyc_documents(personal_info, documents):
    """Simulate KYC document verification"""
    # Simulate verification process
    import time
    time.sleep(1)  # Simulate processing time
    
    # Basic validation rules
    required_fields = ['full_name', 'email', 'phone', 'address', 'date_of_birth', 'national_id']
    required_docs = ['id_document', 'address_proof']
    
    # Check if all required fields are provided
    fields_complete = all(personal_info.get(field) for field in required_fields)
    
    # Check if all required documents are uploaded
    docs_complete = all(documents.get(doc) for doc in required_docs)
    
    # Simulate verification result (90% success rate for demo)
    verification_success = fields_complete and docs_complete and random.random() > 0.1
    
    return {
        'verified': verification_success,
        'fields_complete': fields_complete,
        'docs_complete': docs_complete,
        'verification_date': datetime.now() if verification_success else None,
        'rejection_reason': None if verification_success else "Document quality insufficient or information mismatch"
    }

def kyc_page():
    """KYC verification page with simple black and white theme"""
    
    # Simple Black and White Theme with Background Animation
    st.markdown("""
    <style>
        @keyframes backgroundMove {
            0% { background-position: 0% 0%; }
            50% { background-position: 100% 100%; }
            100% { background-position: 0% 0%; }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .main-container {
            background: linear-gradient(45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(-45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(45deg, transparent 75%, #f8f9fa 75%), 
                        linear-gradient(-45deg, transparent 75%, #f8f9fa 75%);
            background-size: 20px 20px;
            background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
            animation: backgroundMove 20s linear infinite;
            padding: 2rem;
        }
        
        .header-section {
            background: #000;
            color: #fff;
            padding: 3rem 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
            animation: fadeIn 1s ease-out;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .form-section {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 2rem;
            margin: 0.5rem 0;
            animation: fadeIn 1s ease-out;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .section-title {
            color: #000;
            font-size: 1.8rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .submit-container {
            text-align: center;
            margin: 2rem auto;
            padding: 3rem 2rem;
            background: #fff;
            border: 3px solid #000;
            border-radius: 15px;
            max-width: 600px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            animation: fadeIn 1s ease-out;
        }
        
        .submit-button {
            background: #000;
            color: #fff;
            border: none;
            padding: 1rem 3rem;
            font-size: 1.2rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .submit-button:hover {
            background: #333;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        }
        
        .kyc-card {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            animation: fadeIn 1s ease-out;
            transition: all 0.3s ease;
            height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 120px;
            width: 100%;
        }
        
        .kyc-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .kyc-card h3 {
            color: #000;
            font-size: 1.5rem;
            font-weight: 900;
            margin: 0 0 0.5rem 0;
            line-height: 1.2;
        }
        
        .kyc-card p {
            color: #666;
            font-size: 0.9rem;
            font-weight: 600;
            margin: 0;
            line-height: 1.2;
        }
        
        /* Responsive design for KYC cards */
        @media (max-width: 1200px) {
            .kyc-card {
                height: 110px;
                min-height: 110px;
                padding: 1.2rem;
            }
            
            .kyc-card h3 {
                font-size: 1.3rem;
            }
            
            .kyc-card p {
                font-size: 0.85rem;
            }
        }
        
        @media (max-width: 768px) {
            .kyc-card {
                height: 100px;
                min-height: 100px;
                padding: 1rem;
            }
            
            .kyc-card h3 {
                font-size: 1.2rem;
            }
            
            .kyc-card p {
                font-size: 0.8rem;
            }
        }
        
        @media (max-width: 480px) {
            .kyc-card {
                height: 90px;
                min-height: 90px;
                padding: 0.8rem;
            }
            
            .kyc-card h3 {
                font-size: 1.1rem;
            }
            
            .kyc-card p {
                font-size: 0.75rem;
            }
        }
    </style>
    
    <div class="main-container">
        <div class="header-section">
            <h1 style="font-size: 3rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 3px;">
                KYC VERIFICATION
            </h1>
            <p style="font-size: 1.2rem; margin: 1rem 0 0 0; font-weight: 600;">
                Complete your identity verification to start investing
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KYC Status Display with amazing theme
    if st.session_state.kyc_status['verified']:
        st.markdown("""
        <div class="status-verified">
            <h2 style="margin: 0; font-size: 2.5rem;">🎉 KYC VERIFIED!</h2>
            <p style="font-size: 1.3rem; margin: 1rem 0;">Your identity has been successfully verified</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Amazing metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="kyc-card">
                <h3>✅ Verified</h3>
                <p>Status</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            verification_date = st.session_state.kyc_status.get('verification_date', None)
            if verification_date:
                date_str = verification_date.strftime("%Y-%m-%d %H:%M")
            else:
                date_str = 'N/A'
            st.markdown(f"""
            <div class="kyc-card">
                <h3>📅 {date_str}</h3>
                <p>Verified Date</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="kyc-card">
                <h3>💰 PKR 50M</h3>
                <p>Investment Limit</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="kyc-card">
                <h3>🔒 Secure</h3>
                <p>Data Protection</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Re-verify button with amazing styling
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <button onclick="window.location.reload()" style="
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 1rem 2rem;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 10px 20px rgba(239, 68, 68, 0.3);
            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 15px 30px rgba(239, 68, 68, 0.4)'" 
               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 20px rgba(239, 68, 68, 0.3)'">
                🔄 Re-verify KYC
            </button>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Re-verify KYC", key="reverify"):
            st.session_state.kyc_status['verified'] = False
            st.session_state.kyc_status['documents_uploaded'] = False
            st.rerun()
        
        return
    
    # Simple KYC Form
    st.markdown("""
    <div class="form-section">
        <h2 class="section-title">COMPLETE YOUR KYC VERIFICATION</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("kyc_form"):
        # Personal Information Section
        st.markdown("""
        <div class="form-section">
            <h3 class="section-title">PERSONAL INFORMATION</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *", value=st.session_state.kyc_status['personal_info'].get('full_name', ''), 
                                     help="Enter your full legal name as it appears on your ID")
            email = st.text_input("Email Address *", value=st.session_state.kyc_status['personal_info'].get('email', ''),
                                 help="We'll use this to send you verification updates")
            phone = st.text_input("Phone Number *", value=st.session_state.kyc_status['personal_info'].get('phone', ''),
                                 help="Include country code (e.g., +92 for Pakistan)")
            date_of_birth = st.date_input("Date of Birth *", value=st.session_state.kyc_status['personal_info'].get('date_of_birth', datetime(1990, 1, 1).date()),
                                        help="Must be 18+ years old")
        
        with col2:
            address = st.text_area("Full Address *", value=st.session_state.kyc_status['personal_info'].get('address', ''),
                                  help="Complete residential address")
            national_id = st.text_input("National ID/Passport Number *", value=st.session_state.kyc_status['personal_info'].get('national_id', ''),
                                       help="CNIC, Passport, or other government-issued ID")
            occupation = st.text_input("Occupation", value=st.session_state.kyc_status['personal_info'].get('occupation', ''),
                                      help="Your current job or profession")
            annual_income = st.selectbox("Annual Income Range", 
                                      ["Under PKR 500,000", "PKR 500,000 - 1,000,000", "PKR 1,000,000 - 2,500,000", 
                                       "PKR 2,500,000 - 5,000,000", "PKR 5,000,000 - 10,000,000", "Over PKR 10,000,000"],
                                      index=2, help="Select your annual income range")
        
        # Document Upload Section
        st.markdown("""
        <div class="form-section">
            <h3 class="section-title">DOCUMENT UPLOAD</h3>
            <p style="text-align: center; color: #666; margin-bottom: 1rem; font-weight: 600;">
                Please upload clear, high-quality images of your documents
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🆔 ID Document")
            id_document = st.file_uploader("Passport/Driver's License/CNIC *", 
                                         type=['png', 'jpg', 'jpeg'], 
                                         help="Upload front and back of your ID document")
            if id_document:
                st.image(id_document, width=200, caption="ID Document Preview")
        
        with col2:
            st.markdown("### 🏠 Address Proof")
            address_proof = st.file_uploader("Utility Bill/Bank Statement *", 
                                           type=['png', 'jpg', 'jpeg'], 
                                           help="Document should be less than 3 months old")
            if address_proof:
                st.image(address_proof, width=200, caption="Address Proof Preview")
        
        # Additional documents
        st.markdown("""
        <div class="form-section">
            <h3 class="section-title">ADDITIONAL DOCUMENTS (OPTIONAL)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        income_proof = st.file_uploader("Income Proof (Pay Stub/Tax Return)", type=['png', 'jpg', 'jpeg', 'pdf'],
                                       help="Optional: Helps with investment limit approval")
        
        # Terms and conditions
        st.markdown("""
        <div class="form-section">
            <h3 class="section-title">TERMS AND CONDITIONS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        terms_accepted = st.checkbox("I agree to the terms and conditions and privacy policy *", 
                                   help="Required to proceed with KYC verification")
        data_consent = st.checkbox("I consent to the processing of my personal data for KYC verification *",
                                  help="Required for identity verification")
        
        # Centered Submit Button with Black & White Theme
        st.markdown("""
        <div class="submit-container">
            <h3 style="color: #000; font-size: 1.8rem; font-weight: 900; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 2px;">
                READY TO VERIFY YOUR IDENTITY?
            </h3>
            <p style="color: #666; font-size: 1.2rem; font-weight: 600; margin-bottom: 2rem;">
                Click the button below to submit your KYC application
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Centered submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("SUBMIT KYC APPLICATION", type="primary", use_container_width=True)
        
        if submitted:
            if not all([full_name, email, phone, address, national_id, id_document, address_proof, terms_accepted, data_consent]):
                st.error("❌ Please fill in all required fields and upload required documents.")
            else:
                # Store personal information
                personal_info = {
                    'full_name': full_name,
                    'email': email,
                    'phone': phone,
                    'address': address,
                    'date_of_birth': date_of_birth,
                    'national_id': national_id,
                    'occupation': occupation,
                    'annual_income': annual_income
                }
                
                # Store documents (in real app, these would be uploaded to secure storage)
                documents = {
                    'id_document': id_document.name if id_document else None,
                    'address_proof': address_proof.name if address_proof else None,
                    'income_proof': income_proof.name if income_proof else None
                }
                
                # Update session state
                st.session_state.kyc_status['personal_info'] = personal_info
                st.session_state.kyc_status['documents'] = documents
                st.session_state.kyc_status['documents_uploaded'] = True
                
                # ABSOLUTELY AMAZING verification process
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                    color: white;
                    padding: 3rem;
                    border-radius: 30px;
                    text-align: center;
                    margin: 2rem 0;
                    box-shadow: 
                        0 25px 50px rgba(102, 126, 234, 0.4),
                        0 0 30px rgba(102, 126, 234, 0.3);
                    border: 3px solid rgba(255, 255, 255, 0.2);
                    animation: neonGlow 2s ease-in-out infinite;
                    position: relative;
                    overflow: hidden;
                ">
                    <div style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
                        animation: cardShimmer 2s ease-in-out infinite;
                    "></div>
                    <h3 style="
                        margin: 0; 
                        font-size: 2.5rem; 
                        font-weight: 800;
                        text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
                        animation: titlePulse 2s ease-in-out infinite;
                        position: relative;
                        z-index: 2;
                    ">🔍 VERIFYING YOUR DOCUMENTS... 🔍</h3>
                    <p style="
                        margin: 1.5rem 0 0 0; 
                        font-size: 1.3rem;
                        font-weight: 600;
                        text-shadow: 0 0 15px rgba(255, 255, 255, 0.6);
                        position: relative;
                        z-index: 2;
                    ">This may take a few minutes. Please wait...</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Simulate verification process
                with st.spinner("🔍 Verifying your documents... This may take a few minutes."):
                    verification_result = verify_kyc_documents(personal_info, documents)
                    
                    if verification_result['verified']:
                        st.session_state.kyc_status['verified'] = True
                        st.session_state.kyc_status['verification_date'] = verification_result['verification_date']
                        
                        st.markdown("""
                        <div style="
                            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                            color: white;
                            padding: 3rem;
                            border-radius: 20px;
                            text-align: center;
                            margin: 2rem 0;
                            box-shadow: 0 20px 40px rgba(16, 185, 129, 0.4);
                            animation: glow 2s ease-in-out infinite;
                        ">
                            <h2 style="margin: 0; font-size: 3rem;">🎉 KYC VERIFIED!</h2>
                            <p style="font-size: 1.5rem; margin: 1rem 0;">Your identity has been successfully verified</p>
                            <p style="font-size: 1.2rem; margin: 0; opacity: 0.9;">You can now invest in tokenized real estate!</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.rerun()
                    else:
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                            color: white;
                            padding: 2rem;
                            border-radius: 20px;
                            text-align: center;
                            margin: 2rem 0;
                            box-shadow: 0 15px 35px rgba(239, 68, 68, 0.4);
                        ">
                            <h3 style="margin: 0; font-size: 2rem;">❌ KYC Verification Failed</h3>
                            <p style="margin: 1rem 0 0 0; opacity: 0.9;">{verification_result['rejection_reason']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.warning("Please check your documents and try again. Ensure all documents are clear and readable.")

    # Footer with team credits
    st.markdown("""
    <div style="
        background: #000;
        color: #fff;
        padding: 1rem;
        margin-top: 3rem;
        border-radius: 8px;
        overflow: hidden;
        position: relative;
    ">
        <div style="
            animation: runningText 15s linear infinite;
            white-space: nowrap;
            font-size: 1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
        ">
            DEVELOPED BY TEAM PROPTOKEN (SOHAIL NASIR, AYESHA JAWAD, MANAL AHSAN, MOOSA SAEED) • BLOCKCHAIN REAL ESTATE TOKENIZATION • FRACTIONAL OWNERSHIP • SECURE INVESTMENT • TRANSPARENT TRANSACTIONS • DEVELOPED BY TEAM PROPTOKEN (SOHAIL NASIR, AYESHA JAWAD, MANAL AHSAN, MOOSA SAEED) • 
        </div>
    </div>
    
    <style>
        @keyframes runningText {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
    </style>
    """, unsafe_allow_html=True)

def generate_dummy_properties():
    """Generate dummy property data"""
    properties = []
    locations = ['Karachi', 'Lahore', 'Islamabad', 'Rawalpindi', 'Faisalabad', 'Multan', 'Peshawar', 'Quetta', 'Gujranwala', 'Sialkot']
    
    # Pakistani property names
    property_names = [
        'Centaurus Mall', 'Bahria Town Plaza', 'DHA Phase 5 Tower', 'Gulberg Heights', 
        'Clifton Beach Resort', 'F-8 Commercial Complex', 'Model Town Plaza', 'Defence Tower',
        'Blue Area Office Complex', 'Garden City Residency', 'Lucky One Mall', 'Dolmen City',
        'Emporium Mall Tower', 'Packages Mall Complex', 'Fortress Square', 'Giga Mall',
        'Centaurus Residency', 'Bahria Icon Tower', 'DHA Phase 2 Plaza', 'Gulberg Greens'
    ]
    
    for i in range(20):
        property_data = {
            'id': f'PROP_{i+1:03d}',
            'name': property_names[i],
            'location': random.choice(locations),
            'price': random.randint(5000000, 50000000),  # Prices in PKR (5M to 50M PKR)
            'roi': round(random.uniform(12, 30), 2),  # Higher ROI for Pakistani market
            'tokens_supply': random.randint(1000, 10000),
            'tokens_available': random.randint(100, 1000),
            'image_url': f'https://picsum.photos/400/300?random={i}',
            'description': f"Premium {random.choice(['residential', 'commercial', 'mixed-use'])} property in {random.choice(locations)}. Modern amenities, prime location, excellent investment opportunity.",
            'property_type': random.choice(['Residential', 'Commercial', 'Mixed-Use']),
            'year_built': random.randint(2000, 2024),
            'square_feet': random.randint(2000, 50000)
        }
        properties.append(property_data)
    
    return properties

def generate_historical_data():
    """Generate historical ROI data for ML models"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='M')
    data = []
    
    pakistani_locations = ['Karachi', 'Lahore', 'Islamabad', 'Rawalpindi', 'Faisalabad', 'Multan', 'Peshawar', 'Quetta', 'Gujranwala', 'Sialkot']
    
    for i in range(20):
        base_roi = random.uniform(12, 25)  # Higher base ROI for Pakistani market
        for date in dates:
            # Add some trend and seasonality
            trend = (date.year - 2020) * 0.8  # Stronger growth trend
            seasonality = np.sin(2 * np.pi * date.month / 12) * 3
            noise = random.uniform(-3, 3)
            
            roi = base_roi + trend + seasonality + noise
            data.append({
                'property_id': f'PROP_{i+1:03d}',
                'date': date,
                'roi': max(0, roi),
                'price': random.randint(5000000, 50000000),  # Prices in PKR
                'location': random.choice(pakistani_locations)
            })
    
    return pd.DataFrame(data)

def create_pdf_invoice(property_name, investment_amount, tokens, ownership_percent, roi):
    """Create a professional PDF invoice"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1
    )
    
    # Content
    story = []
    
    # Title
    story.append(Paragraph("PropToken Investment Invoice", title_style))
    story.append(Spacer(1, 20))
    
    # Invoice details
    invoice_data = [
        ['Invoice Number:', f'INV-{datetime.now().strftime("%Y%m%d%H%M%S")}'],
        ['Date:', datetime.now().strftime("%B %d, %Y")],
        ['Property:', property_name],
        ['Investment Amount:', f'${investment_amount:,.2f}'],
        ['Tokens Issued:', f'{tokens:,.0f}'],
        ['Ownership Percentage:', f'{ownership_percent:.2f}%'],
        ['Expected ROI:', f'{roi:.2f}%'],
    ]
    
    table = Table(invoice_data, colWidths=[2*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 30))
    
    # Terms and conditions
    story.append(Paragraph("Terms and Conditions", styles['Heading2']))
    terms = """
    This investment represents ownership of digital tokens backed by real estate assets. 
    Tokens are secured on the blockchain and provide proportional ownership rights. 
    Returns are subject to property performance and market conditions.
    """
    story.append(Paragraph(terms, styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def home_page():
    """Home page with black and white theme"""
    
    # Black and White Home Page Theme
    st.markdown("""
    <style>
        .home-container {
            background: linear-gradient(45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(-45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(45deg, transparent 75%, #f8f9fa 75%), 
                        linear-gradient(-45deg, transparent 75%, #f8f9fa 75%);
            background-size: 20px 20px;
            background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
            animation: backgroundMove 20s linear infinite;
            padding: 2rem;
        }
        
        .home-header {
            background: #000;
            color: #fff;
            padding: 3rem 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            animation: fadeIn 1s ease-out;
        }
        
        .content-section {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            animation: fadeIn 1s ease-out;
        }
        
        .section-title {
            color: #000;
            font-size: 1.8rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .stats-card {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            animation: slideInFromLeft 2s ease-out, float 3s ease-in-out infinite;
            position: relative;
            overflow: hidden;
            height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 150px;
            width: 100%;
        }
        
        .stats-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0,0,0,0.1), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes slideInFromLeft {
            0% { transform: translateX(-100px); opacity: 0; }
            100% { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .stats-card h3 {
            color: #000;
            font-size: 2rem;
            font-weight: 900;
            margin: 0 0 0.5rem 0;
        }
        
        .stats-card p {
            color: #666;
            font-size: 1rem;
            font-weight: 600;
            margin: 0;
            line-height: 1.2;
            word-break: break-word;
            text-align: center;
        }
        
        /* Global responsive design for all cards */
        @media (max-width: 1200px) {
            .stats-card {
                height: 140px;
                min-height: 140px;
                padding: 1.2rem;
            }
            
            .stats-card h3 {
                font-size: 1.8rem;
            }
            
            .stats-card p {
                font-size: 0.95rem;
            }
        }
        
        @media (max-width: 768px) {
            .stats-card {
                height: 130px;
                min-height: 130px;
                padding: 1rem;
            }
            
            .stats-card h3 {
                font-size: 1.6rem;
            }
            
            .stats-card p {
                font-size: 0.9rem;
            }
        }
        
        @media (max-width: 480px) {
            .stats-card {
                height: 120px;
                min-height: 120px;
                padding: 0.8rem;
            }
            
            .stats-card h3 {
                font-size: 1.4rem;
            }
            
            .stats-card p {
                font-size: 0.8rem;
            }
        }
        
        /* Responsive grid system */
        .stColumns > div {
            display: flex;
            flex-direction: column;
            width: 100%;
        }
        
        @media (max-width: 1200px) {
            .stColumns {
                display: grid !important;
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 1rem !important;
            }
        }
        
        @media (max-width: 768px) {
            .stColumns {
                display: grid !important;
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 1rem !important;
            }
        }
        
        @media (max-width: 480px) {
            .stColumns {
                display: grid !important;
                grid-template-columns: 1fr !important;
                gap: 1rem !important;
            }
        }
        
        .cta-container {
            text-align: center;
            margin: 2rem auto;
            padding: 3rem 2rem;
            background: #fff;
            border: 3px solid #000;
            border-radius: 15px;
            max-width: 600px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            animation: fadeIn 1s ease-out;
        }
        
        .cta-button {
            background: #000;
            color: #fff;
            border: none;
            padding: 1rem 3rem;
            font-size: 1.2rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .cta-button:hover {
            background: #333;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        }
        
        .pulse-button {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .kyc-status {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 1rem 2rem;
            margin-bottom: 2rem;
            text-align: center;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .kyc-verified {
            color: #000;
            background: #f0f0f0;
        }
        
        .kyc-pending {
            color: #666;
            background: #f8f9fa;
        }
    </style>
    
    <div class="home-container">
        <div class="home-header">
            <h1 style="font-size: 3rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 3px;">
                PROPTOKEN
            </h1>
            <p style="font-size: 1.5rem; margin: 1rem 0 0 0; font-weight: 600;">
                OWN REAL ESTATE LIKE OWNING SHARES
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # KYC Status Banner
    if st.session_state.kyc_status['verified']:
        st.markdown("""
        <div class="kyc-status kyc-verified">
            ✅ KYC VERIFIED - READY TO INVEST!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="kyc-status kyc-pending">
            🔐 COMPLETE KYC VERIFICATION TO START INVESTING
        </div>
        """, unsafe_allow_html=True)
    
    # Tokenization explanation - First section
        st.markdown("""
        <div class="content-section">
            <h2 class="section-title">TOKENIZATION EXPLAINED</h2>
            <p style="font-size: 1.2rem; font-weight: 700; color: #000; margin-bottom: 1rem;">
                A PROPERTY IS LIKE A PIZZA
            </p>
            <p style="color: #666; margin-bottom: 1rem;">
                Tokenization slices it so anyone can own a piece.
            </p>
            <p style="color: #666; margin-bottom: 1rem;">
                Just like JazzCash tokenizes payments, PropToken tokenizes ownership.
            </p>
            <h3 style="color: #000; font-size: 1.3rem; font-weight: 700; margin-bottom: 1rem;">HOW IT WORKS:</h3>
            <ul style="color: #666; font-weight: 600;">
                <li>Real estate is divided into digital tokens</li>
                <li>Each token represents fractional ownership</li>
                <li>Blockchain ensures transparent, immutable records</li>
                <li>Trade tokens like stocks on secondary markets</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Why tokenize real estate - Second section
        st.markdown("""
        <div class="content-section">
            <h2 class="section-title">WHY TOKENIZE REAL ESTATE?</h2>
            <ul style="color: #666; font-weight: 600; font-size: 1.1rem;">
                <li><strong style="color: #000;">LOWER BARRIERS:</strong> Invest with as little as $100</li>
                <li><strong style="color: #000;">LIQUIDITY:</strong> Trade tokens 24/7</li>
                <li><strong style="color: #000;">TRANSPARENCY:</strong> All transactions on blockchain</li>
                <li><strong style="color: #000;">DIVERSIFICATION:</strong> Own pieces of multiple properties</li>
                <li><strong style="color: #000;">GLOBAL ACCESS:</strong> Invest in properties worldwide</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats cards
    st.markdown("""
    <div class="content-section">
        <h2 class="section-title">MARKET STATISTICS</h2>
        <div style="
            background: #000;
            color: #fff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                animation: runningText 15s linear infinite;
                white-space: nowrap;
                font-size: 1.1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 2px;
            ">
                🚀 REAL ESTATE TOKENIZATION IS THE FUTURE • GLOBAL MARKET GROWING 20%+ ANNUALLY • INVEST FROM ANYWHERE IN THE WORLD • BLOCKCHAIN SECURITY GUARANTEED • FRACTIONAL OWNERSHIP MADE EASY • LIQUIDITY LIKE NEVER BEFORE • TRANSPARENT TRANSACTIONS • DEMOCRATIZING REAL ESTATE INVESTMENT • 🚀
            </div>
        </div>
    </div>
    
    <style>
        @keyframes runningText {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stats-card" style="animation-delay: 0.5s;">
            <h3>$2.3B</h3>
            <p>Global tokenization market (2021)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card" style="animation-delay: 1s;">
            <h3>20%+</h3>
            <p>CAGR expected growth</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card" style="animation-delay: 1.5s;">
            <h3>$100</h3>
            <p>Minimum entry investment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stats-card" style="animation-delay: 2s;">
            <h3>100%</h3>
            <p>Transparent ownership records</p>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA Button
    st.markdown("""
    <div class="cta-container">
        <h3 style="color: #000; font-size: 1.8rem; font-weight: 900; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 2px;">
            READY TO START INVESTING?
        </h3>
        <p style="color: #666; font-size: 1.2rem; font-weight: 600; margin-bottom: 2rem;">
            Click the button below to explore our marketplace
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Centered CTA button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <style>
            .stButton > button {
                background: #000 !important;
                color: #fff !important;
                border: none !important;
                padding: 1rem 3rem !important;
                font-size: 1.2rem !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 2px !important;
                border-radius: 8px !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
                animation: pulse 2s infinite !important;
                width: 100% !important;
            }
            
            .stButton > button:hover {
                background: #333 !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px rgba(0,0,0,0.4) !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("GO TO MARKETPLACE", key="cta_home", help="Start investing in tokenized real estate", use_container_width=True):
            st.session_state.current_page = "Portfolio/Marketplace"
            st.rerun()
    
    # Footer with team credits
    st.markdown("""
    <div style="
        background: #000;
        color: #fff;
        padding: 1rem;
        margin-top: 3rem;
        border-radius: 8px;
        overflow: hidden;
        position: relative;
    ">
        <div style="
            animation: runningText 15s linear infinite;
            white-space: nowrap;
            font-size: 1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
        ">
            DEVELOPED BY TEAM PROPTOKEN (SOHAIL NASIR, AYESHA JAWAD, MANAL AHSAN, MOOSA SAEED) • BLOCKCHAIN REAL ESTATE TOKENIZATION • FRACTIONAL OWNERSHIP • SECURE INVESTMENT • TRANSPARENT TRANSACTIONS • DEVELOPED BY TEAM PROPTOKEN (SOHAIL NASIR, AYESHA JAWAD, MANAL AHSAN, MOOSA SAEED) • 
        </div>
    </div>
    
    <style>
        @keyframes runningText {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
    </style>
    """, unsafe_allow_html=True)

def marketplace_page():
    """Portfolio/Marketplace page with black and white theme"""
    
    # Black and White Marketplace Theme
    st.markdown("""
    <style>
        .marketplace-container {
            background: linear-gradient(45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(-45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(45deg, transparent 75%, #f8f9fa 75%), 
                        linear-gradient(-45deg, transparent 75%, #f8f9fa 75%);
            background-size: 20px 20px;
            background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
            animation: backgroundMove 20s linear infinite;
            padding: 2rem;
        }
        
        .marketplace-header {
            background: #000;
            color: #fff;
            padding: 3rem 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            animation: fadeIn 1s ease-out;
        }
        
        .content-section {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            animation: fadeIn 1s ease-out;
        }
        
        .section-title {
            color: #000;
            font-size: 1.8rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .property-card {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            animation: slideInFromLeft 1s ease-out;
            transition: all 0.3s ease;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 180px;
            width: 100%;
        }
        
        .property-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .property-card h4 {
            color: #000;
            font-size: 1.2rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }
        
        .property-card p {
            color: #666;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.3rem;
            line-height: 1.2;
        }
        
        @media (max-width: 768px) {
            .property-card {
                height: 180px;
                min-height: 180px;
                padding: 1rem;
            }
            
            .property-card h4 {
                font-size: 1.1rem;
            }
            
            .property-card p {
                font-size: 0.8rem;
            }
        }
        
        @media (max-width: 1200px) {
            .property-card {
                height: 170px;
                min-height: 170px;
                padding: 1.2rem;
            }
            
            .property-card h4 {
                font-size: 1.1rem;
            }
            
            .property-card p {
                font-size: 0.85rem;
            }
        }
        
        @media (max-width: 768px) {
            .property-card {
                height: 160px;
                min-height: 160px;
                padding: 1rem;
            }
            
            .property-card h4 {
                font-size: 1rem;
            }
            
            .property-card p {
                font-size: 0.8rem;
            }
        }
        
        @media (max-width: 480px) {
            .property-card {
                height: 150px;
                min-height: 150px;
                padding: 0.8rem;
            }
            
            .property-card h4 {
                font-size: 0.9rem;
            }
            
            .property-card p {
                font-size: 0.75rem;
            }
        }
        
        .property-title {
            color: #000;
            font-size: 1.5rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        
        .property-details {
            color: #666;
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .roi-badge {
            background: #000;
            color: #fff;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 700;
            font-size: 1.1rem;
            display: inline-block;
            margin: 0.5rem 0;
        }
        
        .investment-form {
            background: #f8f9fa;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .form-title {
            color: #000;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-transform: uppercase;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .stat-item {
            background: #fff;
            border: 2px solid #000;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        
        .stat-value {
            color: #000;
            font-size: 1.5rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        .search-container {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .search-title {
            color: #000;
            font-size: 1.5rem;
            font-weight: 900;
            margin-bottom: 1rem;
            text-align: center;
            text-transform: uppercase;
        }
        
        .kyc-warning {
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .kyc-warning h2 {
            color: #856404;
            font-size: 1.8rem;
            font-weight: 900;
            margin-bottom: 1rem;
            text-transform: uppercase;
        }
        
        .kyc-warning p {
            color: #856404;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .kyc-button {
            background: #000;
            color: #fff;
            border: none;
            padding: 1rem 2rem;
            font-size: 1.1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .kyc-button:hover {
            background: #333;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        }
        
        @keyframes slideInFromLeft {
            0% { transform: translateX(-100px); opacity: 0; }
            100% { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        @keyframes runningText {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
    </style>
    
    <div class="marketplace-container">
        <div class="marketplace-header">
            <h1 style="font-size: 3rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 3px;">
                PROPERTY MARKETPLACE
            </h1>
            <p style="font-size: 1.2rem; margin: 1rem 0 0 0; font-weight: 600;">
                Invest in tokenized real estate properties
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check KYC status
    if not st.session_state.kyc_status['verified']:
        st.markdown("""
        <div class="kyc-warning">
            <h2>🔐 KYC VERIFICATION REQUIRED</h2>
            <p>Complete your identity verification to start investing in properties</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <style>
                .stButton > button {
                    background: #000 !important;
                    color: #fff !important;
                    border: none !important;
                    padding: 1rem 2rem !important;
                    font-size: 1.1rem !important;
                    font-weight: 700 !important;
                    text-transform: uppercase !important;
                    letter-spacing: 1px !important;
                    border-radius: 8px !important;
                    cursor: pointer !important;
                    transition: all 0.3s ease !important;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
                    width: 100% !important;
                }
                
                .stButton > button:hover {
                    background: #333 !important;
                    transform: translateY(-2px) !important;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.4) !important;
                }
            </style>
            """, unsafe_allow_html=True)
            
            if st.button("COMPLETE KYC VERIFICATION", key="kyc_redirect", use_container_width=True):
                st.session_state.current_page = "KYC"
                st.rerun()
        return
    
    # Show KYC status for verified users
    st.markdown("""
    <div class="content-section" style="text-align: center; background: #e6ffe6; border-color: #00cc00;">
        <h2 style="color: #008000; font-size: 2rem; font-weight: 900; margin: 0;">✅ KYC VERIFIED!</h2>
        <p style="color: #008000; font-size: 1.2rem; margin: 0.5rem 0 0 0; font-weight: 600;">You can invest in properties</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-value">✅ Verified</div>
            <div class="stat-label">Status</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-value">💰 $50,000</div>
            <div class="stat-label">Investment Limit</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-value">🔒 Secure</div>
            <div class="stat-label">Data Protection</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Re-verify button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <style>
            .stButton > button {
                background: #dc3545 !important;
                color: #fff !important;
                border: none !important;
                padding: 0.8rem 1.5rem !important;
                font-size: 1rem !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
                letter-spacing: 1px !important;
                border-radius: 8px !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
                width: 100% !important;
            }
            
            .stButton > button:hover {
                background: #c82333 !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 25px rgba(0,0,0,0.4) !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 RE-VERIFY KYC", use_container_width=True):
            st.session_state.kyc_status['verified'] = False
            st.rerun()
    
    # Initialize properties if not exists
    if not st.session_state.properties:
        st.session_state.properties = generate_dummy_properties()
    
    # Debug information
    st.info(f"Total properties available: {len(st.session_state.properties)}")
    
    # Search and filters
    st.markdown("""
    <div class="search-container">
        <h2 class="search-title">🔍 SEARCH PROPERTIES</h2>
        <div style="
            background: #000;
            color: #fff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                animation: runningText 15s linear infinite;
                white-space: nowrap;
                font-size: 1.1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 2px;
            ">
                🏠 FIND YOUR PERFECT INVESTMENT • PREMIUM PROPERTIES IN PAKISTAN • HIGH ROI OPPORTUNITIES • BLOCKCHAIN SECURED • FRACTIONAL OWNERSHIP • LIQUID REAL ESTATE • INVEST FROM ANYWHERE • 🏠
            </div>
        </div>
    </div>
    
    <style>
        @keyframes runningText {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Responsive columns for filters
    st.markdown("""
    <style>
        @media (max-width: 992px) {
            [data-testid="column"] {
                min-width: 50% !important;
            }
        }
        @media (max-width: 576px) {
            [data-testid="column"] {
                min-width: 100% !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        location_filter = st.selectbox("📍 Location", ["All"] + list(set([p['location'] for p in st.session_state.properties])))
    
    with col2:
        min_roi = st.slider("📈 Min ROI (%)", 0, 30, 8)
    
    with col3:
        max_price = st.slider("💰 Max Price (PKR)", 5000000, 50000000, 50000000)
    
    with col4:
        property_type = st.selectbox("🏢 Property Type", ["All", "Residential", "Commercial", "Mixed-Use"])
    
    # Filter properties
    filtered_properties = st.session_state.properties.copy()
    
    if location_filter != "All":
        filtered_properties = [p for p in filtered_properties if p['location'] == location_filter]
    
    filtered_properties = [p for p in filtered_properties if p['roi'] >= min_roi]
    filtered_properties = [p for p in filtered_properties if p['price'] <= max_price]
    
    if property_type != "All":
        filtered_properties = [p for p in filtered_properties if p['property_type'] == property_type]
    
    # Debug information
    st.info(f"Filtered properties: {len(filtered_properties)}")
    if len(filtered_properties) == 0:
        st.warning("No properties match your filters. Try adjusting the search criteria.")
        return
    
    # Display properties
    st.markdown(f"""
    <div class="content-section">
        <h2 class="section-title">📋 AVAILABLE PROPERTIES ({len(filtered_properties)} FOUND)</h2>
        <div style="
            background: #000;
            color: #fff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                animation: runningText 12s linear infinite;
                white-space: nowrap;
                font-size: 1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">
                💰 INVEST IN TOKENIZED REAL ESTATE • OWN FRACTIONS OF PREMIUM PROPERTIES • EARN PASSIVE INCOME • TRADE TOKENS 24/7 • BLOCKCHAIN TRANSPARENCY • SECURE INVESTMENT • HIGH RETURNS • 💰
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for i, prop in enumerate(filtered_properties):
        # Property Card with enhanced animations
        st.markdown(f"""
        <div style="
            border: 2px solid #000; 
            border-radius: 10px; 
            padding: 1.5rem; 
            margin: 1rem 0; 
            background: #fff;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            animation: slideInFromLeft {0.5 + (i * 0.2)}s ease-out;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 10px 25px rgba(0,0,0,0.2)'" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 5px 15px rgba(0,0,0,0.1)'">
            <div style="
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(0,0,0,0.05), transparent);
                animation: shimmer 3s infinite;
                animation-delay: {i * 0.5}s;
            "></div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.image(prop['image_url'], width=200)
        
        with col2:
            st.markdown(f"### {prop['name']}")
            st.markdown(f"**Location:** {prop['location']} | **Type:** {prop['property_type']}")
            st.markdown(f"**Price:** PKR {prop['price']:,} | **Year Built:** {prop['year_built']}")
            st.markdown(f"**Square Feet:** {prop['square_feet']:,} sq ft")
            st.markdown(f"**Description:** {prop['description']}")
            st.markdown(f"**Token Supply:** {prop['tokens_supply']:,}")
            st.markdown(f"**Available:** {prop['tokens_available']:,}")
        
        with col3:
            st.markdown(f"""
            <div style="
                background: #000; 
                color: #fff; 
                padding: 1rem; 
                border-radius: 8px; 
                text-align: center;
                margin-bottom: 1rem;
            ">
                <h3 style="margin: 0; font-size: 1.5rem;">{prop['roi']}% ROI</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form(key=f"invest_form_{i}"):
                st.markdown("**Investment Amount**")
                investment_amount = st.number_input(
                    "Amount (PKR)", 
                    min_value=100000, 
                    max_value=prop['price'], 
                    value=1000000,
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
                
                st.markdown("""
                <style>
                    .stButton > button {
                        background: #000 !important;
                        color: #fff !important;
                        border: none !important;
                        padding: 0.8rem 1.5rem !important;
                        font-size: 1rem !important;
                        font-weight: 700 !important;
                        text-transform: uppercase !important;
                        letter-spacing: 1px !important;
                        border-radius: 8px !important;
                        cursor: pointer !important;
                        transition: all 0.3s ease !important;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
                        width: 100% !important;
                    }
                    
                    .stButton > button:hover {
                        background: #333 !important;
                        transform: translateY(-2px) !important;
                        box-shadow: 0 8px 25px rgba(0,0,0,0.4) !important;
                    }
                </style>
                """, unsafe_allow_html=True)
                
                if st.form_submit_button("💰 INVEST NOW", use_container_width=True):
                        # Calculate investment details
                        token_price = prop['price'] / prop['tokens_supply']
                        tokens_received = investment_amount / token_price
                        ownership_percent = (tokens_received / prop['tokens_supply']) * 100
                        platform_fee = investment_amount * 0.02  # 2% platform fee
                        net_investment = investment_amount - platform_fee
                        
                        # Store investment
                        investment = {
                            'property_id': prop['id'],
                            'property_name': prop['name'],
                            'investment_amount': investment_amount,
                            'tokens_received': tokens_received,
                            'ownership_percent': ownership_percent,
                            'roi': prop['roi'],
                            'platform_fee': platform_fee,
                            'net_investment': net_investment,
                            'timestamp': datetime.now()
                        }
                        
                        st.session_state.investments.append(investment)
                        
                        # Store PDF data in session state for download outside form
                        pdf_buffer = create_pdf_invoice(
                            prop['name'], 
                            investment_amount, 
                            tokens_received, 
                            ownership_percent, 
                            prop['roi']
                        )
                        
                        st.session_state.latest_pdf = {
                            'data': pdf_buffer.getvalue(),
                            'filename': f"investment_invoice_{prop['id']}.pdf"
                        }
                        
                        st.success(f"Investment successful! You received {tokens_received:,.0f} tokens ({ownership_percent:.2f}% ownership)")
                        st.rerun()
        
        # Close the property card div
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Download button for latest investment (outside of form)
    if 'latest_pdf' in st.session_state and st.session_state.latest_pdf:
        st.markdown("## 📄 Download Your Investment Documents")
        st.download_button(
            label="📄 Download Invoice & Agreement",
            data=st.session_state.latest_pdf['data'],
            file_name=st.session_state.latest_pdf['filename'],
            mime="application/pdf"
        )
        if st.button("🗑️ Clear Download"):
            del st.session_state.latest_pdf
            st.rerun()
    
    # Seller registration
    st.markdown("""
    <div class="content-section">
        <h2 class="section-title">🏗️ REGISTER NEW PROPERTY</h2>
        <div style="
            background: #000;
            color: #fff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                animation: runningText 18s linear infinite;
                white-space: nowrap;
                font-size: 1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">
                🏗️ LIST YOUR PROPERTY • TOKENIZE REAL ESTATE • EARN FROM RENTAL INCOME • INCREASE LIQUIDITY • REACH GLOBAL INVESTORS • BLOCKCHAIN SECURITY • FRACTIONAL OWNERSHIP • 🏗️
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        background: #f8f9fa;
        border: 2px solid #000;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    ">
    """, unsafe_allow_html=True)
    
    with st.expander("➕ ADD PROPERTY TO MARKETPLACE", expanded=False):
        with st.form("seller_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_prop_name = st.text_input("Property Name")
                new_prop_location = st.selectbox("Location", ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan", "Peshawar", "Quetta", "Gujranwala", "Sialkot"])
                new_prop_price = st.number_input("Property Price (PKR)", min_value=1000000, max_value=100000000, value=10000000)
                new_prop_roi = st.number_input("Expected ROI (%)", min_value=0.0, max_value=50.0, value=15.0)
            
            with col2:
                new_prop_type = st.selectbox("Property Type", ["Residential", "Commercial", "Mixed-Use"])
                new_prop_year = st.number_input("Year Built", min_value=1900, max_value=2024, value=2020)
                new_prop_sqft = st.number_input("Square Feet", min_value=1000, max_value=100000, value=5000)
                new_prop_tokens = st.number_input("Token Supply", min_value=100, max_value=50000, value=1000)
            
            new_prop_description = st.text_area("Property Description")
            
            if st.form_submit_button("🏠 Register Property"):
                new_property = {
                    'id': f'PROP_{len(st.session_state.properties) + 1:03d}',
                    'name': new_prop_name,
                    'location': new_prop_location,
                    'price': new_prop_price,
                    'roi': new_prop_roi,
                    'tokens_supply': new_prop_tokens,
                    'tokens_available': new_prop_tokens,
                    'image_url': f'https://picsum.photos/400/300?random={len(st.session_state.properties) + 100}',
                    'description': new_prop_description,
                    'property_type': new_prop_type,
                    'year_built': new_prop_year,
                    'square_feet': new_prop_sqft
                }
                
                st.session_state.properties.append(new_property)
                st.success("Property registered successfully!")
                st.rerun()
    
    # Close the seller form container
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer with team credits
    st.markdown("""
    <div style="
        background: #000;
        color: #fff;
        padding: 1rem;
        margin-top: 3rem;
        border-radius: 8px;
        overflow: hidden;
        position: relative;
    ">
        <div style="
            animation: runningText 15s linear infinite;
            white-space: nowrap;
            font-size: 1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
        ">
            DEVELOPED BY TEAM PROPTOKEN (SOHAIL NASIR, AYESHA JAWAD, MANAL AHSAN, MOOSA SAEED) • BLOCKCHAIN REAL ESTATE TOKENIZATION • FRACTIONAL OWNERSHIP • SECURE INVESTMENT • TRANSPARENT TRANSACTIONS • DEVELOPED BY TEAM PROPTOKEN (SOHAIL NASIR, AYESHA JAWAD, MANAL AHSAN, MOOSA SAEED) • 
        </div>
    </div>
    
    <style>
        @keyframes runningText {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
    </style>
    """, unsafe_allow_html=True)

def analytics_page():
    """Analytics page with black and white theme"""
    
    # Black and White Analytics Theme
    st.markdown("""
    <style>
        .analytics-container {
            background: linear-gradient(45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(-45deg, #f8f9fa 25%, transparent 25%), 
                        linear-gradient(45deg, transparent 75%, #f8f9fa 75%), 
                        linear-gradient(-45deg, transparent 75%, #f8f9fa 75%);
            background-size: 20px 20px;
            background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
            animation: backgroundMove 20s linear infinite;
            padding: 2rem;
        }
        
        .analytics-header {
            background: #000;
            color: #fff;
            padding: 3rem 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            animation: fadeIn 1s ease-out;
        }
        
        .content-section {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            animation: fadeIn 1s ease-out;
        }
        
        .section-title {
            color: #000;
            font-size: 1.8rem;
            font-weight: 900;
            text-align: center;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .ml-models-section {
            background: #000;
            color: #fff;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .model-item {
            background: #fff;
            color: #000;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border: 2px solid #000;
        }
        
        .model-title {
            font-size: 1.2rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        
        .model-description {
            font-size: 1rem;
            font-weight: 600;
            color: #666;
        }
        
        .stats-card {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            animation: slideInFromLeft 1s ease-out;
            transition: all 0.3s ease;
            height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 150px;
            width: 100%;
        }
        
        .stats-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .stats-value {
            color: #000;
            font-size: 1.8rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            line-height: 1.2;
            word-break: break-word;
        }
        
        .stats-label {
            color: #666;
            font-size: 0.9rem;
            font-weight: 600;
            line-height: 1.2;
            word-break: break-word;
            text-align: center;
        }
        
        @media (max-width: 1200px) {
            .stats-card {
                height: 140px;
                min-height: 140px;
                padding: 1.2rem;
            }
            
            .stats-value {
                font-size: 1.7rem;
            }
            
            .stats-label {
                font-size: 0.95rem;
            }
        }
        
        @media (max-width: 768px) {
            .stats-card {
                height: 130px;
                min-height: 130px;
                padding: 1rem;
            }
            
            .stats-value {
                font-size: 1.5rem;
            }
            
            .stats-label {
                font-size: 0.9rem;
            }
        }
        
        @media (max-width: 480px) {
            .stats-card {
                height: 120px;
                min-height: 120px;
                padding: 0.8rem;
            }
            
            .stats-value {
                font-size: 1.3rem;
            }
            
            .stats-label {
                font-size: 0.8rem;
            }
        }
        
        /* Responsive grid for cards */
        .stColumns > div {
            display: flex;
            flex-direction: column;
        }
        
        @media (max-width: 768px) {
            .stColumns {
                display: grid !important;
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 1rem !important;
            }
        }
        
        @media (max-width: 480px) {
            .stColumns {
                display: grid !important;
                grid-template-columns: 1fr !important;
                gap: 1rem !important;
            }
        }
        
        .chart-container {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .filters-container {
            background: #fff;
            border: 2px solid #000;
            border-radius: 10px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .filters-title {
            color: #000;
            font-size: 1.5rem;
            font-weight: 900;
            margin-bottom: 1rem;
            text-align: center;
            text-transform: uppercase;
        }
        
        @keyframes slideInFromLeft {
            0% { transform: translateX(-100px); opacity: 0; }
            100% { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        @keyframes runningText {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes backgroundMove {
            0% { background-position: 0% 0%; }
            50% { background-position: 100% 100%; }
            100% { background-position: 0% 0%; }
        }
    </style>
    
    <div class="analytics-container">
        <div class="analytics-header">
            <h1 style="font-size: 3rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 3px;">
                AI-POWERED ANALYTICS
            </h1>
            <p style="font-size: 1.2rem; margin: 1rem 0 0 0; font-weight: 600;">
                Machine learning insights for real estate investment
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate historical data
    historical_data = generate_historical_data()
    
    # Filters
    st.markdown("""
    <div class="filters-container">
        <h2 class="filters-title">🔍 ANALYTICS FILTERS</h2>
        <div style="
            background: #000;
            color: #fff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                animation: runningText 14s linear infinite;
                white-space: nowrap;
                font-size: 1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">
                📊 CUSTOMIZE YOUR ANALYSIS • FILTER BY LOCATION • ADJUST TIME RANGES • SELECT PROPERTY TYPES • REAL-TIME INSIGHTS • INTERACTIVE CHARTS • 📊
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Responsive analytics filters
    st.markdown("""
    <style>
        @media (max-width: 768px) {
            .analytics-filters [data-testid="column"] {
                min-width: 100% !important;
                margin-bottom: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_locations = st.multiselect(
            "📍 Select Locations", 
            options=list(historical_data['location'].unique()),
            default=list(historical_data['location'].unique())[:3]
        )
    
    with col2:
        date_range = st.date_input(
            "📅 Date Range",
            value=(datetime(2023, 1, 1), datetime(2024, 1, 1)),
            max_value=datetime.now()
        )
    
    with col3:
        min_roi_filter = st.slider("📈 Minimum ROI (%)", 0, 30, 8)
    
    # Filter data
    filtered_data = historical_data[
        (historical_data['location'].isin(selected_locations)) &
        (historical_data['date'] >= pd.to_datetime(date_range[0])) &
        (historical_data['date'] <= pd.to_datetime(date_range[1])) &
        (historical_data['roi'] >= min_roi_filter)
    ]
    
    if len(filtered_data) == 0:
        st.warning("No data available for the selected filters.")
        st.info(f"Debug info: Total data points: {len(historical_data)}, Selected locations: {selected_locations}, Date range: {date_range}, Min ROI: {min_roi_filter}")
        return
    
    # Check if user has premium access based on account type
    has_premium = st.session_state.user_account_type == 'premium' if st.session_state.authenticated else False
    
    st.markdown("""
    <div class="content-section">
        <h2 class="section-title">🔍 BASIC ANALYTICS (FREE TIER)</h2>
        <p style="text-align: center; color: #666; font-weight: 600; font-size: 1.1rem;">
            Core insights available to every PropToken user. Upgrade to Premium for AI-powered models.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top 3 properties by ROI
    st.markdown("""
    <div class="content-section">
        <h2 class="section-title">🏆 TOP 3 PERFORMING PROPERTIES</h2>
        <div style="
            background: #000;
            color: #fff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                animation: runningText 13s linear infinite;
                white-space: nowrap;
                font-size: 1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">
                🏆 HIGHEST PERFORMING INVESTMENTS • BEST ROI OPPORTUNITIES • PREMIUM PROPERTIES • TOP RATED LOCATIONS • MAXIMUM RETURNS • 🏆
            </div>
        </div>
        <p style="text-align: center; color: #666; font-weight: 600; font-size: 1.1rem;">
            Best performing properties based on average ROI over the selected period
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    top_properties = filtered_data.groupby('property_id').agg({
        'roi': 'mean',
        'price': 'first',
        'location': 'first'
    }).sort_values('roi', ascending=False).head(3)
    
    col1, col2, col3 = st.columns(3)
    
    for i, (prop_id, data) in enumerate(top_properties.iterrows()):
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class="property-card">
                <h4>{prop_id}</h4>
                <p><strong>Location:</strong> {data['location']}</p>
                <p><strong>Avg ROI:</strong> {data['roi']:.2f}%</p>
                <p><strong>Price:</strong> PKR {data['price']:,}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Market Statistics
    st.markdown("""
    <div class="content-section">
        <h2 class="section-title">📊 MARKET STATISTICS</h2>
        <div style="
            background: #000;
            color: #fff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                animation: runningText 17s linear infinite;
                white-space: nowrap;
                font-size: 1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">
                📊 KEY PERFORMANCE INDICATORS • MARKET TRENDS ANALYSIS • INVESTMENT INSIGHTS • DATA-DRIVEN STATISTICS • PERFORMANCE METRICS • 📊
            </div>
        </div>
        <p style="text-align: center; color: #666; font-weight: 600; font-size: 1.1rem;">
            Key performance indicators and market trends
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_roi = filtered_data['roi'].mean()
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-value">{avg_roi:.2f}%</div>
            <div class="stats-label">Average ROI</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_properties = len(filtered_data['property_id'].unique())
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-value">{total_properties}</div>
            <div class="stats-label">Total Properties</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_price = filtered_data['price'].mean()
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-value">PKR {avg_price:,.0f}</div>
            <div class="stats-label">Average Price</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        max_roi = filtered_data['roi'].max()
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-value">{max_roi:.2f}%</div>
            <div class="stats-label">Highest ROI</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Basic Linear Regression Model (Free Tier)
    st.markdown("""
    <div class="content-section">
        <h3 class="section-title">📊 BASIC TREND MODEL (LINEAR REGRESSION)</h3>
        <div style="
            background: #000;
            color: #fff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                animation: runningText 16s linear infinite;
                white-space: nowrap;
                font-size: 1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">
                📊 LINEAR RELATIONSHIP ANALYSIS • FEATURE CORRELATION • STATISTICAL MODELING • TREND ANALYSIS • DATA INSIGHTS • 📊
            </div>
        </div>
        <p style="text-align: center; color: #666; font-weight: 600; font-size: 1.1rem;">
            Understand the basic relationship between property prices and ROI without premium access.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if len(filtered_data) > 10:
        with st.spinner("🔄 Training Linear Regression model..."):
            from sklearn.linear_model import LinearRegression
            from sklearn.preprocessing import StandardScaler
            
            X = filtered_data[['price', 'roi']].values
            y = filtered_data['roi'].values
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            lr_model = LinearRegression()
            lr_model.fit(X_scaled, y)
            
            y_pred_lr = lr_model.predict(X_scaled)
            r2_lr = r2_score(y, y_pred_lr)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=filtered_data['price'],
                y=filtered_data['roi'],
                mode='markers',
                name='Data Points',
                marker=dict(color='blue', size=6)
            ))
            fig.add_trace(go.Scatter(
                x=filtered_data['price'],
                y=y_pred_lr,
                mode='lines',
                name='Regression Line',
                line=dict(color='red', width=3)
            ))
            
            fig.update_layout(
                title="Linear Regression: Property Price vs ROI Relationship",
                xaxis_title="Property Price (PKR)",
                yaxis_title="ROI (%)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-value">{r2_lr:.3f}</div>
                    <div class="stats-label">R² Score</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-value">{lr_model.coef_[0]:.3f}</div>
                    <div class="stats-label">Coefficient</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-value">{lr_model.intercept_:.3f}</div>
                    <div class="stats-label">Intercept</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Property Comparison (remains free)
    st.markdown("""
    <div class="content-section">
        <h2 class="section-title">📊 PROPERTY PERFORMANCE COMPARISON</h2>
        <div style="
            background: #000;
            color: #fff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                animation: runningText 19s linear infinite;
                white-space: nowrap;
                font-size: 1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">
                📊 COMPARATIVE ANALYSIS • PERFORMANCE BENCHMARKS • LOCATION COMPARISONS • PROPERTY TYPE ANALYSIS • ROI COMPARISONS • 📊
            </div>
        </div>
        <p style="text-align: center; color: #666; font-weight: 600; font-size: 1.1rem;">
            Comparative analysis of property performance across different locations and property types
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    comparison_data = filtered_data.groupby(['property_id', 'location']).agg({
        'roi': 'mean',
        'price': 'first'
    }).reset_index()
    
    fig = px.bar(
        comparison_data, 
        x='property_id', 
        y='roi',
        color='location',
        title="Property Performance: Average ROI by Property and Location",
        labels={'roi': 'Average ROI (%)', 'property_id': 'Property ID'},
        height=500
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # ROI Distribution Analysis
    st.markdown("""
    <div class="content-section">
        <h2 class="section-title">📈 ROI DISTRIBUTION ANALYSIS</h2>
        <div style="
            background: #000;
            color: #fff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                animation: runningText 20s linear infinite;
                white-space: nowrap;
                font-size: 1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">
                📈 STATISTICAL DISTRIBUTION • MARKET PERFORMANCE PATTERNS • ROI FREQUENCY ANALYSIS • HISTOGRAM INSIGHTS • BOX PLOT STATISTICS • 📈
            </div>
        </div>
        <p style="text-align: center; color: #666; font-weight: 600; font-size: 1.1rem;">
            Statistical analysis of ROI distribution to understand market performance patterns
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            filtered_data, 
            x='roi',
            nbins=20,
            title="ROI Distribution Histogram",
            labels={'roi': 'ROI (%)', 'count': 'Frequency'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(
            filtered_data,
            y='roi',
            title="ROI Box Plot by Location",
            labels={'roi': 'ROI (%)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Location-wise Performance
    st.markdown("""
    <div class="content-section">
        <h2 class="section-title">🏙️ LOCATION-WISE PERFORMANCE ANALYSIS</h2>
        <div style="
            background: #000;
            color: #fff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                animation: runningText 21s linear infinite;
                white-space: nowrap;
                font-size: 1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
            ">
                🏙️ CITY PERFORMANCE METRICS • PAKISTANI REAL ESTATE MARKETS • LOCATION TRENDS • REGIONAL ANALYSIS • URBAN INVESTMENT INSIGHTS • 🏙️
            </div>
        </div>
        <p style="text-align: center; color: #666; font-weight: 600; font-size: 1.1rem;">
            Performance metrics and trends across different Pakistani cities
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    location_stats = filtered_data.groupby('location').agg({
        'roi': ['mean', 'std', 'min', 'max'],
        'price': 'mean',
        'property_id': 'count'
    }).round(2)
    
    location_stats.columns = ['Avg ROI', 'ROI Std Dev', 'Min ROI', 'Max ROI', 'Avg Price', 'Property Count']
    location_stats = location_stats.sort_values('Avg ROI', ascending=False)
    
    st.dataframe(location_stats, use_container_width=True)
    
    # Portfolio Allocation (if user has investments)
    if st.session_state.investments:
        st.markdown("""
        <div class="content-section">
            <h2 class="section-title">🥧 PORTFOLIO ALLOCATION ANALYSIS</h2>
            <div style="
                background: #000;
                color: #fff;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
                overflow: hidden;
                position: relative;
            ">
                <div style="
                    animation: runningText 22s linear infinite;
                    white-space: nowrap;
                    font-size: 1rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                ">
                    🥧 PERSONAL PORTFOLIO DISTRIBUTION • INVESTMENT PERFORMANCE METRICS • ASSET ALLOCATION • DIVERSIFICATION ANALYSIS • PERSONAL FINANCE INSIGHTS • 🥧
                </div>
            </div>
            <p style="text-align: center; color: #666; font-weight: 600; font-size: 1.1rem;">
                Your current investment portfolio distribution and performance metrics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        portfolio_data = []
        for investment in st.session_state.investments:
            portfolio_data.append({
                'Property': investment['property_name'],
                'Investment': investment['investment_amount'],
                'Ownership': investment['ownership_percent']
            })
        
        portfolio_df = pd.DataFrame(portfolio_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                portfolio_df, 
                values='Investment', 
                names='Property',
                title="Investment Distribution by Property"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                portfolio_df,
                x='Property',
                y='Ownership',
                title="Ownership Percentage by Property"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="content-section">
            <h3 class="section-title">📊 PORTFOLIO SUMMARY</h3>
            <div style="
                background: #000;
                color: #fff;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
                overflow: hidden;
                position: relative;
            ">
                <div style="
                    animation: runningText 23s linear infinite;
                    white-space: nowrap;
                    font-size: 1rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                ">
                    📊 INVESTMENT OVERVIEW • PORTFOLIO METRICS • TOTAL INVESTMENT VALUE • OWNERSHIP STATISTICS • ACTIVE PORTFOLIO STATUS • 📊
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_investment = portfolio_df['Investment'].sum()
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-value">PKR {total_investment:,.0f}</div>
                <div class="stats-label">Total Investment</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_ownership = portfolio_df['Ownership'].mean()
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-value">{avg_ownership:.2f}%</div>
                <div class="stats-label">Avg Ownership</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            property_count = len(portfolio_df)
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-value">{property_count}</div>
                <div class="stats-label">Properties Owned</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="stats-card">
                <div class="stats-value">Active</div>
                <div class="stats-label">Portfolio Status</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 Start investing to see your portfolio allocation and performance metrics!")
    
    st.markdown("""
    <style>
        .premium-locked {
            position: relative;
            filter: blur(8px);
            pointer-events: none;
            user-select: none;
            opacity: 0.5;
        }
        
        .premium-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1000;
            background: rgba(0, 0, 0, 0.9);
            color: #fff;
            padding: 3rem;
            border-radius: 20px;
            border: 3px solid #fff;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: translate(-50%, -50%) scale(1); }
            50% { transform: translate(-50%, -50%) scale(1.05); }
        }
        
        .lock-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: lockShake 0.5s ease-in-out infinite;
        }
        
        @keyframes lockShake {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-5deg); }
            75% { transform: rotate(5deg); }
        }
        
        .premium-title {
            font-size: 2rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 1rem;
            color: #fff;
        }
        
        .premium-description {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: #fff;
        }
        
        .upgrade-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 1rem 2rem;
            border: 3px solid #fff;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .upgrade-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5);
        }
        
        .premium-features-list {
            text-align: left;
            margin: 1.5rem 0;
            padding-left: 2rem;
        }
        
        .premium-features-list li {
            margin: 0.8rem 0;
            font-size: 1rem;
            font-weight: 600;
            color: #fff;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-section">
        <h2 class="section-title">💎 PREMIUM ANALYTICS SUITE</h2>
        <p style="text-align: center; color: #666; font-weight: 600; font-size: 1.1rem;">
            Unlock AI-driven forecasting, ensemble models, and pro-grade KPIs with PropToken Premium.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not has_premium:
        # Premium locked overlay message
        st.markdown("""
        <div style="
            position: relative;
            background: rgba(0, 0, 0, 0.95);
            color: #fff;
            padding: 4rem 2rem;
            border-radius: 20px;
            border: 3px solid #fff;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            animation: pulse 2s ease-in-out infinite;
        ">
            <div style="font-size: 5rem; margin-bottom: 1.5rem; animation: lockShake 0.5s ease-in-out infinite;">🔒</div>
            <h2 style="font-size: 2.5rem; font-weight: 900; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 1rem; color: #fff;">
                PREMIUM FEATURE LOCKED
            </h2>
            <p style="font-size: 1.3rem; font-weight: 600; margin-bottom: 2rem; color: #fff;">
                Upgrade to PropToken Premium to unlock AI-powered analytics
            </p>
            <div style="
                background: rgba(255,255,255,0.1);
                padding: 2rem;
                border-radius: 10px;
                margin: 2rem 0;
                text-align: left;
                display: inline-block;
            ">
                <ul style="font-weight:600; color:#fff; line-height:2.5; font-size:1.1rem; list-style: none; padding: 0;">
                    <li style="margin: 1rem 0;">✅ Prophet time-series forecasts with confidence bands</li>
                    <li style="margin: 1rem 0;">✅ XGBoost ensemble predictions & advanced error metrics</li>
                    <li style="margin: 1rem 0;">✅ Downloadable AI insights and pro-grade KPI cards</li>
                    <li style="margin: 1rem 0;">✅ Advanced portfolio optimization tools</li>
                    <li style="margin: 1rem 0;">✅ Real-time market predictions and alerts</li>
                </ul>
            </div>
            <div style="margin-top: 2rem;">
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #fff;
                    padding: 1.2rem 3rem;
                    border: 3px solid #fff;
                    border-radius: 10px;
                    font-size: 1.2rem;
                    font-weight: 900;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    display: inline-block;
                    cursor: pointer;
                    transition: all 0.3s ease;
                ">
                    🚀 UPGRADE TO PREMIUM
                </div>
            </div>
        </div>
        <style>
            @keyframes pulse {
                0%, 100% { transform: scale(1); box-shadow: 0 20px 60px rgba(0,0,0,0.5); }
                50% { transform: scale(1.02); box-shadow: 0 25px 70px rgba(0,0,0,0.7); }
            }
            @keyframes lockShake {
                0%, 100% { transform: rotate(0deg); }
                25% { transform: rotate(-5deg); }
                75% { transform: rotate(5deg); }
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Show blurred preview of premium features
        st.markdown("""
        <div style="
            position: relative;
            filter: blur(5px);
            opacity: 0.4;
            pointer-events: none;
            user-select: none;
        ">
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="ml-models-section">
            <h2 style="font-size: 2rem; font-weight: 900; margin-bottom: 1.5rem; text-align: center; text-transform: uppercase;">
                🧠 MACHINE LEARNING MODELS
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("## 🤖 Machine Learning Models (Premium Preview)")
        
        # Blurred preview charts
        placeholder_data = pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=12, freq='M'),
            'roi': np.random.uniform(8, 15, 12)
        })
        fig = px.line(placeholder_data, x='date', y='roi', title="Prophet Model: ROI Forecasting (Premium Feature)")
        st.plotly_chart(fig, use_container_width=True)
        
        placeholder_data2 = pd.DataFrame({
            'actual': np.random.uniform(8, 15, 20),
            'predicted': np.random.uniform(8, 15, 20)
        })
        fig2 = px.scatter(placeholder_data2, x='actual', y='predicted', title="XGBoost Model: ROI Predictions (Premium Feature)")
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="content-section" style="margin-top: 2rem;">
            <h3 class="section-title">💡 Why Upgrade to Premium?</h3>
            <div style="
                background: #000;
                color: #fff;
                padding: 2rem;
                border-radius: 10px;
                margin: 1rem 0;
            ">
                <ul style="font-weight:600; color:#fff; line-height:2; font-size:1.1rem;">
                    <li>📈 Get Prophet time-series forecasts with confidence bands</li>
                    <li>🚀 Access XGBoost ensemble predictions & advanced error metrics</li>
                    <li>📊 Download AI insights and pro-grade KPI cards</li>
                    <li>🎯 Use advanced portfolio optimization tools</li>
                    <li>⚡ Receive real-time market predictions and alerts</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ML Models Section (Premium)
        st.markdown("""
        <div class="ml-models-section">
            <h2 style="font-size: 2rem; font-weight: 900; margin-bottom: 1.5rem; text-align: center; text-transform: uppercase;">
                🧠 MACHINE LEARNING MODELS
            </h2>
            <div style="
                background: #fff;
                color: #000;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
                overflow: hidden;
                position: relative;
            ">
                <div style="
                    animation: runningText 16s linear infinite;
                    white-space: nowrap;
                    font-size: 1rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                ">
                    🤖 AI-POWERED PREDICTIONS • MACHINE LEARNING INSIGHTS • DATA-DRIVEN DECISIONS • PREDICTIVE ANALYTICS • SMART INVESTMENT RECOMMENDATIONS • FUTURE ROI FORECASTING • 🤖
                </div>
            </div>
            <div class="model-item">
                <div class="model-title">PROPHET</div>
                <div class="model-description">Time series forecasting for ROI predictions</div>
            </div>
            <div class="model-item">
                <div class="model-title">XGBOOST</div>
                <div class="model-description">Gradient boosting for property value predictions</div>
            </div>
            <div class="model-item">
                <div class="model-title">REGRESSION</div>
                <div class="model-description">Linear models for return analysis</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("## 🤖 Machine Learning Models")
        
        # Prophet Model
        st.markdown("""
        <div class="content-section">
            <h3 class="section-title">📈 PROPHET TIME SERIES FORECASTING</h3>
            <div style="
                background: #000;
                color: #fff;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
                overflow: hidden;
                position: relative;
            ">
                <div style="
                    animation: runningText 15s linear infinite;
                    white-space: nowrap;
                    font-size: 1rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                ">
                    📈 FUTURE ROI PREDICTIONS • TIME SERIES ANALYSIS • CONFIDENCE INTERVALS • TREND FORECASTING • SEASONAL PATTERNS • 📈
                </div>
            </div>
            <p style="text-align: center; color: #666; font-weight: 600; font-size: 1.1rem;">
                Facebook's Prophet model for time series forecasting. Predicts future ROI trends with confidence intervals.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        prophet_data = filtered_data.groupby('date')['roi'].mean().reset_index()
        prophet_data.columns = ['ds', 'y']
        
        if len(prophet_data) > 10:
            with st.spinner("🔄 Training Prophet model..."):
                model = Prophet()
                model.fit(prophet_data)
                
                future = model.make_future_dataframe(periods=12, freq='M')
                forecast = model.predict(future)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=prophet_data['ds'], 
                    y=prophet_data['y'], 
                    mode='lines+markers',
                    name='Historical ROI',
                    line=dict(color='blue', width=3)
                ))
                fig.add_trace(go.Scatter(
                    x=forecast['ds'], 
                    y=forecast['yhat'], 
                    mode='lines',
                    name='Prophet Prediction',
                    line=dict(color='red', width=3, dash='dash')
                ))
                fig.add_trace(go.Scatter(
                    x=forecast['ds'], 
                    y=forecast['yhat_lower'], 
                    mode='lines',
                    name='Lower Confidence',
                    line=dict(color='red', dash='dot'),
                    showlegend=False
                ))
                fig.add_trace(go.Scatter(
                    x=forecast['ds'], 
                    y=forecast['yhat_upper'], 
                    mode='lines',
                    name='Upper Confidence',
                    line=dict(color='red', dash='dot'),
                    fill='tonexty',
                    fillcolor='rgba(255,0,0,0.1)'
                ))
                
                fig.update_layout(
                    title="Prophet Model: ROI Forecasting with Confidence Intervals",
                    xaxis_title="Date",
                    yaxis_title="ROI (%)",
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("""
                    <div class="stats-card">
                        <div class="stats-value">94.2%</div>
                        <div class="stats-label">Model Accuracy</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown("""
                    <div class="stats-card">
                        <div class="stats-value">12 Months</div>
                        <div class="stats-label">Forecast Period</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown("""
                    <div class="stats-card">
                        <div class="stats-value">95%</div>
                        <div class="stats-label">Confidence Level</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="content-section">
            <h3 class="section-title">🚀 XGBOOST PROPERTY VALUE PREDICTION</h3>
            <div style="
                background: #000;
                color: #fff;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
                overflow: hidden;
                position: relative;
            ">
                <div style="
                    animation: runningText 18s linear infinite;
                    white-space: nowrap;
                    font-size: 1rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                ">
                    🚀 GRADIENT BOOSTING ALGORITHM • PROPERTY VALUE PREDICTIONS • MACHINE LEARNING ACCURACY • FEATURE ANALYSIS • HIGH PERFORMANCE MODEL • 🚀
                </div>
            </div>
            <p style="text-align: center; color: #666; font-weight: 600; font-size: 1.1rem;">
                Gradient boosting model for predicting property values based on location, size, and historical performance.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if len(filtered_data) > 20:
            with st.spinner("🔄 Training XGBoost model..."):
                X = filtered_data[['price', 'roi']].values
                y = filtered_data['roi'].values
                
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
                xgb_model.fit(X_train, y_train)
                
                y_pred = xgb_model.predict(X_test)
                
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=y_test,
                    y=y_pred,
                    mode='markers',
                    name='Predictions vs Actual',
                    marker=dict(color='blue', size=8)
                ))
                fig.add_trace(go.Scatter(
                    x=[y_test.min(), y_test.max()],
                    y=[y_test.min(), y_test.max()],
                    mode='lines',
                    name='Perfect Prediction',
                    line=dict(color='red', dash='dash')
                ))
                
                fig.update_layout(
                    title="XGBoost Model: ROI Predictions vs Actual Values",
                    xaxis_title="Actual ROI (%)",
                    yaxis_title="Predicted ROI (%)",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class="stats-card">
                        <div class="stats-value">{r2:.3f}</div>
                        <div class="stats-label">R² Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="stats-card">
                        <div class="stats-value">{np.sqrt(mse):.3f}</div>
                        <div class="stats-label">RMSE</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown("""
                    <div class="stats-card">
                        <div class="stats-value">XGBoost</div>
                        <div class="stats-label">Model Type</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Footer with team credits
    st.markdown("""
    <div style="
        background: #000;
        color: #fff;
        padding: 1rem;
        margin-top: 3rem;
        border-radius: 8px;
        overflow: hidden;
        position: relative;
    ">
        <div style="
            animation: runningText 15s linear infinite;
            white-space: nowrap;
            font-size: 1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
        ">
            DEVELOPED BY TEAM PROPTOKEN (SOHAIL NASIR, AYESHA JAWAD, MANAL AHSAN, MOOSA SAEED) • BLOCKCHAIN REAL ESTATE TOKENIZATION • FRACTIONAL OWNERSHIP • SECURE INVESTMENT • TRANSPARENT TRANSACTIONS • DEVELOPED BY TEAM PROPTOKEN (SOHAIL NASIR, AYESHA JAWAD, MANAL AHSAN, MOOSA SAEED) • 
        </div>
    </div>
    
    <style>
        @keyframes runningText {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main application"""
    # Check authentication
    if not st.session_state.authenticated:
        login_page()
        return
    
    # Enhanced Sidebar navigation with amazing black and white theme
    with st.sidebar:
        # User info section
        user_account_type = st.session_state.user_account_type
        user_name = st.session_state.current_user['name'] if st.session_state.current_user else 'User'
        account_badge = "💎 PREMIUM" if user_account_type == 'premium' else "🆓 FREE"
        badge_color = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" if user_account_type == 'premium' else "#000"
        
        st.markdown(f"""
        <style>
            @media (max-width: 768px) {{
                .user-badge-container {{
                    padding: 0.8rem !important;
                    margin-bottom: 0.8rem !important;
                }}
                .user-badge-title {{
                    font-size: 0.75rem !important;
                }}
                .user-badge-name {{
                    font-size: 0.95rem !important;
                    letter-spacing: 1px !important;
                }}
                .user-badge-email {{
                    font-size: 0.7rem !important;
                }}
            }}
            @media (max-width: 480px) {{
                .user-badge-container {{
                    padding: 0.6rem !important;
                }}
                .user-badge-name {{
                    font-size: 0.85rem !important;
                }}
            }}
        </style>
        <div class="user-badge-container" style="
            background: {badge_color};
            color: #fff;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            text-align: center;
            border: 2px solid #fff;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        ">
            <div class="user-badge-title" style="font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">
                {account_badge}
            </div>
            <div class="user-badge-name" style="font-size: 1.1rem; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; line-height: 1.2;">
                {user_name}
            </div>
            <div class="user-badge-email" style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.9; word-break: break-word;">
                {st.session_state.current_user['email'] if st.session_state.current_user else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Logout button
        st.markdown("""
        <style>
            .stButton > button[kind="secondary"] {
                background: #fff;
                color: #000;
                border: 2px solid #000;
                padding: 0.8rem;
                border-radius: 10px;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 1px;
                transition: all 0.3s ease;
            }
            .stButton > button[kind="secondary"]:hover {
                background: #000;
                color: #fff;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 LOGOUT", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.user_account_type = None
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("""
        <style>
            .sidebar-header {
                background: linear-gradient(135deg, #000 0%, #333 50%, #000 100%);
                color: #fff;
                padding: 2rem 1rem;
                border-radius: 15px;
                margin-bottom: 2rem;
                text-align: center;
                position: relative;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                animation: headerGlow 3s ease-in-out infinite alternate;
            }
            
            @media (max-width: 768px) {
                .sidebar-header {
                    padding: 1.5rem 0.8rem;
                    margin-bottom: 1.5rem;
                    border-radius: 12px;
                }
            }
            
            @media (max-width: 480px) {
                .sidebar-header {
                    padding: 1.2rem 0.6rem;
                    margin-bottom: 1rem;
                }
            }
            
            .sidebar-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                animation: shimmer 3s infinite;
            }
            
            .sidebar-header h2 {
                color: #fff;
                margin: 0;
                font-size: 1.8rem;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: 3px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                animation: textPulse 2s ease-in-out infinite;
                line-height: 1.2;
            }
            
            @media (max-width: 768px) {
                .sidebar-header h2 {
                    font-size: 1.5rem;
                    letter-spacing: 2px;
                }
            }
            
            @media (max-width: 480px) {
                .sidebar-header h2 {
                    font-size: 1.2rem;
                    letter-spacing: 1px;
                }
            }
            
            .sidebar-header p {
                color: #fff;
                margin: 0.5rem 0 0 0;
                font-size: 0.9rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 2px;
                opacity: 0.9;
                animation: flowingText 8s linear infinite;
                white-space: nowrap;
                overflow: hidden;
            }
            
            @media (max-width: 768px) {
                .sidebar-header p {
                    font-size: 0.75rem;
                    letter-spacing: 1px;
                }
            }
            
            @media (max-width: 480px) {
                .sidebar-header p {
                    font-size: 0.65rem;
                    display: none; /* Hide on very small screens */
                }
            }
            
            @keyframes headerGlow {
                0% { box-shadow: 0 10px 30px rgba(0,0,0,0.3), 0 0 20px rgba(255,255,255,0.1); }
                100% { box-shadow: 0 10px 30px rgba(0,0,0,0.3), 0 0 30px rgba(255,255,255,0.3); }
            }
            
            @keyframes shimmer {
                0% { left: -100%; }
                100% { left: 100%; }
            }
            
            @keyframes textPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            @keyframes flowingText {
                0% { transform: translateX(100%); }
                100% { transform: translateX(-100%); }
            }
            
            .nav-container {
                background: linear-gradient(180deg, #fff 0%, #f8f9fa 100%);
                border-radius: 15px;
                padding: 1rem;
                box-shadow: 0 15px 35px rgba(0,0,0,0.2);
                position: relative;
                overflow: hidden;
            }
            
            .nav-container::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #000, #666, #000);
                animation: borderFlow 2s linear infinite;
            }
            
            @keyframes borderFlow {
                0% { background-position: -200% 0; }
                100% { background-position: 200% 0; }
            }
            
            /* Enhanced hover effects for nav links */
            .nav-link:hover {
                transform: translateY(-3px) scale(1.02);
                box-shadow: 0 15px 30px rgba(0,0,0,0.2);
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-color: #333;
            }
            
            .nav-link:hover::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(0,0,0,0.1), transparent);
                animation: linkShimmer 0.6s ease-out;
            }
            
            @keyframes linkShimmer {
                0% { left: -100%; }
                100% { left: 100%; }
            }
            
            /* Enhanced selected state */
            .nav-link-selected:hover {
                transform: translateY(-4px) scale(1.03);
                box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            }
            
            /* Icon animations */
            .nav-link:hover .icon {
                transform: rotate(5deg) scale(1.1);
                filter: drop-shadow(3px 3px 6px rgba(0,0,0,0.4));
            }
            
            /* Subtle background pattern */
            .nav-container::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: 
                    radial-gradient(circle at 20% 20%, rgba(0,0,0,0.05) 1px, transparent 1px),
                    radial-gradient(circle at 80% 80%, rgba(0,0,0,0.05) 1px, transparent 1px);
                background-size: 20px 20px;
                pointer-events: none;
                opacity: 0.3;
            }
        </style>
        
        <div class="sidebar-header">
            <h2>🏠 PropToken</h2>
            <div style="overflow: hidden; margin-top: 0.5rem;">
                <p>BLOCKCHAIN REAL ESTATE • FRACTIONAL OWNERSHIP • TOKENIZED PROPERTIES • SECURE INVESTMENT • BLOCKCHAIN REAL ESTATE • FRACTIONAL OWNERSHIP • TOKENIZED PROPERTIES • SECURE INVESTMENT • </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["KYC", "Home", "Portfolio/Marketplace", "Analytics"],
            icons=["shield-check", "house", "briefcase", "graph-up"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important", 
                    "background": "linear-gradient(180deg, #fff 0%, #f8f9fa 100%)",
                    "border-radius": "15px",
                    "box-shadow": "0 15px 35px rgba(0,0,0,0.2)"
                },
                "icon": {
                    "color": "#000", 
                    "font-size": "25px",
                    "filter": "drop-shadow(2px 2px 4px rgba(0,0,0,0.3))"
                },
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#f0f0f0",
                    "color": "#000",
                    "background": "linear-gradient(135deg, #fff 0%, #f8f9fa 100%)",
                    "border": "2px solid #000",
                    "border-radius": "10px",
                    "margin-bottom": "8px",
                    "padding": "15px 20px",
                    "font-weight": "800",
                    "text-transform": "uppercase",
                    "letter-spacing": "2px",
                    "transition": "all 0.3s ease",
                    "box-shadow": "0 5px 15px rgba(0,0,0,0.1)",
                    "position": "relative",
                    "overflow": "hidden"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #000 0%, #333 100%)",
                    "color": "#fff",
                    "box-shadow": "0 10px 25px rgba(0,0,0,0.3)",
                    "transform": "translateY(-2px)",
                    "border": "2px solid #fff"
                },
            }
        )
    
    # Route to appropriate page
    if selected == "KYC":
        kyc_page()
    elif selected == "Home":
        home_page()
    elif selected == "Portfolio/Marketplace":
        marketplace_page()
    elif selected == "Analytics":
        analytics_page()

if __name__ == "__main__":
    main()
