import React, { useState } from 'react';
import axios from 'axios';
import './UserRecommender.css';

function UserRecommender() {
  const [userId, setUserId] = useState('');
  const [results, setResults] = useState([]);

  const fetchUserRecommendations = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/recommend/user?user_id=${userId}`);
      setResults(response.data.recommendations);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setResults([]);
    }
  };

  return (
    <div className="user-recommender">
      <h2>👤 Recommend for User</h2>
      <div className="form-group">
        <input
          type="number"
          placeholder="Enter user ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <button onClick={fetchUserRecommendations}>Get Recommendations</button>
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

export default UserRecommender;
