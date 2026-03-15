import requests

def test_create_language_missing_name(client, headers):
    response = requests.post(
        f"{client}/languages/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]


def test_create_language_wrong_datatype(client, headers):
    payload = {
        "name": 123,
        "code": True
    }

    response = requests.post(
        f"{client}/languages/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code in [400, 422]