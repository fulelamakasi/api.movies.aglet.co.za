import requests

def test_create_role_permission(client, headers):
    payload = {
        "role_id": 1,
        "permission_id": 1
    }

    response = requests.post(
        f"{client}/role_permissions/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 201

def test_get_active_role_permissions(client, headers):
    response = requests.get(
        f"{client}/role_permissions/get-active/v1/1",
        headers=headers
    )

    assert response.status_code == 200

def test_get_all_role_permissions(client, headers):
    response = requests.get(
        f"{client}/role_permissions/v1",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_role_permission_by_id(client, headers):
    role_permission_id = 1

    response = requests.get(
        f"{client}/role_permissions/v1/{role_permission_id}",
        headers=headers
    )

    assert response.status_code in [200, 404]

def test_get_inactive_role_permissions(client, headers):
    response = requests.get(
        f"{client}/role_permissions/get-active/v1/0",
        headers=headers
    )

    assert response.status_code == 200

def test_update_role_permission(client, headers):
    role_permission_id = 2

    payload = {
        "id": 2,
        "role_id": 10,
        "permission_id": 16,
        "is_active": 1,
        "is_deleted": 0,
        "created_at": "2020-03-26 19:00:00",
        "updated_at": ""
    }

    response = requests.put(
        f"{client}/role_permissions/v1/{role_permission_id}",
        headers=headers,
        json=payload
    )

    assert response.status_code in [200, 204]