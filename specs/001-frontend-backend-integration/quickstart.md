# Quickstart Guide: Frontend-Backend Integration for RAG Chatbot

## Prerequisites
- Python 3.9+ for backend API
- Node.js 18+ and npm for Docusaurus frontend
- FastAPI and related dependencies
- Existing RAG agent in backend/agent.py
- Valid API keys in .env file

## Setup

### 1. Backend Setup (FastAPI Server)

1. **Install backend dependencies**:
```bash
cd backend
pip install fastapi uvicorn python-dotenv requests
```

2. **Verify environment variables**:
Ensure your `.env` file contains:
```
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
```

3. **Create the FastAPI backend**:
Create `backend/api.py` with the API endpoints as defined in the contracts

### 2. Frontend Setup (Docusaurus Integration)

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install additional dependencies if needed**:
```bash
npm install axios @docusaurus/core
```

3. **Create chatbot components**:
- Add React components for the chat interface
- Implement API communication logic
- Style components to match Docusaurus theme

### 3. Running the Integrated System

1. **Start the FastAPI backend**:
```bash
cd backend
uvicorn api:app --reload --port 8000
```

2. **Start the Docusaurus frontend**:
```bash
cd frontend
npm run start
```

3. **Access the integrated chatbot**:
Visit your Docusaurus site (usually http://localhost:3000) and navigate to the page with the integrated chatbot.

## Configuration

### Environment Variables
The system relies on these environment variables (set in `.env`):
- `GROQ_API_KEY` - For the RAG agent API access
- `QDRANT_URL` - For vector database access
- `QDRANT_API_KEY` - For Qdrant authentication
- `COHERE_API_KEY` - For embedding generation

### API Endpoint Configuration
- Backend API runs on `http://localhost:8000` by default
- Frontend communicates with `/api/chat` endpoint
- Configure proxy settings in Docusaurus if needed

## Usage

### Basic Interaction
1. Open the Docusaurus site with integrated chatbot
2. Type your question in the chat input field
3. Press Enter or click Send to submit
4. View the response with source citations

### Conversation Flow
- The system maintains conversation context using session IDs
- Follow-up questions reference previous conversation
- Sessions are stored in browser localStorage

## Development

### Running in Development Mode
- Backend: `uvicorn api:app --reload --port 8000`
- Frontend: `npm run start`

### Testing the Integration
1. Verify the backend API is accessible
2. Test API endpoint directly with curl or Postman
3. Check browser console for frontend errors
4. Test end-to-end flow from frontend to backend

### Troubleshooting
- If API requests fail, check that backend is running on correct port
- If CORS errors occur, ensure FastAPI has proper CORS middleware
- If agent responses are incorrect, verify environment variables are set correctly
- Check browser developer tools for frontend errors
- Check backend console for API processing errors

## Deployment Notes
- Deploy backend API to a server accessible by frontend
- Update API endpoint configuration for production
- Ensure SSL certificates for secure API communication
- Monitor API usage to manage costs