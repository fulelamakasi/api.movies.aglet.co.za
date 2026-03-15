import requests

def test_login_success(client, headers):
    payload = {
        "username": "admin@aglet.co.za",
        "password": "12345678"
    }

    response = requests.post(
        f"{client}/auth/login/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 200
    assert "token" in response.json()


def test_login_missing_fields(client, headers):
    payload = {}

    response = requests.post(
        f"{client}/auth/login/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 400