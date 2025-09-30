import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './components/context/AuthProvider';
import Home from './pages/Home/Home';
import Login from './pages/Login/Login';
import Register from './pages/Login/Register';
import Dashboard from './pages/Dashboard/Dashboard';
import SearchComic from './pages/SearchComic/SearchComic';
import SearchAnime from './pages/SearchAnime/SearchAnime';
import UserLibrary from './pages/UserLibrary/UserLibrary';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />{' '}
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/search/anime" element={<SearchAnime />} />
          <Route path="/search/comic" element={<SearchComic />} />
          <Route path="/user/library" element={<UserLibrary />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
