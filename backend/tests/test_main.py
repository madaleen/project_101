from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_app_imports():
    assert app is not None

def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code in (200, 307)