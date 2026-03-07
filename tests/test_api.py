from fastapi.testclient import TestClient

import app.services.ai_summary as ai_summary_service
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


def test_ai_patient_summary_endpoint_fallback_without_api_key(monkeypatch) -> None:
    top_patient = client.get("/patients/high-risk", params={"preset": "baseline", "limit": 1}).json()["patients"][0]["patient_id"]
    monkeypatch.setattr(ai_summary_service, "OPENAI_API_KEY", "")

    response = client.post(
        "/ai/patient-summary",
        json={"preset": "baseline", "patient_id": top_patient},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["fallback_used"] is True
    assert body["fallback_reason"] == "openai_api_key_missing"
    assert body["summary"]["risk_summary"]
    assert len(body["summary"]["recommended_actions"]) >= 1


def test_ai_patient_summary_endpoint_openai_success(monkeypatch) -> None:
    top_patient = client.get("/patients/high-risk", params={"preset": "baseline", "limit": 1}).json()["patients"][0]["patient_id"]
    monkeypatch.setattr(ai_summary_service, "OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(ai_summary_service, "OPENAI_MODEL", "gpt-4o-mini")

    class MockResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {
                "output": [
                    {
                        "content": [
                            {
                                "type": "output_text",
                                "text": (
                                    '{"risk_summary":"AI explanation.",'
                                    '"quantitative_signals":["signal 1","signal 2"],'
                                    '"recommended_actions":["action 1","action 2"],'
                                    '"watchouts":["watchout 1"]}'
                                ),
                            }
                        ]
                    }
                ]
            }

    def fake_post(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(ai_summary_service.httpx, "post", fake_post)

    response = client.post(
        "/ai/patient-summary",
        json={"preset": "baseline", "patient_id": top_patient},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["fallback_used"] is False
    assert body["fallback_reason"] is None
    assert body["llm_model"] == "gpt-4o-mini"
    assert body["summary"]["risk_summary"] == "AI explanation."


def test_ai_patient_summary_endpoint_fallback_on_timeout(monkeypatch) -> None:
    top_patient = client.get("/patients/high-risk", params={"preset": "baseline", "limit": 1}).json()["patients"][0]["patient_id"]
    monkeypatch.setattr(ai_summary_service, "OPENAI_API_KEY", "test-key")

    def fake_post(*args, **kwargs):
        raise ai_summary_service.httpx.TimeoutException("timeout")

    monkeypatch.setattr(ai_summary_service.httpx, "post", fake_post)

    response = client.post(
        "/ai/patient-summary",
        json={"preset": "baseline", "patient_id": top_patient},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["fallback_used"] is True
    assert body["fallback_reason"] == "openai_timeout"


def test_ai_patient_summary_endpoint_fallback_on_http_error(monkeypatch) -> None:
    top_patient = client.get("/patients/high-risk", params={"preset": "baseline", "limit": 1}).json()["patients"][0]["patient_id"]
    monkeypatch.setattr(ai_summary_service, "OPENAI_API_KEY", "test-key")

    def fake_post(*args, **kwargs):
        raise ai_summary_service.httpx.HTTPError("request failed")

    monkeypatch.setattr(ai_summary_service.httpx, "post", fake_post)

    response = client.post(
        "/ai/patient-summary",
        json={"preset": "baseline", "patient_id": top_patient},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["fallback_used"] is True
    assert body["fallback_reason"] == "openai_request_failed"


def test_ai_patient_summary_endpoint_fallback_on_empty_response(monkeypatch) -> None:
    top_patient = client.get("/patients/high-risk", params={"preset": "baseline", "limit": 1}).json()["patients"][0]["patient_id"]
    monkeypatch.setattr(ai_summary_service, "OPENAI_API_KEY", "test-key")

    class MockEmptyResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {"output": []}

    def fake_post(*args, **kwargs):
        return MockEmptyResponse()

    monkeypatch.setattr(ai_summary_service.httpx, "post", fake_post)

    response = client.post(
        "/ai/patient-summary",
        json={"preset": "baseline", "patient_id": top_patient},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["fallback_used"] is True
    assert body["fallback_reason"] == "openai_empty_response"
