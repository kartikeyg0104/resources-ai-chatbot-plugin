import { type Message } from '../model/Message';

export const fetchChatbotReply = async (userMessage: string): Promise<Message> => {
  try {
    const response = await fetch('http://localhost:5000/api/chatbot/reply', {
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

    return {
      id: Date.now(), // Later use UUID
      sender: 'jenkins-bot',
      text: data.reply || 'No response',
    };
  } catch (error) {
    console.error('Chatbot API error:', error);
    return {
      id: Date.now(),
      sender: 'jenkins-bot',
      text: 'Sorry, I had trouble responding.',
    };
  }
};
