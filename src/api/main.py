"""
Main FastAPI application for Mutual Fund FAQ Assistant
"""

import asyncio
import time
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger

from src.config import settings, setup_logging
from src.vector_db.chroma_manager import ChromaManager
from src.llm.google_ai import GoogleAIStudioIntegration
from src.retrieval.adaptive_strategy import AdaptiveRetrievalStrategy
from src.compliance.compliance_check import ComplianceLayer

# Initialize logging
setup_logging()
logger.add("logs/api.log", rotation="1 day", retention="7 days")

app = FastAPI(
    title="HDFC Mutual Fund FAQ Assistant",
    description="RAG-based AI assistant for HDFC Mutual Fund inquiries",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatQuery(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    session_id: Optional[str] = None
    stream: bool = False

class ChatResponse(BaseModel):
    response: str
    source_documents: List[str]
    confidence: float
    intent: str
    metadata: Dict[str, Any]

class HealthStatus(BaseModel):
    status: str
    version: str
    components: Dict[str, str]

# RAG System Wrapper
class RAGSystem:
    def __init__(self):
        self.chroma_manager = ChromaManager()
        self.llm_integration = GoogleAIStudioIntegration()
        self.retrieval_strategy = AdaptiveRetrievalStrategy()
        self.compliance_layer = ComplianceLayer()
        self.llm_timeout_seconds = 25
        
    async def process_query(self, query: str) -> Dict[str, Any]:
        """End-to-end RAG pipeline processing"""
        start_time = time.time()
        
        try:
            # Step 1: Query classification and intent extraction
            query_intent = self.retrieval_strategy.classify_query(query)
            
            # Step 2: Get adaptive weights
            weights = self.retrieval_strategy.get_adaptive_weights(query)
            
            # Step 3: Retrieve documents
            search_results = await self._retrieve_documents(query, weights)
            
            # Step 4: Generate response
            try:
                response_data = await asyncio.wait_for(
                    asyncio.to_thread(
                        self.llm_integration.generate_response,
                        query, search_results, query_intent
                    ),
                    timeout=self.llm_timeout_seconds
                )
            except asyncio.TimeoutError:
                logger.warning(f"LLM timed out after {self.llm_timeout_seconds}s, using local fallback")
                response_data = {
                    'response': self.llm_integration.generate_timeout_fallback(query, search_results),
                    'source_documents': [res.get('id', 'unknown') for res in search_results[:2]],
                    'confidence': self.llm_integration._calculate_confidence(search_results),
                    'intent': query_intent,
                    'model_used': 'local_timeout_fallback'
                }
            
            # Step 4.5: Log response generation details
            logger.info(f"LLM used: {response_data.get('model_used', 'unknown')}")
            logger.info(f"Response Intent: {response_data['intent']}")
            logger.info(f"Response Confidence: {response_data['confidence']:.2f}")
            
            # Step 5: Compliance validation
            compliance_result = await asyncio.to_thread(
                self.compliance_layer.check_response_compliance,
                response_data['response']
            )
            
            if not compliance_result['is_compliant']:
                response_data['response'] = compliance_result['sanitized_response']
                response_data['metadata'] = {
                    'compliance_flag': True,
                    'original_intent': query_intent
                    
                }
            
            # Step 6: Final formatting
            execution_time = time.time() - start_time
            response_data['metadata'] = {
                'processing_time': execution_time,
                'retrieval_weights': weights
            }
            
            return response_data
            
        except Exception as e:
            logger.error(f"RAG pipeline error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def _retrieve_documents(self, query: str, weights: Dict[str, float]) -> List[Dict[str, Any]]:
        """Retrieve documents from vector database"""
        return await asyncio.to_thread(self._retrieve_documents_sync, query, weights)

    def _retrieve_documents_sync(self, query: str, weights: Dict[str, float]) -> List[Dict[str, Any]]:
        """Retrieve documents from vector database without blocking the event loop."""
        try:
            # Perform real search in ChromaDB
            results = self.chroma_manager.search_similar(query, n_results=5)
            
            # Convert SearchResult objects to dicts for LLM integration
            formatted_results = []
            for res in results:
                formatted_results.append({
                    'id': res.id,
                    'content': res.text,
                    'metadata': res.metadata,
                    'similarity_score': res.similarity_score
                })
            
            # Apply HDFC-specific optimization for adaptive reranking
            optimized_results = self.retrieval_strategy.optimize_for_hdfc_data(query, formatted_results)
            # Take top 5 optimized results
            final_results = optimized_results[:5]
            
            # Log retrieved documents for debugging
            if final_results:
                logger.info(f"Retrieved {len(final_results)} documents from ChromaDB after weighting")
                for i, res in enumerate(final_results):
                    logger.debug(f"Doc {i+1}: ID={res['id']}, FinalScore={res.get('final_score', 0):.4f}, Source={res['metadata'].get('source_url', 'unknown')}")
            else:
                logger.warning(f"No relevant documents found for query: {query}")
            
            return final_results
            
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return []

# Initialize RAG system
rag_system = RAGSystem()

# Endpoints
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(query_data: ChatQuery, background_tasks: BackgroundTasks):
    """Primary chat endpoint for the RAG assistant"""
    logger.info(f"Processing query: {query_data.query[:50]}...")
    
    response = await rag_system.process_query(query_data.query)
    
    # Log analytics in background
    background_tasks.add_task(log_analytics, query_data.query, response)
    
    return ChatResponse(
        response=response['response'],
        source_documents=response['source_documents'],
        confidence=response['confidence'],
        intent=response['intent'],
        metadata=response['metadata']
    )

@app.get("/api/health", response_model=HealthStatus)
async def health_check():
    """System health check endpoint"""
    return HealthStatus(
        status="healthy",
        version="1.0.0",
        components={
            "vector_db": "connected",
            "llm_service": "active",
            "compliance_engine": "ready"
        }
    )

async def log_analytics(query: str, response: Dict[str, Any]):
    """Background task for logging analytics"""
    logger.info(f"Analytics: Query='{query[:20]}...', Intent='{response['intent']}', Time={response['metadata']['processing_time']:.2f}s")

@app.on_event("startup")
async def startup_event():
    """Actions to perform on startup"""
    logger.info("RAG System API is starting up...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
