import requests

def test_create_movie_missing_fields(client, headers):
    response = requests.post(
        f"{client}/movies/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_movie_invalid_id(client, headers):
    response = requests.put(
        f"{client}/movies/v1/99999",
        headers=headers,
        json={"name": "update"}
    )

    assert response.status_code in [204, 404]

def test_create_movie_invalid_date(client, headers):
    payload = {
        "name": "John",
        "release_date": "not-an-email"
    }

    response = requests.post(
        f"{client}/movies/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_create_movie_missing_columns(client, headers):
    response = requests.post(
        f"{client}/movies/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_create_movie_wrong_datatype(client, headers):
    payload = {
        "overview": 123,
        "release_date": True
    }

    response = requests.post(
        f"{client}/movies/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_get_movie_invalid_id(client, headers):
    response = requests.get(
        f"{client}/movies/v1/999999",
        headers=headers
    )

    assert response.status_code in [404, 204]

def test_get_movie_bad_id_type(client, headers):
    response = requests.get(
        f"{client}/movies/v1/abc",
        headers=headers
    )

    assert response.status_code in [400, 422]

def test_update_movie_missing_body(client, headers):
    response = requests.put(
        f"{client}/movies/v1/1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_movie_no_auth_header(client):
    response = requests.put(
        f"{client}/movies/v1/1",
        json={"title": "Bad Update"}
    )

    assert response.status_code in [400, 403]
