import requests

def test_create_contact_missing_fields(client, headers):
    response = requests.post(
        f"{client}/contact_us/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_contact_invalid_id(client, headers):
    response = requests.put(
        f"{client}/contact_us/v1/99999",
        headers=headers,
        json={"message": "update"}
    )

    assert response.status_code in [200, 204, 404]

def test_create_contact_invalid_email(client, headers):
    payload = {
        "name": "John",
        "email": "not-an-email",
        "message": "hello"
    }

    response = requests.post(
        f"{client}/contact_us/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 400

def test_create_contact_missing_name(client, headers):
    response = requests.post(
        f"{client}/contact_us/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_create_contact_wrong_datatype(client, headers):
    payload = {
        "name": 123,
        "message": True
    }

    response = requests.post(
        f"{client}/contact_us/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 400

def test_get_contact_invalid_id(client, headers):
    response = requests.get(
        f"{client}/contact_us/v1/999999",
        headers=headers
    )

    assert response.status_code in [404, 204]

def test_get_contact_bad_id_type(client, headers):
    response = requests.get(
        f"{client}/contact_us/v1/abc",
        headers=headers
    )

    assert response.status_code in [400, 404, 422]

def test_update_contact_missing_body(client, headers):
    response = requests.put(
        f"{client}/contact_us/v1/1",
        headers=headers,
        json={}
    )

    assert response.status_code in [200, 400, 422]

def test_update_contact_no_auth_header(client):
    response = requests.put(
        f"{client}/contact_us/v1/1",
        json={"title": "Bad Update"}
    )

    assert response.status_code in [400, 403]
