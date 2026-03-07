from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLOR_SCALE = {
    "high": "#ff6f91",
    "medium": "#ffb55f",
    "low": "#47d7ac",
}

PLOTLY_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": "#eaf2ff"},
    "margin": {"l": 16, "r": 16, "t": 28, "b": 16},
}


def risk_distribution_figure(items: list[dict]) -> go.Figure:
    df = pd.DataFrame(items)
    fig = px.bar(
        df,
        x="label",
        y="value",
        color="label",
        color_discrete_map=COLOR_SCALE,
        text_auto=True,
    )
    fig.update_layout(showlegend=False, **PLOTLY_LAYOUT)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None, gridcolor="rgba(255,255,255,0.08)")
    return fig


def diagnosis_mix_figure(items: list[dict]) -> go.Figure:
    df = pd.DataFrame(items)
    fig = px.pie(
        df,
        names="label",
        values="value",
        hole=0.62,
        color_discrete_sequence=["#59b0ff", "#7a7dff", "#47d7ac", "#ffb55f", "#ff6f91"],
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(**PLOTLY_LAYOUT, legend_title_text="Diagnosis")
    return fig


def explorer_bar_figure(df: pd.DataFrame) -> go.Figure:
    plot_df = df.sort_values("predicted_readmission_probability", ascending=True).tail(12)
    fig = px.bar(
        plot_df,
        x="predicted_readmission_probability",
        y="patient_id",
        orientation="h",
        color="risk_level",
        color_discrete_map=COLOR_SCALE,
        hover_data=["diagnosis_group", "severity_score", "prior_admissions_12m"],
    )
    fig.update_layout(**PLOTLY_LAYOUT, xaxis_tickformat=".0%", yaxis_title=None, xaxis_title="Predicted risk")
    return fig


def gauge_figure(risk_score: float, risk_level: str) -> go.Figure:
    color = COLOR_SCALE.get(risk_level, "#59b0ff")
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score * 100,
            number={"suffix": "%", "font": {"size": 34}},
            title={"text": "Readmission risk"},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#bfd2fb"},
                "bar": {"color": color},
                "bgcolor": "rgba(255,255,255,0.04)",
                "steps": [
                    {"range": [0, 35], "color": "rgba(71,215,172,0.20)"},
                    {"range": [35, 65], "color": "rgba(255,181,95,0.18)"},
                    {"range": [65, 100], "color": "rgba(255,111,145,0.18)"},
                ],
            },
        )
    )
    fig.update_layout(**PLOTLY_LAYOUT, margin={"l": 8, "r": 8, "t": 48, "b": 8}, height=320)
    return fig


def cohort_comparison_figure(profile: dict) -> go.Figure:
    metrics = [
        ("Age", profile["overview"]["age"], profile["cohort_medians"]["age"]),
        ("Chronic", profile["clinical_snapshot"]["chronic_conditions_count"], profile["cohort_medians"]["chronic_conditions_count"]),
        ("Prior Adm", profile["clinical_snapshot"]["prior_admissions_12m"], profile["cohort_medians"]["prior_admissions_12m"]),
        ("LOS", profile["clinical_snapshot"]["length_of_stay"], profile["cohort_medians"]["length_of_stay"]),
        ("Severity", profile["clinical_snapshot"]["severity_score"], profile["cohort_medians"]["severity_score"]),
        ("Meds", profile["discharge_factors"]["medication_complexity"], profile["cohort_medians"]["medication_complexity"]),
    ]
    labels = [item[0] for item in metrics]
    patient_values = [item[1] for item in metrics]
    median_values = [item[2] for item in metrics]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=patient_values, theta=labels, fill="toself", name="Patient", line_color="#59b0ff"))
    fig.add_trace(go.Scatterpolar(r=median_values, theta=labels, fill="toself", name="Cohort median", line_color="#7a7dff"))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        polar={
            "bgcolor": "rgba(0,0,0,0)",
            "radialaxis": {"visible": True, "gridcolor": "rgba(255,255,255,0.08)"},
            "angularaxis": {"gridcolor": "rgba(255,255,255,0.08)"},
        },
        height=360,
    )
    return fig


def similar_cases_figure(similar_cases: list[dict]) -> go.Figure:
    df = pd.DataFrame(similar_cases)
    if df.empty:
        return go.Figure()

    fig = px.bar(
        df.sort_values("similarity_score"),
        x="similarity_score",
        y="patient_id",
        orientation="h",
        color="risk_level",
        color_discrete_map=COLOR_SCALE,
        text="predicted_readmission_probability",
    )
    fig.update_layout(**PLOTLY_LAYOUT, xaxis_title="Similarity score", yaxis_title=None)
    fig.update_traces(texttemplate="risk %{text:.0%}", textposition="outside")
    return fig
