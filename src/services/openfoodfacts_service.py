import requests
import logging
import os
import sys
from typing import Dict, List, Optional

# Add parent directory to path for config import
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenFoodFactsService:
    """Service for OpenFoodFacts API integration"""
    
    def __init__(self):
        """Initialize the OpenFoodFacts service"""
        self.base_url = Config.OPENFOODFACTS_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'IngredientInsight/1.0 (https://github.com/user/ingredient-insight)'
        })
    
    def search_product_by_name(self, product_name: str) -> List[Dict]:
        """
        Search for products by name
        
        Args:
            product_name: Name of the product to search for
            
        Returns:
            List of matching products
        """
        try:
            url = f"{self.base_url}/cgi/search.pl"
            params = {
                'search_terms': product_name,
                'search_simple': 1,
                'action': 'process',
                'json': 1,
                'page_size': 20
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            products = data.get('products', [])
            
            # Filter and clean product data
            cleaned_products = []
            for product in products:
                cleaned_product = self._clean_product_data(product)
                if cleaned_product:
                    cleaned_products.append(cleaned_product)
            
            logger.info(f"Found {len(cleaned_products)} products for '{product_name}'")
            return cleaned_products
            
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return []
    
    def get_product_by_barcode(self, barcode: str) -> Optional[Dict]:
        """
        Get product information by barcode
        
        Args:
            barcode: Product barcode
            
        Returns:
            Product information or None if not found
        """
        try:
            url = f"{self.base_url}/product/{barcode}.json"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 1:
                product = data.get('product', {})
                return self._clean_product_data(product)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting product by barcode: {str(e)}")
            return None
    
    def search_ingredients(self, ingredients: List[str]) -> Dict:
        """
        Search for information about specific ingredients
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            Dictionary with ingredient information
        """
        ingredient_info = {}
        
        for ingredient in ingredients:
            try:
                # Search for products containing this ingredient
                products = self.search_product_by_name(ingredient)
                
                # Analyze ingredient usage
                ingredient_info[ingredient] = {
                    'found_in_products': len(products),
                    'common_categories': self._get_common_categories(products),
                    'potential_allergen': self._check_allergen_status(ingredient),
                    'sample_products': products[:3]  # First 3 products as samples
                }
                
            except Exception as e:
                logger.error(f"Error searching ingredient '{ingredient}': {str(e)}")
                ingredient_info[ingredient] = {
                    'found_in_products': 0,
                    'common_categories': [],
                    'potential_allergen': False,
                    'sample_products': []
                }
        
        return ingredient_info
    
    def get_nutrition_data(self, product_data: Dict) -> Dict:
        """
        Extract nutrition information from product data
        
        Args:
            product_data: Product data from OpenFoodFacts
            
        Returns:
            Nutrition information
        """
        nutrition = {}
        
        nutriments = product_data.get('nutriments', {})
        
        # Extract key nutritional values
        nutrition_keys = [
            'energy-kcal_100g', 'fat_100g', 'saturated-fat_100g',
            'carbohydrates_100g', 'sugars_100g', 'fiber_100g',
            'proteins_100g', 'salt_100g', 'sodium_100g'
        ]
        
        for key in nutrition_keys:
            if key in nutriments:
                nutrition[key.replace('_100g', '')] = nutriments[key]
        
        # Add nutrition grade
        nutrition['nutrition_grade'] = product_data.get('nutrition_grade_fr', 'unknown')
        
        return nutrition
    
    def _clean_product_data(self, product: Dict) -> Optional[Dict]:
        """Clean and extract relevant product data"""
        try:
            # Skip products without essential information
            if not product.get('product_name') and not product.get('generic_name'):
                return None
            
            cleaned = {
                'id': product.get('_id', ''),
                'name': product.get('product_name', product.get('generic_name', 'Unknown')),
                'brand': product.get('brands', 'Unknown'),
                'categories': product.get('categories', '').split(',') if product.get('categories') else [],
                'ingredients_text': product.get('ingredients_text', ''),
                'ingredients': [ing.get('text', '') for ing in product.get('ingredients', [])],
                'allergens': product.get('allergens', '').split(',') if product.get('allergens') else [],
                'additives': product.get('additives_tags', []),
                'nutrition': self.get_nutrition_data(product),
                'image_url': product.get('image_url', ''),
                'countries': product.get('countries', ''),
                'labels': product.get('labels', '').split(',') if product.get('labels') else []
            }
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error cleaning product data: {str(e)}")
            return None
    
    def _get_common_categories(self, products: List[Dict]) -> List[str]:
        """Get common categories from product list"""
        category_counts = {}
        
        for product in products:
            for category in product.get('categories', []):
                if category.strip():
                    category_counts[category.strip()] = category_counts.get(category.strip(), 0) + 1
        
        # Return top 5 categories
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        return [cat[0] for cat in sorted_categories[:5]]
    
    def _check_allergen_status(self, ingredient: str) -> bool:
        """Check if ingredient is a common allergen"""
        ingredient_lower = ingredient.lower()
        
        for allergen in Config.COMMON_ALLERGENS:
            if allergen in ingredient_lower:
                return True
        
        return False
    
    def get_product_additives(self, product_data: Dict) -> List[Dict]:
        """
        Extract and analyze additives from product data
        
        Args:
            product_data: Product data from OpenFoodFacts
            
        Returns:
            List of additives with their risk levels
        """
        additives = []
        additive_tags = product_data.get('additives_tags', [])
        
        for tag in additive_tags:
            # Remove 'en:' prefix if present
            additive_name = tag.replace('en:', '').replace('-', ' ').title()
            
            # Determine risk level (simplified)
            risk_level = self._get_additive_risk_level(additive_name)
            
            additives.append({
                'name': additive_name,
                'tag': tag,
                'risk_level': risk_level
            })
        
        return additives
    
    def _get_additive_risk_level(self, additive_name: str) -> str:
        """Determine risk level for additive (simplified approach)"""
        # High-risk additives (sample list)
        high_risk = ['monosodium glutamate', 'sodium nitrite', 'sodium benzoate']
        moderate_risk = ['citric acid', 'sodium chloride', 'potassium sorbate']
        
        additive_lower = additive_name.lower()
        
        if any(risk in additive_lower for risk in high_risk):
            return 'HIGH'
        elif any(risk in additive_lower for risk in moderate_risk):
            return 'MODERATE'
        else:
            return 'LOW' 