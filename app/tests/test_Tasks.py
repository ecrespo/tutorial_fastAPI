from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task():
    response = client.post(
        "/tasks/",
        json={"task_content": "Test Task", "is_complete": False}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Task has been saved"
    }
