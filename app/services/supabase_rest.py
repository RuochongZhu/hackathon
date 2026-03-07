"""Supabase REST API client — fallback path when direct PostgreSQL is unavailable."""

from __future__ import annotations

import os
from typing import Any
from urllib.parse import urlparse

import httpx
import pandas as pd

from app.config import SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL

_TIMEOUT_SECONDS = 15.0


def _derive_rest_base() -> str:
    explicit = os.getenv("SUPABASE_REST_URL", "").strip().rstrip("/")
    if explicit:
        return explicit

    value = SUPABASE_URL.strip()
    if value:
        if value.startswith("http"):
            return value.split("/rest/")[0].rstrip("/")

        parsed = urlparse(value)
        host = (parsed.hostname or "").strip()
        if host:
            project_ref = host.replace("db.", "").replace(".supabase.co", "")
            if project_ref and project_ref != host:
                return f"https://{project_ref}.supabase.co"

    host_ref = os.getenv("SUPABASE_HOST", "").strip()
    if host_ref:
        project_ref = host_ref.replace("db.", "").replace(".supabase.co", "")
        if project_ref:
            return f"https://{project_ref}.supabase.co"

    return ""


def _headers(for_write: bool = False) -> dict[str, str]:
    key = (
        SUPABASE_SERVICE_ROLE_KEY.strip()
        if for_write and SUPABASE_SERVICE_ROLE_KEY.strip()
        else SUPABASE_ANON_KEY.strip()
    )
    if not key:
        return {}
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
    }
    if for_write:
        headers["Content-Type"] = "application/json"
    return headers


def _rest_url(table: str) -> str:
    base = _derive_rest_base()
    if not base:
        raise ValueError("Supabase REST base URL is not configured.")
    return f"{base}/rest/v1/{table}"


def fetch_table(table: str, params: dict[str, str] | None = None) -> list[dict[str, Any]]:
    url = _rest_url(table)
    headers = _headers(for_write=False)
    if not headers:
        raise ValueError("SUPABASE_ANON_KEY is not set.")
    resp = httpx.get(url, headers=headers, params=params or {}, timeout=_TIMEOUT_SECONDS)
    resp.raise_for_status()
    return resp.json()


def fetch_joined_dataset(preset: str | None = None, limit: int = 1000) -> pd.DataFrame:
    params: dict[str, str] = {
        "select": "*",
        "limit": str(limit),
        "order": "encounter_id",
    }
    if preset:
        params["preset"] = f"eq.{preset}"
    rows = fetch_table("joined_readmission_dataset", params)
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)


def test_rest_connection() -> dict[str, Any]:
    try:
        rows = fetch_table("patients", {"select": "patient_id", "limit": "1"})
        return {
            "connected": True,
            "method": "rest_api",
            "message": f"Supabase REST API reachable. Sample rows: {len(rows)}.",
        }
    except Exception as exc:
        return {
            "connected": False,
            "method": "rest_api",
            "message": f"Supabase REST API failed: {exc.__class__.__name__}.",
        }


def upsert_prediction_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "connected": True,
            "method": "rest_api",
            "written_rows": 0,
            "table": "public.readmission_predictions",
        }

    url = _rest_url("readmission_predictions")
    headers = _headers(for_write=True)
    if not headers:
        raise ValueError("SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY is not set.")

    # Supabase PostgREST upsert via ON CONFLICT (preset, encounter_id).
    request_headers = {
        **headers,
        "Prefer": "resolution=merge-duplicates,return=minimal",
    }
    response = httpx.post(
        url,
        headers=request_headers,
        params={"on_conflict": "preset,encounter_id"},
        json=rows,
        timeout=_TIMEOUT_SECONDS,
    )
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = response.text.strip()
        if len(detail) > 240:
            detail = f"{detail[:237]}..."
        raise RuntimeError(
            f"Supabase REST upsert failed with HTTP {response.status_code}. {detail}"
        ) from exc
    return {
        "connected": True,
        "method": "rest_api",
        "written_rows": len(rows),
        "table": "public.readmission_predictions",
    }
