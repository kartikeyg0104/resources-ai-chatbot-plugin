import { useEffect, useRef } from 'react';
import { type Message } from '../model/Message';
import { chatbotStyles } from '../styles/styles';

interface MessagesProps {
  messages: Message[];
}

export const Messages = ({ messages }: MessagesProps) => {
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div
      style={chatbotStyles.messagesMain}
    >
      {messages.map(msg => (
        <div
          key={msg.id}
          style={chatbotStyles.messageContainer(msg.sender)}
        >
          <span
            style={chatbotStyles.messageBubble(msg.sender)}
          >
            {msg.text}
          </span>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};
