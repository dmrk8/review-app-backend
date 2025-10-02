import { useCallback, useState } from 'react';
import CreateReviewButton from '../../components/reviews/CreateReviewButton';
import { UseInfiniteScroll } from '../../components/useInfiniteScroll';

type Anime = {
  media_id: number;
  title: string; // equivalent to alias "title"
  description?: string; // optional
  start_year?: number; // optional
  end_year?: number; // optional
  type: string;
  cover_image?: string;
};

function SearchAnime() {
  const [page, setPage] = useState<number>(1);
  const [hasNextPage, setHasNextPage] = useState<boolean>(true);
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<Anime[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSearch = useCallback(
    async (newPage = 1) => {
      if (!hasNextPage && newPage !== 1) return; // Stop if no more pages
      try {
        setLoading(true);
        const response = await fetch(
          `http://127.0.0.1:8000/media/search/anime?query=${encodeURIComponent(
            query
          )}&page=${newPage}&per_page=10`
        );
        const data = await response.json();

        setResults((prev) =>
          newPage === 1 ? data.results : [...prev, ...data.results]
        );

        setPage(data.page + 1);
        setHasNextPage(data.hasNextPage);
      } catch (error) {
        console.error(error);
        if (page === 1) setResults([]);
      } finally {
        setLoading(false);
      }
    },
    [query, hasNextPage]
  );

  UseInfiniteScroll({
    callback: () => handleSearch(page),
    isLoading: loading,
    hasNextPage: hasNextPage,
  })

  return (
    <div>
      <h3>Search Anime</h3>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for anime..."
      />
      <button onClick={() => handleSearch(1)}>Search</button>
      {loading && <p>Loading...</p>}
      <ul>
        {results.map((anime) => (
          <li key={anime.media_id}>
            {anime.cover_image && (
              <img src={anime.cover_image} alt={anime.title} />
            )}
            <h3>{anime.title}</h3>
            <p>{anime.description}</p>
            <p>{anime.start_year}</p>
            <p>{anime.end_year}</p>
            <p>Type: {anime.type}</p>

            {/* Add the CreateReviewButton here */}
            <CreateReviewButton
              mediaType={anime.type}
              mediaId={anime.media_id}
              title={anime.title}
            />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SearchAnime;
