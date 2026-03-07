from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

import psycopg

from app.config import DATABASE_URL, MODEL_VERSION

VALID_DB_SCHEMES = {"postgresql", "postgres"}


def database_dsn_status() -> dict[str, Any]:
    value = DATABASE_URL.strip()
    if not value:
        return {
            "configured": False,
            "valid": False,
            "scheme": "",
            "message": "DATABASE_URL is not set.",
        }

    parsed = urlparse(value)
    scheme = parsed.scheme or ""
    valid = scheme in VALID_DB_SCHEMES
    message = "DATABASE_URL looks valid for PostgreSQL." if valid else (
        f"DATABASE_URL uses scheme '{scheme}'. Expected one of: {', '.join(sorted(VALID_DB_SCHEMES))}."
    )

    return {
        "configured": True,
        "valid": valid,
        "scheme": scheme,
        "message": message,
    }


def test_database_connection() -> dict[str, Any]:
    status = database_dsn_status()
    if not status["valid"]:
        status["connected"] = False
        return status

    with psycopg.connect(DATABASE_URL, connect_timeout=10) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), current_user;")
            database_name, current_user = cur.fetchone()

    return {
        **status,
        "connected": True,
        "database": database_name,
        "user": current_user,
    }


def write_prediction_rows(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    status = database_dsn_status()
    if not status["valid"]:
        return {
            **status,
            "connected": False,
            "written_rows": 0,
        }

    now = datetime.now(timezone.utc)
    rows = [
        (
            row["preset"],
            row["encounter_id"],
            row["patient_id"],
            row["predicted_readmission_probability"],
            row["predicted_label"],
            row["risk_level"],
            row["model_name"],
            row["model_version"],
            now,
        )
        for row in predictions
    ]

    with psycopg.connect(DATABASE_URL, connect_timeout=10) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS public.readmission_predictions (
                    preset TEXT NOT NULL,
                    encounter_id TEXT NOT NULL,
                    patient_id TEXT NOT NULL,
                    predicted_readmission_probability DOUBLE PRECISION NOT NULL,
                    predicted_label INTEGER NOT NULL,
                    risk_level TEXT NOT NULL,
                    model_name TEXT NOT NULL,
                    model_version TEXT NOT NULL,
                    generated_at TIMESTAMPTZ NOT NULL,
                    PRIMARY KEY (preset, encounter_id)
                );
                """
            )
            cur.executemany(
                """
                INSERT INTO public.readmission_predictions (
                    preset,
                    encounter_id,
                    patient_id,
                    predicted_readmission_probability,
                    predicted_label,
                    risk_level,
                    model_name,
                    model_version,
                    generated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (preset, encounter_id) DO UPDATE SET
                    patient_id = EXCLUDED.patient_id,
                    predicted_readmission_probability = EXCLUDED.predicted_readmission_probability,
                    predicted_label = EXCLUDED.predicted_label,
                    risk_level = EXCLUDED.risk_level,
                    model_name = EXCLUDED.model_name,
                    model_version = EXCLUDED.model_version,
                    generated_at = EXCLUDED.generated_at;
                """,
                rows,
            )
        conn.commit()

    return {
        **status,
        "connected": True,
        "written_rows": len(rows),
        "table": "public.readmission_predictions",
        "model_version": MODEL_VERSION,
    }
