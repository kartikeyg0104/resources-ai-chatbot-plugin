import React from 'react';
import { getChatbotText } from '../data/chatbotTexts';
import { chatbotStyles } from '../styles/styles';

interface InputProps {
  input: string;
  setInput: (value: string) => void;
  onSend: () => void;
}

export const Input = ({ input, setInput, onSend }: InputProps) => {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div style={{ maxWidth: "90%", padding: '0.75rem', borderTop: '1px solid #eee' }}>
      <input
        type="text"
        value={input}
        placeholder={getChatbotText('placeholder')}
        onChange={e => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        style={chatbotStyles.input}
      />
    </div>
  );
};
