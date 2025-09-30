import { Link } from "react-router-dom";


function Dashboard() {

    return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
            <div>
                <Link to="/search/anime">
                    <button style={{ margin: '10px', padding: '10px 20px' }}>Search Anime</button>
                </Link>
                <Link to="/search/comic">
                    <button style={{ margin: '10px', padding: '10px 20px' }}>Search Comic</button>
                </Link>
            </div>
        </div>
    );
}

export default Dashboard;

