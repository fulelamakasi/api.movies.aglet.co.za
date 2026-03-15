import requests

def test_create_permission(client, headers):
    payload = {
        "name": "Admin",
        "description": "What the permission is about"
    }

    response = requests.post(
        f"{client}/permissions/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 200

def test_get_active_permissions(client, headers):
    response = requests.get(
        f"{client}/permissions/get-active/v1/1",
        headers=headers
    )

    assert response.status_code == 200

def test_get_all_permissions(client, headers):
    response = requests.get(
        f"{client}/permissions/v1",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_permission_by_id(client, headers):
    permission_id = 1

    response = requests.get(
        f"{client}/permissions/v1/{permission_id}",
        headers=headers
    )

    assert response.status_code in [200, 404]

def test_get_inactive_permissions(client, headers):
    response = requests.get(
        f"{client}/permissions/get-active/v1/0",
        headers=headers
    )

    assert response.status_code == 200

def test_update_permission(client, headers):
    permission_id = 3

    payload = {
        "id": 3,
        "name": "Admin",
        "description": "What the permission is about",
        "is_active": 1,
        "is_deleted": 0,
        "created_at": "2020-03-26 19:00:00",
        "updated_at": ""
    }

    response = requests.put(
        f"{client}/permissions/v1/{permission_id}",
        headers=headers,
        json=payload
    )

    assert response.status_code in [200, 204]