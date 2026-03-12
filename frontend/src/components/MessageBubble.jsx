import FeedbackButtons from './FeedbackButtons';

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`message-bubble ${message.role}`}>
      <div className="bubble-avatar">
        {isUser ? '👤' : '⚡'}
      </div>
      <div className="bubble-content">
        <p>{message.content}</p>
        <span className="bubble-time">
          {new Date(message.created_at).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </span>
        {!isUser && <FeedbackButtons messageId={message.id} />}
      </div>
    </div>
  );
}
