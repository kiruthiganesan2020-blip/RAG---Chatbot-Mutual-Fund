# Phase-Wise Architecture: Mutual Fund FAQ Assistant

## Overview

This document outlines the comprehensive phase-wise architecture for developing a Retrieval-Augmented Generation (RAG)-based mutual fund FAQ assistant that adheres to strict compliance and regulatory requirements.

---

## Phase 1: Foundation and Data Collection

### 1.1 Infrastructure Setup
- **Development Environment**
  - Python 3.9+ with virtual environment
  - Version control with Git
  - Containerization with Docker (optional)
  - CI/CD pipeline setup

- **Core Technology Stack**
  - **Vector Database**: ChromaDB or Pinecone
  - **Embedding Model**: Sentence-Transformers (all-MiniLM-L6-v2)
  - **LLM**: OpenAI GPT-4 or Anthropic Claude
  - **Web Framework**: FastAPI or Flask
  - **Frontend**: React/Vue.js with Tailwind CSS

- **CI/CD and Automation**
  - **GitHub Actions**: Automated workflows for data collection and updates
  - **Scheduled Triggers**: Daily (2 AM UTC) and weekly (Sundays 3 AM UTC)
  - **Automated Testing**: Unit tests, integration tests, performance benchmarks
  - **Quality Assurance**: Code quality checks, security scanning, dependency checks
  - **Deployment**: Staging and production environments with automated rollouts

### 1.2 Data Corpus Development ✅ IMPLEMENTED
- **Source Selection**
  - **Primary AMC**: HDFC Mutual Fund
  - **Project Scope**: Only the following 5 specific URLs will be used for this project - no other URLs will be scraped or processed
  - **Selected Schemes (5 diverse categories)**:
    - **Large-cap Fund**: HDFC Large Cap Fund Direct Growth
      - URL: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth
    - **Mid-cap Fund**: HDFC Mid Cap Fund Direct Growth
      - URL: https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth
    - **Equity Fund**: HDFC Equity Fund Direct Growth
      - URL: https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth
    - **Focused Fund**: HDFC Focused Fund Direct Growth
      - URL: https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth
    - **ELSS Tax Saver**: HDFC ELSS Tax Saver Fund Direct Plan Growth
      - URL: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth

- **Data Collection Pipeline**
  ```python
  # Implemented web scraping structure
  sources = {
      'factsheets': {
          'large_cap': 'https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth',
          'mid_cap': 'https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth',
          'equity': 'https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth',
          'focused': 'https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth',
          'elss': 'https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth'
      },
      'kim': {
          'base_url': 'https://www.hdfcfund.com',
          'schemes': ['hdfc-large-cap-fund', 'hdfc-mid-cap-fund', 'hdfc-equity-fund', 'hdfc-focused-fund', 'hdfc-elss-tax-saver-fund']
      },
      'sid': {
          'base_url': 'https://www.hdfcfund.com',
          'schemes': ['hdfc-large-cap-fund', 'hdfc-mid-cap-fund', 'hdfc-equity-fund', 'hdfc-focused-fund', 'hdfc-elss-tax-saver-fund']
      },
      'faqs': {
          'base_url': 'https://www.hdfcfund.com',
          'sections': ['general', 'investment', 'tax', 'redemption']
      },
      'regulatory': {
          'amfi': 'https://www.amfiindia.com',
          'sebi': 'https://www.sebi.gov.in'
      }
  }
  ```

- **Content Processing** ✅ IMPLEMENTED
  - PDF parsing for KIM/SID documents (PyPDF2, pdfplumber)
  - HTML scraping for web pages (BeautifulSoup, Selenium fallback)
  - Text cleaning and normalization (HTML tag removal, whitespace normalization)
  - Metadata extraction (fund name, NAV, expense ratio, category, risk level, etc.)

- **Data Validation Framework** ✅ IMPLEMENTED
  - Required fields validation (fund_name, nav, category)
  - Format validation (NAV format, expense ratio format, date format)
  - Text length validation (min: 50, max: 50000 characters)
  - Quality checks and error reporting

- **Data Storage Structure** ✅ IMPLEMENTED
  ```
  data/raw/
  ├── factsheets/     # HTML content from Groww URLs
  ├── kim/            # Key Information Memorandum PDFs
  ├── sid/            # Scheme Information Documents
  ├── faqs/           # FAQ content from HDFC website
  └── regulatory/     # AMFI/SEBI regulatory documents
  ```

### 1.3 Vector Database Setup ✅ IMPLEMENTED
- **Document Processing Pipeline**
  - **Chunking Strategy**: Sentence-based chunking with configurable overlap
  - **Optimal chunk size**: 800 tokens (as implemented)
  - **Overlap**: 75 tokens (as implemented)
  - **Implementation**: Simple sentence splitting with overlap calculation
  - **Note**: Current implementation uses basic sentence splitting; can be enhanced to semantic chunking

- **Embedding Generation**
  - **Model**: Sentence-Transformers (all-MiniLM-L6-v2)
  - **Batch processing**: Configurable batch sizes for efficiency
  - **Embedding dimension**: 384 dimensions
  - **Data type**: float32
  - **Implementation**: Automatic model download and caching

- **Vector Database Setup**
  - **Database**: ChromaDB with persistent storage
  - **Schema Design**:
  ```python
  collection_schema = {
     'document_id': 'string',
     'content': 'string',
     'metadata': {
         'source': 'string',
         'scheme': 'string',
         'document_type': 'string',
         'last_updated': 'datetime',
         'url': 'string'
     },
     'embedding': 'vector'
  }
  ```

- **Indexing Strategy**
  - **Algorithm**: Hierarchical Navigable Small World (HNSW)
  - **Space**: Cosine similarity
  - **Parameters**: M=16 connections, ef_construction=200, ef_search=50
  - **Implementation**: Configurable indexing parameters

- **Retrieval System**
  - **Query Processing**: Intent classification (factual vs. advisory)
  - **Entity Recognition**: HDFC scheme name recognition
  - **Search Methods**: Semantic similarity search
  - **Metadata Filtering**: Source, scheme, document type filtering
  - **Full-text Integration**: Hybrid search capabilities

- **Database Operations**
  - **Add Documents**: Batch document insertion with embeddings
  - **Query Documents**: Similarity search with metadata filtering
  - **Update Documents**: Existing document updates
  - **Delete Documents**: Document removal from collection
  - **Collection Management**: Create, delete, get collection info

- **Storage Structure**
  ```
  data/embeddings/            # ChromaDB vector database
  ├── chroma.db           # Main database file
  ├── test_mutual_funds/  # Test collection
  └── backup_*.json       # Database backups
  ```

---

### Phase 1.4: Automated Data Collection and Updates ✅ IMPLEMENTED 

### GitHub Actions Integration
- **Automated Workflows**: GitHub Actions for CI/CD and data collection
- **Scheduled Triggers**: 
  - Daily data updates at 2 AM UTC (7:30 AM IST)
  - Weekly full refresh on Sundays at 3 AM UTC (8:30 AM IST)
  - Manual trigger with force refresh option

### Data Collection Workflow
- **Phase 1.1.2**: Automated web scraping from HDFC Groww URLs
- **Phase 1.1.3**: Content processing and text cleaning
- **Phase 1.2**: Data corpus development and validation
- **Phase 1.3**: Vector database setup and indexing
- **Phase 2.1**: Document processing pipeline execution
- **Phase 2.2**: Enhanced vector database operations

### Quality Assurance Workflow
- **Unit Tests**: Multi-Python version testing (3.11, 3.12, 3.13)
- **Integration Tests**: End-to-end phase testing
- **Performance Tests**: Embedding model comparison and benchmarks
- **Code Quality**: Flake8, Black, isort, mypy, bandit, safety checks
- **Security Scanning**: Dependency vulnerability assessment

### Deployment Pipeline
- **Staging Environment**: Automated deployment on develop branch
- **Production Environment**: Automated deployment on main branch
- **Artifact Management**: Data backups and performance reports
- **Monitoring**: Workflow execution summaries and failure notifications

### Workflow Features
- **Manual Triggers**: Force refresh and selective data collection
- **Artifact Storage**: 30-day retention for data, 90-day for backups
- **Performance Monitoring**: Embedding throughput and memory usage tracking
- **Backup Management**: Automated database backups with metadata
- **Error Handling**: Comprehensive logging and notification system

### Configuration Files
- **Data Collection**: `.github/workflows/data-collection.yml`
- **Testing**: `.github/workflows/testing.yml`
- **Environment Variables**: GitHub secrets for sensitive data
- **Schedule Management**: Cron-based triggers with manual override

### Benefits
- **Latest Data**: Always up-to-date mutual fund information
- **Automated Quality**: Continuous testing and validation
- **Reliability**: Automated backups and recovery mechanisms
- **Scalability**: Configurable for different data volumes
- **Monitoring**: Real-time workflow status and performance metrics

---

## Phase 1 Sub-Phases

#### 1.1.1 Environment Setup and Configuration
**Objective**: Establish development environment and configuration management

**Tasks**:
- Create project folder structure with proper separation
- Set up Python virtual environment and dependencies
- Configure environment variables and settings management
- Initialize Git repository and add .gitignore
- Set up Docker containerization (optional)
- Create logging and monitoring infrastructure

**Deliverables**:
- `requirements.txt` with all dependencies
- `.env.example` configuration template
- `src/config/` module with settings management
- `docker-compose.yml` for containerized deployment
- Logging configuration and setup

#### 1.1.2 Web Scraping Implementation
**Objective**: Build robust web scraping for HDFC mutual fund URLs

**Tasks**:
- Implement HTML content extraction from Groww URLs
- Create fallback mechanisms with Selenium for JavaScript-heavy pages
- Add retry logic and error handling for network issues
- Implement rate limiting and respectful scraping practices
- Extract structured data (fund name, NAV, expense ratio, etc.)
- Save raw scraped data with metadata

**Deliverables**:
- `src/data_collection/scraper.py` with HDFCFundScraper class
- Support for both requests and Selenium-based scraping
- Raw data storage in `data/raw/` directory
- Comprehensive error handling and logging

#### 1.1.3 Content Processing and Structuring
**Objective**: Process raw content into structured, searchable format

**Tasks**:
- Implement HTML content cleaning and sanitization
- Create text chunking strategy for optimal embedding
- Extract metadata using pattern matching and NLP
- Handle PDF documents if available
- Create semantic chunks with proper overlap
- Validate and clean extracted data

**Deliverables**:
- `src/data_collection/content_processor.py` with ContentProcessor class
- `src/data_collection/metadata_extractor.py` with MetadataExtractor class
- Processed data storage in `data/processed/` directory
- Metadata validation and quality checks

#### 1.1.4 Vector Database Integration
**Objective**: Set up ChromaDB for vector storage and retrieval

**Tasks**:
- Initialize ChromaDB with proper schema design
- Create document chunk embedding pipeline
- Implement batch processing for efficiency
- Set up metadata filtering capabilities
- Create search and retrieval functions
- Add database backup and recovery mechanisms

**Deliverables**:
- `src/vector_db/` module with ChromaDB integration
- `src/vector_db/schema.py` with data models
- Vector database storage in `data/embeddings/` directory
- Search and retrieval API functions

#### 1.1.5 Testing and Validation
**Objective**: Ensure system reliability and data quality

**Tasks**:
- Create unit tests for all components
- Implement integration tests for end-to-end pipeline
- Add performance benchmarks and monitoring
- Validate data quality and completeness
- Test error scenarios and edge cases
- Create automated test pipeline

**Deliverables**:
- `tests/` directory with comprehensive test suite
- Test coverage reports and validation
- Performance metrics and benchmarks
- Quality assurance procedures

#### 1.1.6 Documentation and Deployment
**Objective**: Complete documentation and deployment preparation

**Tasks**:
- Create comprehensive README with setup instructions
- Document API endpoints and usage examples
- Add troubleshooting guides and FAQ
- Create deployment scripts and Docker setup
- Generate API documentation
- Prepare for Phase 2 transition

**Deliverables**:
- Updated `README.md` with Phase 1 instructions
- `docs/phase1-implementation-guide.md`
- Example usage scripts in `scripts/` directory
- Deployment configuration and Docker setup

---

## Phase 2: RAG System Implementation

### 2.1 Document Processing Pipeline
- **Chunking Strategy**
  - Sentence-based chunking with configurable overlap (current implementation)
  - Optimal chunk size: 800 tokens (as implemented)
  - Overlap: 75 tokens (as implemented)
  - Note: Current implementation uses basic sentence splitting; can be enhanced to semantic chunking
  - Planned enhancement: Semantic chunking based on content sections

- **Embedding Generation**
  - Batch processing for efficiency
  - Embedding caching mechanism
  - Similarity threshold optimization

### 2.2 Vector Database Setup
- **Schema Design**
  ```python
  collection_schema = {
      'document_id': 'string',
      'content': 'string',
      'metadata': {
          'source': 'string',
          'scheme': 'string',
          'document_type': 'string',
          'last_updated': 'datetime',
          'url': 'string'
      },
      'embedding': 'vector'
  }
  ```

- **Indexing Strategy**
  - Hierarchical Navigable Small World (HNSW) indexing
  - Metadata filtering capabilities
  - Full-text search integration

### 2.3 Retrieval System ✅ IMPLEMENTED
- **Query Processing**
  - Intent classification (factual vs. advisory)
  - Query expansion and reformulation
  - Entity recognition for scheme names

- **Search Algorithm**
  - Semantic search with vector similarity
  - Hybrid search (semantic + keyword)
  - Re-ranking using cross-encoders

- **Best Retrieval Strategy for Current Data**
  - **Primary Strategy**: Adaptive Hybrid Search with query-based weighting
  - **Default Configuration**: 70% semantic + 30% keyword
  - **Adaptive Weighting**: 
    - Factual queries: 80% semantic, 20% keyword
    - Entity-specific queries: 40% semantic, 60% keyword
    - Comparative queries: 50% semantic, 50% keyword
  - **Cross-encoder Re-ranking**: Always applied for final optimization
  - **Metadata Filtering**: HDFC fund-specific and document type filtering

- **Performance Optimizations**
  - **Precision@5 Target**: >80% for factual queries
  - **Recall Target**: >70% across all query types
  - **Response Time Target**: <2 seconds for complex queries
  - **Domain-Specific Enhancements**: HDFC fund entity recognition, financial term extraction

---

## Phase 3: Response Generation Engine ✅ IMPLEMENTED

### 3.1 LLM Integration
- **Google AI Studio Integration**
  - **Model**: Gemini Pro (gemini-pro) for response generation
  - **API Key**: Required via GOOGLE_AI_STUDIO_API_KEY environment variable
  - **Rate Limits**: 60 requests per minute (free tier)
  - **Safety Settings**: Enhanced filtering for financial content

- **Prompt Engineering**
  ```python
  system_prompt = """
  You are a mutual fund FAQ assistant powered by Google AI Studio. Rules:
  1. Only answer factual questions about mutual funds
  2. Maximum 3 sentences per response
  3. Include exactly one source citation
  4. Add footer: "Last updated from sources: {date}"
  5. Never provide investment advice or recommendations
  6. For advisory questions, politely refuse and provide educational links
  7. PRIVACY: Never include URLs with personal information
  8. PRIVACY: If answer unknown, do not provide any URLs
  """
  ```

- **Response Validation**
  - Length validation (max 3 sentences)
  - Citation verification
  - Compliance checking for advice content
  - Privacy validation (no personal URLs)
  - Google AI Studio safety filter integration

### 3.2 Compliance Layer
- **Content Filtering**
  - Investment advice detection
  - Performance comparison prevention
  - Personal data protection enforcement
  - URL privacy filtering

- **Source Attribution**
  - Automatic citation linking
  - Source verification
  - Privacy-safe URL generation

### 3.3 Privacy and Safety Constraints
- **Personal Information Protection**
  - No URLs containing personal data
  - No external links for unknown answers
  - Safe educational links only for advisory questions
  - Source validation for all citations

- **Answer Confidence Management**
  - Unknown answer detection
  - Safe fallback responses
  - Educational resource linking
  - Privacy-first approach
  - Date tracking for freshness

---

## Phase 4: User Interface Development

### 4.1 Frontend Architecture
- **Component Structure**
  ```
  src/
  ├── components/
  │   ├── ChatInterface/
  │   ├── MessageDisplay/
  │   ├── SourceCitation/
  │   └── Disclaimer/
  ├── services/
  │   ├── api.js
  │   └── validation.js
  └── utils/
      ├── formatters.js
      └── constants.js
  ```

- **UI/UX Design**
  - Clean, minimal interface
  - Responsive design for mobile/desktop
  - Accessibility compliance (WCAG 2.1)

### 4.2 Backend API
- **Endpoint Design**
  ```python
  @app.post("/api/chat")
  async def chat_endpoint(request: ChatRequest):
      # Query processing
      # Retrieval from vector DB
      # LLM generation
      # Compliance validation
      # Response formatting
  
  @app.get("/api/health")
  async def health_check():
      # System status monitoring
  ```

---

## Phase 5: Security and Compliance

### 5.1 Security Implementation
- **Data Protection**
  - Encryption at rest and in transit
  - Input sanitization
  - Rate limiting and DDoS protection

- **Privacy Controls**
  - No PII collection or storage
  - Session management
  - Audit logging

### 5.2 Regulatory Compliance
- **Financial Regulations**
  - SEBI compliance framework
  - AMFI guidelines adherence
  - Disclaimer management

- **Content Governance**
  - Source verification workflow
  - Content update automation
  - Compliance audit trail

---

## Phase 6: Testing and Quality Assurance

### 6.1 Testing Strategy
- **Unit Testing**
  - Component-level testing
  - API endpoint testing
  - Database operations testing

- **Integration Testing**
  - End-to-end user flows
  - RAG pipeline testing
  - Cross-system integration

### 6.2 Quality Metrics
- **Performance Benchmarks**
  - Response time < 3 seconds
  - Accuracy > 95%
  - Source coverage > 90%

- **Compliance Validation**
  - Advisory query rejection rate: 100%
  - Citation accuracy: 100%
  - Response length compliance: 100%

---

## Phase 7: Deployment and Monitoring

### 7.1 Deployment Architecture
- **Cloud Infrastructure**
  - Container orchestration (Kubernetes)
  - Load balancing
  - Auto-scaling configuration

- **CI/CD Pipeline**
  - Automated testing
  - Staged deployments
  - Rollback mechanisms

### 7.2 Monitoring and Maintenance
- **System Monitoring**
  - Application performance metrics
  - Error tracking and alerting
  - Resource utilization monitoring

- **Content Freshness**
  - Automated source updates
  - Vector database refresh
  - Compliance audit scheduling

---

## Phase 8: Optimization and Scaling

### 8.1 Performance Optimization
- **Caching Strategy**
  - Response caching for common queries
  - Embedding cache management
  - Database query optimization

- **Resource Management**
  - Memory optimization
  - GPU utilization for embeddings
  - Batch processing efficiency

### 8.2 Scalability Planning
- **Horizontal Scaling**
  - Microservices architecture
  - Database sharding
  - CDN integration

- **Feature Expansion**
  - Multi-AMC support
  - Advanced query understanding
  - Personalization (within compliance bounds)

---

## Technology Stack Summary

### Backend
- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Vector DB**: ChromaDB/Pinecone
- **LLM**: OpenAI GPT-4/Claude
- **Embeddings**: Sentence-Transformers

### Frontend
- **Framework**: React/Vue.js
- **Styling**: Tailwind CSS
- **State Management**: Redux/Vuex
- **Build Tool**: Vite/Webpack

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Monitoring**: Prometheus/Grafana
- **Logging**: ELK Stack

### DevOps
- **CI/CD**: GitHub Actions/GitLab CI
- **Version Control**: Git
- **Testing**: Pytest/Jest
- **Documentation**: Swagger/OpenAPI

---

## Success Metrics and KPIs

### Technical Metrics
- **Response Time**: < 3 seconds
- **Availability**: 99.9% uptime
- **Accuracy**: > 95% factual correctness
- **Source Coverage**: > 90% query coverage

### Business Metrics
- **User Satisfaction**: > 4.5/5 rating
- **Query Resolution**: > 90% first-contact resolution
- **Compliance**: 100% regulatory adherence
- **Cost Efficiency**: Optimized token usage

---

## Risk Mitigation

### Technical Risks
- **LLM Hallucination**: Source verification and fact-checking
- **Performance Issues**: Caching and optimization strategies
- **Data Freshness**: Automated update mechanisms

### Compliance Risks
- **Regulatory Changes**: Continuous monitoring framework
- **Advice Generation**: Strict content filtering
- **Data Privacy**: Zero PII collection policy

---

## Future Roadmap

### Short-term (3-6 months)
- Multi-AMC support
- Advanced query understanding
- Mobile application

### Long-term (6-12 months)
- Voice interface integration
- Advanced analytics dashboard
- API ecosystem for third-party integration

This architecture provides a robust, scalable, and compliant foundation for the mutual fund FAQ assistant while ensuring regulatory adherence and optimal user experience.
