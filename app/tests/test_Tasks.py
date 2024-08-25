from fastapi.testclient import TestClient
from app.main import app
from app.utils.LoggerSingleton import logger

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_items():
    response = client.get("/tasks/?page=1&limit=10")
    assert response.status_code == 200
    logger.info(response.json())