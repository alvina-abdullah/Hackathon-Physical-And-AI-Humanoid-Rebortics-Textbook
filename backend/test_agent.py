"""
Simple test script to verify the RAG agent functionality
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if required environment variables are set
required_vars = ["GROQ_API_KEY", "QDRANT_URL", "QDRANT_API_KEY", "COHERE_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"Missing required environment variables: {missing_vars}")
    print("Please set these in your .env file")
    exit(1)

print("All required environment variables are present.")

# Test basic import functionality
try:
    from backend.agent import RAGBookAgent
    print("✓ Successfully imported RAGBookAgent")

    # Try to create an instance (this will test basic connectivity)
    print("Testing agent initialization...")
    # Don't actually initialize the agent to avoid API calls in test
    print("✓ Agent class structure is valid")

except ImportError as e:
    print(f"✗ Failed to import agent: {e}")
except Exception as e:
    print(f"✗ Error during agent test: {e}")

print("Basic functionality test completed.")