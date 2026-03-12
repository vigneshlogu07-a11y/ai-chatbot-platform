import { useState, useEffect } from 'react';
import API from '../api/client';
import { useAuth } from '../context/AuthContext';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';
import UploadPanel from '../components/UploadPanel';

export default function ChatPage() {
  const { user, logout } = useAuth();
  const [chats, setChats] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);
  const [showUpload, setShowUpload] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Load chats on mount
  useEffect(() => {
    loadChats();
  }, []);

  const loadChats = async () => {
    try {
      const res = await API.get('/chats/');
      setChats(res.data.chats);
    } catch (err) {
      console.error('Failed to load chats:', err);
    }
  };

  const createChat = async () => {
    try {
      const res = await API.post('/chats/', { title: 'New Chat' });
      setChats((prev) => [res.data, ...prev]);
      setActiveChatId(res.data.id);
    } catch (err) {
      console.error('Failed to create chat:', err);
    }
  };

  const deleteChat = async (chatId) => {
    try {
      await API.delete(`/chats/${chatId}`);
      setChats((prev) => prev.filter((c) => c.id !== chatId));
      if (activeChatId === chatId) setActiveChatId(null);
    } catch (err) {
      console.error('Failed to delete chat:', err);
    }
  };

  const onChatUpdated = (chatId, newTitle) => {
    setChats((prev) =>
      prev.map((c) => (c.id === chatId ? { ...c, title: newTitle } : c))
    );
  };

  return (
    <div className="chat-page">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onSelectChat={setActiveChatId}
        onNewChat={createChat}
        onDeleteChat={deleteChat}
        user={user}
        onLogout={logout}
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        onShowUpload={() => setShowUpload(true)}
      />

      <main className={`chat-main ${sidebarOpen ? '' : 'expanded'}`}>
        {activeChatId ? (
          <ChatWindow
            chatId={activeChatId}
            onChatUpdated={onChatUpdated}
          />
        ) : (
          <div className="chat-empty">
            <div className="empty-icon">⚡</div>
            <h2>LexRam.AI</h2>
            <p>Select a conversation or start a new chat to begin.</p>
            <button className="start-chat-btn" onClick={createChat}>
              + New Chat
            </button>
          </div>
        )}
      </main>

      {showUpload && (
        <UploadPanel
          chatId={activeChatId}
          onClose={() => setShowUpload(false)}
        />
      )}
    </div>
  );
}
