import requests

def test_create_role(client, headers):
    payload = {
        "name": "Admin",
        "description": "What the role is about"
    }

    response = requests.post(
        f"{client}/roles/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 200

def test_get_active_roles(client, headers):
    response = requests.get(
        f"{client}/roles/get-active/v1/1",
        headers=headers
    )

    assert response.status_code == 200

def test_get_all_roles(client, headers):
    response = requests.get(
        f"{client}/roles/v1",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_role_by_id(client, headers):
    role_id = 1

    response = requests.get(
        f"{client}/roles/v1/{role_id}",
        headers=headers
    )

    assert response.status_code in [200, 404]

def test_get_inactive_roles(client, headers):
    response = requests.get(
        f"{client}/roles/get-active/v1/0",
        headers=headers
    )

    assert response.status_code == 200

def test_update_role(client, headers):
    role_id = 1

    payload = {
        "id": 1,
        "name": "WHO",
        "description": "What the role is about",
        "is_active": 1,
        "is_deleted": 0,
        "created_at": "2020-03-26 19:00:00",
        "updated_at": ""
    }

    response = requests.put(
        f"{client}/roles/v1/{role_id}",
        headers=headers,
        json=payload
    )

    assert response.status_code in [200, 204]