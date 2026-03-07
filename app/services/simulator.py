from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from app.config import DATASETS_DIR, DEFAULT_SEED, PRESET_CONFIGS


PATIENT_COLUMNS = [
    "patient_id",
    "age",
    "sex",
    "chronic_conditions_count",
    "diagnosis_group",
    "insurance_type",
    "living_alone",
    "primary_language",
]

ENCOUNTER_COLUMNS = [
    "encounter_id",
    "patient_id",
    "admit_date",
    "discharge_date",
    "length_of_stay",
    "severity_score",
    "icu_flag",
    "prior_admissions_12m",
    "readmitted_30d",
]

DISCHARGE_COLUMNS = [
    "encounter_id",
    "discharge_disposition",
    "followup_scheduled",
    "medication_complexity",
    "transportation_barrier",
    "missed_appointments_history",
]

VITALS_COLUMNS = [
    "encounter_id",
    "last_temp",
    "last_oxygen_sat",
    "last_systolic_bp",
    "last_heart_rate",
    "abnormal_vitals_flag",
]

MODEL_INPUT_COLUMNS = [
    "encounter_id",
    "patient_id",
    "age",
    "sex",
    "chronic_conditions_count",
    "diagnosis_group",
    "insurance_type",
    "living_alone",
    "primary_language",
    "length_of_stay",
    "severity_score",
    "icu_flag",
    "prior_admissions_12m",
    "discharge_disposition",
    "followup_scheduled",
    "medication_complexity",
    "transportation_barrier",
    "missed_appointments_history",
    "last_temp",
    "last_oxygen_sat",
    "last_systolic_bp",
    "last_heart_rate",
    "abnormal_vitals_flag",
    "simulated_readmission_probability",
    "readmitted_30d",
]


@dataclass(frozen=True)
class DatasetBundle:
    preset: str
    title: str
    patients: pd.DataFrame
    encounters: pd.DataFrame
    discharge_factors: pd.DataFrame
    vitals_summary: pd.DataFrame
    model_input: pd.DataFrame

    @property
    def readmission_rate(self) -> float:
        return float(self.encounters["readmitted_30d"].mean())


def logistic(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-values))


def _preset_or_raise(preset: str) -> dict:
    if preset not in PRESET_CONFIGS:
        valid = ", ".join(sorted(PRESET_CONFIGS))
        raise ValueError(f"Unknown preset '{preset}'. Valid presets: {valid}")
    return PRESET_CONFIGS[preset]


def _choice(rng: np.random.Generator, options: list[str], probs: list[float], size: int) -> np.ndarray:
    return rng.choice(options, size=size, p=probs)


def generate_dataset_bundle(
    preset: str,
    patient_count: int | None = None,
    seed: int = DEFAULT_SEED,
) -> DatasetBundle:
    config = _preset_or_raise(preset)
    patient_count = patient_count or config["patient_count"]
    rng = np.random.default_rng(seed)

    patient_ids = [f"P{index:04d}" for index in range(1, patient_count + 1)]
    encounter_ids = [f"E{index:05d}" for index in range(1, patient_count + 1)]

    ages = np.clip(rng.normal(loc=62, scale=16, size=patient_count).round(), 18, 92).astype(int)
    chronic_conditions = np.clip(rng.poisson(lam=2.4 + config["social_shift"], size=patient_count), 0, 8)
    living_alone = rng.binomial(1, np.clip(0.22 + (ages > 74) * 0.16 + config["social_shift"] * 0.18, 0, 0.8))
    severity = np.clip(
        np.round(
            1
            + rng.normal(1.7, 0.85, patient_count)
            + 0.22 * chronic_conditions
            + 0.35 * config["winter_shift"]
        ),
        1,
        5,
    ).astype(int)

    patients = pd.DataFrame(
        {
            "patient_id": patient_ids,
            "age": ages,
            "sex": _choice(rng, ["female", "male"], [0.54, 0.46], patient_count),
            "chronic_conditions_count": chronic_conditions,
            "diagnosis_group": _choice(
                rng,
                ["cardiology", "pulmonary", "endocrine", "infectious_disease", "general_medicine"],
                [0.22, 0.19 + config["winter_shift"] * 0.1, 0.18, 0.12 + config["winter_shift"] * 0.06, 0.29 - config["winter_shift"] * 0.16],
                patient_count,
            ),
            "insurance_type": _choice(rng, ["medicare", "medicaid", "commercial", "self_pay"], [0.42, 0.18, 0.33, 0.07], patient_count),
            "living_alone": living_alone,
            "primary_language": _choice(rng, ["English", "Spanish", "Mandarin", "Other"], [0.74, 0.14, 0.06, 0.06], patient_count),
        }
    )[PATIENT_COLUMNS]

    prior_admissions = np.clip(
        rng.poisson(lam=0.45 + chronic_conditions * 0.38 + config["risk_shift"] * 0.55, size=patient_count),
        0,
        7,
    )
    length_of_stay = np.clip(
        np.round(rng.normal(loc=3.2, scale=1.3, size=patient_count) + severity * 0.95 + chronic_conditions * 0.28),
        1,
        15,
    ).astype(int)
    icu_probability = np.clip(0.04 + severity * 0.06 + config["winter_shift"] * 0.08, 0.04, 0.6)
    icu_flag = rng.binomial(1, icu_probability)

    discharge_base = pd.Timestamp("2025-10-01") + pd.to_timedelta(rng.integers(0, 120, size=patient_count), unit="D")
    admit_date = discharge_base - pd.to_timedelta(length_of_stay, unit="D")

    encounters = pd.DataFrame(
        {
            "encounter_id": encounter_ids,
            "patient_id": patient_ids,
            "admit_date": admit_date.astype(str),
            "discharge_date": discharge_base.astype(str),
            "length_of_stay": length_of_stay,
            "severity_score": severity,
            "icu_flag": icu_flag,
            "prior_admissions_12m": prior_admissions,
        }
    )

    followup_probability = np.clip(
        0.82 - 0.09 * living_alone - 0.12 * config["social_shift"] - 0.03 * prior_admissions,
        0.3,
        0.95,
    )
    transportation_probability = np.clip(0.14 + config["social_shift"] * 0.34 + living_alone * 0.08, 0.08, 0.75)
    missed_appointments = np.clip(
        rng.poisson(lam=0.45 + prior_admissions * 0.22 + config["social_shift"] * 0.9, size=patient_count),
        0,
        6,
    )

    discharge_factors = pd.DataFrame(
        {
            "encounter_id": encounter_ids,
            "discharge_disposition": _choice(rng, ["home", "home_health", "skilled_nursing", "rehab"], [0.58, 0.16, 0.16, 0.10], patient_count),
            "followup_scheduled": rng.binomial(1, followup_probability),
            "medication_complexity": np.clip(rng.poisson(lam=4.0 + chronic_conditions * 0.8, size=patient_count), 1, 18),
            "transportation_barrier": rng.binomial(1, transportation_probability),
            "missed_appointments_history": missed_appointments,
        }
    )[DISCHARGE_COLUMNS]

    oxygen_sat = np.clip(rng.normal(loc=96.4 - severity * 0.55 - config["winter_shift"] * 0.5, scale=1.7, size=patient_count), 84, 100).round(1)
    heart_rate = np.clip(rng.normal(loc=78 + severity * 3.3, scale=8.5, size=patient_count), 55, 138).round().astype(int)
    systolic_bp = np.clip(rng.normal(loc=124 - severity * 1.5, scale=13.0, size=patient_count), 88, 180).round().astype(int)
    temp = np.clip(rng.normal(loc=98.1 + config["winter_shift"] * 0.12, scale=0.7, size=patient_count), 96.0, 102.4).round(1)
    abnormal_vitals_flag = ((oxygen_sat < 92) | (heart_rate > 110) | (temp > 100.4) | (systolic_bp < 95)).astype(int)

    vitals_summary = pd.DataFrame(
        {
            "encounter_id": encounter_ids,
            "last_temp": temp,
            "last_oxygen_sat": oxygen_sat,
            "last_systolic_bp": systolic_bp,
            "last_heart_rate": heart_rate,
            "abnormal_vitals_flag": abnormal_vitals_flag,
        }
    )[VITALS_COLUMNS]

    risk_linear = (
        -4.4
        + (ages >= 75) * 0.5
        + chronic_conditions * 0.22
        + prior_admissions * 0.34
        + severity * 0.24
        + icu_flag * 0.5
        + length_of_stay * 0.08
        + abnormal_vitals_flag * 0.72
        + (1 - discharge_factors["followup_scheduled"].to_numpy()) * 0.48
        + discharge_factors["transportation_barrier"].to_numpy() * 0.52
        + discharge_factors["missed_appointments_history"].to_numpy() * 0.14
        + living_alone * 0.18
        + config["risk_shift"]
    )
    simulated_probability = np.round(logistic(risk_linear), 4)
    readmitted = rng.binomial(1, simulated_probability)
    encounters["readmitted_30d"] = readmitted

    model_input = (
        patients.merge(encounters, on="patient_id", how="inner")
        .merge(discharge_factors, on="encounter_id", how="inner")
        .merge(vitals_summary, on="encounter_id", how="inner")
        .assign(simulated_readmission_probability=simulated_probability)
    )[MODEL_INPUT_COLUMNS]

    return DatasetBundle(
        preset=preset,
        title=config["name"],
        patients=patients,
        encounters=encounters[ENCOUNTER_COLUMNS],
        discharge_factors=discharge_factors,
        vitals_summary=vitals_summary,
        model_input=model_input,
    )


def write_dataset_bundle(bundle: DatasetBundle, root_dir: Path = DATASETS_DIR) -> Dict[str, Path]:
    dataset_dir = root_dir / bundle.preset
    dataset_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "patients": dataset_dir / "patients.csv",
        "encounters": dataset_dir / "encounters.csv",
        "discharge_factors": dataset_dir / "discharge_factors.csv",
        "vitals_summary": dataset_dir / "vitals_summary.csv",
        "model_input": dataset_dir / "model_input.csv",
    }

    bundle.patients.to_csv(outputs["patients"], index=False)
    bundle.encounters.to_csv(outputs["encounters"], index=False)
    bundle.discharge_factors.to_csv(outputs["discharge_factors"], index=False)
    bundle.vitals_summary.to_csv(outputs["vitals_summary"], index=False)
    bundle.model_input.to_csv(outputs["model_input"], index=False)

    return outputs


def load_model_input_summary(preset: str, root_dir: Path = DATASETS_DIR) -> dict:
    model_input_path = root_dir / preset / "model_input.csv"
    if not model_input_path.exists():
        raise FileNotFoundError(f"Dataset preset '{preset}' has not been generated yet")

    df = pd.read_csv(model_input_path)
    high_risk = df.nlargest(3, "simulated_readmission_probability")

    return {
        "preset": preset,
        "title": PRESET_CONFIGS[preset]["name"],
        "patient_count": int(df["patient_id"].nunique()),
        "encounter_count": int(df["encounter_id"].nunique()),
        "readmission_rate": round(float(df["readmitted_30d"].mean()), 4),
        "high_risk_signals": [
            f"{row.patient_id}: {row.simulated_readmission_probability:.1%} predicted risk"
            for row in high_risk.itertuples()
        ],
        "artifacts": [
            {
                "name": file_name,
                "rows": int(pd.read_csv(root_dir / preset / file_name).shape[0]),
                "path": str(root_dir / preset / file_name),
            }
            for file_name in [
                "patients.csv",
                "encounters.csv",
                "discharge_factors.csv",
                "vitals_summary.csv",
                "model_input.csv",
            ]
        ],
    }
