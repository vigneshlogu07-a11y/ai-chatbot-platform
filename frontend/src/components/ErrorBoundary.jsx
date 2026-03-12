import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI.
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // You can also log the error to an error reporting service
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return (
        <div style={{ padding: '2rem', textAlign: 'center', backgroundColor: '#1a1b26', color: '#e0af68', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <h2 style={{ color: '#f7768e', marginBottom: '1rem' }}>Oops! Something went wrong in the UI.</h2>
          <div style={{ padding: '1rem', backgroundColor: '#16161e', borderRadius: '8px', maxWidth: '600px', whiteSpace: 'pre-wrap', wordBreak: 'break-word', border: '1px solid #f7768e' }}>
            <p style={{ fontFamily: 'monospace' }}>{this.state.error?.toString()}</p>
          </div>
          <button 
            onClick={() => window.location.href = '/'}
            style={{ marginTop: '2rem', padding: '0.75rem 1.5rem', backgroundColor: '#7aa2f7', color: '#1a1b26', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}
          >
            Return to Home
          </button>
        </div>
      );
    }

    return this.props.children; 
  }
}

export default ErrorBoundary;
