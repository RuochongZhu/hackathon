CUSTOM_CSS = """
:root {
  --bg: #f5f5f7;
  --surface: rgba(255, 255, 255, 0.72);
  --surface-solid: #ffffff;
  --border: rgba(0, 0, 0, 0.06);
  --border-hover: rgba(0, 0, 0, 0.12);
  --text-primary: #1d1d1f;
  --text-secondary: #6e6e73;
  --text-tertiary: #aeaeb2;
  --accent: #0071e3;
  --accent-soft: rgba(0, 113, 227, 0.08);
  --red: #ff3b30;
  --orange: #ff9500;
  --green: #34c759;
  --risk-neutral: #d8dee7;
  --red-soft: rgba(255, 59, 48, 0.10);
  --orange-soft: rgba(255, 149, 0, 0.10);
  --green-soft: rgba(52, 199, 89, 0.10);
  --radius: 16px;
  --radius-sm: 10px;
  --shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  --shadow-hover: 0 4px 20px rgba(0, 0, 0, 0.08);
  --blur: blur(40px) saturate(180%);
}

*, *::before, *::after { box-sizing: border-box; }

html, body {
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background: var(--bg);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
  font-size: 14px;
  line-height: 1.5;
}

/* ── Hero ── */
.hero-shell { padding: 1.25rem 1.5rem 0; }

.hero-panel {
  background: var(--surface);
  backdrop-filter: var(--blur);
  -webkit-backdrop-filter: var(--blur);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem 1.75rem 1.25rem;
  box-shadow: var(--shadow);
}

.hero-title {
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: var(--text-primary);
}

.hero-subtitle {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
  max-width: 680px;
}

.hero-meta {
  display: flex;
  gap: 1.5rem;
  margin-top: 0.75rem;
  flex-wrap: wrap;
}

.hero-meta-item {
  font-size: 0.78rem;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.hero-meta-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot-green { background: var(--green); }
.dot-orange { background: var(--orange); }
.dot-red { background: var(--red); }
.dot-gray { background: var(--text-tertiary); }

/* ── Sidebar ── */
.bslib-sidebar-layout > .sidebar {
  background: var(--surface) !important;
  backdrop-filter: var(--blur) !important;
  -webkit-backdrop-filter: var(--blur) !important;
  border-right: 1px solid var(--border) !important;
}

.sidebar-section-label {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-tertiary);
  margin: 0.75rem 0 0.35rem;
}

.shiny-input-container,
.control-label,
.shiny-input-container .form-check-label {
  color: var(--text-primary) !important;
  font-size: 0.85rem !important;
}

.form-control, .form-select {
  border-radius: var(--radius-sm) !important;
  border: 1px solid var(--border) !important;
  background: var(--surface-solid) !important;
  font-size: 0.85rem !important;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-control:focus, .form-select:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px var(--accent-soft) !important;
}

/* ── Tabs ── */
.nav-tabs, .nav-pills { border-bottom: 1px solid var(--border); }

.nav-tabs .nav-link, .nav-pills .nav-link {
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.85rem;
  padding: 0.45rem 0.9rem;
  transition: all 0.2s;
}

.nav-tabs .nav-link:hover, .nav-pills .nav-link:hover {
  color: var(--text-primary);
  background: rgba(0, 0, 0, 0.03);
}

.nav-tabs .nav-link.active, .nav-pills .nav-link.active {
  color: var(--text-primary);
  background: var(--surface-solid);
  border: 1px solid var(--border);
  font-weight: 600;
}

/* ── Metric cards ── */
.overview-shell {
  display: grid;
  gap: 0.85rem;
  margin: 0.75rem 0 1rem;
}

/* ── AI workspace ── */
.ai-workspace {
  margin: 0.2rem 0 0.3rem;
}

.ai-workspace > .card.bslib-card {
  min-height: 760px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.86), rgba(255, 255, 255, 0.74));
  border: 1px solid var(--border);
  border-radius: calc(var(--radius) + 2px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.ai-workspace > .card.bslib-card > .card-header {
  background: rgba(255, 255, 255, 0.8);
  border-bottom: 1px solid var(--border);
  padding: 0.72rem 0.95rem 0.2rem;
}

.ai-workspace > .card.bslib-card > .card-body {
  padding: 1.1rem 1.2rem 1.2rem;
  overflow: visible;
}

.ai-workspace .nav-tabs .nav-link {
  font-size: 0.92rem;
  padding: 0.54rem 1.05rem;
}

.ai-workspace .tab-content,
.ai-workspace .tab-pane {
  height: 100%;
  overflow: visible;
}

.ai-tab-stack {
  display: grid;
  grid-template-rows: minmax(520px, auto) auto;
  gap: 1rem;
}

.ai-main-panel {
  min-height: 520px;
  padding: 1.25rem 1.35rem;
  margin-bottom: 0;
}

.ai-chat-panel {
  margin-bottom: 0;
  padding: 0.95rem 1.1rem;
}

.ai-main-panel .section-title {
  font-size: 0.86rem;
  margin-bottom: 0.72rem;
}

.ai-main-panel .ai-narrative {
  min-height: 170px;
  padding: 1rem 1.08rem;
  font-size: 0.93rem;
  line-height: 1.72;
}

.ai-main-panel .signal-list,
.ai-main-panel .action-list-ordered,
.ai-main-panel .cases-grid {
  gap: 0.62rem;
}

.ai-main-panel .action-card {
  padding: 0.75rem 0.85rem;
}

.ai-main-panel .case-card {
  padding: 0.72rem 0.85rem;
}

.ai-chat-panel .chat-thread {
  max-height: 220px;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
  margin: 0;
}

.metric-card {
  background: var(--surface);
  backdrop-filter: var(--blur);
  -webkit-backdrop-filter: var(--blur);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.1rem;
  box-shadow: var(--shadow);
  transition: box-shadow 0.25s, border-color 0.25s;
}

.metric-card:hover {
  box-shadow: var(--shadow-hover);
  border-color: var(--border-hover);
}

.metric-label {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--text-tertiary);
}

.metric-value {
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin-top: 0.15rem;
  font-variant-numeric: tabular-nums;
}

.metric-footnote {
  font-size: 0.78rem;
  color: var(--text-secondary);
  margin-top: 0.15rem;
}

/* ── Cohort risk distribution ── */
.cohort-risk-card {
  padding: 1rem 1.15rem 1.05rem;
}

.cohort-risk-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.cohort-risk-subtitle {
  font-size: 0.78rem;
  color: var(--text-tertiary);
}

.cohort-risk-body {
  display: grid;
  grid-template-columns: minmax(210px, 250px) 1fr;
  gap: 1rem;
  align-items: center;
}

.cohort-risk-donut-wrap {
  position: relative;
  display: grid;
  place-items: center;
  min-height: 190px;
}

.cohort-risk-donut {
  --high-pct: 0;
  width: 190px;
  height: 190px;
  border-radius: 50%;
  position: relative;
  background: conic-gradient(
    var(--red) calc(var(--high-pct) * 1%),
    var(--risk-neutral) 0
  );
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.04);
}

.cohort-risk-donut::after {
  content: "";
  position: absolute;
  inset: 26px;
  border-radius: 50%;
  background: var(--surface-solid);
  border: 1px solid var(--border);
}

.cohort-risk-center {
  position: absolute;
  z-index: 2;
  text-align: center;
}

.cohort-risk-center-value {
  font-size: 1.45rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

.cohort-risk-center-label {
  font-size: 0.74rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-tertiary);
  margin-top: 0.1rem;
}

.cohort-risk-stats {
  display: grid;
  gap: 0.5rem;
}

.cohort-risk-stat {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.56rem 0.7rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: rgba(0, 0, 0, 0.015);
}

.cohort-risk-stat-label {
  display: flex;
  align-items: center;
  gap: 0.42rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.cohort-risk-stat-label::before {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-tertiary);
  flex-shrink: 0;
}

.cohort-risk-stat-value {
  font-size: 0.94rem;
  font-weight: 650;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

.cohort-risk-stat.tone-high {
  border-color: rgba(255, 59, 48, 0.22);
  background: var(--red-soft);
}

.cohort-risk-stat.tone-high .cohort-risk-stat-label::before {
  background: var(--red);
}

.cohort-risk-stat.tone-high .cohort-risk-stat-value {
  color: var(--red);
}

.cohort-risk-stat.tone-neutral .cohort-risk-stat-label::before {
  background: #9ea5b1;
}

.cohort-risk-stat.tone-accent {
  border-color: rgba(0, 113, 227, 0.18);
  background: var(--accent-soft);
}

.cohort-risk-stat.tone-accent .cohort-risk-stat-label::before {
  background: var(--accent);
}

.cohort-risk-stat.tone-accent .cohort-risk-stat-value {
  color: var(--accent);
}

.cohort-risk-total {
  margin-top: 0.15rem;
  font-size: 0.78rem;
  color: var(--text-tertiary);
}

/* ── Panel cards ── */
.panel-card {
  background: var(--surface);
  backdrop-filter: var(--blur);
  -webkit-backdrop-filter: var(--blur);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.15rem;
  box-shadow: var(--shadow);
  margin-bottom: 0.75rem;
  transition: box-shadow 0.25s, border-color 0.25s;
}

.panel-card:hover {
  box-shadow: var(--shadow-hover);
  border-color: var(--border-hover);
}

.section-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.6rem;
}

/* ── Risk badges ── */
.badge {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 0.2rem 0.6rem;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.badge-high { color: var(--red); background: var(--red-soft); }
.badge-medium { color: var(--orange); background: var(--orange-soft); }
.badge-low { color: var(--green); background: var(--green-soft); }

/* ── Signal / driver / action lists ── */
.signal-list, .driver-list, .action-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 0.4rem;
}

.signal-item, .driver-item, .action-item {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.45;
  padding: 0.4rem 0.6rem;
  border-radius: var(--radius-sm);
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid transparent;
  transition: background 0.2s, border-color 0.2s;
}

.signal-item:hover, .driver-item:hover, .action-item:hover {
  background: rgba(0, 0, 0, 0.04);
  border-color: var(--border);
}

/* ── Profile grid ── */
.profile-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.profile-card {
  background: var(--surface);
  backdrop-filter: var(--blur);
  -webkit-backdrop-filter: var(--blur);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.9rem 1rem;
  box-shadow: var(--shadow);
}

.profile-note {
  margin-top: 0.5rem;
  font-size: 0.82rem;
  color: var(--text-secondary);
}

.profile-text {
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.55;
  margin: 0;
}

/* ── KV grid ── */
.kv-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.45rem;
}

.kv-item {
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.45rem 0.55rem;
  transition: background 0.2s;
}

.kv-item:hover { background: rgba(0, 0, 0, 0.04); }

.kv-label {
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-tertiary);
}

.kv-value {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-top: 0.05rem;
  font-variant-numeric: tabular-nums;
}

/* ── Integration / audit ── */
.integration-box {
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.65rem 0.75rem;
  background: rgba(0, 0, 0, 0.015);
}

.integration-pill {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.06em;
}

.integration-pill.tone-pass { color: var(--green); background: var(--green-soft); }
.integration-pill.tone-warn { color: var(--orange); background: var(--orange-soft); }
.integration-pill.tone-fail { color: var(--red); background: var(--red-soft); }

.integration-text { margin: 0.4rem 0 0; color: var(--text-secondary); font-size: 0.85rem; line-height: 1.4; }
.integration-subtext { margin: 0.2rem 0 0; color: var(--text-tertiary); font-size: 0.8rem; }

.audit-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.check-list { list-style: none; padding: 0; margin: 0; display: grid; gap: 0.5rem; }

.check-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.5rem;
  align-items: start;
  padding: 0.55rem 0.65rem;
  border-radius: var(--radius-sm);
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid var(--border);
}

.check-dot { width: 8px; height: 8px; margin-top: 0.3rem; border-radius: 50%; }
.check-dot.check-pass { background: var(--green); }
.check-dot.check-fail { background: var(--red); }
.check-title { font-weight: 600; font-size: 0.85rem; color: var(--text-primary); }
.check-detail { font-size: 0.8rem; color: var(--text-tertiary); margin-top: 0.1rem; }

/* ── Data grid ── */
.data-grid, .dataframe { border-radius: var(--radius-sm) !important; overflow: hidden; }

/* ── AI summary ── */
.ai-meta-item { color: var(--text-tertiary); font-size: 0.8rem; }

.ai-narrative {
  color: var(--text-secondary);
  line-height: 1.65;
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.75rem 0.85rem;
  font-size: 0.88rem;
}

.ai-alert {
  color: var(--red);
  background: var(--red-soft);
  border: 1px solid rgba(255, 59, 48, 0.2);
  border-radius: var(--radius-sm);
  padding: 0.6rem 0.75rem;
  font-size: 0.85rem;
}

.action-list-numbered {
  padding-left: 1.2rem;
  margin: 0;
  display: grid;
  gap: 0.45rem;
}

.action-list-numbered .action-item {
  font-size: 0.88rem;
  color: var(--text-secondary);
  line-height: 1.5;
  padding: 0.45rem 0.65rem;
  border-radius: var(--radius-sm);
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid transparent;
  transition: background 0.2s, border-color 0.2s;
}

.action-list-numbered .action-item:hover {
  background: rgba(0, 0, 0, 0.04);
  border-color: var(--border);
}

/* ── DB status chip ── */
.db-status {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.78rem;
  color: var(--text-tertiary);
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.03);
  border: 1px solid var(--border);
}

/* ── Responsive ── */
@media (max-width: 1100px) {
  .metric-grid { grid-template-columns: repeat(2, 1fr); }
  .profile-grid, .audit-grid { grid-template-columns: 1fr; }
  .cohort-risk-body { grid-template-columns: 1fr; gap: 0.8rem; }
  .ai-workspace > .card.bslib-card { min-height: 680px; }
  .ai-tab-stack { grid-template-rows: minmax(430px, auto) auto; }
  .ai-main-panel { min-height: 430px; }
}

@media (max-width: 768px) {
  .metric-grid { grid-template-columns: 1fr; }
  .hero-title { font-size: 1.35rem; }
  .hero-panel { padding: 1rem 1.15rem 0.85rem; }
  .kv-grid { grid-template-columns: 1fr; }
  .cohort-risk-header { flex-direction: column; align-items: flex-start; gap: 0.2rem; }
  .cohort-risk-donut { width: 170px; height: 170px; }
  .cohort-risk-donut::after { inset: 22px; }
  .ai-workspace > .card.bslib-card { min-height: 0; }
  .ai-workspace > .card.bslib-card > .card-body { padding: 0.82rem; }
  .ai-tab-stack { grid-template-rows: minmax(340px, auto) auto; gap: 0.8rem; }
  .ai-main-panel { min-height: 340px; padding: 1rem; }
  .ai-chat-panel { padding: 0.85rem 0.95rem; }
  .ai-main-panel .ai-narrative { min-height: 135px; font-size: 0.9rem; }
}

/* ── Patient header ── */
.patient-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.patient-id {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.risk-pct {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-secondary);
  font-variant-numeric: tabular-nums;
}

.ai-meta-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

/* ── Action cards ── */
.action-list-ordered {
  list-style: none;
  counter-reset: action-counter;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 0.5rem;
}

.action-card {
  counter-increment: action-counter;
  padding: 0.6rem 0.75rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: rgba(0, 0, 0, 0.015);
  transition: background 0.2s, border-color 0.2s;
}

.action-card:hover {
  background: rgba(0, 0, 0, 0.035);
  border-color: var(--border-hover);
}

.action-card::before {
  content: counter(action-counter);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px; height: 20px;
  border-radius: 50%;
  font-size: 0.68rem;
  font-weight: 700;
  margin-right: 0.5rem;
  flex-shrink: 0;
  vertical-align: middle;
}

.priority-high::before { background: var(--red-soft); color: var(--red); }
.priority-medium::before { background: var(--orange-soft); color: var(--orange); }
.priority-low::before { background: var(--green-soft); color: var(--green); }

.action-text {
  display: inline;
  font-size: 0.88rem;
  color: var(--text-primary);
  line-height: 1.45;
}

.action-rationale {
  display: block;
  margin-top: 0.2rem;
  margin-left: 2rem;
  font-size: 0.8rem;
  color: var(--text-tertiary);
  line-height: 1.4;
}

/* ── Similar case cards ── */
.cases-grid {
  display: grid;
  gap: 0.5rem;
}

.case-card {
  padding: 0.55rem 0.7rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: rgba(0, 0, 0, 0.015);
  transition: background 0.2s;
}

.case-card:hover { background: rgba(0, 0, 0, 0.035); }

.case-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.case-id {
  font-weight: 600;
  font-size: 0.88rem;
  color: var(--text-primary);
}

.case-readmit {
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.12rem 0.45rem;
  border-radius: 999px;
}

.readmit-yes { color: var(--red); background: var(--red-soft); }
.readmit-no { color: var(--green); background: var(--green-soft); }

.case-details {
  font-size: 0.8rem;
  color: var(--text-tertiary);
  margin-top: 0.15rem;
}

.pattern-insight {
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--accent);
  background: var(--accent-soft);
  border: 1px solid rgba(0, 113, 227, 0.12);
  border-radius: var(--radius-sm);
  padding: 0.55rem 0.7rem;
}

/* ── Chat dialog ── */
.chat-input-row {
  display: flex;
  gap: 0.4rem;
  align-items: flex-end;
  margin-top: 0.5rem;
}

.chat-input-row .shiny-input-container {
  flex: 1;
  margin-bottom: 0 !important;
}

.chat-input-row .form-control {
  padding: 0.45rem 0.65rem !important;
}

.btn-send {
  background: var(--accent) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  padding: 0.45rem 0.85rem !important;
  font-weight: 600 !important;
  font-size: 0.82rem !important;
  white-space: nowrap;
  transition: opacity 0.2s;
}

.btn-send:hover { opacity: 0.85; }

.chat-thread {
  display: grid;
  gap: 0.4rem;
  max-height: 280px;
  overflow-y: auto;
  padding: 0.25rem 0;
}

.chat-bubble {
  padding: 0.5rem 0.7rem;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  line-height: 1.5;
  max-width: 85%;
}

.chat-user {
  background: var(--accent);
  color: #fff;
  justify-self: end;
  border-bottom-right-radius: 4px;
}

.chat-ai {
  background: rgba(0, 0, 0, 0.04);
  color: var(--text-primary);
  border: 1px solid var(--border);
  justify-self: start;
  border-bottom-left-radius: 4px;
}

.chat-empty {
  font-size: 0.82rem;
  color: var(--text-tertiary);
  padding: 0.5rem 0;
}
"""
