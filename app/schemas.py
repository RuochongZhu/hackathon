from typing import List

from pydantic import BaseModel, Field


class GenerateDatasetRequest(BaseModel):
    preset: str = Field(default="baseline", description="Dataset preset name")
    patient_count: int | None = Field(default=None, ge=25, le=1000)
    seed: int = Field(default=42, ge=1, le=100000)


class DatasetArtifact(BaseModel):
    name: str
    rows: int
    path: str


class DatasetSummary(BaseModel):
    preset: str
    title: str
    patient_count: int
    encounter_count: int
    readmission_rate: float
    high_risk_signals: List[str]
    artifacts: List[DatasetArtifact]

