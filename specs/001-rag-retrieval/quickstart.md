# Quickstart: RAG Retrieval & Pipeline Testing

## Prerequisites

- Python 3.11 or higher
- Pip package manager
- Git (for cloning if needed)
- Cohere API key
- Qdrant Cloud account and API key
- Previously created embeddings in Qdrant (from Spec-1)

## Setup

### 1. Navigate to Backend Directory
```bash
cd /path/to/your/project/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Create `requirements.txt`:
```txt
cohere==4.4.3
qdrant-client==1.7.0
python-dotenv==1.0.0
```

Install with pip:
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create `.env` file (use `.env.example` as template):
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_URL=your_qdrant_cluster_url
COLLECTION_NAME=RAG-embedding
```

## Implementation

### Create the retrieve.py file with required functions:

```python
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
    Generate embedding for the query using Cohere.
    """
    try:
        response = co.embed(
            texts=[query],
            model='embed-english-v3.0',
            input_type='search_query'  # Use 'search_query' for queries
        )

        logger.info(f"Generated embedding for query: {query[:50]}...")
        return response.embeddings[0]
    except Exception as e:
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
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        results = []
        for result in search_results:
            results.append({
                'content_chunk': result.payload.get('content', ''),
                'similarity_score': result.score,
                'source_url': result.payload.get('source_url', ''),
                'document_title': result.payload.get('document_title', ''),
                'chunk_position': result.payload.get('chunk_position', -1),
                'word_count': result.payload.get('word_count', 0),
                'created_at': result.payload.get('created_at', None)
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

        if result['retrieval_success']:
            logger.info(f"Query {i+1} successful - {result['retrieved_chunks_count']} chunks retrieved")
            logger.info(f"Response time: {result['response_time']:.2f}s")
            logger.info(f"Top similarity score: {result['top_similarity_score']:.3f}")
        else:
            logger.error(f"Query {i+1} failed: {result.get('error_message', 'Unknown error')}")

        # Add delay to respect API limits
        time.sleep(0.1)

    logger.info("RAG Retrieval & Pipeline Testing completed")

if __name__ == "__main__":
    main()
```

## Usage

1. **Run the retrieval and testing**:
```bash
cd backend
python retrieve.py
```

2. **Monitor the logs** for search results and validation reports.

## Configuration

- Adjust `top_k` in the `search_similar_chunks` function to change number of results returned
- Modify the `sample_queries` list in the `main` function to test different queries
- Update the `COLLECTION_NAME` in environment variables if using a different collection

## Troubleshooting

- **API Rate Limits**: The code includes delays to respect API limits, but you may need to adjust based on your Cohere plan
- **Qdrant Connection**: Ensure your Qdrant URL and API key are correctly configured in the environment variables
- **Collection Not Found**: Verify that the RAG-embedding collection was created in the previous step (Spec-1)
- **No Results**: Check that embeddings were properly created and stored in Qdrant