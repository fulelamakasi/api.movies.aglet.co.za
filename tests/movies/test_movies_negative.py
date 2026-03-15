import requests

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