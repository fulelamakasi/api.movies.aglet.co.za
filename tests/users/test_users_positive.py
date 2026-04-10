import requests

def test_create_user(client, headers):
    payload = {
        "email": "jane@radiorecord.co.za",
        "name": "Joe Soap",
        "password": "12345678",
        "phonenumber": "0717654321"
    }

    response = requests.post(
        f"{client}/users/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 201

def test_get_active_users(client, headers):
    response = requests.get(
        f"{client}/users/get-active/v1/1",
        headers=headers
    )

    assert response.status_code == 200

def test_get_all_users(client, headers):
    response = requests.get(
        f"{client}/users/v1",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_by_id(client, headers):
    user_id = 1

    response = requests.get(
        f"{client}/users/v1/{user_id}",
        headers=headers
    )

    assert response.status_code in [200, 404]

def test_get_active_users(client, headers):
    response = requests.get(
        f"{client}/users/get-active/v1/0",
        headers=headers
    )

    assert response.status_code == 200

def test_update_user(client, headers):
    user_id = 10

    payload = {
        "id": 10,
        "email": "jane@aglet.co.za",
        "name": "Jane Doe",
        "phonenumber": "0827654321",
        "password": "12345678",
        "is_active": 1,
        "is_deleted": 0,
        "token": "10235463-8728-0913-9837-127634524310",
        "created_at": "2020-03-26 19:00:00",
        "updated_at": ""
    }

    response = requests.put(
        f"{client}/users/v1/{user_id}",
        headers=headers,
        json=payload
    )

    assert response.status_code in [200, 204]