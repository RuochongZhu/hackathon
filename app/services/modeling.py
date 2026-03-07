from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from app.config import MODEL_VERSION, MODELS_DIR, PREDICTIONS_DIR
from app.services.database import write_prediction_rows
from app.services.repository import _risk_level, ensure_dataset_exists

CATEGORICAL_FEATURES = [
    "sex",
    "diagnosis_group",
    "insurance_type",
    "primary_language",
    "discharge_disposition",
]

NUMERIC_FEATURES = [
    "age",
    "chronic_conditions_count",
    "living_alone",
    "length_of_stay",
    "severity_score",
    "icu_flag",
    "prior_admissions_12m",
    "followup_scheduled",
    "medication_complexity",
    "transportation_barrier",
    "missed_appointments_history",
    "last_temp",
    "last_oxygen_sat",
    "last_systolic_bp",
    "last_heart_rate",
    "abnormal_vitals_flag",
]

TARGET_COLUMN = "readmitted_30d"
MODEL_NAME = "logistic_regression"


def _artifact_paths(preset: str) -> dict[str, Path]:
    model_dir = MODELS_DIR / preset
    prediction_dir = PREDICTIONS_DIR / preset
    model_dir.mkdir(parents=True, exist_ok=True)
    prediction_dir.mkdir(parents=True, exist_ok=True)

    return {
        "model": model_dir / "baseline_logreg.joblib",
        "metrics": model_dir / "metrics.json",
        "predictions": prediction_dir / "predictions.csv",
    }


def _load_training_frame(preset: str) -> pd.DataFrame:
    path = ensure_dataset_exists(preset)
    return pd.read_csv(path)


def _build_pipeline() -> Pipeline:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1200, class_weight="balanced")),
        ]
    )


def train_baseline_model(preset: str, write_to_db: bool = False) -> dict[str, Any]:
    df = _load_training_frame(preset)
    features = df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
    target = df[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.25,
        random_state=42,
        stratify=target,
    )

    pipeline = _build_pipeline()
    pipeline.fit(x_train, y_train)

    test_probability = pipeline.predict_proba(x_test)[:, 1]
    test_predictions = (test_probability >= 0.5).astype(int)

    metrics = {
        "accuracy": round(float(accuracy_score(y_test, test_predictions)), 4),
        "precision": round(float(precision_score(y_test, test_predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, test_predictions, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, test_probability)), 4),
    }

    all_probability = pipeline.predict_proba(features)[:, 1]
    predictions_df = pd.DataFrame(
        {
            "preset": preset,
            "patient_id": df["patient_id"],
            "encounter_id": df["encounter_id"],
            "predicted_readmission_probability": all_probability.round(4),
            "predicted_label": (all_probability >= 0.5).astype(int),
            "risk_level": pd.Series(all_probability).map(_risk_level),
            "model_name": MODEL_NAME,
            "model_version": MODEL_VERSION,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
    )

    artifacts = _artifact_paths(preset)
    joblib.dump(pipeline, artifacts["model"])
    predictions_df.to_csv(artifacts["predictions"], index=False)

    db_result = None
    if write_to_db:
        db_result = write_prediction_rows(predictions_df.to_dict(orient="records"))

    return {
        "preset": preset,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "train_rows": int(x_train.shape[0]),
        "test_rows": int(x_test.shape[0]),
        "metrics": metrics,
        "prediction_rows": int(predictions_df.shape[0]),
        "artifacts": {
            "model_path": str(artifacts["model"]),
            "predictions_path": str(artifacts["predictions"]),
        },
        "db_write": db_result,
    }


def load_prediction_summary(preset: str) -> dict[str, Any]:
    artifacts = _artifact_paths(preset)
    if not artifacts["predictions"].exists():
        raise FileNotFoundError(f"No prediction artifact found for preset '{preset}'. Train the model first.")

    df = pd.read_csv(artifacts["predictions"])
    top = df.sort_values("predicted_readmission_probability", ascending=False).head(5)
    return {
        "preset": preset,
        "prediction_rows": int(df.shape[0]),
        "avg_predicted_risk": round(float(df["predicted_readmission_probability"].mean()), 4),
        "high_risk_count": int((df["risk_level"] == "high").sum()),
        "top_patients": top[["patient_id", "predicted_readmission_probability", "risk_level"]].to_dict(orient="records"),
        "predictions_path": str(artifacts["predictions"]),
    }
