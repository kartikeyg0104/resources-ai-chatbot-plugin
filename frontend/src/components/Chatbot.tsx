import { useState, useEffect } from 'react';
import { type Message } from '../model/Message';
import { type ChatSession } from '../model/ChatSession';
import { fetchChatbotReply, createChatSession, deleteChatSession } from '../api/chatbot';
import { Header } from './Header';
import { Messages } from './Messages';
import { Input } from './Input';
import { chatbotStyles } from '../styles/styles';
import { getChatbotText } from '../data/chatbotTexts';
import { v4 as uuidv4 } from 'uuid';

/**
 * Chatbot is the core component responsible for managing the chatbot display.
 */
export const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [isChat, setIsChat] = useState<boolean>(false);

  /**
   * Messages shown in the chat.
   * Initialized from sessionStorage to keep messages between refreshes.
   */
  const [messages, setMessages] = useState<Message[]>(() => {
    const saved = sessionStorage.getItem('chatbot-messages');
    return saved ? JSON.parse(saved) : [];
  });
  const [loading, setLoading] = useState(false);

  /**
   * Saving the chat sessions in the session storage only 
   * when the component umounts to avoid continuos savings.
   */
  useEffect(() => {
    return () => {
      sessionStorage.setItem('chatbot-sessions', JSON.stringify(sessions));
    };
  }, [sessions]);

  /**
   * Loading the chat sessions from the session storage at mount time.
   */
  useEffect(() => {
    const saved = sessionStorage.getItem('chatbot-sessions');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setSessions(parsed);
        if (parsed.length > 0) {
          setCurrentSessionId(parsed[0].id);
          setIsChat(true);
        }
      } catch (e) {
        console.error("Failed to parse saved chat sessions", e);
      }
    }
  }, []);

  useEffect(() => {
    //sessionStorage.setItem('chatbot-messages', JSON.stringify(messages));
  }, [currentSessionId, sessions]);

  const getSessionMessages = (sessionId: string | null)  => {
    if (currentSessionId === null){
      console.error("No current session")
      return []
    }
    let chatSession = sessions.find(item => item.id === sessionId);

    if (chatSession){
      return chatSession.messages;
    }
    
    console.error(`No session found with sessionId ${sessionId}`)
    return []
  }

  const handleDeleteChat = async () => {
    if (currentSessionId === null){
      console.error("No current session active")
      return
    }

    await deleteChatSession(currentSessionId);
    const updatedSessions = sessions.filter(s => s.id !== currentSessionId);
    setSessions(updatedSessions)
    if (updatedSessions.length === 0) {
      setIsChat(false)
      setCurrentSessionId(null);
    } else {
      setCurrentSessionId(updatedSessions[0].id)
    }
  };

  const handleNewChat = async () => {
    const id = await createChatSession();
    
    if (id === "") {//TODO
      console.error("Add error showage for a couple of seconds.")
      return
    }
    const newSession: ChatSession = { id, messages: [], createdAt: new Date().toISOString() };
    setSessions(prev => [newSession, ...prev]);
    setCurrentSessionId(id);
    setIsChat(true)
  };

  const appendMessageToCurrentSession = (message: Message) => {
    setSessions(prevSessions =>
      prevSessions.map(session =>
        session.id === currentSessionId
          ? { ...session, messages: [...session.messages, message] }
          : session
      )
    );
  };

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed || !currentSessionId) {
      console.error("Empty message or no sessions available")
      return;
    }
    const userMessage: Message = {
      id: uuidv4(),
      sender: 'user',
      text: trimmed,
    };

    setInput('');
    setLoading(true);
    appendMessageToCurrentSession(userMessage);

    const botReply = await fetchChatbotReply(currentSessionId!, trimmed);
    setLoading(false);
    appendMessageToCurrentSession(botReply);
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={chatbotStyles.toggleButton}
      >
        {getChatbotText("toggleButtonLabel")}
      </button>

      {isOpen && (
        <div
           style={chatbotStyles.container}
        >
          <Header clearMessages={handleDeleteChat} />
          {isChat ?
            <>
              <Messages messages={getSessionMessages(currentSessionId)} loading={loading} />
              <Input input={input} setInput={setInput} onSend={sendMessage} />
            </>
            :
            <div
              style={{
                height: '70%',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
              }}
            >
              <div style={{ textAlign: 'center', color: '#888' }}>
                <h2 style={{ marginBottom: '0.5rem' }}>Welcome to Jenkins AI Assistant</h2>
                <p>Create a new chat to get started.</p>
                <button style={{
                  backgroundColor:"#0073e6",
                  padding: "1rem",
                  borderRadius: "1rem",
                  color: '#ffffff',
                  cursor: 'pointer',
                  border: 0
                }}
                onClick={handleNewChat}
                >
                  Start Chatting
                </button>
              </div>
            </div>
          }
        </div>
      )}
    </>
  );
};
