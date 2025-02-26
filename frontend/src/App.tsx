import React, { useState } from 'react';
import { Input, Button, Avatar } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined } from '@ant-design/icons';
import './App.css';
import { Message } from './types';

function App() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSend = async () => {
    if (!message.trim()) return;
    
    const userMessage: Message = {
      text: message,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setMessage('');
    
    try {
      console.log('Sending message to backend:', message);
      
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ 
          message: message,
          conversation_id: 'default'
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Received response from backend:', data);
      
      const aiMessage: Message = {
        text: data.response,
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
      
    } catch (error) {
      console.error('Error in handleSend:', error);
      const errorMessage: Message = {
        text: error instanceof Error ? error.message : 'Failed to send message',
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
                {typeof msg.text === 'string' ? msg.text : 'Invalid message format'}
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