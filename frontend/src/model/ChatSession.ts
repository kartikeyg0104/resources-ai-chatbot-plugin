import { type Message } from './Message';

export interface ChatSession {
  id: string;
  messages: Message[];
  createdAt: string;
}
