import { useState, useEffect, useRef } from 'react';
import API from '../api/client';

export default function UploadPanel({ chatId, onClose }) {
  const [docs, setDocs] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState('');
  const fileInput = useRef(null);

  useEffect(() => {
    loadDocs();
  }, []);

  const loadDocs = async () => {
    try {
      const res = await API.get('/documents/');
      setDocs(res.data.documents);
    } catch (err) {
      console.error('Failed to load documents:', err);
    }
  };

  const uploadFile = async (file) => {
    setError('');
    const allowed = ['pdf', 'txt', 'docx'];
    const ext = file.name.split('.').pop().toLowerCase();
    if (!allowed.includes(ext)) {
      setError(`File type .${ext} not allowed. Use: ${allowed.join(', ')}`);
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('File exceeds 10MB limit');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    if (chatId) formData.append('chat_id', chatId);

    try {
      await API.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      loadDocs();
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer.files[0];
    if (file) uploadFile(file);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) uploadFile(file);
  };

  const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
  };

  return (
    <div className="upload-overlay" onClick={onClose}>
      <div className="upload-panel" onClick={(e) => e.stopPropagation()}>
        <div className="upload-header">
          <h3>📎 Documents</h3>
          <button className="upload-close" onClick={onClose}>✕</button>
        </div>

        <div
          className={`upload-dropzone ${dragActive ? 'active' : ''}`}
          onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          onClick={() => fileInput.current?.click()}
        >
          {uploading ? (
            <div className="upload-spinner" />
          ) : (
            <>
              <span className="dropzone-icon">📄</span>
              <p>Drag & drop a file here, or click to browse</p>
              <small>PDF, TXT, DOCX — Max 10MB</small>
            </>
          )}
          <input
            ref={fileInput}
            type="file"
            accept=".pdf,.txt,.docx"
            onChange={handleFileSelect}
            hidden
          />
        </div>

        {error && <div className="upload-error">{error}</div>}

        <div className="upload-list">
          <h4>Uploaded Files ({docs.length})</h4>
          {docs.length === 0 ? (
            <p className="no-docs">No documents uploaded yet</p>
          ) : (
            docs.map((doc) => (
              <div key={doc.id} className="doc-item">
                <span className="doc-icon">
                  {doc.file_type === 'pdf' ? '📕' : doc.file_type === 'docx' ? '📘' : '📄'}
                </span>
                <div className="doc-info">
                  <span className="doc-name">{doc.original_name}</span>
                  <span className="doc-meta">
                    {doc.file_type.toUpperCase()} · {formatSize(doc.file_size)}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
