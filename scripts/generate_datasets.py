from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from app.config import PRESET_CONFIGS
from app.services.simulator import generate_dataset_bundle, write_dataset_bundle


def main() -> None:
    for preset, config in PRESET_CONFIGS.items():
        bundle = generate_dataset_bundle(preset=preset, patient_count=config["patient_count"], seed=42)
        outputs = write_dataset_bundle(bundle)
        print(
            f"Generated {preset}: patients={bundle.patients.shape[0]}, "
            f"readmission_rate={bundle.readmission_rate:.1%}, files={len(outputs)}"
        )


if __name__ == "__main__":
    main()
