import SearchMedia from '../../components/SearchMedia';

function SearchAnime() {
  return (
    <SearchMedia
      mediaType="anime"
      apiEndpoint="http://127.0.0.1:8000/media/search/anime"
      placeholder="Search for anime..."
    />
  );
}

export default SearchAnime;
