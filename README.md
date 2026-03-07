# Readmission Hackathon Developer Notes

## Project Direction

### Selected Prompt
Prompt 2 — Digital Health: Patient Digital Twins

### Current Focus
We are using **30-day readmission prediction** as the core function of the project.

### Product Goal
Build an **AI-powered hospital decision-support tool** that uses synthetic patient data to:

- predict 30-day readmission risk
- identify high-risk patients
- generate patient digital twin profiles
- compare a patient with similar historical cases
- generate AI summaries and recommended next steps for hospital decision-makers

### Primary Stakeholders
- hospital operations managers
- discharge planning teams
- care coordination staff
- clinical administrators

### Core User Question
Which patients are at highest risk of being readmitted within 30 days after discharge?

---

## MVP Scope

To keep the project realistic for a Hackathon, the MVP will focus on the following:

### Must Have
- synthetic patient dataset
- readmission prediction model
- high-risk patient ranking
- patient digital twin profile page
- AI-generated risk summary
- AI-generated recommended actions

### Nice to Have
- similar historical case comparison
- natural language query interface
- hospital-wide summary dashboard

### Out of Scope for Now
- ICU forecasting as a core module
- appointment no-show prediction
- highly complex clinical simulation
- advanced real-time streaming architecture

---

## System Overview

The project will follow this workflow:

1. generate synthetic patient data
2. store the data in a structured database
3. train a readmission prediction model
4. write predictions back into the system
5. retrieve patient-level results
6. use AI to generate summaries and recommendations
7. display results in a dashboard / patient profile UI

---

## Recommended Tech Stack

### Frontend
- Streamlit or Python Shiny

### Backend
- FastAPI

### Database
- Supabase PostgreSQL

### Model Layer
- Logistic Regression for baseline
- XGBoost as the main model

### AI Layer
- OpenAI API for:
  - patient risk summaries
  - recommended interventions
  - similar-case explanation

### Deployment
- one deployed frontend
- one deployed backend API

---

## Core Data Model

We currently plan to use four main tables.

### 1. patients
Stores patient demographic and baseline information.

Suggested fields:
- patient_id
- age
- sex
- chronic_conditions_count
- diagnosis_group
- insurance_type
- living_alone
- primary_language

### 2. encounters
Stores hospital admission and discharge history.

Suggested fields:
- encounter_id
- patient_id
- admit_date
- discharge_date
- length_of_stay
- severity_score
- icu_flag
- prior_admissions_12m
- readmitted_30d

### 3. discharge_factors
Stores discharge-related risk factors.

Suggested fields:
- encounter_id
- discharge_disposition
- followup_scheduled
- medication_complexity
- transportation_barrier
- missed_appointments_history

### 4. vitals_summary
Stores the latest patient condition snapshot before discharge.

Suggested fields:
- encounter_id
- last_temp
- last_oxygen_sat
- last_systolic_bp
- last_heart_rate
- abnormal_vitals_flag

### Optional 5. predictions
Stores model outputs.

Suggested fields:
- encounter_id
- predicted_readmission_probability
- risk_level
- generated_at

---

## Synthetic Data Design Logic

The synthetic data should not be purely random. It should reflect reasonable healthcare patterns.

### Factors that should increase readmission risk
- older age
- more chronic conditions
- more prior admissions in the last 12 months
- longer length of stay
- ICU stay
- abnormal vitals near discharge
- no follow-up scheduled
- transportation barriers
- more missed appointments
- living alone
- higher severity score
- more complex discharge medication profile

### Data Generation Strategy
Recommended process:

1. generate patient baseline records
2. generate encounter records linked to patients
3. generate discharge and vitals factors
4. compute a latent risk score using defined rules
5. convert that risk score into a readmitted_30d label
6. train the model on the resulting dataset

This makes the dataset internally consistent and easier to explain during demo.

---

## Modeling Plan

### Primary Objective
Predict whether a patient will be readmitted within 30 days.

### Baseline Model
Logistic Regression

Reason:
- simple
- fast
- interpretable
- good for baseline comparison

### Main Model
XGBoost

Reason:
- performs well on structured tabular data
- handles nonlinear relationships
- gives stronger predictive performance for demo purposes

### Model Output
For each patient encounter, return:
- readmission probability
- risk level: low / medium / high
- major contributing factors

### Evaluation
Since this is synthetic data, the most important thing is not perfect realism but:
- consistent risk ranking
- reasonable feature behavior
- interpretable outputs
- a good demo story

Possible evaluation metrics:
- accuracy
- precision
- recall
- AUC
- confusion matrix

---

## Similar Case Retrieval Plan

This module helps support the “digital twin” idea.

### Goal
For a selected patient, retrieve the most similar historical cases.

### Suggested features for similarity
- age
- chronic_conditions_count
- prior_admissions_12m
- severity_score
- abnormal_vitals_flag
- length_of_stay
- diagnosis_group

### Suggested method
- normalize selected features
- use Euclidean distance or cosine similarity
- return top 3 most similar historical cases

### Output
- similar patient IDs
- similarity reasoning
- whether those historical cases were readmitted

This can later be passed into the AI layer for narrative comparison.

---

## AI Layer Design

The AI layer should not directly do prediction. The model handles prediction.

The AI layer should turn structured outputs into readable decision-support text.

### AI Inputs
- patient demographic summary
- encounter summary
- predicted readmission probability
- risk level
- key risk drivers
- similar cases
- discharge barriers

### AI Outputs
#### 1. Risk Summary
A short explanation of why the patient is high or low risk.

#### 2. Key Drivers
A concise description of the main factors driving the score.

#### 3. Recommended Actions
Examples:
- schedule follow-up before discharge
- assign case manager outreach
- perform medication reconciliation
- support transportation planning
- arrange post-discharge monitoring

### Design Principle
AI should act as an explanation and action layer, not as the core predictor.

---

## Frontend Plan

The UI should be kept simple and demo-friendly.

### Page 1: Hospital Overview
Purpose:
Show the overall readmission risk picture.

Possible components:
- total patients
- number of high-risk patients
- average readmission risk
- diagnosis group distribution
- risk level distribution
- top risk factors

### Page 2: High-Risk Patient Explorer
Purpose:
Let users browse and rank patients by risk.

Possible columns:
- patient_id
- age
- diagnosis_group
- prior_admissions_12m
- predicted_readmission_probability
- risk_level
- recommended_action

Possible interactions:
- filter by risk level
- sort by probability
- filter by diagnosis
- click into patient detail

### Page 3: Patient Digital Twin Profile
Purpose:
Show the full patient-level decision-support view.

Possible sections:
- patient demographics
- recent encounter summary
- discharge factors
- vitals snapshot
- readmission score
- key drivers
- similar cases
- AI summary
- recommended actions

This is likely the most important demo page.

---

## Backend API Plan

Suggested API endpoints:

### POST /generate-data
Generate synthetic patient data.

### POST /train-model
Train the readmission prediction model and save outputs.

### GET /dashboard/summary
Return high-level summary metrics for the overview dashboard.

### GET /patients/high-risk
Return high-risk patient list, sorted by risk score.

### GET /patients/{patient_id}/profile
Return a full digital twin profile for the selected patient.

### GET /patients/{patient_id}/similar-cases
Return top similar historical cases.

### POST /ai/patient-summary
Generate AI summary and recommended actions for a patient.

### POST /query
Optional natural language query endpoint.

---

## End-to-End Workflow

### Data Flow
1. synthetic generator creates patient datasets
2. datasets are loaded into Supabase/Postgres
3. model training script reads the data
4. model produces readmission predictions
5. predictions are stored in the database
6. backend serves data to frontend
7. AI layer generates summaries from structured results
8. frontend displays insights to the user

### User Flow
1. user opens dashboard
2. user sees high-level risk overview
3. user opens high-risk patient explorer
4. user selects a patient
5. user views digital twin profile
6. user reads AI-generated summary and recommended next steps

---

## Development Priorities

The team should build in this order.

### Phase 1 — Lock Scope
Finalize:
- project name
- user story
- MVP boundary
- data tables
- model target

### Phase 2 — Build Synthetic Data
Create:
- patient records
- encounter records
- discharge factors
- vitals summaries
- labels for readmitted_30d

### Phase 3 — Train Baseline Model
Implement:
- feature preparation
- logistic regression baseline
- XGBoost main model
- prediction outputs

### Phase 4 — Store Predictions
Create a prediction table and save risk outputs for each encounter.

### Phase 5 — Build Core APIs
Implement:
- dashboard summary
- high-risk patient list
- patient profile
- similar cases

### Phase 6 — Add AI Layer
Implement:
- prompt design
- summary format
- recommendations format

### Phase 7 — Build Frontend
Create:
- overview page
- patient explorer
- patient profile page

### Phase 8 — Final Demo Polish
Prepare:
- cleaner charts
- sample patients
- clear storytelling
- README
- codebook

---

## Immediate Next Steps

These are the next concrete tasks the team should do now.

### Task 1
Finalize the schema for:
- patients
- encounters
- discharge_factors
- vitals_summary
- predictions

### Task 2
Write the synthetic data generation script.

### Task 3
Define the label-generation logic for `readmitted_30d`.

### Task 4
Prepare a baseline model training notebook or script.

### Task 5
Define the API contract between frontend and backend.

### Task 6
Decide the frontend framework:
- Streamlit
or
- Python Shiny

### Task 7
Draft the AI prompt template for patient summary generation.

---

## Current Scaffold Status

### Phase 0 / Phase 1 Completed
- FastAPI scaffold is prepared in `app/`
- synthetic dataset generator is prepared in `app/services/simulator.py`
- small demo datasets are generated under `data/datasets/`
- codebook is documented in `docs/codebook.md`
- initial tests are available in `tests/test_simulator.py`

### Quick Start

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Generate demo datasets:

```bash
python scripts/generate_datasets.py
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Useful endpoints:
- `GET /`
- `GET /health`
- `GET /datasets`
- `POST /generate-data`
- `GET /dashboard/summary?preset=baseline`
- `GET /patients/high-risk?preset=baseline&limit=1`
- `POST /ai/patient-summary`
- `GET /mosaic-data?preset=baseline` — aggregated counts for mosaic plot (diagnosis_group × risk_level × readmitted_30d)

Optional — React mosaic plot dashboard (separate UI, no conflict with Shiny):

```bash
cd frontend && npm install && npm run dev
```

Then open http://localhost:3000. Ensure the API is running on port 8000.

### GenAI Integration Endpoint

`POST /ai/patient-summary` converts existing model outputs into an AI-generated clinical decision-support summary.

Important guardrails:
- Uses existing structured outputs (`risk_score`, `key_drivers`, `recommended_actions`, `similar_cases`) as context
- Does not re-predict risk; it explains current model output and proposes actions
- If OpenAI is unavailable, automatic deterministic fallback is returned with:
  - `fallback_used: true`
  - `fallback_reason: <reason_code>`

Example request:

```bash
curl -s -X POST "http://127.0.0.1:8000/ai/patient-summary" \
  -H "Content-Type: application/json" \
  -d '{
    "preset": "baseline",
    "patient_id": "P0001",
    "temperature": 0.2,
    "max_output_tokens": 500
  }'
```

Expected response keys:
- `source_model`
- `llm_model`
- `generated_at`
- `fallback_used`
- `fallback_reason`
- `summary` (`risk_summary`, `quantitative_signals`, `recommended_actions`, `watchouts`)

---

## Suggested Team Split

### Data Engineer
- schema design
- synthetic data generation
- codebook

### ML Engineer
- feature engineering
- model training
- prediction outputs
- evaluation

### Backend Engineer
- FastAPI
- database connection
- endpoints
- AI request handling

### Frontend Engineer
- dashboard
- patient explorer
- digital twin profile UI

### Product / Demo Lead
- README
- demo script
- prompt wording
- stakeholder framing
- final presentation flow

---

## Demo Narrative

A clean demo should follow this story:

1. show the hospital overview
2. show how the system identifies high-risk patients
3. click one patient and open the digital twin profile
4. explain the risk score and major drivers
5. compare that patient with similar historical cases
6. show the AI-generated summary and recommended actions

### Demo Script (API)

1. Start API server: `uvicorn app.main:app --reload`
2. Fetch one high-risk patient ID:
   - `GET /patients/high-risk?preset=baseline&limit=1`
3. Call `POST /ai/patient-summary` for that patient.
4. Confirm scoring evidence:
   - `fallback_used` is `false` (real OpenAI path)
   - response includes actionable recommendations and quantitative signals
5. Reliability check (optional): unset `OPENAI_API_KEY` and call again to show deterministic fallback with `fallback_used=true`.

### Demo Message
The system is not just predicting risk.  
It is helping hospital decision-makers understand which patients need attention and why.

---

## Working Project Definition

### Project Name Ideas
- ReadmitIQ
- TwinCare AI
- CareTwin
- DischargeSignal
- TwinRisk Health

### One-Sentence Description
An AI-powered hospital decision-support platform that predicts 30-day readmission risk using synthetic patient digital twins and generates actionable summaries for care teams.

---

## Notes for README Later
The final README should include:
- project overview
- stakeholder need
- system architecture
- data schema
- setup instructions
- how to run backend
- how to run frontend
- sample queries
- explanation of AI usage
- limitations
- future work


### Phase 2 API additions

- `GET /api/database/health`
- `POST /api/train-model`
- `GET /api/predictions/summary?preset=baseline`
