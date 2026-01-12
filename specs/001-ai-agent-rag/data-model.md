# Data Model for AI Agent with RAG Capabilities

## Entities

### Agent
- **id**: string (OpenAI assistant ID)
- **name**: string (name of the agent)
- **description**: string (description of the agent's purpose)
- **instructions**: string (system instructions for the agent)
- **tools**: list of tool definitions (retrieval tool configuration)
- **model**: string (OpenAI model identifier)

### Retrieval Tool
- **type**: string ("function")
- **function**: object containing:
  - **name**: string ("retrieve_content")
  - **description**: string ("Retrieve relevant content from the book database based on user query")
  - **parameters**: object defining query parameter
  - **returns**: array of document chunks with content, source URL, and title

### Document Chunk
- **content**: string (text content of the chunk)
- **source_url**: string (URL where the content originated)
- **title**: string (title of the source document)
- **similarity_score**: float (similarity score from vector search)
- **metadata**: object (additional metadata from Qdrant)

### User Query
- **text**: string (the natural language query from user)
- **timestamp**: datetime (when query was submitted)
- **session_id**: string (conversation session identifier)

### Agent Response
- **text**: string (the agent's response to the user)
- **sources**: array of document chunks used to generate response
- **timestamp**: datetime (when response was generated)
- **query**: string (original user query)

## Relationships
- Agent has many conversations
- Conversation has many User Queries
- User Query has many Agent Responses
- Agent Response references many Document Chunks
- Retrieval Tool returns many Document Chunks