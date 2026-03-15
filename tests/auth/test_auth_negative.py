import requests

def test_login_missing_body(client, headers):
    response = requests.post(
        f"{client}/auth/login/v1",
        headers=headers,
        json={}
    )

    assert response.status_code == 400


def test_login_invalid_credentials(client, headers):
    payload = {
        "username": "wrong@aglet.co.za",
        "password": "wrongpass"
    }

    response = requests.post(
        f"{client}/auth/login/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 403

def test_login_missing_header(client):
    payload = {
        "username": "admin@aglet.co.za",
        "password": "password"
    }

    response = requests.post(
        f"{client}/auth/login/v1",
        json=payload
    )

    assert response.status_code in [400, 403]