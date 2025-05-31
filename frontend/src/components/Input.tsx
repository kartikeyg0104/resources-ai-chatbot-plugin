import React from 'react';
import { getChatbotText } from '../data/chatbotTexts';
import { chatbotStyles } from '../styles/styles';

interface InputProps {
  input: string;
  setInput: (value: string) => void;
  onSend: () => void;
}

export const Input = ({ input, setInput, onSend }: InputProps) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div style={{ padding: '0.75rem', borderTop: '1px solid #eee' }}>
      <textarea
        value={input}
        placeholder={getChatbotText('placeholder')}
        onChange={e => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        style={{
          ...chatbotStyles.input,
          minHeight: '60px',
          maxHeight: '150px',
          resize: 'none',
          overflow: 'auto',
          lineHeight: '1.5',
        }}
      />
    </div>
  );
};
