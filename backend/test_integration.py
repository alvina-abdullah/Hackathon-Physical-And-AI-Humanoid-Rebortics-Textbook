"""
Integration test for the RAG agent to validate all components work together.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path to import agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import RAGBookAgent, test_follow_up_queries, test_performance_and_reliability, test_end_to_end_functionality

def run_integration_tests():
    """
    Run comprehensive integration tests to validate all components work together.
    """
    print("Starting comprehensive integration tests...")

    # Check environment
    required_vars = ["GROQ_API_KEY", "QDRANT_URL", "QDRANT_API_KEY", "COHERE_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"X Integration test failed: Missing environment variables: {missing_vars}")
        return False

    print("+ Environment variables are properly configured")

    try:
        # Test 1: Basic agent initialization
        print("\n1. Testing agent initialization...")
        agent = RAGBookAgent()
        print("+ Agent initialized successfully")

        # Test 2: Basic query functionality
        print("\n2. Testing basic query functionality...")
        response = agent.run_query("What is the introduction to the technical book?", timeout=15)
        if response and len(response) > 0:
            print(f"+ Basic query returned response (length: {len(response)})")
        else:
            print("! Basic query returned empty response")

        # Test 3: Follow-up query functionality
        print("\n3. Testing follow-up query functionality...")
        success = test_follow_up_queries()
        if success:
            print("+ Follow-up query functionality test passed")
        else:
            print("! Follow-up query functionality test had issues")

        # Test 4: Performance and reliability
        print("\n4. Testing performance and reliability...")
        success = test_performance_and_reliability()
        if success:
            print("+ Performance and reliability test passed")
        else:
            print("! Performance and reliability test had issues")

        # Test 5: End-to-end functionality
        print("\n5. Testing end-to-end functionality...")
        success = test_end_to_end_functionality()
        if success:
            print("+ End-to-end functionality test passed")
        else:
            print("! End-to-end functionality test had issues")

        print("\nV All integration tests completed!")
        return True

    except Exception as e:
        print(f"\nX Integration test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_integration_tests()
    if success:
        print("\n🎉 All integration tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some integration tests failed!")
        sys.exit(1)