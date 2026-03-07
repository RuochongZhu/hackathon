from __future__ import annotations

import pandas as pd
import shinyswatch
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, render_widget

from app.config import PRESET_CONFIGS
from app.services.ai_summary import generate_patient_summary
from app.services.repository import (
    get_dashboard_summary,
    get_high_risk_patients,
    get_patient_profile,
    list_patient_ids,
    load_model_input,
)
from dashboard.charts import (
    cohort_comparison_figure,
    diagnosis_mix_figure,
    explorer_bar_figure,
    gauge_figure,
    risk_distribution_figure,
    similar_cases_figure,
)
from dashboard.styles import CUSTOM_CSS

RISK_CHOICES = {"all": "All risk tiers", "high": "High", "medium": "Medium", "low": "Low"}


app_ui = ui.page_fillable(
    ui.tags.head(
        ui.tags.style(CUSTOM_CSS),
        ui.tags.link(rel="preconnect", href="https://fonts.googleapis.com"),
        ui.tags.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        ui.tags.link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
        ),
    ),
    ui.div(
        {"class": "hero-shell"},
        ui.div(
            {"class": "hero-panel"},
            ui.div({"class": "hero-title"}, "TwinReadmit — Patient Digital Twin Command Center"),
            ui.div(
                {"class": "hero-subtitle"},
                "A polished, interactive decision-support workspace for readmission risk, patient exploration, and digital twin triage. Built to stay hackathon-fast today and maintainable for deeper expert refinement tomorrow.",
            ),
        ),
    ),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "preset",
                "Cohort scenario",
                {preset: config["name"] for preset, config in PRESET_CONFIGS.items()},
                selected="baseline",
            ),
            ui.output_ui("diagnosis_filter_ui"),
            ui.input_select("risk_filter", "Risk tier", RISK_CHOICES, selected="all"),
            ui.input_slider("top_n", "Explorer rows", min=5, max=25, value=12),
            ui.output_ui("patient_selector_ui"),
            ui.markdown(
                """**Demo posture**  
- API-first backend  
- dynamic Shiny interface  
- synthetic but structured hospital cohorts  
- ready for model + GenAI upgrades"""
            ),
            width=360,
            open="desktop",
        ),
        ui.navset_card_tab(
            ui.nav_panel(
                "Overview",
                ui.output_ui("metric_cards"),
                ui.layout_columns(
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Risk tier distribution"),
                        output_widget("risk_distribution_plot"),
                    ),
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Diagnosis mix"),
                        output_widget("diagnosis_mix_plot"),
                    ),
                    col_widths=[6, 6],
                ),
                ui.layout_columns(
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Immediate watchlist"),
                        ui.output_ui("high_risk_signals_ui"),
                    ),
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Cohort framing"),
                        ui.output_ui("cohort_story_ui"),
                    ),
                    col_widths=[6, 6],
                ),
            ),
            ui.nav_panel(
                "Explorer",
                ui.layout_columns(
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Risk-ranked patient explorer"),
                        ui.output_data_frame("patient_table"),
                    ),
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Top patient risk profile"),
                        output_widget("explorer_plot"),
                    ),
                    col_widths=[7, 5],
                ),
            ),
            ui.nav_panel(
                "Digital Twin",
                ui.layout_columns(
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Patient risk gauge"),
                        output_widget("risk_gauge_plot"),
                    ),
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Patient vs cohort median"),
                        output_widget("cohort_comparison_plot"),
                    ),
                    col_widths=[5, 7],
                ),
                ui.output_ui("profile_ui"),
                ui.layout_columns(
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Why this patient is risky"),
                        ui.output_ui("drivers_ui"),
                    ),
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Suggested next actions"),
                        ui.output_ui("actions_ui"),
                    ),
                    col_widths=[6, 6],
                ),
                ui.layout_columns(
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Closest historical analogs"),
                        output_widget("similar_cases_plot"),
                    ),
                    ui.div(
                        {"class": "panel-card"},
                        ui.div({"class": "section-title"}, "Similar case detail"),
                        ui.output_ui("similar_cases_ui"),
                    ),
                    col_widths=[6, 6],
                ),
                ui.div(
                    {"class": "panel-card"},
                    ui.layout_columns(
                        ui.div({"class": "section-title"}, "AI care-team summary"),
                        ui.div(
                            ui.input_action_button("refresh_ai_summary", "Regenerate AI Summary"),
                            style="display:flex; justify-content:flex-end;",
                        ),
                        col_widths=[9, 3],
                    ),
                    ui.output_ui("ai_summary_ui"),
                ),
            ),
        ),
    ),
    title="TwinReadmit Dashboard",
    fillable=True,
    theme=shinyswatch.theme.cyborg(),
)


def risk_badge(level: str):
    return ui.span({"class": f"badge badge-{level}"}, level.upper())


def server(input, output, session):
    @reactive.calc
    def selected_patient_id() -> str:
        patient_id = input.patient_id()
        if patient_id:
            return patient_id
        ids = list_patient_ids(input.preset())
        return ids[0]

    @reactive.calc
    def cohort_df() -> pd.DataFrame:
        return load_model_input(input.preset())

    @reactive.calc
    def summary() -> dict:
        return get_dashboard_summary(input.preset())

    @reactive.calc
    def diagnosis_choices() -> dict[str, str]:
        df = cohort_df()
        diagnoses = sorted(df["diagnosis_group"].unique().tolist())
        return {"all": "All diagnoses", **{value: value.replace("_", " ").title() for value in diagnoses}}

    @output
    @render.ui
    def diagnosis_filter_ui():
        return ui.input_select("diagnosis_filter", "Diagnosis focus", diagnosis_choices(), selected="all")

    @reactive.calc
    def filtered_patients() -> pd.DataFrame:
        rows = get_high_risk_patients(
            preset=input.preset(),
            limit=input.top_n(),
            diagnosis_group=input.diagnosis_filter(),
            risk_level=input.risk_filter(),
        )
        return pd.DataFrame(rows)

    @reactive.effect
    def _update_patient_selector():
        patient_ids = list_patient_ids(input.preset())
        preferred = patient_ids[0] if patient_ids else None
        if not filtered_patients().empty:
            preferred = filtered_patients().iloc[0]["patient_id"]
        ui.update_selectize("patient_id", choices=patient_ids, selected=preferred)

    @output
    @render.ui
    def patient_selector_ui():
        return ui.input_selectize("patient_id", "Digital twin focus", choices=list_patient_ids(input.preset()), selected=None)

    @reactive.calc
    def profile() -> dict:
        return get_patient_profile(input.preset(), selected_patient_id())

    @reactive.calc
    def ai_summary_response() -> dict:
        # Button clicks invalidate this reactive value and regenerate the summary.
        _ = input.refresh_ai_summary()
        try:
            return generate_patient_summary(
                preset=input.preset(),
                patient_id=selected_patient_id(),
                temperature=0.2,
                max_output_tokens=500,
                timeout_seconds=20.0,
            )
        except Exception as exc:
            return {
                "preset": input.preset(),
                "patient_id": selected_patient_id(),
                "error": str(exc),
            }

    @output
    @render.ui
    def metric_cards():
        data = summary()
        cards = [
            ("Patients", f"{data['patient_count']}", data["title"]),
            ("High-risk", f"{data['high_risk_count']}", "Priority queue for care management"),
            ("Avg predicted risk", f"{data['avg_risk']:.1%}", "Mean cohort risk score"),
            ("Model status", "READY" if data.get("model_ready") else "SIM ONLY", "Logistic baseline trained" if data.get("model_ready") else "Using latent simulation risk"),
        ]
        return ui.div(
            {"class": "metric-grid"},
            *[
                ui.div(
                    {"class": "metric-card"},
                    ui.div({"class": "metric-label"}, label),
                    ui.div({"class": "metric-value"}, value),
                    ui.div({"class": "metric-footnote"}, footnote),
                )
                for label, value, footnote in cards
            ],
        )

    @output
    @render.ui
    def high_risk_signals_ui():
        return ui.tags.ul(
            {"class": "signal-list"},
            *[ui.tags.li({"class": "signal-item"}, signal) for signal in summary()["high_risk_signals"]],
        )

    @output
    @render.ui
    def cohort_story_ui():
        df = cohort_df()
        diagnosis = df["diagnosis_group"].mode().iat[0].replace("_", " ").title()
        followup_gap = float((1 - df["followup_scheduled"].mean()) * 100)
        barrier_share = float(df["transportation_barrier"].mean() * 100)
        return ui.tags.ul(
            {"class": "signal-list"},
            ui.tags.li({"class": "signal-item"}, f"Most common diagnosis group: {diagnosis}.") ,
            ui.tags.li({"class": "signal-item"}, f"{followup_gap:.0f}% of patients leave without documented follow-up scheduling."),
            ui.tags.li({"class": "signal-item"}, f"{barrier_share:.0f}% of the cohort carries a transportation barrier signal."),
        )

    @output
    @render_widget
    def risk_distribution_plot():
        return risk_distribution_figure(summary()["risk_level_distribution"])

    @output
    @render_widget
    def diagnosis_mix_plot():
        return diagnosis_mix_figure(summary()["diagnosis_distribution"])

    @output
    @render.data_frame
    def patient_table():
        df = filtered_patients().copy()
        if df.empty:
            return render.DataGrid(pd.DataFrame({"message": ["No patients match the current filters."]}), row_selection_mode="none")

        display = df.rename(
            columns={
                "predicted_readmission_probability": "predicted_risk",
                "prior_admissions_12m": "prior_adm_12m",
            }
        )
        display["predicted_risk"] = display["predicted_risk"].map(lambda value: f"{value:.1%}")
        return render.DataGrid(display, filters=True, summary=False, width="100%")

    @output
    @render_widget
    def explorer_plot():
        df = filtered_patients()
        if df.empty:
            fallback = cohort_df().copy()
            fallback["predicted_readmission_probability"] = fallback["active_risk_probability"]
            return explorer_bar_figure(fallback.nlargest(1, "predicted_readmission_probability"))
        return explorer_bar_figure(df)

    @output
    @render_widget
    def risk_gauge_plot():
        data = profile()
        return gauge_figure(data["risk_score"], data["risk_level"])

    @output
    @render_widget
    def cohort_comparison_plot():
        return cohort_comparison_figure(profile())

    @output
    @render_widget
    def similar_cases_plot():
        return similar_cases_figure(profile()["similar_cases"])

    @output
    @render.ui
    def profile_ui():
        data = profile()
        overview = data["overview"]
        clinical = data["clinical_snapshot"]
        discharge = data["discharge_factors"]
        vitals = data["vitals"]

        def kv_section(title: str, mapping: dict):
            return ui.div(
                {"class": "profile-card"},
                ui.div({"class": "section-title"}, title),
                ui.div(
                    {"class": "kv-grid"},
                    *[
                        ui.div(
                            {"class": "kv-item"},
                            ui.div({"class": "kv-label"}, key.replace("_", " ")),
                            ui.div({"class": "kv-value"}, str(value)),
                        )
                        for key, value in mapping.items()
                    ],
                ),
            )

        return ui.div(
            {"class": "profile-grid"},
            ui.div(
                {"class": "profile-card"},
                ui.div({"class": "section-title"}, f"Patient {data['patient_id']} · Encounter {data['encounter_id']}"),
                ui.div(risk_badge(data["risk_level"])),
                ui.div(
                    {"style": "margin-top: 0.9rem; color: #bfd2fb;"},
                    f"Observed readmission label: {data['readmitted_30d']} · This profile is driven by structured clinical, discharge, and social-risk factors.",
                ),
            ),
            ui.div(
                {"class": "profile-card"},
                ui.div({"class": "section-title"}, "Care team headline"),
                ui.tags.p(
                    f"{overview['age']}-year-old {overview['sex']} patient in {overview['diagnosis_group'].replace('_', ' ')} with risk score {data['risk_score']:.1%}. Model source: {data['model_name']} ({data['model_version']}). Prior admissions, discharge friction, and vitals should guide intervention intensity.",
                    style="color:#dfeaff; line-height:1.6; margin:0;",
                ),
            ),
            kv_section("Patient overview", overview),
            kv_section("Clinical snapshot", clinical),
            kv_section("Discharge factors", discharge),
            kv_section("Latest vitals", vitals),
        )

    @output
    @render.ui
    def drivers_ui():
        return ui.tags.ul(
            {"class": "driver-list"},
            *[ui.tags.li({"class": "driver-item"}, driver) for driver in profile()["key_drivers"]],
        )

    @output
    @render.ui
    def actions_ui():
        return ui.tags.ul(
            {"class": "action-list"},
            *[ui.tags.li({"class": "action-item"}, action) for action in profile()["recommended_actions"]],
        )

    @output
    @render.ui
    def similar_cases_ui():
        items = profile()["similar_cases"]
        if not items:
            return ui.tags.p("No similar cases available yet.")
        return ui.tags.ul(
            {"class": "signal-list"},
            *[
                ui.tags.li(
                    {"class": "signal-item"},
                    f"{item['patient_id']} · similarity {item['similarity_score']:.2f} · risk {item['predicted_readmission_probability']:.1%} · diagnosis {item['diagnosis_group'].replace('_', ' ')}",
                )
                for item in items
            ],
        )

    @output
    @render.ui
    def ai_summary_ui():
        payload = ai_summary_response()
        error = payload.get("error")
        if error:
            return ui.tags.div(
                {"class": "ai-alert"},
                f"AI summary unavailable: {error}",
            )

        summary = payload.get("summary", {})
        fallback_used = bool(payload.get("fallback_used"))
        fallback_reason = payload.get("fallback_reason") or "none"
        status_class = "badge-medium" if fallback_used else "badge-low"
        status_label = "Fallback active" if fallback_used else "OpenAI live"

        def list_block(title: str, items: list[str], css_class: str):
            return ui.div(
                {"class": "ai-section"},
                ui.div({"class": "ai-section-title"}, title),
                ui.tags.ul(
                    {"class": css_class},
                    *[ui.tags.li(item) for item in items],
                ),
            )

        return ui.div(
            {"class": "ai-summary"},
            ui.div(
                {"class": "ai-meta-row"},
                ui.span({"class": f"badge {status_class}"}, status_label),
                ui.span(
                    {"class": "ai-meta-item"},
                    f"Model: {payload.get('llm_model', 'unknown')}",
                ),
                ui.span(
                    {"class": "ai-meta-item"},
                    f"Fallback reason: {fallback_reason}",
                ),
            ),
            ui.div({"class": "ai-risk-summary"}, summary.get("risk_summary", "")),
            list_block("Quantitative signals", summary.get("quantitative_signals", []), "signal-list"),
            list_block("Recommended actions", summary.get("recommended_actions", []), "action-list"),
            list_block("Watchouts", summary.get("watchouts", []), "driver-list"),
        )


app = App(app_ui, server)
