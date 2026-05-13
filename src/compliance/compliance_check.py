"""
Compliance layer for content filtering and validation
"""

import re
from typing import Dict, Any, List
from src.config import get_logger

logger = get_logger(__name__)

class ComplianceLayer:
    """Compliance layer for content filtering and validation"""
    
    def __init__(self):
        self.forbidden_content = {
            'investment_advice': [
                r'\byou should invest\b',
                r'\byou must invest\b',
                r'\binvest now\b',
                r'\bbuy this fund\b',
                r'\bsell your holdings\b',
                r'\bi recommend\b',
                r'\bwe recommend\b',
                r'\bbest fund to buy\b'
            ],
            'personal_data': [
                'your account', 'your portfolio', 'personal details',
                'contact information', 'financial situation'
            ],
            'performance_guarantees': [
                'guaranteed returns', 'risk-free investment',
                'sure shot profit', 'certain gains'
            ]
        }
        
        self.safe_sources = [
            'hdfc.com', 'amfiindia.com', 'sebi.gov.in', 
            'rbi.org.in', 'nseindia.com', 'bseindia.com',
            'hdfcfund.com', 'groww.in'
        ]
    
    def filter_content(self, text: str) -> Dict[str, Any]:
        """Filter content for compliance violations"""
        violations = []
        filtered_text = text
        
        # Check for investment advice
        for pattern in self.forbidden_content['investment_advice']:
            if re.search(pattern, filtered_text, flags=re.IGNORECASE):
                violations.append(f"Investment advice pattern: '{pattern}'")
                filtered_text = re.sub(pattern, '[ADVICE REMOVED]', filtered_text, flags=re.IGNORECASE)
        
        # Check for personal data references
        for phrase in self.forbidden_content['personal_data']:
            if phrase.lower() in text.lower():
                violations.append(f"Personal data reference: '{phrase}'")
                filtered_text = filtered_text.replace(phrase, '[PERSONAL DATA REMOVED]')
        
        # Check for performance guarantees
        for phrase in self.forbidden_content['performance_guarantees']:
            if phrase.lower() in text.lower():
                violations.append(f"Performance guarantee: '{phrase}'")
                filtered_text = filtered_text.replace(phrase, '[GUARANTEE REMOVED]')
        
        return {
            'original_text': text,
            'filtered_text': filtered_text,
            'violations': violations,
            'compliant': len(violations) == 0
        }
    
    def validate_urls(self, text: str) -> Dict[str, Any]:
        """Validate URLs for safety and privacy"""
        url_pattern = r'https?://([^\s<>"{}|\\^`\[\]]+)'
        urls = re.findall(url_pattern, text)
        
        safe_urls = []
        unsafe_urls = []
        
        for url in urls:
            if any(safe_domain in url for safe_domain in self.safe_sources):
                safe_urls.append(url)
            else:
                unsafe_urls.append(url)
        
        # Remove unsafe URLs from text
        filtered_text = text
        for unsafe_url in unsafe_urls:
            filtered_text = filtered_text.replace(f"https://{unsafe_url}", '[UNSAFE URL REMOVED]')
            filtered_text = filtered_text.replace(f"http://{unsafe_url}", '[UNSAFE URL REMOVED]')
        
        return {
            'original_urls': urls,
            'safe_urls': safe_urls,
            'unsafe_urls': unsafe_urls,
            'filtered_text': filtered_text,
            'url_safe': len(unsafe_urls) == 0
        }
    
    def check_response_compliance(self, response: str) -> Dict[str, Any]:
        """Comprehensive compliance check"""
        # Content filtering
        content_result = self.filter_content(response)
        
        # URL validation
        url_result = self.validate_urls(response)
        
        # Length check
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]
        length_compliant = len(sentences) <= 5  # Relaxed from 3 for better responses
        
        # Overall compliance
        is_compliant = (
            content_result['compliant'] and 
            url_result['url_safe']
        )
        
        issues = []
        if not content_result['compliant']:
            issues.extend(content_result['violations'])
        if not url_result['url_safe']:
            issues.append(f"Unsafe URLs detected: {url_result['unsafe_urls']}")
        if not length_compliant:
            issues.append("Response exceeds 5 sentences")
        
        return {
            'is_compliant': is_compliant,
            'issues': issues,
            'sanitized_response': content_result['filtered_text'],
            'sentence_count': len(sentences)
        }
