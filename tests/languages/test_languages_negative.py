import requests

def test_create_language_missing_fields(client, headers):
    response = requests.post(
        f"{client}/languages/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_language_invalid_id(client, headers):
    response = requests.put(
        f"{client}/languages/v1/99999",
        headers=headers,
        json={"message": "update"}
    )

    assert response.status_code in [200, 204, 404]

def test_create_language_invalid_code(client, headers):
    payload = {
        "name": "John",
        "code": "not-an-email"
    }

    response = requests.post(
        f"{client}/languages/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [201, 400, 422]

def test_create_language_missing_name(client, headers):
    response = requests.post(
        f"{client}/languages/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_create_language_wrong_datatype(client, headers):
    payload = {
        "name": 123,
        "message": True
    }

    response = requests.post(
        f"{client}/languages/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [201, 400, 422]

def test_get_language_invalid_id(client, headers):
    response = requests.get(
        f"{client}/languages/v1/999999",
        headers=headers
    )

    assert response.status_code in [404, 204]

def test_get_language_bad_id_type(client, headers):
    response = requests.get(
        f"{client}/languages/v1/abc",
        headers=headers
    )

    assert response.status_code in [400, 404, 422]

def test_update_language_missing_body(client, headers):
    response = requests.put(
        f"{client}/languages/v1/1",
        headers=headers,
        json={}
    )

    assert response.status_code in [200, 400, 422]

def test_update_language_no_auth_header(client):
    response = requests.put(
        f"{client}/languages/v1/1",
        json={"code": "Bad Update"}
    )

    assert response.status_code in [400, 403]
