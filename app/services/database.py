from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

import psycopg

from app.config import DATABASE_URL, MODEL_VERSION
from app.services.supabase_rest import test_rest_connection, upsert_prediction_rows

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
    direct_error: Exception | None = None

    if status["valid"]:
        try:
            with psycopg.connect(DATABASE_URL, connect_timeout=10) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT current_database(), current_user;")
                    database_name, current_user = cur.fetchone()
            return {
                **status,
                "connected": True,
                "database": database_name,
                "user": current_user,
                "method": "postgresql",
                "message": "Connected using direct PostgreSQL.",
            }
        except Exception as exc:
            direct_error = exc

    rest_status = test_rest_connection()
    if rest_status.get("connected", False):
        direct_detail = (
            f" Direct PostgreSQL failed with {direct_error.__class__.__name__}."
            if direct_error is not None
            else ""
        )
        return {
            **status,
            "connected": True,
            "database": "supabase_rest",
            "user": "service",
            "method": "rest_api",
            "message": f"Connected using Supabase REST fallback.{direct_detail}",
        }

    if not status["valid"]:
        return {
            **status,
            "connected": False,
            "method": "none",
            "message": f"{status['message']} {rest_status.get('message', '').strip()}".strip(),
        }

    return {
        **status,
        "connected": False,
        "method": "none",
        "message": (
            f"Database connection failed: {direct_error.__class__.__name__ if direct_error else 'UnknownError'}; "
            f"{rest_status.get('message', 'REST fallback unavailable')}"
        ),
    }


def write_prediction_rows(predictions: list[dict[str, Any]]) -> dict[str, Any]:
    status = database_dsn_status()
    if not predictions:
        return {
            **status,
            "connected": True,
            "written_rows": 0,
            "table": "public.readmission_predictions",
            "model_version": MODEL_VERSION,
            "message": "No prediction rows supplied.",
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

    direct_error: Exception | None = None
    if status["valid"]:
        try:
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
                "method": "postgresql",
            }
        except Exception as exc:
            direct_error = exc

    rest_payload = [
        {
            "preset": row["preset"],
            "encounter_id": row["encounter_id"],
            "patient_id": row["patient_id"],
            "predicted_readmission_probability": row["predicted_readmission_probability"],
            "predicted_label": row["predicted_label"],
            "risk_level": row["risk_level"],
            "model_name": row["model_name"],
            "model_version": row["model_version"],
            "generated_at": row.get("generated_at") or now.isoformat(),
        }
        for row in predictions
    ]

    try:
        rest_result = upsert_prediction_rows(rest_payload)
        message = "Predictions written via Supabase REST fallback."
        if direct_error is not None:
            message = f"{message} Direct PostgreSQL failed with {direct_error.__class__.__name__}."
        return {
            **status,
            "connected": True,
            "written_rows": rest_result["written_rows"],
            "table": rest_result["table"],
            "model_version": MODEL_VERSION,
            "method": "rest_api",
            "message": message,
        }
    except Exception as rest_exc:
        detail = (
            f"Direct PostgreSQL failed with {direct_error.__class__.__name__}. "
            if direct_error is not None
            else ""
        )
        rest_detail = str(rest_exc).strip() or rest_exc.__class__.__name__
        if len(rest_detail) > 260:
            rest_detail = f"{rest_detail[:257]}..."
        return {
            **status,
            "connected": False,
            "written_rows": 0,
            "table": "public.readmission_predictions",
            "model_version": MODEL_VERSION,
            "method": "none",
            "message": f"{detail}REST write failed. {rest_detail}",
        }
