from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "data" / "datasets"
DEFAULT_SEED = 42


PRESET_CONFIGS = {
    "baseline": {
        "name": "Baseline Hospital Cohort",
        "patient_count": 120,
        "risk_shift": 0.0,
        "social_shift": 0.0,
        "winter_shift": 0.0,
    },
    "winter_surge": {
        "name": "Winter Surge Cohort",
        "patient_count": 140,
        "risk_shift": 0.35,
        "social_shift": 0.1,
        "winter_shift": 0.35,
    },
    "high_social_risk": {
        "name": "High Social Risk Cohort",
        "patient_count": 130,
        "risk_shift": 0.3,
        "social_shift": 0.45,
        "winter_shift": 0.0,
    },
}
