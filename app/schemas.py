from typing import Any, List

from pydantic import BaseModel, Field


class GenerateDatasetRequest(BaseModel):
    preset: str = Field(default="baseline", description="Dataset preset name")
    patient_count: int | None = Field(default=None, ge=25, le=1000)
    seed: int = Field(default=42, ge=1, le=100000)


class TrainModelRequest(BaseModel):
    preset: str = Field(default="baseline")
    write_to_db: bool = Field(default=False)


class AIPatientSummaryRequest(BaseModel):
    preset: str = Field(default="baseline")
    patient_id: str = Field(min_length=1)
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    max_output_tokens: int = Field(default=500, ge=100, le=2000)
    timeout_seconds: float = Field(default=20.0, ge=1.0, le=120.0)


class DatasetArtifact(BaseModel):
    name: str
    rows: int
    path: str


class DistributionItem(BaseModel):
    label: str
    value: int


class DatasetSummary(BaseModel):
    preset: str
    title: str
    patient_count: int
    encounter_count: int
    readmission_rate: float
    avg_risk: float | None = None
    high_risk_count: int | None = None
    model_ready: bool | None = None
    high_risk_signals: List[str]
    risk_level_distribution: List[DistributionItem] = Field(default_factory=list)
    diagnosis_distribution: List[DistributionItem] = Field(default_factory=list)
    artifacts: List[DatasetArtifact]


class PatientListItem(BaseModel):
    patient_id: str
    encounter_id: str
    age: int
    diagnosis_group: str
    prior_admissions_12m: int
    severity_score: int
    predicted_readmission_probability: float
    risk_level: str
    recommended_action: str
    readmitted_30d: int
    model_name: str
    model_version: str


class PatientListResponse(BaseModel):
    preset: str
    count: int
    patients: List[PatientListItem]


class SimilarCaseItem(BaseModel):
    patient_id: str
    encounter_id: str
    diagnosis_group: str
    risk_level: str
    predicted_readmission_probability: float
    readmitted_30d: int
    similarity_score: float


class PatientProfileResponse(BaseModel):
    preset: str
    patient_id: str
    encounter_id: str
    risk_score: float
    risk_level: str
    readmitted_30d: int
    model_name: str
    model_version: str
    key_drivers: List[str]
    recommended_actions: List[str]
    overview: dict[str, Any]
    clinical_snapshot: dict[str, Any]
    discharge_factors: dict[str, Any]
    vitals: dict[str, Any]
    cohort_medians: dict[str, float]
    similar_cases: List[SimilarCaseItem]


class ModelTrainingResponse(BaseModel):
    preset: str
    model_name: str
    model_version: str
    train_rows: int
    test_rows: int
    metrics: dict[str, float]
    prediction_rows: int
    artifacts: dict[str, str]
    db_write: dict[str, Any] | None = None


class PredictionSummaryResponse(BaseModel):
    preset: str
    prediction_rows: int
    avg_predicted_risk: float
    high_risk_count: int
    top_patients: List[dict[str, Any]]
    predictions_path: str


class DatabaseHealthResponse(BaseModel):
    configured: bool
    valid: bool
    scheme: str
    message: str
    connected: bool = False
    database: str | None = None
    user: str | None = None


class AISourceModel(BaseModel):
    model_name: str
    model_version: str


class AISummaryContent(BaseModel):
    risk_summary: str
    quantitative_signals: List[str]
    recommended_actions: List[str]
    watchouts: List[str]


class AIPatientSummaryResponse(BaseModel):
    preset: str
    patient_id: str
    source_model: AISourceModel
    llm_model: str
    generated_at: str
    fallback_used: bool
    fallback_reason: str | None = None
    summary: AISummaryContent
