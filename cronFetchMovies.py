import requests
import pymysql
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
BASE_URL = os.getenv("BASE_URL")

MOVIES_PER_PAGE = 20

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json;charset=utf-8"
}
db_config = {
    'host': os.getenv('DB_HOST', "127.0.0.1"),
    'user': os.getenv('DB_USER', "aglet_user"),
    'password': os.getenv('DB_PASS', "12345678"),
    'database': os.getenv('DB_NAME', "aglet_movies")
}

def get_db_connection():
    try:
        conn = pymysql.connect(**db_config)
        if not conn:
            return False
        return conn
    except pymysql.MySQLError as err:
        print(f"Error connecting to the database: {err}")

def get_movies(limit=100):
    movies = []
    total_pages = (limit + MOVIES_PER_PAGE - 1)

    for page in range(1, total_pages + 1):
        url = f"{BASE_URL}?page={page}"
        response = requests.get(url, headers=headers)
        data = response.json()
        movies.extend(data["results"])

        if len(movies) >= limit:
            break

    return movies[:limit]


def save_movies(movies):
    connection = get_db_connection()

    cursor = connection.cursor()
    sql = """
    INSERT INTO movies
    (tmdb_id,title,overview,release_date,poster_path,backdrop_path,popularity,vote_average,vote_count,language_id)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
    title=VALUES(title),
    overview=VALUES(overview),
    popularity=VALUES(popularity),
    vote_average=VALUES(vote_average),
    vote_count=VALUES(vote_count)
    """

    for movie in movies:

        cursor.execute(sql, (
            movie["id"],
            movie["title"],
            movie["overview"],
            movie.get("release_date"),
            movie.get("poster_path"),
            movie.get("backdrop_path"),
            movie.get("popularity"),
            movie.get("vote_average"),
            movie.get("vote_count"),
            get_language_id(movie.get("original_language"))
        ))

    connection.commit()

    cursor.close()
    connection.close()

def get_language_id(name):
    connection = get_db_connection()

    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM languages WHERE name = %s LIMIT 1', (name,))
    language = cursor.fetchone()

    cursor.close()
    connection.close()

    if language:
        return language['id']
    else:
        return 1
def main():
    parser = argparse.ArgumentParser(description="Fetch and sync movies from TMDB")
    parser.add_argument("--limit", type=int, default=100, help="Number of movies to fetch (default: 100)")
    args = parser.parse_args()

    movies = get_movies(limit=args.limit)

    save_movies(movies)

    print(f"{len(movies)} movies synced successfully")


if __name__ == "__main__":
    main()
