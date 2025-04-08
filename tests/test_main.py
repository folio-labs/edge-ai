from fastapi.testclient import TestClient

from edge_ai.main import app

client = TestClient(app)


def test_base_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "folio-edge-ai"


def test_module_descriptor():
    response = client.get("moduleDescriptor.json")
    assert response.status_code == 200
    assert response.json()["name"] == "folio-edge-ai"
    assert (
        response.json()["provides"][0]["handlers"][0]["pathPattern"]
        == "/inventory/instance/generate"
    )
    assert (
        response.json()["provides"][0]["handlers"][1]["pathPattern"]
        == "/inventory/instance/generate_from_image"
    )


def test_converstation():
    response = client.post("/conversation?prompt=test")
    assert response.status_code == 200
    assert response.json() == {"message": "Not implemented"}
