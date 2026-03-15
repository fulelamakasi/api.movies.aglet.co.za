import requests

def test_create_user_role(client, headers):
    payload = {
        "role_id": 1,
        "user_id": 1
    }

    response = requests.post(
        f"{client}/user_roles/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 200

def test_get_active_user_roles(client, headers):
    response = requests.get(
        f"{client}/user_roles/get-active/v1/1",
        headers=headers
    )

    assert response.status_code == 200

def test_get_all_user_roles(client, headers):
    response = requests.get(
        f"{client}/user_roles/v1",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_role_by_id(client, headers):
    user_role_id = 1

    response = requests.get(
        f"{client}/user_roles/v1/{user_role_id}",
        headers=headers
    )

    assert response.status_code in [200, 404]

def test_get_inactive_user_roles(client, headers):
    response = requests.get(
        f"{client}/user_roles/get-active/v1/0",
        headers=headers
    )

    assert response.status_code == 200

def test_update_user_role(client, headers):
    user_role_id = 3

    payload = {
        "id": 3,
        "role_id": 2,
        "user_id": 1,
        "is_active": 1,
        "is_deleted": 0,
        "created_at": "2020-03-26 19:00:00",
        "updated_at": ""
    }

    response = requests.put(
        f"{client}/user_roles/v1/{user_role_id}",
        headers=headers,
        json=payload
    )

    assert response.status_code in [200, 204]