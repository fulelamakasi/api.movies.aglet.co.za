import requests

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


def test_get_active_movies(client, headers):
    response = requests.get(
        f"{client}/movies/get-active/v1/0",
        headers=headers
    )

    assert response.status_code == 200

def test_update_movie(client, headers):
    movie_id = 1

    payload = {
        "title": "Updated Movie Title",
        "overview": "Updated overview"
    }

    response = requests.put(
        f"{client}/movies/v1/{movie_id}",
        headers=headers,
        json=payload
    )

    assert response.status_code in [200, 204]