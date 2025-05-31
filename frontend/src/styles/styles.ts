import { type CSSProperties } from 'react';

export const chatbotStyles = {  
  toggleButton: {
    position: 'fixed',
    bottom: '3rem',
    right: '2rem',
    zIndex: 1000,
    borderRadius: '50%',
    width: '60px',
    height: '60px',
    backgroundColor: '#0073e6',
    color: 'white',
    fontSize: '24px',
    border: 'none',
    cursor: 'pointer',
  } as CSSProperties,

  container: {
    position: 'fixed',
    bottom: '6rem',
    right: '2rem',
    width: '600px',
    height: '800px',
    backgroundColor: 'white',
    border: '1px solid #ccc',
    borderRadius: '10px',
    display: 'flex',
    flexDirection: 'column',
    zIndex: 999,
    boxShadow: '0 0 20px rgba(0,0,0,0.2)',
  } as CSSProperties,

  inputContainer: {
    padding: '0.75rem',
    borderTop: '1px solid #eee' 
  },

  input: {
    width: '100%',
    padding: '0.5rem',
    borderRadius: '6px',
    border: '1px solid #ccc',
    fontSize: '14px',
    fontFamily: 'inherit',
    boxSizing: 'border-box',
    scrollbarWidth: 'none',
    msOverflowStyle: 'none',
    minHeight: '60px',
    maxHeight: '150px',
    resize: 'none',
    overflow: 'auto',
    lineHeight: '1.5',
  } as CSSProperties,

  chatbotHeader: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: '1rem',
    borderBottom: '1px solid #eee',
    fontWeight: 'bold',
    fontSize: '16px',
    backgroundColor: '#f5f5f5',
  } as CSSProperties,

  clearButton: {
    backgroundColor: 'transparent',
    border: 'none',
    color: 'black',
    cursor: 'pointer',
    fontSize: '14px',
  },

  messagesMain: {
    flex: 1,
    padding: '0.75rem',
    overflowY: 'auto',
    fontSize: '14px',
  } as CSSProperties,

  messageContainer: (sender: 'user' | 'jenkins-bot'): CSSProperties => ({
    marginBottom: '0.5rem',
    textAlign: sender === 'user' ? 'right' : 'left',
  } as CSSProperties),

  messageBubble: (sender: 'user' | 'jenkins-bot'): CSSProperties => ({
    display: 'inline-block',
    padding: '0.5rem 0.75rem',
    borderTopLeftRadius: sender === 'user' ? 20 : 6,
    borderTopRightRadius: 20,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: sender === 'user' ? 6 : 20,
    backgroundColor: sender === 'user' ? '#0073e6' : '#2d2d2d',
    color: sender === 'user' ? '#fff' : '#f0f0f0',
    maxWidth: '80%',
    wordWrap: 'break-word',
  } as CSSProperties),
};
