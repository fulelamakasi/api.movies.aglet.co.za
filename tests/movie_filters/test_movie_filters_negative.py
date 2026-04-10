import requests

def test_create_movie_favourite_missing_fields(client, headers):
    response = requests.post(
        f"{client}/movie_favourites/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_movie_favourite_invalid_id(client, headers):
    response = requests.put(
        f"{client}/movie_favourites/v1/99999",
        headers=headers,
        json={"name": "update"}
    )

    assert response.status_code in [200, 204, 400, 404]

def test_create_movie_favourite_invalid_movie_id(client, headers):
    payload = {
        "movie_id": "John",
        "user_id": 16
    }

    response = requests.post(
        f"{client}/movie_favourites/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_create_movie_favourite_invalid_user_id(client, headers):
    payload = {
        "movie_id": 95,
        "user_id": "not-an-email"
    }

    response = requests.post(
        f"{client}/movie_favourites/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_create_movie_favourite_missing_columns(client, headers):
    response = requests.post(
        f"{client}/movie_favourites/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_create_movie_favourite_wrong_datatype(client, headers):
    payload = {
        "movie_id": True,
        "user_id": False
    }

    response = requests.post(
        f"{client}/movie_favourites/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_get_movie_favourite_invalid_id(client, headers):
    response = requests.get(
        f"{client}/movie_favourites/v1/999999",
        headers=headers
    )

    assert response.status_code in [404, 204]

def test_get_movie_favourite_bad_id_type(client, headers):
    response = requests.get(
        f"{client}/movie_favourites/v1/abc",
        headers=headers
    )

    assert response.status_code in [400, 404, 422]

def test_update_movie_favourite_missing_body(client, headers):
    response = requests.put(
        f"{client}/movie_favourites/v1/1",
        headers=headers,
        json={}
    )

    assert response.status_code == 400

def test_update_movie_favourite_no_auth_header(client):
    response = requests.put(
        f"{client}/movie_favourites/v1/1",
        json={"movie_id": 95, "user_id": 16}
    )

    assert response.status_code in [400, 403]
