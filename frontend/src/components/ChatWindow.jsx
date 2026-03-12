import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import API from '../api/client';
import MessageBubble from './MessageBubble';

export default function ChatWindow({ chatId, onChatUpdated }) {
  const { token } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const [streamingText, setStreamingText] = useState('');
  const [streamingMsgId, setStreamingMsgId] = useState(null);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  // Load messages when chat changes
  useEffect(() => {
    if (!chatId) return;
    setMessages([]);
    setStreamingText('');
    setStreamingMsgId(null);
    API.get(`/chats/${chatId}/messages`)
      .then((res) => setMessages(res.data.messages))
      .catch(console.error);
  }, [chatId]);

  // Auto-scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingText]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || streaming) return;
    setInput('');

    // Optimistic user message
    const tempUserMsg = {
      id: Date.now(),
      role: 'user',
      content: text,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    // Start SSE streaming
    setStreaming(true);
    setStreamingText('');

    const baseUrl = '/api';
    const params = new URLSearchParams({
      message: text,
      token: token,
    });
    const url = `${baseUrl}/chats/${chatId}/stream?${params}`;

    try {
      const response = await fetch(url);
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullText = '';
      let msgId = null;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const data = line.slice(6).trim();
          if (data === '[DONE]') continue;

          try {
            const parsed = JSON.parse(data);
            if (parsed.msg_id) {
              msgId = parsed.msg_id;
              setStreamingMsgId(msgId);
            } else if (parsed.token) {
              fullText += parsed.token;
              setStreamingText(fullText);
            }
          } catch (e) {
            // skip non-JSON lines
          }
        }
      }

      // Finalize: add assistant message
      const assistantMsg = {
        id: msgId || Date.now() + 1,
        role: 'assistant',
        content: fullText,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setStreamingText('');
      setStreamingMsgId(null);

      // Update chat title on first message
      if (messages.length === 0) {
        onChatUpdated?.(chatId, text.slice(0, 80));
      }
    } catch (err) {
      console.error('Streaming error:', err);
    } finally {
      setStreaming(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-window">
      <div className="messages-container">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {streaming && streamingText && (
          <div className="message-bubble assistant">
            <div className="bubble-avatar">⚡</div>
            <div className="bubble-content">
              <p>{streamingText}<span className="cursor-blink">▊</span></p>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="chat-input-area">
        <div className="input-wrapper">
          <textarea
            ref={inputRef}
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            rows={1}
            disabled={streaming}
          />
          <button
            className="send-btn"
            onClick={sendMessage}
            disabled={streaming || !input.trim()}
            title="Send message"
          >
            {streaming ? '⟳' : '➤'}
          </button>
        </div>
        <p className="input-hint">Press Enter to send, Shift+Enter for new line</p>
      </div>
    </div>
  );
}
