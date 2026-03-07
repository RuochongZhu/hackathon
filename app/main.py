import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import PRESET_CONFIGS
from app.schemas import (
    AIPatientSummaryRequest,
    AIPatientSummaryResponse,
    AuditResponse,
    DatasetArtifact,
    DatasetSummary,
    DatabaseHealthResponse,
    GenerateDatasetRequest,
    IntegrationStatusResponse,
    ModelTrainingResponse,
    PatientListResponse,
    PatientProfileResponse,
    PredictionSummaryResponse,
    TrainModelRequest,
)
from app.services.ai_summary import generate_patient_summary
from app.services.audit import run_system_audit
from app.services.database import test_database_connection
from app.services.integrations import database_status, llm_status
from app.services.modeling import load_prediction_summary, train_baseline_model
from app.services.repository import (
    PatientNotFoundError,
    PresetNotFoundError,
    get_boxplot_data,
    get_dashboard_summary,
    get_high_risk_patients,
    get_mosaic_data,
    get_patient_profile,
    get_similar_cases,
)
from app.services.simulator import generate_dataset_bundle, write_dataset_bundle


app = FastAPI(
    title="TwinReadmit API",
    description="Synthetic readmission-risk API powering the TwinReadmit dashboard and future digital twin workflows.",
    version="0.3.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict:
    revision = os.getenv("APP_REVISION", "").strip()
    return {
        "message": "TwinReadmit API is running.",
        "available_presets": list(PRESET_CONFIGS),
        "docs": "/docs",
        "revision": revision[:12] if revision else "local",
    }


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/database/health", response_model=DatabaseHealthResponse)
async def database_health() -> DatabaseHealthResponse:
    status = database_status(live_check=True)
    return DatabaseHealthResponse(**status)


@app.get("/integrations/llm", response_model=IntegrationStatusResponse)
async def integrations_llm(live_check: bool = Query(default=False)) -> IntegrationStatusResponse:
    return IntegrationStatusResponse(**llm_status(live_check=live_check))


@app.get("/audit/system", response_model=AuditResponse)
async def audit_system(
    preset: str = Query(default="baseline"),
    live_checks: bool = Query(default=False),
) -> AuditResponse:
    try:
        report = run_system_audit(preset=preset, live_checks=live_checks)
    except PresetNotFoundError as exc:
        raise HTTPException(status_code=400, detail=f"Unknown preset '{preset}'") from exc
    return AuditResponse(**report)


@app.get("/datasets")
async def list_datasets() -> dict:
    return {
        "presets": [
            {"preset": preset, "title": config["name"], "default_patient_count": config["patient_count"]}
            for preset, config in PRESET_CONFIGS.items()
        ]
    }


@app.post("/generate-data", response_model=DatasetSummary)
async def generate_data(request: GenerateDatasetRequest) -> DatasetSummary:
    try:
        bundle = generate_dataset_bundle(
            preset=request.preset,
            patient_count=request.patient_count,
            seed=request.seed,
        )
        output_paths = write_dataset_bundle(bundle)
        summary = get_dashboard_summary(request.preset)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    summary["artifacts"] = [
        DatasetArtifact(name=key, rows=value_rows["rows"], path=value_rows["path"])
        for key, value_rows in {
            file_key: {
                "rows": bundle.model_input.shape[0] if file_key == "model_input" else getattr(bundle, file_key).shape[0],
                "path": str(path),
            }
            for file_key, path in output_paths.items()
        }.items()
    ]
    return DatasetSummary(**summary)


@app.post("/train-model", response_model=ModelTrainingResponse)
async def train_model(request: TrainModelRequest) -> ModelTrainingResponse:
    try:
        result = train_baseline_model(request.preset, write_to_db=request.write_to_db)
    except PresetNotFoundError as exc:
        raise HTTPException(status_code=400, detail=f"Unknown preset '{request.preset}'") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ModelTrainingResponse(**result)


@app.get("/predictions/summary", response_model=PredictionSummaryResponse)
async def predictions_summary(preset: str = "baseline") -> PredictionSummaryResponse:
    try:
        summary = load_prediction_summary(preset)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return PredictionSummaryResponse(**summary)


@app.get("/dashboard/summary", response_model=DatasetSummary)
async def dashboard_summary(preset: str = "baseline") -> DatasetSummary:
    try:
        summary = get_dashboard_summary(preset)
    except PresetNotFoundError as exc:
        raise HTTPException(status_code=400, detail=f"Unknown preset '{preset}'") from exc
    return DatasetSummary(**summary)


@app.get("/mosaic-data")
async def mosaic_data(preset: str = "baseline") -> dict:
    """Aggregated counts by diagnosis_group, risk_level, readmitted_30d for mosaic plot."""
    try:
        return get_mosaic_data(preset)
    except PresetNotFoundError as exc:
        raise HTTPException(status_code=400, detail=f"Unknown preset '{preset}'") from exc


@app.get("/boxplot-data")
async def boxplot_data(preset: str = "baseline") -> dict:
    """Raw rows for box plot: group and numeric columns for 30-day readmission cohort."""
    try:
        return get_boxplot_data(preset)
    except PresetNotFoundError as exc:
        raise HTTPException(status_code=400, detail=f"Unknown preset '{preset}'") from exc


@app.get("/patients/high-risk", response_model=PatientListResponse)
async def patients_high_risk(
    preset: str = "baseline",
    limit: int = Query(default=15, ge=1, le=50),
    diagnosis_group: str | None = Query(default=None),
    risk_level: str | None = Query(default=None),
) -> PatientListResponse:
    try:
        patients = get_high_risk_patients(
            preset=preset,
            limit=limit,
            diagnosis_group=diagnosis_group,
            risk_level=risk_level,
        )
    except PresetNotFoundError as exc:
        raise HTTPException(status_code=400, detail=f"Unknown preset '{preset}'") from exc

    return PatientListResponse(preset=preset, count=len(patients), patients=patients)


@app.get("/patients/{patient_id}/profile", response_model=PatientProfileResponse)
async def patient_profile(preset: str, patient_id: str) -> PatientProfileResponse:
    try:
        profile = get_patient_profile(preset=preset, patient_id=patient_id)
    except PresetNotFoundError as exc:
        raise HTTPException(status_code=400, detail=f"Unknown preset '{preset}'") from exc
    except PatientNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown patient '{patient_id}'") from exc

    return PatientProfileResponse(**profile)


@app.get("/patients/{patient_id}/similar-cases")
async def patient_similar_cases(
    preset: str,
    patient_id: str,
    limit: int = Query(default=3, ge=1, le=10),
) -> dict:
    try:
        similar_cases = get_similar_cases(preset=preset, patient_id=patient_id, limit=limit)
    except PresetNotFoundError as exc:
        raise HTTPException(status_code=400, detail=f"Unknown preset '{preset}'") from exc
    except PatientNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown patient '{patient_id}'") from exc

    return {"preset": preset, "patient_id": patient_id, "similar_cases": similar_cases}


@app.post("/ai/patient-summary", response_model=AIPatientSummaryResponse)
async def ai_patient_summary(request: AIPatientSummaryRequest) -> AIPatientSummaryResponse:
    try:
        summary = generate_patient_summary(
            preset=request.preset,
            patient_id=request.patient_id,
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
            timeout_seconds=request.timeout_seconds,
        )
    except PresetNotFoundError as exc:
        raise HTTPException(status_code=400, detail=f"Unknown preset '{request.preset}'") from exc
    except PatientNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown patient '{request.patient_id}'") from exc

    return AIPatientSummaryResponse(**summary)
