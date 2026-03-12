import { useState } from 'react';
import API from '../api/client';

export default function FeedbackButtons({ messageId }) {
  const [rating, setRating] = useState(null); // 'like' | 'dislike' | null
  const [showComment, setShowComment] = useState(false);
  const [comment, setComment] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const sendFeedback = async (newRating) => {
    const r = rating === newRating ? null : newRating;
    setRating(r);
    if (!r) return;
    try {
      await API.post('/feedback/', {
        message_id: messageId,
        rating: r,
        comment: comment || null,
      });
    } catch (err) {
      console.error('Feedback error:', err);
    }
  };

  const submitComment = async () => {
    if (!comment.trim()) return;
    try {
      await API.post('/feedback/', {
        message_id: messageId,
        rating: rating || 'like',
        comment: comment,
      });
      setSubmitted(true);
      setTimeout(() => setShowComment(false), 1500);
    } catch (err) {
      console.error('Comment error:', err);
    }
  };

  return (
    <div className="feedback-buttons">
      <button
        className={`fb-btn ${rating === 'like' ? 'active-like' : ''}`}
        onClick={() => sendFeedback('like')}
        title="Helpful"
      >
        👍
      </button>
      <button
        className={`fb-btn ${rating === 'dislike' ? 'active-dislike' : ''}`}
        onClick={() => sendFeedback('dislike')}
        title="Not helpful"
      >
        👎
      </button>
      <button
        className="fb-btn fb-comment-btn"
        onClick={() => setShowComment(!showComment)}
        title="Add comment"
      >
        💬
      </button>

      {showComment && (
        <div className="feedback-comment-box">
          {submitted ? (
            <p className="comment-thanks">Thanks for your feedback!</p>
          ) : (
            <>
              <textarea
                className="comment-input"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Tell us more (optional)..."
                rows={2}
              />
              <button className="comment-submit" onClick={submitComment}>
                Submit
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}
