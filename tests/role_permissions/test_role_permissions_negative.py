import requests

def test_get_active_role_permissions_invalid_flag(client, headers):
    response = requests.get(
        f"{client}/role_permissions/get-active/v1/abc",
        headers=headers
    )

    assert response.status_code in [400, 404, 422]