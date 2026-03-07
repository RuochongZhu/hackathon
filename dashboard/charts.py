from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLOR_SCALE = {
    "high": "#ff5f73",
    "medium": "#f4b942",
    "low": "#2ccf9f",
}

DIAGNOSIS_COLORS = ["#2ccf9f", "#3ba8ff", "#f4b942", "#ff8b61", "#ff5f73", "#58d2e8"]

PLOTLY_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": "#e7f6fb", "family": "'IBM Plex Sans', sans-serif"},
    "margin": {"l": 16, "r": 16, "t": 28, "b": 16},
}

GRID_COLOR = "rgba(137, 178, 192, 0.22)"


def _empty_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        showarrow=False,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        font={"size": 14, "color": "#9ec4d0"},
    )
    fig.update_layout(
        **PLOTLY_LAYOUT,
        xaxis={"visible": False},
        yaxis={"visible": False},
        height=280,
    )
    return fig


def risk_distribution_figure(items: list[dict]) -> go.Figure:
    df = pd.DataFrame(items)
    if df.empty or not {"label", "value"}.issubset(df.columns):
        return _empty_figure("No risk-tier data available for this filter.")

    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
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
    fig.update_yaxes(title=None, gridcolor=GRID_COLOR)
    return fig


def diagnosis_mix_figure(items: list[dict]) -> go.Figure:
    df = pd.DataFrame(items)
    if df.empty or not {"label", "value"}.issubset(df.columns):
        return _empty_figure("No diagnosis-mix data available for this filter.")

    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
    df = df[df["value"] > 0]
    if df.empty:
        return _empty_figure("No diagnosis-mix data available for this filter.")

    fig = px.pie(
        df,
        names="label",
        values="value",
        hole=0.64,
        color_discrete_sequence=DIAGNOSIS_COLORS,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(**PLOTLY_LAYOUT, legend_title_text="Diagnosis")
    return fig


def explorer_bar_figure(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_figure("No patients match your current explorer filters.")

    plot_df = df.copy()
    if "predicted_readmission_probability" not in plot_df.columns:
        if "active_risk_probability" in plot_df.columns:
            plot_df["predicted_readmission_probability"] = plot_df["active_risk_probability"]
        else:
            return _empty_figure("Missing risk fields for the explorer chart.")
    if "risk_level" not in plot_df.columns:
        plot_df["risk_level"] = "medium"
    if "patient_id" not in plot_df.columns:
        plot_df["patient_id"] = [f"patient_{idx + 1}" for idx in range(len(plot_df))]

    plot_df = plot_df.sort_values("predicted_readmission_probability", ascending=True).tail(12)
    fig = px.bar(
        plot_df,
        x="predicted_readmission_probability",
        y="patient_id",
        orientation="h",
        color="risk_level",
        color_discrete_map=COLOR_SCALE,
        hover_data=[col for col in ["diagnosis_group", "severity_score", "prior_admissions_12m"] if col in plot_df.columns],
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
                    {"range": [0, 35], "color": "rgba(44,207,159,0.20)"},
                    {"range": [35, 65], "color": "rgba(244,185,66,0.18)"},
                    {"range": [65, 100], "color": "rgba(255,95,115,0.18)"},
                ],
            },
        )
    )
    fig.update_layout(**PLOTLY_LAYOUT, margin={"l": 8, "r": 8, "t": 48, "b": 8}, height=320)
    return fig


def cohort_comparison_figure(profile: dict) -> go.Figure:
    overview = profile.get("overview", {})
    clinical = profile.get("clinical_snapshot", {})
    discharge = profile.get("discharge_factors", {})
    medians = profile.get("cohort_medians", {})

    metrics = [
        ("Age", overview.get("age", 0), medians.get("age", 0)),
        ("Chronic", clinical.get("chronic_conditions_count", 0), medians.get("chronic_conditions_count", 0)),
        ("Prior Adm", clinical.get("prior_admissions_12m", 0), medians.get("prior_admissions_12m", 0)),
        ("LOS", clinical.get("length_of_stay", 0), medians.get("length_of_stay", 0)),
        ("Severity", clinical.get("severity_score", 0), medians.get("severity_score", 0)),
        ("Meds", discharge.get("medication_complexity", 0), medians.get("medication_complexity", 0)),
    ]
    labels = [item[0] for item in metrics]
    patient_values = [float(item[1]) for item in metrics]
    median_values = [float(item[2]) for item in metrics]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=patient_values, theta=labels, fill="toself", name="Patient", line_color="#3ba8ff"))
    fig.add_trace(go.Scatterpolar(r=median_values, theta=labels, fill="toself", name="Cohort median", line_color="#2ccf9f"))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        polar={
            "bgcolor": "rgba(0,0,0,0)",
            "radialaxis": {"visible": True, "gridcolor": GRID_COLOR},
            "angularaxis": {"gridcolor": GRID_COLOR},
        },
        height=360,
    )
    return fig


def similar_cases_figure(similar_cases: list[dict]) -> go.Figure:
    df = pd.DataFrame(similar_cases)
    if df.empty or not {"similarity_score", "patient_id"}.issubset(df.columns):
        return _empty_figure("No historical analogs found for this patient.")

    fig = px.bar(
        df.sort_values("similarity_score"),
        x="similarity_score",
        y="patient_id",
        orientation="h",
        color="risk_level",
        color_discrete_map=COLOR_SCALE,
        text="predicted_readmission_probability" if "predicted_readmission_probability" in df.columns else None,
    )
    fig.update_layout(**PLOTLY_LAYOUT, xaxis_title="Similarity score", yaxis_title=None)
    if "predicted_readmission_probability" in df.columns:
        fig.update_traces(texttemplate="risk %{text:.0%}", textposition="outside")
    return fig
