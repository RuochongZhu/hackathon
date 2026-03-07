# TwinReadmit Codebook

## Overview

This project currently ships three small synthetic datasets for the Phase 0/1 MVP scaffold:

- `baseline`
- `winter_surge`
- `high_social_risk`

Each preset writes five CSV files under `data/datasets/<preset>/`.

## Files

### `patients.csv`
- `patient_id`: synthetic patient identifier
- `age`: patient age in years
- `sex`: synthetic sex label
- `chronic_conditions_count`: count of chronic conditions
- `diagnosis_group`: broad diagnosis grouping for the latest encounter
- `insurance_type`: payer category
- `living_alone`: `1` if the patient lives alone, else `0`
- `primary_language`: preferred language category

### `encounters.csv`
- `encounter_id`: synthetic encounter identifier
- `patient_id`: foreign key to `patients.csv`
- `admit_date`: admission date
- `discharge_date`: discharge date
- `length_of_stay`: stay length in days
- `severity_score`: 1–5 acuity score
- `icu_flag`: `1` if ICU was used during the stay, else `0`
- `prior_admissions_12m`: prior inpatient admissions during the last 12 months
- `readmitted_30d`: synthetic outcome label

### `discharge_factors.csv`
- `encounter_id`: foreign key to `encounters.csv`
- `discharge_disposition`: discharge destination category
- `followup_scheduled`: `1` if follow-up was scheduled before discharge
- `medication_complexity`: count-style medication complexity score
- `transportation_barrier`: `1` if transportation issues are present
- `missed_appointments_history`: number of recent missed visits

### `vitals_summary.csv`
- `encounter_id`: foreign key to `encounters.csv`
- `last_temp`: latest temperature before discharge
- `last_oxygen_sat`: latest oxygen saturation percentage
- `last_systolic_bp`: latest systolic blood pressure
- `last_heart_rate`: latest heart rate
- `abnormal_vitals_flag`: derived abnormal vitals indicator

### `model_input.csv`
- Denormalized modeling table created by joining the four source tables
- `simulated_readmission_probability`: latent probability used to generate labels
- `readmitted_30d`: synthetic binary target for later model training

## Preset Logic

### `baseline`
Represents a normal operating environment with moderate utilization and default social risk.

### `winter_surge`
Shifts the cohort toward more pulmonary and infectious disease cases, slightly higher severity, and higher readmission pressure.

### `high_social_risk`
Raises transportation barriers, missed appointments, and lower follow-up scheduling to mimic a more vulnerable discharge population.

## Important Notes

- These files are synthetic and are not derived from real patient records.
- The dataset is intentionally small for hackathon development and testing.
- Labels are generated from internally consistent rules so model behavior is explainable during demo.
