from __future__ import annotations

from typing import Any

import httpx

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.services.database import database_dsn_status, test_database_connection


def llm_status(live_check: bool = True, timeout_seconds: float = 8.0) -> dict[str, Any]:
    key = OPENAI_API_KEY.strip()
    status: dict[str, Any] = {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "configured": bool(key),
        "api_reachable": False,
        "auth_valid": False,
        "model_available": False,
        "message": "OPENAI_API_KEY is not set.",
    }

    if not key:
        return status

    if not live_check:
        status["message"] = "OPENAI key is configured. Live reachability check skipped."
        return status

    headers = {"Authorization": f"Bearer {key}"}
    endpoint = f"https://api.openai.com/v1/models/{OPENAI_MODEL}"

    try:
        response = httpx.get(endpoint, headers=headers, timeout=timeout_seconds)
    except httpx.HTTPError as exc:
        status["message"] = f"OpenAI connectivity failed: {exc.__class__.__name__}."
        return status

    status["api_reachable"] = True

    if response.status_code == 200:
        status["auth_valid"] = True
        status["model_available"] = True
        status["message"] = f"Connected to OpenAI and model '{OPENAI_MODEL}' is available."
        return status

    detail = ""
    try:
        detail = response.json().get("error", {}).get("message", "")
    except ValueError:
        detail = ""

    if response.status_code in {401, 403}:
        status["message"] = f"OpenAI authentication failed ({response.status_code})."
    elif response.status_code == 404:
        status["auth_valid"] = True
        status["message"] = f"OpenAI auth is valid but model '{OPENAI_MODEL}' is unavailable."
    else:
        status["message"] = f"OpenAI returned HTTP {response.status_code}."

    if detail:
        status["message"] = f"{status['message']} {detail}"

    return status


def database_status(live_check: bool = False) -> dict[str, Any]:
    status = database_dsn_status()
    if not live_check or not status.get("valid", False):
        return {
            **status,
            "connected": False,
            "message": status["message"] if not live_check else f"{status['message']} Live connection skipped.",
        }

    try:
        return test_database_connection()
    except Exception as exc:
        return {
            **status,
            "connected": False,
            "message": f"Database connection failed: {exc.__class__.__name__}.",
        }
