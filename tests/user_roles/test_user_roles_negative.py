import requests

def test_create_user_role_missing_fields(client, headers):
    response = requests.post(
        f"{client}/user_roles/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_user_role_invalid_id(client, headers):
    response = requests.put(
        f"{client}/user_roles/v1/99999",
        headers=headers,
        json={"user_id": "update"}
    )

    assert response.status_code in [204, 404]

def test_create_user_role_invalid_role(client, headers):
    payload = {
        "user_id": 1,
        "role_id": ""
    }

    response = requests.post(
        f"{client}/user_roles/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_create_user_role_missing_columns(client, headers):
    response = requests.post(
        f"{client}/user_roles/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_create_user_role_wrong_datatype(client, headers):
    payload = {
        "user_id": False,
        "role_id": True
    }

    response = requests.post(
        f"{client}/user_roles/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]

def test_get_user_role_invalid_id(client, headers):
    response = requests.get(
        f"{client}/user_roles/v1/999999",
        headers=headers
    )

    assert response.status_code in [404, 204]

def test_get_user_role_bad_id_type(client, headers):
    response = requests.get(
        f"{client}/user_roles/v1/abc",
        headers=headers
    )

    assert response.status_code in [400, 422]

def test_update_user_role_missing_body(client, headers):
    response = requests.put(
        f"{client}/user_roles/v1/1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]

def test_update_user_role_no_auth_header(client):
    response = requests.put(
        f"{client}/user_roles/v1/1",
        json={"is_active": "Bad Update"}
    )

    assert response.status_code in [400, 403]
