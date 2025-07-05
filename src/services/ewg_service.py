import requests
import logging
import os
import sys
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import time

# Add parent directory to path for config import
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EWGService:
    """Service for Environmental Working Group (EWG) database integration"""
    
    def __init__(self):
        """Initialize the EWG service"""
        self.base_url = Config.EWG_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # EWG hazard levels
        self.hazard_levels = {
            1: 'LOW',
            2: 'LOW',
            3: 'MODERATE',
            4: 'MODERATE',
            5: 'HIGH',
            6: 'HIGH',
            7: 'HIGH',
            8: 'SEVERE',
            9: 'SEVERE',
            10: 'SEVERE'
        }
        
        # Known toxic chemicals database (simplified)
        self.toxic_chemicals = {
            'formaldehyde': {'hazard': 8, 'concerns': ['cancer', 'allergies', 'respiratory']},
            'parabens': {'hazard': 5, 'concerns': ['endocrine disruption', 'skin irritation']},
            'phthalates': {'hazard': 7, 'concerns': ['endocrine disruption', 'reproductive']},
            'triclosan': {'hazard': 6, 'concerns': ['endocrine disruption', 'antibiotic resistance']},
            'sodium lauryl sulfate': {'hazard': 4, 'concerns': ['skin irritation', 'eye irritation']},
            'bisphenol a': {'hazard': 8, 'concerns': ['endocrine disruption', 'developmental']},
            'mercury': {'hazard': 10, 'concerns': ['neurotoxicity', 'developmental']},
            'lead': {'hazard': 9, 'concerns': ['neurotoxicity', 'developmental']},
            'hydroquinone': {'hazard': 7, 'concerns': ['skin sensitization', 'cancer']},
            'coal tar': {'hazard': 8, 'concerns': ['cancer', 'skin irritation']},
            'sodium nitrite': {'hazard': 5, 'concerns': ['cancer', 'cardiovascular']},
            'monosodium glutamate': {'hazard': 3, 'concerns': ['headaches', 'allergic reactions']},
            'artificial colors': {'hazard': 4, 'concerns': ['hyperactivity', 'allergies']},
            'sodium benzoate': {'hazard': 4, 'concerns': ['allergies', 'hyperactivity']},
            'potassium bromate': {'hazard': 8, 'concerns': ['cancer', 'kidney damage']},
            'butylated hydroxytoluene': {'hazard': 5, 'concerns': ['allergies', 'endocrine disruption']},
            'tertiary butylhydroquinone': {'hazard': 5, 'concerns': ['nausea', 'skin irritation']},
            'carrageenan': {'hazard': 4, 'concerns': ['digestive issues', 'inflammation']},
            'high fructose corn syrup': {'hazard': 3, 'concerns': ['obesity', 'diabetes']},
            'trans fats': {'hazard': 6, 'concerns': ['cardiovascular', 'cholesterol']}
        }
    
    def analyze_ingredient_safety(self, ingredient: str) -> Dict:
        """
        Analyze ingredient safety based on EWG data
        
        Args:
            ingredient: Ingredient name to analyze
            
        Returns:
            Dictionary with safety analysis
        """
        try:
            ingredient_lower = ingredient.lower().strip()
            
            # Direct lookup in our database
            if ingredient_lower in self.toxic_chemicals:
                chem_data = self.toxic_chemicals[ingredient_lower]
                return {
                    'ingredient': ingredient,
                    'found': True,
                    'hazard_score': chem_data['hazard'],
                    'hazard_level': self.hazard_levels.get(chem_data['hazard'], 'UNKNOWN'),
                    'concerns': chem_data['concerns'],
                    'source': 'EWG Database',
                    'recommendation': self._get_recommendation(chem_data['hazard'])
                }
            
            # Check for partial matches (contains toxic compounds)
            for toxic_chem, data in self.toxic_chemicals.items():
                if toxic_chem in ingredient_lower or ingredient_lower in toxic_chem:
                    return {
                        'ingredient': ingredient,
                        'found': True,
                        'hazard_score': data['hazard'],
                        'hazard_level': self.hazard_levels.get(data['hazard'], 'UNKNOWN'),
                        'concerns': data['concerns'],
                        'source': 'EWG Database (partial match)',
                        'matched_chemical': toxic_chem,
                        'recommendation': self._get_recommendation(data['hazard'])
                    }
            
            # If not found in database, return low risk
            return {
                'ingredient': ingredient,
                'found': False,
                'hazard_score': 1,
                'hazard_level': 'LOW',
                'concerns': [],
                'source': 'Not found in EWG database',
                'recommendation': 'Generally considered safe'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing ingredient safety: {str(e)}")
            return {
                'ingredient': ingredient,
                'found': False,
                'hazard_score': 1,
                'hazard_level': 'UNKNOWN',
                'concerns': [],
                'source': 'Error during analysis',
                'recommendation': 'Unable to analyze - consult healthcare provider'
            }
    
    def analyze_ingredients_batch(self, ingredients: List[str]) -> List[Dict]:
        """
        Analyze multiple ingredients for safety
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            List of safety analyses
        """
        results = []
        
        for ingredient in ingredients:
            if ingredient.strip():
                analysis = self.analyze_ingredient_safety(ingredient)
                results.append(analysis)
                
                # Rate limiting - be respectful
                time.sleep(0.1)
        
        return results
    
    def get_product_safety_score(self, ingredients: List[str]) -> Dict:
        """
        Calculate overall product safety score
        
        Args:
            ingredients: List of ingredients
            
        Returns:
            Overall safety assessment
        """
        try:
            analyses = self.analyze_ingredients_batch(ingredients)
            
            if not analyses:
                return {
                    'overall_score': 1,
                    'overall_level': 'LOW',
                    'total_ingredients': 0,
                    'high_risk_ingredients': 0,
                    'moderate_risk_ingredients': 0,
                    'low_risk_ingredients': 0,
                    'recommendations': []
                }
            
            # Calculate scores
            total_score = sum(analysis['hazard_score'] for analysis in analyses)
            avg_score = total_score / len(analyses)
            
            # Count risk levels
            high_risk = sum(1 for a in analyses if a['hazard_level'] in ['HIGH', 'SEVERE'])
            moderate_risk = sum(1 for a in analyses if a['hazard_level'] == 'MODERATE')
            low_risk = sum(1 for a in analyses if a['hazard_level'] == 'LOW')
            
            # Determine overall level
            if high_risk > 0:
                overall_level = 'HIGH'
            elif moderate_risk > len(analyses) * 0.3:  # More than 30% moderate risk
                overall_level = 'MODERATE'
            else:
                overall_level = 'LOW'
            
            # Generate recommendations
            recommendations = self._generate_recommendations(analyses, high_risk, moderate_risk)
            
            return {
                'overall_score': round(avg_score, 2),
                'overall_level': overall_level,
                'total_ingredients': len(analyses),
                'high_risk_ingredients': high_risk,
                'moderate_risk_ingredients': moderate_risk,
                'low_risk_ingredients': low_risk,
                'recommendations': recommendations,
                'detailed_analyses': analyses
            }
            
        except Exception as e:
            logger.error(f"Error calculating product safety score: {str(e)}")
            return {
                'overall_score': 0,
                'overall_level': 'UNKNOWN',
                'total_ingredients': 0,
                'high_risk_ingredients': 0,
                'moderate_risk_ingredients': 0,
                'low_risk_ingredients': 0,
                'recommendations': ['Unable to analyze product safety'],
                'detailed_analyses': []
            }
    
    def check_banned_substances(self, ingredients: List[str]) -> List[Dict]:
        """
        Check for banned or restricted substances
        
        Args:
            ingredients: List of ingredients to check
            
        Returns:
            List of banned substances found
        """
        banned_found = []
        
        for ingredient in ingredients:
            ingredient_lower = ingredient.lower().strip()
            
            # Check against our banned chemicals list
            for banned_chem in Config.BANNED_CHEMICALS:
                if banned_chem in ingredient_lower:
                    banned_found.append({
                        'ingredient': ingredient,
                        'banned_substance': banned_chem,
                        'reason': 'Potentially harmful chemical',
                        'severity': 'HIGH'
                    })
        
        return banned_found
    
    def _get_recommendation(self, hazard_score: int) -> str:
        """Get recommendation based on hazard score"""
        if hazard_score >= 8:
            return "Avoid - High risk chemical. Consider alternatives."
        elif hazard_score >= 5:
            return "Use with caution - Moderate to high risk."
        elif hazard_score >= 3:
            return "Generally safe but monitor usage."
        else:
            return "Generally considered safe."
    
    def _generate_recommendations(self, analyses: List[Dict], high_risk: int, moderate_risk: int) -> List[str]:
        """Generate product recommendations"""
        recommendations = []
        
        if high_risk > 0:
            recommendations.append(f"⚠️ Contains {high_risk} high-risk ingredient(s). Consider alternative products.")
        
        if moderate_risk > 0:
            recommendations.append(f"⚡ Contains {moderate_risk} moderate-risk ingredient(s). Use with caution.")
        
        # Specific recommendations based on concerns
        all_concerns = []
        for analysis in analyses:
            all_concerns.extend(analysis.get('concerns', []))
        
        concern_counts = {}
        for concern in all_concerns:
            concern_counts[concern] = concern_counts.get(concern, 0) + 1
        
        # Top concerns
        if concern_counts:
            top_concerns = sorted(concern_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            for concern, count in top_concerns:
                if count >= 2:
                    recommendations.append(f"🔍 Multiple ingredients linked to {concern}")
        
        if not recommendations:
            recommendations.append("✅ Generally safe ingredient profile")
        
        return recommendations
    
    def get_safer_alternatives(self, ingredient: str) -> List[str]:
        """
        Suggest safer alternatives for high-risk ingredients
        
        Args:
            ingredient: Ingredient to find alternatives for
            
        Returns:
            List of safer alternatives
        """
        alternatives = {
            'parabens': ['phenoxyethanol', 'benzyl alcohol', 'potassium sorbate'],
            'sodium lauryl sulfate': ['sodium laureth sulfate', 'coco glucoside', 'decyl glucoside'],
            'formaldehyde': ['phenoxyethanol', 'ethylhexylglycerin', 'caprylyl glycol'],
            'phthalates': ['plant-based plasticizers', 'citric acid esters'],
            'triclosan': ['tea tree oil', 'thymol', 'benzalkonium chloride'],
            'artificial colors': ['natural colorants', 'plant-based dyes', 'mineral pigments'],
            'high fructose corn syrup': ['honey', 'maple syrup', 'coconut sugar'],
            'trans fats': ['olive oil', 'coconut oil', 'avocado oil']
        }
        
        ingredient_lower = ingredient.lower()
        
        for key, alts in alternatives.items():
            if key in ingredient_lower:
                return alts
        
        return [] 