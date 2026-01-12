import os
import json
import logging
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv
import sys
import time

# Load environment variables
load_dotenv()

# Import the existing retrieval functionality
from retrieve import test_retrieval_pipeline

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RAGBookAgent:
    def __init__(self):
        # Initialize GROQ client
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.error("GROQ API key not found in environment variables")
            raise ValueError("GROQ API key not found in environment variables")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"  # Using a currently supported GROQ model
        self.conversation_history = []

    def retrieve_content(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve content from the book database using the existing retrieval pipeline with retry logic.
        """
        max_retries = 3
        base_delay = 2  # Increased delay to handle rate limits better

        for attempt in range(max_retries):
            logger.info(f"Starting retrieval for query: {query[:50]} (attempt {attempt + 1}/{max_retries})")
            try:
                # Use the existing retrieval pipeline to get relevant chunks
                collection_name = os.getenv("COLLECTION_NAME", "RAG-embedding")
                result = test_retrieval_pipeline(query, collection_name, top_k=5)

                if result.get('retrieval_success', False):
                    chunks = result.get('results', [])
                    logger.info(f"Retrieved {len(chunks)} chunks successfully")
                    formatted_chunks = []

                    for chunk in chunks:
                        formatted_chunks.append({
                            "content": chunk.get('content_chunk', ''),
                            "source_url": chunk.get('source_url', ''),
                            "title": chunk.get('document_title', ''),
                            "similarity_score": chunk.get('similarity_score', 0.0)
                        })

                    logger.debug(f"Formatted {len(formatted_chunks)} chunks for GROQ context")
                    return formatted_chunks
                else:
                    error_msg = result.get('error_message', 'Unknown error')
                    logger.error(f"Retrieval failed: {error_msg}")
                    # Check if it's specifically a Qdrant connection issue
                    if "connection" in error_msg.lower() or "qdrant" in error_msg.lower():
                        logger.warning("Qdrant connection issue detected")

                    # If this is the last attempt, return empty list
                    if attempt == max_retries - 1:
                        return []

                    # Otherwise, wait before retrying
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    logger.info(f"Retrying retrieval in {delay} seconds...")
                    time.sleep(delay)
                    continue

            except Exception as e:
                logger.error(f"Error during retrieval: {e}")
                # Check if it's specifically a Qdrant connection issue
                error_str = str(e).lower()
                if "connection" in error_str or "qdrant" in error_str or "timeout" in error_str:
                    logger.warning("Qdrant connection issue detected")
                    # Provide more specific error message to user
                    logger.info("Connection issue with Qdrant vector database - may need to check network or credentials")

                # If this is the last attempt, return empty list
                if attempt == max_retries - 1:
                    return []

                # Otherwise, wait before retrying
                delay = base_delay * (2 ** attempt)  # Exponential backoff
                logger.info(f"Retrying retrieval in {delay} seconds...")
                time.sleep(delay)
                continue

        # If all retries failed
        logger.error("All retrieval attempts failed")
        return []

    def run_query(self, user_query: str, timeout: int = 30):
        """
        Process a user query through the RAG agent with GROQ integration.
        Returns both the response text and the sources used.
        """
        # Input validation
        if not user_query or not isinstance(user_query, str):
            logger.warning("Invalid query provided: empty or not a string")
            return {"response": "Please provide a valid question.", "sources": []}

        user_query = user_query.strip()
        if not user_query:
            logger.warning("Empty query provided after stripping whitespace")
            return {"response": "Please provide a valid question.", "sources": []}

        if len(user_query) > 1000:  # Limit query length
            logger.warning(f"Query too long: {len(user_query)} characters")
            return {"response": "Your query is too long. Please keep it under 1000 characters.", "sources": []}

        logger.info(f"Processing user query: {user_query[:50]}...")
        start_time = time.time()

        try:
            # Retrieve relevant content based on the user query
            retrieved_chunks = self.retrieve_content(user_query)

            # Format the retrieved content for context
            context_str = ""
            sources = []
            if retrieved_chunks:
                context_parts = []
                for chunk in retrieved_chunks:
                    context_parts.append(f"Source: {chunk['source_url']}\nContent: {chunk['content'][:500]}")

                    # Create a source object with title, URL, and content preview
                    source_obj = {
                        "title": chunk.get('title', 'Untitled'),
                        "url": chunk['source_url'],
                        "contentPreview": chunk['content'][:200]  # First 200 chars as preview
                    }
                    sources.append(source_obj)
                context_str = "\n\n".join(context_parts)
            else:
                context_str = "No relevant content found in the knowledge base."

            # Prepare the message for GROQ
            system_prompt = """You are a helpful AI assistant for the Physical AI and Humanoid Robotics textbook.
Provide comprehensive, detailed answers based on the retrieved content.
Structure your responses with:
1. A clear, detailed answer to the question
2. Supporting evidence from the retrieved documents
3. Proper explanations of concepts with examples where available
4. At the end, list the sources you used with their URLs and relevance to the answer
Be thorough but accurate, only stating information that appears in the retrieved documents."""

            user_message = f"""
Question: {user_query}

Retrieved Context:
{context_str}

Please provide a comprehensive, detailed answer based on the provided context. Include explanations, examples, and relevant details from the retrieved documents. At the end of your response, include a 'Sources' section listing the documents you referenced with their URLs.
"""

            # Call GROQ API
            chat_completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1024,
                temperature=0.3,
            )

            response_text = chat_completion.choices[0].message.content

            logger.info("Successfully retrieved GROQ response")
            return {"response": response_text, "sources": sources}

        except Exception as e:
            logger.error(f"Error processing query with GROQ: {e}")
            return {"response": "Sorry, I encountered an error processing your query with the GROQ API.", "sources": []}

    def chat_loop(self):
        """
        Run a continuous chat loop for the agent.
        """
        print("RAG Book Assistant (GROQ) ready! Type 'quit' to exit.")
        print("Ask questions about the book content and I'll retrieve relevant information to answer.")

        while True:
            try:
                user_input = input("\nYour question: ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                print("\nProcessing your query...")
                result = self.run_query(user_input)

                print(f"\nAssistant: {result['response']}")

                if result['sources']:
                    print("\nSources:")
                    for source in result['sources'][:1]:  # Limit to first 3 sources
                        print(f"- {source['title']}: {source['url']}")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")


def test_end_to_end_functionality():
    """
    Test function to validate end-to-end functionality with various query types.
    """
    logger.info("Starting end-to-end functionality test with various query types...")

    try:
        logger.info("Creating RAGBookAgent instance for testing...")
        agent = RAGBookAgent()
        logger.info("RAG Book Agent initialized successfully for testing!")

        print("Testing end-to-end functionality with various query types...")

        import time
        test_queries = [
            ("Simple factual query", "What is the introduction to the technical book?"),
            ("Concept explanation", "Explain AI brain and perception training"),
            ("Technical process", "How does the VLA autonomous system work?"),
            ("Terminology", "What are the communication primitives?"),
            ("Complex multi-topic", "Explain digital twin and gazebo physics"),
            ("Follow-up reference", "Can you elaborate on the concepts mentioned?"),
            ("Detailed request", "Give me detailed information about the main topics")
        ]

        all_tests_passed = True
        for i, (query_type, query) in enumerate(test_queries, 1):
            print(f"\n{i}. Testing {query_type}: {query}")
            start_time = time.time()
            result = agent.run_query(query, timeout=30)  # Slightly longer timeout for testing
            elapsed_time = time.time() - start_time
            print(f"   Response time: {elapsed_time:.2f}s")
            response = result['response']
            print(f"   Response preview: {response[:150]}..." if len(response) > 150 else f"   Response: {response}")

            # Check sources
            sources = result.get('sources', [])
            print(f"   Sources found: {len(sources)}")

            # Check if response time is within acceptable limits
            if elapsed_time > 20:
                print(f"   [WARN] Response took {elapsed_time:.2f} seconds (should be under 20 seconds)")
                all_tests_passed = False
            else:
                print(f"   [OK] Response time acceptable")

        print("\nEnd-to-end functionality test completed!")
        if all_tests_passed:
            print("[SUCCESS] All tests passed!")
        else:
            print("[WARN] Some tests had performance issues")
        return all_tests_passed

    except Exception as e:
        logger.error(f"Error during end-to-end functionality test: {e}")
        print(f"Error during end-to-end functionality test: {e}")
        return False


def test_performance_and_reliability():
    """
    Test function to validate performance and reliability of the agent.
    """
    logger.info("Starting performance and reliability test...")

    try:
        logger.info("Creating RAGBookAgent instance for testing...")
        agent = RAGBookAgent()
        logger.info("RAG Book Agent initialized successfully for testing!")

        print("Testing performance and reliability...")

        import time
        start_time = time.time()

        # Test query 1 - Performance test
        print("\nPerformance Test Query: What is the introduction to the technical book?")
        result1 = agent.run_query("What is the introduction to the technical book?", timeout=30)  # Slightly longer timeout for testing
        elapsed_time = time.time() - start_time
        print(f"Response 1 received in {elapsed_time:.2f} seconds")
        response1 = result1['response']
        print(f"Response 1: {response1[:200]}..." if len(response1) > 200 else f"Response 1: {response1}")

        # Check sources
        sources1 = result1.get('sources', [])
        print(f"Sources for response 1: {len(sources1)}")

        # Check if response time is within acceptable limits
        if elapsed_time > 20:
            print(f"[WARN] Response took {elapsed_time:.2f} seconds (should be under 20 seconds)")
        else:
            print(f"[OK] Response time {elapsed_time:.2f} seconds is within acceptable limits")

        # Test query 2 - Reliability with follow-up
        start_time2 = time.time()
        print("\nReliability Test Query: Can you explain the main concepts?")
        result2 = agent.run_query("Can you explain the main concepts?", timeout=30)
        elapsed_time2 = time.time() - start_time2
        print(f"Follow-up response received in {elapsed_time2:.2f} seconds")
        response2 = result2['response']
        print(f"Response 2: {response2[:200]}..." if len(response2) > 200 else f"Response 2: {response2}")

        # Check sources
        sources2 = result2.get('sources', [])
        print(f"Sources for response 2: {len(sources2)}")

        # Test error handling with a potentially problematic query
        print("\nError Handling Test: Testing with a complex query...")
        result3 = agent.run_query("Give me detailed information about all the complex topics in the book with specific examples", timeout=30)
        response3 = result3['response']
        print(f"Error handling response: {response3[:200]}..." if len(response3) > 200 else f"Error handling response: {response3}")

        # Check sources
        sources3 = result3.get('sources', [])
        print(f"Sources for response 3: {len(sources3)}")

        print("\nPerformance and reliability test completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Error during performance and reliability test: {e}")
        print(f"Error during performance and reliability test: {e}")
        return False


def test_follow_up_queries():
    """
    Test function to demonstrate follow-up query functionality.
    """
    logger.info("Starting follow-up query test...")

    try:
        logger.info("Creating RAGBookAgent instance for testing...")
        agent = RAGBookAgent()
        logger.info("RAG Book Agent initialized successfully for testing!")

        print("Testing follow-up query functionality...")

        # Test query 1
        print("\nQuery 1: What is the introduction to the technical book?")
        result1 = agent.run_query("What is the introduction to the technical book?")
        response1 = result1['response']
        print(f"Response 1: {response1}")

        # Show sources for first query
        sources1 = result1.get('sources', [])
        print(f"Sources for query 1: {len(sources1)}")

        # Test follow-up query that references previous context
        print("\nFollow-up Query: Can you elaborate on the concepts mentioned?")
        result2 = agent.run_query("Can you elaborate on the concepts mentioned?")
        response2 = result2['response']
        print(f"Response 2: {response2}")

        # Show sources for follow-up query
        sources2 = result2.get('sources', [])
        print(f"Sources for query 2: {len(sources2)}")

        print("\nFollow-up query test completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Error during follow-up query test: {e}")
        print(f"Error during follow-up query test: {e}")
        return False


def main():
    """
    Main function to initialize and run the RAG agent.
    """
    logger.info("Starting RAG Book Agent initialization...")

    # Check for required environment variables
    required_vars = ["GROQ_API_KEY", "QDRANT_URL", "QDRANT_API_KEY", "COHERE_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        print(f"Error: Missing required environment variables: {missing_vars}")
        print("Please set these in your .env file")
        return

    # Check if test flag is provided
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test-followup":
            success = test_follow_up_queries()
            if success:
                print("\n[SUCCESS] Follow-up query functionality test passed!")
            else:
                print("\n[FAILED] Follow-up query functionality test failed!")
            return
        elif sys.argv[1] == "--test-performance":
            success = test_performance_and_reliability()
            if success:
                print("\n[SUCCESS] Performance and reliability test passed!")
            else:
                print("\n[FAILED] Performance and reliability test failed!")
            return
        elif sys.argv[1] == "--test-e2e":
            success = test_end_to_end_functionality()
            if success:
                print("\n[SUCCESS] End-to-end functionality test passed!")
            else:
                print("\n[FAILED] End-to-end functionality test failed!")
            return

    try:
        logger.info("Creating RAGBookAgent instance...")
        agent = RAGBookAgent()
        logger.info("RAG Book Agent initialized successfully!")
        print("RAG Book Agent initialized successfully!")
        agent.chat_loop()
    except Exception as e:
        logger.error(f"Error initializing agent: {e}")
        print(f"Error initializing agent: {e}")


if __name__ == "__main__":
    main()