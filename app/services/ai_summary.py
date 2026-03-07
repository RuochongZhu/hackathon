from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any

import httpx

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.services.repository import get_patient_profile

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def _format_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _quantitative_signals(profile: dict[str, Any]) -> list[str]:
    clinical = profile["clinical_snapshot"]
    discharge = profile["discharge_factors"]
    vitals = profile["vitals"]
    return [
        f"Predicted readmission risk: {_format_pct(float(profile['risk_score']))} ({profile['risk_level']} risk).",
        f"Prior admissions in last 12 months: {clinical['prior_admissions_12m']}.",
        f"Severity score: {clinical['severity_score']} with length of stay {clinical['length_of_stay']} days.",
        f"Follow-up scheduled: {discharge['followup_scheduled']}; transportation barrier: {discharge['transportation_barrier']}.",
        f"Abnormal vitals flag: {vitals['abnormal_vitals_flag']} (SpO2 {vitals['last_oxygen_sat']}%, HR {vitals['last_heart_rate']}).",
    ]


def _fallback_summary(profile: dict[str, Any], reason: str) -> dict[str, Any]:
    drivers = profile.get("key_drivers", [])[:4]
    actions = profile.get("recommended_actions", [])[:5]
    if not actions:
        actions = ["Maintain routine follow-up and reinforce discharge education."]

    driver_text = ", ".join(drivers) if drivers else "general discharge and chronic risk factors"
    summary = {
        "risk_summary": (
            f"Patient {profile['patient_id']} is {profile['risk_level']} risk "
            f"({_format_pct(float(profile['risk_score']))}) based on model output. "
            f"Top drivers include {driver_text}."
        ),
        "quantitative_signals": _quantitative_signals(profile),
        "recommended_actions": actions,
        "watchouts": [
            "This output is deterministic fallback content based on structured model features.",
            f"Fallback reason: {reason}.",
            "Use this tool for prioritization support, not as a standalone clinical diagnosis.",
        ],
    }
    return summary


def _extract_output_text(payload: dict[str, Any]) -> str:
    output_text = payload.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    parts: list[str] = []
    for item in payload.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if isinstance(text, str) and text.strip():
                parts.append(text.strip())

    return "\n".join(parts).strip()


def _load_summary_json(text: str) -> dict[str, Any] | None:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    try:
        result = json.loads(cleaned)
        return result if isinstance(result, dict) else None
    except json.JSONDecodeError:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        try:
            result = json.loads(cleaned[start : end + 1])
            return result if isinstance(result, dict) else None
        except json.JSONDecodeError:
            return None
    return None


def _coerce_summary(summary_payload: dict[str, Any]) -> dict[str, Any] | None:
    required = ["risk_summary", "quantitative_signals", "recommended_actions", "watchouts"]
    if not all(key in summary_payload for key in required):
        return None

    risk_summary = summary_payload.get("risk_summary")
    quantitative = summary_payload.get("quantitative_signals")
    actions = summary_payload.get("recommended_actions")
    watchouts = summary_payload.get("watchouts")

    if not isinstance(risk_summary, str):
        return None
    if not isinstance(quantitative, list) or not all(isinstance(item, str) for item in quantitative):
        return None
    if not isinstance(actions, list) or not all(isinstance(item, str) for item in actions):
        return None
    if not isinstance(watchouts, list) or not all(isinstance(item, str) for item in watchouts):
        return None

    if not risk_summary.strip() or not actions:
        return None

    return {
        "risk_summary": risk_summary.strip(),
        "quantitative_signals": [item.strip() for item in quantitative if item.strip()],
        "recommended_actions": [item.strip() for item in actions if item.strip()],
        "watchouts": [item.strip() for item in watchouts if item.strip()],
    }


def _build_openai_request(profile: dict[str, Any], temperature: float, max_output_tokens: int) -> dict[str, Any]:
    context = {
        "patient_id": profile["patient_id"],
        "encounter_id": profile["encounter_id"],
        "risk_score": profile["risk_score"],
        "risk_level": profile["risk_level"],
        "key_drivers": profile["key_drivers"],
        "recommended_actions": profile["recommended_actions"],
        "overview": profile["overview"],
        "clinical_snapshot": profile["clinical_snapshot"],
        "discharge_factors": profile["discharge_factors"],
        "vitals": profile["vitals"],
        "similar_cases": profile["similar_cases"],
    }

    system_prompt = (
        "You are a hospital readmission decision-support assistant. "
        "You must not re-predict risk. Use only the provided structured data and explain it."
    )
    user_prompt = (
        "Generate a concise JSON object with keys: risk_summary, quantitative_signals, "
        "recommended_actions, watchouts.\n"
        "Constraints:\n"
        "- risk_summary: 2-4 sentences, explain current model risk and why.\n"
        "- quantitative_signals: 3-5 bullet-like strings using numeric facts.\n"
        "- recommended_actions: 3-5 practical actions for care team prioritization.\n"
        "- watchouts: 2-3 caveats, including uncertainty and non-diagnostic limitations.\n"
        "- Do not invent data.\n"
        "Return JSON only, no markdown.\n\n"
        f"Structured patient context:\n{json.dumps(context, ensure_ascii=True)}"
    )

    return {
        "model": OPENAI_MODEL,
        "input": [
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "input_text", "text": user_prompt}]},
        ],
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }


def generate_patient_summary(
    preset: str,
    patient_id: str,
    temperature: float = 0.2,
    max_output_tokens: int = 500,
    timeout_seconds: float = 20.0,
) -> dict[str, Any]:
    profile = get_patient_profile(preset=preset, patient_id=patient_id)
    generated_at = datetime.now(timezone.utc).isoformat()
    source_model = {
        "model_name": profile["model_name"],
        "model_version": profile["model_version"],
    }

    def fallback(reason: str) -> dict[str, Any]:
        return {
            "preset": preset,
            "patient_id": patient_id,
            "source_model": source_model,
            "llm_model": OPENAI_MODEL,
            "generated_at": generated_at,
            "fallback_used": True,
            "fallback_reason": reason,
            "summary": _fallback_summary(profile, reason=reason),
        }

    api_key = OPENAI_API_KEY.strip()
    if not api_key:
        return fallback("openai_api_key_missing")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = _build_openai_request(profile, temperature=temperature, max_output_tokens=max_output_tokens)

    try:
        response = httpx.post(
            OPENAI_RESPONSES_URL,
            headers=headers,
            json=payload,
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        body = response.json()
    except httpx.TimeoutException:
        return fallback("openai_timeout")
    except httpx.HTTPError:
        return fallback("openai_request_failed")
    except ValueError:
        return fallback("openai_invalid_json_response")

    output_text = _extract_output_text(body)
    if not output_text:
        return fallback("openai_empty_response")

    structured = _load_summary_json(output_text)
    if structured is None:
        return fallback("openai_non_json_response")

    summary = _coerce_summary(structured)
    if summary is None:
        return fallback("openai_invalid_summary_shape")

    return {
        "preset": preset,
        "patient_id": patient_id,
        "source_model": source_model,
        "llm_model": OPENAI_MODEL,
        "generated_at": generated_at,
        "fallback_used": False,
        "fallback_reason": None,
        "summary": summary,
    }
