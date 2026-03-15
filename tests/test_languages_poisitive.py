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