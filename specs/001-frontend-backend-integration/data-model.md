# Data Model: Frontend-Backend Integration for RAG Chatbot

## Entities

### QueryRequest
- **query**: string (required) - The user's question text
- **sessionId**: string (optional) - Identifier for conversation context
- **timestamp**: datetime (optional) - When the query was created

### QueryResponse
- **response**: string (required) - The RAG agent's answer to the query
- **sources**: array of Source objects (optional) - Document sources used in the response
- **sessionId**: string (required) - Session identifier for conversation continuity
- **timestamp**: datetime (required) - When the response was generated
- **status**: enum (success, error) - Status of the query processing

### Source
- **title**: string (required) - Title of the source document
- **url**: string (required) - URL where the source can be accessed
- **contentPreview**: string (required) - Brief preview of the source content
- **score**: number (optional) - Relevance score of the source

### Message
- **id**: string (required) - Unique identifier for the message
- **sender**: enum (user, agent) - Who sent the message
- **content**: string (required) - The message text content
- **timestamp**: datetime (required) - When the message was created
- **sources**: array of Source objects (optional) - Sources associated with agent response

### Session
- **id**: string (required) - Unique session identifier
- **createdAt**: datetime (required) - When the session was created
- **lastActive**: datetime (required) - When the session was last used
- **messages**: array of Message objects (required) - Messages in the conversation

## Relationships

- Session contains many Messages
- QueryRequest has one Session (optional)
- QueryResponse has one Session
- QueryResponse contains many Sources
- Message may have many Sources (for agent responses)

## State Transitions

### Message States
- `pending` → `processing` → `received` (for user messages)
- `received` → `processing` → `sent` (for agent responses)

### Query States
- `submitted` → `processing` → `completed` | `failed`

## Validation Rules

### QueryRequest
- query must be between 1 and 1000 characters
- sessionId must be a valid UUID format if provided

### QueryResponse
- response must not be empty if status is success
- sources array must contain valid Source objects
- timestamp must be in ISO 8601 format

### Source
- title must not be empty
- url must be a valid URL format
- contentPreview must be less than 500 characters

### Session
- id must be a valid UUID format
- createdAt must be before or equal to lastActive
- messages array must not exceed 100 messages

## API Payload Specifications

### Request Payload for /api/chat
```
{
  "query": "string (required)",
  "sessionId": "string (optional)"
}
```

### Response Payload for /api/chat
```
{
  "response": "string",
  "sources": [
    {
      "title": "string",
      "url": "string",
      "contentPreview": "string"
    }
  ],
  "sessionId": "string",
  "timestamp": "ISO 8601 datetime string",
  "status": "success | error"
}
```

## Data Flow

1. Frontend sends QueryRequest to backend API
2. Backend processes request with RAG agent
3. Backend returns QueryResponse with sources
4. Frontend displays response in chat interface
5. Session state is maintained for conversation continuity