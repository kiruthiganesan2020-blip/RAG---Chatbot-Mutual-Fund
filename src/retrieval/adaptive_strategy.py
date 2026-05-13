"""
Adaptive retrieval strategy with query-based weighting
"""

import re
from typing import Dict, Any, List
from datetime import datetime
from src.config import get_logger

logger = get_logger(__name__)

class AdaptiveRetrievalStrategy:
    """Adaptive retrieval strategy with query-based weighting"""
    
    def __init__(self):
        self.default_weights = {
            'semantic_weight': 0.7,
            'keyword_weight': 0.3
        }
        
        self.query_type_weights = {
            'factual': {'semantic_weight': 0.8, 'keyword_weight': 0.2},
            'entity_specific': {'semantic_weight': 0.4, 'keyword_weight': 0.6},
            'comparative': {'semantic_weight': 0.5, 'keyword_weight': 0.5},
            'default': {'semantic_weight': 0.7, 'keyword_weight': 0.3}
        }
        
        self.performance_metrics = {
            'precision_at_5': 0.0,
            'recall': 0.0,
            'response_time': 0.0,
            'user_satisfaction': 0.0
        }
    
    def classify_query(self, query: str) -> str:
        """Classify query for adaptive weighting (alias for classify_query_type return['type'])"""
        return self.classify_query_type(query)['type']

    def classify_query_type(self, query: str) -> Dict[str, Any]:
        """Classify query type for adaptive weighting"""
        query_lower = query.lower()
        
        # Check for entity-specific patterns
        entity_patterns = [
            r'hdfc\s+(large\s+cap|mid\s+cap|equity|focused|elss)',
            r'nav\s+of\s+hdfc',
            r'hdfc\s+(mutual\s+)?fund'
        ]
        
        for pattern in entity_patterns:
            if re.search(pattern, query_lower):
                return {'type': 'entity_specific', 'confidence': 0.9}
        
        # Check for comparative patterns
        comparative_words = ['compare', 'vs', 'versus', 'better', 'worse', 'difference', 'between']
        if any(word in query_lower for word in comparative_words):
            return {'type': 'comparative', 'confidence': 0.8}
        
        # Check for factual patterns
        factual_words = ['what', 'how', 'when', 'where', 'who', 'which', 'explain', 'define']
        if any(word in query_lower for word in factual_words):
            return {'type': 'factual', 'confidence': 0.7}
        
        # Default
        return {'type': 'default', 'confidence': 0.5}
    
    def get_adaptive_weights(self, query: str) -> Dict[str, float]:
        """Get adaptive weights based on query type"""
        query_classification = self.classify_query_type(query)
        query_type = query_classification['type']
        
        weights = self.query_type_weights.get(query_type, self.default_weights)
        
        return {
            'semantic_weight': weights['semantic_weight'],
            'keyword_weight': weights['keyword_weight'],
            'query_type': query_type,
            'confidence': query_classification['confidence']
        }
    
    def optimize_for_hdfc_data(self, query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize results specifically for HDFC mutual fund data"""
        optimized_results = []
        
        hdfc_funds = [
            'hdfc large cap', 'hdfc mid cap', 'hdfc equity', 
            'hdfc focused', 'hdfc elss'
        ]
        
        for result in results:
            content_lower = result.get('content', '').lower()
            metadata = result.get('metadata', {})
            
            # HDFC fund boost
            fund_boost = 0.0
            for fund in hdfc_funds:
                if fund in content_lower:
                    fund_boost = 0.2
                    break
            
            # Official source boost
            source_boost = 0.0
            if metadata.get('source') == 'hdfc':
                source_boost = 0.15
            elif metadata.get('source') == 'amfi':
                source_boost = 0.10
            
            # Recency boost (prefer newer documents)
            recency_boost = 0.0
            if 'last_updated' in metadata:
                try:
                    doc_date = datetime.fromisoformat(metadata['last_updated'])
                    days_old = (datetime.now() - doc_date).days
                    if days_old < 30:
                        recency_boost = 0.1
                    elif days_old < 90:
                        recency_boost = 0.05
                except:
                    pass
            
            # Apply boosts
            optimized_result = result.copy()
            original_score = result.get('hybrid_score', result.get('similarity_score', 0))
            boosted_score = original_score + fund_boost + source_boost + recency_boost
            
            optimized_result['original_score'] = original_score
            optimized_result['boosted_score'] = boosted_score
            optimized_result['fund_boost'] = fund_boost
            optimized_result['source_boost'] = source_boost
            optimized_result['recency_boost'] = recency_boost
            optimized_result['final_score'] = boosted_score
            
            optimized_results.append(optimized_result)
        
        # Re-sort by boosted score
        optimized_results.sort(key=lambda x: x.get('final_score', 0), reverse=True)
        
        # Update ranks
        for i, result in enumerate(optimized_results):
            result['optimized_rank'] = i + 1
        
        return optimized_results
