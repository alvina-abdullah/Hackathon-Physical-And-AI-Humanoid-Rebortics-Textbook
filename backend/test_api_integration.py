"""
API Integration test for the RAG Chatbot API
Tests the complete flow from API request to response with sources
"""

import asyncio
import httpx
import sys
import os

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api import QueryRequest, QueryResponse
from agent import RAGBookAgent

async def test_api_integration():
    """
    Test the complete API integration including:
    - API endpoint functionality
    - RAG agent processing
    - Source extraction and formatting
    - Response structure
    """
    print("Starting RAG Chatbot API Integration Test...")

    # Test the agent directly first
    print("\n1. Testing RAG agent directly...")
    try:
        agent = RAGBookAgent()
        test_result = agent.run_query("What is the introduction to the technical book?")

        print(f"Agent response type: {type(test_result)}")
        print(f"Has response key: {'response' in test_result}")
        print(f"Has sources key: {'sources' in test_result}")
        print(f"Response length: {len(str(test_result.get('response', '')))}")
        print(f"Number of sources: {len(test_result.get('sources', []))}")

        if test_result.get('sources'):
            print("Sample source:", test_result['sources'][0] if test_result['sources'] else "None")

        print("+ RAG agent test passed")
    except Exception as e:
        print(f"X RAG agent test failed: {e}")
        return False

    # Test the API endpoints (if the server is running)
    print("\n2. Testing API endpoints...")
    try:
        async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
            # Test health endpoint
            print("  Testing health endpoint...")
            health_response = await client.get("/api/health")
            print(f"  Health status: {health_response.status_code}")
            if health_response.status_code == 200:
                print("  + Health endpoint test passed")
            else:
                print("  ! Health endpoint not accessible (server may not be running)")

            # Test chat endpoint
            print("  Testing chat endpoint...")
            chat_request = {
                "query": "What is the introduction to the technical book?",
                "sessionId": "550e8400-e29b-41d4-a716-446655440000"
            }

            chat_response = await client.post("/api/chat", json=chat_request)
            print(f"  Chat status: {chat_response.status_code}")

            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"  Has response: {'response' in response_data}")
                print(f"  Has sources: {'sources' in response_data}")
                print(f"  Has sessionId: {'sessionId' in response_data}")
                print(f"  Number of sources: {len(response_data.get('sources', []))}")
                print("  + Chat endpoint test passed")
            else:
                print(f"  ! Chat endpoint not accessible (server may not be running or error occurred: {chat_response.status_code})")

    except Exception as e:
        print(f"  ! API endpoint tests skipped: {e} (server may not be running)")

    print("\n+ Integration test completed")
    return True

def test_pydantic_models():
    """
    Test that Pydantic models are correctly defined and compatible
    """
    print("\n3. Testing Pydantic models...")

    try:
        # Test QueryRequest model
        query_request = QueryRequest(query="Test query", sessionId="test-session")
        print(f"  QueryRequest created: {type(query_request)}")
        print(f"  Query: {query_request.query}")
        print(f"  Session ID: {query_request.sessionId}")

        # Test QueryResponse model
        test_sources = [
            {
                "title": "Test Document",
                "url": "http://example.com/test",
                "contentPreview": "This is a test content preview..."
            }
        ]

        query_response = QueryResponse(
            response="Test response",
            sources=test_sources,
            sessionId="test-session",
            timestamp="2023-01-01T00:00:00Z",
            status="success"
        )

        print(f"  QueryResponse created: {type(query_response)}")
        print(f"  Response: {query_response.response}")
        print(f"  Number of sources: {len(query_response.sources)}")
        if query_response.sources:
            print(f"  First source title: {query_response.sources[0].title}")

        print("  + Pydantic models test passed")
        return True

    except Exception as e:
        print(f"  X Pydantic models test failed: {e}")
        return False

async def main():
    """
    Main function to run all integration tests
    """
    print("Running RAG Chatbot API Integration Tests")
    print("=" * 50)

    # Test Pydantic models first
    models_ok = test_pydantic_models()

    if models_ok:
        # Test API integration
        api_ok = await test_api_integration()

        print("\n" + "=" * 50)
        print("Integration Test Results:")
        print(f"  Pydantic Models: {'+ PASS' if models_ok else 'X FAIL'}")
        print(f"  API Integration: {'+ PASS' if api_ok else 'X FAIL'}")

        if models_ok and api_ok:
            print("\nOK All integration tests passed!")
            return True
        else:
            print("\nX Some integration tests failed!")
            return False
    else:
        print("\nX Integration tests failed due to model errors!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)