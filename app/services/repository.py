from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from app.config import DATASETS_DIR, PREDICTIONS_DIR, PRESET_CONFIGS
from app.services.simulator import generate_dataset_bundle, write_dataset_bundle

import logging

_log = logging.getLogger(__name__)

RISK_THRESHOLDS = {
    "high": 0.65,
    "medium": 0.35,
}

NUMERIC_SIMILARITY_COLUMNS = [
    "age",
    "chronic_conditions_count",
    "prior_admissions_12m",
    "length_of_stay",
    "severity_score",
    "medication_complexity",
    "missed_appointments_history",
    "last_oxygen_sat",
    "last_heart_rate",
]


class DatasetNotFoundError(FileNotFoundError):
    pass


class PatientNotFoundError(LookupError):
    pass


class PresetNotFoundError(KeyError):
    pass


def ensure_dataset_exists(preset: str) -> Path:
    if preset not in PRESET_CONFIGS:
        raise PresetNotFoundError(preset)

    model_input_path = DATASETS_DIR / preset / "model_input.csv"
    if model_input_path.exists():
        return model_input_path

    config = PRESET_CONFIGS[preset]
    bundle = generate_dataset_bundle(
        preset=preset,
        patient_count=config["patient_count"],
        seed=42,
    )
    write_dataset_bundle(bundle)
    return model_input_path


def _risk_level(probability: float) -> str:
    if probability >= RISK_THRESHOLDS["high"]:
        return "high"
    if probability >= RISK_THRESHOLDS["medium"]:
        return "medium"
    return "low"


def load_from_supabase(preset: str | None = None) -> pd.DataFrame | None:
    """Fetch from Supabase joined_readmission_dataset view, filtered by preset."""
    try:
        from app.services.supabase_rest import fetch_joined_dataset
        df = fetch_joined_dataset(preset=preset, limit=3000)
        if df.empty:
            return None
        # Client-side filter as safety net
        if preset and "preset" in df.columns:
            df = df[df["preset"] == preset]
            if df.empty:
                return None
        # Derive columns expected by downstream code
        if "predicted_readmission_probability" not in df.columns or df["predicted_readmission_probability"].isna().all():
            # Recompute risk probability using the same logistic formula as simulator
            risk_linear = (
                -4.4
                + (df["age"] >= 75).astype(float) * 0.5
                + df["chronic_conditions_count"] * 0.22
                + df["prior_admissions_12m"] * 0.34
                + df["severity_score"] * 0.24
                + df["icu_flag"] * 0.5
                + df["length_of_stay"] * 0.08
                + df["abnormal_vitals_flag"] * 0.72
                + (1 - df["followup_scheduled"]) * 0.48
                + df["transportation_barrier"] * 0.52
                + df["missed_appointments_history"] * 0.14
                + df["living_alone"] * 0.18
            )
            df["predicted_readmission_probability"] = np.round(1.0 / (1.0 + np.exp(-risk_linear)), 4)
        df["active_risk_probability"] = pd.to_numeric(
            df["predicted_readmission_probability"], errors="coerce"
        ).fillna(0.0)
        df["simulated_readmission_probability"] = df["active_risk_probability"]
        if "risk_level" not in df.columns or df["risk_level"].isna().all():
            df["risk_level"] = df["active_risk_probability"].apply(_risk_level)
        df["risk_level"] = df["risk_level"].fillna(
            df["active_risk_probability"].apply(_risk_level)
        )
        if "model_name" not in df.columns:
            df["model_name"] = "logistic_regression"
        if "model_version" not in df.columns:
            df["model_version"] = "baseline-logreg-v1"
        if "generated_at" not in df.columns:
            df["generated_at"] = None
        if "preset" not in df.columns:
            df["preset"] = preset or "supabase"
        df["recommended_action"] = df.apply(_recommended_action_label, axis=1)
        _log.info("Loaded %d rows from Supabase", len(df))
        return df
    except Exception as exc:
        _log.debug("Supabase load failed: %s", exc)
        return None


def _prediction_path(preset: str) -> Path:
    return PREDICTIONS_DIR / preset / "predictions.csv"


def _load_prediction_frame(preset: str) -> pd.DataFrame | None:
    path = _prediction_path(preset)
    if not path.exists():
        return None
    return pd.read_csv(path)


def _driver_candidates(row: pd.Series) -> list[tuple[str, float]]:
    return [
        ("Abnormal discharge vitals", 0.72 if row["abnormal_vitals_flag"] else 0.0),
        ("No follow-up scheduled", 0.48 if not row["followup_scheduled"] else 0.0),
        ("Transportation barrier", 0.52 if row["transportation_barrier"] else 0.0),
        ("ICU stay during admission", 0.50 if row["icu_flag"] else 0.0),
        ("Frequent recent admissions", 0.34 * row["prior_admissions_12m"]),
        ("High chronic condition burden", 0.22 * row["chronic_conditions_count"]),
        ("Complex medication plan", 0.07 * row["medication_complexity"]),
        ("Older age profile", 0.50 if row["age"] >= 75 else 0.0),
        ("Lives alone", 0.18 if row["living_alone"] else 0.0),
        ("Missed appointment history", 0.14 * row["missed_appointments_history"]),
    ]


def build_key_drivers(row: pd.Series, limit: int = 4) -> list[str]:
    candidates = sorted(_driver_candidates(row), key=lambda item: item[1], reverse=True)
    return [label for label, score in candidates if score > 0][:limit]


def build_recommended_actions(row: pd.Series, limit: int = 4) -> list[str]:
    actions: list[str] = []

    if not row["followup_scheduled"]:
        actions.append("Schedule a follow-up visit before discharge closes.")
    if row["transportation_barrier"]:
        actions.append("Arrange transportation support for post-discharge follow-up.")
    if row["medication_complexity"] >= 8:
        actions.append("Perform pharmacist-led medication reconciliation and teach-back.")
    if row["abnormal_vitals_flag"]:
        actions.append("Add 48-hour nurse outreach and symptom monitoring.")
    if row["prior_admissions_12m"] >= 2:
        actions.append("Escalate to care coordination for intensive discharge planning.")
    if row["living_alone"]:
        actions.append("Assess home support and consider community care services.")

    if not actions:
        actions.append("Maintain routine follow-up and reinforce discharge education.")

    return actions[:limit]


def _recommended_action_label(row: pd.Series) -> str:
    return build_recommended_actions(row, limit=1)[0]


def load_model_input(preset: str) -> pd.DataFrame:
    # Try Supabase first
    supa_df = load_from_supabase(preset)
    if supa_df is not None and not supa_df.empty:
        return supa_df

    path = ensure_dataset_exists(preset)
    if not path.exists():
        raise DatasetNotFoundError(f"Dataset preset '{preset}' has not been generated yet")

    df = pd.read_csv(path)

    predictions = _load_prediction_frame(preset)
    if predictions is not None:
        df = df.merge(
            predictions[
                [
                    "preset",
                    "patient_id",
                    "encounter_id",
                    "predicted_readmission_probability",
                    "predicted_label",
                    "risk_level",
                    "model_name",
                    "model_version",
                    "generated_at",
                ]
            ],
            on=["patient_id", "encounter_id"],
            how="left",
        )
    else:
        df["predicted_readmission_probability"] = df["simulated_readmission_probability"]
        df["predicted_label"] = (df["simulated_readmission_probability"] >= 0.5).astype(int)
        df["risk_level"] = df["simulated_readmission_probability"].apply(_risk_level)
        df["model_name"] = "latent_simulation_rule"
        df["model_version"] = "simulation-only"
        df["generated_at"] = None

    df["active_risk_probability"] = df["predicted_readmission_probability"].fillna(df["simulated_readmission_probability"])
    df["risk_level"] = df["risk_level"].fillna(df["active_risk_probability"].apply(_risk_level))
    df["recommended_action"] = df.apply(_recommended_action_label, axis=1)
    return df


def _distribution_items(series: pd.Series) -> list[dict[str, Any]]:
    counts = series.value_counts(dropna=False)
    return [{"label": str(label), "value": int(value)} for label, value in counts.items()]


def get_dashboard_summary(preset: str) -> dict[str, Any]:
    df = load_model_input(preset)
    high_risk = df.nlargest(3, "active_risk_probability")
    prediction_path = _prediction_path(preset)

    return {
        "preset": preset,
        "title": PRESET_CONFIGS[preset]["name"],
        "patient_count": int(df["patient_id"].nunique()),
        "encounter_count": int(df["encounter_id"].nunique()),
        "readmission_rate": round(float(df["readmitted_30d"].mean()), 4),
        "avg_risk": round(float(df["active_risk_probability"].mean()), 4),
        "high_risk_count": int((df["risk_level"] == "high").sum()),
        "model_ready": prediction_path.exists(),
        "high_risk_signals": [
            f"{row.patient_id}: {row.active_risk_probability:.1%} predicted risk"
            for row in high_risk.itertuples()
        ],
        "risk_level_distribution": _distribution_items(df["risk_level"]),
        "diagnosis_distribution": _distribution_items(df["diagnosis_group"]),
        "artifacts": [
            {
                "name": file_name,
                "rows": int(pd.read_csv(DATASETS_DIR / preset / file_name).shape[0]),
                "path": str(DATASETS_DIR / preset / file_name),
            }
            for file_name in [
                "patients.csv",
                "encounters.csv",
                "discharge_factors.csv",
                "vitals_summary.csv",
                "model_input.csv",
            ]
        ] + (
            [{"name": "predictions.csv", "rows": int(pd.read_csv(prediction_path).shape[0]), "path": str(prediction_path)}]
            if prediction_path.exists()
            else []
        ),
    }


def list_patient_ids(preset: str) -> list[str]:
    df = load_model_input(preset)
    return df.sort_values("active_risk_probability", ascending=False)["patient_id"].tolist()


def get_high_risk_patients(
    preset: str,
    limit: int = 15,
    diagnosis_group: str | None = None,
    risk_level: str | None = None,
) -> list[dict[str, Any]]:
    df = load_model_input(preset)

    if diagnosis_group and diagnosis_group != "all":
        df = df[df["diagnosis_group"] == diagnosis_group]
    if risk_level and risk_level != "all":
        df = df[df["risk_level"] == risk_level]

    columns = [
        "patient_id",
        "encounter_id",
        "age",
        "diagnosis_group",
        "prior_admissions_12m",
        "severity_score",
        "predicted_readmission_probability",
        "risk_level",
        "recommended_action",
        "readmitted_30d",
        "model_name",
        "model_version",
    ]

    top = df.sort_values("active_risk_probability", ascending=False).head(limit).copy()
    top["predicted_readmission_probability"] = top["active_risk_probability"].round(4)

    return top[columns].to_dict(orient="records")


def _cohort_medians(df: pd.DataFrame) -> dict[str, float]:
    return {column: float(df[column].median()) for column in NUMERIC_SIMILARITY_COLUMNS}


def get_patient_profile(preset: str, patient_id: str, similar_limit: int = 3) -> dict[str, Any]:
    df = load_model_input(preset)
    row_matches = df[df["patient_id"] == patient_id]
    if row_matches.empty:
        raise PatientNotFoundError(patient_id)

    row = row_matches.iloc[0]
    similar_cases = get_similar_cases(preset, patient_id, limit=similar_limit)
    key_drivers = build_key_drivers(row)
    recommended_actions = build_recommended_actions(row)
    cohort_medians = _cohort_medians(df)

    return {
        "preset": preset,
        "patient_id": str(row["patient_id"]),
        "encounter_id": str(row["encounter_id"]),
        "risk_score": round(float(row["active_risk_probability"]), 4),
        "risk_level": str(row["risk_level"]),
        "readmitted_30d": int(row["readmitted_30d"]),
        "model_name": str(row["model_name"]),
        "model_version": str(row["model_version"]),
        "key_drivers": key_drivers,
        "recommended_actions": recommended_actions,
        "overview": {
            "age": int(row["age"]),
            "sex": str(row["sex"]),
            "diagnosis_group": str(row["diagnosis_group"]),
            "insurance_type": str(row["insurance_type"]),
            "living_alone": int(row["living_alone"]),
            "primary_language": str(row["primary_language"]),
        },
        "clinical_snapshot": {
            "chronic_conditions_count": int(row["chronic_conditions_count"]),
            "severity_score": int(row["severity_score"]),
            "length_of_stay": int(row["length_of_stay"]),
            "prior_admissions_12m": int(row["prior_admissions_12m"]),
            "icu_flag": int(row["icu_flag"]),
        },
        "discharge_factors": {
            "discharge_disposition": str(row["discharge_disposition"]),
            "followup_scheduled": int(row["followup_scheduled"]),
            "medication_complexity": int(row["medication_complexity"]),
            "transportation_barrier": int(row["transportation_barrier"]),
            "missed_appointments_history": int(row["missed_appointments_history"]),
        },
        "vitals": {
            "last_temp": float(row["last_temp"]),
            "last_oxygen_sat": float(row["last_oxygen_sat"]),
            "last_systolic_bp": int(row["last_systolic_bp"]),
            "last_heart_rate": int(row["last_heart_rate"]),
            "abnormal_vitals_flag": int(row["abnormal_vitals_flag"]),
        },
        "cohort_medians": cohort_medians,
        "similar_cases": similar_cases,
    }


def get_similar_cases(preset: str, patient_id: str, limit: int = 3) -> list[dict[str, Any]]:
    df = load_model_input(preset)
    row_matches = df[df["patient_id"] == patient_id]
    if row_matches.empty:
        raise PatientNotFoundError(patient_id)

    target = row_matches.iloc[0]
    others = df[df["patient_id"] != patient_id].copy()
    if others.empty:
        return []

    matrix = others[NUMERIC_SIMILARITY_COLUMNS].astype(float)
    target_values = target[NUMERIC_SIMILARITY_COLUMNS].astype(float)
    std = matrix.std(ddof=0).replace(0, 1)

    normalized = (matrix - target_values) / std
    others["distance"] = np.sqrt((normalized**2).sum(axis=1))
    others["similarity_score"] = 1 / (1 + others["distance"])

    top = others.nsmallest(limit, "distance").copy()
    top["similarity_score"] = top["similarity_score"].round(4)
    top["predicted_readmission_probability"] = top["active_risk_probability"].round(4)

    columns = [
        "patient_id",
        "encounter_id",
        "diagnosis_group",
        "risk_level",
        "predicted_readmission_probability",
        "readmitted_30d",
        "similarity_score",
    ]
    return top[columns].to_dict(orient="records")
