import { getChatbotText } from '../data/chatbotTexts';
import { chatbotStyles } from '../styles/styles';

interface HeaderProps {
  clearMessages: () => void;
}

export const Header = ({ clearMessages }: HeaderProps) => (
  <div
    style={chatbotStyles.chatbotHeader}
  >
      <p>{getChatbotText('title')}</p>
      <button
        onClick={clearMessages}
        style={{
          backgroundColor: 'transparent',
          border: 'none',
          color: 'black',
          cursor: 'pointer',
          fontSize: '14px',
        }}
      >
        Clear chat
    </button>
  </div>
);
