from app.services.audit import run_system_audit


def test_system_audit_checkset_and_model_payload() -> None:
    audit = run_system_audit("baseline", live_checks=False)
    assert audit["preset"] == "baseline"
    assert isinstance(audit["overall_passed"], bool)
    assert len(audit["checks"]) >= 4
    assert all("name" in item and "status" in item and "detail" in item for item in audit["checks"])
    assert "model" in audit and "llm" in audit and "database" in audit
    assert audit["model"]["prediction_rows"] > 0
