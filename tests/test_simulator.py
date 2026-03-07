import pandas as pd

from app.services.simulator import generate_dataset_bundle, write_dataset_bundle


def test_generate_dataset_bundle_has_expected_shapes() -> None:
    bundle = generate_dataset_bundle("baseline", patient_count=50, seed=7)

    assert bundle.patients.shape[0] == 50
    assert bundle.encounters.shape[0] == 50
    assert bundle.discharge_factors.shape[0] == 50
    assert bundle.vitals_summary.shape[0] == 50
    assert bundle.model_input.shape[0] == 50
    assert 0.0 <= bundle.readmission_rate <= 1.0


def test_generated_tables_join_without_missing_keys(tmp_path) -> None:
    bundle = generate_dataset_bundle("winter_surge", patient_count=60, seed=9)
    outputs = write_dataset_bundle(bundle, root_dir=tmp_path)

    patients = pd.read_csv(outputs["patients"])
    encounters = pd.read_csv(outputs["encounters"])
    discharge = pd.read_csv(outputs["discharge_factors"])
    vitals = pd.read_csv(outputs["vitals_summary"])

    assert set(encounters["patient_id"]) == set(patients["patient_id"])
    assert set(discharge["encounter_id"]) == set(encounters["encounter_id"])
    assert set(vitals["encounter_id"]) == set(encounters["encounter_id"])


def test_high_social_risk_preset_has_higher_average_probability() -> None:
    baseline = generate_dataset_bundle("baseline", patient_count=500, seed=42)
    social = generate_dataset_bundle("high_social_risk", patient_count=500, seed=42)

    assert social.model_input["simulated_readmission_probability"].mean() > baseline.model_input[
        "simulated_readmission_probability"
    ].mean()
