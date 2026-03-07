from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any

import httpx

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.services.repository import get_patient_profile

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"


def _format_pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _call_openai(messages: list[dict], model: str, temperature: float = 0.2, max_tokens: int = 600, timeout: float = 20.0) -> dict[str, Any]:
    """Generic OpenAI Responses API call. Returns parsed JSON or error dict."""
    api_key = OPENAI_API_KEY.strip()
    if not api_key:
        return {"error": "openai_api_key_missing"}

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "input": messages,
        "temperature": temperature,
        "max_output_tokens": max_tokens,
    }

    try:
        resp = httpx.post(OPENAI_RESPONSES_URL, headers=headers, json=payload, timeout=timeout)
        resp.raise_for_status()
        body = resp.json()
    except httpx.TimeoutException:
        return {"error": "openai_timeout"}
    except httpx.HTTPError:
        return {"error": "openai_request_failed"}
    except ValueError:
        return {"error": "openai_invalid_response"}

    text = _extract_output_text(body)
    if not text:
        return {"error": "openai_empty_response"}

    return {"text": text}


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


def _parse_json(text: str) -> dict[str, Any] | None:
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


def _build_context(profile: dict[str, Any]) -> str:
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
    return json.dumps(context, ensure_ascii=True)


# ── Feature 1: AI Risk Summary ──

RISK_SUMMARY_SYSTEM = (
    "You are a clinical decision-support assistant. Your job is to explain "
    "WHY a patient is at risk for 30-day hospital readmission. "
    "Write as if briefing a care coordination team. Be specific — reference "
    "the patient's actual clinical data. Do not re-predict risk."
)

RISK_SUMMARY_PROMPT = (
    "Analyze this patient and generate a JSON object:\n\n"
    '{{\n'
    '  "risk_narrative": "A 4-6 sentence clinical narrative explaining why this '
    "patient is at their current risk level. Start with the patient's risk score "
    "and level. Then explain the key risk factors: prior admissions, severity, "
    "comorbidities, vitals, social factors (living alone, transportation, follow-up). "
    "End with what the care team should pay most attention to. "
    'Be specific with numbers from the data.",\n'
    '  "key_factors": ["List the 3-5 most important risk factors as short bullet points, '
    'each referencing a specific data point. Example: Prior admissions: 3 in last 12 months"]\n'
    '}}\n\n'
    "Return JSON only, no markdown.\n\n"
    "Patient data:\n{context}"
)


def generate_risk_summary(profile: dict[str, Any], model: str = "", temperature: float = 0.2) -> dict[str, Any]:
    model = model or OPENAI_MODEL
    context = _build_context(profile)
    messages = [
        {"role": "system", "content": [{"type": "input_text", "text": RISK_SUMMARY_SYSTEM}]},
        {"role": "user", "content": [{"type": "input_text", "text": RISK_SUMMARY_PROMPT.format(context=context)}]},
    ]
    result = _call_openai(messages, model=model, temperature=temperature)
    if "error" in result:
        drivers = profile.get("key_drivers", [])[:5]
        driver_text = ", ".join(drivers) if drivers else "general clinical risk factors"
        return {
            "fallback": True,
            "risk_narrative": (
                f"Patient {profile['patient_id']} has a {profile['risk_level']} "
                f"readmission risk of {_format_pct(profile['risk_score'])}. "
                f"Key contributing factors include {driver_text}. "
                f"The care team should review this patient's discharge plan."
            ),
            "key_factors": drivers,
            "model": model,
        }
    parsed = _parse_json(result["text"])
    if not parsed or "risk_narrative" not in parsed:
        return {
            "fallback": True,
            "risk_narrative": result["text"],
            "key_factors": profile.get("key_drivers", [])[:5],
            "model": model,
        }
    return {
        "fallback": False,
        "risk_narrative": parsed["risk_narrative"],
        "key_factors": parsed.get("key_factors", profile.get("key_drivers", [])),
        "model": model,
    }


# ── Feature 2: AI Recommended Actions ──

ACTIONS_SYSTEM = (
    "You are a hospital care coordination assistant. Your job is to recommend "
    "specific, actionable next steps for the clinical team based on a patient's "
    "risk profile. Focus on MODIFIABLE risk factors — things the team can actually "
    "change. Be concrete: name specific interventions, timeframes, and responsible parties."
)

ACTIONS_PROMPT = (
    "Based on this patient's risk profile, generate a JSON object:\n\n"
    '{{\n'
    '  "action_plan": "A 3-4 sentence summary of the overall intervention strategy. '
    "What is the priority? What should happen first? What's the timeline?\",\n"
    '  "actions": [\n'
    '    {{"action": "Specific intervention", "rationale": "Why this matters for this patient", "priority": "high/medium/low"}},\n'
    "    ... (3-5 actions)\n"
    "  ]\n"
    '}}\n\n'
    "Focus on:\n"
    "- Follow-up scheduling if not scheduled\n"
    "- Transportation if barrier exists\n"
    "- Medication reconciliation if complex\n"
    "- Vitals monitoring if abnormal\n"
    "- Social support if living alone\n"
    "- Care escalation if frequent admissions\n\n"
    "Return JSON only, no markdown.\n\n"
    "Patient data:\n{context}"
)


def generate_actions(profile: dict[str, Any], model: str = "", temperature: float = 0.2) -> dict[str, Any]:
    model = model or OPENAI_MODEL
    context = _build_context(profile)
    messages = [
        {"role": "system", "content": [{"type": "input_text", "text": ACTIONS_SYSTEM}]},
        {"role": "user", "content": [{"type": "input_text", "text": ACTIONS_PROMPT.format(context=context)}]},
    ]
    result = _call_openai(messages, model=model, temperature=temperature)
    if "error" in result:
        return {
            "fallback": True,
            "action_plan": f"Patient {profile['patient_id']} requires targeted interventions based on their {profile['risk_level']} risk profile.",
            "actions": [{"action": a, "rationale": "", "priority": "high"} for a in profile.get("recommended_actions", [])[:5]],
            "model": model,
        }
    parsed = _parse_json(result["text"])
    if not parsed or "actions" not in parsed:
        return {
            "fallback": True,
            "action_plan": result["text"],
            "actions": [{"action": a, "rationale": "", "priority": "high"} for a in profile.get("recommended_actions", [])[:5]],
            "model": model,
        }
    return {
        "fallback": False,
        "action_plan": parsed.get("action_plan", ""),
        "actions": parsed.get("actions", []),
        "model": model,
    }


# ── Feature 3: AI Similar Case Comparison ──

SIMILAR_SYSTEM = (
    "You are a clinical analytics assistant. Your job is to compare a patient "
    "to similar historical cases and explain what those comparisons mean for "
    "the patient's likely trajectory. Focus on outcomes — did similar patients "
    "get readmitted? What patterns emerge?"
)

SIMILAR_PROMPT = (
    "Compare this patient to their similar historical cases and generate a JSON object:\n\n"
    '{{\n'
    '  "comparison_narrative": "A 4-6 sentence analysis comparing this patient to the '
    "similar cases. For each similar case, note: their risk level, whether they were "
    "readmitted, and what they share with the current patient. End with what this "
    'pattern suggests for the current patient\'s outcome.",\n'
    '  "pattern_insight": "One sentence summarizing the key takeaway from the comparison."\n'
    '}}\n\n'
    "Return JSON only, no markdown.\n\n"
    "Patient data:\n{context}"
)


def generate_similar_analysis(profile: dict[str, Any], model: str = "", temperature: float = 0.2) -> dict[str, Any]:
    model = model or OPENAI_MODEL
    context = _build_context(profile)
    similar = profile.get("similar_cases", [])
    messages = [
        {"role": "system", "content": [{"type": "input_text", "text": SIMILAR_SYSTEM}]},
        {"role": "user", "content": [{"type": "input_text", "text": SIMILAR_PROMPT.format(context=context)}]},
    ]
    result = _call_openai(messages, model=model, temperature=temperature)
    if "error" in result:
        if similar:
            ids = ", ".join(c["patient_id"] for c in similar[:3])
            readmitted = sum(1 for c in similar if c.get("readmitted_30d"))
            return {
                "fallback": True,
                "comparison_narrative": (
                    f"Patient {profile['patient_id']} has {len(similar)} similar historical cases ({ids}). "
                    f"Of these, {readmitted} were readmitted within 30 days. "
                    f"This pattern suggests {'elevated' if readmitted > 0 else 'moderate'} risk for this patient."
                ),
                "pattern_insight": f"{readmitted} of {len(similar)} similar patients were readmitted.",
                "model": model,
            }
        return {
            "fallback": True,
            "comparison_narrative": "No similar historical cases available for comparison.",
            "pattern_insight": "",
            "model": model,
        }
    parsed = _parse_json(result["text"])
    if not parsed or "comparison_narrative" not in parsed:
        return {
            "fallback": True,
            "comparison_narrative": result["text"],
            "pattern_insight": "",
            "model": model,
        }
    return {
        "fallback": False,
        "comparison_narrative": parsed["comparison_narrative"],
        "pattern_insight": parsed.get("pattern_insight", ""),
        "model": model,
    }


# ── Follow-up chat ──

def chat_followup(profile: dict[str, Any], history: list[dict[str, str]], user_message: str, model: str = "", temperature: float = 0.3) -> str:
    """Continue a conversation about a patient using Chat Completions API for multi-turn support."""
    model = model or OPENAI_MODEL
    api_key = OPENAI_API_KEY.strip()
    if not api_key:
        return "Unable to respond: openai_api_key_missing"

    context = _build_context(profile)
    system = (
        "You are a clinical decision-support assistant. You are discussing a specific patient "
        "with a care team member. Answer questions about this patient's risk, interventions, "
        "or similar cases using ONLY the provided data. Be concise and clinical. "
        "Do not invent data.\n\n"
        f"Patient context:\n{context}"
    )
    messages = [{"role": "system", "content": system}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 400,
    }
    try:
        resp = httpx.post(OPENAI_CHAT_URL, headers=headers, json=payload, timeout=20.0)
        resp.raise_for_status()
        body = resp.json()
        return body["choices"][0]["message"]["content"].strip()
    except Exception:
        return "Unable to respond: openai_request_failed"


# ── Legacy wrapper (kept for API compatibility) ──

def generate_patient_summary(
    preset: str,
    patient_id: str,
    temperature: float = 0.2,
    max_output_tokens: int = 600,
    timeout_seconds: float = 20.0,
) -> dict[str, Any]:
    profile = get_patient_profile(preset=preset, patient_id=patient_id)
    risk = generate_risk_summary(profile, temperature=temperature)
    actions = generate_actions(profile, temperature=temperature)
    similar = generate_similar_analysis(profile, temperature=temperature)
    return {
        "preset": preset,
        "patient_id": patient_id,
        "source_model": {"model_name": profile["model_name"], "model_version": profile["model_version"]},
        "llm_model": OPENAI_MODEL,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fallback_used": risk["fallback"] or actions["fallback"] or similar["fallback"],
        "summary": {
            "risk_summary": risk["risk_narrative"],
            "recommended_actions": [a["action"] if isinstance(a, dict) else a for a in actions.get("actions", [])],
            "similar_case_analysis": similar["comparison_narrative"],
        },
    }
