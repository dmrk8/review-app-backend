import SearchMedia from '../../components/SearchMedia';

function SearchComic() {
  return (
    <SearchMedia
      mediaType="comic"
      apiEndpoint="/media/search/comic"
      placeholder="Search for comic..."
    />
  );
}

export default SearchComic;
