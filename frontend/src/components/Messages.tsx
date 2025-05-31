import React, { useEffect, useRef } from 'react';
import { type Message } from '../model/Message';
import { chatbotStyles } from '../styles/styles';
import { getChatbotText } from '../data/chatbotTexts';

interface MessagesProps {
  messages: Message[];
  loading: boolean;
}

export const Messages = ({ messages, loading }: MessagesProps) => {
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const renderMessage = (text: string, sender: 'user' | 'jenkins-bot', key: React.Key) => (
    <div key={key} style={chatbotStyles.messageContainer(sender)}>
      <span style={chatbotStyles.messageBubble(sender)}>
        {text.split('\n').map((line, i) => (
          <React.Fragment key={i}>
            {line}
            <br />
          </React.Fragment>
        ))}
      </span>
    </div>
  );

  return (
    <div style={chatbotStyles.messagesMain}>
      {messages.map(msg => renderMessage(msg.text, msg.sender, msg.id))}
      {loading && renderMessage(getChatbotText('generatingMessage'), 'jenkins-bot', 'loading')}
      <div ref={messagesEndRef} />
    </div>
  );
};
