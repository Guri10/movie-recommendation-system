import pandas as pd
import psycopg2
import sys
import os

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )

# MovieLens 100K genre labels
genre_cols = [
    "unknown", "Action", "Adventure", "Animation", "Children", "Comedy", "Crime",
    "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery",
    "Romance", "Sci-Fi", "Thriller", "War", "Western"
]

# Load movies data
def load_movies():
    conn = connect_db()
    cur = conn.cursor()
    
    movies = pd.read_csv(
        "/Users/atharvagurav/Documents/movie-recommendation-system/data/ml-100k/u.item", sep="|", encoding="latin-1", header=None,
        usecols=[0, 1] + list(range(5, 24)), names=["movie_id", "title"] + genre_cols
    )
    
    # Convert genre flags to a single string
    movies["genre"] = movies[genre_cols].apply(lambda x: ", ".join(x.index[x == 1]), axis=1)
    movies = movies[["movie_id", "title", "genre"]]
    
    for _, row in movies.iterrows():
        cur.execute(
            "INSERT INTO movies (movie_id, title, genre) VALUES (%s, %s, %s) ON CONFLICT (movie_id) DO NOTHING",
            (row.movie_id, row.title, row.genre)
        )
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Movies data loaded successfully!")

# Load users data
def load_users():
    conn = connect_db()
    cur = conn.cursor()
    
    users = pd.read_csv("/Users/atharvagurav/Documents/movie-recommendation-system/data/ml-100k/u.user", sep="|", encoding="latin-1", header=None,
                         names=["user_id", "age", "gender", "occupation", "zip_code"])
    
    for _, row in users.iterrows():
        cur.execute(
            "INSERT INTO users (user_id, age, gender, occupation, zip_code) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO NOTHING",
            (row.user_id, row.age, row.gender, row.occupation, row.zip_code)
        )
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Users data loaded successfully!")

# Load ratings data
def load_ratings():
    conn = connect_db()
    cur = conn.cursor()
    
    ratings = pd.read_csv("/Users/atharvagurav/Documents/movie-recommendation-system/data/ml-100k/u.data", sep="\t", encoding="latin-1", header=None,
                          names=["user_id", "movie_id", "rating", "timestamp"])
    
    for _, row in ratings.iterrows():
        cur.execute(
            "INSERT INTO ratings (user_id, movie_id, rating, timestamp) VALUES (%s, %s, %s, to_timestamp(%s)) ON CONFLICT DO NOTHING",
            (int(row.user_id), int(row.movie_id), int(row.rating), int(row.timestamp))
        )

    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Ratings data loaded successfully!")

# Run all data loads
if __name__ == "__main__":
    load_movies()
    load_users()
    load_ratings()
    print("🎉 All data successfully loaded into PostgreSQL!")