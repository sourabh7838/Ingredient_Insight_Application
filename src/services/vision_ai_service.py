import os
import sys
import logging
from typing import List, Dict, Optional, Tuple
from google.cloud import vision
from PIL import Image
import io
import cv2
import numpy as np

# Add parent directory to path for config import
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VisionAIService:
    """Service for Google Cloud Vision AI integration"""
    
    def __init__(self):
        """Initialize the Vision AI client"""
        self.demo_mode = False
        try:
            if Config.GOOGLE_CLOUD_CREDENTIALS_PATH and Config.GOOGLE_CLOUD_CREDENTIALS_PATH.strip():
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Config.GOOGLE_CLOUD_CREDENTIALS_PATH
                self.client = vision.ImageAnnotatorClient()
                logger.info("Google Cloud Vision AI client initialized successfully")
            else:
                logger.warning("No Google Cloud credentials found - running in demo mode")
                self.demo_mode = True
                self.client = None
        except Exception as e:
            logger.warning(f"Failed to initialize Google Cloud Vision AI client: {str(e)} - running in demo mode")
            self.demo_mode = True
            self.client = None
    
    def detect_product_labels(self, image_path: str) -> List[Dict]:
        """
        Detect product labels and objects in the image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of detected labels with confidence scores
        """
        if self.demo_mode:
            # Return demo data for testing
            logger.info("Running in demo mode - returning sample labels")
            return [
                {'description': 'Food', 'score': 0.95, 'confidence': 95.0},
                {'description': 'Snack food', 'score': 0.89, 'confidence': 89.0},
                {'description': 'Package', 'score': 0.87, 'confidence': 87.0},
                {'description': 'Product', 'score': 0.85, 'confidence': 85.0}
            ]
        
        try:
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Perform label detection
            response = self.client.label_detection(image=image)
            labels = response.label_annotations
            
            if response.error.message:
                raise Exception(f'Vision API error: {response.error.message}')
            
            detected_labels = []
            for label in labels:
                detected_labels.append({
                    'description': label.description,
                    'score': label.score,
                    'confidence': label.score * 100
                })
            
            logger.info(f"Detected {len(detected_labels)} labels in the image")
            return detected_labels
            
        except Exception as e:
            logger.error(f"Error detecting labels: {str(e)}")
            return []
    
    def extract_text_from_image(self, image_path: str) -> Dict:
        """
        Extract text from image using OCR
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing extracted text and confidence
        """
        if self.demo_mode:
            # Return demo ingredients for testing
            logger.info("Running in demo mode - returning sample ingredients")
            demo_text = """INGREDIENTS: Water, Sugar, Modified Corn Starch, Citric Acid, Natural Flavors, 
            Sodium Benzoate (Preservative), Red 40, Blue 1, Vitamin C (Ascorbic Acid), 
            High Fructose Corn Syrup, Artificial Colors, Potassium Sorbate"""
            
            demo_ingredients = [
                'Water', 'Sugar', 'Modified Corn Starch', 'Citric Acid', 'Natural Flavors',
                'Sodium Benzoate', 'Red 40', 'Blue 1', 'Vitamin C', 'High Fructose Corn Syrup',
                'Artificial Colors', 'Potassium Sorbate'
            ]
            
            return {
                'text': demo_text,
                'confidence': 0.85,
                'ingredients': demo_ingredients,
                'word_count': len(demo_text.split())
            }
        
        try:
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Perform text detection
            response = self.client.text_detection(image=image)
            texts = response.text_annotations
            
            if response.error.message:
                raise Exception(f'Vision API error: {response.error.message}')
            
            if not texts:
                return {'text': '', 'confidence': 0, 'ingredients': []}
            
            # The first text annotation contains the entire text
            full_text = texts[0].description
            
            # Extract potential ingredients
            ingredients = self._extract_ingredients_from_text(full_text)
            
            result = {
                'text': full_text,
                'confidence': texts[0].score if hasattr(texts[0], 'score') else 0.9,
                'ingredients': ingredients,
                'word_count': len(full_text.split())
            }
            
            logger.info(f"Extracted {len(ingredients)} potential ingredients from text")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            return {'text': '', 'confidence': 0, 'ingredients': []}
    
    def detect_product_info(self, image_path: str) -> Dict:
        """
        Comprehensive product detection combining labels and text
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with product information
        """
        try:
            # Get labels and text simultaneously
            labels = self.detect_product_labels(image_path)
            text_info = self.extract_text_from_image(image_path)
            
            # Determine product type
            product_type = self._determine_product_type(labels)
            
            # Extract brand information
            brand = self._extract_brand_from_text(text_info['text'])
            
            return {
                'product_type': product_type,
                'brand': brand,
                'labels': labels,
                'text_info': text_info,
                'ingredients': text_info['ingredients'],
                'confidence': text_info['confidence']
            }
            
        except Exception as e:
            logger.error(f"Error detecting product info: {str(e)}")
            return {}
    
    def _extract_ingredients_from_text(self, text: str) -> List[str]:
        """Extract ingredients from OCR text"""
        ingredients = []
        
        # Common patterns for ingredient lists
        ingredient_keywords = [
            'ingredients:', 'ingredients', 'contains:', 'contains',
            'ingrédients:', 'composition:', 'composition'
        ]
        
        text_lower = text.lower()
        
        # Find ingredient section
        for keyword in ingredient_keywords:
            if keyword in text_lower:
                # Extract text after the keyword
                start_idx = text_lower.find(keyword) + len(keyword)
                ingredient_text = text[start_idx:].strip()
                
                # Split by common separators
                separators = [',', ';', '\n', '•', '·']
                for sep in separators:
                    if sep in ingredient_text:
                        ingredients = [ing.strip() for ing in ingredient_text.split(sep)]
                        break
                
                # Clean up ingredients
                ingredients = [ing for ing in ingredients if ing and len(ing) > 1]
                break
        
        return ingredients[:20]  # Limit to first 20 ingredients
    
    def _determine_product_type(self, labels: List[Dict]) -> str:
        """Determine if product is food or personal care"""
        food_keywords = [
            'food', 'snack', 'drink', 'beverage', 'fruit', 'vegetable',
            'meat', 'dairy', 'bread', 'cereal', 'candy', 'chocolate'
        ]
        
        personal_care_keywords = [
            'cosmetics', 'shampoo', 'soap', 'lotion', 'cream', 'deodorant',
            'toothpaste', 'perfume', 'skincare', 'beauty', 'hygiene'
        ]
        
        for label in labels:
            description = label['description'].lower()
            
            if any(keyword in description for keyword in food_keywords):
                return 'food'
            elif any(keyword in description for keyword in personal_care_keywords):
                return 'personal_care'
        
        return 'unknown'
    
    def _extract_brand_from_text(self, text: str) -> str:
        """Extract brand name from text (simplified approach)"""
        lines = text.split('\n')
        
        # Usually brand is in the first few lines and in caps
        for line in lines[:3]:
            if line.isupper() and len(line) > 2:
                return line.strip()
        
        return "Unknown"
    
    def preprocess_image(self, image_path: str) -> str:
        """
        Preprocess image for better OCR results
        
        Args:
            image_path: Path to the original image
            
        Returns:
            Path to the preprocessed image
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply denoising
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Enhance contrast
            enhanced = cv2.equalizeHist(denoised)
            
            # Save preprocessed image
            preprocessed_path = image_path.replace('.', '_preprocessed.')
            cv2.imwrite(preprocessed_path, enhanced)
            
            return preprocessed_path
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return image_path 