import { useState, useEffect } from 'react';
import type { LibraryReviewType } from '../../types/LibraryReviewType';
import api from '../../components/api/api';
import { useNavigate } from 'react-router-dom';

export default function UserLibrary() {
  const navigate = useNavigate();

  const [library, setLibrary] = useState<LibraryReviewType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchLibrary() {
      try {
        const res = await api.get('review/library');
        setLibrary(res.data);
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (err: any) {
        setError(
          err.response?.data?.detail || err.message || 'Failed to load library'
        );
      } finally {
        setLoading(false);
      }
    }
    fetchLibrary();
  }, []);

  async function handleUpdate(updated: LibraryReviewType) {
    try {
      await api.put(`review/update/${updated.type}`, {
        review_id: updated.review_id,
        review: updated.review,
        rating: updated.rating,
      });
      // Update local state to reflect changes
      setLibrary((prevLibrary) =>
        prevLibrary.map((item) =>
          item.review_id === updated.review_id ? { ...item, ...updated } : item
        )
      );
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update review');
    }
  }

  async function handleDelete(deleted: LibraryReviewType) {
    try {
      await api.delete(
        `review/delete/${deleted.type}/${deleted.review_id}`
      );

      navigate('/user/library');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete review');
    }
  }

  const handleEdit = (item: LibraryReviewType) => {
    const newReview = window.prompt('Edit Review:', item.review);
    if (newReview === null) return; // User canceled
    const newRatingStr = window.prompt(
      'Edit Rating (1-10):',
      item.rating?.toString()
    );
    if (newRatingStr === null) return; // User canceled
    const newRating = parseInt(newRatingStr, 10);
    if (isNaN(newRating) || newRating < 1 || newRating > 10) {
      alert('Invalid rating. Please enter a number between 1 and 10.');
      return;
    }
    const updated = { ...item, review: newReview, rating: newRating };
    handleUpdate(updated);
  };

  if (loading) return <div>Loading Library...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <h2>Your Library</h2>
      {library.length === 0 ? (
        <p>No reviews found.</p>
      ) : (
        <ul>
          {library.map((item) => (
            <li key={item.review_id} style={{ marginBottom: '1em' }}>
              {item.cover_image && (
                <img src={item.cover_image} alt={item.title} width={100} />
              )}
              <div>
                <strong>Title:</strong> {item.title}
              </div>
              <div>
                <strong>Description:</strong> {item.description}
              </div>
              <div>
                <strong>Type:</strong> {item.type}
              </div>
              <div>
                <strong>Review:</strong> {item.review}
              </div>
              <div>
                <strong>Rating:</strong> {item.rating}
              </div>
              <div>
                <strong>Start Year:</strong> {item.start_year}
              </div>
              <div>
                <strong>End Year:</strong> {item.end_year}
              </div>
              <div>
                <strong>Created At:</strong> {item.created_at}
              </div>
              <div>
                <strong>Updated At:</strong> {item.updated_at}
              </div>
              {/* Action buttons */}
              <div style={{ marginTop: '0.5em' }}>
                <button onClick={() => handleEdit(item)}>Edit</button>
                <button
                  onClick={() => {
                    if (
                      window.confirm(
                        'Are you sure you want to delete this review?'
                      )
                    ) {
                      handleDelete(item);
                    }
                  }}
                  style={{ marginLeft: '0.5em', color: 'red' }}
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
