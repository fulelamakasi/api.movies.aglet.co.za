import requests


def test_create_contact(client, headers):

    payload = {
        "name": "John Doe",
        "email": "john@test.com",
        "message": "Testing contact endpoint",
        "phone_number": "0797666321",
        "company_name": "Swift Operators"
    }

    response = requests.post(
        f"{client}/contact_us/v1",
        headers=headers,
        json=payload
    )

    assert response.status_code == 200