import requests

def test_create_role_missing_fields(client, headers):
    response = requests.post(
        f"{client}/roles/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_role_invalid_id(client, headers):
    response = requests.put(
        f"{client}/roles/v1/99999",
        headers=headers,
        json={"name": "update"}
    )

    assert response.status_code in [204, 404]

def test_create_role_invalid_date(client, headers):
    payload = {
        "name": "ADMIN",
        "description": ""
    }

    response = requests.post(
        f"{client}/roles/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_create_role_missing_columns(client, headers):
    response = requests.post(
        f"{client}/roles/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_create_role_wrong_datatype(client, headers):
    payload = {
        "name": 123,
        "description": True
    }

    response = requests.post(
        f"{client}/roles/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_get_role_invalid_id(client, headers):
    response = requests.get(
        f"{client}/roles/v1/999999",
        headers=headers
    )

    assert response.status_code in [404, 204]

def test_get_role_bad_id_type(client, headers):
    response = requests.get(
        f"{client}/roles/v1/abc",
        headers=headers
    )

    assert response.status_code in [400, 422]

def test_update_role_missing_body(client, headers):
    response = requests.put(
        f"{client}/roles/v1/1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_role_no_auth_header(client):
    response = requests.put(
        f"{client}/roles/v1/1",
        json={"is_active": "Bad Update"}
    )

    assert response.status_code in [400, 403]
