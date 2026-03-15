import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api"

@pytest.fixture
def headers():
    return {
        "User-Id": "10235463-8728-0913-9837-127634524310",
        "Content-Type": "application/json"
    }

@pytest.fixture
def client():
    return BASE_URL