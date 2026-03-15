import requests

def test_get_active_permissions_invalid_flag(client, headers):
    response = requests.get(
        f"{client}/permissions/get-active/v1/abc",
        headers=headers
    )

    assert response.status_code in [400, 422]