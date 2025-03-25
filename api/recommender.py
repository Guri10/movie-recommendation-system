# api/recommender.py

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import sys
from urllib.parse import quote_plus

# Load environment
sys.path.append(os.path.abspath("/Users/atharvagurav/Documents/movie-recommendation-system"))  # Adjust if needed
import config
load_dotenv()

# Connect to PostgreSQL
DB_PORT = int(config.DB_PORT)
encoded_DB_PASSWORD = quote_plus(config.DB_PASSWORD)
DATABASE_URL = f"postgresql://{config.DB_USER}:{encoded_DB_PASSWORD}@{config.DB_HOST}:{DB_PORT}/{config.DB_NAME}"
engine = create_engine(DATABASE_URL)

# Load Data
movies_df = pd.read_sql("SELECT movie_id, title, genre FROM movies", engine)
ratings_df = pd.read_sql("SELECT user_id, movie_id, rating FROM ratings", engine)
merged = ratings_df.merge(movies_df, on="movie_id")

# Clean Movie Data
movies = merged[['movie_id', 'title', 'genre']].drop_duplicates().reset_index(drop=True)

# Compute movie-level stats
movie_stats = merged.groupby('title').agg({'rating': ['mean', 'count']}).reset_index()
movie_stats.columns = ['title', 'avg_rating', 'rating_count']
movies = movies.merge(movie_stats, on='title')

# Genre TF-IDF
tfidf = TfidfVectorizer(tokenizer=lambda x: x.split(', '))
tfidf_matrix = tfidf.fit_transform(movies['genre'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
movie_indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# -------------------- API Functions --------------------

def recommend_by_title(title, num_recommendations=10):
    if title not in movie_indices:
        return []

    idx = movie_indices[title]
    if isinstance(idx, pd.Series):
        idx = idx.iloc[0]
    idx = int(idx)

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations + 1]

    indices = [i[0] for i in sim_scores if i[0] < len(movies)]
    return movies.iloc[indices][['title', 'genre', 'avg_rating', 'rating_count']].to_dict(orient='records')

def recommend_for_user_global(user_id, top_n_movies=3, recs_total=10):
    user_seen = merged[merged['user_id'] == user_id]['title'].unique()
    user_top = merged[(merged['user_id'] == user_id) & (merged['rating'] >= 4)]['title'].head(top_n_movies)

    scores = np.zeros(cosine_sim.shape[0])

    for title in user_top:
        if title in movie_indices:
            idx = movie_indices[title]
            if isinstance(idx, pd.Series):
                idx = idx.iloc[0]
            idx = int(idx)
            similarity_scores = np.array(cosine_sim[idx]).flatten()
            scores += similarity_scores

    popularity = np.log1p(movies['rating_count']) * movies['avg_rating']
    scores = scores * popularity

    seen_indices = [movie_indices[title].iloc[0] if isinstance(movie_indices[title], pd.Series) else movie_indices[title] for title in user_seen if title in movie_indices]
    scores[seen_indices] = 0

    top_indices = scores.argsort()[::-1][:recs_total]
    return movies.iloc[top_indices][['title', 'genre', 'avg_rating', 'rating_count']].reset_index(drop=True).to_dict(orient='records')
