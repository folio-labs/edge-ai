from fastapi.testclient import TestClient

from edge_ai.main import app

client = TestClient(app)

def test_base_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()['name'] == "folio-edge-ai"