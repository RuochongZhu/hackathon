import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATASETS_DIR = BASE_DIR / "data" / "datasets"
PREDICTIONS_DIR = BASE_DIR / "data" / "predictions"
MODELS_DIR = BASE_DIR / "models"
DEFAULT_SEED = 42

APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATABASE_URL = os.getenv("DATABASE_URL", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY", "")
SUPABASE_HOST = os.getenv("SUPABASE_HOST", "")
SUPABASE_PORT = int(os.getenv("SUPABASE_PORT", "5432"))
SUPABASE_DB = os.getenv("SUPABASE_DB", "postgres")
SUPABASE_USER = os.getenv("SUPABASE_USER", "postgres")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD", "")
MODEL_VERSION = os.getenv("MODEL_VERSION", "baseline-logreg-v1")


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
