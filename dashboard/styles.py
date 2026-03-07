CUSTOM_CSS = """
:root {
  --bg-1: #eef5f8;
  --bg-2: #e7f1f5;
  --panel: rgba(255, 255, 255, 0.88);
  --panel-border: rgba(36, 88, 107, 0.16);
  --panel-shadow: 0 14px 34px rgba(23, 60, 72, 0.12);
  --text: #12313d;
  --muted: #557684;
  --accent: #0f9ea8;
  --accent-soft: rgba(15, 158, 168, 0.14);
  --blue: #2a86d1;
  --success: #0f8f5a;
  --warning: #c27a12;
  --danger: #c64343;
}

* {
  box-sizing: border-box;
}

html,
body {
  min-height: 100%;
}

body {
  position: relative;
  overflow-x: hidden;
  color: var(--text);
  font-family: "IBM Plex Sans", "Helvetica Neue", sans-serif;
  background:
    radial-gradient(circle at 10% -10%, rgba(38, 140, 193, 0.18), transparent 36%),
    radial-gradient(circle at 92% -6%, rgba(15, 158, 168, 0.16), transparent 34%),
    linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%);
}

.bg-orb {
  position: fixed;
  width: 380px;
  height: 380px;
  border-radius: 999px;
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
}

.bg-orb-a {
  top: -130px;
  right: -110px;
  background: rgba(42, 134, 209, 0.22);
}

.bg-orb-b {
  bottom: -160px;
  left: -120px;
  background: rgba(15, 158, 168, 0.18);
}

.hero-shell,
.bslib-sidebar-layout {
  position: relative;
  z-index: 2;
}

.hero-shell {
  padding: 1.2rem 1.35rem 0.45rem;
}

.hero-panel {
  border: 1px solid rgba(31, 97, 121, 0.18);
  background: linear-gradient(125deg, rgba(13, 53, 71, 0.96), rgba(11, 32, 56, 0.96));
  border-radius: 24px;
  padding: 1.2rem 1.35rem 1rem;
  box-shadow: 0 20px 42px rgba(17, 45, 58, 0.28);
}

.hero-title {
  font-family: "Manrope", "IBM Plex Sans", sans-serif;
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: #f0fbff;
  margin-bottom: 0.2rem;
}

.hero-subtitle {
  font-size: 1rem;
  color: rgba(217, 241, 248, 0.9);
  max-width: 980px;
}

.status-chip-row {
  margin-top: 0.9rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.status-chip {
  min-width: 130px;
  padding: 0.46rem 0.68rem;
  border-radius: 12px;
  border: 1px solid rgba(153, 201, 220, 0.24);
  background: rgba(255, 255, 255, 0.08);
}

.status-chip-label {
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(205, 231, 239, 0.9);
}

.status-chip-value {
  margin-top: 0.12rem;
  font-size: 0.9rem;
  font-weight: 700;
  color: #ffffff;
}

.status-chip.tone-pass {
  border-color: rgba(30, 197, 131, 0.35);
  background: rgba(20, 173, 117, 0.16);
}

.status-chip.tone-warn {
  border-color: rgba(237, 183, 95, 0.46);
  background: rgba(226, 162, 44, 0.18);
}

.status-chip.tone-fail {
  border-color: rgba(255, 120, 120, 0.4);
  background: rgba(189, 66, 66, 0.18);
}

.status-chip.tone-neutral {
  border-color: rgba(153, 201, 220, 0.35);
}

.bslib-sidebar-layout > .sidebar {
  background: linear-gradient(180deg, rgba(7, 34, 52, 0.98), rgba(5, 27, 42, 0.98)) !important;
  border-right: 1px solid rgba(107, 165, 188, 0.24);
}

.sidebar-group-title {
  margin: 0.25rem 0 0.45rem;
  font-family: "Manrope", sans-serif;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: #c5ebf8;
}

.sidebar-note {
  color: #9fc4d2;
  font-size: 0.84rem;
  margin-top: 0.2rem;
  line-height: 1.35;
}

.sidebar-list {
  padding-left: 1rem;
  color: #d4edf7;
  margin-bottom: 0;
}

.sidebar-list li {
  margin-bottom: 0.25rem;
}

.shiny-input-container,
.control-label,
.shiny-input-container .form-check-label {
  color: #e5f4fb !important;
}

.nav-tabs,
.nav-pills {
  border-bottom-color: rgba(41, 93, 113, 0.22);
}

.nav-tabs .nav-link,
.nav-pills .nav-link {
  border-radius: 10px;
  color: #447083;
  font-weight: 700;
}

.nav-tabs .nav-link.active,
.nav-pills .nav-link.active {
  color: #f7feff;
  border-color: rgba(17, 118, 150, 0.24);
  background: linear-gradient(135deg, #1a9ba8, #1f7fc9);
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 0.82rem;
  margin-top: 0.8rem;
  margin-bottom: 0.25rem;
}

.metric-card,
.panel-card,
.profile-card {
  background: var(--panel);
  border: 1px solid var(--panel-border);
  box-shadow: var(--panel-shadow);
}

.metric-card {
  border-radius: 16px;
  padding: 0.85rem 0.92rem;
}

.metric-label {
  color: #507181;
  font-size: 0.76rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 600;
}

.metric-value {
  font-family: "Manrope", sans-serif;
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  margin-top: 0.08rem;
  color: #12313d;
}

.metric-footnote {
  color: #5a7b89;
  font-size: 0.84rem;
  margin-top: 0.2rem;
  line-height: 1.28;
}

.panel-card {
  border-radius: 16px;
  padding: 0.86rem 0.95rem 0.95rem;
  margin-bottom: 0.95rem;
}

.section-title {
  font-family: "Manrope", sans-serif;
  font-size: 1.02rem;
  font-weight: 700;
  color: #153743;
  margin-bottom: 0.66rem;
}

.signal-list,
.driver-list,
.action-list {
  display: grid;
  gap: 0.56rem;
  margin: 0;
  padding-left: 1rem;
}

.signal-item,
.driver-item,
.action-item {
  color: #1b4453;
  line-height: 1.4;
}

.profile-grid {
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 0.88rem;
}

.profile-card {
  border-radius: 15px;
  padding: 0.88rem;
}

.profile-note {
  margin-top: 0.7rem;
  color: #496a79;
}

.profile-text {
  color: #1f4553;
  line-height: 1.58;
  margin: 0;
}

.kv-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.58rem;
}

.kv-item {
  background: rgba(231, 243, 247, 0.95);
  border: 1px solid rgba(42, 117, 147, 0.16);
  border-radius: 12px;
  padding: 0.58rem 0.66rem;
}

.kv-label {
  font-size: 0.73rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #547785;
}

.kv-value {
  margin-top: 0.14rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: #173845;
}

.badge {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 0.26rem 0.68rem;
  font-size: 0.76rem;
  font-weight: 800;
  letter-spacing: 0.06em;
}

.badge-high {
  color: #ffffff;
  background: #d64d4d;
}

.badge-medium {
  color: #ffffff;
  background: #d08c1f;
}

.badge-low {
  color: #ffffff;
  background: #128a62;
}

.integration-box {
  border: 1px solid rgba(52, 126, 149, 0.2);
  border-radius: 12px;
  padding: 0.75rem;
  background: rgba(241, 250, 253, 0.92);
}

.integration-pill {
  display: inline-block;
  padding: 0.18rem 0.56rem;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.integration-pill.tone-pass {
  color: #ffffff;
  background: var(--success);
}

.integration-pill.tone-warn {
  color: #ffffff;
  background: var(--warning);
}

.integration-pill.tone-fail {
  color: #ffffff;
  background: var(--danger);
}

.integration-text {
  margin: 0.55rem 0 0;
  color: #1f4454;
  line-height: 1.38;
}

.integration-subtext {
  margin: 0.35rem 0 0;
  color: #567a88;
  font-size: 0.86rem;
}

.audit-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.8rem;
}

.check-list {
  display: grid;
  gap: 0.66rem;
  list-style: none;
  padding: 0;
  margin: 0;
}

.check-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.55rem;
  align-items: start;
  padding: 0.65rem 0.74rem;
  border-radius: 12px;
  background: rgba(243, 250, 253, 0.9);
  border: 1px solid rgba(74, 132, 150, 0.16);
}

.check-dot {
  width: 10px;
  height: 10px;
  margin-top: 0.35rem;
  border-radius: 999px;
}

.check-dot.check-pass {
  background: var(--success);
}

.check-dot.check-fail {
  background: var(--danger);
}

.check-title {
  font-weight: 700;
  color: #173f4d;
}

.check-detail {
  margin-top: 0.15rem;
  color: #567785;
  font-size: 0.86rem;
}

.data-grid,
.dataframe {
  border-radius: 12px !important;
  overflow: hidden;
}

.form-control,
.form-select {
  border-radius: 10px !important;
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

@media (max-width: 1200px) {
  .profile-grid,
  .audit-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .hero-title {
    font-size: 1.6rem;
  }

  .status-chip {
    min-width: 110px;
  }
}
"""
