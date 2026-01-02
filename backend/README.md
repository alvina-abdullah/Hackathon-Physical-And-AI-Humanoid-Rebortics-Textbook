# RAG Knowledge Ingestion & Vector Indexing System

This project implements a RAG (Retrieval Augmented Generation) system that crawls Docusaurus-based technical books, extracts content, generates embeddings using Cohere, and stores vectors in Qdrant for similarity search.

## Prerequisites

- Python 3.11+
- UV package manager
- Cohere API key
- Qdrant Cloud account and API key

## Setup

1. Install dependencies:
   ```bash
   cd backend
   uv sync
   ```

2. Create a `.env` file with your credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

3. Required environment variables:
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `QDRANT_URL`: Your Qdrant cluster URL
   - `BOOK_URL`: The URL of the Docusaurus site to crawl (default: https://hackathon-physical-and-ai-humanoid.vercel.app/)

## Usage

Run the ingestion pipeline:
```bash
uv run main.py
```

## Features

- **URL Crawling**: Discovers all pages from a Docusaurus site
- **Content Extraction**: Extracts main content from each page
- **Text Chunking**: Splits content into 500-1000 word chunks with overlap
- **Embedding Generation**: Creates Cohere embeddings for content chunks
- **Vector Storage**: Stores embeddings with metadata in Qdrant
- **Similarity Search**: Performs vector similarity search for content retrieval
- **Error Handling**: Comprehensive error handling and retry logic
- **Logging**: Detailed logging throughout the process

## Architecture

The system is implemented as a single Python file with functions for each major component:
- `get_all_urls()`: Crawls and discovers URLs
- `extract_text_from_url()`: Extracts content from URLs
- `chunk_text()`: Processes and chunks text with metadata
- `embed()`: Generates Cohere embeddings
- `create_collection()`: Sets up Qdrant collection
- `save_chunk_to_qdrant()`: Stores embeddings in Qdrant
- `search()`: Performs similarity search
- `main()`: Orchestrates the complete pipeline