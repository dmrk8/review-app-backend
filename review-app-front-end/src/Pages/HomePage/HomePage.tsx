import { Link } from "react-router-dom";

function HomePage() {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Welcome to My Media Library</h1>
      <div style={{ marginTop: "20px" }}>
        <Link to="/search/anime">
          <button style={{ margin: "10px", padding: "10px 20px" }}>Search Anime</button>
        </Link>
        <Link to="/search/comic">
          <button style={{ margin: "10px", padding: "10px 20px" }}>Search Comic</button>
        </Link>
      </div>
    </div>
  );
}

export default HomePage;
