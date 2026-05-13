# Phase 1.1.3: Content Processing and Structuring

## Overview

This sub-phase processes raw scraped content into structured, searchable format with semantic chunking and metadata extraction.

## Objective

Process raw content into structured, searchable format with HTML cleaning, text chunking, and metadata extraction.

## Components

### Content Processor
- `src/data_collection/content_processor.py` - ContentProcessor class
- HTML content cleaning and sanitization
- Text chunking strategy for optimal embedding
- PDF processing capabilities

### Metadata Extractor
- `src/data_collection/metadata_extractor.py` - MetadataExtractor class
- Pattern matching for financial metrics
- NLP-based entity recognition
- Data validation and cleaning

### Chunking Strategy
- Semantic chunking with configurable size
- Sentence-based tokenization
- Overlap for context preservation
- Batch processing for efficiency

## Usage

### Content Processing
```python
from src.data_collection import ContentProcessor, MetadataExtractor

processor = ContentProcessor()
metadata_extractor = MetadataExtractor()

# Process HTML content
processed = processor.process_html_content(html, source_url)

# Extract metadata
metadata = metadata_extractor.extract_metadata(processed)

# Create chunks
chunks = processor.chunk_content(processed)
```

### Command Line
```bash
# Process existing raw data
python src/main.py --mode process

# Process with custom chunk size
python src/main.py --mode process --chunk-size 256

# Process with debug logging
python src/main.py --mode process --log-level DEBUG
```

## Configuration

### Processing Settings
- `CHUNK_SIZE` - Maximum chunk size (default: 512 tokens)
- `CHUNK_OVERLAP` - Overlap between chunks (default: 50 tokens)
- `BATCH_SIZE` - Processing batch size (default: 10)
- `MAX_DOCUMENT_SIZE` - Maximum document size limit

### NLP Settings
- spaCy model for entity recognition
- NLTK for sentence tokenization
- Pattern matching for financial metrics

## Data Structure

### Processed Content Format
```json
{
  "source_type": "html",
  "source_url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
  "cleaned_text": "Cleaned and sanitized content...",
  "title": "HDFC Large Cap Fund",
  "metadata": {
    "fund_name": "HDFC Large Cap Fund",
    "category": "Large Cap",
    "expense_ratio": "1.25%"
  },
  "sections": [
    {
      "level": 1,
      "text": "HDFC Large Cap Fund"
    }
  ],
  "tables": [],
  "links": [],
  "processed_at": "2023-01-01T12:00:00"
}
```

### Chunk Format
```json
{
  "chunk_id": "fund_chunk_0",
  "chunk_index": 0,
  "text": "Chunk text content...",
  "source_url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
  "source_type": "html",
  "metadata": {
    "total_chunks": 5,
    "chunk_index": 0,
    "fund_name": "HDFC Large Cap Fund"
  }
}
```

## Processing Pipeline

### 1. Content Cleaning
- HTML tag removal and sanitization
- Unicode normalization
- Whitespace cleanup
- Control character removal

### 2. Structure Extraction
- Section identification and hierarchy
- Table extraction and parsing
- Link extraction and validation
- Title and heading extraction

### 3. Metadata Extraction
- Financial metrics (expense ratio, NAV, minimum investment)
- Fund information (category, risk level, scheme type)
- Contact information (phone, email, website)
- Regulatory information (AMFI/SEBI registration)

### 4. Text Chunking
- Sentence-based tokenization
- Semantic boundary detection
- Size optimization for embedding
- Overlap application for context

## Validation

Run processing validation:
```bash
python src/main.py --mode validate
```

## Quality Assurance

### Data Validation
- Required field completeness
- Data type verification
- Format consistency
- Content quality checks

### Error Handling
- Malformed content recovery
- Missing data handling
- Large document truncation
- Unicode error handling

## Deliverables

✅ `src/data_collection/content_processor.py` with ContentProcessor class
✅ `src/data_collection/metadata_extractor.py` with MetadataExtractor class
✅ Processed data storage in `data/processed/` directory
✅ Metadata validation and quality checks
✅ Semantic chunking with proper overlap
✅ PDF processing capabilities
✅ HTML content cleaning and sanitization

## Next Steps

After completing Phase 1.1.3, proceed to Phase 1.1.4: Vector Database Integration.
