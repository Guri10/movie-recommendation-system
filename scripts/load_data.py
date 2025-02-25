import pandas as pd
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
cur = conn.cursor()







# Load Movies Data
print("📥 Loading movies data...")
movies = pd.read_csv("../data/ml-100k/u.item", sep="|", encoding="latin-1", usecols=[0, 1, 2], names=["movie_id", "title", "genre"])
print("Movies DataFrame Columns:", movies.columns)
for _, row in movies.iterrows():
    cur.execute("INSERT INTO movies (movie_id, title, genre) VALUES (%s, %s, %s)", (row.movie_id, row.title, row.genre))

# Load Users Data
print("📥 Loading users data...")
users = pd.read_csv("../data/ml-100k/u.user", sep="|", names=["user_id", "age", "gender", "occupation", "zip_code"])
print("Users DataFrame Columns:", users.columns)
for _, row in users.iterrows():
    cur.execute("INSERT INTO users (user_id, age, gender, occupation, zip_code) VALUES (%s, %s, %s, %s, %s)", (row.user_id, row.age, row.gender, row.occupation, row.zip_code))

# Load Ratings Data
print("📥 Loading ratings data...")
ratings = pd.read_csv("../data/ml-100k/u.data", sep="\t", names=["user_id", "movie_id", "rating", "timestamp"])
print("Ratings DataFrame Columns:", ratings.columns)
for _, row in ratings.iterrows():
    cur.execute(
        "INSERT INTO ratings (user_id, movie_id, rating, timestamp) VALUES (%s, %s, %s, to_timestamp(%s))",
        (int(row["user_id"]), int(row["movie_id"]), int(row["rating"]), int(row["timestamp"]))
    )



# Commit changes and close connection
conn.commit()
cur.close()
conn.close()

print("✅ Data successfully loaded into PostgreSQL!")
