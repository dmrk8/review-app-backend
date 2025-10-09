import { useCallback, useRef, useState } from 'react';
import { UseInfiniteScroll } from './useInfiniteScroll';
import MediaModal from './MediaModal';
import SearchBar from './SearchBar';
import BoxGrid from './BoxGrid';
import type { MediaType } from '../types/Media';

interface SearchMediaProps {
  mediaType: string; // e.g., "anime", "manga", "movies"
  apiEndpoint: string; // API endpoint for fetching media
  placeholder?: string; // Placeholder for the search bar
}

function SearchMedia({
  mediaType,
  apiEndpoint,
  placeholder = 'Search...',
}: SearchMediaProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [page, setPage] = useState<number>(1);
  const [hasNextPage, setHasNextPage] = useState<boolean>(true);
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<MediaType[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedMedia, setSelectedMedia] = useState<MediaType | null>(null);

  const handleSearch = useCallback(
    async (newPage = 1) => {
      if (!hasNextPage && newPage !== 1) return;
      try {
        setLoading(true);

        const perPage = newPage === 1 ? 30 : 10;

        const response = await fetch(
          `${apiEndpoint}?query=${encodeURIComponent(
            query
          )}&page=${newPage}&per_page=${perPage}`
        );
        const data = await response.json();

        setResults((prev) =>
          newPage === 1 ? data.results : [...prev, ...data.results]
        );

        setPage(data.page + 1);
        setHasNextPage(data.hasNextPage);
      } catch (error) {
        console.error(error);
        if (newPage === 1) setResults([]);
      } finally {
        setLoading(false);
      }
    },
    [query, hasNextPage, apiEndpoint]
  );

  UseInfiniteScroll({
    callback: () => handleSearch(page),
    isLoading: loading,
    hasNextPage: hasNextPage,
    container: containerRef.current,
  });

  return (
    <div className="h-screen flex flex-col">
      {/* Search bar */}
      <SearchBar
        value={query}
        onChange={(value) => setQuery(value)}
        onSearch={() => handleSearch(1)}
        placeholder={placeholder}
      />

      {/* Box grid */}
      <div ref={containerRef} className="flex-1 overflow-auto p-4">
        <BoxGrid
          items={results}
          renderItem={(media) =>
            media.cover_image ? (
              <div
                key={media.media_id}
                className="relative cursor-pointer transform hover:scale-105 transition-transform"
                onClick={() => setSelectedMedia(media)}
              >
                <img
                  src={media.cover_image}
                  alt={media.title}
                  className="w-full h-48 object-cover rounded-xl shadow-lg"
                />
                <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity rounded-xl">
                  <span className="text-white text-center font-semibold">
                    {media.title}
                  </span>
                </div>
              </div>
            ) : null
          }
        />
        {loading && <p className="text-center mt-4">Loading...</p>}
      </div>

      {/* Modal */}
      <MediaModal
        media={selectedMedia}
        onClose={() => setSelectedMedia(null)}
      />
    </div>
  );
}

export default SearchMedia;
