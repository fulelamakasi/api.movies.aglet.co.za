import requests

def test_create_movie(client, headers):
    payload = {
        "tmdb_id": "1",
        "title": "The Boondock Saints",
        "overview": "The Boondock Saints is a 1999 vigilante action thriller film written and directed by Troy Duffy in his feature directorial debut.",
        "release_date": "04 August 1999",
        "poster_path": "random string blob text",
        "backdrop_path": "random string blob text",
        "popularity": "100%",
        "vote_average": "70%",
        "vote_count": "70%",
        "language_id": "1"
    }

    response = requests.post(
        f"{client}/movies/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 200

def test_get_active_movies(client, headers):
    response = requests.get(
        f"{client}/movies/get-active/v1/1",
        headers=headers
    )

    assert response.status_code == 200

def test_get_all_movies(client, headers):
    response = requests.get(
        f"{client}/movies/v1",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movie_by_id(client, headers):
    movie_id = 1

    response = requests.get(
        f"{client}/movies/v1/{movie_id}",
        headers=headers
    )

    assert response.status_code in [200, 404]

def test_get_inactive_movies(client, headers):
    response = requests.get(
        f"{client}/movies/get-active/v1/0",
        headers=headers
    )

    assert response.status_code == 200

def test_update_movie(client, headers):
    movie_id = 2

    payload = {
        "id": 2,
        "tmdb_id": "1",
        "title": "The Boondock Saints",
        "overview": "The Boondock Saints is a 1999 vigilante action thriller film written and directed by Troy Duffy in his feature directorial debut.",
        "release_date": "04 August 1999",
        "poster_path": "random string blob text",
        "backdrop_path": "random string blob text",
        "popularity": "100%",
        "vote_average": "70%",
        "vote_count": "70%",
        "language_id": "1",
        "is_deleted": 0,
        "created_at": "2026-03-15 19:00:00",
        "updated_at": ""
    }

    response = requests.put(
        f"{client}/movies/v1/{movie_id}",
        headers=headers,
        json=payload
    )

    assert response.status_code in [200, 204]