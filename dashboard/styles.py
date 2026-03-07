CUSTOM_CSS = """
:root {
  /* Main colors */
  --primary: #0071e3;
  --bg: #f5f5f7;
  --surface: rgba(255, 255, 255, 0.72);
  --surface-solid: #ffffff;

  /* Borders and shadows */
  --border: rgba(0, 0, 0, 0.08);
  --border-hover: rgba(0, 0, 0, 0.12);
  --shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
  --shadow-hover: 0 4px 24px rgba(0, 0, 0, 0.10);

  /* Text hierarchy */
  --text-primary: #1d1d1f;
  --text-secondary: #6e6e73;
  --text-tertiary: #aeaeb2;

  /* Risk colors */
  --risk-high: #ff3b30;
  --risk-medium: #ff9500;
  --risk-low: #34c759;
  --risk-high-soft: rgba(255, 59, 48, 0.08);
  --risk-medium-soft: rgba(255, 149, 0, 0.08);
  --risk-low-soft: rgba(52, 199, 89, 0.08);

  /* Spacing system (8px grid) */
  --spacing-xs: 0.25rem;   /* 4px */
  --spacing-sm: 0.5rem;    /* 8px */
  --spacing-md: 1rem;      /* 16px */
  --spacing-lg: 1.5rem;    /* 24px */
  --spacing-xl: 2rem;      /* 32px */
  --spacing-2xl: 3rem;     /* 48px */

  /* Typography scale */
  --text-xs: 0.64rem;   /* 10px */
  --text-sm: 0.8rem;    /* 13px */
  --text-base: 1rem;    /* 16px */
  --text-lg: 1.25rem;   /* 20px */
  --text-xl: 1.563rem;  /* 25px */
  --text-2xl: 1.953rem; /* 31px */

  /* Border radius */
  --radius: 16px;
  --radius-sm: 10px;

  /* Effects */
  --blur: blur(40px) saturate(180%);
}

*, *::before, *::after {
  box-sizing: border-box;
}

html, body {
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Global transitions */
* {
  transition-property: background-color, border-color, color, opacity, transform;
  transition-duration: 0.2s;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Disable transitions for animations */
*:where([class*="animate-"], [class*="pulse-"]) {
  transition: none;
}

body {
  background: var(--bg);
  color: var(--text-primary);
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif;
  font-size: var(--text-base);
  line-height: 1.6;
}

/* ── Hero ── */
.hero-shell { padding: var(--spacing-lg) var(--spacing-xl) 0; }

.hero-panel {
  background: var(--surface);
  backdrop-filter: var(--blur);
  -webkit-backdrop-filter: var(--blur);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--spacing-xl) var(--spacing-2xl) var(--spacing-lg);
  box-shadow: var(--shadow);
}

.hero-title {
  font-size: var(--text-2xl);
  font-weight: 700;
  letter-spacing: -0.025em;
  color: var(--text-primary);
}

.hero-subtitle {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-top: var(--spacing-xs);
  max-width: 680px;
}

.hero-meta {
  display: flex;
  gap: var(--spacing-xl);
  margin-top: var(--spacing-md);
  flex-wrap: wrap;
}

.hero-meta-item {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

/* ── Sidebar ── */
.bslib-sidebar-layout > .sidebar {
  background: var(--surface) !important;
  backdrop-filter: var(--blur) !important;
  -webkit-backdrop-filter: var(--blur) !important;
  border-right: 1px solid var(--border) !important;
}

.sidebar-section-label {
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-tertiary);
  margin: var(--spacing-md) 0 var(--spacing-sm);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.shiny-input-container,
.control-label,
.shiny-input-container .form-check-label {
  color: var(--text-primary) !important;
  font-size: var(--text-sm) !important;
}

.form-control, .form-select {
  border-radius: var(--radius-sm) !important;
  border: 1px solid var(--border) !important;
  background: var(--surface-solid) !important;
  font-size: var(--text-sm) !important;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-control:focus, .form-select:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.08) !important;
}

/* ── Tabs ── */
.nav-tabs, .nav-pills { border-bottom: 1px solid var(--border); }

.nav-tabs .nav-link, .nav-pills .nav-link {
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-weight: 500;
  font-size: var(--text-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  transition: all 0.2s ease;
}

.nav-tabs .nav-link:hover, .nav-pills .nav-link:hover {
  color: var(--text-primary);
  background: rgba(0, 0, 0, 0.03);
  transform: translateY(-1px);
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
  gap: var(--spacing-md);
  margin: var(--spacing-md) 0;
}

/* ── AI workspace ── */
.ai-workspace {
  margin: var(--spacing-sm) 0;
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
  padding: var(--spacing-md) var(--spacing-lg) var(--spacing-sm);
}

.ai-workspace > .card.bslib-card > .card-body {
  padding: var(--spacing-lg) var(--spacing-xl);
  overflow: visible;
}

.ai-workspace .nav-tabs .nav-link {
  font-size: var(--text-base);
  padding: var(--spacing-sm) var(--spacing-lg);
}

.ai-workspace .tab-content,
.ai-workspace .tab-pane {
  height: 100%;
  overflow: visible;
}

.ai-tab-stack {
  display: grid;
  grid-template-rows: minmax(520px, auto) auto;
  gap: var(--spacing-lg);
}

.ai-main-panel {
  min-height: 520px;
  padding: var(--spacing-xl) var(--spacing-2xl);
  margin-bottom: 0;
}

.ai-chat-panel {
  margin-bottom: 0;
  padding: var(--spacing-lg) var(--spacing-xl);
}

.ai-main-panel .section-title {
  font-size: var(--text-lg);
  margin-bottom: var(--spacing-md);
}

.ai-main-panel .ai-narrative {
  min-height: 170px;
  padding: var(--spacing-lg) var(--spacing-xl);
  font-size: var(--text-base);
  line-height: 1.7;
}

.ai-main-panel .signal-list,
.ai-main-panel .action-list-ordered,
.ai-main-panel .cases-grid {
  gap: var(--spacing-sm);
}

.ai-main-panel .action-card {
  padding: var(--spacing-md) var(--spacing-lg);
}

.ai-main-panel .case-card {
  padding: var(--spacing-md) var(--spacing-lg);
}

.ai-chat-panel .chat-thread {
  max-height: 220px;
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.85rem;
  align-items: stretch;
}

.charts-row .panel-card {
  min-height: 400px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
  margin: 0;
}

.metric-card {
  background: var(--surface);
  backdrop-filter: var(--blur);
  -webkit-backdrop-filter: var(--blur);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--spacing-lg) var(--spacing-xl);
  box-shadow: var(--shadow);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover);
  border-color: var(--border-hover);
}

.metric-label {
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--text-tertiary);
}

.metric-value {
  font-size: var(--text-xl);
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin-top: var(--spacing-xs);
  font-variant-numeric: tabular-nums;
}

.metric-footnote {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-top: var(--spacing-xs);
}

/* ── Mosaic plot (embedded in Shiny) ── */
.mosaic-card {
  padding: 1rem 1.15rem;
}

.mosaic-subtitle {
  font-size: 0.78rem;
  color: var(--text-tertiary);
  margin-bottom: 0.75rem;
}

.mosaic-wrap {
  width: 100%;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: rgba(0, 0, 0, 0.02);
  overflow: hidden;
}

.mosaic-svg-wrap {
  width: 100%;
  line-height: 0;
}

.mosaic-svg {
  width: 100%;
  display: block;
}

.mosaic-empty {
  padding: 2rem;
  text-align: center;
  color: var(--text-tertiary);
  font-size: 0.9rem;
}

.mosaic-legend {
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.mosaic-legend-swatch {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 2px;
  margin-right: 0.2rem;
  vertical-align: middle;
}

/* ── Box plot (embedded in Shiny) ── */
.boxplot-card {
  padding: var(--spacing-lg) var(--spacing-xl);
}

.boxplot-wrap {
  width: 100%;
  border-radius: var(--radius-sm);
  background: rgba(0, 0, 0, 0.015);
  overflow: hidden;
  margin-top: var(--spacing-sm);
}

.boxplot-svg-wrap {
  width: 100%;
  line-height: 0;
}

.boxplot-svg {
  display: block;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
}

/* ── Cohort risk distribution ── */
.cohort-risk-card {
  padding: var(--spacing-lg) var(--spacing-xl);
}

.cohort-risk-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--spacing-xs);
  margin-bottom: 0.95rem;
}

.cohort-risk-subtitle {
  font-size: 0.78rem;
  color: var(--text-tertiary);
  line-height: 1.35;
}

.cohort-risk-body {
  display: grid;
  grid-template-columns: minmax(272px, 1.2fr) minmax(186px, 0.8fr);
  gap: var(--spacing-md);
  align-items: stretch;
  min-height: 340px;
  flex: 1;
}

.cohort-risk-donut-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 340px;
  padding: var(--spacing-sm) 0;
}

.cohort-risk-donut {
  --high-pct: 0;
  width: 236px;
  height: 236px;
  border-radius: 50%;
  position: relative;
  margin-inline: auto;
  background: conic-gradient(
    var(--risk-high) calc(var(--high-pct) * 1%),
    #d8dee7 0
  );
  box-shadow:
    inset 0 0 0 1px rgba(0, 0, 0, 0.04),
    0 12px 28px rgba(255, 59, 48, 0.10);
}

.cohort-risk-donut::after {
  content: "";
  position: absolute;
  inset: 30px;
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
  font-size: clamp(1.65rem, 2.4vw, 1.95rem);
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

.cohort-risk-center-label {
  font-size: 0.58rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-tertiary);
  margin-top: var(--spacing-xs);
}

.cohort-risk-stats {
  display: grid;
  gap: 0.42rem;
  align-self: stretch;
  align-content: center;
  justify-self: end;
  max-width: 220px;
}

.cohort-risk-stat {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-sm);
  padding: 0.34rem 0.54rem;
  border-radius: var(--radius-sm);
  border: 1px solid rgba(0, 0, 0, 0.055);
  background: rgba(0, 0, 0, 0.008);
}

.cohort-risk-stat-label {
  display: flex;
  align-items: center;
  gap: 0.34rem;
  font-size: var(--text-xs);
  color: var(--text-secondary);
  opacity: 0.9;
}

.cohort-risk-stat-label::before {
  content: "";
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--text-tertiary);
  flex-shrink: 0;
}

.cohort-risk-stat-value {
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

.cohort-risk-stat.tone-high {
  border-color: rgba(255, 59, 48, 0.14);
  background: rgba(255, 59, 48, 0.05);
}

.cohort-risk-stat.tone-high .cohort-risk-stat-label::before {
  background: var(--risk-high);
}

.cohort-risk-stat.tone-high .cohort-risk-stat-value {
  color: #cf6d67;
}

.cohort-risk-stat.tone-neutral .cohort-risk-stat-label::before {
  background: #9ea5b1;
}

.cohort-risk-stat.tone-accent {
  border-color: rgba(0, 113, 227, 0.12);
  background: rgba(0, 113, 227, 0.045);
}

.cohort-risk-stat.tone-accent .cohort-risk-stat-label::before {
  background: var(--primary);
}

.cohort-risk-stat.tone-accent .cohort-risk-stat-value {
  color: #5f84a9;
}

.cohort-risk-total {
  margin-top: 0.1rem;
  font-size: 0.7rem;
  color: var(--text-tertiary);
  opacity: 0.92;
}

/* ── Panel cards ── */
.panel-card {
  background: var(--surface);
  backdrop-filter: var(--blur);
  -webkit-backdrop-filter: var(--blur);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--spacing-lg) var(--spacing-xl);
  box-shadow: var(--shadow);
  margin-bottom: var(--spacing-md);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.panel-card:hover {
  box-shadow: var(--shadow-hover);
  border-color: var(--border-hover);
}

.section-title {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

/* ── Risk badges ── */
.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  border-radius: 999px;
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.04em;
  transition: all 0.2s ease;
}

.badge-high {
  color: var(--risk-high);
  background: var(--risk-high-soft);
  animation: pulse-high 2s ease-in-out infinite;
}

.badge-medium {
  color: var(--risk-medium);
  background: var(--risk-medium-soft);
}

.badge-low {
  color: var(--risk-low);
  background: var(--risk-low-soft);
}

@keyframes pulse-high {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* ── Signal / driver / action lists ── */
.signal-list, .driver-list, .action-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: var(--spacing-sm);
}

.signal-item, .driver-item, .action-item {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.5;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-sm);
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.signal-item:hover, .driver-item:hover, .action-item:hover {
  background: rgba(0, 0, 0, 0.04);
  border-color: var(--border);
  transform: translateX(2px);
}

/* ── Profile grid ── */
.profile-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.profile-card {
  background: var(--surface);
  backdrop-filter: var(--blur);
  -webkit-backdrop-filter: var(--blur);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--spacing-lg) var(--spacing-xl);
  box-shadow: var(--shadow);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.profile-card:hover {
  box-shadow: var(--shadow-hover);
  border-color: var(--border-hover);
}

.profile-note {
  margin-top: var(--spacing-sm);
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.profile-text {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

/* ── KV grid ── */
.kv-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-sm);
}

.kv-item {
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  transition: all 0.2s ease;
}

.kv-item:hover {
  background: rgba(0, 0, 0, 0.04);
  transform: translateY(-1px);
}

.kv-label {
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-tertiary);
}

.kv-value {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-primary);
  margin-top: var(--spacing-xs);
  font-variant-numeric: tabular-nums;
}

/* ── Integration / audit ── */
.integration-box {
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  background: rgba(0, 0, 0, 0.015);
  transition: all 0.2s ease;
}

.integration-box:hover {
  background: rgba(0, 0, 0, 0.025);
}

.integration-pill {
  display: inline-block;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: 999px;
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.06em;
}

.integration-pill.tone-pass { color: var(--risk-low); background: var(--risk-low-soft); }
.integration-pill.tone-warn { color: var(--risk-medium); background: var(--risk-medium-soft); }
.integration-pill.tone-fail { color: var(--risk-high); background: var(--risk-high-soft); }

.integration-text {
  margin: var(--spacing-sm) 0 0;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.5;
}

.integration-subtext {
  margin: var(--spacing-xs) 0 0;
  color: var(--text-tertiary);
  font-size: var(--text-sm);
}

.audit-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
}

.check-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: var(--spacing-sm);
}

.check-item {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: var(--spacing-sm);
  align-items: start;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-sm);
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid var(--border);
  transition: all 0.2s ease;
}

.check-item:hover {
  background: rgba(0, 0, 0, 0.04);
}

.check-dot {
  width: 8px;
  height: 8px;
  margin-top: 0.3rem;
  border-radius: 50%;
}

.check-dot.check-pass { background: var(--risk-low); }
.check-dot.check-fail { background: var(--risk-high); }

.check-title {
  font-weight: 600;
  font-size: var(--text-sm);
  color: var(--text-primary);
}

.check-detail {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  margin-top: var(--spacing-xs);
}

/* ── Data grid ── */
.data-grid, .dataframe {
  border-radius: var(--radius-sm) !important;
  overflow: hidden;
  border: 1px solid var(--border) !important;
}

/* ── DB status chip ── */
.db-status {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.03);
  border: 1px solid var(--border);
}

/* ── Action list numbered ── */
.action-list-numbered {
  padding-left: 1.2rem;
  margin: 0;
  display: grid;
  gap: var(--spacing-sm);
}

.action-list-numbered .action-item {
  font-size: var(--text-base);
  color: var(--text-secondary);
  line-height: 1.5;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-sm);
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.action-list-numbered .action-item:hover {
  background: rgba(0, 0, 0, 0.04);
  border-color: var(--border);
  transform: translateX(2px);
}
.ai-meta-item {
  color: var(--text-tertiary);
  font-size: var(--text-sm);
}

.ai-narrative {
  color: var(--text-secondary);
  line-height: 1.7;
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--text-base);
}

.ai-narrative::first-letter {
  font-size: 1.5em;
  font-weight: 700;
  color: var(--primary);
  float: left;
  line-height: 1;
  margin-right: 0.1em;
}

.ai-alert {
  color: var(--risk-high);
  background: var(--risk-high-soft);
  border: 1px solid rgba(255, 59, 48, 0.2);
  border-radius: var(--radius-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--text-sm);
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

/* ── Icon styles ── */
.icon {
  display: inline-block;
  vertical-align: middle;
  stroke: currentColor;
  fill: none;
  flex-shrink: 0;
}

.hero-icon {
  color: var(--text-tertiary);
}

.hero-icon-green {
  color: var(--risk-low);
}

.hero-icon-red {
  color: var(--risk-high);
}

.section-icon {
  color: var(--text-tertiary);
}

.tab-icon {
  flex-shrink: 0;
}

.badge-icon {
  flex-shrink: 0;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

/* ── Scrollbar styling ── */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.15);
  border-radius: 999px;
  transition: background 0.2s;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.25);
}

/* Firefox scrollbar */
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.15) transparent;
}

/* ── Loading states ── */
@keyframes skeleton-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.04) 25%,
    rgba(0, 0, 0, 0.08) 50%,
    rgba(0, 0, 0, 0.04) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
  border-radius: var(--radius-sm);
}

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spinner-rotate 0.6s linear infinite;
}

@keyframes spinner-rotate {
  to { transform: rotate(360deg); }
}

/* ── Fade in animation ── */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.3s ease-out;
}

/* ── Focus styles ── */
*:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

button:focus-visible,
.btn:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

/* ── Selection styles ── */
::selection {
  background: rgba(0, 113, 227, 0.2);
  color: var(--text-primary);
}

::-moz-selection {
  background: rgba(0, 113, 227, 0.2);
  color: var(--text-primary);
}

/* ── Responsive ── */
@media (max-width: 1100px) {
  .metric-grid { grid-template-columns: repeat(2, 1fr); }
  .profile-grid, .audit-grid { grid-template-columns: 1fr; }
  .cohort-risk-body { grid-template-columns: 1fr; gap: var(--spacing-md); min-height: 0; }
  .cohort-risk-donut-wrap { min-height: 288px; padding-bottom: var(--spacing-sm); }
  .cohort-risk-stats { max-width: none; width: 100%; justify-self: stretch; }
  .ai-workspace > .card.bslib-card { min-height: 680px; }
  .ai-tab-stack { grid-template-rows: minmax(430px, auto) auto; }
  .ai-main-panel { min-height: 430px; }
  .charts-row { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  :root {
    --spacing-lg: 1rem;
    --spacing-xl: 1.5rem;
  }

  .metric-grid { grid-template-columns: 1fr; }
  .hero-title { font-size: var(--text-xl); }
  .hero-panel { padding: var(--spacing-lg) var(--spacing-xl); }
  .kv-grid { grid-template-columns: 1fr; }
  .cohort-risk-header { margin-bottom: var(--spacing-sm); }
  .cohort-risk-donut-wrap { min-height: 236px; padding-bottom: var(--spacing-sm); }
  .cohort-risk-donut { width: 184px; height: 184px; }
  .cohort-risk-donut::after { inset: 24px; }
  .ai-workspace > .card.bslib-card { min-height: 0; }
  .ai-workspace > .card.bslib-card > .card-body { padding: var(--spacing-md); }
  .ai-tab-stack { grid-template-rows: minmax(340px, auto) auto; gap: var(--spacing-md); }
  .ai-main-panel { min-height: 340px; padding: var(--spacing-lg); }
  .ai-chat-panel { padding: var(--spacing-md); }
  .ai-main-panel .ai-narrative { min-height: 135px; font-size: var(--text-sm); }
  .metric-card { padding: var(--spacing-md); }
}

/* ── Patient header ── */
.patient-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.patient-id {
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.risk-pct {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-secondary);
  font-variant-numeric: tabular-nums;
}

.ai-meta-row {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

/* ── Action cards ── */
.action-list-ordered {
  list-style: none;
  counter-reset: action-counter;
  padding: 0;
  margin: 0;
  display: grid;
  gap: var(--spacing-sm);
}

.action-card {
  counter-increment: action-counter;
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: rgba(0, 0, 0, 0.015);
  transition: all 0.2s ease;
}

.action-card:hover {
  background: rgba(0, 0, 0, 0.035);
  border-color: var(--border-hover);
  transform: translateX(2px);
}

.action-card::before {
  content: counter(action-counter);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px; height: 20px;
  border-radius: 50%;
  font-size: var(--text-xs);
  font-weight: 700;
  margin-right: var(--spacing-sm);
  flex-shrink: 0;
  vertical-align: middle;
}

.priority-high::before { background: var(--risk-high-soft); color: var(--risk-high); }
.priority-medium::before { background: var(--risk-medium-soft); color: var(--risk-medium); }
.priority-low::before { background: var(--risk-low-soft); color: var(--risk-low); }

.action-text {
  display: inline;
  font-size: var(--text-base);
  color: var(--text-primary);
  line-height: 1.5;
}

.action-rationale {
  display: block;
  margin-top: var(--spacing-xs);
  margin-left: 2rem;
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  line-height: 1.4;
}

/* ── Similar case cards ── */
.cases-grid {
  display: grid;
  gap: var(--spacing-sm);
}

.case-card {
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: rgba(0, 0, 0, 0.015);
  transition: all 0.2s ease;
}

.case-card:hover {
  background: rgba(0, 0, 0, 0.035);
  transform: translateX(2px);
}

.case-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.case-id {
  font-weight: 600;
  font-size: var(--text-base);
  color: var(--text-primary);
}

.case-readmit {
  font-size: var(--text-xs);
  font-weight: 600;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: 999px;
}

.readmit-yes { color: var(--risk-high); background: var(--risk-high-soft); }
.readmit-no { color: var(--risk-low); background: var(--risk-low-soft); }

.case-details {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  margin-top: var(--spacing-xs);
}

.pattern-insight {
  font-size: var(--text-base);
  font-weight: 500;
  color: var(--primary);
  background: rgba(0, 113, 227, 0.08);
  border: 1px solid rgba(0, 113, 227, 0.12);
  border-radius: var(--radius-sm);
  padding: var(--spacing-sm) var(--spacing-md);
}

/* ── Chat dialog ── */
.chat-input-row {
  display: flex;
  gap: var(--spacing-sm);
  align-items: flex-end;
  margin-top: var(--spacing-sm);
}

.chat-input-row .shiny-input-container {
  flex: 1;
  margin-bottom: 0 !important;
}

.chat-input-row .form-control {
  padding: var(--spacing-sm) var(--spacing-md) !important;
}

.btn-send {
  background: var(--primary) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  padding: var(--spacing-sm) var(--spacing-lg) !important;
  font-weight: 600 !important;
  font-size: var(--text-sm) !important;
  white-space: nowrap;
  transition: opacity 0.2s;
}

.btn-send:hover { opacity: 0.85; }

.chat-thread {
  display: grid;
  gap: var(--spacing-sm);
  max-height: 280px;
  overflow-y: auto;
  padding: var(--spacing-xs) 0;
}

.chat-bubble {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
  line-height: 1.5;
  max-width: 85%;
}

.chat-user {
  background: var(--primary);
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
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  padding: var(--spacing-sm) 0;
}
"""
