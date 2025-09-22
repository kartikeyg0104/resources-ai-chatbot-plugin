import { type Message } from "../model/Message";
import { getChatbotText } from "../data/chatbotTexts";
import { v4 as uuidv4 } from "uuid";
import { CHATBOT_API_TIMEOUTS_MS } from "../config";
import { callChatbotApi } from "../utils/callChatbotApi";
import { openChatbotStream, type StreamMessage } from "../utils/callChatbotApi";

/**
 * Send a request to the backend to create a new chat session and returns the id of the
 * chat session created.
 *
 * @returns A Promise resolving to the id of the new chat session
 */
export const createChatSession = async (): Promise<string> => {
  const data = await callChatbotApi<{ session_id: string }>(
    "sessions",
    { method: "POST" },
    { session_id: "" },
    CHATBOT_API_TIMEOUTS_MS.CREATE_SESSION,
  );

  if (!data.session_id) {
    console.error(
      "Failed to create chat session: session_id missing in response",
      data,
    );
    return "";
  }

  return data.session_id;
};

/**
 * Sends the user's message to the backend chatbot API and returns the bot's response.
 * If the API call fails or returns an invalid response, a fallback error message is used.
 *
 * @param sessionId - The session id of the chat
 * @param userMessage - The message input from the user
 * @returns A Promise resolving to a bot-generated Message
 */
export const fetchChatbotReply = async (
  sessionId: string,
  userMessage: string,
): Promise<Message> => {
  const data = await callChatbotApi<{ reply?: string }>(
    `sessions/${sessionId}/message`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage }),
    },
    {},
    CHATBOT_API_TIMEOUTS_MS.GENERATE_MESSAGE,
  );

  const botReply = data.reply || getChatbotText("errorMessage");
  return createBotMessage(botReply);
};

/**
 * Start a WebSocket stream for token-by-token reply.
 * Returns helpers to manage the stream and a function to create a bot message.
 */
export const streamChatbotReply = (
  sessionId: string,
  userMessage: string,
  onToken: (token: string) => void,
  onEnd?: () => void,
  onError?: (error: string) => void,
) => {
  const { send, close, socket } = openChatbotStream(
    sessionId,
    (msg: StreamMessage) => {
      if (msg.type === "token") onToken(msg.token);
      if (msg.type === "end") onEnd && onEnd();
      if (msg.type === "error") onError && onError(msg.error);
    },
  );

  send(userMessage);
  return { close, socket };
};

/**
 * Sends a request to the backend to delete the chat session with session id sessionId.
 *
 * @param sessionId - The session id of the chat to delete
 */
export const deleteChatSession = async (sessionId: string): Promise<void> => {
  await callChatbotApi<void>(
    `sessions/${sessionId}`,
    { method: "DELETE" },
    undefined,
    CHATBOT_API_TIMEOUTS_MS.DELETE_SESSION,
  );
};

/**
 * Utility function to create a Message object from the bot,
 * using a UUID as the message ID.
 *
 * @param text - The text content of the bot's message
 * @returns A new Message object from the bot
 */
export const createBotMessage = (text: string): Message => ({
  id: uuidv4(),
  sender: "jenkins-bot",
  text,
});
