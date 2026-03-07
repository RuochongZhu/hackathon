from fastapi import FastAPI, HTTPException

from app.config import PRESET_CONFIGS
from app.schemas import DatasetArtifact, DatasetSummary, GenerateDatasetRequest
from app.services.simulator import generate_dataset_bundle, load_model_input_summary, write_dataset_bundle


app = FastAPI(
    title="TwinReadmit API",
    description="Phase 0/1 scaffold for synthetic readmission-risk datasets and future digital twin workflows.",
    version="0.1.0",
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
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    summary = load_model_input_summary(request.preset)
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


@app.get("/dashboard/summary", response_model=DatasetSummary)
async def dashboard_summary(preset: str = "baseline") -> DatasetSummary:
    try:
        summary = load_model_input_summary(preset)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"Unknown preset '{preset}'") from exc
    return DatasetSummary(**summary)
