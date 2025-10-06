import { useState, useEffect, useCallback } from 'react';
import api from '../../components/api/api';
import { useNavigate } from 'react-router-dom';
import { UseInfiniteScroll } from '../../components/useInfiniteScroll';
import type { LibraryReviewType } from '../../types/LibraryReviewType';

export default function UserLibrary() {
  const navigate = useNavigate();

  const [library, setLibrary] = useState<LibraryReviewType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState<number>(1);
  const [perPage] = useState<number>(10);
  const [hasNextPage, setHasNextPage] = useState<boolean>(true);

  // Sorting and filtering
  const [sortBy, setSortBy] = useState<string>('created_at');
  const [sortOrder, setSortOrder] = useState<number>(-1); // 1 = ascending, -1 = descending
  const [filters, setFilters] = useState<Record<string, any>>({});

  const fetchLibrary = useCallback(
    async (newPage = 1) => {
      try {
        setLoading(true);
        const res = await api.get('review/library/anime', {
          params: {
            page: newPage,
            per_page: perPage,
            sort_by: sortBy,
            sort_order: sortOrder,
            ...filters,
          },
        });
        const data = res.data;

        setLibrary((prev) =>
          newPage === 1 ? data.results : [...prev, ...data.results]
        );

        // Add these to fix infinite scroll
        setPage(newPage);
        setHasNextPage(data.hasNextPage);
      } catch (err: any) {
        setError(
          err.response?.data?.detail || err.message || 'Failed to load library'
        );
      } finally {
        setLoading(false);
      }
    },
    [perPage, sortBy, sortOrder, filters]
  );

  useEffect(() => {
    fetchLibrary(1);
  }, [fetchLibrary]);

  UseInfiniteScroll({
    callback: () => fetchLibrary(page + 1),
    isLoading: loading,
    hasNextPage,
  });

  // Add the missing functions
  const handleEdit = (item: LibraryReviewType) => {
    const newReview = window.prompt('Edit Review:', item.review);
    if (newReview === null) return;
    const newRatingStr = window.prompt(
      'Edit Rating (1-10):',
      item.rating?.toString()
    );
    if (newRatingStr === null) return;
    const newRating = parseInt(newRatingStr, 10);
    if (isNaN(newRating) || newRating < 1 || newRating > 10) {
      alert('Invalid rating. Please enter a number between 1 and 10.');
      return;
    }
    const updated = { ...item, review: newReview, rating: newRating };
    handleUpdate(updated);
  };

  const handleUpdate = async (updated: LibraryReviewType) => {
    try {
      await api.put(`review/update/${updated.type}`, {
        review_id: updated.review_id,
        review: updated.review,
        rating: updated.rating,
      });
      setLibrary((prev) =>
        prev.map((item) =>
          item.review_id === updated.review_id ? { ...item, ...updated } : item
        )
      );
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update review');
    }
  };

  const handleDelete = async (item: LibraryReviewType) => {
    try {
      await api.delete(`review/delete/${item.type}/${item.review_id}`);
      setLibrary((prev) => prev.filter((i) => i.review_id !== item.review_id));
      navigate('/user/library');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete review');
    }
  };

  if (loading && page === 1) return <div>Loading Library...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <h2>Your Library</h2>
      {/* Sorting & filtering controls */}
      <div style={{ marginBottom: '1em' }}>
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="created_at">Sort by Date</option>
          <option value="rating">Sort by Rating</option>
          <option value="title">Sort by Title</option>
        </select>
        <button onClick={() => setSortOrder(sortOrder * -1)}>
          {sortOrder === 1 ? 'Asc ↑' : 'Desc ↓'}
        </button>
        <input
          type="text"
          placeholder="Filter by title"
          onChange={(e) => setFilters((f) => ({ ...f, title: e.target.value }))}
          style={{ marginLeft: '0.5em' }}
        />
      </div>
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
                  onClick={() => handleDelete(item)}
                  style={{ marginLeft: '0.5em', color: 'red' }}
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}

      {loading && page > 1 && <p>Loading more...</p>}
    </div>
  );
}
