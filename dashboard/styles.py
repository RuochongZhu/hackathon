CUSTOM_CSS = """
:root {
  --bg: #07111f;
  --bg-soft: #0c1a2c;
  --panel: rgba(11, 23, 39, 0.82);
  --panel-border: rgba(112, 163, 255, 0.24);
  --text: #eaf2ff;
  --muted: #9cb2d9;
  --accent: #59b0ff;
  --accent-2: #7a7dff;
  --success: #47d7ac;
  --warning: #ffb55f;
  --danger: #ff6f91;
}
body {
  background:
    radial-gradient(circle at top left, rgba(89, 176, 255, 0.20), transparent 28%),
    radial-gradient(circle at top right, rgba(122, 125, 255, 0.18), transparent 26%),
    linear-gradient(180deg, #08111d 0%, #050b14 100%);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}
.hero-shell {
  padding: 1.2rem 1.4rem 0.4rem 1.4rem;
}
.hero-panel {
  border: 1px solid rgba(120, 174, 255, 0.18);
  background: linear-gradient(135deg, rgba(14, 31, 54, 0.95), rgba(6, 16, 28, 0.88));
  border-radius: 24px;
  padding: 1.25rem 1.4rem;
  box-shadow: 0 18px 42px rgba(0, 0, 0, 0.28);
}
.hero-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-bottom: 0.35rem;
}
.hero-subtitle {
  color: var(--muted);
  font-size: 1rem;
  max-width: 940px;
}
.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.9rem;
  margin-top: 0.9rem;
}
.metric-card {
  background: linear-gradient(180deg, rgba(11, 24, 41, 0.94), rgba(8, 18, 31, 0.82));
  border: 1px solid var(--panel-border);
  border-radius: 20px;
  padding: 1rem 1rem 0.9rem;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.03), 0 16px 30px rgba(0,0,0,0.18);
}
.metric-label {
  color: var(--muted);
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.metric-value {
  font-size: 1.95rem;
  font-weight: 800;
  letter-spacing: -0.04em;
  margin-top: 0.2rem;
}
.metric-footnote {
  color: #b9c7ea;
  font-size: 0.88rem;
  margin-top: 0.35rem;
}
.panel-card {
  background: var(--panel);
  border: 1px solid var(--panel-border);
  border-radius: 22px;
  padding: 0.9rem 1rem 1rem;
  box-shadow: 0 14px 28px rgba(0,0,0,0.16);
  backdrop-filter: blur(12px);
}
.section-title {
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 0.7rem;
}
.signal-list,
.driver-list,
.action-list {
  display: grid;
  gap: 0.55rem;
  margin: 0;
  padding-left: 1rem;
}
.signal-item,
.driver-item,
.action-item {
  color: #deebff;
}
.profile-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 1rem;
}
.profile-card {
  background: rgba(9, 20, 34, 0.88);
  border: 1px solid var(--panel-border);
  border-radius: 20px;
  padding: 1rem;
}
.kv-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.7rem;
}
.kv-item {
  padding: 0.7rem 0.8rem;
  border-radius: 14px;
  background: rgba(13, 27, 46, 0.85);
  border: 1px solid rgba(113, 166, 255, 0.12);
}
.kv-label {
  color: var(--muted);
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}
.kv-value {
  font-size: 1rem;
  font-weight: 700;
  margin-top: 0.2rem;
}
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.8rem;
}
.badge-high { background: rgba(255,111,145,0.16); color: #ff9ab1; }
.badge-medium { background: rgba(255,181,95,0.16); color: #ffd29a; }
.badge-low { background: rgba(71,215,172,0.16); color: #8ff1d0; }
.shiny-input-container, .control-label {
  color: var(--text) !important;
}
.bslib-sidebar-layout > .sidebar {
  background: rgba(7, 18, 31, 0.95) !important;
  border-right: 1px solid rgba(123, 163, 255, 0.16);
}
.nav-tabs .nav-link,
.nav-pills .nav-link {
  color: #bfd2fb;
}
.nav-tabs .nav-link.active,
.nav-pills .nav-link.active {
  background: linear-gradient(135deg, rgba(89,176,255,0.18), rgba(122,125,255,0.18));
  color: #ffffff;
  border: 1px solid rgba(113, 166, 255, 0.22);
}
.data-grid, .dataframe {
  border-radius: 18px !important;
  overflow: hidden;
}
.ai-summary {
  display: grid;
  gap: 0.85rem;
}
.ai-meta-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
}
.ai-meta-item {
  color: #b8cef7;
  font-size: 0.88rem;
}
.ai-risk-summary {
  color: #e5efff;
  line-height: 1.65;
  background: rgba(15, 30, 51, 0.65);
  border: 1px solid rgba(113, 166, 255, 0.18);
  border-radius: 14px;
  padding: 0.8rem 0.9rem;
}
.ai-section {
  display: grid;
  gap: 0.45rem;
}
.ai-section-title {
  color: #d2e3ff;
  font-size: 0.92rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.ai-alert {
  color: #ffbac9;
  background: rgba(255, 111, 145, 0.14);
  border: 1px solid rgba(255, 111, 145, 0.35);
  border-radius: 14px;
  padding: 0.75rem 0.9rem;
}
@media (max-width: 1100px) {
  .metric-grid, .profile-grid {
    grid-template-columns: 1fr;
  }
}
"""
