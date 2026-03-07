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


# ── Mosaic plot (statistical: area ∝ frequency) ──
READM_COLORS = {0: "#e0f2fe", 1: "#fecaca"}  # not readmitted / readmitted


def mosaic_layout(tiles: list[dict], total: int) -> list[dict]:
    """Compute (x, y, width, height) in [0,1] for each tile. diagnosis_group → risk_level → readmitted_30d."""
    if not total or not tiles:
        return []
    by_d: dict = {}
    for t in tiles:
        d = str(t["diagnosis_group"])
        r = str(t["risk_level"])
        k = int(t["readmitted_30d"])
        c = int(t["count"])
        if d not in by_d:
            by_d[d] = {"total": 0, "by_r": {}}
        by_d[d]["total"] += c
        if r not in by_d[d]["by_r"]:
            by_d[d]["by_r"][r] = {"total": 0, "by_k": {}}
        by_d[d]["by_r"][r]["total"] += c
        by_d[d]["by_r"][r]["by_k"][k] = by_d[d]["by_r"][r]["by_k"].get(k, 0) + c
    risk_order = {"high": 0, "medium": 1, "low": 2}
    diagnoses = sorted(by_d.keys())
    layout = []
    x_col = 0.0
    for d in diagnoses:
        n_d = by_d[d]["total"]
        col_w = n_d / total
        risks = sorted(by_d[d]["by_r"].keys(), key=lambda r: risk_order.get(r, 3))
        y = 0.0
        for r in risks:
            n_dr = by_d[d]["by_r"][r]["total"]
            row_h = n_dr / n_d
            readm_keys = sorted(by_d[d]["by_r"][r]["by_k"].keys())
            x_cell = 0
            for k in readm_keys:
                n_drk = by_d[d]["by_r"][r]["by_k"][k]
                tile_w = (n_drk / n_dr) * col_w
                layout.append({
                    "diagnosis_group": d,
                    "risk_level": r,
                    "readmitted_30d": k,
                    "count": n_drk,
                    "pct": (n_drk / total) * 100,
                    "x": x_col + (x_cell / n_dr) * col_w,
                    "y": y,
                    "width": tile_w,
                    "height": row_h,
                })
                x_cell += n_drk
            y += row_h
        x_col += col_w
    return layout


def mosaic_svg_html(mosaic_data: dict | None, height_px: int = 320) -> str:
    """Return HTML string for embedded mosaic plot (SVG with rects + legend)."""
    if not mosaic_data or not mosaic_data.get("tiles") or not mosaic_data.get("total"):
        return '<div class="mosaic-wrap"><p class="mosaic-empty">No mosaic data. Load cohort first.</p></div>'
    total = mosaic_data["total"]
    tiles = mosaic_data["tiles"]
    layout = mosaic_layout(tiles, total)
    readm_colors = READM_COLORS
    rects = []
    for t in layout:
        x_pct = t["x"] * 100
        y_pct = t["y"] * 100
        w_pct = t["width"] * 100
        h_pct = t["height"] * 100
        readm_label = "Readmitted" if t["readmitted_30d"] == 1 else "Not readmitted"
        title = f"{t['diagnosis_group']} · {t['risk_level']} · {readm_label}\nn={t['count']} ({t['pct']:.1f}%)"
        fill = readm_colors.get(t["readmitted_30d"], "#e5e7eb")
        rects.append(
            f'<rect x="{x_pct}%" y="{y_pct}%" width="{w_pct}%" height="{h_pct}%" '
            f'fill="{fill}" stroke="#fff" stroke-width="0.3%" data-count="{t["count"]}" data-pct="{t["pct"]:.1f}" '
            f'><title>{title}</title></rect>'
        )
    legend = (
        '<div class="mosaic-legend">'
        '<span>readmitted_30d:</span> '
        '<span><span class="mosaic-legend-swatch" style="background:#e0f2fe"></span> No</span> '
        '<span><span class="mosaic-legend-swatch" style="background:#fecaca"></span> Yes</span>'
        '</div>'
    )
    svg = (
        f'<svg viewBox="0 0 100 100" preserveAspectRatio="none" class="mosaic-svg" style="height:{height_px}px">'
        + "".join(rects) +
        "</svg>"
    )
    return f'<div class="mosaic-wrap"><div class="mosaic-svg-wrap">{svg}</div>{legend}</div>'


# ── Box plot (box-and-whisker: median, Q1, Q3, whiskers, outliers) ──
def _quantile(sorted_arr: list[float], p: float) -> float:
    if not sorted_arr:
        return 0.0
    n = len(sorted_arr)
    i = (n + 1) * p - 1
    lo = max(0, int(i))
    hi = min(n - 1, (int(i) + 1) if i != int(i) else int(i))
    if lo == hi:
        return float(sorted_arr[lo])
    return sorted_arr[lo] + (sorted_arr[hi] - sorted_arr[lo]) * (i - lo)


def _box_stats(values: list[float]) -> dict | None:
    sorted_vals = sorted(v for v in values if v is not None and not (isinstance(v, float) and (v != v)))[:]

    if not sorted_vals:
        return None
    n = len(sorted_vals)
    q1 = _quantile(sorted_vals, 0.25)
    q3 = _quantile(sorted_vals, 0.75)
    median = _quantile(sorted_vals, 0.5)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    whisker_min = next((v for v in sorted_vals if v >= lower_fence), q1)
    whisker_max = next((v for v in reversed(sorted_vals) if v <= upper_fence), q3)
    outliers = [v for v in sorted_vals if v < whisker_min or v > whisker_max]
    return {
        "n": n,
        "q1": q1,
        "median": median,
        "q3": q3,
        "whisker_min": whisker_min,
        "whisker_max": whisker_max,
        "outlier_count": len(outliers),
        "outliers": outliers,
    }


_RISK_COLORS = {
    "high":   {"fill": "rgba(255, 59, 48, 0.12)", "stroke": "#ff3b30", "median": "#cc2d24", "label": "High"},
    "medium": {"fill": "rgba(255, 149, 0, 0.15)", "stroke": "#ff9500", "median": "#cc7700", "label": "Medium"},
    "low":    {"fill": "rgba(52, 199, 89, 0.12)", "stroke": "#34c759", "median": "#279c43", "label": "Low"},
}
_DEFAULT_COLOR = {"fill": "#e0f2fe", "stroke": "#0ea5e9", "median": "#0369a1", "label": "Other"}


def boxplot_svg_html(
    boxplot_data: dict | None,
    group_key: str = "risk_level",
    value_key: str = "predicted_readmission_probability",
    height_px: int = 340,
    selected_patient: dict | None = None,
) -> str:
    """Return HTML string for embedded box-and-whisker plot (SVG).
    selected_patient: optional dict with patient_id, risk_level, value.
    """
    if not boxplot_data or not boxplot_data.get("rows"):
        return '<div class="boxplot-wrap"><p class="mosaic-empty">No box plot data. Load cohort first.</p></div>'
    rows = boxplot_data["rows"]
    by_group: dict[str, list[float]] = {}
    for row in rows:
        g = str(row.get(group_key, "null"))
        v = row.get(value_key)
        if v is not None:
            try:
                val = float(v)
                if val == val:
                    by_group.setdefault(g, []).append(val)
            except (TypeError, ValueError):
                pass
    ordered = ["high", "medium", "low"]
    groups = [g for g in ordered if g in by_group] + sorted(g for g in by_group if g not in ordered)
    box_stats = []
    for name in groups:
        st = _box_stats(by_group[name])
        if st:
            box_stats.append((name, st))
    if not box_stats:
        return '<div class="boxplot-wrap"><p class="mosaic-empty">No numeric values for this group/metric.</p></div>'

    y_vals = []
    for _, st in box_stats:
        y_vals.extend([st["whisker_min"], st["whisker_max"]] + st["outliers"])
    y_min_raw = min(y_vals)
    y_max_raw = max(y_vals)
    y_range_raw = y_max_raw - y_min_raw or 1
    y_min = y_min_raw - y_range_raw * 0.08
    y_max = y_max_raw + y_range_raw * 0.08
    y_range = y_max - y_min

    is_pct = value_key == "predicted_readmission_probability"
    def fmt(v: float) -> str:
        return f"{v * 100:.1f}%" if is_pct else f"{v:.2f}"

    pad_left = 52
    pad_bottom = 44
    pad_top = 16
    pad_right = 100
    w = 600
    h = height_px
    chart_w = w - pad_left - pad_right
    chart_h = h - pad_top - pad_bottom

    def sy(v: float) -> float:
        return pad_top + chart_h - (v - y_min) / y_range * chart_h

    n_groups = len(box_stats)
    box_width = min(54, (chart_w / n_groups) * 0.55) if n_groups else 30
    step = chart_w / n_groups if n_groups else chart_w

    parts: list[str] = []

    # horizontal grid lines
    n_ticks = 5
    y_axis_ticks = [y_min + y_range * i / (n_ticks - 1) for i in range(n_ticks)]
    for v in y_axis_ticks:
        y = sy(v)
        parts.append(f'<line x1="{pad_left}" y1="{y}" x2="{pad_left + chart_w}" y2="{y}" stroke="#f1f5f9" stroke-width="1"/>')

    # y-axis + ticks
    parts.append(f'<line x1="{pad_left}" y1="{pad_top}" x2="{pad_left}" y2="{pad_top + chart_h}" stroke="#e2e8f0"/>')
    parts.append(f'<line x1="{pad_left}" y1="{pad_top + chart_h}" x2="{pad_left + chart_w}" y2="{pad_top + chart_h}" stroke="#e2e8f0"/>')
    for v in y_axis_ticks:
        y = sy(v)
        parts.append(f'<line x1="{pad_left - 4}" y1="{y}" x2="{pad_left}" y2="{y}" stroke="#cbd5e1"/>')
        parts.append(f'<text x="{pad_left - 6}" y="{y + 3.5}" text-anchor="end" font-size="9" fill="#94a3b8">{fmt(v)}</text>')

    # boxes
    for i, (name, st) in enumerate(box_stats):
        colors = _RISK_COLORS.get(name, _DEFAULT_COLOR)
        cx = pad_left + (i + 0.5) * step
        wmin_y = sy(st["whisker_min"])
        wmax_y = sy(st["whisker_max"])
        q1y = sy(st["q1"])
        q3y = sy(st["q3"])
        medy = sy(st["median"])
        hw = box_width / 2
        cap_w = box_width * 0.35

        # whisker lines
        parts.append(f'<line x1="{cx}" y1="{wmax_y}" x2="{cx}" y2="{q3y}" stroke="{colors["stroke"]}" stroke-width="1" opacity="0.5"/>')
        parts.append(f'<line x1="{cx}" y1="{q1y}" x2="{cx}" y2="{wmin_y}" stroke="{colors["stroke"]}" stroke-width="1" opacity="0.5"/>')
        # whisker caps
        parts.append(f'<line x1="{cx - cap_w}" y1="{wmax_y}" x2="{cx + cap_w}" y2="{wmax_y}" stroke="{colors["stroke"]}" stroke-width="1.5" stroke-linecap="round"/>')
        parts.append(f'<line x1="{cx - cap_w}" y1="{wmin_y}" x2="{cx + cap_w}" y2="{wmin_y}" stroke="{colors["stroke"]}" stroke-width="1.5" stroke-linecap="round"/>')
        # IQR box with rounded corners
        parts.append(f'<rect x="{cx - hw}" y="{q3y}" width="{box_width}" height="{q1y - q3y}" rx="3" ry="3" fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="1.5"/>')
        # median line
        parts.append(f'<line x1="{cx - hw + 2}" y1="{medy}" x2="{cx + hw - 2}" y2="{medy}" stroke="{colors["median"]}" stroke-width="2.5" stroke-linecap="round"/>')

        # value labels
        med_label = fmt(st["median"])
        parts.append(f'<text x="{cx + hw + 4}" y="{medy + 3}" text-anchor="start" font-size="9" font-weight="600" fill="{colors["median"]}">{med_label}</text>')
        if abs(q3y - medy) > 14:
            parts.append(f'<text x="{cx + hw + 4}" y="{q3y + 3}" text-anchor="start" font-size="8" fill="#94a3b8">Q3 {fmt(st["q3"])}</text>')
        if abs(q1y - medy) > 14:
            parts.append(f'<text x="{cx + hw + 4}" y="{q1y + 3}" text-anchor="start" font-size="8" fill="#94a3b8">Q1 {fmt(st["q1"])}</text>')

        # tooltip hover area
        title = f"{colors['label']} risk\nn={st['n']}  Median={fmt(st['median'])}  Q1={fmt(st['q1'])}  Q3={fmt(st['q3'])}\nWhisker: {fmt(st['whisker_min'])} – {fmt(st['whisker_max'])}  Outliers: {st['outlier_count']}"
        title_esc = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        parts.append(f'<rect x="{cx - hw}" y="{q3y}" width="{box_width}" height="{q1y - q3y}" fill="transparent" stroke="none"><title>{title_esc}</title></rect>')

        # outliers
        for j, ov in enumerate(st["outliers"]):
            oy = sy(ov)
            dx = (j % 3 - 1) * box_width * 0.2
            parts.append(f'<circle cx="{cx + dx}" cy="{oy}" r="2.5" fill="{colors["stroke"]}" fill-opacity="0.4" stroke="#fff" stroke-width="0.8"/>')

    # x-axis labels
    for i, (name, st) in enumerate(box_stats):
        colors = _RISK_COLORS.get(name, _DEFAULT_COLOR)
        cx = pad_left + (i + 0.5) * step
        display_name = colors.get("label", name.capitalize())
        parts.append(f'<text x="{cx}" y="{pad_top + chart_h + 16}" text-anchor="middle" font-size="10" font-weight="500" fill="#475569">{display_name}</text>')
        parts.append(f'<text x="{cx}" y="{pad_top + chart_h + 28}" text-anchor="middle" font-size="8" fill="#94a3b8">n={st["n"]}</text>')

    # selected patient annotation
    if selected_patient and selected_patient.get("risk_level") in groups:
        try:
            pid = str(selected_patient.get("patient_id", "Selected"))
            val = float(selected_patient.get("value", 0))
            if y_min <= val <= y_max:
                idx = groups.index(selected_patient["risk_level"])
                cx_pt = pad_left + (idx + 0.5) * step
                cy_pt = sy(val)
                label_x = pad_left + chart_w + 8
                # dashed connector line
                parts.append(
                    f'<line x1="{cx_pt + box_width / 2 + 2}" y1="{cy_pt}" x2="{label_x - 2}" y2="{cy_pt}" '
                    f'stroke="#7c3aed" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>'
                )
                # diamond marker on the box
                d = 5
                parts.append(
                    f'<polygon points="{cx_pt},{cy_pt - d} {cx_pt + d},{cy_pt} {cx_pt},{cy_pt + d} {cx_pt - d},{cy_pt}" '
                    f'fill="#7c3aed" stroke="#fff" stroke-width="1.5"/>'
                )
                # label block on the right
                label = pid if len(pid) <= 8 else pid[:6] + "…"
                parts.append(f'<text x="{label_x}" y="{cy_pt - 5}" font-size="9" font-weight="600" fill="#5b21b6">{label}</text>')
                parts.append(f'<text x="{label_x}" y="{cy_pt + 6}" font-size="8" fill="#7c3aed">{fmt(val)}</text>')
        except (TypeError, ValueError, KeyError):
            pass

    # legend at top-right
    leg_x = pad_left + chart_w - 10
    leg_y = pad_top + 2
    for i, (name, _) in enumerate(box_stats):
        colors = _RISK_COLORS.get(name, _DEFAULT_COLOR)
        lx = leg_x - i * 62
        parts.append(f'<rect x="{lx}" y="{leg_y}" width="8" height="8" rx="2" fill="{colors["stroke"]}"/>')
        parts.append(f'<text x="{lx + 11}" y="{leg_y + 7}" font-size="8" fill="#64748b">{colors["label"]}</text>')

    svg = f'<svg viewBox="0 0 {w} {h}" class="boxplot-svg" style="max-width:100%;height:{height_px}px"><g>{"".join(parts)}</g></svg>'
    return f'<div class="boxplot-wrap"><div class="boxplot-svg-wrap">{svg}</div></div>'
