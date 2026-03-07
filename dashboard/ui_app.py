from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import shinyswatch
from shiny import App, reactive, render, ui

# Ensure imports work both when running from repo root and from dashboard/ as app dir.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import PRESET_CONFIGS
from app.services.ai_summary import (
    chat_followup,
    generate_actions,
    generate_risk_summary,
    generate_similar_analysis,
)
from app.services.repository import (
    get_boxplot_data,
    get_patient_profile,
    load_model_input,
)
from app.services.supabase_rest import test_rest_connection
from dashboard.charts import boxplot_svg_html
from dashboard.styles import CUSTOM_CSS

MODEL_CHOICES = {
    "gpt-4o-mini": "GPT-4o Mini (fast)",
    "gpt-4o": "GPT-4o (best)",
    "gpt-4.1-mini": "GPT-4.1 Mini",
    "gpt-4.1-nano": "GPT-4.1 Nano (cheapest)",
}


def icon(name: str, size: int = 16, css_class: str = "") -> ui.Tag:
    """Generate Lucide icon"""
    return ui.tags.i({
        "data-lucide": name,
        "class": f"icon {css_class}",
        "style": f"width:{size}px;height:{size}px;stroke-width:2;"
    })


def risk_badge(level: str):
    n = (level or "medium").lower()
    icon_map = {
        "high": "alert-triangle",
        "medium": "alert-circle",
        "low": "check-circle"
    }
    return ui.div(
        {"class": f"badge badge-{n}"},
        icon(icon_map.get(n, "alert-circle"), 12, "badge-icon"),
        ui.span(n.upper())
    )


def _patient_header(data: dict) -> ui.Tag:
    return ui.div(
        {"class": "patient-header"},
        ui.span({"class": "patient-id"}, data["patient_id"]),
        risk_badge(data["risk_level"]),
        ui.span({"class": "risk-pct"}, f"{data['risk_score']:.1%}"),
    )


def _cohort_stat_row(label: str, value: str, tone: str = "neutral") -> ui.Tag:
    return ui.div(
        {"class": f"cohort-risk-stat tone-{tone}"},
        ui.div({"class": "cohort-risk-stat-label"}, label),
        ui.div({"class": "cohort-risk-stat-value"}, value),
    )


# ── UI ──

app_ui = ui.page_fillable(
    ui.tags.head(
        ui.tags.style(CUSTOM_CSS),
        ui.tags.link(rel="preconnect", href="https://fonts.googleapis.com"),
        ui.tags.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        ui.tags.link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        ),
        ui.tags.script(src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"),
        ui.tags.script("""
            document.addEventListener('DOMContentLoaded', function() {
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            });
            // Re-create icons when Shiny updates the DOM
            $(document).on('shiny:value', function() {
                setTimeout(function() {
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                }, 100);
            });
        """),
    ),
    ui.div(
        {"class": "hero-shell"},
        ui.div(
            {"class": "hero-panel"},
            ui.div({"class": "hero-title"}, "TwinReadmit"),
            ui.div({"class": "hero-subtitle"}, "AI explains patient risk, recommends interventions, and compares to similar historical cases."),
            ui.output_ui("hero_meta_ui"),
        ),
    ),
    ui.layout_sidebar(
        ui.sidebar(
            ui.div(
                {"class": "sidebar-section-label"},
                icon("folder", 12, "section-icon"),
                ui.span("Data")
            ),
            ui.input_select("preset", "Cohort", {p: c["name"] for p, c in PRESET_CONFIGS.items()}, selected="baseline"),
            ui.input_select(
                "patient_sort",
                "Sort patients by",
                {"id": "Patient ID", "risk": "Risk (high → low)"},
                selected="id",
            ),
            ui.output_ui("patient_selector_ui"),
            ui.div(
                {"class": "sidebar-section-label"},
                icon("bot", 12, "section-icon"),
                ui.span("AI Model")
            ),
            ui.input_select("llm_model", "LLM", MODEL_CHOICES, selected="gpt-4o-mini"),
            width=260,
            open="desktop",
        ),
        ui.div(
            {"class": "overview-shell"},
            ui.output_ui("metric_cards"),
            # pull 的 cohort 图 + 箱线图同一排
            ui.div(
                {"class": "charts-row"},
                ui.output_ui("cohort_risk_distribution"),
                ui.output_ui("boxplot_ui"),
            ),
        ),
        ui.div(
            {"class": "ai-workspace"},
            ui.navset_card_tab(
                # Tab 1
                ui.nav_panel(
                    ui.div(
                        {"class": "tab-label"},
                        icon("activity", 16, "tab-icon"),
                        ui.span("AI Risk Summary")
                    ),
                    ui.div(
                        {"class": "ai-tab-stack"},
                        ui.div({"class": "panel-card ai-main-panel"}, ui.output_ui("tab1_content")),
                        ui.div(
                            {"class": "panel-card ai-chat-panel"},
                            ui.div({"class": "section-title"}, "Continue the conversation"),
                            ui.output_ui("chat1_history"),
                            ui.div(
                                {"class": "chat-input-row"},
                                ui.input_text("chat1_input", None, placeholder="Ask about this patient's risk..."),
                                ui.input_action_button("chat1_send", "Send", class_="btn-sm btn-send"),
                            ),
                        ),
                    ),
                ),
                # Tab 2
                ui.nav_panel(
                    ui.div(
                        {"class": "tab-label"},
                        icon("clipboard-check", 16, "tab-icon"),
                        ui.span("AI Recommended Actions")
                    ),
                    ui.div(
                        {"class": "ai-tab-stack"},
                        ui.div({"class": "panel-card ai-main-panel"}, ui.output_ui("tab2_content")),
                        ui.div(
                            {"class": "panel-card ai-chat-panel"},
                            ui.div({"class": "section-title"}, "Continue the conversation"),
                            ui.output_ui("chat2_history"),
                            ui.div(
                                {"class": "chat-input-row"},
                                ui.input_text("chat2_input", None, placeholder="Ask about interventions..."),
                                ui.input_action_button("chat2_send", "Send", class_="btn-sm btn-send"),
                            ),
                        ),
                    ),
                ),
                # Tab 3
                ui.nav_panel(
                    ui.div(
                        {"class": "tab-label"},
                        icon("git-compare", 16, "tab-icon"),
                        ui.span("AI Similar Cases")
                    ),
                    ui.div(
                        {"class": "ai-tab-stack"},
                        ui.div({"class": "panel-card ai-main-panel"}, ui.output_ui("tab3_content")),
                        ui.div(
                            {"class": "panel-card ai-chat-panel"},
                            ui.div({"class": "section-title"}, "Continue the conversation"),
                            ui.output_ui("chat3_history"),
                            ui.div(
                                {"class": "chat-input-row"},
                                ui.input_text("chat3_input", None, placeholder="Ask about similar cases..."),
                                ui.input_action_button("chat3_send", "Send", class_="btn-sm btn-send"),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    ),
    title="TwinReadmit",
    fillable=True,
    theme=shinyswatch.theme.flatly(),
)


# ── Server ──

def server(input, output, session):

    # ── Reactive state for chat histories ──
    chat1_messages: reactive.Value[list[dict]] = reactive.Value([])
    chat2_messages: reactive.Value[list[dict]] = reactive.Value([])
    chat3_messages: reactive.Value[list[dict]] = reactive.Value([])

    # ── Data ──

    @reactive.calc
    def db_connected() -> bool:
        try:
            return test_rest_connection().get("connected", False)
        except Exception:
            return False

    @reactive.calc
    def cohort_df() -> pd.DataFrame:
        return load_model_input(input.preset())

    @reactive.calc
    def all_patient_ids() -> list[str]:
        df = cohort_df()
        if input.patient_sort() == "risk":
            ordered = df.sort_values("active_risk_probability", ascending=False)
        else:
            ordered = df.sort_values("patient_id")
        return ordered["patient_id"].unique().tolist()

    @reactive.calc
    def selected_patient_id() -> str:
        pid = input.patient_id()
        return pid if pid else (all_patient_ids()[0] if all_patient_ids() else "")

    @reactive.effect
    def _update_patient_selector():
        ids = all_patient_ids()
        if not ids:
            return
        current = input.patient_id()
        selected = current if current in ids else ids[0]
        ui.update_selectize("patient_id", choices=ids, selected=selected)

    @output
    @render.ui
    def patient_selector_ui():
        return ui.input_selectize("patient_id", "Patient", choices=all_patient_ids(), selected=None)

    @reactive.calc
    def profile() -> dict:
        pid = selected_patient_id()
        if not pid:
            return {}
        return get_patient_profile(input.preset(), pid)

    # Reset chat when patient changes
    @reactive.effect
    @reactive.event(input.patient_id)
    def _reset_chats():
        chat1_messages.set([])
        chat2_messages.set([])
        chat3_messages.set([])

    # ── LLM calls (one per tab, triggered by patient selection) ──

    @reactive.calc
    def risk_result() -> dict:
        data = profile()
        if not data:
            return
        return generate_risk_summary(data, model=input.llm_model())

    @reactive.calc
    def actions_result() -> dict:
        data = profile()
        if not data:
            return {}
        return generate_actions(data, model=input.llm_model())

    @reactive.calc
    def similar_result() -> dict:
        data = profile()
        if not data:
            return {}
        return generate_similar_analysis(data, model=input.llm_model())

    # ── Hero ──

    @output
    @render.ui
    def hero_meta_ui():
        df = cohort_df()
        connected = db_connected()
        db_icon = "database" if connected else "database-x"
        db_class = "hero-icon-green" if connected else "hero-icon-red"
        label = "Supabase live" if connected else "CSV fallback"
        n_patients = int(df["patient_id"].nunique())
        n_high = int((df["risk_level"] == "high").sum())
        return ui.div(
            {"class": "hero-meta"},
            ui.div({"class": "hero-meta-item"}, icon(db_icon, 14, db_class), label),
            ui.div({"class": "hero-meta-item"}, icon("users", 14, "hero-icon"), f"{n_patients} patients"),
            ui.div({"class": "hero-meta-item"}, icon("alert-triangle", 14, "hero-icon"), f"{n_high} high-risk"),
        )

    # ── Metrics ──

    @output
    @render.ui
    def metric_cards():
        df = cohort_df()
        data = profile()
        n = int(df["patient_id"].nunique())
        high = int((df["risk_level"] == "high").sum())
        avg = float(df["active_risk_probability"].mean())
        patient_risk = f"{data['risk_score']:.1%}" if data else "—"
        cards = [
            ("Cohort", str(n), "patients"),
            ("High-risk", str(high), "need intervention"),
            ("Avg risk", f"{avg:.1%}", "cohort mean"),
            ("Selected", patient_risk, data.get("patient_id", "—")),
        ]
        return ui.div(
            {"class": "metric-grid"},
            *[ui.div({"class": "metric-card"}, ui.div({"class": "metric-label"}, l), ui.div({"class": "metric-value"}, v), ui.div({"class": "metric-footnote"}, n)) for l, v, n in cards],
        )

    @reactive.calc
    def cohort_risk_metrics() -> dict[str, int | float]:
        df = cohort_df()
        cohort_total = int(df["patient_id"].nunique())
        high_count = int((df["risk_level"] == "high").sum())
        high_count = min(high_count, cohort_total)
        non_high_count = max(cohort_total - high_count, 0)
        high_pct = (high_count / cohort_total) if cohort_total else 0.0
        return {
            "cohort_total": cohort_total,
            "high_count": high_count,
            "non_high_count": non_high_count,
            "high_pct": high_pct,
        }

    @output
    @render.ui
    def cohort_risk_distribution():
        stats = cohort_risk_metrics()
        return ui.div(
            {"class": "panel-card cohort-risk-card"},
            ui.div(
                {"class": "cohort-risk-header"},
                ui.div({"class": "section-title"}, "Cohort Risk Distribution"),
                ui.div({"class": "cohort-risk-subtitle"}, "High-risk vs non-high-risk patients"),
            ),
            ui.div(
                {"class": "cohort-risk-body"},
                ui.div(
                    {"class": "cohort-risk-donut-wrap"},
                    ui.div(
                        {"class": "cohort-risk-donut", "style": f"--high-pct: {stats['high_pct'] * 100:.2f};"},
                    ),
                    ui.div(
                        {"class": "cohort-risk-center"},
                        ui.div({"class": "cohort-risk-center-value"}, f"{stats['high_pct']:.1%}"),
                        ui.div({"class": "cohort-risk-center-label"}, "High-risk"),
                    ),
                ),
                ui.div(
                    {"class": "cohort-risk-stats"},
                    _cohort_stat_row("High-risk count", str(stats["high_count"]), tone="high"),
                    _cohort_stat_row("Non-high-risk count", str(stats["non_high_count"]), tone="neutral"),
                    _cohort_stat_row("High-risk percentage", f"{stats['high_pct']:.1%}", tone="accent"),
                    ui.div({"class": "cohort-risk-total"}, f"Cohort total: {stats['cohort_total']} patients"),
                ),
            ),
        )

    @output
    @render.ui
    def boxplot_ui():
        try:
            data = get_boxplot_data(input.preset())
        except Exception:
            data = None
        data_profile = profile()
        selected_patient = None
        if data_profile:
            selected_patient = {
                "patient_id": data_profile["patient_id"],
                "risk_level": data_profile["risk_level"],
                "value": data_profile["risk_score"],
            }
        html = boxplot_svg_html(
            data,
            group_key="risk_level",
            value_key="predicted_readmission_probability",
            height_px=340,
            selected_patient=selected_patient,
        )
        return ui.div(
            {"class": "panel-card boxplot-card"},
            ui.div({"class": "section-title", "style": "margin-bottom:0.25rem;"}, "Readmission Probability by Risk Level"),
            ui.div(
                {"class": "mosaic-subtitle"},
                "Cohort distribution with selected patient. Hover for details.",
            ),
            ui.HTML(html),
        )

    # ── Tab 1: AI Risk Summary ──

    @output
    @render.ui
    def tab1_content():
        data = profile()
        if not data:
            return ui.p("Select a patient.", style="color:var(--text-tertiary);")
        r = risk_result()
        fallback_badge = ui.span({"class": "badge badge-medium"}, "FALLBACK") if r.get("fallback") else ui.span({"class": "badge badge-low"}, "LIVE")

        factors = r.get("key_factors", [])
        factor_items = [ui.tags.li({"class": "signal-item"}, f) for f in factors] if factors else []

        return ui.div(
            _patient_header(data),
            ui.div({"class": "ai-meta-row"}, fallback_badge, ui.span({"class": "ai-meta-item"}, f"Model: {r.get('model', '?')}")),
            ui.div({"class": "section-title", "style": "margin-top:0.75rem;"}, "Why is this patient at risk?"),
            ui.div({"class": "ai-narrative"}, r.get("risk_narrative", "")),
            ui.div({"class": "section-title", "style": "margin-top:0.75rem;"}, "Key risk factors") if factors else None,
            ui.tags.ul({"class": "signal-list"}, *factor_items) if factor_items else None,
        )

    # ── Tab 2: AI Recommended Actions ──

    @output
    @render.ui
    def tab2_content():
        data = profile()
        if not data:
            return ui.p("Select a patient.", style="color:var(--text-tertiary);")
        a = actions_result()
        fallback_badge = ui.span({"class": "badge badge-medium"}, "FALLBACK") if a.get("fallback") else ui.span({"class": "badge badge-low"}, "LIVE")

        action_items = []
        for act in a.get("actions", []):
            if isinstance(act, dict):
                priority = act.get("priority", "medium").lower()
                p_class = f"priority-{priority}"
                action_items.append(ui.tags.li(
                    {"class": f"action-card {p_class}"},
                    ui.div({"class": "action-text"}, act.get("action", "")),
                    ui.div({"class": "action-rationale"}, act.get("rationale", "")) if act.get("rationale") else None,
                ))
            else:
                action_items.append(ui.tags.li({"class": "action-card priority-high"}, ui.div({"class": "action-text"}, str(act))))

        return ui.div(
            _patient_header(data),
            ui.div({"class": "ai-meta-row"}, fallback_badge, ui.span({"class": "ai-meta-item"}, f"Model: {a.get('model', '?')}")),
            ui.div({"class": "section-title", "style": "margin-top:0.75rem;"}, "What should we do next?"),
            ui.div({"class": "ai-narrative"}, a.get("action_plan", "")) if a.get("action_plan") else None,
            ui.tags.ol({"class": "action-list-ordered", "style": "margin-top:0.6rem;"}, *action_items) if action_items else None,
        )

    # ── Tab 3: AI Similar Cases ──

    @output
    @render.ui
    def tab3_content():
        data = profile()
        if not data:
            return ui.p("Select a patient.", style="color:var(--text-tertiary);")
        s = similar_result()
        fallback_badge = ui.span({"class": "badge badge-medium"}, "FALLBACK") if s.get("fallback") else ui.span({"class": "badge badge-low"}, "LIVE")

        cases = data.get("similar_cases", [])
        case_items = []
        for c in cases:
            readmit = "Readmitted" if c.get("readmitted_30d") else "Not readmitted"
            readmit_class = "readmit-yes" if c.get("readmitted_30d") else "readmit-no"
            case_items.append(ui.div(
                {"class": "case-card"},
                ui.div({"class": "case-header"},
                    ui.span({"class": "case-id"}, c["patient_id"]),
                    ui.span({"class": f"case-readmit {readmit_class}"}, readmit),
                ),
                ui.div({"class": "case-details"},
                    f"{c['diagnosis_group'].replace('_',' ').title()} · "
                    f"{c['similarity_score']:.0%} match · "
                    f"{c['predicted_readmission_probability']:.1%} risk"
                ),
            ))

        return ui.div(
            _patient_header(data),
            ui.div({"class": "ai-meta-row"}, fallback_badge, ui.span({"class": "ai-meta-item"}, f"Model: {s.get('model', '?')}")),
            ui.div({"class": "section-title", "style": "margin-top:0.75rem;"}, "How does this compare to similar patients?"),
            ui.div({"class": "ai-narrative"}, s.get("comparison_narrative", "")),
            ui.div({"class": "section-title", "style": "margin-top:0.75rem;"}, "Pattern insight") if s.get("pattern_insight") else None,
            ui.div({"class": "pattern-insight"}, s.get("pattern_insight", "")) if s.get("pattern_insight") else None,
            ui.div({"class": "section-title", "style": "margin-top:0.75rem;"}, f"Similar cases ({len(cases)})") if cases else None,
            ui.div({"class": "cases-grid"}, *case_items) if case_items else None,
        )

    # ── Chat handlers ──

    def _render_chat(messages: list[dict]) -> ui.Tag:
        if not messages:
            return ui.div({"class": "chat-empty"}, "No messages yet. Ask a question below.")
        items = []
        for msg in messages:
            cls = "chat-user" if msg["role"] == "user" else "chat-ai"
            items.append(ui.div({"class": f"chat-bubble {cls}"}, msg["content"]))
        return ui.div({"class": "chat-thread"}, *items)

    @reactive.effect
    @reactive.event(input.chat1_send)
    def _handle_chat1():
        text = input.chat1_input().strip()
        if not text or not profile():
            return
        history = list(chat1_messages.get())
        history.append({"role": "user", "content": text})
        reply = chat_followup(profile(), history, text, model=input.llm_model())
        history.append({"role": "assistant", "content": reply})
        chat1_messages.set(history)
        ui.update_text("chat1_input", value="")

    @reactive.effect
    @reactive.event(input.chat2_send)
    def _handle_chat2():
        text = input.chat2_input().strip()
        if not text or not profile():
            return
        history = list(chat2_messages.get())
        history.append({"role": "user", "content": text})
        reply = chat_followup(profile(), history, text, model=input.llm_model())
        history.append({"role": "assistant", "content": reply})
        chat2_messages.set(history)
        ui.update_text("chat2_input", value="")

    @reactive.effect
    @reactive.event(input.chat3_send)
    def _handle_chat3():
        text = input.chat3_input().strip()
        if not text or not profile():
            return
        history = list(chat3_messages.get())
        history.append({"role": "user", "content": text})
        reply = chat_followup(profile(), history, text, model=input.llm_model())
        history.append({"role": "assistant", "content": reply})
        chat3_messages.set(history)
        ui.update_text("chat3_input", value="")

    @output
    @render.ui
    def chat1_history():
        return _render_chat(chat1_messages.get())

    @output
    @render.ui
    def chat2_history():
        return _render_chat(chat2_messages.get())

    @output
    @render.ui
    def chat3_history():
        return _render_chat(chat3_messages.get())


app = App(app_ui, server)
