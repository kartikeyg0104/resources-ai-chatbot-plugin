import { getChatbotText } from '../data/chatbotTexts';
import { chatbotStyles } from '../styles/styles';

export const ChatbotHeader = () => (
  <div
    style={chatbotStyles.chatbotHeader}
  >
    {getChatbotText('title')}
  </div>
);
