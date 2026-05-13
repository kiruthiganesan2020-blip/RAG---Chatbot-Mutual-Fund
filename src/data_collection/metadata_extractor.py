"""
Metadata extraction logic
"""

import re
from typing import Dict, Any
from src.config import get_logger

logger = get_logger(__name__)

class MetadataExtractor:
    """Extracts structured metadata from processed content"""
    
    def __init__(self):
        self.patterns = {
            'nav': r'NAV[:\s]*([\d,\.]+)',
            'expense_ratio': r'Expense Ratio[:\s]*([\d\.]+%)',
            'category': r'Category[:\s]*([^\n\.]+)',
            'min_investment': r'Minimum Investment[:\s]*([^\n\.]+)',
            'risk_level': r'Risk Level[:\s]*([^\n\.]+)',
            'aum': r'AUM[:\s]*([^\n\.]+)'
        }
    
    def extract_metadata(self, processed_content: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata using regex patterns"""
        text = processed_content.get('text', '')
        metadata = {
            'source_title': processed_content.get('title', ''),
            'source_url': processed_content.get('source_url', '')
        }
        
        for key, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metadata[key] = match.group(1).strip()
                
        return metadata
