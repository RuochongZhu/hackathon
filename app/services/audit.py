from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import PREDICTIONS_DIR
from app.services.integrations import database_status, llm_status
from app.services.repository import (
    RISK_THRESHOLDS,
    get_dashboard_summary,
    get_high_risk_patients,
    load_model_input,
)


def _check(name: str, passed: bool, detail: str) -> dict[str, str]:
    return {"name": name, "status": "pass" if passed else "fail", "detail": detail}


def run_system_audit(preset: str, live_checks: bool = False) -> dict[str, Any]:
    df = load_model_input(preset)
    summary = get_dashboard_summary(preset)

    checks: list[dict[str, str]] = []
    checks.append(
        _check(
            "Patient count matches summary",
            summary["patient_count"] == int(df["patient_id"].nunique()),
            f"summary={summary['patient_count']} dataset={int(df['patient_id'].nunique())}",
        )
    )

    checks.append(
        _check(
            "Risk distribution totals are consistent",
            sum(item["value"] for item in summary["risk_level_distribution"]) == int(df.shape[0]),
            f"distribution_total={sum(item['value'] for item in summary['risk_level_distribution'])} rows={int(df.shape[0])}",
        )
    )

    checks.append(
        _check(
            "Diagnosis distribution totals are consistent",
            sum(item["value"] for item in summary["diagnosis_distribution"]) == int(df.shape[0]),
            f"distribution_total={sum(item['value'] for item in summary['diagnosis_distribution'])} rows={int(df.shape[0])}",
        )
    )

    probabilities = df["active_risk_probability"].astype(float)
    checks.append(
        _check(
            "Risk scores are bounded between 0 and 1",
            bool(((probabilities >= 0) & (probabilities <= 1)).all()),
            f"min={probabilities.min():.4f} max={probabilities.max():.4f}",
        )
    )

    expected_high_risk = int((probabilities >= RISK_THRESHOLDS["high"]).sum())
    checks.append(
        _check(
            "High-risk count aligns with configured threshold",
            summary["high_risk_count"] == expected_high_risk,
            f"summary={summary['high_risk_count']} threshold_count={expected_high_risk} (>= {RISK_THRESHOLDS['high']})",
        )
    )

    top_rows = get_high_risk_patients(preset=preset, limit=min(10, int(df.shape[0])))
    probs = [row["predicted_readmission_probability"] for row in top_rows]
    checks.append(
        _check(
            "High-risk explorer rows are sorted descending",
            probs == sorted(probs, reverse=True),
            f"top_probabilities={probs[:5]}",
        )
    )

    prediction_path = Path(PREDICTIONS_DIR / preset / "predictions.csv")
    model_name = str(df["model_name"].mode().iat[0]) if "model_name" in df.columns else "unknown"
    model_version = str(df["model_version"].mode().iat[0]) if "model_version" in df.columns else "unknown"
    prediction_rows = int(df["predicted_readmission_probability"].notna().sum())

    llm = llm_status(live_check=live_checks)
    db = database_status(live_check=live_checks)

    overall = all(item["status"] == "pass" for item in checks)

    return {
        "preset": preset,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_passed": overall,
        "checks": checks,
        "model": {
            "ready": bool(prediction_path.exists()),
            "name": model_name,
            "version": model_version,
            "prediction_rows": prediction_rows,
            "prediction_artifact": str(prediction_path),
            "thresholds": RISK_THRESHOLDS,
        },
        "llm": llm,
        "database": db,
    }
