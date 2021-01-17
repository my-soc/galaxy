from fastapi.testclient import TestClient

from server import app

client = TestClient(app)


def test_get_entries():
    response = client.get("/api/generator/objects")
    assert response.status_code == 200
