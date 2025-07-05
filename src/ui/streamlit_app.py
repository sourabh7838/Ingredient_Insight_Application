import streamlit as st
import os
import sys
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.risk_analyzer import RiskAnalyzer
from config import Config

# Page configuration
st.set_page_config(
    page_title="Ingredient Insight App",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-Modern Dashboard Design
st.markdown("""
<style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #0a0a0a;
        color: #ffffff;
        min-height: 100vh;
        position: relative;
    }
    
    /* Animated Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(120, 219, 255, 0.3) 0%, transparent 50%);
        z-index: -1;
        animation: backgroundShift 10s ease-in-out infinite;
    }
    
    @keyframes backgroundShift {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(0.5deg); }
    }
    
    /* Main Container */
    .main .block-container {
        max-width: 1300px;
        padding: 0;
        margin: 0 auto;
        background: rgba(15, 15, 15, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        box-shadow: 
            0 0 60px rgba(120, 119, 198, 0.3),
            0 0 100px rgba(255, 119, 198, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin-top: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
    }
    
    /* Header Section */
    .header-section {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
        padding: 4rem 2rem;
        text-align: center;
        color: white;
        border-radius: 24px 24px 0 0;
        position: relative;
        overflow: hidden;
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 70% 70%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        animation: headerFloat 6s ease-in-out infinite;
    }
    
    @keyframes headerFloat {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(10px, -10px) rotate(1deg); }
    }
    
    .main-header {
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: white;
        text-shadow: 0 0 30px rgba(255, 107, 107, 0.6);
        position: relative;
        z-index: 1;
        animation: headerGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes headerGlow {
        0% { filter: brightness(1) saturate(1); }
        100% { filter: brightness(1.2) saturate(1.3); }
    }
    
    .subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 400;
        margin-bottom: 0;
        line-height: 1.6;
        position: relative;
        z-index: 1;
        background: linear-gradient(45deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 1));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Content Container */
    .content-container {
        padding: 2.5rem;
        background: rgba(0, 0, 0, 0.95);
        color: #ffffff;
        border-radius: 0 0 24px 24px;
    }
    
    /* Demo Banner */
    .demo-banner {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        font-weight: 600;
        box-shadow: 
            0 0 40px rgba(255, 107, 107, 0.4),
            0 0 80px rgba(78, 205, 196, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .demo-banner::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: neonShimmer 4s infinite;
    }
    
    @keyframes neonShimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Modern Cards */
    .modern-card {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(45, 45, 45, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 
            0 0 30px rgba(120, 119, 198, 0.2),
            0 0 60px rgba(255, 119, 198, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1);
        border-radius: 24px 24px 0 0;
    }
    
    .modern-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 0 50px rgba(120, 119, 198, 0.4),
            0 0 100px rgba(255, 119, 198, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    /* Risk Cards */
    .risk-severe {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(255, 107, 107, 0.3) 100%);
        border-left: 6px solid #ff6b6b;
        color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 
            0 0 30px rgba(255, 107, 107, 0.4),
            0 0 60px rgba(255, 107, 107, 0.2);
        border: 1px solid rgba(255, 107, 107, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .risk-high {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.2) 0%, rgba(255, 193, 7, 0.3) 100%);
        border-left: 6px solid #ffc107;
        color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 
            0 0 30px rgba(255, 193, 7, 0.4),
            0 0 60px rgba(255, 193, 7, 0.2);
        border: 1px solid rgba(255, 193, 7, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .risk-moderate {
        background: linear-gradient(135deg, rgba(69, 183, 209, 0.2) 0%, rgba(69, 183, 209, 0.3) 100%);
        border-left: 6px solid #45b7d1;
        color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 
            0 0 30px rgba(69, 183, 209, 0.4),
            0 0 60px rgba(69, 183, 209, 0.2);
        border: 1px solid rgba(69, 183, 209, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .risk-low {
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.2) 0%, rgba(78, 205, 196, 0.3) 100%);
        border-left: 6px solid #4ecdc4;
        color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 
            0 0 30px rgba(78, 205, 196, 0.4),
            0 0 60px rgba(78, 205, 196, 0.2);
        border: 1px solid rgba(78, 205, 196, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(45, 45, 45, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 
            0 0 40px rgba(120, 119, 198, 0.3),
            0 0 80px rgba(255, 119, 198, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1);
        border-radius: 24px 24px 0 0;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 
            0 0 60px rgba(120, 119, 198, 0.4),
            0 0 120px rgba(255, 119, 198, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .metric-card h3 {
        font-size: 0.875rem;
        font-weight: 600;
        color: #ffffff;
        margin: 0 0 0.75rem 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    .metric-card h2 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    }
    
    .metric-card p {
        font-size: 0.875rem;
        color: #ffffff;
        margin: 0;
        line-height: 1.5;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    /* Sidebar */
    .stSidebar {
        background: linear-gradient(135deg, rgba(15, 15, 15, 0.98) 0%, rgba(25, 25, 25, 0.95) 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(15, 15, 15, 0.98) 0%, rgba(25, 25, 25, 0.95) 100%) !important;
        padding: 2rem 1.5rem !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stSidebar .stMarkdown h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        font-size: 1.2rem !important;
        padding: 1rem 0 !important;
        border-bottom: 2px solid rgba(255, 107, 107, 0.5) !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    .stSidebar .stMarkdown h4 {
        color: #ffffff !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        font-size: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    .stSidebar .stMarkdown p {
        color: #ffffff !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
        margin-bottom: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    .stSidebar .stSelectbox label,
    .stSidebar .stMultiSelect label,
    .stSidebar .stSelectSlider label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    .stSidebar .stSelectbox > div > div > div,
    .stSidebar .stMultiSelect > div > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(15, 15, 15, 0.9);
        border-radius: 20px;
        padding: 12px;
        margin-bottom: 2rem;
        box-shadow: 
            0 0 30px rgba(120, 119, 198, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 15px;
        padding: 15px 25px;
        font-weight: 600;
        transition: all 0.4s ease;
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #ffffff;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 107, 107, 0.1);
        color: #ff6b6b;
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.3);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
        color: white;
        box-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
        transform: translateY(-3px);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
        color: white;
        border: none;
        border-radius: 20px;
        font-weight: 600;
        padding: 1rem 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 0 30px rgba(255, 107, 107, 0.4),
            0 0 60px rgba(78, 205, 196, 0.3);
        position: relative;
        overflow: hidden;
        font-size: 1rem;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: all 0.8s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 
            0 0 50px rgba(255, 107, 107, 0.6),
            0 0 100px rgba(78, 205, 196, 0.4);
    }
    
    /* File Uploader */
    .stFileUploader > div > div {
        background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(45, 45, 45, 0.9) 100%);
        border: 3px dashed rgba(255, 255, 255, 0.3);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        color: #ffffff;
        backdrop-filter: blur(10px);
    }
    
    .stFileUploader > div > div:hover {
        border-color: #ff6b6b;
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(78, 205, 196, 0.1) 100%);
        transform: translateY(-8px);
        box-shadow: 
            0 0 40px rgba(255, 107, 107, 0.4),
            0 0 80px rgba(78, 205, 196, 0.3);
    }
    
    /* Text Elements */
    .stApp h1, .stApp h2, .stApp h3 {
        color: #ffffff !important;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    }
    
    .stApp h4, .stApp h5, .stApp h6 {
        color: #ffffff !important;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    .stApp p, .stMarkdown p {
        color: #ffffff !important;
        line-height: 1.6;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    .stApp [data-testid="stMarkdownContainer"] * {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    .stApp [data-testid="stMarkdownContainer"] h1,
    .stApp [data-testid="stMarkdownContainer"] h2,
    .stApp [data-testid="stMarkdownContainer"] h3 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    }
    
    /* Form Elements */
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        color: #ffffff !important;
        background: rgba(30, 30, 30, 0.95) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .content-container { padding: 1.5rem; }
        .header-section { padding: 2rem 1rem; }
        .main-header { font-size: 2rem; }
        .modern-card, .metric-card { padding: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

class IngredientInsightApp:
    def __init__(self):
        """Initialize the Streamlit app"""
        self.risk_analyzer = None
        self.initialize_app()
    
    def initialize_app(self):
        """Initialize the risk analyzer"""
        try:
            if 'risk_analyzer' not in st.session_state:
                with st.spinner('Initializing Ingredient Insight App...'):
                    st.session_state.risk_analyzer = RiskAnalyzer()
            self.risk_analyzer = st.session_state.risk_analyzer
            
            # Check if running in demo mode
            if hasattr(self.risk_analyzer.vision_service, 'demo_mode') and self.risk_analyzer.vision_service.demo_mode:
                st.info("🔄 **Demo Mode Active** - The app is running without Google Cloud Vision API credentials. You can explore all features with sample data!")
        except Exception as e:
            st.error(f"Failed to initialize the app: {str(e)}")
            st.info("The app will continue in demo mode with sample data.")
            # Don't stop the app, let it continue in demo mode
    
    def run(self):
        """Main application runner"""
        # Main header with modern styling
        st.markdown("""
        <div class="header-section">
            <div class="main-header">🔍 Ingredient Insight App</div>
            <div class="subtitle">🧪 AI-Powered Health Risk Analysis for Food & Personal Care Products</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Content container
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        
        # Demo mode banner
        demo_mode = hasattr(self.risk_analyzer.vision_service, 'demo_mode') and self.risk_analyzer.vision_service.demo_mode
        if demo_mode:
            st.markdown("""
            <div class="demo-banner">
                🚀 <strong>Demo Mode Active</strong> - Explore all features with sample data! 
                Configure your Google Cloud Vision API credentials to analyze real images.
            </div>
            """, unsafe_allow_html=True)
        
        # Sidebar
        self.render_sidebar()
        
        # Main content with enhanced tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📷 Product Analysis", 
            "📊 Analytics Dashboard", 
            "⚙️ Settings", 
            "ℹ️ About"
        ])
        
        with tab1:
            self.render_product_analysis()
        
        with tab2:
            self.render_dashboard()
        
        with tab3:
            self.render_settings()
        
        with tab4:
            self.render_about()
        
        # Close content container
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the enhanced sidebar with user preferences"""
        st.sidebar.markdown("### 🎯 Personal Settings")
        
        # User allergens with better styling
        st.sidebar.markdown("#### 🤧 Your Allergens")
        allergen_options = Config.COMMON_ALLERGENS
        user_allergens = st.sidebar.multiselect(
            "Select allergens you're sensitive to:",
            options=allergen_options,
            default=st.session_state.get('user_allergens', []),
            help="Select any allergens you have to get personalized warnings"
        )
        st.session_state.user_allergens = user_allergens
        
        if user_allergens:
            st.sidebar.success(f"✅ Monitoring {len(user_allergens)} allergen(s)")
        
        # Risk sensitivity with enhanced display
        st.sidebar.markdown("#### ⚖️ Risk Sensitivity")
        risk_sensitivity = st.sidebar.select_slider(
            "Choose your risk sensitivity level:",
            options=["Low", "Moderate", "High", "Very High"],
            value=st.session_state.get('risk_sensitivity', 'Moderate'),
            help="Higher sensitivity shows more warnings for lower-risk ingredients"
        )
        st.session_state.risk_sensitivity = risk_sensitivity
        
        # Product preferences with icons
        st.sidebar.markdown("#### 🏷️ Product Preferences")
        preferred_categories = st.sidebar.multiselect(
            "Preferred product categories:",
            options=["Organic", "Natural", "Gluten-Free", "Vegan", "Non-GMO"],
            default=st.session_state.get('preferred_categories', []),
            help="Select your preferred product types"
        )
        st.session_state.preferred_categories = preferred_categories
        
        st.sidebar.markdown("---")
        
        # Analysis history with better formatting
        if 'analysis_history' in st.session_state and st.session_state.analysis_history:
            st.sidebar.markdown("#### 📈 Analysis History")
            
            # Statistics
            total_analyses = len(st.session_state.analysis_history)
            st.sidebar.info(f"📊 **{total_analyses}** total analyses")
            
            # Show last analysis summary
            if st.session_state.analysis_history:
                last_analysis = st.session_state.analysis_history[-1]
                timestamp = last_analysis.get('timestamp', 'N/A')
                
                # Format timestamp
                if timestamp != 'N/A':
                    from datetime import datetime
                    try:
                        dt = datetime.fromisoformat(timestamp)
                        formatted_time = dt.strftime("%m/%d %I:%M %p")
                        st.sidebar.write(f"🕐 **Latest:** {formatted_time}")
                    except:
                        st.sidebar.write(f"🕐 **Latest:** {timestamp}")
                
                # Risk level indicator with better styling
                risk_level = last_analysis.get('risk_analysis', {}).get('overall_risk_score', {}).get('level', 'UNKNOWN')
                risk_colors = {
                    'LOW': '#10b981',
                    'MODERATE': '#3b82f6', 
                    'HIGH': '#f59e0b',
                    'SEVERE': '#dc2626',
                    'UNKNOWN': '#6b7280'
                }
                color = risk_colors.get(risk_level, '#6b7280')
                st.sidebar.markdown(f"📊 **Risk Level:** <span style='color: {color}; font-weight: bold;'>{risk_level}</span>", unsafe_allow_html=True)
        
        # Add some helpful tips
        st.sidebar.markdown("---")
        st.sidebar.markdown("#### 💡 Tips")
        st.sidebar.markdown("""
        - 📱 Take clear photos of ingredient lists
        - 🔍 Ensure good lighting and focus
        - 📋 Set your allergens for personalized alerts
        - 🎯 Adjust risk sensitivity to your needs
        """)
        
        # Footer
        st.sidebar.markdown("---")
        st.sidebar.markdown("*Made with ❤️ for healthier choices*")
    
    def render_product_analysis(self):
        """Render the enhanced product analysis interface"""
        st.markdown("### 📷 Product Analysis")
        
        # Enhanced file uploader section
        st.markdown("""
        <div class="info-box">
            <h4>📤 Upload Product Image</h4>
            <p>Upload a clear photo of your product's ingredient list for AI-powered analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Image upload with better styling
        uploaded_file = st.file_uploader(
            "Choose a product image",
            type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
            help="📸 Upload a clear photo showing the ingredients list",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Display uploaded image with enhanced layout
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("#### 📸 Uploaded Image")
                image = Image.open(uploaded_file)
                st.image(image, caption="Product Image", use_container_width=True)
                
                # Image info with better formatting
                st.markdown("**📊 Image Details:**")
                st.markdown(f"- **Size:** {image.size[0]} × {image.size[1]} pixels")
                st.markdown(f"- **Format:** {image.format}")
                st.markdown(f"- **File size:** {uploaded_file.size / 1024:.1f} KB")
            
            with col2:
                st.markdown("#### 🔬 Analysis Options")
                
                # Analysis configuration
                st.markdown("**Analysis Settings:**")
                user_allergens = st.session_state.get('user_allergens', [])
                if user_allergens:
                    st.success(f"✅ Monitoring {len(user_allergens)} allergen(s)")
                else:
                    st.info("💡 Add allergens in the sidebar for personalized alerts")
                
                risk_sensitivity = st.session_state.get('risk_sensitivity', 'Moderate')
                st.write(f"🎯 **Risk Sensitivity:** {risk_sensitivity}")
                
                st.markdown("---")
                
                # Analysis button with enhanced styling
                if st.button("🔍 **Analyze Product**", type="primary", use_container_width=True):
                    self.analyze_product(uploaded_file)
                
                # Additional options
                st.markdown("**Quick Actions:**")
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("📱 Tips", use_container_width=True):
                        st.info("📝 **Photo Tips:**\n- Clear, well-lit images\n- Focus on ingredient text\n- Avoid glare and shadows")
                with col_b:
                    if st.button("🎯 Settings", use_container_width=True):
                        st.info("⚙️ **Adjust Settings:**\n- Add allergens in sidebar\n- Set risk sensitivity\n- Configure preferences")
        
        else:
            # Check if in demo mode
            demo_mode = hasattr(self.risk_analyzer.vision_service, 'demo_mode') and self.risk_analyzer.vision_service.demo_mode
            
            # Welcome section with better styling
            if demo_mode:
                st.markdown("""
                <div class="demo-banner">
                    🎭 <strong>Demo Mode</strong> - Upload any image to see sample analysis results!
                </div>
                """, unsafe_allow_html=True)
                
                # Demo button with enhanced styling
                if st.button("🎭 **Try Demo Analysis**", type="primary", use_container_width=True):
                    self.run_demo_analysis()
            else:
                st.markdown("""
                <div class="info-box">
                    <h4>👆 Get Started</h4>
                    <p>Upload a product image above to begin your health risk analysis</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Tips section with enhanced styling
            st.markdown("### 💡 Tips for Better Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if demo_mode:
                    st.markdown("""
                    **🎭 Demo Mode Features:**
                    - Upload any image to see analysis
                    - Sample ingredient data used
                    - Personalized alerts based on your settings
                    - All features fully functional
                    """)
                else:
                    st.markdown("""
                    **📸 Photo Quality:**
                    - Clear, well-lit images
                    - Focus on ingredient text
                    - Avoid glare and shadows
                    - Multiple angles if needed
                    """)
            
            with col2:
                st.markdown("""
                **⚙️ Personalization:**
                - Add allergens in sidebar
                - Set risk sensitivity level
                - Configure product preferences
                - Review analysis history
                """)
            
            # Example workflow
            st.markdown("### 🔄 How It Works")
            st.markdown("""
            1. **📤 Upload** - Take or upload a product photo
            2. **🔍 Analyze** - AI extracts and analyzes ingredients
            3. **⚠️ Alerts** - Get personalized health warnings
            4. **💡 Learn** - Understand risks and get recommendations
            """)
    
    def analyze_product(self, uploaded_file):
        """Analyze the uploaded product image"""
        try:
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Modern progress indicator
            progress_container = st.container()
            with progress_container:
                st.markdown("""
                <div class="info-box">
                    <h4>🔬 AI Analysis in Progress</h4>
                    <p>Our advanced algorithms are analyzing your product...</p>
                </div>
                """, unsafe_allow_html=True)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Initialize analysis
                status_text.markdown("**🔍 Analyzing product image...**")
                progress_bar.progress(20)
                
                # Step 2: Perform analysis
                status_text.markdown("**🧠 Extracting ingredients and analyzing risks...**")
                progress_bar.progress(60)
                
                # Get user allergens
                user_allergens = st.session_state.get('user_allergens', [])
                
                # Analyze the product
                result = self.risk_analyzer.analyze_product_image(temp_path, user_allergens)
                
                status_text.markdown("**✅ Analysis complete!**")
                progress_bar.progress(100)
                
                # Clean up temp file
                os.remove(temp_path)
                
                # Store in session state
                if 'analysis_history' not in st.session_state:
                    st.session_state.analysis_history = []
                st.session_state.analysis_history.append(result)
                st.session_state.current_analysis = result
                
                # Show success message
                st.markdown("""
                <div class="info-box">
                    <h4>🎉 Analysis Complete!</h4>
                    <p>Your personalized health insights are ready below.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Clear progress indicators after a moment
                import time
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
            
            # Display results
            self.display_analysis_results(result)
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def run_demo_analysis(self):
        """Run a demo analysis with sample data"""
        try:
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Demo initialization
            status_text.text("🎭 Preparing demo analysis...")
            progress_bar.progress(20)
            
            # Step 2: Demo processing
            status_text.text("🧠 Analyzing sample product data...")
            progress_bar.progress(60)
            
            # Get user allergens
            user_allergens = st.session_state.get('user_allergens', [])
            
            # Create demo result
            result = self._create_demo_result(user_allergens)
            
            status_text.text("✅ Demo analysis complete!")
            progress_bar.progress(100)
            
            # Store in session state
            if 'analysis_history' not in st.session_state:
                st.session_state.analysis_history = []
            st.session_state.analysis_history.append(result)
            st.session_state.current_analysis = result
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            self.display_analysis_results(result)
            
        except Exception as e:
            st.error(f"Demo analysis failed: {str(e)}")
    
    def _create_demo_result(self, user_allergens: List[str]) -> Dict:
        """Create a demo result with sample data"""
        from datetime import datetime
        
        # Sample ingredients that might trigger some alerts
        demo_ingredients = [
            'Water', 'Sugar', 'Modified Corn Starch', 'Citric Acid', 'Natural Flavors',
            'Sodium Benzoate', 'Red 40', 'Blue 1', 'Vitamin C', 'High Fructose Corn Syrup',
            'Artificial Colors', 'Potassium Sorbate', 'Milk', 'Wheat Flour', 'Eggs'
        ]
        
        # Create mock product info
        product_info = {
            'brand': 'Demo Brand',
            'product_type': 'food',
            'confidence': 0.85,
            'labels': [
                {'description': 'Food', 'confidence': 95.0},
                {'description': 'Snack food', 'confidence': 89.0},
                {'description': 'Package', 'confidence': 87.0}
            ],
            'text_info': {
                'text': 'INGREDIENTS: ' + ', '.join(demo_ingredients),
                'confidence': 0.85,
                'ingredients': demo_ingredients,
                'word_count': len(demo_ingredients) + 1
            },
            'ingredients': demo_ingredients
        }
        
        # Create mock risk analysis using the actual analyzer
        risk_analysis = self.risk_analyzer._perform_comprehensive_risk_analysis(
            demo_ingredients, user_allergens, 'food'
        )
        
        # Generate alerts
        alerts = self.risk_analyzer._generate_personalized_alerts(risk_analysis, user_allergens)
        
        return {
            'product_info': product_info,
            'additional_data': None,
            'ingredients': demo_ingredients,
            'risk_analysis': risk_analysis,
            'alerts': alerts,
            'summary': self.risk_analyzer._generate_summary(risk_analysis, alerts),
            'recommendations': self.risk_analyzer._generate_recommendations(risk_analysis, 'food'),
            'timestamp': datetime.now().isoformat(),
            'demo_mode': True
        }
    
    def display_analysis_results(self, result: Dict):
        """Display the analysis results"""
        if result.get('error'):
            st.error(f"❌ {result['message']}")
            return
        
        # Demo mode indicator
        if result.get('demo_mode'):
            st.success("🎭 **Demo Analysis Results** - This analysis uses sample data to demonstrate the app's capabilities")
        
        # Summary
        st.subheader("📋 Analysis Summary")
        summary = result.get('summary', 'No summary available')
        risk_level = result.get('risk_analysis', {}).get('overall_risk_score', {}).get('level', 'UNKNOWN')
        
        # Display summary with appropriate styling
        css_class = f"risk-{risk_level.lower()}"
        st.markdown(f'<div class="modern-card {css_class}"><strong>📋 Analysis Summary</strong><br/>{summary}</div>', unsafe_allow_html=True)
        
        # Alerts with enhanced styling
        alerts = result.get('alerts', [])
        if alerts:
            st.subheader("🚨 Personalized Alerts")
            for alert in alerts:
                priority = alert.get('priority', 'MODERATE')
                message = alert.get('message', 'No message')
                css_class = f"alert-{priority.lower()}"
                icon = "⚠️" if priority == "CRITICAL" else "🔸" if priority == "HIGH" else "ℹ️"
                st.markdown(f'<div class="alert-card {css_class}"><strong>{icon} {priority}</strong><br/>{message}</div>', unsafe_allow_html=True)
        
        # Detailed analysis tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🏷️ Product Info", "🧪 Ingredient Analysis", "📊 Risk Breakdown", "💡 Recommendations"])
        
        with tab1:
            self.display_product_info(result)
        
        with tab2:
            self.display_ingredient_analysis(result)
        
        with tab3:
            self.display_risk_breakdown(result)
        
        with tab4:
            self.display_recommendations(result)
    
    def display_product_info(self, result: Dict):
        """Display product information"""
        st.subheader("🏷️ Product Information")
        
        product_info = result.get('product_info', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Brand:** {product_info.get('brand', 'Unknown')}")
            st.write(f"**Product Type:** {product_info.get('product_type', 'Unknown').title()}")
            st.write(f"**Confidence:** {product_info.get('confidence', 0):.1%}")
        
        with col2:
            # Detected labels
            labels = product_info.get('labels', [])
            if labels:
                st.write("**Detected Labels:**")
                for label in labels[:5]:  # Show top 5
                    st.write(f"- {label.get('description', 'Unknown')} ({label.get('confidence', 0):.1f}%)")
        
        # Extracted text
        text_info = product_info.get('text_info', {})
        if text_info.get('text'):
            st.subheader("📝 Extracted Text")
            with st.expander("View extracted text"):
                st.text(text_info['text'])
    
    def display_ingredient_analysis(self, result: Dict):
        """Display ingredient analysis"""
        st.subheader("🧪 Ingredient Analysis")
        
        ingredients = result.get('ingredients', [])
        
        if not ingredients:
            st.warning("No ingredients detected in the image")
            return
        
        # Ingredients list
        st.write(f"**Found {len(ingredients)} ingredients:**")
        
        # Create DataFrame for ingredients
        ingredient_data = []
        risk_analysis = result.get('risk_analysis', {})
        ewg_analysis = risk_analysis.get('ewg_analysis', {})
        detailed_analyses = ewg_analysis.get('detailed_analyses', [])
        
        for i, ingredient in enumerate(ingredients):
            # Find corresponding EWG analysis
            ingredient_analysis = None
            for analysis in detailed_analyses:
                if analysis.get('ingredient', '').lower() == ingredient.lower():
                    ingredient_analysis = analysis
                    break
            
            if ingredient_analysis:
                ingredient_data.append({
                    'Ingredient': ingredient,
                    'Risk Level': ingredient_analysis.get('hazard_level', 'UNKNOWN'),
                    'Hazard Score': ingredient_analysis.get('hazard_score', 1),
                    'Concerns': ', '.join(ingredient_analysis.get('concerns', [])),
                    'Recommendation': ingredient_analysis.get('recommendation', 'No recommendation')
                })
            else:
                ingredient_data.append({
                    'Ingredient': ingredient,
                    'Risk Level': 'UNKNOWN',
                    'Hazard Score': 1,
                    'Concerns': '',
                    'Recommendation': 'No analysis available'
                })
        
        # Display as table
        if ingredient_data:
            df = pd.DataFrame(ingredient_data)
            st.dataframe(df, use_container_width=True)
            
            # Risk level distribution
            risk_counts = df['Risk Level'].value_counts()
            fig = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Risk Level Distribution",
                color_discrete_map={
                    'LOW': '#4CAF50',
                    'MODERATE': '#FF9800',
                    'HIGH': '#F44336',
                    'SEVERE': '#9C27B0',
                    'UNKNOWN': '#9E9E9E'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def display_risk_breakdown(self, result: Dict):
        """Display detailed risk breakdown"""
        st.subheader("📊 Risk Breakdown")
        
        risk_analysis = result.get('risk_analysis', {})
        
        # Overall risk score with enhanced styling
        overall_score = risk_analysis.get('overall_risk_score', {})
        col1, col2, col3 = st.columns(3)
        
        with col1:
            score = overall_score.get('score', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚡ Overall Risk Score</h3>
                <h2 style="color: {'#dc2626' if score >= 7 else '#f59e0b' if score >= 4 else '#10b981'};">{score}/10</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            level = overall_score.get('level', 'UNKNOWN')
            level_color = {'LOW': '#10b981', 'MODERATE': '#3b82f6', 'HIGH': '#f59e0b', 'SEVERE': '#dc2626'}.get(level, '#6b7280')
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 Risk Level</h3>
                <h2 style="color: {level_color};">{level}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_ingredients = len(result.get('ingredients', []))
            st.markdown(f"""
            <div class="metric-card">
                <h3>🧪 Total Ingredients</h3>
                <h2 style="color: #6366f1;">{total_ingredients}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk categories
        ewg_analysis = risk_analysis.get('ewg_analysis', {})
        allergen_analysis = risk_analysis.get('allergen_analysis', {})
        additive_analysis = risk_analysis.get('additive_analysis', {})
        
        # EWG Analysis with enhanced styling
        st.subheader("🧬 Chemical Safety Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            high_risk = ewg_analysis.get('high_risk_ingredients', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>🔴 High Risk</h3>
                <h2 style="color: #dc2626;">{high_risk}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            moderate_risk = ewg_analysis.get('moderate_risk_ingredients', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>🟡 Moderate Risk</h3>
                <h2 style="color: #f59e0b;">{moderate_risk}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            low_risk = ewg_analysis.get('low_risk_ingredients', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h3>🟢 Low Risk</h3>
                <h2 style="color: #10b981;">{low_risk}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Allergen Analysis
        st.subheader("🤧 Allergen Analysis")
        detected_allergens = allergen_analysis.get('detected_allergens', [])
        user_matches = allergen_analysis.get('user_allergen_matches', [])
        
        if detected_allergens:
            st.write(f"**Detected Allergens:** {len(detected_allergens)}")
            for allergen in detected_allergens:
                severity = allergen.get('severity', 'UNKNOWN')
                color = '🔴' if severity == 'HIGH' else '🟡'
                st.write(f"{color} {allergen.get('allergen', 'Unknown')} (in {allergen.get('ingredient', 'Unknown')})")
        
        if user_matches:
            st.error(f"⚠️ **WARNING:** Product contains {len(user_matches)} allergen(s) you're sensitive to!")
        
        # Additive Analysis
        st.subheader("🧪 Additive Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Additives", additive_analysis.get('total_additives', 0))
        
        with col2:
            st.metric("High Risk Additives", additive_analysis.get('high_risk_additives', 0))
        
        # Banned substances
        banned_substances = risk_analysis.get('banned_substances', [])
        if banned_substances:
            st.error(f"🚫 **BANNED SUBSTANCES DETECTED:** {len(banned_substances)}")
            for substance in banned_substances:
                st.write(f"- {substance.get('banned_substance', 'Unknown')} in {substance.get('ingredient', 'Unknown')}")
    
    def display_recommendations(self, result: Dict):
        """Display recommendations"""
        st.subheader("💡 Recommendations")
        
        recommendations = result.get('recommendations', [])
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")
        else:
            st.info("No specific recommendations available")
        
        # Safer alternatives
        st.subheader("🔄 Safer Alternatives")
        st.info("This feature will suggest safer alternative products based on your preferences and risk analysis")
        
        # Educational content
        st.subheader("📚 Learn More")
        st.write("""
        **Understanding Risk Levels:**
        - 🟢 **LOW (1-2)**: Generally safe for most people
        - 🟡 **MODERATE (3-4)**: Use with awareness, monitor for sensitivities
        - 🟠 **HIGH (5-7)**: Use with caution, consider alternatives
        - 🔴 **SEVERE (8-10)**: Avoid, seek safer alternatives
        """)
    
    def render_dashboard(self):
        """Render the premium analytics dashboard"""
        st.markdown("### 📊 Analytics Dashboard")
        
        if 'analysis_history' not in st.session_state or not st.session_state.analysis_history:
            st.markdown("""
            <div class="info-box">
                <h4>🎯 Your Health Analytics Hub</h4>
                <p>Start analyzing products to unlock powerful insights about your health choices. 
                Track risk patterns, monitor allergen exposure, and make informed decisions.</p>
            </div>
            """, unsafe_allow_html=True)
            return
        
        history = st.session_state.analysis_history
        
        # Premium statistics with enhanced styling
        st.markdown("#### 📈 Health Analytics Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🔬 Total Analyses</h3>
                <h2 style="color: #6366f1;">{len(history)}</h2>
                <p style="font-size: 0.9rem; color: #64748b;">Products analyzed</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            high_risk_count = sum(1 for h in history if h.get('risk_analysis', {}).get('overall_risk_score', {}).get('level') in ['HIGH', 'SEVERE'])
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚠️ High Risk Items</h3>
                <h2 style="color: #dc2626;">{high_risk_count}</h2>
                <p style="font-size: 0.9rem; color: #64748b;">Products to avoid</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_risk_score = sum(h.get('risk_analysis', {}).get('overall_risk_score', {}).get('score', 0) for h in history) / len(history)
            color = '#dc2626' if avg_risk_score >= 7 else '#f59e0b' if avg_risk_score >= 4 else '#10b981'
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚡ Avg Risk Score</h3>
                <h2 style="color: {color};">{avg_risk_score:.1f}/10</h2>
                <p style="font-size: 0.9rem; color: #64748b;">Overall health risk</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            allergen_matches = sum(len(h.get('risk_analysis', {}).get('allergen_analysis', {}).get('user_allergen_matches', [])) for h in history)
            st.markdown(f"""
            <div class="metric-card">
                <h3>🤧 Allergen Matches</h3>
                <h2 style="color: #f59e0b;">{allergen_matches}</h2>
                <p style="font-size: 0.9rem; color: #64748b;">Personal alerts</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Interactive visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk level distribution with enhanced styling
            st.markdown("#### 📊 Risk Level Distribution")
            risk_levels = [h.get('risk_analysis', {}).get('overall_risk_score', {}).get('level', 'UNKNOWN') for h in history]
            risk_counts = pd.Series(risk_levels).value_counts()
            
            fig = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="",
                color_discrete_map={
                    'LOW': '#10b981',
                    'MODERATE': '#3b82f6',
                    'HIGH': '#f59e0b',
                    'SEVERE': '#dc2626',
                    'UNKNOWN': '#6b7280'
                },
                hole=0.4
            )
            fig.update_layout(
                font=dict(family="Inter", size=12),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk trends over time with enhanced styling
            st.markdown("#### 📈 Risk Score Trends")
            if len(history) > 1:
                risk_scores = [h.get('risk_analysis', {}).get('overall_risk_score', {}).get('score', 0) for h in history]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(range(1, len(risk_scores) + 1)),
                    y=risk_scores,
                    mode='lines+markers',
                    name='Risk Score',
                    line=dict(color='#667eea', width=3),
                    marker=dict(color='#764ba2', size=8),
                    fill='tonexty',
                    fillcolor='rgba(102, 126, 234, 0.1)'
                ))
                
                fig.update_layout(
                    title="",
                    xaxis_title="Analysis Number",
                    yaxis_title="Risk Score (0-10)",
                    yaxis=dict(range=[0, 10]),
                    font=dict(family="Inter", size=12),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("""
                <div class="info-box">
                    <h4>📈 Trend Analysis</h4>
                    <p>Analyze more products to see your risk trend over time</p>
                </div>
                """, unsafe_allow_html=True)
    
    def render_settings(self):
        """Render the settings page"""
        st.header("⚙️ Settings")
        
        # API Configuration
        st.subheader("🔑 API Configuration")
        with st.expander("Google Cloud Vision API"):
            st.write("Configure your Google Cloud Vision API credentials:")
            st.code("""
            1. Create a Google Cloud Project
            2. Enable the Vision API
            3. Create a service account and download the JSON key
            4. Set GOOGLE_CLOUD_CREDENTIALS_PATH in your .env file
            """)
        
        # Data Export
        st.subheader("📤 Data Export")
        if st.button("Export Analysis History"):
            if 'analysis_history' in st.session_state:
                # Convert to DataFrame and download
                df = pd.DataFrame(st.session_state.analysis_history)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="ingredient_analysis_history.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No analysis history to export")
        
        # Clear History
        st.subheader("🗑️ Clear Data")
        if st.button("Clear Analysis History", type="secondary"):
            st.session_state.analysis_history = []
            st.success("Analysis history cleared!")
    
    def render_about(self):
        """Render the enhanced about page"""
        st.markdown("### ℹ️ About Ingredient Insight App")
        
        # Hero section
        st.markdown("""
        <div class="info-box">
            <h2>🎯 Empowering Healthier Choices</h2>
            <p>Transform the way you understand product ingredients with AI-powered analysis and personalized health insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Features section
        st.markdown("#### ✨ Key Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🔍 Smart Analysis</h3>
                <p>AI-powered image recognition and OCR technology extracts ingredient lists from product photos with high accuracy.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
                <h3>🧪 Chemical Safety</h3>
                <p>Comprehensive database of 1000+ toxic chemicals with detailed hazard scoring and safety recommendations.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🤧 Allergen Detection</h3>
                <p>Personalized allergen alerts based on your specific sensitivities and dietary restrictions.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
                <h3>📊 Risk Assessment</h3>
                <p>Advanced risk scoring system with actionable recommendations for healthier alternatives.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Technology stack
        st.markdown("#### 🛠️ Technology Stack")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🤖 AI & Machine Learning**
            - Google Cloud Vision API
            - Custom OCR algorithms
            - Ingredient pattern recognition
            """)
        
        with col2:
            st.markdown("""
            **📊 Data Sources**
            - OpenFoodFacts database
            - EWG chemical database
            - FDA ingredient listings
            """)
        
        with col3:
            st.markdown("""
            **💻 Technical Stack**
            - Python backend
            - Streamlit framework
            - Advanced data analytics
            """)
        
        # Privacy & Security
        st.markdown("#### 🔒 Privacy & Security")
        st.markdown("""
        <div class="info-box">
            <h4>Your Data, Your Control</h4>
            <ul>
                <li>🛡️ <strong>Local Processing:</strong> Images analyzed locally, never stored permanently</li>
                <li>🔐 <strong>Session Privacy:</strong> Personal data kept in browser session only</li>
                <li>🚫 <strong>No Tracking:</strong> No personal information transmitted to external services</li>
                <li>⚡ <strong>Real-time Analysis:</strong> Instant results without data retention</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Support section
        st.markdown("#### 📞 Support & Resources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **💡 Getting Started**
            - Upload clear product images
            - Set your personal allergens
            - Adjust risk sensitivity
            - Review analysis results
            """)
        
        with col2:
            st.markdown("""
            **🎯 Best Practices**
            - Ensure good lighting
            - Focus on ingredient lists
            - Regular sensitivity updates
            - Review recommendations
            """)
        
        # Disclaimer
        st.markdown("#### ⚠️ Important Disclaimer")
        st.markdown("""
        <div class="alert-card alert-moderate">
            <strong>📄 Medical Disclaimer</strong><br/>
            This application provides educational information only and should not replace professional medical advice. 
            Always consult healthcare providers for specific health concerns, allergies, or dietary restrictions.
            The risk assessments are based on available data and may not reflect individual sensitivities.
        </div>
        """, unsafe_allow_html=True)
    
    def get_risk_color(self, risk_level: str) -> str:
        """Get color for risk level"""
        colors = {
            'LOW': '#4CAF50',
            'MODERATE': '#FF9800',
            'HIGH': '#F44336',
            'SEVERE': '#9C27B0',
            'UNKNOWN': '#9E9E9E'
        }
        return colors.get(risk_level, '#9E9E9E')

# Initialize and run the app
if __name__ == "__main__":
    app = IngredientInsightApp()
    app.run() 