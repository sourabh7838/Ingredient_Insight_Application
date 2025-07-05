# 🔍 Ingredient Insight App

A comprehensive Python application that analyzes food and personal care product images to identify ingredients and assess health risks using AI-powered computer vision and integrated health databases.

## 🎯 Features

- **🔍 AI-Powered Image Analysis**: Uses Google Cloud Vision AI for OCR and product recognition
- **🧪 Ingredient Safety Analysis**: Integrates EWG (Environmental Working Group) database for toxic chemical identification
- **🤧 Allergen Detection**: Identifies common allergens and provides personalized alerts
- **📊 Risk Assessment**: Comprehensive health risk scoring with actionable recommendations
- **📈 Analytics Dashboard**: Track your product analysis history and risk trends
- **🌐 Web Interface**: Beautiful, user-friendly Streamlit interface

## 🛠️ Technology Stack

- **Computer Vision**: Google Cloud Vision API
- **Data Sources**: OpenFoodFacts API, EWG Database
- **Backend**: Python 3.8+
- **Frontend**: Streamlit
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **Image Processing**: OpenCV, Pillow

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Cloud Vision API credentials
- Internet connection for API calls

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ingredient-insight-app.git
   cd ingredient-insight-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud Vision API**
   - Create a Google Cloud Project
   - Enable the Vision API
   - Create a service account and download the JSON key file
   - Set up your environment variables:
   
   ```bash
   cp .env.example .env
   # Edit .env and add your credentials path
   ```

### Running the Application

1. **Start the application**
   ```bash
   python main.py
   ```
   
   Or run directly with Streamlit:
   ```bash
   streamlit run src/ui/streamlit_app.py
   ```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

## 🏃‍♂️ How to Run It

### Quick Start (5 minutes)

1. **Clone and Navigate**
   ```bash
   git clone https://github.com/yourusername/ingredient-insight-app.git
   cd ingredient-insight-app
   ```

2. **Setup Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Google Cloud Vision** (Optional for demo mode)
   - Create a Google Cloud Project and enable Vision API
   - Download service account JSON key
   - Set environment variable: `GOOGLE_CLOUD_CREDENTIALS_PATH=path/to/your/key.json`

4. **Launch the App**
   ```bash
   streamlit run src/ui/streamlit_app.py
   ```

5. **Access the App**
   - Open your browser to `http://localhost:8504`
   - Start analyzing product images!

### Demo Mode
The app includes a demo mode that works without API credentials, allowing you to explore features with sample data.

## 📸 Screenshots

### Main Dashboard
![Main Dashboard](screenshots/main-dashboard.png)
*Modern dark-themed dashboard with animated background and glassmorphism effects. Features product upload area and real-time analysis capabilities.*

### Product Analysis Interface
![Product Analysis](screenshots/product-analysis.png)
*Clean interface showing product image upload area with drag-and-drop functionality. Sidebar contains personal preferences and allergen settings.*

### Risk Analysis Results
![Risk Analysis](screenshots/risk-analysis.png)
*Comprehensive risk assessment display with color-coded alerts, detailed ingredient breakdown, and personalized health recommendations.*

### Ingredient Details View
![Ingredient Details](screenshots/ingredient-details.png)
*Detailed ingredient analysis showing individual risk scores, allergen information, and EWG safety ratings with explanatory descriptions.*

### Personal Preferences Sidebar
![Personal Preferences](screenshots/sidebar-preferences.png)
*Customizable sidebar with allergen selection, risk sensitivity settings, and product category preferences for personalized analysis.*

### Demo Mode Interface
![Demo Mode](screenshots/demo-mode.png)
*Demo mode banner with sample product analysis, allowing users to explore features without API credentials or image upload.*

## 📸 How to Use

1. **Upload a Product Image**
   - Click "Upload a product image"
   - Select a clear photo showing the ingredients list

2. **Set Personal Preferences**
   - Use the sidebar to set your allergens
   - Adjust risk sensitivity level
   - Select preferred product categories

3. **Analyze the Product**
   - Click "🔍 Analyze Product"
   - Wait for the AI analysis to complete

4. **Review Results**
   - Check the risk summary and alerts
   - Review detailed ingredient analysis
   - Read personalized recommendations

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Google Cloud Vision API
GOOGLE_CLOUD_CREDENTIALS_PATH=path/to/your/google-credentials.json

# Optional: Set your Google Cloud Project ID
GOOGLE_CLOUD_PROJECT_ID=your-project-id

# Application settings
DEBUG=True
```

### Customization

- **Risk Thresholds**: Modify `config.py` to adjust risk scoring
- **Chemical Database**: Update `src/services/ewg_service.py` to add more chemicals
- **Allergen Lists**: Customize allergen detection in `config.py`

## 📊 Understanding Risk Levels

The app uses a 10-point risk scoring system:

- 🟢 **LOW (1-2)**: Generally safe for most people
- 🟡 **MODERATE (3-4)**: Use with awareness, monitor for sensitivities
- 🟠 **HIGH (5-7)**: Use with caution, consider alternatives
- 🔴 **SEVERE (8-10)**: Avoid, seek safer alternatives

## 🧪 Supported Product Types

- **Food Products**: Packaged foods, beverages, snacks
- **Personal Care**: Cosmetics, skincare, hygiene products
- **Household Items**: Cleaning products, detergents

## 📁 Project Structure

```
ingredient-insight-app/
├── src/
│   ├── services/
│   │   ├── vision_ai_service.py      # Google Cloud Vision integration
│   │   ├── openfoodfacts_service.py  # OpenFoodFacts API
│   │   ├── ewg_service.py            # EWG database integration
│   │   └── risk_analyzer.py          # Main analysis engine
│   ├── ui/
│   │   └── streamlit_app.py          # Streamlit web interface
│   └── utils/
├── config.py                         # Configuration settings
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🔒 Privacy & Security

- **Image Processing**: Images are processed locally and not stored permanently
- **Personal Data**: Allergen preferences are stored only in your browser session
- **API Calls**: Only ingredient text is sent to external APIs, not images
- **Data Encryption**: All API communications use HTTPS

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Development Setup

For development:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 src/
black src/

# Type checking
mypy src/
```

## 🐛 Known Issues

- OCR accuracy depends on image quality
- Some ingredients may not be in the EWG database
- Rate limiting may affect batch processing

## 🚀 Future Enhancements

- [ ] Barcode scanning for direct product lookup
- [ ] Mobile app version
- [ ] Product comparison features
- [ ] Community ratings and reviews
- [ ] Multi-language support
- [ ] Batch processing for multiple images
- [ ] Integration with more health databases

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ingredient-insight-app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ingredient-insight-app/discussions)
- **Email**: support@ingredient-insight.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Cloud Vision AI** for image processing capabilities
- **OpenFoodFacts** for comprehensive food product database
- **Environmental Working Group (EWG)** for chemical safety data
- **Streamlit** for the amazing web framework
- **Open Source Community** for various libraries and tools

## ⚠️ Disclaimer

This application provides educational information only and should not replace professional medical advice. Always consult with healthcare providers for specific health concerns and before making significant dietary or product usage changes.

## 📊 Statistics

- **Supported Ingredients**: 50,000+ from OpenFoodFacts database
- **Chemical Database**: 1,000+ toxic chemicals from EWG
- **Allergen Detection**: 11 major allergen categories
- **Risk Factors**: 20+ health concern categories

---

**Made with ❤️ by [Your Name]**

If you find this project helpful, please consider giving it a ⭐ on GitHub! 