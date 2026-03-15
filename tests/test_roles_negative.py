import requests

def test_create_role_empty_payload(client, headers):
    response = requests.post(
        f"{client}/roles/v1",
        headers=headers,
        json={}
    )

    assert response.status_code in [400, 422]