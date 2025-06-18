import { useState, useEffect } from 'react';
import { type Message } from '../model/Message';
import { type ChatSession } from '../model/ChatSession';
import { fetchChatbotReply, createChatSession, deleteChatSession } from '../api/chatbot';
import { Header } from './Header';
import { Messages } from './Messages';
import { Sidebar } from './Sidebar';
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
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);

  /**
   * Messages shown in the chat.
   * Initialized from sessionStorage to keep messages between refreshes.
   */
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
    if (saved && saved.length > 0) {
      try {
        const parsed = JSON.parse(saved);
        setSessions(parsed);
        if (parsed.length > 0) {
          setCurrentSessionId(parsed[0].id);
        }
      } catch (e) {
        console.error("Failed to parse saved chat sessions", e);
      }
    }
  }, []);

  /**
   * Returns the messages of a chat session.
   * @param sessionId The sessionId of the chat session.
   * @returns The messages of the chat with id equals to sessionId
   */
  const getSessionMessages = (sessionId: string | null)  => {
    if (currentSessionId === null){
      console.error("No current session")
      return []
    }
    const chatSession = sessions.find(item => item.id === sessionId);

    if (chatSession){
      return chatSession.messages;
    }
    
    console.error(`No session found with sessionId ${sessionId}`)
    return []
  }

  /**
   * Handles the delete process of a chat session.
   */
  const handleDeleteChat = async () => {
    if (currentSessionId === null){
      console.error("No current session active")
      return
    }

    await deleteChatSession(currentSessionId);
    const updatedSessions = sessions.filter(s => s.id !== currentSessionId);
    setSessions(updatedSessions)
    if (updatedSessions.length === 0) {
      setCurrentSessionId(null);
    } else {
      setCurrentSessionId(updatedSessions[0].id)
    }
  };

  /**
   * Handles the creation process of a chat session.
   */
  const handleNewChat = async () => {
    const id = await createChatSession();
    
    if (id === "") {
      console.error("Add error showage for a couple of seconds.")
      return
    }
    const newSession: ChatSession = { id, messages: [], createdAt: new Date().toISOString() };
    setSessions(prev => [newSession, ...prev]);
    setCurrentSessionId(id);
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

  /**
   * Handles the send process in a chat session.
   */
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

  const openSideBar = () => {
    setIsSidebarOpen(!isSidebarOpen)
  }

  const onSwitchChat = (chatSessionId: string) => {
    openSideBar();
    setCurrentSessionId(chatSessionId)
  }

  const getWelcomePage = () => {
    return(
      <div
        style={chatbotStyles.containerWelcomePage}
      >
        <div style={chatbotStyles.boxWelcomePage}>
          <h2 style={chatbotStyles.welcomePageH2}>{getChatbotText("welcomeMessage")}</h2>
          <p>{getChatbotText("welcomeDescription")}</p>
          <button style={chatbotStyles.welcomePageNewChatButton}
          onClick={handleNewChat}
          >
            {getChatbotText("createNewChat")}
          </button>
        </div>
      </div>
    )
  }

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
           style={{...chatbotStyles.container}}
        >
          {isSidebarOpen && (
            <Sidebar
              onClose={() => setIsSidebarOpen(false)}
              onCreateChat={handleNewChat}
              onSwitchChat={onSwitchChat}
              chatList={sessions}
              activeChatId={currentSessionId}
            />
          )}
          <Header isChat={currentSessionId !== null} openSideBar={openSideBar} clearMessages={handleDeleteChat} />
          {(currentSessionId !== null) ?
            <>
              <Messages messages={getSessionMessages(currentSessionId)} loading={loading} />
              <Input input={input} setInput={setInput} onSend={sendMessage} />
            </>
            : getWelcomePage()
          }
        </div>
      )}
    </>
  );
};
