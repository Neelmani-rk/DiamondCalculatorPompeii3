import streamlit as st
import requests
import json
import re
import logging
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Natural Diamonds Price Data
NATURAL_DIAMOND_PRICES = [
    {"productId": "ND+4/0", "caratPerUnit": 0.003, "itemPrice": 0.36, "size": "0.80 mm"},
    {"productId": "ND+3/0", "caratPerUnit": 0.004, "itemPrice": 0.48, "size": "0.90 mm"},
    {"productId": "ND+2/0", "caratPerUnit": 0.005, "itemPrice": 0.60, "size": "1.05 mm"},
    {"productId": "ND+G0", "caratPerUnit": 0.006, "itemPrice": 0.744, "size": "1.10 mm"},
    {"productId": "ND+1", "caratPerUnit": 0.007, "itemPrice": 0.864, "size": "1.15 mm"},
    {"productId": "ND+1.5", "caratPerUnit": 0.008, "itemPrice": 0.912, "size": "1.20 mm"},
    {"productId": "ND+2", "caratPerUnit": 0.009, "itemPrice": 1.08, "size": "1.25 mm"},
    {"productId": "ND+2.5", "caratPerUnit": 0.010, "itemPrice": 1.20, "size": "1.30 mm"},
    {"productId": "ND+3", "caratPerUnit": 0.011, "itemPrice": 1.32, "size": "1.35 mm"},
    {"productId": "ND+3.5", "caratPerUnit": 0.013, "itemPrice": 1.50, "size": "1.40 mm"},
    {"productId": "ND+4", "caratPerUnit": 0.014, "itemPrice": 1.68, "size": "1.45 mm"},
    {"productId": "ND+4.5", "caratPerUnit": 0.015, "itemPrice": 1.80, "size": "1.50 mm"},
    {"productId": "ND+5", "caratPerUnit": 0.016, "itemPrice": 1.92, "size": "1.55 mm"},
    {"productId": "ND+5.5", "caratPerUnit": 0.018, "itemPrice": 2.16, "size": "1.60 mm"},
    {"productId": "ND+6", "caratPerUnit": 0.022, "itemPrice": 2.64, "size": "1.70 mm"},
    {"productId": "ND+6.5", "caratPerUnit": 0.026, "itemPrice": 3.12, "size": "1.80 mm"},
    {"productId": "ND+7", "caratPerUnit": 0.033, "itemPrice": 3.96, "size": "1.90 mm"},
    {"productId": "ND+7.5", "caratPerUnit": 0.035, "itemPrice": 4.20, "size": "2.00 mm"},
    {"productId": "ND+8", "caratPerUnit": 0.040, "itemPrice": 4.80, "size": "2.10 mm"},
    {"productId": "ND+8.5", "caratPerUnit": 0.045, "itemPrice": 5.40, "size": "2.20 mm"},
    {"productId": "ND+9", "caratPerUnit": 0.051, "itemPrice": 6.12, "size": "2.30 mm"},
    {"productId": "ND+9.5", "caratPerUnit": 0.058, "itemPrice": 6.96, "size": "2.40 mm"},
    {"productId": "ND+10", "caratPerUnit": 0.067, "itemPrice": 8.04, "size": "2.50 mm"},
    {"productId": "ND+10.5", "caratPerUnit": 0.073, "itemPrice": 8.76, "size": "2.60 mm"},
    {"productId": "ND+11", "caratPerUnit": 0.083, "itemPrice": 11.205, "size": "2.70 mm"},
    {"productId": "ND+11.5", "caratPerUnit": 0.091, "itemPrice": 12.285, "size": "2.80 mm"},
    {"productId": "ND+12", "caratPerUnit": 0.105, "itemPrice": 14.175, "size": "2.90 mm"},
    {"productId": "ND+12.5", "caratPerUnit": 0.114, "itemPrice": 15.39, "size": "3.00 mm"},
    {"productId": "ND+13", "caratPerUnit": 0.125, "itemPrice": 16.875, "size": "3.10 mm"},
    {"productId": "ND+13.5", "caratPerUnit": 0.135, "itemPrice": 18.225, "size": "3.20 mm"},
    {"productId": "ND+14", "caratPerUnit": 0.145, "itemPrice": 19.575, "size": "3.30 mm"},
    {"productId": "ND+14.5", "caratPerUnit": 0.165, "itemPrice": 22.275, "size": "3.40 mm"},
    {"productId": "ND.20", "caratPerUnit": 0.200, "itemPrice": 30.00, "size": "3.5-3.8 mm"},
    {"productId": "ND.25", "caratPerUnit": 0.250, "itemPrice": 37.50, "size": "3.8-4.1 mm"},
    {"productId": "ND.33", "caratPerUnit": 0.330, "itemPrice": 49.50, "size": "4.1-4.4 mm"},
    {"productId": "ND.40", "caratPerUnit": 0.400, "itemPrice": 60.00, "size": "4.4-4.7 mm"},
    {"productId": "ND.50", "caratPerUnit": 0.500, "itemPrice": 125.00, "size": "5.0 mm"},
    {"productId": "ND.62", "caratPerUnit": 0.620, "itemPrice": 155.00, "size": "5.37 mm"},
    {"productId": "ND.75", "caratPerUnit": 0.750, "itemPrice": 131.25, "size": "5.75 mm"},
    {"productId": "ND.87", "caratPerUnit": 0.875, "itemPrice": 240.625, "size": "6.12 mm"},
    {"productId": "ND1.00", "caratPerUnit": 1.000, "itemPrice": 500.00, "size": "6.5 mm"},
    {"productId": "ND1.25", "caratPerUnit": 1.250, "itemPrice": 625.00, "size": "6.8 mm"},
    {"productId": "ND1.50", "caratPerUnit": 1.500, "itemPrice": 900.00, "size": "7.3 mm"},
    {"productId": "ND2.00", "caratPerUnit": 2.000, "itemPrice": 1600.00, "size": "8.0 mm"}
]

# Lab Grown Diamonds Price Data
LAB_GROWN_DIAMOND_PRICES = [
    {"productId": "LD+4/0", "caratPerUnit": 0.003, "itemPrice": 0.327, "size": "0.80 mm"},
    {"productId": "LD+3/0", "caratPerUnit": 0.004, "itemPrice": 0.436, "size": "0.90 mm"},
    {"productId": "LD+2/0", "caratPerUnit": 0.005, "itemPrice": 0.545, "size": "1.05 mm"},
    {"productId": "LD+0", "caratPerUnit": 0.006, "itemPrice": 0.676, "size": "1.10 mm"},
    {"productId": "LD+1", "caratPerUnit": 0.007, "itemPrice": 0.785, "size": "1.15 mm"},
    {"productId": "LD1.5", "caratPerUnit": 0.008, "itemPrice": 0.828, "size": "1.20 mm"},
    {"productId": "LD+2", "caratPerUnit": 0.009, "itemPrice": 0.504, "size": "1.25 mm"},
    {"productId": "LD+2.5", "caratPerUnit": 0.010, "itemPrice": 0.560, "size": "1.30 mm"},
    {"productId": "LD+3", "caratPerUnit": 0.011, "itemPrice": 0.616, "size": "1.35 mm"},
    {"productId": "LD+3.5", "caratPerUnit": 0.013, "itemPrice": 0.700, "size": "1.40 mm"},
    {"productId": "LD+4", "caratPerUnit": 0.014, "itemPrice": 0.784, "size": "1.45 mm"},
    {"productId": "LD+4.5", "caratPerUnit": 0.015, "itemPrice": 0.840, "size": "1.50 mm"},
    {"productId": "LD+5", "caratPerUnit": 0.016, "itemPrice": 0.896, "size": "1.55 mm"},
    {"productId": "LD+5.5", "caratPerUnit": 0.018, "itemPrice": 1.008, "size": "1.60 mm"},
    {"productId": "LD+6", "caratPerUnit": 0.022, "itemPrice": 1.232, "size": "1.70 mm"},
    {"productId": "LD+6.5", "caratPerUnit": 0.026, "itemPrice": 0.910, "size": "1.80 mm"},
    {"productId": "LD+7", "caratPerUnit": 0.033, "itemPrice": 1.155, "size": "1.90 mm"},
    {"productId": "LD+7.5", "caratPerUnit": 0.035, "itemPrice": 1.225, "size": "2.00 mm"},
    {"productId": "LD+8", "caratPerUnit": 0.040, "itemPrice": 1.400, "size": "2.10 mm"},
    {"productId": "LD+8.5", "caratPerUnit": 0.045, "itemPrice": 1.575, "size": "2.20 mm"},
    {"productId": "LD+9", "caratPerUnit": 0.051, "itemPrice": 1.785, "size": "2.30 mm"},
    {"productId": "LD+9.5", "caratPerUnit": 0.058, "itemPrice": 2.030, "size": "2.40 mm"},
    {"productId": "LD+10", "caratPerUnit": 0.067, "itemPrice": 2.345, "size": "2.50 mm"},
    {"productId": "LD+10.5", "caratPerUnit": 0.073, "itemPrice": 2.555, "size": "2.60 mm"},
    {"productId": "LD+11", "caratPerUnit": 0.083, "itemPrice": 2.905, "size": "2.70 mm"},
    {"productId": "LD+11.5", "caratPerUnit": 0.091, "itemPrice": 3.185, "size": "2.80 mm"},
    {"productId": "LD+12", "caratPerUnit": 0.105, "itemPrice": 3.675, "size": "2.90 mm"},
    {"productId": "LD+12.5", "caratPerUnit": 0.114, "itemPrice": 3.990, "size": "3.00 mm"},
    {"productId": "LD+13", "caratPerUnit": 0.125, "itemPrice": 4.375, "size": "3.10 mm"},
    {"productId": "LD+13.5", "caratPerUnit": 0.135, "itemPrice": 4.725, "size": "3.20 mm"},
    {"productId": "LD+14", "caratPerUnit": 0.145, "itemPrice": 5.075, "size": "3.30 mm"},
    {"productId": "LD+14.5", "caratPerUnit": 0.165, "itemPrice": 5.775, "size": "3.40 mm"},
    {"productId": "LD.20", "caratPerUnit": 0.200, "itemPrice": 10.000, "size": "3.5-3.8 mm"},
    {"productId": "LD.25", "caratPerUnit": 0.250, "itemPrice": 13.750, "size": "3.8-4.1 mm"},
    {"productId": "LD.33", "caratPerUnit": 0.330, "itemPrice": 18.480, "size": "4.1-4.4 mm"},
    {"productId": "LD.40", "caratPerUnit": 0.400, "itemPrice": 22.400, "size": "4.4-4.7 mm"},
    {"productId": "LD.50", "caratPerUnit": 0.500, "itemPrice": 36.000, "size": "5.0 mm"},
    {"productId": "LD.62", "caratPerUnit": 0.620, "itemPrice": 44.640, "size": "5.37 mm"},
    {"productId": "LD.75", "caratPerUnit": 0.750, "itemPrice": 54.000, "size": "5.75 mm"},
    {"productId": "LD.87", "caratPerUnit": 0.875, "itemPrice": 63.000, "size": "6.12 mm"},
    {"productId": "LD1.00", "caratPerUnit": 1.000, "itemPrice": 75.000, "size": "6.5 mm"},
    {"productId": "LD1.25", "caratPerUnit": 1.250, "itemPrice": 93.750, "size": "6.8 mm"},
    {"productId": "LD1.50", "caratPerUnit": 1.500, "itemPrice": 112.50, "size": "7.3 mm"},
    {"productId": "LD2.00", "caratPerUnit": 2.000, "itemPrice": 170.000, "size": "8.0 mm"}
]

# Configuration
class Config:
    CA_BASE_URL = "https://api.channeladvisor.com/v1"
    CA_CLIENT_ID = "1aad9geoo60y5e8z0jr496fwcq1ybti4"
    CA_CLIENT_SECRET = "jHlILAQ-jU22FwsWtfZ1zQ"
    CA_REFRESH_TOKEN = "mKJx-l2zTVtY8YFQ38oN6tpMIPTdBgxqql191I1KjzI"
    
    GEMINI_API_KEY = "AIzaSyC6zsmC4Dj6L8zsPA2Byw59fR1OQsQiPM4"
    GEMINI_MODEL = "gemini-2.0-flash"
    GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    
    CONVERSION_FACTOR = 0.2

class DiamondAnalysisService:
    """Service for comprehensive diamond analysis with strict type separation and exact value matching"""
    
    def __init__(self):
        self.natural_data = NATURAL_DIAMOND_PRICES
        self.lab_data = LAB_GROWN_DIAMOND_PRICES
        # Create sorted lists for next higher value lookup
        self.natural_sorted = sorted(self.natural_data, key=lambda x: x['caratPerUnit'])
        self.lab_sorted = sorted(self.lab_data, key=lambda x: x['caratPerUnit'])
    
    def get_pricing_database_text(self) -> str:
        """Convert complete pricing database to text for Gemini prompts"""
        text = "COMPLETE NATURAL DIAMOND PRICING DATABASE:\n"
        for item in self.natural_data:
            text += f"{item['productId']}: caratPerUnit={item['caratPerUnit']}, itemPrice=${item['itemPrice']}, size={item['size']}\n"
        
        text += "\nCOMPLETE LAB GROWN DIAMOND PRICING DATABASE:\n"
        for item in self.lab_data:
            text += f"{item['productId']}: caratPerUnit={item['caratPerUnit']}, itemPrice=${item['itemPrice']}, size={item['size']}\n"
        
        return text
    
    def find_exact_or_next_higher(self, carat_value: float, diamond_type: str) -> Dict[str, Any]:
        """Find exact match or next higher value in dataset"""
        dataset = self.natural_sorted if diamond_type == 'Natural Diamond' else self.lab_sorted
        
        # First try exact match
        for item in dataset:
            if abs(item['caratPerUnit'] - carat_value) < 0.001:  # Very close match
                return item
        
        # Find next higher value
        for item in dataset:
            if item['caratPerUnit'] > carat_value:
                return item
        
        # If no higher value found, return the highest
        return dataset[-1] if dataset else {}
    
    def calculate_total_carat_from_picks(self, data: Dict[str, Any]) -> float:
        """Calculate total carat from all pick fields strictly"""
        total_carat = 0
        
        for pick_field in ['Pick 1', 'Pick 2', 'Pick 3']:
            pick_value = data.get(pick_field, '')
            if pick_value and pick_value != 'Not Available':
                total_carat += self._parse_pick_field_carat(pick_value, data)
        
        return total_carat
    
    def _parse_pick_field_carat(self, pick_value: str, data: Dict[str, Any]) -> float:
        """Parse carat from individual pick field"""
        total = 0
        
        # Determine diamond type from product context
        title = data.get('Title', '').lower()
        main_stone = data.get('Main Stone', '').lower()
        
        diamond_type = 'Lab Grown' if 'lab grown' in title or 'lab grown' in main_stone else 'Natural Diamond'
        
        # Parse entries like "29+7, 58+6"
        entries = re.findall(r'(\d+)\+(\w+)', pick_value)
        
        for qty_str, product_num in entries:
            try:
                qty = int(qty_str)
                prefix = 'LD' if diamond_type == 'Lab Grown' else 'ND'
                product_id = f"{prefix}+{product_num}"
                
                # Get exact carat per unit from database
                carat_per_unit = self._get_carat_per_unit_by_id(product_id)
                if carat_per_unit:
                    total += qty * carat_per_unit
            except:
                continue
        
        return total
    
    def _get_carat_per_unit_by_id(self, product_id: str) -> float:
        """Get carat per unit by exact product ID"""
        dataset = self.natural_data if product_id.startswith('ND') else self.lab_data
        
        for item in dataset:
            if item['productId'] == product_id:
                return item['caratPerUnit']
        
        return 0

class DiamondPricingService:
    """Enhanced service for diamond pricing with strict type separation"""
    
    def __init__(self):
        self.natural_data = NATURAL_DIAMOND_PRICES
        self.lab_data = LAB_GROWN_DIAMOND_PRICES
        self.analysis_service = DiamondAnalysisService()
    
    def get_pricing_data_by_type(self, diamond_type: str) -> List[Dict[str, Any]]:
        """Get pricing data strictly by diamond type"""
        if diamond_type == 'Natural Diamond':
            return self.natural_data
        elif diamond_type == 'Lab Grown':
            return self.lab_data
        else:
            # Default to Natural Diamond if type is unclear
            return self.natural_data
    
    def find_closest_or_next_higher_match(self, carat_value: float, diamond_type: str) -> Dict[str, Any]:
        """Find exact match or next higher value using strict type separation"""
        return self.analysis_service.find_exact_or_next_higher(carat_value, diamond_type)
    
    def calculate_comprehensive_pricing(self, diamonds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate pricing with comprehensive rules"""
        processed_diamonds = []
        
        for diamond in diamonds:
            processed_diamond = diamond.copy()
            
            diamond_type = diamond.get('diamondType', 'Natural Diamond')
            quantity = diamond.get('quantity', 1)
            
            # Handle MM format vs standard format
            if diamond.get('width'):
                # MM format - convert to carat
                width = diamond.get('width', 0)
                closest_match = self._find_closest_mm_match(width, diamond_type)
                unit_price = closest_match.get('itemPrice', 0)
                carat_per_unit = closest_match.get('caratPerUnit', 0)
            else:
                # Standard format
                carat_value_str = str(diamond.get('carat_value', ''))
                carat_value = self._parse_carat_string(carat_value_str)
                
                closest_match = self.find_closest_or_next_higher_match(carat_value, diamond_type)
                unit_price = closest_match.get('itemPrice', 0)
                carat_per_unit = closest_match.get('caratPerUnit', 0)
            
            total_price = unit_price * quantity
            total_carat = carat_per_unit * quantity
            
            processed_diamond.update({
                'unit_price': unit_price,
                'total_price': total_price,
                'TotalCarat': round(total_carat, 3),
                'ProductId': closest_match.get('productId', 'N/A'),
                'matched_carat_per_unit': carat_per_unit
            })
            
            processed_diamonds.append(processed_diamond)
        
        return processed_diamonds
    
    def _find_closest_mm_match(self, width: float, diamond_type: str) -> Dict[str, Any]:
        """Find closest match for MM format diamonds"""
        dataset = self.get_pricing_data_by_type(diamond_type)
        
        best_match = None
        min_diff = float('inf')
        
        for item in dataset:
            size_str = item['size']
            # Extract numeric value from size (e.g., "1.70 mm" -> 1.70)
            size_match = re.search(r'(\d+\.?\d*)', size_str)
            if size_match:
                size_value = float(size_match.group(1))
                diff = abs(size_value - width)
                if diff < min_diff:
                    min_diff = diff
                    best_match = item
        
        return best_match or {}
    
    def _parse_carat_string(self, carat_str: str) -> float:
        """Parse carat string to float"""
        try:
            if '/' in carat_str:
                parts = carat_str.split('/')
                return float(parts[0]) / float(parts[1])
            else:
                return float(carat_str)
        except:
            return 0.0

class ChannelAdvisorService:
    def __init__(self):
        self.access_token = None
        self.base_url = Config.CA_BASE_URL
        
    def get_access_token(self) -> Optional[str]:
        """Get OAuth access token"""
        try:
            token_url = "https://api.channeladvisor.com/oauth2/token"
            payload = {
                'client_id': Config.CA_CLIENT_ID,
                'client_secret': Config.CA_CLIENT_SECRET,
                'grant_type': 'refresh_token',
                'refresh_token': Config.CA_REFRESH_TOKEN
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            response = requests.post(token_url, data=payload, headers=headers)
            if response.status_code == 200:
                self.access_token = response.json().get('access_token')
                return self.access_token
            return None
        except Exception as e:
            logger.error(f"Error getting access token: {e}")
            return None
    
    def get_product_id_by_sku(self, sku: str) -> Optional[str]:
        """Get product ID by SKU"""
        if not self.access_token:
            self.get_access_token()
            
        try:
            url = f"{self.base_url}/Products"
            params = {'$filter': f"Sku eq '{sku}'", '$select': 'ID,Sku'}
            headers = {'Authorization': f'Bearer {self.access_token}'}
            
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('value') and len(data['value']) > 0:
                    return str(data['value'][0]['ID'])
            return None
        except Exception as e:
            logger.error(f"Error fetching product ID: {e}")
            return None
    
    def fetch_product_details(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Fetch product details by ID"""
        if not self.access_token:
            self.get_access_token()
            
        try:
            url = f"{self.base_url}/Products({product_id})"
            params = {'$expand': 'Attributes,Images'}
            headers = {'Authorization': f'Bearer {self.access_token}'}
            
            response = requests.get(url, params=params, headers=headers)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Error fetching product details: {e}")
            return None

class GeminiService:
    def __init__(self):
        self.api_url = Config.GEMINI_API_URL
        self.analysis_service = DiamondAnalysisService()
        self.pricing_service = DiamondPricingService()
    
    def get_product_understanding(self, data: Dict[str, Any]) -> Optional[str]:
        """Generate product understanding with complete pricing database context"""
        prompt = self._create_comprehensive_understanding_prompt(data)
        
        request_body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "topK": 1,
                "topP": 0.1,
                "maxOutputTokens": 1024,
            }
        }
        
        try:
            response = requests.post(self.api_url, json=request_body)
            if response.status_code == 200:
                response_data = response.json()
                if (response_data.get('candidates') and 
                    response_data['candidates'][0].get('content') and
                    response_data['candidates'][0]['content'].get('parts') and
                    response_data['candidates'][0]['content']['parts'][0].get('text')):
                    return response_data['candidates'][0]['content']['parts'][0]['text'].strip()
            return None
        except Exception as e:
            logger.error(f"Error in Gemini understanding: {e}")
            return None
    
    def _create_comprehensive_understanding_prompt(self, data: Dict[str, Any]) -> str:
        """Create comprehensive understanding prompt with complete database and strict rules"""
        
        # Get complete pricing database
        pricing_database = self.analysis_service.get_pricing_database_text()
        
        # Calculate totals for comparison
        calculated_total = self.analysis_service.calculate_total_carat_from_picks(data)
        exact_total = float(data.get('Exact Carat Total Weight', 0))
        
        # Pre-analyze pick fields
        pick_analysis = self._pre_analyze_picks(data)
        
        prompt = f"""You are an expert jewelry analyst with access to the complete diamond pricing database. Analyze this jewelry product focusing ONLY on diamond details with STRICT type separation and exact value matching.

COMPLETE DIAMOND PRICING DATABASE:
{pricing_database}

STRICT ANALYSIS RULES:
1. NATURAL DIAMOND vs LAB GROWN: Use ONLY the respective dataset - never mix them
2. EXACT VALUE MATCHING: If exact caratPerUnit not found, use the NEXT HIGHER value from the dataset
3. PICK FIELD PRIORITY: Extract from Pick 1, Pick 2, Pick 3 fields STRICTLY
4. TOTAL CARAT VALIDATION: Compare calculated total with Exact Carat Total Weight
5. MISSING VALUES: If significant difference, consider Title and Description to adjust

PRE-CALCULATED ANALYSIS:
{pick_analysis}

CALCULATED TOTALS:
- Calculated from Picks: {calculated_total:.3f} carats
- Exact Carat Total Weight: {exact_total} carats
- Difference: {abs(calculated_total - exact_total):.3f} carats

EXAMPLE CALCULATIONS (using database):
- "29+7" = 29 diamonds × LD+7 (caratPerUnit: 0.033) = {29 * 0.033:.3f} carats
- "58+6" = 58 diamonds × LD+6 (caratPerUnit: 0.022) = {58 * 0.022:.3f} carats

PRODUCT INFORMATION:
{json.dumps(data, indent=2)}

Provide comprehensive analysis explaining:
- Exact diamond calculations using ONLY the appropriate dataset (Natural or Lab Grown)
- Precise Pick field breakdown with database caratPerUnit values
- Total carat calculation vs stated Exact Carat Total Weight
- Cost analysis using actual itemPrice values from the correct dataset
- Address discrepancies and suggest adjustments if needed

Use the complete pricing database for ALL calculations. Be precise and professional."""

        return prompt
    
    def _pre_analyze_picks(self, data: Dict[str, Any]) -> str:
        """Pre-analyze pick fields with database lookup"""
        analysis_parts = []
        
        # Determine diamond type
        title = data.get('Title', '').lower()
        main_stone = data.get('Main Stone', '').lower()
        diamond_type = 'Lab Grown' if 'lab grown' in title or 'lab grown' in main_stone else 'Natural Diamond'
        
        for pick_field in ['Pick 1', 'Pick 2', 'Pick 3']:
            pick_value = data.get(pick_field, '')
            if pick_value and pick_value != 'Not Available':
                entries = re.findall(r'(\d+)\+(\w+)', pick_value)
                
                for qty_str, product_num in entries:
                    try:
                        qty = int(qty_str)
                        prefix = 'LD' if diamond_type == 'Lab Grown' else 'ND'
                        product_id = f"{prefix}+{product_num}"
                        
                        # Get from database
                        carat_per_unit = self.analysis_service._get_carat_per_unit_by_id(product_id)
                        if carat_per_unit:
                            total_carat = qty * carat_per_unit
                            analysis_parts.append(
                                f'{pick_field}: "{qty}+{product_num}" = {qty} diamonds × {product_id} '
                                f'(caratPerUnit: {carat_per_unit}) = {total_carat:.3f} carats'
                            )
                    except:
                        continue
        
        return "PICK FIELD DATABASE ANALYSIS:\n" + "\n".join(analysis_parts) if analysis_parts else "No valid pick entries found."
    
    def process_with_gemini(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process with comprehensive diamond analysis"""
        prompt = self._create_extraction_prompt(data)
        
        request_body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "topK": 1,
                "topP": 0.1,
                "maxOutputTokens": 2048,
            }
        }
        
        try:
            response = requests.post(self.api_url, json=request_body)
            if response.status_code == 200:
                response_data = response.json()
                if (response_data.get('candidates') and 
                    response_data['candidates'][0].get('content') and
                    response_data['candidates'][0]['content'].get('parts') and
                    response_data['candidates'][0]['content']['parts'][0].get('text')):
                    
                    generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
                    json_match = re.search(r'\{[\s\S]*\}', generated_text)
                    
                    if json_match:
                        result = json.loads(json_match.group(0))
                        result = self._calculate_metal_weight(result, data)
                        result = self._process_diamonds_with_database(result, data)
                        return result
            return None
        except Exception as e:
            logger.error(f"Error in Gemini processing: {e}")
            return None
    
    def _create_extraction_prompt(self, data: Dict[str, Any]) -> str:
        """Create extraction prompt with complete database context"""
        
        pricing_database = self.analysis_service.get_pricing_database_text()
        
        return f"""You are an expert in jewelry data extraction with access to the complete diamond pricing database. Extract DIAMOND details ONLY using strict type separation and exact value matching.

COMPLETE DIAMOND PRICING DATABASE:
{pricing_database}

STRICT EXTRACTION RULES:
1. DIAMOND TYPE SEPARATION: Use ONLY Natural Diamond OR Lab Grown - never mix
2. EXACT VALUE MATCHING: If exact caratPerUnit not found, use NEXT HIGHER value
3. PICK FIELD PRIORITY: Extract from Pick 1, Pick 2, Pick 3 STRICTLY
4. DATABASE VALIDATION: All calculations must reference the pricing database above

EXTRACTION LOGIC:
For "29+7" format:
- 29 = quantity of diamonds
- 7 = carat_value (refers to LD+7 or ND+7 in database)
- Extract: quantity=29, carat_value="7", diamondType="Lab Grown"
- Use LD+7 from database: caratPerUnit=0.033, itemPrice=1.155

Expected JSON Output:
{{
  "metal_purity": "string",
  "metal_weight": "string",
  "stone_used": "Yes/No",
  "diamond_details": {{
    "diamonds": [
      {{
        "diamondType": "string",
        "quantity": number,
        "carat_value": "string",
        "database_reference": "string",
        "calculated_carat_per_unit": number,
        "calculated_item_price": number
      }}
    ],
    "total_calculated_carat": number,
    "database_analysis": "string"
  }},
  "gemstone_details": null
}}

PRODUCT DATA:
{json.dumps(data, indent=2)}

IMPORTANT:
1. Extract ALL diamond entries from Pick fields
2. For each diamond, include database_reference showing which productId was used
3. Include calculated_carat_per_unit and calculated_item_price from database lookup
4. Calculate total_calculated_carat as sum of (quantity × calculated_carat_per_unit)
5. Provide database_analysis comparing with Exact Carat Total Weight
6. Use STRICT type separation - Natural Diamond OR Lab Grown only
7. Return only the JSON with accurate database-based calculations."""
        
    def _process_diamonds_with_database(self, result: Dict[str, Any], original_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process diamonds with comprehensive database integration"""
        if result.get('diamond_details') and result['diamond_details'].get('diamonds'):
            processed_diamonds = self.pricing_service.calculate_comprehensive_pricing(
                result['diamond_details']['diamonds']
            )
            
            # Add comprehensive analysis
            total_calculated = sum(d.get('TotalCarat', 0) for d in processed_diamonds)
            exact_total = float(original_data.get('Exact Carat Total Weight', 0))
            
            database_analysis = f"Database Calculation: {total_calculated:.3f} carats vs Exact Total: {exact_total} carats"
            difference = abs(total_calculated - exact_total)
            
            if difference > 0.1:
                database_analysis += f" (Significant difference: {difference:.3f} carats - consider Title/Description)"
            else:
                database_analysis += " (Good match - using Pick field data)"
            
            result['diamond_details']['diamonds'] = processed_diamonds
            result['diamond_details']['total_calculated_carat'] = round(total_calculated, 3)
            result['diamond_details']['database_analysis'] = database_analysis
            result['diamond_details']['exact_total_weight'] = exact_total
        
        return result
    
    def _calculate_metal_weight(self, result: Dict[str, Any], original_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate metal weight if needed"""
        metal_weight = result.get('metal_weight')
        if not metal_weight or (isinstance(metal_weight, str) and metal_weight.strip().upper() == 'N/A'):
            try:
                original_weight = float(original_data.get('Weight', 0))
                exact_carat_weight = float(original_data.get('Exact Carat Total Weight', 0))
                
                if original_weight > 0 and exact_carat_weight >= 0:
                    calculated_metal_weight = original_weight - (exact_carat_weight * Config.CONVERSION_FACTOR)
                    result['metal_weight'] = f"{calculated_metal_weight:.2f}"
                else:
                    result['metal_weight'] = ""
            except (ValueError, TypeError):
                result['metal_weight'] = ""
        
        return result

def main():
    st.set_page_config(
        page_title="Complete Diamond BOM Calculator",
        page_icon="💎",
        layout="wide"
    )
    
    st.title("💎 Complete Diamond BOM Calculator with Strict Type Separation")
    st.markdown("### Comprehensive Diamond Analysis Using Complete Pricing Database with Exact Value Matching")
    
    # Initialize services
    if 'ca_service' not in st.session_state:
        st.session_state.ca_service = ChannelAdvisorService()
    
    if 'gemini_service' not in st.session_state:
        st.session_state.gemini_service = GeminiService()
    
    if 'pricing_service' not in st.session_state:
        st.session_state.pricing_service = DiamondPricingService()
    
    if 'analysis_service' not in st.session_state:
        st.session_state.analysis_service = DiamondAnalysisService()
    
    # Input section
    with st.container():
        st.subheader("📝 Product Input")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            sku_input = st.text_input(
                "Enter SKU:",
                placeholder="e.g., EWB2153.7",
                help="Enter the product SKU to retrieve details"
            )
        
        with col2:
            st.write("")
            search_button = st.button("🔍 Search Product", type="primary")
    
    # Display database info
    with st.expander("🔍 View Complete Diamond Pricing Database"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Natural Diamond Prices:**")
            st.dataframe(NATURAL_DIAMOND_PRICES, use_container_width=True)
        with col2:
            st.markdown("**Lab Grown Diamond Prices:**")
            st.dataframe(LAB_GROWN_DIAMOND_PRICES, use_container_width=True)
        
        st.info(f"**Database Coverage:** {len(NATURAL_DIAMOND_PRICES)} Natural + {len(LAB_GROWN_DIAMOND_PRICES)} Lab Grown diamonds with complete pricing")
    
    # Process button click
    if search_button and sku_input:
        with st.spinner("Retrieving product information..."):
            # Get Product ID
            product_id = st.session_state.ca_service.get_product_id_by_sku(sku_input)
            
            if not product_id:
                st.error(f"❌ Product not found for SKU: {sku_input}")
                return
            
            st.success(f"✅ Found Product ID: {product_id}")
            
            # Get Product Details
            product_details = st.session_state.ca_service.fetch_product_details(product_id)
            
            if not product_details:
                st.error("❌ Failed to retrieve product details")
                return
            
            # Display Results
            display_product_information(product_details, sku_input)
            
            # Comprehensive Diamond Understanding
            with st.spinner("Analyzing diamonds with complete database and strict rules..."):
                understanding_text = get_comprehensive_product_understanding(product_details)
                if understanding_text:
                    display_comprehensive_understanding(understanding_text, sku_input)
            
            # Complete Diamond Processing
            with st.spinner("Processing with AI using complete database and strict type separation..."):
                processed_data = process_comprehensive_product_data(product_details)
                if processed_data:
                    display_comprehensive_analysis(processed_data)

def display_product_information(data: Dict[str, Any], sku: str):
    """Display comprehensive product information"""
    st.subheader("📋 Product Information")
    
    basic = data if not data.get('basic') else data['basic']
    attributes = data.get('Attributes', []) or data.get('attributes', {}).get('value', [])
    
    attr_dict = {}
    for attr in attributes:
        attr_dict[attr.get('Name', '')] = attr.get('Value', '')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Basic Information")
        info_data = {
            "SKU": sku,
            "Product ID": basic.get('ID', 'N/A'),
            "Title": basic.get('Title', 'N/A'),
            "Description": basic.get('Description', 'N/A')[:200] + "..." if len(basic.get('Description', '')) > 200 else basic.get('Description', 'N/A')
        }
        
        for key, value in info_data.items():
            st.text(f"{key}: {value}")
    
    with col2:
        st.markdown("#### Material Details")
        material_data = {
            "Pick 1": attr_dict.get('Pick 1', 'Not Available'),
            "Pick 2": attr_dict.get('Pick 2', 'Not Available'),
            "Pick 3": attr_dict.get('Pick 3', 'Not Available'),
            "Exact Carat Total Weight": attr_dict.get('Exact Carat Total Weight', 'N/A'),
            "Stone Carat": attr_dict.get('Stone Carat', 'N/A'),
            "Number of Diamonds": attr_dict.get('Number Of Diamonds', 'N/A'),
            "Main Stone": attr_dict.get('Main Stone', 'N/A')
        }
        
        for key, value in material_data.items():
            st.text(f"{key}: {value}")
    
    # Show calculated totals
    analysis_service = st.session_state.analysis_service
    calculated_total = analysis_service.calculate_total_carat_from_picks({
        **{k: v for k, v in info_data.items()},
        **{k: v for k, v in material_data.items()},
        **{k: v for k, v in attr_dict.items()},
        'Weight': basic.get('Weight', 'N/A')
    })
    
    exact_total = float(attr_dict.get('Exact Carat Total Weight', 0))
    
    st.markdown("#### 🔸 Carat Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Calculated from Picks", f"{calculated_total:.3f} carats")
    with col2:
        st.metric("Exact Carat Total", f"{exact_total} carats")
    with col3:
        difference = abs(calculated_total - exact_total)
        st.metric("Difference", f"{difference:.3f} carats", delta=f"{'✓' if difference < 0.1 else '⚠️'}")
    
    # Store data for processing
    st.session_state.current_product_data = {
        **{k: v for k, v in info_data.items()},
        **{k: v for k, v in material_data.items()},
        **{k: v for k, v in attr_dict.items()},
        'Weight': basic.get('Weight', 'N/A')
    }

def get_comprehensive_product_understanding(product_details: Dict[str, Any]) -> Optional[str]:
    """Get comprehensive understanding with complete database"""
    processed_data = st.session_state.current_product_data
    
    try:
        understanding = st.session_state.gemini_service.get_product_understanding(processed_data)
        return understanding
    except Exception as e:
        st.error(f"❌ Comprehensive Understanding failed: {e}")
        return None

def display_comprehensive_understanding(understanding_text: str, sku: str):
    """Display comprehensive understanding with database context"""
    st.subheader("🔍 Comprehensive Diamond Analysis with Complete Database")
    st.markdown(f"**Analysis Using Complete Pricing Database with Strict Type Separation for SKU: {sku}**")
    
    if understanding_text:
        st.markdown("---")
        paragraphs = understanding_text.split('\n\n')
        
        for paragraph in paragraphs:
            if paragraph.strip():
                st.markdown(paragraph.strip())
                st.markdown("")
    else:
        st.info("No comprehensive diamond analysis available.")

def process_comprehensive_product_data(product_details: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process with comprehensive analysis"""
    processed_data = st.session_state.current_product_data
    
    try:
        result = st.session_state.gemini_service.process_with_gemini(processed_data)
        return result
    except Exception as e:
        st.error(f"❌ Comprehensive Processing failed: {e}")
        return None

def display_comprehensive_analysis(data: Dict[str, Any]):
    """Display comprehensive analysis with complete database integration"""
    st.subheader("🤖 Comprehensive AI Diamond Analysis with Complete Database")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Metal Purity", data.get('metal_purity', 'N/A'))
    
    with col2:
        st.metric("Metal Weight", f"{data.get('metal_weight', 'N/A')} g")
    
    with col3:
        st.metric("Stone Used", data.get('stone_used', 'N/A'))
    
    # Comprehensive Diamond Analysis
    if data.get('diamond_details') and data['diamond_details'].get('diamonds'):
        st.markdown("#### 💎 Complete Diamond Analysis with Database Integration")
        
        diamonds = data['diamond_details']['diamonds']
        diamond_data = []
        total_carat = 0
        total_price = 0
        
        for i, diamond in enumerate(diamonds, 1):
            diamond_info = {
                "Diamond": f"Diamond {i}",
                "Type": diamond.get('diamondType', 'N/A'),
                "Quantity": diamond.get('quantity', 'N/A'),
                "Carat Value": diamond.get('carat_value', 'N/A'),
                "ProductId": diamond.get('ProductId', 'N/A'),
                "DB Carat/Unit": f"{diamond.get('matched_carat_per_unit', 0):.3f}",
                "Unit Price": f"${diamond.get('unit_price', 0):.2f}",
                "TotalCarat": diamond.get('TotalCarat', 0),
                "Total Price": f"${diamond.get('total_price', 0):.2f}"
            }
            diamond_data.append(diamond_info)
            total_carat += diamond.get('TotalCarat', 0)
            total_price += diamond.get('total_price', 0)
        
        # Add comprehensive total
        diamond_data.append({
            "Diamond": "**TOTAL**",
            "Type": "",
            "Quantity": "",
            "Carat Value": "",
            "ProductId": "",
            "DB Carat/Unit": "",
            "Unit Price": "",
            "TotalCarat": f"**{round(total_carat, 3)}**",
            "Total Price": f"**${total_price:.2f}**"
        })
        
        st.dataframe(diamond_data, use_container_width=True)
        
        # Database Analysis Summary
        if data['diamond_details'].get('database_analysis'):
            st.info(f"**Database Analysis:** {data['diamond_details']['database_analysis']}")
        
        # Detailed Breakdown
        st.markdown("**Complete Database Calculation Breakdown:**")
        for i, diamond in enumerate(diamonds, 1):
            qty = diamond.get('quantity', 0)
            product_id = diamond.get('ProductId', '')
            carat_per_unit = diamond.get('matched_carat_per_unit', 0)
            unit_price = diamond.get('unit_price', 0)
            total_carat_calc = diamond.get('TotalCarat', 0)
            total_price_calc = diamond.get('total_price', 0)
            
            st.text(f"Diamond {i} ({product_id}): {qty} × {carat_per_unit:.3f} carats = {total_carat_calc:.3f} total carats")
            st.text(f"  Price: {qty} × ${unit_price:.2f} = ${total_price_calc:.2f}")
        
        st.success(f"**Complete Database Integration:** Used exact/next-higher values from pricing database with strict type separation for precise calculations.")
        
    else:
        st.info("No diamonds found in this product.")

if __name__ == "__main__":
    main()
