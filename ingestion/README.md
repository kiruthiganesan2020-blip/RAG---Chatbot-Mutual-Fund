# Ingestion Pipeline - Phase 1 Sub-Phases

## Overview

This directory contains the organized implementation of Phase 1 sub-phases for the Mutual Fund FAQ Assistant. Each sub-phase is structured as an independent module with its own documentation and execution scripts.

## Phase 1.1 Sub-Phases Structure

```
ingestion/
├── README.md                    # This file - Overview and navigation
├── phase1_1_1/                  # Environment Setup and Configuration
│   ├── README.md               # Sub-phase documentation
│   └── main.py                 # Execution script
├── phase1_1_2/                  # Web Scraping Implementation
│   └── README.md               # Sub-phase documentation
├── phase1_1_3/                  # Content Processing and Structuring
│   └── README.md               # Sub-phase documentation
├── phase1_1_4/                  # Vector Database Integration
│   └── README.md               # Sub-phase documentation
├── phase1_1_5/                  # Testing and Validation
│   └── README.md               # Sub-phase documentation
└── phase1_1_6/                  # Documentation and Deployment
    └── README.md               # Sub-phase documentation
```

## Sub-Phase Descriptions

### Phase 1.1.1: Environment Setup and Configuration
**Objective**: Establish development environment and configuration management

**Components**:
- Project folder structure with proper separation
- Python virtual environment and dependencies
- Environment variables and settings management
- Git repository initialization with .gitignore
- Docker containerization setup
- Logging and monitoring infrastructure

**Execution**: `python ingestion/phase1_1_1/main.py`

### Phase 1.1.2: Web Scraping Implementation
**Objective**: Build robust web scraping for HDFC mutual fund URLs

**Components**:
- HTML content extraction from Groww URLs
- Selenium fallback mechanisms for JavaScript-heavy pages
- Retry logic and error handling for network issues
- Rate limiting and respectful scraping practices
- Structured data extraction (fund name, NAV, expense ratio, etc.)
- Raw data storage with metadata

**Execution**: `python src/main.py --mode collect`

### Phase 1.1.3: Content Processing and Structuring
**Objective**: Process raw content into structured, searchable format

**Components**:
- HTML content cleaning and sanitization
- Text chunking strategy for optimal embedding
- Metadata extraction using pattern matching and NLP
- PDF document handling capabilities
- Semantic chunks with proper overlap
- Data validation and cleaning

**Execution**: `python src/main.py --mode process`

### Phase 1.1.4: Vector Database Integration
**Objective**: Set up ChromaDB for vector storage and retrieval

**Components**:
- ChromaDB initialization with proper schema design
- Document chunk embedding pipeline
- Batch processing for efficiency
- Metadata filtering capabilities
- Search and retrieval functions
- Database backup and recovery mechanisms

**Execution**: `python src/main.py --mode embed`

### Phase 1.1.5: Testing and Validation
**Objective**: Ensure system reliability and data quality

**Components**:
- Unit tests for all components
- Integration tests for end-to-end pipeline
- Performance benchmarks and monitoring
- Data quality and completeness validation
- Error scenario and edge case testing
- Automated test pipeline

**Execution**: `pytest tests/ -v`

### Phase 1.1.6: Documentation and Deployment
**Objective**: Complete documentation and deployment preparation

**Components**:
- Comprehensive README with setup instructions
- API endpoints and usage examples documentation
- Troubleshooting guides and FAQ
- Deployment scripts and Docker setup
- API documentation generation
- Phase 2 transition preparation

**Execution**: `python scripts/run_phase1.py`

## Usage Guide

### Sequential Execution

Run sub-phases in sequence for complete Phase 1 implementation:

```bash
# Phase 1.1.1: Environment Setup
python ingestion/phase1_1_1/main.py

# Phase 1.1.2: Web Scraping
python src/main.py --mode collect

# Phase 1.1.3: Content Processing  
python src/main.py --mode process

# Phase 1.1.4: Vector Database
python src/main.py --mode embed

# Phase 1.1.5: Testing
pytest tests/ -v

# Phase 1.1.6: Full Pipeline
python scripts/run_phase1.py
```

### Individual Sub-Phase Execution

Each sub-phase can be run independently:

```bash
# Run specific sub-phase documentation
cat ingestion/phase1_1_1/README.md

# Validate specific component
python src/main.py --mode validate
```

### Docker Execution

```bash
# Run with Docker
docker-compose up --build

# View logs
docker-compose logs -f app
```

## Integration Points

### Data Flow
1. **Phase 1.1.1** → Environment setup and configuration
2. **Phase 1.1.2** → Raw data collection from URLs
3. **Phase 1.1.3** → Content processing and structuring
4. **Phase 1.1.4** → Vector database storage
5. **Phase 1.1.5** → Testing and validation
6. **Phase 1.1.6** → Documentation and deployment

### Shared Components
- **Configuration**: `src/config/` modules
- **Logging**: `src/utils/logger.py`
- **Data Storage**: `data/` directories
- **Testing**: `tests/` directory
- **Documentation**: `docs/` directory

## Quality Assurance

### Validation Commands
```bash
# Test environment setup
python ingestion/phase1_1_1/main.py

# Validate data collection
python src/main.py --mode validate

# Run comprehensive tests
pytest tests/ -v --cov=src
```

### Health Checks
```bash
# System health check
python scripts/test_setup.py

# Database validation
python src/main.py --mode validate

# Performance monitoring
python src/main.py --mode benchmark
```

## Compliance Notes

- **Facts-Only**: All sub-phases enforce facts-only responses
- **Source Verification**: Only official HDFC/AMFI/SEBI sources
- **Data Privacy**: No PII collection or storage
- **Regulatory Compliance**: SEBI guidelines adherence

## Troubleshooting

### Common Issues
1. **Environment Setup**: Check Python version and dependencies
2. **Web Scraping**: Verify network connectivity and URL accessibility
3. **Content Processing**: Check data formats and encoding
4. **Vector Database**: Verify ChromaDB installation and permissions
5. **Testing**: Check test environment and fixtures

### Debug Mode
```bash
# Enable debug logging
python ingestion/phase1_1_1/main.py --log-level DEBUG

# Run with verbose output
python src/main.py --mode full --log-level DEBUG
```

## Next Steps

After completing all Phase 1.1 sub-phases:

1. **Validate**: Run comprehensive testing suite
2. **Document**: Review all documentation
3. **Deploy**: Set up production environment
4. **Monitor**: Establish monitoring and alerting
5. **Phase 2**: Begin RAG System Implementation

## Support

For issues with specific sub-phases:
1. Check the sub-phase README file
2. Review logs in `logs/` directory
3. Run validation commands
4. Check troubleshooting guides
5. Review test results

## Architecture Evolution

The ingestion pipeline provides a solid foundation for:
- **Phase 2**: RAG System Implementation
- **Phase 3**: Response Generation Engine
- **Phase 4**: User Interface Development
- **Phase 5**: Security and Compliance
- **Phase 6**: Testing and Quality Assurance
- **Phase 7**: Deployment and Monitoring
- **Phase 8**: Optimization and Scaling
