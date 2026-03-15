import requests

def test_get_active_user_roles(client, headers):
    response = requests.get(
        f"{client}/user_roles/get-active/v1/1",
        headers=headers
    )

    assert response.status_code == 200