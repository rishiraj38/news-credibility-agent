"""
Veritas AI — Precision-Industrial News Credibility Analyzer UI.
World-class flat design. No gradients. SVG icons. Fully responsive.
Tabs: Analyzer | Architecture & Workflow.
"""

import gradio as gr
import json
from agent.graph import run_analysis


def analyze(input_text: str):
    """Analyze article and return results."""
    if not input_text or not input_text.strip():
        return "Error", 0, json.dumps({"error": "No input provided"}, indent=2)

    try:
        is_url = input_text.strip().startswith("http")
        report = run_analysis(input_text, article_url=input_text if is_url else None)

        verdict = report.get("verdict", {})

        if "Failed to extract content from URL" in str(report):
            return "Extraction Error", 0, json.dumps(report, indent=2)

        return (
            verdict.get("credibility", "Unknown"),
            verdict.get("confidence_score", 0),
            json.dumps(report, indent=2),
        )

    except Exception as e:
        print(f"Error: {e}")
        return "Error", 0, json.dumps({"error": str(e)}, indent=2)


# ─────────────────────────────────────────────────────────────
#  SVG ICON HELPERS
# ─────────────────────────────────────────────────────────────

def svg(path_d, size=16, stroke="#6b7a8d", fill="none", stroke_width=1.6):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
        f'{path_d}</svg>'
    )

ICON_SHIELD    = svg('<path d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.25C17.25 22.15 21 17.25 21 12V7z"/>', stroke="#00c4ff")
ICON_CPU       = svg('<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/>', stroke="#00c4ff")
ICON_DATABASE  = svg('<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>', stroke="#6b7a8d")
ICON_NETWORK   = svg('<circle cx="12" cy="5" r="3"/><line x1="12" y1="8" x2="12" y2="16"/><circle cx="5" cy="19" r="3"/><circle cx="19" cy="19" r="3"/><line x1="12" y1="16" x2="5" y2="17"/><line x1="12" y1="16" x2="19" y2="17"/>', stroke="#6b7a8d")
ICON_ACTIVITY  = svg('<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>', stroke="#00c4ff")
ICON_SEARCH    = svg('<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>', stroke="#6b7a8d")
ICON_ALERT     = svg('<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>', stroke="#6b7a8d")
ICON_CODE      = svg('<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>', stroke="#6b7a8d")
ICON_ZAP       = svg('<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>', stroke="#00c4ff", fill="#00c4ff")
ICON_LAYERS    = svg('<rect x="2" y="3" width="20" height="4" rx="1"/><rect x="2" y="10" width="20" height="4" rx="1"/><rect x="2" y="17" width="20" height="4" rx="1"/>', stroke="#6b7a8d")
ICON_FILTER    = svg('<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>', stroke="#6b7a8d")
ICON_FLAG      = svg('<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/>', stroke="#6b7a8d")


# ─────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────

CSS = """
/* ── Reset & Global ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg-base:    #07090e;
    --bg-surface: #0d1117;
    --bg-raised:  #111820;
    --bg-hover:   #151d26;
    --border:     #1c2536;
    --border-hi:  #273347;
    --accent:     #00c4ff;
    --accent-dim: #005f7a;
    --success:    #00c853;
    --warning:    #ffab00;
    --danger:     #ff3d5a;
    --txt-1:      #dce6f0;
    --txt-2:      #8596aa;
    --txt-3:      #4a5668;
    --mono:       'IBM Plex Mono', monospace;
    --sans:       'DM Sans', sans-serif;
}

/* ── Container ─────────────────────────────────────────────── */
.gradio-container, .gradio-container * { box-sizing: border-box; }
.gradio-container {
    background-color: var(--bg-base) !important;
    font-family: var(--sans) !important;
    color: var(--txt-1) !important;
    min-height: 100vh;
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}

/* ── Sidebar ───────────────────────────────────────────────── */
.veritas-sidebar {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
    padding: 0 !important;
    min-height: 100vh;
}
.sidebar-section {
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid var(--border);
}
.sidebar-label {
    font-family: var(--mono);
    font-size: 0.625rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--txt-3);
    margin-bottom: 1rem;
}
.status-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.75rem;
    font-size: 0.8rem;
}
.status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--success);
    flex-shrink: 0;
    box-shadow: 0 0 6px var(--success);
}
.status-key {
    color: var(--txt-3);
    font-family: var(--mono);
    font-size: 0.7rem;
}
.status-val {
    color: var(--txt-1);
    font-family: var(--mono);
    font-size: 0.7rem;
    margin-left: auto;
    background: var(--bg-raised);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 8px;
}
.info-text {
    font-size: 0.76rem;
    color: var(--txt-2);
    line-height: 1.65;
}
.sidebar-logo {
    padding: 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.sidebar-logo-text {
    font-family: var(--mono);
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--txt-1);
    letter-spacing: 0.05em;
}
.sidebar-logo-sub {
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--txt-3);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── Main Header ───────────────────────────────────────────── */
.veritas-header {
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
}
.veritas-title {
    font-family: var(--mono) !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: var(--txt-1) !important;
    letter-spacing: 0.06em !important;
    margin: 0 !important;
}
.veritas-badge {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid var(--accent-dim);
    border-radius: 3px;
    padding: 3px 10px;
    background: color-mix(in srgb, var(--accent) 6%, transparent);
}
.breadcrumb {
    font-family: var(--mono);
    font-size: 0.68rem;
    color: var(--txt-3);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.breadcrumb span { color: var(--txt-3); }

/* ── Panel Cards ───────────────────────────────────────────── */
.panel-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
}
.panel-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.875rem 1.25rem;
    border-bottom: 1px solid var(--border);
    background: var(--bg-raised);
}
.panel-title {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--txt-2);
}
.panel-body { padding: 1.25rem; }

/* ── Input ─────────────────────────────────────────────────── */
.gradio-container textarea, 
.gradio-container .gr-textbox textarea {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: 5px !important;
    color: var(--txt-1) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    line-height: 1.7 !important;
    padding: 1rem !important;
    resize: vertical;
    transition: border-color 0.15s;
}
.gradio-container textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent) 12%, transparent) !important;
    outline: none !important;
}
.gradio-container label span, 
.gradio-container .gr-textbox label span {
    font-family: var(--mono) !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--txt-3) !important;
    margin-bottom: 0.5rem !important;
}

/* ── Button ────────────────────────────────────────────────── */
.analyze-btn, 
.gradio-container button.primary, 
.gradio-container button[variant="primary"] {
    background: var(--accent) !important;
    border: none !important;
    border-radius: 5px !important;
    color: #000 !important;
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.8rem 1.5rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.15s, transform 0.1s !important;
    margin-top: 0.75rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0.5rem !important;
}
.gradio-container button.primary:hover { opacity: 0.88 !important; }
.gradio-container button.primary:active { transform: scale(0.985) !important; }

/* ── Outputs ───────────────────────────────────────────────── */
.gradio-container .gr-label,
.gradio-container output {
    background: transparent !important;
    border: none !important;
}
.gradio-container .gr-label .label-output,
.gradio-container .gr-label span {
    font-family: var(--mono) !important;
    font-size: 0.85rem !important;
    color: var(--accent) !important;
}
.gradio-container .gr-number input {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: 5px !important;
    color: var(--accent) !important;
    font-family: var(--mono) !important;
    font-size: 1.4rem !important;
    font-weight: 600 !important;
    text-align: center !important;
}
.gradio-container .codemirror-wrapper,
.gradio-container .code-output, 
.gradio-container pre {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border) !important;
    border-radius: 5px !important;
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
}

/* ── Accordion ─────────────────────────────────────────────── */
.gradio-container .gr-accordion {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    margin-top: 0.75rem !important;
}
.gradio-container .gr-accordion > div:first-child {
    background: var(--bg-raised) !important;
    border-bottom: 1px solid var(--border) !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 0.875rem 1.25rem !important;
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--txt-2) !important;
}

/* ── Metrics Row ───────────────────────────────────────────── */
.metrics-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}
.metric-cell {
    background: var(--bg-raised);
    border: 1px solid var(--border);
    border-radius: 5px;
    padding: 1rem;
}
.metric-label {
    font-family: var(--mono);
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--txt-3);
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: var(--mono);
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--accent);
}

/* ── Footer ────────────────────────────────────────────────── */
.veritas-footer {
    border-top: 1px solid var(--border);
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.footer-text {
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--txt-3);
    letter-spacing: 0.06em;
}
.footer-divider { color: var(--border); margin: 0 0.4rem; }

/* ── Responsive ────────────────────────────────────────────── */
@media (max-width: 900px) {
    .veritas-header { padding: 1rem 1.25rem; }
    .metrics-grid { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
    .veritas-badge { display: none; }
    .panel-body { padding: 0.875rem; }
}

/* ── Tabs ──────────────────────────────────────────────────── */
.gradio-container .gr-tab-nav,
.gradio-container [role="tablist"] {
    background: var(--bg-surface) !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 0 1.5rem !important;
    gap: 0 !important;
}
.gradio-container .gr-tab-nav button,
.gradio-container [role="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    color: var(--txt-3) !important;
    font-family: var(--mono) !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.09em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 1.25rem !important;
    margin: 0 !important;
    transition: color 0.15s, border-color 0.15s !important;
}
.gradio-container .gr-tab-nav button.selected,
.gradio-container [role="tab"][aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}
.gradio-container .gr-tab-nav button:hover,
.gradio-container [role="tab"]:hover {
    color: var(--txt-1) !important;
}

/* ── Architecture Pipeline ─────────────────────────────────── */
.arch-wrap {
    padding: 2rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0;
}
.arch-step {
    display: grid;
    grid-template-columns: 48px 1fr;
    gap: 0 1.25rem;
    align-items: stretch;
}
.arch-spine {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.arch-node-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 1px solid var(--border-hi);
    background: var(--bg-raised);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 0.875rem;
}
.arch-node-circle span {
    font-family: var(--mono);
    font-size: 0.6rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.05em;
}
.arch-connector {
    width: 1px;
    flex: 1;
    background: var(--border);
    min-height: 1.5rem;
}
.arch-connector.dashed {
    background: repeating-linear-gradient(
        to bottom,
        var(--border) 0px,
        var(--border) 4px,
        transparent 4px,
        transparent 8px
    );
    width: 1px;
}
.arch-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 7px;
    margin: 0.5rem 0 0.5rem 0;
    overflow: hidden;
}
.arch-card-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.8rem 1.1rem;
    background: var(--bg-raised);
    border-bottom: 1px solid var(--border);
}
.arch-card-title {
    font-family: var(--mono);
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--txt-1);
    letter-spacing: 0.04em;
}
.arch-card-tag {
    font-family: var(--mono);
    font-size: 0.55rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-radius: 3px;
    padding: 2px 8px;
    margin-left: auto;
}
.tag-input   { color: #7dd3fc; background: rgba(125,211,252,0.08); border: 1px solid rgba(125,211,252,0.2); }
.tag-llm     { color: #a78bfa; background: rgba(167,139,250,0.08); border: 1px solid rgba(167,139,250,0.2); }
.tag-rag     { color: #34d399; background: rgba(52,211,153,0.08);  border: 1px solid rgba(52,211,153,0.2);  }
.tag-report  { color: #fbbf24; background: rgba(251,191,36,0.08);  border: 1px solid rgba(251,191,36,0.2);  }
.arch-card-body {
    padding: 1rem 1.1rem;
}
.arch-desc {
    font-family: var(--sans);
    font-size: 0.78rem;
    color: var(--txt-2);
    line-height: 1.7;
    margin-bottom: 0.75rem;
}
.arch-desc:last-child { margin-bottom: 0; }
.arch-substeps {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
.arch-substep {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    background: var(--bg-raised);
    border: 1px solid var(--border);
    border-radius: 5px;
    padding: 0.65rem 0.875rem;
}
.substep-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--txt-3);
    background: var(--bg-base);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 2px 7px;
    flex-shrink: 0;
    margin-top: 1px;
}
.substep-text {
    font-family: var(--sans);
    font-size: 0.75rem;
    color: var(--txt-2);
    line-height: 1.6;
}
.arch-outcomes {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    margin-top: 0.75rem;
}
.outcome-chip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    border-radius: 5px;
    padding: 0.55rem 0.75rem;
    border: 1px solid;
}
.outcome-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
}
.outcome-text {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.outcome-sub {
    font-family: var(--sans);
    font-size: 0.63rem;
    margin-top: 2px;
}
.chip-high {
    background: rgba(0,200,83,0.06);
    border-color: rgba(0,200,83,0.2);
}
.chip-high .outcome-dot  { background: #00c853; }
.chip-high .outcome-text { color: #00c853; }
.chip-high .outcome-sub  { color: rgba(0,200,83,0.6); }
.chip-low {
    background: rgba(255,61,90,0.06);
    border-color: rgba(255,61,90,0.2);
}
.chip-low .outcome-dot  { background: #ff3d5a; }
.chip-low .outcome-text { color: #ff3d5a; }
.chip-low .outcome-sub  { color: rgba(255,61,90,0.6); }
.chip-mid {
    background: rgba(255,171,0,0.06);
    border-color: rgba(255,171,0,0.2);
}
.chip-mid .outcome-dot  { background: #ffab00; }
.chip-mid .outcome-text { color: #ffab00; }
.chip-mid .outcome-sub  { color: rgba(255,171,0,0.6); }

/* ── Gradio Overrides ──────────────────────────────────────── */
.gradio-container .gr-box,
.gradio-container .gr-form,
.gradio-container .gr-block {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    gap: 0.75rem !important;
}
.gradio-container .gr-padded { padding: 0 !important; }
footer.svelte-1rjryqp { display: none !important; }
.gradio-container .wrap { gap: 0.75rem !important; }
"""


# ─────────────────────────────────────────────────────────────
#  HTML COMPONENTS
# ─────────────────────────────────────────────────────────────

def sidebar_logo_html():
    return f"""
    <div class="sidebar-logo">
        {ICON_SHIELD.replace('width="16"', 'width="22"').replace('height="16"', 'height="22"')}
        <div>
            <div class="sidebar-logo-text">Veritas AI</div>
            <div class="sidebar-logo-sub">Credibility Engine</div>
        </div>
    </div>
    """

def sidebar_status_html(model_name):
    return f"""
    <div class="sidebar-section">
        <div class="sidebar-label">System Status</div>
        <div class="status-row">
            <div class="status-dot"></div>
            <span class="status-key">Model</span>
            <span class="status-val">{model_name}</span>
        </div>
        <div class="status-row">
            <div class="status-dot"></div>
            <span class="status-key">Backend</span>
            <span class="status-val">LangGraph</span>
        </div>
        <div class="status-row">
            <div class="status-dot"></div>
            <span class="status-key">RAG Index</span>
            <span class="status-val">FAISS</span>
        </div>
        <div class="status-row">
            <div class="status-dot"></div>
            <span class="status-key">Vector Sim</span>
            <span class="status-val">Cosine</span>
        </div>
    </div>
    """

def sidebar_info_html():
    return f"""
    <div class="sidebar-section">
        <div class="sidebar-label">About</div>
        <p class="info-text">
            Veritas uses semantic analysis and retrieval-augmented 
            generation to verify news claims in real-time against 
            indexed reference corpora.
        </p>
    </div>
    <div class="sidebar-section">
        <div class="sidebar-label">Input Modes</div>
        <div class="status-row" style="margin-bottom:0.5rem;">
            {ICON_NETWORK}
            <span class="info-text" style="margin:0;">URL — live article scraping</span>
        </div>
        <div class="status-row">
            {ICON_SEARCH}
            <span class="info-text" style="margin:0;">Text — raw content analysis</span>
        </div>
    </div>
    """

def header_html():
    return f"""
    <div class="veritas-header">
        <div style="display:flex; align-items:center; gap:0.75rem;">
            <div class="breadcrumb">
                <span>Veritas</span>
                <span>›</span>
                <span style="color:var(--txt-2)">Analyzer</span>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:0.75rem;">
            {ICON_ACTIVITY.replace('width="16"', 'width="14"').replace('height="16"', 'height="14"')}
            <span style="font-family:var(--mono);font-size:0.68rem;color:var(--txt-3);">LIVE</span>
            <span style="width:6px;height:6px;border-radius:50%;background:var(--success);display:inline-block;box-shadow:0 0 6px var(--success);"></span>
            <span class="veritas-badge">v2.0 — Milestone 2</span>
        </div>
    </div>
    """

def input_panel_header():
    return f"""
    <div class="panel-header">
        {ICON_CODE}
        <span class="panel-title">Input — URL or Raw Text</span>
    </div>
    """

def results_panel_header():
    return f"""
    <div class="panel-header">
        {ICON_ACTIVITY}
        <span class="panel-title">Analysis Results</span>
    </div>
    """

def trace_panel_header():
    return f"""
    <div class="panel-header">
        {ICON_CPU}
        <span class="panel-title">Technical Trace — Agent State JSON</span>
    </div>
    """

def footer_html():
    return """
    <div class="veritas-footer">
        <span class="footer-text">Capstone Project <span class="footer-divider">|</span> Milestone 2</span>
        <span class="footer-text">Optimized for Reliability</span>
    </div>
    """

def architecture_html():
    return f"""
    <div class="arch-wrap">

        <!-- Step 1: Input -->
        <div class="arch-step">
            <div class="arch-spine">
                <div class="arch-node-circle"><span>01</span></div>
                <div class="arch-connector"></div>
            </div>
            <div class="arch-card">
                <div class="arch-card-header">
                    {ICON_LAYERS}
                    <span class="arch-card-title">Input Node</span>
                    <span class="arch-card-tag tag-input">Entry Point</span>
                </div>
                <div class="arch-card-body">
                    <p class="arch-desc">
                        Accepts a URL or raw article text. If a URL is provided,
                        <code style="font-family:var(--mono);font-size:0.72rem;color:var(--accent);background:var(--bg-raised);padding:1px 6px;border-radius:3px;">utils/url_loader.py</code>
                        scrapes the article content — bypassing paywalls and bot-checks where possible — and injects it into the agent state.
                    </p>
                    <div class="arch-substeps">
                        <div class="arch-substep">
                            <span class="substep-label">URL</span>
                            <span class="substep-text">Live article scraping via <code style="font-family:var(--mono);font-size:0.7rem;color:var(--txt-1);">url_loader.py</code> — paywall bypass attempted</span>
                        </div>
                        <div class="arch-substep">
                            <span class="substep-label">TEXT</span>
                            <span class="substep-text">Raw content passed directly into agent state — no scraping required</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Step 2: Analysis -->
        <div class="arch-step">
            <div class="arch-spine">
                <div class="arch-node-circle"><span>02</span></div>
                <div class="arch-connector"></div>
            </div>
            <div class="arch-card">
                <div class="arch-card-header">
                    {ICON_FILTER}
                    <span class="arch-card-title">Analysis Node</span>
                    <span class="arch-card-tag tag-llm">LLM</span>
                </div>
                <div class="arch-card-body">
                    <p class="arch-desc">
                        The LLM reads the full article text and performs structured extraction — identifying
                        all verifiable factual claims alongside risk signals that indicate potential misinformation.
                    </p>
                    <div class="arch-substeps">
                        <div class="arch-substep">
                            <span class="substep-label">CLAIMS</span>
                            <span class="substep-text">Verifiable factual assertions extracted for downstream fact-checking</span>
                        </div>
                        <div class="arch-substep">
                            <span class="substep-label">RISKS</span>
                            <span class="substep-text">Sensational language, anonymous sources, unverifiable statistics flagged as risk factors</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Step 3: Fact-Check -->
        <div class="arch-step">
            <div class="arch-spine">
                <div class="arch-node-circle"><span>03</span></div>
                <div class="arch-connector"></div>
            </div>
            <div class="arch-card">
                <div class="arch-card-header">
                    {ICON_DATABASE}
                    <span class="arch-card-title">Fact-Check Node</span>
                    <span class="arch-card-tag tag-rag">RAG + Web</span>
                </div>
                <div class="arch-card-body">
                    <p class="arch-desc">
                        A two-stage retrieval pipeline. Claims are first matched against a local FAISS index; 
                        if similarity scores fall below threshold, a live web search is triggered as fallback.
                        The best available evidence is then passed to the LLM for verdict assignment.
                    </p>
                    <div class="arch-substeps">
                        <div class="arch-substep">
                            <span class="substep-label">A · RAG</span>
                            <span class="substep-text">Claims embedded and queried against FAISS index using cosine similarity — local knowledge base searched first</span>
                        </div>
                        <div class="arch-substep">
                            <span class="substep-label">B · WEB</span>
                            <span class="substep-text">If local similarity score is too low, agent executes a live web search to source external evidence</span>
                        </div>
                        <div class="arch-substep">
                            <span class="substep-label">VERIFY</span>
                            <span class="substep-text">LLM evaluates best evidence against each claim — returns <strong style="color:var(--txt-1);font-weight:600;">Supports</strong>, <strong style="color:var(--txt-1);font-weight:600;">Contradicts</strong>, or <strong style="color:var(--txt-1);font-weight:600;">Unverified</strong></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Step 4: Report -->
        <div class="arch-step">
            <div class="arch-spine">
                <div class="arch-node-circle"><span>04</span></div>
                <div style="flex:1;"></div>
            </div>
            <div class="arch-card">
                <div class="arch-card-header">
                    {ICON_FLAG}
                    <span class="arch-card-title">Report Node</span>
                    <span class="arch-card-tag tag-report">Output</span>
                </div>
                <div class="arch-card-body">
                    <p class="arch-desc">
                        Dynamically calculates the final credibility rating from the evidence outcomes.
                        When claims are unverified, the system falls back to the risk factors extracted in
                        step 2 — ensuring robust evaluation even for novel or uncovered articles.
                    </p>
                    <div class="arch-outcomes">
                        <div class="outcome-chip chip-high">
                            <div class="outcome-dot"></div>
                            <div>
                                <div class="outcome-text">High</div>
                                <div class="outcome-sub">Evidence supports claims</div>
                            </div>
                        </div>
                        <div class="outcome-chip chip-low">
                            <div class="outcome-dot"></div>
                            <div>
                                <div class="outcome-text">Low</div>
                                <div class="outcome-sub">Evidence contradicts</div>
                            </div>
                        </div>
                        <div class="outcome-chip chip-mid">
                            <div class="outcome-dot"></div>
                            <div>
                                <div class="outcome-text">Scored</div>
                                <div class="outcome-sub">Risk-factor analysis</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
    """


# ─────────────────────────────────────────────────────────────
#  UI BUILDER
# ─────────────────────────────────────────────────────────────

def create_ui():
    from config.settings import get_llm_config
    llm_conf   = get_llm_config()
    model_name = llm_conf.get("model", "Llama-3")

    with gr.Blocks(title="Veritas AI", css=CSS) as demo:

        # ── Sidebar ────────────────────────────────────────
        with gr.Sidebar(elem_classes="veritas-sidebar"):
            gr.HTML(sidebar_logo_html())
            gr.HTML(sidebar_status_html(model_name))
            gr.HTML(sidebar_info_html())

        # ── Header ─────────────────────────────────────────
        gr.HTML(header_html())

        # ── Tabs ───────────────────────────────────────────
        with gr.Tabs():

            # ── Tab 1: Analyzer ────────────────────────────
            with gr.TabItem("Analyzer"):
                with gr.Row(equal_height=False):

                    # LEFT — Input Panel
                    with gr.Column(scale=3):
                        gr.HTML(input_panel_header())
                        article_input = gr.Textbox(
                            label="Paste article content or enter a URL",
                            placeholder="https://example.com/article  —or—  paste full article text here...",
                            lines=16,
                            max_lines=32,
                            show_label=True,
                        )
                        analyze_btn = gr.Button(
                            "Run Credibility Analysis",
                            variant="primary",
                            elem_classes="analyze-btn",
                        )

                    # RIGHT — Results Panel
                    with gr.Column(scale=2):
                        gr.HTML(results_panel_header())
                        with gr.Row():
                            cred_output = gr.Label(
                                label="Credibility Verdict",
                                num_top_classes=1,
                            )
                            conf_output = gr.Number(
                                label="Confidence Score (%)",
                                precision=1,
                            )

                        with gr.Accordion(label="Technical Trace", open=False):
                            gr.HTML(trace_panel_header())
                            full_report = gr.Code(
                                label="",
                                language="json",
                                lines=18,
                            )

                # ── Event ──────────────────────────────────
                analyze_btn.click(
                    fn=analyze,
                    inputs=[article_input],
                    outputs=[cred_output, conf_output, full_report],
                )

            # ── Tab 2: Architecture ────────────────────────
            with gr.TabItem("Architecture & Workflow"):
                gr.HTML(architecture_html())

        # ── Footer ─────────────────────────────────────────
        gr.HTML(footer_html())

    return demo


# ─────────────────────────────────────────────────────────────
#  LAUNCH
# ─────────────────────────────────────────────────────────────

def launch():
    print("\n  Veritas AI — Precision UI starting on :7860\n")
    demo = create_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    launch()