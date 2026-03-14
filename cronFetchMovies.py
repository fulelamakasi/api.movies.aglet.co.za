import requests
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
BASE_URL = os.getenv("BASE_URL")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json;charset=utf-8"
}

def get_movies():

    movies = []

    for page in range(1, 6): 

        url = f"{BASE_URL}?page={page}"

        response = requests.get(url, headers=headers)

        data = response.json()

        movies.extend(data["results"])

    return movies


def save_movies(movies):

    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

    cursor = connection.cursor()
# first check if movie was not previously created by tmdb_id
    sql = """
    INSERT INTO movies
    (tmdb_id,title,overview,release_date,poster_path,backdrop_path,popularity,vote_average,vote_count,language)
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
            movie.get("original_language")
        ))

    connection.commit()

    cursor.close()
    connection.close()


def main():

    movies = get_movies()

    save_movies(movies)

    print(f"{len(movies)} movies synced successfully")


if __name__ == "__main__":
    main()