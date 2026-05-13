# Phase 1.1.4: Vector Database Integration

## Overview

This sub-phase sets up ChromaDB for vector storage and retrieval with proper schema design, batch processing, and search capabilities.

## Objective

Set up ChromaDB for vector storage and retrieval with document embedding pipeline, batch processing, and metadata filtering.

## Components

### Vector Database Manager
- `src/vector_db/chroma_manager.py` - ChromaManager class
- Persistent client setup with configuration
- Collection management and schema design
- Database backup and recovery

### Schema Design
- `src/vector_db/schema.py` - Data models and validation
- DocumentChunk and SearchResult dataclasses
- Metadata field definitions and types
- Schema validation and compliance

### Embedding Pipeline
- Default embedding function integration
- Batch processing for efficiency
- Embedding caching and optimization
- Similarity search capabilities

## Usage

### Vector Database Operations
```python
from src.vector_db import ChromaManager, VectorDBSchema

async with ChromaManager() as vector_db:
    # Add documents
    chunk_ids = vector_db.add_documents(chunks)
    
    # Search documents
    results = vector_db.search_similar("HDFC large cap fund", n_results=5)
    
    # Get collection stats
    stats = vector_db.get_collection_stats()
    
    # Backup collection
    backup_file = vector_db.backup_collection()
```

### Command Line
```bash
# Create embeddings from processed data
python src/main.py --mode embed

# Validate vector database
python src/main.py --mode validate

# Backup database
python src/main.py --mode backup
```

## Configuration

### Database Settings
- `CHROMA_DB_PATH` - Path for ChromaDB storage
- `BATCH_SIZE` - Embedding batch size (default: 10)
- `COLLECTION_NAME` - Collection name (default: "mutual_funds")

### Embedding Settings
- Default embedding model: all-MiniLM-L6-v2
- Vector dimension: 384
- Similarity metric: cosine similarity

## Data Structure

### DocumentChunk Schema
```python
@dataclass
class DocumentChunk:
    chunk_id: str
    chunk_index: int
    text: str
    source_url: str
    source_type: str
    metadata: Dict[str, Any]
    total_chunks: int
    chunk_size: int
    source_title: str
    processed_at: str
```

### SearchResult Schema
```python
@dataclass
class SearchResult:
    id: str
    text: str
    metadata: Dict[str, Any]
    distance: float
    similarity_score: float
```

### Collection Metadata
```json
{
  "description": "HDFC Mutual Fund FAQ Assistant Vector Database",
  "version": "1.0.0",
  "created_by": "RAG System",
  "compliance": "facts-only",
  "required_fields": ["source_url", "source_type", "chunk_index"],
  "field_types": {
    "source_url": "string",
    "chunk_index": "integer",
    "fund_name": "string"
  }
}
```

## Database Operations

### 1. Collection Management
- Create collections with metadata
- Get or create existing collections
- Reset collections for fresh start
- Delete collections and data

### 2. Document Operations
- Add documents with embeddings
- Update existing documents
- Delete specific documents
- Delete by source URL

### 3. Search Operations
- Semantic search with similarity scoring
- Metadata filtering support
- Hybrid search capabilities
- Result ranking and limiting

### 4. Backup and Recovery
- JSON-based backup format
- Collection restoration procedures
- Data integrity validation
- Backup scheduling and rotation

## Search Capabilities

### Semantic Search
```python
# Basic semantic search
results = vector_db.search_similar("expense ratio", n_results=5)

# Search with metadata filtering
results = vector_db.search_similar(
    "minimum investment",
    where={"fund_name": "HDFC Large Cap Fund"},
    n_results=3
)
```

### Metadata Filtering
```python
# Filter by fund category
results = vector_db.search_similar(
    "risk level",
    where={"category": "Large Cap"}
)

# Filter by source type
results = vector_db.search_similar(
    "fund details",
    where={"source_type": "html"}
)
```

## Performance Optimization

### Batch Processing
- Efficient embedding generation
- Memory-optimized chunk processing
- Progress tracking and logging
- Error handling for batch failures

### Indexing Strategy
- HNSW indexing for fast search
- Metadata indexing for filtering
- Full-text search integration
- Similarity threshold optimization

## Validation

Run database validation:
```bash
python src/main.py --mode validate
```

## Compliance

### Data Privacy
- No PII storage in embeddings
- Source attribution maintained
- Data retention policies
- Access control considerations

### Regulatory Compliance
- Facts-only content enforcement
- Source verification requirements
- Audit trail maintenance
- Data integrity checks

## Deliverables

✅ `src/vector_db/` module with ChromaDB integration
✅ `src/vector_db/schema.py` with data models
✅ Vector database storage in `data/embeddings/` directory
✅ Search and retrieval API functions
✅ Batch processing for efficiency
✅ Metadata filtering capabilities
✅ Database backup and recovery mechanisms
✅ Collection management and schema design

## Next Steps

After completing Phase 1.1.4, proceed to Phase 1.1.5: Testing and Validation.
