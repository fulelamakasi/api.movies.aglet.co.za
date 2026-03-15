import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api"

@pytest.fixture
def headers():
    return {
        "User-Id": "79f04878-a79d-4ea9-ba40-8ee21abab16c",
        "Content-Type": "application/json"
    }

@pytest.fixture
def client():
    return BASE_URL