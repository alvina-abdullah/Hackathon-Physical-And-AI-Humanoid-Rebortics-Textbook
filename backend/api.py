"""
FastAPI backend for RAG Chatbot integration.

This module provides API endpoints for the frontend to communicate with the RAG agent.
"""
import os
import uuid
import time
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import the RAG agent
from agent import RAGBookAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="The user's question or query")
    sessionId: Optional[str] = Field(None, description="Session identifier for conversation context")


class Source(BaseModel):
    title: str = Field(..., description="Title of the source document")
    url: str = Field(..., description="URL of the source document")
    contentPreview: str = Field(..., description="Preview of the content used from the source")


class QueryResponse(BaseModel):
    response: str = Field(..., description="The RAG agent's response to the query")
    sources: List[Source] = Field(default=[], description="List of sources used in the response")
    sessionId: str = Field(..., description="Session identifier for conversation continuity")
    timestamp: str = Field(..., description="ISO 8601 timestamp of response generation")
    status: str = Field("success", description="Status of the query processing")


class HealthResponse(BaseModel):
    status: str = Field("healthy", description="Health status of the API")
    timestamp: str = Field(..., description="ISO 8601 timestamp")


# Global variable to hold the RAG agent instance
rag_agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the RAG agent when the application starts."""
    global rag_agent
    logger.info("Starting up RAG Chatbot API...")

    try:
        # Initialize the RAG agent
        rag_agent = RAGBookAgent()
        logger.info("RAG agent initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize RAG agent: {e}")
        raise
    finally:
        logger.info("Shutting down RAG Chatbot API...")


# Create FastAPI app with lifespan
app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG Chatbot integration with frontend",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Default Docusaurus dev server
        "http://localhost:5000",  # Alternative dev server
        "http://localhost:8080",  # Another common dev server
        "http://127.0.0.1:3000",  # IPv4 localhost
        "http://127.0.0.1:5000",  # IPv4 alternative
        "http://127.0.0.1:8080",  # IPv4 another common
        "http://localhost:3001",  # Docusaurus live reload
        "http://127.0.0.1:3001",  # Docusaurus live reload IPv4
    ],  # In production, add your production domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API is running."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/api/chat", response_model=QueryResponse)
async def chat_endpoint(request: QueryRequest):
    """
    Process user query through the RAG agent and return response with sources.
    """
    global rag_agent

    if not rag_agent:
        logger.error("RAG agent not initialized")
        raise HTTPException(status_code=500, detail="RAG agent not initialized")

    try:
        # Validate session ID if provided
        if request.sessionId:
            try:
                uuid.UUID(request.sessionId)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid session ID format")

        # Generate a new session ID if not provided
        session_id = request.sessionId or str(uuid.uuid4())

        logger.info(f"Processing query: {request.query[:50]}... for session {session_id}")

        # Process the query using the RAG agent
        start_time = time.time()

        # Integrate with the actual RAG agent (now returns dict with response and sources)
        agent_response = rag_agent.run_query(request.query)

        # Create response object with actual response and sources from the agent
        response_obj = QueryResponse(
            response=agent_response["response"],
            sources=agent_response["sources"],
            sessionId=session_id,
            timestamp=datetime.utcnow().isoformat(),
            status="success"
        )

        processing_time = time.time() - start_time
        logger.info(f"Query processed in {processing_time:.2f}s for session {session_id}")

        return response_obj

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "RAG Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/health": "Health check endpoint",
            "POST /api/chat": "Chat endpoint for processing queries"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)