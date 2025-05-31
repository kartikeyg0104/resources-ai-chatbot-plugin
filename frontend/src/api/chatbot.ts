import { type Message } from '../model/Message';
import { API_BASE_URL } from '../config';
import { getChatbotText } from '../data/chatbotTexts';
import { v4 as uuidv4 } from 'uuid';

export const fetchChatbotReply = async (userMessage: string): Promise<Message> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chatbot/reply`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userMessage }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();

    return createBotMessage(data.reply || getChatbotText('noResponseMessage'));
  } catch (error) {
    console.error('Chatbot API error:', error);
    return createBotMessage(getChatbotText('errorMessage'));
  }
};

export const createBotMessage = (text: string): Message => ({
  id: uuidv4(),
  sender: 'jenkins-bot',
  text,
});
