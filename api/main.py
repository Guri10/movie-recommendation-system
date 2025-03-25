# api/main.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from api.recommender import recommend_by_title, recommend_for_user_global

app = FastAPI(title="Movie Recommendation API")

# Optional: Allow frontend or external tools to access your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "🎬 Welcome to the Movie Recommendation API"}

@app.get("/recommend/movie")
def get_movie_recommendations(title: str = Query(..., description="Exact movie title to base recommendations on")):
    results = recommend_by_title(title)
    return {"input_title": title, "recommendations": results}

@app.get("/recommend/user")
def get_user_recommendations(user_id: int = Query(..., description="User ID to generate personalized recommendations for")):
    results = recommend_for_user_global(user_id)
    return {"user_id": user_id, "recommendations": results}
