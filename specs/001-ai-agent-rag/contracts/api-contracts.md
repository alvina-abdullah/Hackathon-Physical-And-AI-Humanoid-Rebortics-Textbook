# API Contracts for AI Agent with RAG Capabilities

## OpenAI Assistant Configuration

### Assistant Creation
```
POST /assistants
{
  "name": "RAG Book Assistant",
  "description": "An AI assistant that answers questions about book content using retrieval-augmented generation",
  "model": "gpt-4-turbo",
  "instructions": "You are a helpful assistant that answers questions based on retrieved book content. Always cite your sources and only provide information that appears in the retrieved documents. If the information is not available in the retrieved content, acknowledge this limitation.",
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "retrieve_content",
        "description": "Retrieve relevant content from the book database based on user query",
        "parameters": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "The user's question or query about book content"
            }
          },
          "required": ["query"]
        }
      }
    }
  ]
}
```

## Tool Function Contract

### retrieve_content(query: string) -> array[DocumentChunk]

**Purpose**: Retrieve relevant document chunks from Qdrant based on the user's query

**Input**:
- query: string - The user's question or information request

**Output**:
- Array of DocumentChunk objects with:
  - content: string - The text content of the retrieved chunk
  - source_url: string - URL where the content originated
  - title: string - Title of the source document
  - similarity_score: number - Similarity score from vector search

**Error Handling**:
- Returns empty array if no relevant content found
- Throws error if Qdrant connection fails

## Conversation Flow

### Thread Creation
```
POST /threads
{
  "messages": [
    {
      "role": "user",
      "content": "Your question here"
    }
  ]
}
```

### Run Creation
```
POST /threads/{thread_id}/runs
{
  "assistant_id": "assistant_id_here",
  "instructions": "Follow these instructions when responding..."
}
```

### Tool Call Execution
When the assistant calls retrieve_content, the system executes the function and returns results to the assistant.