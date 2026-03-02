from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_validate_endpoint_success():
    payload = {
        "amount": 5000,
        "email": "user@company.com",
        "user_id": "550e8400-e29b-41d4-a716-446655440000"
    }

    response = client.post("/validate", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["overall_status"] == "success"
    assert data["summary"]["failed"] == 0


def test_validate_endpoint_failure():
    payload = {
        "password": "123",
        "amount": 20000
    }

    response = client.post("/validate", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["overall_status"] == "failure"
    assert data["summary"]["failed"] >= 1
    
def test_invalid_json():
    response = client.post("/validate", data="not json")

    assert response.status_code == 400