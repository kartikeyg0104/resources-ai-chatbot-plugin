import type { ChatSession } from "../model/ChatSession";

interface SidebarProps {
  onClose: () => void;
  onCreateChat: () => void;
  onSwitchChat: (chatSessionId: string) => void;
  chatList: ChatSession[];
  activeChatId: string | null;
}

export const Sidebar = ({ onClose, onCreateChat, onSwitchChat, chatList, activeChatId }: SidebarProps) => {
    const getChatName = (chat: ChatSession, index: number) => {
        if (chat.messages.length > 0){
            let firstMessage = chat.messages[0].text;
            return firstMessage.slice(0, 20);
        }

        return `Chat ${index + 1}`
    }
  return (
    <div style={{
      position: 'absolute',
      top: 0,
      left: 0,
      height: '96%',
      width: '250px',
      backgroundColor: 'rgba(240, 240, 240, 0.9)',
      boxShadow: '2px 0 5px rgba(0,0,0,0.1)',
      zIndex: 10,
      display: 'flex',
      flexDirection: 'column',
      padding: '1rem',
    }}>
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <button
          onClick={onClose}
          style={{
            background: 'none',
            border: 'none',
            fontSize: '1.5rem',
            cursor: 'pointer',
            color: '#555',
            marginBottom: '1rem'
          }}
        >
          &times;
        </button>
      </div>

      <button
        onClick={() => {
            onClose();
            onCreateChat();
        }}
        style={{
          marginBottom: '1rem',
          padding: '0.75rem',
          borderRadius: '0.5rem',
          border: 'none',
          backgroundColor: '#0073e6',
          color: '#fff',
          cursor: 'pointer',
          fontSize: '1rem',
          fontWeight: '500'
        }}
      >
        + Create New Chat
      </button>

       <div style={{ overflowY: 'auto', flex: 1 }}>
        {chatList.length === 0 ? (
          <p style={{ color: '#666' }}>No active chats yet.</p>
        ) : (
          chatList.map((chat, index) => {
            const isActive = chat.id === activeChatId;
            return (
              <div
                key={chat.id}
                onClick={() => onSwitchChat(chat.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  padding: '0.75rem',
                  marginBottom: '0.5rem',
                  borderRadius: '0.5rem',
                  backgroundColor: isActive ? '#d0e7ff' : '#fff',
                  borderLeft: isActive ? '4px solid #0073e6' : '4px solid transparent',
                  fontWeight: isActive ? 'bold' : 'normal',
                  color: isActive ? '#0073e6' : '#333',
                  cursor: 'pointer',
                  transition: 'background 0.2s, border-left 0.2s',
                }}
              >
                {getChatName(chat, index)}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
