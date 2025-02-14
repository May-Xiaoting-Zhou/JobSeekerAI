import React, { useState } from 'react';
import { Input, Button, Avatar } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined } from '@ant-design/icons';
import './App.css';

interface Message {
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

function App() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSend = async () => {
    if (!message.trim()) return;
    
    // Add user message to chat
    const userMessage: Message = {
      text: message,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    
    // Clear input field
    setMessage('');
    
    try {
      // Send message to backend
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      
      // Add AI response to chat
      const aiMessage: Message = {
        text: data.response,
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error:', error);
      // Optionally add error message to chat
      const errorMessage: Message = {
        text: "Sorry, there was an error processing your message.",
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <Avatar icon={<RobotOutlined />} className="ai-avatar" />
          <span className="header-title">AI Assistant</span>
        </div>
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message-bubble ${msg.sender}`}>
              <div className="message-avatar">
                {msg.sender === 'ai' ? (
                  <Avatar icon={<RobotOutlined />} className="ai-avatar" />
                ) : (
                  <Avatar icon={<UserOutlined />} className="user-avatar" />
                )}
              </div>
              <div className="message-content">
                {msg.text}
              </div>
            </div>
          ))}
        </div>
        <div className="chat-input">
          <Input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onPressEnter={handleSend}
            placeholder="Type your message..."
            suffix={
              <Button 
                type="primary" 
                icon={<SendOutlined />} 
                onClick={handleSend}
              />
            }
          />
        </div>
      </div>
    </div>
  );
}

export default App; 