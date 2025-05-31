import React, { useEffect, useRef } from 'react';
import { type Message } from '../model/Message';
import { chatbotStyles } from '../styles/styles';

interface MessagesProps {
  messages: Message[];
  loading: boolean;
}

export const Messages = ({ messages, loading }: MessagesProps) => {
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
            {msg.text.split('\n').map((line, i) => (
            <React.Fragment key={i}>
              {line}
              <br />
            </React.Fragment>
          ))}
          </span>
        </div>
      ))}
      {loading &&
        <div
          style={chatbotStyles.messageContainer('jenkins-bot')}
        >
          <span
            style={chatbotStyles.messageBubble('jenkins-bot')}
          >
            Generating...
          </span>
        </div>
      }
      <div ref={messagesEndRef} />
    </div>
  );
};
