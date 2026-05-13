# Phase 4.1: Backend API Development

## Overview

Phase 4.1 implements the complete FastAPI backend for the HDFC Mutual Fund RAG system, providing RESTful endpoints for chat interactions, health monitoring, and system management.

## Architecture

### Core Components

1. **FastAPI Application** (`simple_backend.py`)
   - High-performance async web framework
   - Automatic API documentation with Swagger/OpenAPI
   - Built-in request validation and serialization
   - CORS support for frontend integration

2. **API Endpoints**
   - `POST /api/chat` - Main chat endpoint for RAG queries
   - `GET /api/health` - Health check and system status
   - `GET /api/stats` - System statistics and metrics
   - `GET /docs` - Interactive API documentation

3. **Request/Response Models**
   - `ChatRequest` - Input validation with Pydantic
   - `ChatResponse` - Structured response format
   - Error handling with proper HTTP status codes

## Implementation Details

### Chat Endpoint (`/api/chat`)

**Purpose**: Process user queries through the complete RAG pipeline

**Request Format**:
```json
{
  "query": "What is the NAV of HDFC Large Cap Fund?",
  "session_id": "user_session_123",
  "user_id": "optional_user_id"
}
```

**Response Format**:
```json
{
  "response": "The current NAV of HDFC Large Cap Fund is ₹125.45...",
  "confidence": 0.85,
  "sources": ["HDFC Large Cap Fund Factsheet"],
  "intent": "factual",
  "model_used": "google_gemini_pro",
  "response_time": 1.23,
  "timestamp": "2026-05-09T16:30:00Z"
}
```

**Features**:
- Input validation (min/max length constraints)
- Session management for conversation context
- Intent classification (factual vs advisory)
- Source citation and confidence scoring
- Response time tracking
- Error handling with meaningful messages

### Health Check Endpoint (`/api/health`)

**Purpose**: Monitor system health and component status

**Response Format**:
```json
{
  "status": "healthy",
  "timestamp": "2026-05-09T16:30:00Z",
  "version": "1.0.0",
  "components": {
    "vector_db": "healthy",
    "embedding_model": "healthy",
    "llm_service": "healthy",
    "data_pipeline": "healthy"
  },
  "uptime": 86400,
  "total_requests": 1250
}
```

### Statistics Endpoint (`/api/stats`)

**Purpose**: Provide system performance metrics

**Response Format**:
```json
{
  "total_requests": 1250,
  "successful_requests": 1198,
  "failed_requests": 52,
  "average_response_time": 1.45,
  "cache_hit_rate": 0.78,
  "vector_db_size": 1250,
  "last_updated": "2026-05-09T16:30:00Z"
}
```

## Configuration

### Environment Variables

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false

# LLM Configuration
GOOGLE_AI_STUDIO_API_KEY=your_api_key_here
LLM_MODEL=google_gemini_pro

# Vector Database Configuration
CHROMA_DB_PATH=/app/data/chroma
EMBEDDING_MODEL=sentence_transformers

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=/app/logs/api.log
```

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Security Features

### Input Validation
- Query length constraints (3-500 characters)
- SQL injection prevention
- XSS protection
- Rate limiting per IP

### Error Handling
- Structured error responses
- Proper HTTP status codes
- Sensitive information filtering
- Graceful degradation for service failures

### Authentication (Future Enhancement)
- JWT token support planned
- API key authentication
- User session management

## Performance Optimizations

### Async Processing
- Non-blocking I/O operations
- Concurrent request handling
- Connection pooling for database operations

### Caching Strategy
- Response caching for common queries
- Embedding cache for repeated documents
- Session state management

### Database Optimization
- Connection pooling
- Query optimization
- Batch processing for embeddings

## Monitoring and Logging

### Request Logging
```python
logger.info(f"Chat request: {request.query} (session: {request.session_id})")
logger.info(f"Response generated in {response_time:.2f}s")
```

### Error Tracking
```python
logger.error(f"Request failed: {error_type} - {error_message}")
```

### Performance Metrics
- Response time tracking
- Error rate monitoring
- Resource usage statistics
- Cache hit/miss ratios

## Deployment

### Docker Configuration
```dockerfile
# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Startup command
CMD ["python", "simple_backend.py"]
```

### Environment Setup
1. **Development**: `python simple_backend.py`
2. **Production**: `uvicorn simple_backend:app --host 0.0.0.0 --port 8000`
3. **Docker**: `docker run -p 8000:8000 hdfc-rag-system`

## Integration Points

### Frontend Integration
- CORS-enabled endpoints
- JSON API responses
- Error handling for frontend consumption
- Real-time response streaming (planned)

### Vector Database Integration
- ChromaDB connection management
- Embedding generation and storage
- Semantic search capabilities

### LLM Integration
- Google AI Studio API integration
- Prompt engineering for mutual funds
- Response validation and filtering

## Testing

### Unit Tests
```python
def test_chat_endpoint():
    response = client.post("/api/chat", json={
        "query": "What is HDFC Large Cap Fund?",
        "session_id": "test_session"
    })
    assert response.status_code == 200
    assert "response" in response.json()
```

### Load Testing
- Concurrent request handling
- Memory usage monitoring
- Response time benchmarks
- Error rate validation

## Troubleshooting

### Common Issues

1. **422 Validation Errors**
   - Check query length constraints
   - Verify JSON format
   - Validate session_id format

2. **Connection Refused**
   - Verify port availability
   - Check firewall settings
   - Confirm API host configuration

3. **Slow Response Times**
   - Monitor vector database performance
   - Check LLM API latency
   - Review caching effectiveness

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

### Phase 4.1.1: Advanced Features
- WebSocket support for real-time chat
- File upload for document analysis
- Multi-language support

### Phase 4.1.2: Performance
- Response streaming
- Advanced caching strategies
- Horizontal scaling support

### Phase 4.1.3: Security
- OAuth 2.0 integration
- API rate limiting
- Advanced input sanitization

---

**Status**: ✅ Completed
**Last Updated**: 2026-05-09
**Version**: 1.0.0
