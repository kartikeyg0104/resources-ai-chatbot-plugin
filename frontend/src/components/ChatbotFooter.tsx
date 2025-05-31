import { useState } from 'react';
import { type Message } from '../model/Message';
import { fetchChatbotReply } from '../api/chatbot';
import { Header } from './Header';
import { Messages } from './Messages';
import { Input } from './Input';
import { chatbotStyles } from '../styles/styles';

export const ChatbotFooter = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const clearMessages = () => {
    setMessages([]);
  };

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMessage: Message = {
      id: messages.length + 1,
      sender: 'user',
      text: trimmed,
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    const botReply = await fetchChatbotReply(trimmed);
    setLoading(false);
    setMessages(prev => [...prev, botReply]);
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={chatbotStyles.toggleButton}
      >
        💬
      </button>

      {isOpen && (
        <div
           style={chatbotStyles.container}
        >
          <Header 
            clearMessages={clearMessages}
          />
          <Messages messages={messages} loading={loading} />
          <Input input={input} setInput={setInput} onSend={sendMessage} />
        </div>
      )}
    </>
  );
};
