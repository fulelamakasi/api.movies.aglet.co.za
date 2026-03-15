import requests

def test_create_role(client, headers):
    payload = {
        "name": "Admin",
        "description": "What the role is about"
    }

    response = requests.post(
        f"{client}/roles/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 200