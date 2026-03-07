from app.services.repository import get_dashboard_summary, get_high_risk_patients, get_patient_profile, list_patient_ids


def test_dashboard_summary_has_enriched_metrics() -> None:
    summary = get_dashboard_summary("baseline")
    assert summary["patient_count"] > 0
    assert summary["avg_risk"] > 0
    assert len(summary["risk_level_distribution"]) >= 1
    assert len(summary["diagnosis_distribution"]) >= 1


def test_high_risk_patients_sorted_desc() -> None:
    patients = get_high_risk_patients("baseline", limit=5)
    probabilities = [item["predicted_readmission_probability"] for item in patients]
    assert probabilities == sorted(probabilities, reverse=True)


def test_patient_profile_contains_actions_and_similar_cases() -> None:
    patient_id = list_patient_ids("baseline")[0]
    profile = get_patient_profile("baseline", patient_id)
    assert profile["risk_score"] >= 0
    assert len(profile["key_drivers"]) >= 1
    assert len(profile["recommended_actions"]) >= 1
    assert len(profile["similar_cases"]) >= 1
