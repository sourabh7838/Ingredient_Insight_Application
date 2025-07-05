#!/usr/bin/env python3
"""
Ingredient Insight App - Main Entry Point

This application analyzes food and personal care product images to identify
ingredients and assess health risks using Google Cloud Vision AI, OpenFoodFacts,
and EWG databases.
"""

import sys
import os
import logging
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    try:
        # Check if running in Streamlit
        if 'streamlit' in sys.modules:
            logger.info("Running in Streamlit mode")
            from ui.streamlit_app import IngredientInsightApp
            app = IngredientInsightApp()
            app.run()
        else:
            # Command line mode
            logger.info("Starting Ingredient Insight App...")
            
            # Check for required environment variables
            from config import Config
            if not Config.GOOGLE_CLOUD_CREDENTIALS_PATH:
                logger.error("GOOGLE_CLOUD_CREDENTIALS_PATH not set in environment")
                print("Please set up your Google Cloud Vision API credentials:")
                print("1. Create a .env file in the project root")
                print("2. Add: GOOGLE_CLOUD_CREDENTIALS_PATH=path/to/your/credentials.json")
                return
            
            # Start Streamlit app
            import subprocess
            streamlit_path = sys.executable.replace("python", "streamlit")
            if not os.path.exists(streamlit_path):
                # Try to find streamlit in the current environment
                streamlit_path = "streamlit"
            
            cmd = [streamlit_path, "run", "src/ui/streamlit_app.py"]
            logger.info(f"Starting Streamlit with command: {' '.join(cmd)}")
            subprocess.run(cmd)
    
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 