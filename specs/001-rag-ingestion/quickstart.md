# Quickstart: RAG Knowledge Ingestion & Vector Indexing

## Prerequisites

- Python 3.11 or higher
- Pip package manager
- Git (for cloning if needed)
- Cohere API key
- Qdrant Cloud account and API key

## Setup

### 1. Clone or Navigate to Project Directory
```bash
cd /path/to/your/project
```

### 2. Create Backend Directory
```bash
mkdir backend
cd backend
```

### 3. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
Create `requirements.txt`:
```txt
requests==2.31.0
beautifulsoup4==4.12.2
cohere==4.4.3
qdrant-client==1.7.0
python-dotenv==1.0.0
```

Install with pip:
```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables
Create `.env` file (use `.env.example` as template):
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_URL=your_qdrant_cluster_url
BOOK_URL=https://hackathon-physical-and-ai-humanoid.vercel.app/
```

## Implementation

### Create the main.py file with required functions:

```python
import os
import requests
from bs4 import BeautifulSoup
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import time
import logging
from urllib.parse import urljoin, urlparse
import re

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

def get_all_urls(base_url):
    """
    Crawl the base URL and return all discovered URLs from the Docusaurus site.
    """
    urls = set()
    urls.add(base_url)

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)

            # Only add URLs from the same domain
            if urlparse(base_url).netloc == urlparse(full_url).netloc:
                if full_url.startswith(base_url):
                    urls.add(full_url)

        logger.info(f"Found {len(urls)} URLs from base URL: {base_url}")
        return list(urls)

    except requests.RequestException as e:
        logger.error(f"Error crawling {base_url}: {e}")
        return [base_url]  # Return the base URL as fallback

def extract_text_from_url(url):
    """
    Extract main content from a given URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Try to find main content areas in Docusaurus
        content_selectors = [
            'main article',  # Common Docusaurus selector
            '.markdown',     # Docusaurus markdown content
            '.theme-doc-markdown',  # Docusaurus theme content
            'article',       # Generic article
            '.container',    # Common container
            'main',          # Main content area
            'body'           # Fallback to entire body
        ]

        text_content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    text_content += element.get_text(separator=' ', strip=True) + "\n\n"
                break

        # If no content found with selectors, use body
        if not text_content.strip():
            text_content = soup.get_text(separator=' ', strip=True)

        # Clean up the text
        text_content = re.sub(r'\n+', '\n', text_content)  # Replace multiple newlines with single
        text_content = re.sub(r' +', ' ', text_content)    # Replace multiple spaces with single

        logger.info(f"Extracted {len(text_content)} characters from {url}")
        return text_content.strip()

    except Exception as e:
        logger.error(f"Error extracting text from {url}: {e}")
        return ""

def chunk_text(text, chunk_size=800, overlap=100):
    """
    Split text into chunks with specified size and overlap.
    """
    if not text:
        return []

    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = ' '.join(chunk_words)

        chunks.append({
            'text': chunk_text,
            'start_pos': start,
            'end_pos': end,
            'word_count': len(chunk_words)
        })

        # Move start position by chunk_size - overlap to create overlap
        start = end - overlap if end < len(words) else len(words)

    logger.info(f"Created {len(chunks)} chunks from text")
    return chunks

def embed(texts):
    """
    Generate embeddings for a list of texts using Cohere.
    """
    if not texts:
        return []

    try:
        response = co.embed(
            texts=texts,
            model='embed-english-v3.0',
            input_type='search_document'  # Use 'search_document' for stored chunks
        )

        logger.info(f"Generated embeddings for {len(texts)} texts")
        return response.embeddings

    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return []

def create_collection(collection_name="rag_embedding"):
    """
    Create a Qdrant collection for storing embeddings.
    """
    try:
        # Check if collection already exists
        try:
            qdrant_client.get_collection(collection_name)
            logger.info(f"Collection {collection_name} already exists")
            return True
        except:
            pass  # Collection doesn't exist, proceed to create

        # Create collection with 1024 dimensions for Cohere embeddings
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
        )

        logger.info(f"Created collection {collection_name} with 1024 dimensions")
        return True

    except Exception as e:
        logger.error(f"Error creating collection {collection_name}: {e}")
        return False

def save_chunk_to_qdrant(collection_name, chunk_data, embedding, url, doc_title, chunk_pos):
    """
    Save a chunk with its embedding to Qdrant.
    """
    try:
        # Prepare the payload with metadata
        payload = {
            "content": chunk_data['text'],
            "source_url": url,
            "document_title": doc_title,
            "chunk_position": chunk_pos,
            "word_count": chunk_data['word_count'],
            "created_at": time.time()
        }

        # Generate a unique ID for this chunk
        chunk_id = f"{url}_chunk_{chunk_pos}"

        # Upsert the point to Qdrant
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=hash(chunk_id) % (10**9),  # Generate numeric ID
                    vector=embedding,
                    payload=payload
                )
            ]
        )

        logger.info(f"Saved chunk to Qdrant: {chunk_id}")
        return True

    except Exception as e:
        logger.error(f"Error saving chunk to Qdrant: {e}")
        return False

def main():
    """
    Main function to execute the RAG ingestion pipeline.
    """
    logger.info("Starting RAG Knowledge Ingestion Pipeline")

    # Configuration
    book_url = os.getenv("BOOK_URL", "https://hackathon-physical-and-ai-humanoid.vercel.app/")
    collection_name = "rag_embedding"

    # Step 1: Create collection
    if not create_collection(collection_name):
        logger.error("Failed to create Qdrant collection")
        return

    # Step 2: Get all URLs from the book site
    logger.info(f"Discovering URLs from: {book_url}")
    urls = get_all_urls(book_url)
    logger.info(f"Discovered {len(urls)} URLs")

    # Process each URL
    for i, url in enumerate(urls):
        logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

        # Extract text from URL
        text_content = extract_text_from_url(url)
        if not text_content.strip():
            logger.warning(f"No content extracted from {url}, skipping")
            continue

        # Extract document title from URL or content
        doc_title = urlparse(url).path.strip('/').replace('-', ' ').title() or "Untitled Document"

        # Chunk the text
        chunks = chunk_text(text_content)
        logger.info(f"Processing {len(chunks)} chunks for {url}")

        # Process each chunk
        for j, chunk in enumerate(chunks):
            # Generate embedding for the chunk
            embeddings = embed([chunk['text']])
            if not embeddings:
                logger.warning(f"Failed to generate embedding for chunk {j} of {url}")
                continue

            embedding = embeddings[0]

            # Save to Qdrant
            success = save_chunk_to_qdrant(
                collection_name=collection_name,
                chunk_data=chunk,
                embedding=embedding,
                url=url,
                doc_title=doc_title,
                chunk_pos=j
            )

            if success:
                logger.info(f"Successfully saved chunk {j} of {url}")
            else:
                logger.error(f"Failed to save chunk {j} of {url}")

            # Add a small delay to respect API limits
            time.sleep(0.1)

    logger.info("RAG Knowledge Ingestion Pipeline completed")

if __name__ == "__main__":
    main()
```

## Usage

1. **Run the ingestion**:
```bash
cd backend
python main.py
```

2. **Monitor the logs** for progress and any errors.

## Configuration

- Adjust `chunk_size` and `overlap` in the `chunk_text` function to control chunking behavior
- Modify the `collection_name` in the `create_collection` function if needed
- Update the URL selectors in `extract_text_from_url` based on your specific Docusaurus theme

## Troubleshooting

- **API Rate Limits**: The code includes delays to respect API limits, but you may need to adjust based on your Cohere plan
- **Content Extraction**: If content extraction isn't working, inspect the HTML structure of your Docusaurus site and update selectors in `extract_text_from_url`
- **Qdrant Connection**: Ensure your Qdrant URL and API key are correctly configured in the environment variables