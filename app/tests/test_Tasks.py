from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_item():
    response = client.post(
        "/tasks/",
        json={"name": "Foo", "price": 45.2},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Foo",
        "price": 45.2,
        "id": 1,
    }