import requests

def test_create_language(client, headers):
    payload = {
        "name": "English",
        "description": "The oldest language"
    }

    response = requests.post(
        f"{client}/languages/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 200

def test_get_active_languages(client, headers):
    response = requests.get(
        f"{client}/language/get-active/v1/1",
        headers=headers
    )

    assert response.status_code == 200

def test_get_all_languages(client, headers):
    response = requests.get(
        f"{client}/languages/v1",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_language_by_id(client, headers):
    language_id = 1

    response = requests.get(
        f"{client}/languages/v1/{language_id}",
        headers=headers
    )

    assert response.status_code in [200, 404]

def test_get_inactive_languages(client, headers):
    response = requests.get(
        f"{client}/language/get-active/v1/0",
        headers=headers
    )

    assert response.status_code == 200

def test_update_language(client, headers):
    language_id = 2

    payload = {
        "id": 2,
        "name": "English",
        "description": "The oldest language",
        "is_active": 1,
        "is_deleted": 0,
        "created_at": "2026-03-15 19:00:00",
        "updated_at": ""
    }

    response = requests.put(
        f"{client}/languages/v1/{language_id}",
        headers=headers,
        json=payload
    )

    assert response.status_code in [200, 204]