import requests


def test_get_active_role_permissions(client, headers):
    response = requests.get(
        f"{client}/role_permissions/get-active/v1/1",
        headers=headers
    )

    assert response.status_code == 200