import requests

def test_create_user_missing_fields(client, headers):
    response = requests.post(
        f"{client}/users/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_user_invalid_id(client, headers):
    response = requests.put(
        f"{client}/users/v1/99999",
        headers=headers,
        json={"message": "update"}
    )

    assert response.status_code in [204, 404]

def test_create_user_invalid_is_active(client, headers):
    payload = {
        "name": "John",
        "email": "not-an-email",
        "is_active": "hello"
    }

    response = requests.post(
        f"{client}/users/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_create_user_missing_name(client, headers):
    response = requests.post(
        f"{client}/users/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_create_user_wrong_datatype(client, headers):
    payload = {
        "name": 123,
        "email": True
    }

    response = requests.post(
        f"{client}/users/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_get_user_invalid_id(client, headers):
    response = requests.get(
        f"{client}/users/v1/999999",
        headers=headers
    )

    assert response.status_code in [404, 204]

def test_get_user_bad_id_type(client, headers):
    response = requests.get(
        f"{client}/users/v1/abc",
        headers=headers
    )

    assert response.status_code in [400, 422]

def test_update_user_missing_body(client, headers):
    response = requests.put(
        f"{client}/users/v1/1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_user_no_auth_header(client):
    response = requests.put(
        f"{client}/users/v1/1",
        json={"phonenumber": "Bad Update", "token": ""}
    )

    assert response.status_code in [400, 403]
