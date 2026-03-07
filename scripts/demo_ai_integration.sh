#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

if [[ ! -x ".venv/bin/python" ]]; then
  echo "Error: .venv/bin/python not found. Create virtualenv and install dependencies first."
  exit 1
fi

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  read -r -s -p "Enter OPENAI_API_KEY: " OPENAI_API_KEY
  echo
fi

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "Error: OPENAI_API_KEY is required."
  exit 1
fi

export OPENAI_API_KEY
export OPENAI_MODEL="${OPENAI_MODEL:-gpt-4o-mini}"
export PYTHONPATH="${ROOT_DIR}:${PYTHONPATH:-}"

HOST="127.0.0.1"
PORT="${PORT:-8000}"
BASE_URL="http://${HOST}:${PORT}"

cleanup() {
  if [[ -n "${SERVER_PID:-}" ]] && kill -0 "${SERVER_PID}" 2>/dev/null; then
    kill "${SERVER_PID}" 2>/dev/null || true
    wait "${SERVER_PID}" 2>/dev/null || true
  fi
}
trap cleanup EXIT

echo "Starting API server on ${BASE_URL} ..."
.venv/bin/python -m uvicorn app.main:app --host "${HOST}" --port "${PORT}" >/tmp/twinreadmit_ai_demo.log 2>&1 &
SERVER_PID=$!

for _ in $(seq 1 30); do
  if curl -s "${BASE_URL}/health" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

if ! curl -s "${BASE_URL}/health" >/dev/null 2>&1; then
  echo "Error: API server did not become healthy in time."
  echo "Server logs: /tmp/twinreadmit_ai_demo.log"
  exit 1
fi

PATIENT_ID="$(curl -s "${BASE_URL}/patients/high-risk?preset=baseline&limit=1" \
  | .venv/bin/python -c "import json,sys; print(json.load(sys.stdin)['patients'][0]['patient_id'])")"

echo "Using patient_id=${PATIENT_ID}"

RESPONSE_JSON="$(curl -s -X POST "${BASE_URL}/ai/patient-summary" \
  -H "Content-Type: application/json" \
  -d "{\"preset\":\"baseline\",\"patient_id\":\"${PATIENT_ID}\",\"temperature\":0.2,\"max_output_tokens\":500}")"

echo "AI endpoint response:"
echo "${RESPONSE_JSON}" | .venv/bin/python -m json.tool

FALLBACK_USED="$(echo "${RESPONSE_JSON}" | .venv/bin/python -c "import json,sys; print(str(json.load(sys.stdin).get('fallback_used', '')).lower())")"
FALLBACK_REASON="$(echo "${RESPONSE_JSON}" | .venv/bin/python -c "import json,sys; print(json.load(sys.stdin).get('fallback_reason'))")"

echo
echo "fallback_used=${FALLBACK_USED}"
echo "fallback_reason=${FALLBACK_REASON}"

if [[ "${FALLBACK_USED}" == "false" ]]; then
  echo "Success: Real OpenAI path is active."
  exit 0
fi

echo "Warning: Fallback path used. Check fallback_reason and API key/network/model settings."
exit 2
