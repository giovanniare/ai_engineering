"""Valida que el servicio FastAPI arranque y sus endpoints respondan.

No llama a ningun LLM real: el servicio de estimacion se sustituye por un
stub para que el pipeline de CI no dependa de API keys ni consuma creditos.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.routers import estimations


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_docs_available():
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200


def test_estimate_endpoint(monkeypatch):
    def fake_generate_estimation(transcription: str):
        return "## Estimacion falsa\nTotal: 10 horas", "gpt-4o-mini", "openai"

    monkeypatch.setattr(estimations, "generate_estimation", fake_generate_estimation)

    client = TestClient(app)
    response = client.post(
        "/api/v1/estimate",
        json={"transcription": "Necesitamos una app movil de pedidos."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "openai"
    assert body["model"] == "gpt-4o-mini"
    assert "Estimacion" in body["estimation"]


def test_estimate_endpoint_rejects_empty_transcription():
    client = TestClient(app)
    response = client.post("/api/v1/estimate", json={"transcription": ""})
    assert response.status_code == 422
