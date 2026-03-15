import requests

def test_create_contact_missing_fields(client, headers):
    response = requests.post(
        f"{client}/contact_us/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]


def test_update_contact_invalid_id(client, headers):
    response = requests.put(
        f"{client}/contact_us/v1/99999",
        headers=headers,
        json={"message": "update"}
    )

    assert response.status_code in [204, 404]


def test_create_contact_invalid_email(client, headers):
    payload = {
        "name": "John",
        "email": "not-an-email",
        "message": "hello"
    }

    response = requests.post(
        f"{client}/contact_us/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]