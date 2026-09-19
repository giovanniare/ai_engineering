"""Verifica que el servicio FastAPI funcione end-to-end (con el LLM mockeado)."""

from fastapi.testclient import TestClient

from app.main import app
from app.routers import estimations
from app.services.llm_service import EstimationResult

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200


def test_estimate_endpoint_returns_estimation(monkeypatch):
    fake_result = EstimationResult(
        estimation="## Estimacion de prueba\n\n**Total estimado: 100 horas**",
        model="claude-haiku-4-5",
        provider="anthropic",
    )

    monkeypatch.setattr(estimations, "generate_estimation", lambda transcription: fake_result)

    response = client.post(
        "/api/v1/estimate",
        json={"transcription": "El cliente necesita una app de reservas de citas."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["estimation"] == fake_result.estimation
    assert body["model"] == "claude-haiku-4-5"
    assert body["provider"] == "anthropic"


def test_estimate_endpoint_requires_transcription():
    response = client.post("/api/v1/estimate", json={})
    assert response.status_code == 422


def test_estimate_endpoint_handles_llm_errors(monkeypatch):
    def _raise(transcription):
        raise RuntimeError("simulated LLM failure")

    monkeypatch.setattr(estimations, "generate_estimation", _raise)

    response = client.post("/api/v1/estimate", json={"transcription": "algo"})
    assert response.status_code == 502
