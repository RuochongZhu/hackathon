from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLOR_SCALE = {
    "high": "#ff3b30",
    "medium": "#ff9500",
    "low": "#34c759",
}

PLOTLY_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": "#1d1d1f", "family": "-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif", "size": 12},
    "margin": {"l": 12, "r": 12, "t": 24, "b": 12},
}

GRID_COLOR = "rgba(0, 0, 0, 0.06)"


def _empty_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, showarrow=False, x=0.5, y=0.5, xref="paper", yref="paper", font={"size": 13, "color": "#aeaeb2"})
    fig.update_layout(**PLOTLY_LAYOUT, xaxis={"visible": False}, yaxis={"visible": False}, height=260)
    return fig


def risk_distribution_figure(items: list[dict]) -> go.Figure:
    df = pd.DataFrame(items)
    if df.empty or not {"label", "value"}.issubset(df.columns):
        return _empty_figure("No risk data available.")
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
    fig = px.bar(df, x="label", y="value", color="label", color_discrete_map=COLOR_SCALE, text_auto=True)
    fig.update_layout(showlegend=False, **PLOTLY_LAYOUT, height=280)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None, gridcolor=GRID_COLOR)
    fig.update_traces(marker_line_width=0, textfont_size=11)
    return fig


def diagnosis_mix_figure(items: list[dict]) -> go.Figure:
    df = pd.DataFrame(items)
    if df.empty or not {"label", "value"}.issubset(df.columns):
        return _empty_figure("No diagnosis data available.")
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
    df = df[df["value"] > 0]
    if df.empty:
        return _empty_figure("No diagnosis data available.")
    fig = px.pie(df, names="label", values="value", hole=0.65, color_discrete_sequence=["#0071e3", "#34c759", "#ff9500", "#ff3b30", "#af52de", "#5ac8fa"])
    fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=10)
    fig.update_layout(**PLOTLY_LAYOUT, legend_title_text="", height=280, showlegend=False)
    return fig


def explorer_bar_figure(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return _empty_figure("No patients match filters.")
    plot_df = df.copy()
    if "predicted_readmission_probability" not in plot_df.columns:
        if "active_risk_probability" in plot_df.columns:
            plot_df["predicted_readmission_probability"] = plot_df["active_risk_probability"]
        else:
            return _empty_figure("Missing risk data.")
    if "risk_level" not in plot_df.columns:
        plot_df["risk_level"] = "medium"
    if "patient_id" not in plot_df.columns:
        plot_df["patient_id"] = [f"P{i+1}" for i in range(len(plot_df))]
    plot_df = plot_df.sort_values("predicted_readmission_probability", ascending=True).tail(10)
    fig = px.bar(plot_df, x="predicted_readmission_probability", y="patient_id", orientation="h", color="risk_level", color_discrete_map=COLOR_SCALE)
    fig.update_layout(**PLOTLY_LAYOUT, xaxis_tickformat=".0%", yaxis_title=None, xaxis_title=None, showlegend=False, height=300)
    fig.update_traces(marker_line_width=0)
    return fig


def gauge_figure(risk_score: float, risk_level: str) -> go.Figure:
    color = COLOR_SCALE.get(risk_level, "#0071e3")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score * 100,
        number={"suffix": "%", "font": {"size": 32, "color": "#1d1d1f"}},
        title={"text": "30-day readmission risk", "font": {"size": 13, "color": "#6e6e73"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#aeaeb2", "tickfont": {"size": 10}},
            "bar": {"color": color, "thickness": 0.75},
            "bgcolor": "rgba(0,0,0,0.03)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 35], "color": "rgba(52,199,89,0.08)"},
                {"range": [35, 65], "color": "rgba(255,149,0,0.08)"},
                {"range": [65, 100], "color": "rgba(255,59,48,0.08)"},
            ],
        },
    ))
    fig.update_layout(**PLOTLY_LAYOUT, margin={"l": 8, "r": 8, "t": 40, "b": 8}, height=280)
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
    labels = [m[0] for m in metrics]
    patient_vals = [float(m[1]) for m in metrics]
    median_vals = [float(m[2]) for m in metrics]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=patient_vals, theta=labels, fill="toself", name="Patient", line_color="#0071e3", fillcolor="rgba(0,113,227,0.08)"))
    fig.add_trace(go.Scatterpolar(r=median_vals, theta=labels, fill="toself", name="Cohort", line_color="#aeaeb2", fillcolor="rgba(174,174,178,0.06)"))
    fig.update_layout(**PLOTLY_LAYOUT, polar={"bgcolor": "rgba(0,0,0,0)", "radialaxis": {"visible": True, "gridcolor": GRID_COLOR, "tickfont": {"size": 9}}, "angularaxis": {"gridcolor": GRID_COLOR}}, height=300, legend={"font": {"size": 11}})
    return fig


def similar_cases_figure(similar_cases: list[dict]) -> go.Figure:
    df = pd.DataFrame(similar_cases)
    if df.empty or not {"similarity_score", "patient_id"}.issubset(df.columns):
        return _empty_figure("No historical analogs found.")
    fig = px.bar(df.sort_values("similarity_score"), x="similarity_score", y="patient_id", orientation="h", color="risk_level", color_discrete_map=COLOR_SCALE)
    fig.update_layout(**PLOTLY_LAYOUT, xaxis_title=None, yaxis_title=None, showlegend=False, height=240)
    fig.update_traces(marker_line_width=0)
    return fig
