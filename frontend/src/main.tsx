import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ChatbotFooter } from './components/ChatbotFooter';

const footerRoot = document.getElementById('root')!;

createRoot(footerRoot).render(
  <StrictMode>
    <ChatbotFooter />
  </StrictMode>,
)
