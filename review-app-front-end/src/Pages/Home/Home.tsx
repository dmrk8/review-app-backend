import { Link } from 'react-router-dom';

function Home() {
  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Welcome to My Media Library</h1>
      <div style={{ marginTop: '20px' }}>
        <Link to="/login">
          <button style={{ margin: '10px', padding: '10px 20px' }}>
            Login
          </button>
        </Link>
        <Link to="/register">
          <button style={{ margin: '10px', padding: '10px 20px' }}>
            Register
          </button>
        </Link>
      </div>
    </div>
  );
}

export default Home;
