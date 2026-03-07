-- Run in Supabase SQL Editor to enable prediction persistence.
create table if not exists public.readmission_predictions (
    preset text not null,
    encounter_id text not null,
    patient_id text not null,
    predicted_readmission_probability double precision not null,
    predicted_label integer not null,
    risk_level text not null,
    model_name text not null,
    model_version text not null,
    generated_at timestamptz not null,
    primary key (preset, encounter_id)
);
