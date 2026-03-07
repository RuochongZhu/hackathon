from fastapi import FastAPI, HTTPException, Query

from app.config import PRESET_CONFIGS
from app.schemas import (
    AIPatientSummaryRequest,
    AIPatientSummaryResponse,
    DatasetArtifact,
    DatasetSummary,
    DatabaseHealthResponse,
    GenerateDatasetRequest,
    ModelTrainingResponse,
    PatientListResponse,
    PatientProfileResponse,
    PredictionSummaryResponse,
    TrainModelRequest,
)
from app.services.ai_summary import generate_patient_summary
from app.services.database import test_database_connection
from app.services.modeling import load_prediction_summary, train_baseline_model
from app.services.repository import (
    PatientNotFoundError,
    PresetNotFoundError,
    get_dashboard_summary,
    get_high_risk_patients,
    get_patient_profile,
    get_similar_cases,
)
from app.services.simulator import generate_dataset_bundle, write_dataset_bundle


app = FastAPI(
    title="TwinReadmit API",
    description="Synthetic readmission-risk API powering the TwinReadmit dashboard and future digital twin workflows.",
    version="0.3.0",
)


@app.get("/")
async def root() -> dict:
    return {
        "message": "TwinReadmit API is running.",
        "available_presets": list(PRESET_CONFIGS),
        "docs": "/docs",
    }


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/database/health", response_model=DatabaseHealthResponse)
async def database_health() -> DatabaseHealthResponse:
    try:
        status = test_database_connection()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database connectivity test failed: {exc}") from exc
    return DatabaseHealthResponse(**status)


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
