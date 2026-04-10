import requests

def test_create_movie_filter(client, headers):
    payload = {
        "movie_id": 1,
        "user_id": 1
    }

    response = requests.post(
        f"{client}/movie_favourites/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 201

def test_get_active_movie_filters(client, headers):
    response = requests.get(
        f"{client}/movie_favourites/get-active/v1/1",
        headers=headers
    )

    assert response.status_code == 200

def test_get_all_movie_filters(client, headers):
    response = requests.get(
        f"{client}/movie_favourites/v1",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movie_filter_by_id(client, headers):
    movie_id = 1

    response = requests.get(
        f"{client}/movie_favourites/v1/{movie_id}",
        headers=headers
    )

    assert response.status_code in [200, 404]

def test_get_movie_filter_by_movie(client, headers):
    movie_id = 1

    response = requests.get(
        f"{client}/movie_favourites/get-by-movie/v1/{movie_id}",
        headers=headers
    )

    assert response.status_code in [200, 404]

def test_get_movie_filter_by_user(client, headers):
    user_id = 1

    response = requests.get(
        f"{client}/movie_favourites/get-by-user/v1/{user_id}",
        headers=headers
    )

    assert response.status_code in [200, 404]

def test_get_inactive_movie_filters(client, headers):
    response = requests.get(
        f"{client}/movie_favourites/get-active/v1/0",
        headers=headers
    )

    assert response.status_code == 200

def test_update_movie_filter(client, headers):
    movie_favourite_id = 2

    payload = {
        "id": 2,
        "movie_id": 1,
        "user_id": 1,
        "is_active": 0,
        "is_deleted": 1,
        "created_at": "2026-03-26 19:00:00",
        "updated_at": ""
    }

    response = requests.put(
        f"{client}/movie_favourites/v1/{movie_favourite_id}",
        headers=headers,
        json=payload
    )

    assert response.status_code in [200, 204]