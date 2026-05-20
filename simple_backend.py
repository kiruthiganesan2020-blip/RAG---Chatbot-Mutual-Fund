#!/usr/bin/env python3
"""
Simple Backend Server for Testing
HDFC Mutual Fund RAG System
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import time
import asyncio
import json

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Install with: pip install fastapi uvicorn pydantic")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="HDFC Mutual Fund RAG API",
    description="Backend API for HDFC Mutual Fund FAQ System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="User query")
    session_id: str = Field(default="test_session", description="Session identifier")
    user_id: str | None = Field(default="test_user", description="User identifier")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Generated response")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence")
    sources: list = Field(default_factory=list, description="Source citations")
    intent: str = Field(..., description="Query intent")
    model_used: str = Field(..., description="LLM model used")
    response_time: float = Field(..., description="Response time in seconds")
    timestamp: str = Field(..., description="Response timestamp")

class HealthResponse(BaseModel):
    status: str = Field(..., description="System status")
    version: str = Field(..., description="API version")
    components: dict = Field(..., description="Component statuses")
    uptime: float = Field(..., description="System uptime in seconds")
    timestamp: str = Field(..., description="Health check timestamp")

# Global variables
start_time = time.time()
frontend_dir = Path(__file__).parent / "frontend"
frontend_src_dir = frontend_dir / "src"

# Mock responses for testing
MOCK_RESPONSES = {
    "hdfc": "HDFC Mutual Fund is one of India's leading asset management companies offering various mutual fund schemes including equity, debt, and hybrid funds.",
    "large cap": "HDFC Large Cap Fund invests primarily in large-cap companies with market capitalization ranking within the top 100 companies.",
    "mid cap": "HDFC Mid-Cap Fund focuses on investing in mid-sized companies that have the potential to become large-cap companies.",
    "equity": "HDFC Equity Fund is an open-ended equity scheme investing across market capitalization.",
    "nav": "NAV (Net Asset Value) represents the per-unit value of a mutual fund scheme. Current NAVs are available on the HDFC website.",
    "investment": "To invest in HDFC mutual funds, you can visit the HDFC website, use online platforms, or consult with a financial advisor.",
    "risk": "All mutual fund investments are subject to market risks. Please read the scheme information document carefully before investing.",
    "default": "I can help you with factual information about HDFC mutual funds. Please ask specific questions about funds, NAV, investment process, or scheme details."
}

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        uptime = time.time() - start_time
        
        components = {
            "api": "healthy",
            "database": "mock_mode",
            "llm": "mock_mode"
        }
        
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            components=components,
            uptime=uptime,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for processing user queries"""
    try:
        # Log the incoming request for debugging
        print(f"=== DEBUG: Incoming request ===")
        print(f"Query: '{request.query}'")
        print(f"Session ID: '{request.session_id}'")
        print(f"User ID: '{request.user_id}'")
        print(f"Request model: {request.model_dump()}")
        
        start_time_req = time.time()
        
        # Validate request manually
        if not request.query or len(request.query.strip()) == 0:
            print("ERROR: Empty query detected")
            raise HTTPException(status_code=422, detail="Message cannot be empty")
        
        if len(request.query.strip()) < 3:
            print(f"ERROR: Query too short: {len(request.query.strip())}")
            raise HTTPException(status_code=422, detail="Message must be at least 3 characters long")
        
        # Process query (mock implementation)
        query_lower = request.query.lower()
        response_text = MOCK_RESPONSES["default"]
        confidence = 0.5
        intent = "factual"
        
        # Find matching response
        for key, response in MOCK_RESPONSES.items():
            if key in query_lower:
                response_text = response
                confidence = 0.8
                break
        
        # Generate response
        response_time = time.time() - start_time_req
        
        print(f"=== DEBUG: Sending response ===")
        print(f"Response: '{response_text}'")
        print(f"Confidence: {confidence}")
        print(f"Intent: {intent}")
        print(f"Response time: {response_time}")
        
        return ChatResponse(
            response=response_text,
            confidence=confidence,
            sources=["HDFC Mutual Fund"],
            intent=intent,
            model_used="mock_model",
            response_time=response_time,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        print(f"ERROR: Exception in chat_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    try:
        stats = {
            "total_queries": 0,
            "avg_response_time": 0.0,
            "system_uptime": time.time() - start_time,
            "components": {"api": "running", "database": "mock", "llm": "mock"},
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(content=stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")

@app.get("/")
async def root():
    """Serve the frontend when available, otherwise expose API metadata."""
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)

    return {
        "message": "HDFC Mutual Fund RAG API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

if frontend_src_dir.exists():
    app.mount("/src", StaticFiles(directory=frontend_src_dir), name="frontend-src")

def main():
    """Main function"""
    print("HDFC Mutual Fund RAG Simple Backend")
    print("=" * 50)
    print("Starting simple backend server...")
    print("Note: This is a mock server for testing")
    port = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))

    print(f"Frontend URL: http://localhost:{port}")
    print(f"Backend URL: http://localhost:{port}")
    print(f"API Documentation: http://localhost:{port}/docs")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()
