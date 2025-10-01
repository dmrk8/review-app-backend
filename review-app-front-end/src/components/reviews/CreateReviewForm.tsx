import { useState } from 'react';
import api from '../api/api';

interface CreateReviewFormProps {
  mediaType: string;
  mediaId: number;
  title: string;
  onClose: () => void;
  onCreated?: () => void;
}

export default function CreateReviewForm({
  mediaType,
  mediaId,
  title,
  onClose,
  onCreated,
}: CreateReviewFormProps) {
  const [review, setReview] = useState('');
  const [rating, setRating] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!review.trim()) {
      setError('Review cannot be empty');
      return;
    }
    if (rating < 1 || rating > 10) {
      setError('Rating must be between 1 and 10');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await api.post('/review/create', {
        media_id: mediaId,
        title,
        type: mediaType,
        review,
        rating: parseFloat(rating.toFixed(1)),
      });

      if (onCreated) onCreated();
      onClose(); // close modal
      setReview('');
      setRating(5);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create review');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0,0,0,0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000,
      }}
    >
      <form
        onSubmit={handleSubmit}
        style={{
          backgroundColor: 'green',
          padding: '1.5em',
          borderRadius: '8px',
          width: '320px',
          display: 'flex',
          flexDirection: 'column',
          gap: '1em',
        }}
      >
        <h3>Create Review for "{title}"</h3>

        <label>
          Review:
          <textarea
            value={review}
            onChange={(e) => setReview(e.target.value)}
            rows={4}
            style={{ width: '100%', marginTop: '0.3em' }}
          />
        </label>

        <label>
          Rating (1-10):
          <input
            type="number"
            min={1}
            max={10}
            value={rating}
            onChange={(e) => setRating(Number(e.target.value))}
            style={{ width: '60px', marginLeft: '0.5em' }}
          />
        </label>

        {error && <p style={{ color: 'red' }}>{error}</p>}

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5em' }}>
          <button type="button" onClick={onClose} disabled={loading}>
            Cancel
          </button>
          <button type="submit" disabled={loading}>
            {loading ? 'Saving...' : 'Save'}
          </button>
        </div>
      </form>
    </div>
  );
}
