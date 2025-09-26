import { useState } from "react";


type Anime = {
    media_id: number;
    title_english: string;        // equivalent to alias "title"
    description?: string;         // optional
    start_year?: number;          // optional
    end_year?: number;            // optional
    type: string;
    cover_image?: string;
};


function SearchAnime() {

    const [query, setQuery] = useState<string>('');
    const [results, setResults] = useState<Anime[]>([]);
    const [loading, setLoading] = useState<boolean>(false);

    const handleSearch = async () => {
        try {
            setLoading(true);
            const response = await fetch(
                `http://127.0.0.1:8000/media/search/anime?query=${encodeURIComponent(query)}`
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
            <h3>Search Anime</h3>
            <input
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Search for animes..."
            />
            <button onClick={handleSearch}>Search</button>
            {loading && <p>loading...</p>}
            <ul>
                {results.map(anime =>
                    <li key={anime.media_id}>
                        {anime.cover_image && <img src={anime.cover_image} />}
                        <h3>{anime.title_english}</h3>
                        <p>{anime.description}</p>
                        <p>{anime.start_year}</p>
                        <p>{anime.end_year}</p>
                        <p>Type: {anime.type}</p>
                    </li>
                )}
            </ul>
        </div>
    )
}

export default SearchAnime