# TwinReadmit Phase 0/1

## What is implemented now

- FastAPI scaffold with health and dataset endpoints
- Deterministic synthetic data generator for three preset cohorts
- Small CSV artifacts aligned with the root `README.md` schema direction
- Initial tests for dataset integrity and preset risk behavior

## Immediate next phase

1. Train the baseline readmission model on `model_input.csv`
2. Add prediction storage and patient profile endpoints
3. Add AI summary generation on top of structured outputs

## Human setup checklist

- Create `OpenAI` API key
- Create `Supabase` project and capture connection info
- Create `DigitalOcean App Platform` app target
- Create `GitHub` repository for deployment
