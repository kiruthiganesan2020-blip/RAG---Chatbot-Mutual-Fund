"""
Schema definitions for vector database
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class DocumentChunk:
    """Represents a chunk of document for vector storage"""
    chunk_id: str
    chunk_index: int
    text: str
    source_url: str
    source_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    total_chunks: int = 1
    chunk_size: int = 0
    source_title: str = ""
    processed_at: str = ""


@dataclass
class SearchResult:
    """Represents a search result from vector database"""
    id: str
    text: str
    metadata: Dict[str, Any]
    distance: float
    similarity_score: float


class VectorDBSchema:
    """Schema definitions for vector database"""
    
    # Collection metadata
    COLLECTION_METADATA = {
        "description": "HDFC Mutual Fund FAQ Assistant Vector Database",
        "version": "1.0.0",
        "created_by": "RAG System",
        "compliance": "facts-only"
    }
    
    # Required metadata fields
    REQUIRED_METADATA_FIELDS = [
        "source_url",
        "source_type", 
        "chunk_index",
        "total_chunks",
        "chunk_size",
        "processed_at"
    ]
    
    # Optional metadata fields
    OPTIONAL_METADATA_FIELDS = [
        "fund_name",
        "category",
        "source_title",
        "amc",
        "scheme_type",
        "expense_ratio",
        "nav",
        "min_investment",
        "risk_level",
        "added_at"
    ]
    
    # Metadata field types
    METADATA_TYPES = {
        "source_url": "string",
        "source_type": "string",
        "chunk_index": "integer",
        "total_chunks": "integer", 
        "chunk_size": "integer",
        "processed_at": "datetime",
        "fund_name": "string",
        "category": "string",
        "source_title": "string",
        "amc": "string",
        "scheme_type": "string",
        "expense_ratio": "string",
        "nav": "string",
        "min_investment": "string",
        "risk_level": "string",
        "added_at": "datetime"
    }
    
    @classmethod
    def get_collection_metadata(cls) -> Dict[str, Any]:
        """Get collection metadata"""
        import json
        return {
            **cls.COLLECTION_METADATA,
            "required_fields": json.dumps(cls.REQUIRED_METADATA_FIELDS),
            "optional_fields": json.dumps(cls.OPTIONAL_METADATA_FIELDS),
            "field_types": json.dumps(cls.METADATA_TYPES),
            "created_at": datetime.now().isoformat()
        }
    
    @classmethod
    def validate_metadata(cls, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate metadata against schema"""
        validated = {}
        errors = []
        
        # Check required fields
        for field in cls.REQUIRED_METADATA_FIELDS:
            if field not in metadata:
                errors.append(f"Missing required field: {field}")
            else:
                validated[field] = metadata[field]
        
        # Add optional fields
        for field in cls.OPTIONAL_METADATA_FIELDS:
            if field in metadata:
                validated[field] = metadata[field]
        
        # Validate field types
        for field, value in validated.items():
            expected_type = cls.METADATA_TYPES.get(field)
            if expected_type and not cls._validate_field_type(value, expected_type):
                errors.append(f"Invalid type for {field}: expected {expected_type}")
        
        if errors:
            raise ValueError(f"Metadata validation failed: {errors}")
        
        return validated
    
    @classmethod
    def _validate_field_type(cls, value: Any, expected_type: str) -> bool:
        """Validate field type"""
        type_mapping = {
            "string": str,
            "integer": int,
            "datetime": str,
            "float": float,
            "boolean": bool
        }
        
        expected_python_type = type_mapping.get(expected_type)
        if expected_python_type:
            return isinstance(value, expected_python_type)
        
        return True
    
    @classmethod
    def create_document_chunk(
        cls,
        text: str,
        source_url: str,
        source_type: str,
        chunk_index: int = 0,
        total_chunks: int = 1,
        metadata: Optional[Dict[str, Any]] = None
    ) -> DocumentChunk:
        """Create a DocumentChunk with proper validation"""
        chunk_id = f"{source_url}_chunk_{chunk_index}"
        
        return DocumentChunk(
            chunk_id=chunk_id,
            chunk_index=chunk_index,
            text=text,
            source_url=source_url,
            source_type=source_type,
            metadata=metadata or {},
            total_chunks=total_chunks,
            chunk_size=len(text),
            processed_at=datetime.now().isoformat()
        )
    
    @classmethod
    def create_search_result(
        cls,
        id: str,
        text: str,
        metadata: Dict[str, Any],
        distance: float,
        similarity_score: float
    ) -> SearchResult:
        """Create a SearchResult with proper validation"""
        return SearchResult(
            id=id,
            text=text,
            metadata=metadata,
            distance=distance,
            similarity_score=similarity_score
        )
    
    @classmethod
    def get_filterable_fields(cls) -> List[str]:
        """Get list of fields that can be used for filtering"""
        return cls.REQUIRED_METADATA_FIELDS + cls.OPTIONAL_METADATA_FIELDS
    
    @classmethod
    def get_source_types(cls) -> List[str]:
        """Get valid source types"""
        return ["html", "pdf", "text", "json"]
    
    @classmethod
    def get_fund_categories(cls) -> List[str]:
        """Get valid fund categories"""
        return [
            "large-cap",
            "mid-cap", 
            "equity",
            "focused",
            "elss",
            "hybrid",
            "debt",
            "flexi-cap"
        ]
    
    @classmethod
    def get_risk_levels(cls) -> List[str]:
        """Get valid risk levels"""
        return [
            "very-low",
            "low", 
            "moderately-low",
            "moderate",
            "moderately-high",
            "high",
            "very-high"
        ]
    
    @classmethod
    def get_scheme_types(cls) -> List[str]:
        """Get valid scheme types"""
        return [
            "direct",
            "regular",
            "growth",
            "dividend",
            "elss"
        ]
