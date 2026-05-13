import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { validateQuery } from '../utils/validation';
import { formatTimestamp } from '../utils/formatting';

/**
 * Chat Interface Component
 * Modern React component with real-time chat interface
 */
const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (messagesEndRef.current && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Handle message submission
  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    
    // Get fresh message from input (avoiding stale state if called from event listeners)
    const messageToSend = inputValue.trim();
    
    if (messageToSend.length < 3) {
      alert('Please enter a message (at least 3 characters)');
      return;
    }
    
    // Set loading state immediately
    setIsLoading(true);
    
    // Add user message to UI immediately
    const userMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue, // Preserve original input with spaces for display
      timestamp: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    // Clear input immediately after adding user message to UI
    setInputValue('');
    setIsTyping(false);
    
    try {
      const response = await axios.post('/api/chat', {
        query: messageToSend,
        sessionId: localStorage.getItem('sessionId') || 'anonymous'
      });
      
      if (response.data && response.data.response) {
        // Add assistant response to UI
        const assistantMessage = {
          id: (Date.now() + 1).toString(),
          type: 'assistant',
          content: response.data.response,
          timestamp: new Date().toISOString(),
          sources: response.data.sources || []
        };
        
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        throw new Error('Invalid API response');
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: (Date.now() + 2).toString(),
        type: 'error',
        content: 'Sorry, there was an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      // Refocus input
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }
  };

  // Handle typing indicator and input updates
  const handleInputChange = (e) => {
    // Preserve ALL characters exactly as typed (no trimming here!)
    const newValue = e.target.value;
    setInputValue(newValue);
    setIsTyping(newValue.trim().length > 0);
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h1>HDFC Mutual Fund RAG Assistant</h1>
        <p>Ask questions about mutual funds, schemes, and investments</p>
      </div>
      
      <div className="chat-messages" ref={messagesEndRef}>
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            <div className="message-wrapper">
              <div className="message-bubble">
                <div className="message-content">
                  {message.content}
                </div>
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <p className="sources-title">Sources:</p>
                    <ul>
                      {message.sources.map((source, i) => (
                        <li key={i}>{source.title || source}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              <div className="message-metadata">
                <span className="sender">{message.type === 'user' ? 'You' : 'Assistant'}</span>
                <span className="time">• Just now</span>
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant typing">
            <div className="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
      </div>
      
      <div className="chat-input-container">
        <div className="input-group">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={handleInputChange}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
                handleSubmit(e);
              }
            }}
            placeholder="Type your message here..."
            disabled={isLoading}
            className="chat-input"
          />
          <button 
            onClick={handleSubmit}
            disabled={isLoading || !inputValue.trim()}
            className="send-button"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
