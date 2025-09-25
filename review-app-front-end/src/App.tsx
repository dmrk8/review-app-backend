import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SearchComic from './Pages/SearchComic/SearchComic';
import SearchAnime from './Pages/SearchAnime/SearchAnime';
import HomePage from './Pages/HomePage/HomePage';


function App() {
  return (
    <BrowserRouter>
      <Routes>  
        <Route path="/" element={<HomePage />} />
        <Route path="/search/anime" element={<SearchAnime/>} />
        <Route path="/search/comic" element={<SearchComic />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;