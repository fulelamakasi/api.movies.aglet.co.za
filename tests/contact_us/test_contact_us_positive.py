import requests

def test_create_contact_us(client, headers):
    payload = {
        "name": "John Doe",
        "email": "john@test.com",
        "message": "Testing contact endpoint",
        "phone_number": "0797666321",
        "company_name": "Swift Operators"
    }

    response = requests.post(
        f"{client}/contact_us/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 201

def test_get_non_actioned_contact_us(client, headers):
    response = requests.get(
        f"{client}/languages/get-active/v1/0",
        headers=headers
    )

    assert response.status_code == 200

def test_get_all_contact_us(client, headers):
    response = requests.get(
        f"{client}/contact_us/v1",
        headers=headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_contact_us_by_id(client, headers):
    contact_us_id = 1

    response = requests.get(
        f"{client}/contact_us/v1/{contact_us_id}",
        headers=headers
    )

    assert response.status_code in [200, 404]

def test_get_actioned_contact_us(client, headers):
    response = requests.get(
        f"{client}/languages/get-active/v1/1",
        headers=headers
    )

    assert response.status_code == 200

def test_update_contact_us(client, headers):
    contact_us_id = 2

    payload = {
        "id": 2,
        "name": "John Doe",
        "message": "I am enquiring on an inquiry about the inquiry of inquiries",
        "email": "john@aglet.co.za",
        "phone_number": "0797666321",
        "company_name": "Swift Operators",
        "is_actioned": 0,
        "created_at": "2026-03-15 19:00:00",
        "updated_at": ""
    }

    response = requests.put(
        f"{client}/contact_us/v1/{contact_us_id}",
        headers=headers,
        json=payload
    )

    assert response.status_code in [200, 204]
