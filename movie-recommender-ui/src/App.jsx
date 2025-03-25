import React from 'react';
import MovieRecommender from './components/MovieRecommender';
import UserRecommender from './components/UserRecommender';
import './App.css'

function App() {
  return (
    <div>
      <div className='page-header'>
      <h1>🎬 Movie Recommendation System</h1>
      </div>
      <MovieRecommender />
      <hr />
      <UserRecommender />
    </div>
  );
}

export default App;
