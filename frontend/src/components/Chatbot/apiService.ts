/**
 * API Service for RAG Chatbot communication
 * Handles all HTTP requests between the frontend and backend
 */

// Define TypeScript interfaces
interface QueryRequest {
  query: string;
  sessionId?: string;
}

interface Source {
  title: string;
  url: string;
  contentPreview: string;
}

interface QueryResponse {
  response: string;
  sources: Source[];
  sessionId: string;
  timestamp: string;
  status: string;
}

interface HealthResponse {
  status: string;
  timestamp: string;
}

class ChatApiService {
  private baseUrl: string;
  private readonly timeout: number = 30000; // 30 seconds

  constructor(baseUrl?: string) {
    // In development, connect to the backend server running on port 8000
    // For production, this can be overridden via environment variables
    // Using typeof check to avoid "process is not defined" error in browser
    const getEnvVar = (name: string): string | undefined => {
      if (typeof process !== 'undefined' && process.env) {
        return process.env[name];
      }
      // Also check for browser environment variables if needed
      return undefined;
    };

    this.baseUrl = baseUrl ||
                   getEnvVar('REACT_APP_API_BASE_URL') ||
                   getEnvVar('DOCUSAURUS_API_BASE_URL') ||
                   'http://127.0.0.1:8000'; // Default to local backend server
  }

  /**
   * Sends a query to the RAG agent and returns the response
   * @param request - The query request containing the user's question and optional session ID
   * @returns Promise resolving to the query response
   */
  async sendQuery(request: QueryRequest): Promise<QueryResponse> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      // Construct the full URL properly handling relative paths
      const url = this.baseUrl ? `${this.baseUrl}/api/chat` : '/api/chat';
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorData || response.statusText}`);
      }

      const data: QueryResponse = await response.json();
      return data;
    } catch (error) {
      clearTimeout(timeoutId);

      if ((error as Error).name === 'AbortError') {
        throw new Error('Request timed out');
      }

      throw error;
    }
  }

  /**
   * Checks the health status of the backend API
   * @returns Promise resolving to the health response
   */
  async healthCheck(): Promise<HealthResponse> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      // Construct the full URL properly handling relative paths
      const url = this.baseUrl ? `${this.baseUrl}/api/health` : '/api/health';
      const response = await fetch(url, {
        method: 'GET',
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status} ${response.statusText}`);
      }

      const data: HealthResponse = await response.json();
      return data;
    } catch (error) {
      clearTimeout(timeoutId);

      if ((error as Error).name === 'AbortError') {
        throw new Error('Health check timed out');
      }

      throw error;
    }
  }

  /**
   * Sets a new base URL for the API
   * @param baseUrl - The new base URL for API requests
   */
  setBaseUrl(baseUrl: string): void {
    this.baseUrl = baseUrl;
  }

  /**
   * Gets the current base URL for the API
   * @returns The current base URL
   */
  getBaseUrl(): string {
    return this.baseUrl;
  }
}

// Create a singleton instance of the API service
const chatApiService = new ChatApiService();

export { chatApiService, ChatApiService, QueryRequest, QueryResponse, Source, HealthResponse };