# Quickstart Guide: AI Agent with RAG Capabilities

## Prerequisites
- Python 3.9+
- OpenAI API key
- Qdrant vector database with book content
- Environment variables configured (see .env.example)

## Setup

1. **Install dependencies**:
```bash
pip install openai qdrant-client python-dotenv cohere
```

2. **Configure environment variables**:
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
COLLECTION_NAME=RAG-embedding
```

3. **Ensure Qdrant collection exists** with book content vectors

## Running the Agent

1. **Start the agent**:
```bash
python backend/agent.py
```

2. **The agent will**:
   - Initialize the OpenAI Assistant with retrieval tool
   - Wait for user input
   - Process queries through the retrieval tool
   - Generate responses based on retrieved content

## Example Usage

```
> What is the introduction to the technical book?
< The introduction chapter provides an overview of the book's content...
  Sources:
  - https://example.com/book/intro
  - https://example.com/book/overview
```

## Testing Options

The agent includes several testing modes:

1. **Follow-up query testing**:
```bash
python backend/agent.py --test-followup
```

2. **Performance and reliability testing**:
```bash
python backend/agent.py --test-performance
```

3. **End-to-end functionality testing**:
```bash
python backend/agent.py --test-e2e
```

## Additional Features

- **Timeout handling**: Queries automatically time out after 10 seconds
- **Retry logic**: Failed retrieval attempts are retried with exponential backoff
- **Input validation**: Queries are validated for length and content
- **Error handling**: Graceful handling of Qdrant connection failures
- **Logging**: Comprehensive logging for debugging and monitoring

## Troubleshooting

- If you get API key errors, verify your .env file contains all required keys
- If retrieval fails, check that your Qdrant database has the correct collection
- If responses take too long, check your network connection to Qdrant and OpenAI