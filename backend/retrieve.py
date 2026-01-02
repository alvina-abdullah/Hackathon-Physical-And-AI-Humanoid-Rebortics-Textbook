import os
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import time
import logging
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

# Initialize clients
co = cohere.Client(os.getenv("COHERE_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_qdrant(collection_name: str) -> bool:
    """
    Connect to Qdrant and verify the collection exists.
    """
    try:
        # Check if collection exists
        qdrant_client.get_collection(collection_name)
        logger.info(f"Successfully connected to collection: {collection_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to collection {collection_name}: {e}")
        return False

def generate_query_embedding(query: str) -> Optional[List[float]]:
    """
    Generate embedding for the query using Cohere with retry logic for rate limiting.
    """
    import httpx
    max_retries = 5
    base_delay = 1  # Start with 1 second

    for attempt in range(max_retries):
        try:
            response = co.embed(
                texts=[query],
                model='embed-english-v3.0',
                input_type='search_query'  # Use 'search_query' for queries
            )

            logger.info(f"Generated embedding for query: {query[:50]}...")
            return response.embeddings[0]
        except Exception as e:
            # Check if it's a rate limit error by examining the exception details
            if "429" in str(e) or "Too Many Requests" in str(e) or (hasattr(e, 'status_code') and e.status_code == 429):
                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Rate limit hit (429), retrying in {delay}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                    continue
                else:
                    logger.error(f"Max retries exceeded for query embedding: {e}")
                    return None
            else:
                logger.error(f"Error generating query embedding: {e}")
                return None

def search_similar_chunks(
    query_embedding: List[float],
    collection_name: str,
    top_k: int = 5
) -> List[Dict]:
    """
    Perform similarity search in Qdrant and retrieve top-k chunks.
    """
    try:
        from qdrant_client.http import models
        search_results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_embedding,
            limit=top_k,
            with_payload=True
        )

        results = []
        # The query_points method returns a named tuple-like object with 'points' attribute
        points = search_results.points if hasattr(search_results, 'points') else search_results
        for result in points:
            results.append({
                'content_chunk': result.payload.get('content', '') if result.payload else '',
                'similarity_score': result.score if hasattr(result, 'score') else result.score,
                'source_url': result.payload.get('source_url', '') if result.payload else '',
                'document_title': result.payload.get('document_title', '') if result.payload else '',
                'chunk_position': result.payload.get('chunk_position', -1) if result.payload else -1,
                'word_count': result.payload.get('word_count', 0) if result.payload else 0,
                'created_at': result.payload.get('created_at', None) if result.payload else None
            })

        logger.info(f"Retrieved {len(results)} chunks for query")
        return results
    except Exception as e:
        logger.error(f"Error performing similarity search: {e}")
        return []

def validate_retrieved_content(results: List[Dict]) -> Dict:
    """
    Validate retrieved content and metadata against source URLs.
    """
    validation_report = {
        'total_results': len(results),
        'valid_results': 0,
        'invalid_results': 0,
        'validation_details': []
    }

    for result in results:
        is_valid = True
        details = {
            'result_id': hash(result['source_url'] + str(result['chunk_position'])) % (10**9),
            'is_valid': True,
            'issues': []
        }

        # Validate content is not empty
        if not result.get('content_chunk', '').strip():
            is_valid = False
            details['issues'].append('Content chunk is empty')

        # Validate source URL format
        source_url = result.get('source_url', '')
        if not source_url or not source_url.startswith('http'):
            is_valid = False
            details['issues'].append('Invalid source URL')

        # Validate document title exists
        if not result.get('document_title', '').strip():
            is_valid = False
            details['issues'].append('Document title is missing')

        # Validate chunk position is reasonable
        if result.get('chunk_position', -1) < 0:
            is_valid = False
            details['issues'].append('Invalid chunk position')

        details['is_valid'] = is_valid
        if is_valid:
            validation_report['valid_results'] += 1
        else:
            validation_report['invalid_results'] += 1

        validation_report['validation_details'].append(details)

    logger.info(f"Validation completed: {validation_report['valid_results']} valid, {validation_report['invalid_results']} invalid")
    return validation_report

def test_retrieval_pipeline(query: str, collection_name: str, top_k: int = 5) -> Dict:
    """
    Test the complete retrieval pipeline: query -> embedding -> search -> validation.
    """
    logger.info(f"Testing retrieval pipeline for query: {query}")

    start_time = time.time()

    # Step 1: Generate query embedding
    query_embedding = generate_query_embedding(query)
    if not query_embedding:
        logger.error("Failed to generate query embedding")
        return {
            'query': query,
            'retrieval_success': False,
            'error_message': 'Failed to generate query embedding',
            'response_time': time.time() - start_time
        }

    # Step 2: Search for similar chunks
    search_results = search_similar_chunks(query_embedding, collection_name, top_k)
    if not search_results:
        logger.warning("No results found for query")
        return {
            'query': query,
            'retrieval_success': True,
            'results': [],
            'validation_success': True,
            'validation_report': validate_retrieved_content([]),
            'response_time': time.time() - start_time
        }

    # Step 3: Validate retrieved content
    validation_report = validate_retrieved_content(search_results)

    # Step 4: Prepare pipeline test result
    pipeline_result = {
        'query': query,
        'retrieval_success': True,
        'results': search_results,
        'validation_success': validation_report['invalid_results'] == 0,
        'validation_report': validation_report,
        'response_time': time.time() - start_time,
        'retrieved_chunks_count': len(search_results),
        'top_similarity_score': max([r['similarity_score'] for r in search_results]) if search_results else 0.0
    }

    logger.info(f"Pipeline test completed in {pipeline_result['response_time']:.2f} seconds")
    return pipeline_result

def main():
    """
    Main function to execute RAG retrieval and testing.
    """
    logger.info("Starting RAG Retrieval & Pipeline Testing")

    # Configuration
    collection_name = os.getenv("COLLECTION_NAME", "RAG-embedding")

    # Verify connection to Qdrant
    if not connect_to_qdrant(collection_name):
        logger.error("Failed to connect to Qdrant")
        return

    # Check if command line arguments were provided
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "--query":
        sample_queries = [sys.argv[2]]  # Use the provided query
    else:
        # Sample queries for testing
        sample_queries = [
            "What is the introduction to the technical book?",
            "Explain AI brain and perception training",
            "How does the VLA autonomous system work?",
            "What are the communication primitives?",
            "Explain digital twin and gazebo physics"
        ]

    # Test each query
    for i, query in enumerate(sample_queries):
        logger.info(f"Processing query {i+1}/{len(sample_queries)}: {query}")

        result = test_retrieval_pipeline(query, collection_name)

        if result.get('retrieval_success', False):
            retrieved_chunks_count = result.get('retrieved_chunks_count', 0)
            logger.info(f"Query {i+1} successful - {retrieved_chunks_count} chunks retrieved")
            logger.info(f"Response time: {result.get('response_time', 0):.2f}s")
            logger.info(f"Top similarity score: {result.get('top_similarity_score', 0):.3f}")

            # Print first result as example
            if result.get('results', []):
                first_result = result['results'][0]
                # Handle Unicode characters for console output by cleaning the strings first
                content_preview = first_result['content_chunk'][:100]
                source_url = first_result['source_url']
                document_title = first_result.get('document_title', 'Untitled')

                # Clean content to remove problematic Unicode characters
                clean_content = content_preview.encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                clean_source = source_url.encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                clean_title = document_title.encode('ascii', errors='ignore').decode('ascii', errors='ignore')

                print(f"  Content preview: {clean_content}...")
                print(f"  Source URL: {clean_source}")
                print(f"  Title: {clean_title}")
        else:
            logger.error(f"Query {i+1} failed: {result.get('error_message', 'Unknown error')}")

        # Add delay to respect API limits
        time.sleep(1.0)  # Increased delay to be more respectful of API rate limits

    logger.info("RAG Retrieval & Pipeline Testing completed")

if __name__ == "__main__":
    main()