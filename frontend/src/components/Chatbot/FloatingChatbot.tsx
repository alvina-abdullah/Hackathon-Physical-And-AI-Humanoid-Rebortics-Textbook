import React, { useState } from 'react';
import clsx from 'clsx';
import ChatInterface from './ChatInterface';
import styles from './floatingChatbot.module.css';

const FloatingChatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  // Simple toggle function
  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Check if we're on the client side
  if (typeof window === 'undefined') {
    return null;
  }

  return (
    <>
      {isOpen && (
        <div className={styles.chatContainer}>
          <div className={styles.chatHeader}>
            <h3>🤖 AI Assistant</h3>
            <button
              className={styles.closeButton}
              onClick={toggleChat}
              aria-label="Close chat"
            >
              ✕
            </button>
          </div>
          <div className={styles.chatContent}>
            <ChatInterface />
          </div>
        </div>
      )}

      <button
        className={clsx(styles.floatingButton, {
          [styles.isOpen]: isOpen,
        })}
        onClick={toggleChat}
        aria-label={isOpen ? "Close chat" : "Open chat"}
        title={isOpen ? "Close AI Assistant" : "Open AI Assistant"}
      >
        {isOpen ? (
          <span className={styles.closeIcon}>✕</span>
        ) : (
          <span className={styles.chatIcon}>🤖</span>
        )}
      </button>
    </>
  );
};

export default FloatingChatbot;