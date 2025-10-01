import { useState } from 'react';
import CreateReviewButton from '../../components/reviews/CreateReviewButton';

type Comic = {
  media_id: number;
  title: string; // equivalent to alias "title"
  description?: string; // optional
  start_year?: number; // optional
  end_year?: number; // optional
  type: string;
  cover_image?: string; // optional
};

function SearchComic() {
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<Comic[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/media/search/comic?query=${encodeURIComponent(
          query
        )}`
      );
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error(error);
      setResults([]);
    }
    setLoading(false);
  };

  return (
    <div>
      <h1>Search Comic</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for comics.."
      />
      <button onClick={handleSearch}>Search</button>
      {loading && <p>Loading...</p>}
      <ul>
        {results.map((comic) => (
          <li key={comic.media_id}>
            {comic.cover_image && <img src={comic.cover_image} />}
            <h3>{comic.title}</h3>
            <p>{comic.description}</p>
            <p>{comic.start_year}</p>
            <p>{comic.end_year}</p>
            <p>Type: {comic.type}</p>
            {/* Add the CreateReviewButton here */}
            <CreateReviewButton
              mediaType={comic.type}
              mediaId={comic.media_id}
              title={comic.title}
            />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SearchComic;
