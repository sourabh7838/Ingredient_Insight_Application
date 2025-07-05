import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Google Cloud Vision AI
    GOOGLE_CLOUD_CREDENTIALS_PATH = os.getenv('GOOGLE_CLOUD_CREDENTIALS_PATH', '')
    
    # OpenFoodFacts API
    OPENFOODFACTS_BASE_URL = "https://world.openfoodfacts.org/api/v0"
    
    # EWG Database settings
    EWG_BASE_URL = "https://www.ewg.org"
    
    # Application settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    
    # Risk levels
    RISK_LEVELS = {
        'LOW': 1,
        'MODERATE': 2,
        'HIGH': 3,
        'SEVERE': 4
    }
    
    # Common allergens
    COMMON_ALLERGENS = [
        'milk', 'eggs', 'fish', 'shellfish', 'tree nuts', 'peanuts', 
        'wheat', 'soybeans', 'sesame', 'gluten', 'lactose'
    ]
    
    # Banned/restricted chemicals (sample list)
    BANNED_CHEMICALS = [
        'bisphenol a', 'bpa', 'phthalates', 'parabens', 'formaldehyde',
        'triclosan', 'triclocarban', 'hydroquinone', 'mercury', 'lead'
    ] 