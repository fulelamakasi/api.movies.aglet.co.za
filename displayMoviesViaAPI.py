import requests
import os
import argparse
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

BASE_URL = os.getenv("BASE_URL")

MOVIES_PER_PAGE = 20

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json;charset=utf-8"
}

def get_movies(limit=100):
    movies = []
    current_page = 1
    
    while len(movies) < limit:
        url = f"{BASE_URL}?page={current_page}"
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Check if response has results
        if not data.get("results"):
            break
            
        movies.extend(data["results"])
        current_page += 1
        
        # Stop if no more pages
        if current_page > data.get("total_pages", 0):
            break
    
    return movies[:limit]

def main():
    parser = argparse.ArgumentParser(description="Fetch and sync movies from TMDB")
    parser.add_argument("--limit", type=int, default=100, help="Number of movies to fetch (default: 100)")
    args = parser.parse_args()

    movies = get_movies(limit=args.limit)
    print(f"{len(movies)} movies synced successfully")

    for movie in movies:
        print(json.dumps(movie))


if __name__ == "__main__":
    main()