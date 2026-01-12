import React, { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';
import styles from './chatInterface.module.css';
import { chatApiService } from './apiService';

// Define TypeScript interfaces
interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  sources?: Array<{
    title: string;
    url: string;
    contentPreview: string;
  }>;
}

interface ChatProps {
  className?: string;
}

const ChatInterface: React.FC<ChatProps> = ({ className }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [sessionId, setSessionId] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize session ID on component mount
  useEffect(() => {
    // Generate or retrieve session ID
    const storedSessionId = localStorage.getItem('chatbot-session-id');
    if (storedSessionId) {
      setSessionId(storedSessionId);
    } else {
      const newSessionId = generateSessionId();
      setSessionId(newSessionId);
      localStorage.setItem('chatbot-session-id', newSessionId);
    }

    // Add welcome message
    setMessages([
      {
        id: 'welcome',
        content: 'Hello! I\'m your AI assistant for the robotics textbook. Ask me anything about the content!',
        role: 'assistant',
        timestamp: new Date(),
      }
    ]);
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const generateSessionId = (): string => {
    // Generate a proper UUID v4 format
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send request to backend API using the service
      // Only include sessionId if it's a valid UUID format
      const requestObj: QueryRequest = {
        query: inputValue,
      };

      // Only add sessionId if it's not empty and is a valid UUID format
      if (sessionId && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(sessionId)) {
        requestObj.sessionId = sessionId;
      }

      const response = await chatApiService.sendQuery(requestObj);

      // Add assistant response to chat
      const assistantMessage: Message = {
        id: Date.now().toString(),
        content: response.response,
        role: 'assistant',
        timestamp: new Date(),
        sources: response.sources || [],
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to chat
      const errorMessage: Message = {
        id: Date.now().toString(),
        content: `Sorry, I encountered an error processing your request: ${(error as Error).message}`,
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  return (
    <div className={clsx(styles.chatContainer, className)}>
      <div className={styles.chatHeader}>
        <h3>🤖 AI Assistant for Robotics Textbook</h3>
      </div>

      <div className={styles.chatMessages}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={clsx(
              styles.message,
              message.role === 'user' ? styles.userMessage : styles.assistantMessage
            )}
          >
            <div className={styles.messageContent}>
              <div className={styles.messageText}>{message.content}</div>

              {message.sources && message.sources.length > 0 && (
                <div className={styles.sourcesSection}>
                  <strong>📚 Sources:</strong>
                  <ul className={styles.sourcesList}>
                    {message.sources.map((source, index) => (
                      <li key={index} className={styles.sourceItem}>
                        <a href={source.url} target="_blank" rel="noopener noreferrer">
                          {source.title}
                        </a>
                        <span className={styles.sourcePreview}>📝 {source.contentPreview.substring(0, 100)}...</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
            <div className={styles.messageTimestamp}>
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className={clsx(styles.message, styles.assistantMessage)}>
            <div className={styles.messageContent}>
              <div className={styles.typingIndicator}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className={styles.chatInputForm}>
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="🤔 Ask anything about robotics, AI, or the textbook content..."
          className={styles.chatInput}
          rows={2}
          disabled={isLoading}
        />
        <button
          type="submit"
          className={clsx(styles.sendButton, isLoading ? styles.disabled : '')}
          disabled={!inputValue.trim() || isLoading}
        >
          {isLoading ? (
            <>{/* Loading indicator */}</>
          ) : (
            <>🚀 Send</>
          )}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;