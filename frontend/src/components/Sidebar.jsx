export default function Sidebar({
  chats,
  activeChatId,
  onSelectChat,
  onNewChat,
  onDeleteChat,
  user,
  onLogout,
  isOpen,
  onToggle,
  onShowUpload,
}) {
  return (
    <>
      <button className="sidebar-toggle" onClick={onToggle} title="Toggle sidebar">
        {isOpen ? '✕' : '☰'}
      </button>

      <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <span className="logo-icon-sm">⚡</span>
            <span className="sidebar-title">LexRam.AI</span>
          </div>
          <button className="new-chat-btn" onClick={onNewChat} title="New Chat">
            ＋
          </button>
        </div>

        <div className="sidebar-chats">
          {chats.length === 0 ? (
            <p className="no-chats">No conversations yet</p>
          ) : (
            chats.map((chat) => (
              <div
                key={chat.id}
                className={`chat-item ${chat.id === activeChatId ? 'active' : ''}`}
                onClick={() => onSelectChat(chat.id)}
              >
                <span className="chat-item-icon">💬</span>
                <span className="chat-item-title">{chat.title}</span>
                <button
                  className="chat-item-delete"
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteChat(chat.id);
                  }}
                  title="Delete chat"
                >
                  🗑
                </button>
              </div>
            ))
          )}
        </div>

        <div className="sidebar-footer">
          <button className="sidebar-action-btn" onClick={onShowUpload}>
            📎 Upload Files
          </button>
          <div className="sidebar-user">
            <div className="user-avatar">
              {user?.username?.[0]?.toUpperCase() || 'U'}
            </div>
            <span className="user-name">{user?.username}</span>
            <button className="logout-btn" onClick={onLogout} title="Logout">
              ⎋
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
