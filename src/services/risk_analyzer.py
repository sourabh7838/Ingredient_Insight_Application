import logging
import os
import sys
from typing import Dict, List, Optional
from .vision_ai_service import VisionAIService
from .openfoodfacts_service import OpenFoodFactsService
from .ewg_service import EWGService

# Add parent directory to path for config import
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskAnalyzer:
    """Main risk analysis engine that combines all services"""
    
    def __init__(self):
        """Initialize all services"""
        try:
            self.vision_service = VisionAIService()
            self.openfoodfacts_service = OpenFoodFactsService()
            self.ewg_service = EWGService()
            
            if self.vision_service.demo_mode:
                logger.info("Risk analyzer initialized successfully in DEMO MODE")
            else:
                logger.info("Risk analyzer initialized successfully with full API access")
        except Exception as e:
            logger.error(f"Error initializing risk analyzer: {str(e)}")
            raise
    
    def analyze_product_image(self, image_path: str, user_allergens: List[str] = None) -> Dict:
        """
        Comprehensive product analysis from image
        
        Args:
            image_path: Path to the product image
            user_allergens: List of user's known allergens
            
        Returns:
            Complete risk analysis
        """
        try:
            logger.info(f"Starting comprehensive analysis of {image_path}")
            
            # Step 1: Extract product information using Vision AI
            product_info = self.vision_service.detect_product_info(image_path)
            
            if not product_info:
                return self._create_error_result("Failed to extract product information from image")
            
            # Step 2: Get additional product data from OpenFoodFacts
            additional_data = None
            if product_info.get('brand') and product_info.get('brand') != 'Unknown':
                additional_data = self.openfoodfacts_service.search_product_by_name(
                    f"{product_info['brand']} {product_info.get('labels', [{}])[0].get('description', '')}"
                )
            
            # Step 3: Analyze ingredients for safety
            ingredients = product_info.get('ingredients', [])
            if not ingredients and additional_data:
                # Try to get ingredients from OpenFoodFacts
                for product in additional_data:
                    if product.get('ingredients'):
                        ingredients.extend(product['ingredients'])
                        break
            
            # Step 4: Perform risk analysis
            risk_analysis = self._perform_comprehensive_risk_analysis(
                ingredients, user_allergens, product_info.get('product_type', 'unknown')
            )
            
            # Step 5: Generate personalized alerts
            alerts = self._generate_personalized_alerts(risk_analysis, user_allergens)
            
            # Step 6: Compile final result
            result = {
                'product_info': product_info,
                'additional_data': additional_data,
                'ingredients': ingredients,
                'risk_analysis': risk_analysis,
                'alerts': alerts,
                'summary': self._generate_summary(risk_analysis, alerts),
                'recommendations': self._generate_recommendations(risk_analysis, product_info.get('product_type')),
                'timestamp': self._get_timestamp()
            }
            
            logger.info("Comprehensive analysis completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error during comprehensive analysis: {str(e)}")
            return self._create_error_result(f"Analysis failed: {str(e)}")
    
    def _perform_comprehensive_risk_analysis(self, ingredients: List[str], 
                                           user_allergens: List[str], 
                                           product_type: str) -> Dict:
        """Perform comprehensive risk analysis"""
        try:
            # EWG Safety Analysis
            ewg_analysis = self.ewg_service.get_product_safety_score(ingredients)
            
            # Allergen Analysis
            allergen_analysis = self._analyze_allergens(ingredients, user_allergens or [])
            
            # Additive Analysis
            additive_analysis = self._analyze_additives(ingredients)
            
            # Banned Substances Check
            banned_substances = self.ewg_service.check_banned_substances(ingredients)
            
            # Nutrition Analysis (if food product)
            nutrition_analysis = None
            if product_type == 'food':
                nutrition_analysis = self._analyze_nutrition_concerns(ingredients)
            
            return {
                'ewg_analysis': ewg_analysis,
                'allergen_analysis': allergen_analysis,
                'additive_analysis': additive_analysis,
                'banned_substances': banned_substances,
                'nutrition_analysis': nutrition_analysis,
                'overall_risk_score': self._calculate_overall_risk_score(
                    ewg_analysis, allergen_analysis, additive_analysis, banned_substances
                )
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive risk analysis: {str(e)}")
            return {
                'ewg_analysis': {},
                'allergen_analysis': {},
                'additive_analysis': {},
                'banned_substances': [],
                'nutrition_analysis': None,
                'overall_risk_score': {'score': 0, 'level': 'UNKNOWN'}
            }
    
    def _analyze_allergens(self, ingredients: List[str], user_allergens: List[str]) -> Dict:
        """Analyze allergens in ingredients"""
        detected_allergens = []
        potential_allergens = []
        
        for ingredient in ingredients:
            ingredient_lower = ingredient.lower()
            
            # Check against common allergens
            for allergen in Config.COMMON_ALLERGENS:
                if allergen in ingredient_lower:
                    detected_allergens.append({
                        'allergen': allergen,
                        'ingredient': ingredient,
                        'severity': 'HIGH' if allergen in user_allergens else 'MODERATE'
                    })
            
            # Check for potential allergens (cross-contamination warnings)
            if 'may contain' in ingredient_lower or 'traces of' in ingredient_lower:
                potential_allergens.append(ingredient)
        
        return {
            'detected_allergens': detected_allergens,
            'potential_allergens': potential_allergens,
            'user_allergen_matches': [
                da for da in detected_allergens 
                if da['allergen'] in user_allergens
            ],
            'allergen_risk_level': self._determine_allergen_risk_level(detected_allergens, user_allergens)
        }
    
    def _analyze_additives(self, ingredients: List[str]) -> Dict:
        """Analyze food additives and preservatives"""
        additives = []
        preservatives = []
        
        # Common additives patterns
        additive_patterns = [
            'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9',  # E-numbers
            'sodium', 'potassium', 'calcium', 'artificial', 'natural'
        ]
        
        for ingredient in ingredients:
            ingredient_lower = ingredient.lower()
            
            # Check for E-numbers and additives
            if any(pattern in ingredient_lower for pattern in additive_patterns):
                risk_level = self._assess_additive_risk(ingredient)
                additives.append({
                    'name': ingredient,
                    'type': 'additive',
                    'risk_level': risk_level
                })
            
            # Check for preservatives
            if any(term in ingredient_lower for term in ['preservative', 'sodium benzoate', 'potassium sorbate']):
                preservatives.append({
                    'name': ingredient,
                    'type': 'preservative',
                    'risk_level': self._assess_additive_risk(ingredient)
                })
        
        return {
            'additives': additives,
            'preservatives': preservatives,
            'total_additives': len(additives) + len(preservatives),
            'high_risk_additives': len([a for a in additives + preservatives if a['risk_level'] == 'HIGH'])
        }
    
    def _analyze_nutrition_concerns(self, ingredients: List[str]) -> Dict:
        """Analyze nutritional concerns for food products"""
        concerns = []
        
        # Check for high-concern ingredients
        high_sugar = any('sugar' in ing.lower() or 'syrup' in ing.lower() for ing in ingredients)
        high_sodium = any('sodium' in ing.lower() or 'salt' in ing.lower() for ing in ingredients)
        artificial_ingredients = any('artificial' in ing.lower() for ing in ingredients)
        trans_fats = any('trans' in ing.lower() or 'hydrogenated' in ing.lower() for ing in ingredients)
        
        if high_sugar:
            concerns.append({
                'type': 'high_sugar',
                'severity': 'MODERATE',
                'message': 'Contains high sugar content'
            })
        
        if high_sodium:
            concerns.append({
                'type': 'high_sodium',
                'severity': 'MODERATE',
                'message': 'Contains high sodium content'
            })
        
        if artificial_ingredients:
            concerns.append({
                'type': 'artificial_ingredients',
                'severity': 'LOW',
                'message': 'Contains artificial ingredients'
            })
        
        if trans_fats:
            concerns.append({
                'type': 'trans_fats',
                'severity': 'HIGH',
                'message': 'Contains trans fats'
            })
        
        return {
            'concerns': concerns,
            'overall_nutrition_score': self._calculate_nutrition_score(concerns)
        }
    
    def _generate_personalized_alerts(self, risk_analysis: Dict, user_allergens: List[str]) -> List[Dict]:
        """Generate personalized alerts based on risk analysis"""
        alerts = []
        
        # High-priority alerts
        if risk_analysis['banned_substances']:
            alerts.append({
                'type': 'BANNED_SUBSTANCE',
                'priority': 'CRITICAL',
                'message': f"Contains {len(risk_analysis['banned_substances'])} banned substance(s)",
                'substances': risk_analysis['banned_substances']
            })
        
        # Allergen alerts
        user_matches = risk_analysis['allergen_analysis'].get('user_allergen_matches', [])
        if user_matches:
            alerts.append({
                'type': 'ALLERGEN_ALERT',
                'priority': 'HIGH',
                'message': f"Contains allergen(s) you're sensitive to: {', '.join([m['allergen'] for m in user_matches])}",
                'allergens': user_matches
            })
        
        # EWG risk alerts
        ewg_analysis = risk_analysis['ewg_analysis']
        if ewg_analysis.get('overall_level') in ['HIGH', 'SEVERE']:
            alerts.append({
                'type': 'CHEMICAL_RISK',
                'priority': 'HIGH',
                'message': f"High chemical risk - {ewg_analysis.get('high_risk_ingredients', 0)} concerning ingredient(s)",
                'details': ewg_analysis
            })
        
        # Additive alerts
        additive_analysis = risk_analysis['additive_analysis']
        if additive_analysis.get('high_risk_additives', 0) > 0:
            alerts.append({
                'type': 'ADDITIVE_CONCERN',
                'priority': 'MODERATE',
                'message': f"Contains {additive_analysis['high_risk_additives']} high-risk additive(s)",
                'details': additive_analysis
            })
        
        return alerts
    
    def _calculate_overall_risk_score(self, ewg_analysis: Dict, allergen_analysis: Dict, 
                                    additive_analysis: Dict, banned_substances: List) -> Dict:
        """Calculate overall risk score"""
        try:
            # Base score from EWG analysis
            base_score = ewg_analysis.get('overall_score', 1)
            
            # Add penalty for banned substances
            if banned_substances:
                base_score += len(banned_substances) * 2
            
            # Add penalty for high-risk additives
            if additive_analysis.get('high_risk_additives', 0) > 0:
                base_score += additive_analysis['high_risk_additives'] * 0.5
            
            # Add penalty for allergens
            if allergen_analysis.get('user_allergen_matches'):
                base_score += len(allergen_analysis['user_allergen_matches']) * 1.5
            
            # Cap at 10
            final_score = min(base_score, 10)
            
            # Determine level
            if final_score >= 7:
                level = 'SEVERE'
            elif final_score >= 5:
                level = 'HIGH'
            elif final_score >= 3:
                level = 'MODERATE'
            else:
                level = 'LOW'
            
            return {
                'score': round(final_score, 2),
                'level': level,
                'max_score': 10
            }
            
        except Exception as e:
            logger.error(f"Error calculating overall risk score: {str(e)}")
            return {'score': 0, 'level': 'UNKNOWN', 'max_score': 10}
    
    def _generate_summary(self, risk_analysis: Dict, alerts: List[Dict]) -> str:
        """Generate a summary of the analysis"""
        overall_score = risk_analysis['overall_risk_score']
        level = overall_score.get('level', 'UNKNOWN')
        
        if level == 'SEVERE':
            return f"⚠️ HIGH RISK PRODUCT - Score: {overall_score['score']}/10. Contains concerning ingredients."
        elif level == 'HIGH':
            return f"⚡ MODERATE TO HIGH RISK - Score: {overall_score['score']}/10. Use with caution."
        elif level == 'MODERATE':
            return f"⚠️ MODERATE RISK - Score: {overall_score['score']}/10. Generally safe but monitor usage."
        else:
            return f"✅ LOW RISK - Score: {overall_score['score']}/10. Generally safe product."
    
    def _generate_recommendations(self, risk_analysis: Dict, product_type: str) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        overall_level = risk_analysis['overall_risk_score'].get('level', 'UNKNOWN')
        
        if overall_level in ['HIGH', 'SEVERE']:
            recommendations.append("Consider looking for alternative products with safer ingredients")
        
        if risk_analysis['banned_substances']:
            recommendations.append("Avoid products containing banned substances")
        
        if risk_analysis['allergen_analysis'].get('user_allergen_matches'):
            recommendations.append("This product contains allergens you're sensitive to - avoid usage")
        
        if product_type == 'food':
            nutrition_analysis = risk_analysis.get('nutrition_analysis', {})
            if nutrition_analysis and nutrition_analysis.get('concerns'):
                recommendations.append("Monitor intake due to nutritional concerns")
        
        if not recommendations:
            recommendations.append("Product appears to be generally safe based on available data")
        
        return recommendations
    
    def _create_error_result(self, error_message: str) -> Dict:
        """Create an error result"""
        return {
            'error': True,
            'message': error_message,
            'product_info': {},
            'risk_analysis': {},
            'alerts': [],
            'summary': f"❌ Analysis failed: {error_message}",
            'recommendations': ['Unable to analyze product - please try again'],
            'timestamp': self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _determine_allergen_risk_level(self, detected_allergens: List[Dict], user_allergens: List[str]) -> str:
        """Determine allergen risk level"""
        if any(da['allergen'] in user_allergens for da in detected_allergens):
            return 'HIGH'
        elif detected_allergens:
            return 'MODERATE'
        else:
            return 'LOW'
    
    def _assess_additive_risk(self, ingredient: str) -> str:
        """Assess risk level of additive"""
        ingredient_lower = ingredient.lower()
        
        # High-risk additives
        if any(term in ingredient_lower for term in ['artificial color', 'sodium nitrite', 'bha', 'bht']):
            return 'HIGH'
        elif any(term in ingredient_lower for term in ['sodium benzoate', 'potassium sorbate', 'citric acid']):
            return 'MODERATE'
        else:
            return 'LOW'
    
    def _calculate_nutrition_score(self, concerns: List[Dict]) -> int:
        """Calculate nutrition score based on concerns"""
        if not concerns:
            return 8  # Good score
        
        high_concerns = sum(1 for c in concerns if c['severity'] == 'HIGH')
        moderate_concerns = sum(1 for c in concerns if c['severity'] == 'MODERATE')
        
        base_score = 8
        base_score -= high_concerns * 3
        base_score -= moderate_concerns * 1.5
        
        return max(1, int(base_score)) 