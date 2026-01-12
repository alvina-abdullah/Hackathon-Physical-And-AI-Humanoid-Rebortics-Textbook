# API Contracts: Frontend-Backend Integration for RAG Chatbot

## FastAPI Endpoints

### POST /api/chat

**Description**: Process user query through RAG agent and return response with sources

**Request**:
```
Method: POST
Path: /api/chat
Content-Type: application/json
```

**Request Body**:
```
{
  "query": {
    "type": "string",
    "description": "The user's question or query",
    "minLength": 1,
    "maxLength": 1000,
    "required": true
  },
  "sessionId": {
    "type": "string",
    "description": "Session identifier for conversation context (optional)",
    "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    "required": false
  }
}
```

**Example Request**:
```
{
  "query": "What is the main concept of the book?",
  "sessionId": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```

**Response**:
```
Status: 200 OK
Content-Type: application/json
```

**Response Body**:
```
{
  "response": {
    "type": "string",
    "description": "The RAG agent's response to the query",
    "required": true
  },
  "sources": {
    "type": "array",
    "description": "List of sources used in the response",
    "items": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "description": "Title of the source document",
          "required": true
        },
        "url": {
          "type": "string",
          "description": "URL of the source document",
          "format": "uri",
          "required": true
        },
        "contentPreview": {
          "type": "string",
          "description": "Preview of the content used from the source",
          "required": true
        }
      }
    },
    "required": true
  },
  "sessionId": {
    "type": "string",
    "description": "Session identifier for conversation continuity",
    "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    "required": true
  },
  "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "ISO 8601 timestamp of response generation",
    "required": true
  },
  "status": {
    "type": "string",
    "enum": ["success", "error"],
    "description": "Status of the query processing",
    "required": true
  }
}
```

**Example Response**:
```
{
  "response": "The main concept of the book is about AI robotics and how to build intelligent systems...",
  "sources": [
    {
      "title": "Introduction to AI Robotics",
      "url": "https://example.com/book/introduction",
      "contentPreview": "The introduction chapter discusses the fundamentals of AI robotics..."
    }
  ],
  "sessionId": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "timestamp": "2026-01-05T15:30:00Z",
  "status": "success"
}
```

**Error Response** (400 Bad Request):
```
{
  "detail": "string",
  "status_code": 400,
  "timestamp": "string (ISO 8601)"
}
```

**Error Response** (500 Internal Server Error):
```
{
  "detail": "string",
  "status_code": 500,
  "timestamp": "string (ISO 8601)"
}
```

### GET /api/health

**Description**: Check the health status of the API service

**Request**:
```
Method: GET
Path: /api/health
```

**Response** (200 OK):
```
{
  "status": "healthy",
  "timestamp": "string (ISO 8601)"
}
```

## WebSocket Endpoint (Optional Future Enhancement)

### GET /api/chat/ws

**Description**: WebSocket endpoint for real-time chat streaming

**Request**:
```
Method: GET
Path: /api/chat/ws
Headers: {
  "Upgrade": "websocket",
  "Connection": "Upgrade",
  ...
}
```

**Message Format**:
```
{
  "type": "message",
  "data": {
    "query": "string",
    "response": "string",
    "sources": "array of source objects",
    "sessionId": "string"
  }
}
```

## Rate Limiting

All endpoints are subject to rate limiting:
- Per IP: 100 requests per minute
- Per session: 10 requests per minute

## Authentication

Currently no authentication required - this endpoint is designed for public access.
Future enhancement could add optional authentication for personalized experiences.

## Validation

Request bodies will be validated against the schemas defined above. Invalid requests will return 400 Bad Request with detailed error messages.