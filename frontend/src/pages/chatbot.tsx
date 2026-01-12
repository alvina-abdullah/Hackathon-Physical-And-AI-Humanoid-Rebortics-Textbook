import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import ChatInterface from '../components/Chatbot/ChatInterface';
import FloatingChatbot from '../components/Chatbot/FloatingChatbot';
import styles from './chatbot.module.css';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

function ChatbotPage(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();

  return (
    <Layout
      title={`AI Assistant | ${siteConfig.title}`}
      description="AI-powered chatbot for robotics textbook questions">
      <FloatingChatbot /> {/* Include the floating chatbot on this page as well */}
      <main className={styles.main}>
        <div className={styles.container}>
          <div className={styles.header}>
            <h1>🤖 AI Assistant for Robotics Textbook</h1>
            <p>🧠 Ask questions about robotics, AI, and textbook content • Get intelligent responses powered by RAG system</p>
          </div>

          <div className={styles.chatWrapper}>
            <ChatInterface className={styles.chatComponent} />
          </div>

          <div className={styles.information}>
            <h3>How it works</h3>
            <ul>
              <li>Ask questions about robotics concepts, theory, or applications</li>
              <li>Our AI assistant retrieves relevant information from the textbook</li>
              <li>Sources are cited so you can verify the information</li>
              <li>Have follow-up conversations to dive deeper into topics</li>
            </ul>
          </div>
        </div>
      </main>
    </Layout>
  );
}

export default ChatbotPage;