import { useState } from 'react';
import { type Message } from '../model/Message';
import { fetchChatbotReply } from '../api/chatbot';
import { ChatbotHeader } from './Header';
import { Messages } from './Messages';
import { Input } from './Input';
import { chatbotStyles } from '../styles/styles';

export const ChatbotFooter = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);

  // const sendMessage = () => {
  //   if (!input.trim()) return;

  //   const userMessage: Message = {
  //     id: messages.length + 1,
  //     sender: 'user',
  //     text: input.trim(),
  //   };

  //   setMessages([...messages, userMessage]);

  //   setTimeout(() => {
  //     setMessages(prev => [
  //       ...prev,
  //       {
  //         id: prev.length + 2,
  //         sender: 'jenkins-bot',
  //         text: `${getChatbotText('botReplyPrefix')}"${input.trim()}"`,
  //       },
  //     ]);
  //   }, 600);

  //   setInput('');
  // };

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

    const botReply = await fetchChatbotReply(trimmed);
    setMessages(prev => [...prev, botReply]);
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={chatbotStyles.toggleButton}
      >
        {//<img src="../icons/messageIcon.svg" alt="Message Icon" />
        }
        💬
      </button>

      {isOpen && (
        <div
          style={chatbotStyles.container}
        >
          <ChatbotHeader />
          <Messages messages={messages} />
          <Input input={input} setInput={setInput} onSend={sendMessage} />
        </div>
      )}
    </>
  );
};
