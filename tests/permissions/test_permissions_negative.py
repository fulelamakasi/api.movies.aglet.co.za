import requests

def test_create_permission_missing_fields(client, headers):
    response = requests.post(
        f"{client}/permissions/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_permission_invalid_id(client, headers):
    response = requests.put(
        f"{client}/permissions/v1/99999",
        headers=headers,
        json={"name": "update"}
    )

    assert response.status_code in [204, 404]

def test_create_permission_invalid_date(client, headers):
    payload = {
        "name": "CREATE MOVIES",
        "description": ""
    }

    response = requests.post(
        f"{client}/permissions/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_create_permission_missing_columns(client, headers):
    response = requests.post(
        f"{client}/permissions/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_create_permission_wrong_datatype(client, headers):
    payload = {
        "name": 123,
        "description": True
    }

    response = requests.post(
        f"{client}/permissions/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_get_permission_invalid_id(client, headers):
    response = requests.get(
        f"{client}/permissions/v1/999999",
        headers=headers
    )

    assert response.status_code in [404, 204]

def test_get_permission_bad_id_type(client, headers):
    response = requests.get(
        f"{client}/permissions/v1/abc",
        headers=headers
    )

    assert response.status_code in [400, 422]

def test_update_permission_missing_body(client, headers):
    response = requests.put(
        f"{client}/permissions/v1/1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_permission_no_auth_header(client):
    response = requests.put(
        f"{client}/permissions/v1/1",
        json={"is_active": "Bad Update"}
    )

    assert response.status_code in [400, 403]
