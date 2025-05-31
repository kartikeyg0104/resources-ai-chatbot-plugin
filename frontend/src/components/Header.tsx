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
        style={chatbotStyles.clearButton}
      >
        {getChatbotText("clearChat")}
    </button>
  </div>
);
