import React, { useState } from 'react';
import axios from 'axios';
import './MovieRecommender.css';

function MovieRecommender() {
  const [title, setTitle] = useState('');
  const [results, setResults] = useState([]);

  const fetchRecommendations = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/recommend/movie?title=${encodeURIComponent(title)}`);
      setResults(response.data.recommendations);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setResults([]);
    }
  };

  return (
    <div className="movie-recommender">
      <h2>📽️ Recommend Based on Movie</h2>
      <div className="form-group">
        <input
          type="text"
          placeholder="Enter movie title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button onClick={fetchRecommendations}>Get Recommendations</button>
      </div>

      <ul>
        {results.map((movie, index) => (
          <li key={index}>
            {movie.title} — {movie.genre}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MovieRecommender;
