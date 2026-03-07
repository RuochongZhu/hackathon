from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_summary_endpoint() -> None:
    response = client.get("/dashboard/summary", params={"preset": "baseline"})
    assert response.status_code == 200
    body = response.json()
    assert body["preset"] == "baseline"
    assert "avg_risk" in body


def test_database_health_endpoint_reports_status() -> None:
    response = client.get("/database/health")
    assert response.status_code == 200
    body = response.json()
    assert "configured" in body
    assert "valid" in body


def test_high_risk_endpoint() -> None:
    response = client.get("/patients/high-risk", params={"preset": "baseline", "limit": 5})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 5
    assert len(body["patients"]) == 5


def test_patient_profile_endpoint() -> None:
    top_patient = client.get("/patients/high-risk", params={"preset": "baseline", "limit": 1}).json()["patients"][0]["patient_id"]
    response = client.get(f"/patients/{top_patient}/profile", params={"preset": "baseline"})
    assert response.status_code == 200
    body = response.json()
    assert body["patient_id"] == top_patient
    assert "key_drivers" in body


def test_llm_integration_status_endpoint() -> None:
    response = client.get("/integrations/llm")
    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "openai"
    assert "configured" in body
    assert "message" in body


def test_system_audit_endpoint() -> None:
    response = client.get("/audit/system", params={"preset": "baseline"})
    assert response.status_code == 200
    body = response.json()
    assert body["preset"] == "baseline"
    assert "checks" in body
    assert len(body["checks"]) >= 1
