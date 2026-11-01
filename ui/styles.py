"""
ui/styles.py
Central Styling, Custom CSS & Reusable Component Helpers for FDSS Studio.
Author: Atharv Ranade
"""

from typing import Optional, Dict, Any
import streamlit as st

CUSTOM_THEME_CSS = """
<style>
:root {
    --bg-dark: #070F1E;
    --card-bg: rgba(14, 27, 49, 0.75);
    --card-hover: rgba(18, 35, 64, 0.90);
    --border-subtle: rgba(56, 189, 248, 0.16);
    --border-hover: rgba(56, 189, 248, 0.42);
    --accent-blue: #38BDF8;
    --accent-green: #10B981;
    --accent-red: #F43F5E;
    --accent-amber: #F59E0B;
    --accent-purple: #818CF8;
    --text-primary: #F8FAFC;
    --text-muted: #94A3B8;
}

/* Global Background */
.stApp {
    background: radial-gradient(circle at 10% 8%, #0C1A30 0%, #070F1E 100%);
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Plus Jakarta Sans", sans-serif;
    letter-spacing: 0.01em;
}

/* Layout Container Spacing */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 4rem;
    max-width: 95% !important;
}

/* App Header / Top Navigation */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0 1.5rem 0;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1.8rem;
}

.brand-wrapper {
    display: flex;
    align-items: center;
    gap: 14px;
}

.brand-pill {
    background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
    color: #070F1E;
    font-weight: 900;
    font-size: 1.2rem;
    padding: 6px 14px;
    border-radius: 8px;
    letter-spacing: -0.03em;
    box-shadow: 0 4px 14px rgba(56, 189, 248, 0.28);
}

.brand-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    line-height: 1.25;
}

.brand-subtitle {
    font-size: 0.84rem;
    color: var(--text-muted);
    margin-top: 2px;
}

/* Section Headings */
h4, h5, .section-heading {
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
    color: #F1F5F9 !important;
    margin-bottom: 1.2rem !important;
    margin-top: 0.6rem !important;
}

/* Preset Buttons Container */
div[data-testid="stHorizontalBlock"]:has(button) {
    margin-top: 0.4rem;
    margin-bottom: 1.6rem;
    gap: 10px;
}

div[data-testid="stHorizontalBlock"] button {
    font-size: 0.82rem !important;
    padding: 8px 10px !important;
    white-space: normal !important;
    min-height: 42px !important;
    line-height: 1.25 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    border: 1px solid var(--border-subtle) !important;
    background: rgba(14, 27, 49, 0.6) !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stHorizontalBlock"] button:hover {
    border-color: var(--accent-blue) !important;
    background: rgba(56, 189, 248, 0.12) !important;
    color: #FFFFFF !important;
}

/* Form Input Element Spacing */
div[data-testid="stSlider"] {
    margin-bottom: 1.5rem;
}
div[data-testid="stNumberInput"] {
    margin-bottom: 1.5rem;
}
div[data-testid="stSelectbox"] {
    margin-bottom: 1.5rem;
}
div[data-testid="stTextInput"] {
    margin-bottom: 1.5rem;
}

/* Refined Stat Cards */
.fdss-card {
    background: var(--card-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1rem 1.15rem;
    backdrop-filter: blur(12px);
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 4px 18px -2px rgba(0, 0, 0, 0.40);
    margin-bottom: 1.2rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 108px;
    box-sizing: border-box;
}

.fdss-card:hover {
    border-color: var(--border-hover);
    background: var(--card-hover);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px -4px rgba(56, 189, 248, 0.15);
}

.card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    margin-bottom: 0.25rem;
}

.card-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.05em;
    line-height: 1.2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.card-value {
    font-size: clamp(1.3rem, 1.8vw, 1.6rem);
    font-weight: 700;
    color: #FFFFFF;
    font-family: 'JetBrains Mono', 'Segoe UI Mono', monospace;
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin: 0.25rem 0;
    white-space: nowrap !important;
    text-transform: none !important;
}

.card-subtext {
    font-size: 0.76rem;
    color: var(--text-muted);
    line-height: 1.3;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-transform: none !important;
}

/* Micro Badges & Deltas */
.delta-badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 5px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    white-space: nowrap;
    text-transform: none !important;
}
.delta-green { background: rgba(16, 185, 129, 0.16); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.35); }
.delta-red { background: rgba(244, 63, 94, 0.16); color: #F43F5E; border: 1px solid rgba(244, 63, 94, 0.35); }
.delta-blue { background: rgba(56, 189, 248, 0.16); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.35); }
.delta-amber { background: rgba(245, 158, 11, 0.16); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.35); }

/* Clean Chart Heading Outside Plotly */
.chart-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.01em;
    margin-bottom: 0.2rem;
}
.chart-subtitle {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin-bottom: 0.6rem;
    line-height: 1.4;
}

/* Mathematical Exponents & Subscripts Typography */
sup {
    font-size: 0.72em;
    line-height: 0;
    position: relative;
    vertical-align: baseline;
    top: -0.42em;
    font-family: inherit;
}

sub {
    font-size: 0.72em;
    line-height: 0;
    position: relative;
    vertical-align: baseline;
    bottom: -0.22em;
    font-family: inherit;
}

/* Mathematical Vertical Fractions (Numerator over Denominator) */
.math-frac {
    display: inline-flex;
    flex-direction: column;
    vertical-align: middle;
    text-align: center;
    padding: 0 4px;
    font-family: 'JetBrains Mono', 'Segoe UI Mono', monospace;
    font-size: 0.82em;
    line-height: 1.05;
    margin: 0 3px;
}

.math-num {
    border-bottom: 1.5px solid rgba(248, 250, 252, 0.55);
    padding-bottom: 1.5px;
    font-size: 0.95em;
    color: #F8FAFC;
    font-weight: 600;
}

.math-denom {
    padding-top: 1.5px;
    font-size: 0.95em;
    color: #94A3B8;
    font-weight: 600;
}

/* Mathematical Callout Box */
.math-callout {
    background: rgba(14, 27, 49, 0.75);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin-top: 0.8rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
}

.callout-header {
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent-blue);
    margin-bottom: 0.6rem;
}

.callout-body {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
}

.callout-col {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
}

.callout-val {
    font-size: 1.15rem;
    font-weight: 700;
    color: #FFFFFF;
    font-family: 'JetBrains Mono', monospace;
}

.callout-eq {
    font-size: 0.75rem;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 4px;
}

.callout-sep {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-muted);
    padding: 0 6px;
    text-transform: uppercase;
}

/* Chart Container Spacing */
div[data-testid="stPlotlyChart"] {
    margin-top: 0.5rem;
    margin-bottom: 2.2rem;
    background: rgba(14, 27, 49, 0.3);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 10px;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 6px;
    margin-bottom: 1.6rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px 6px 0 0;
    color: var(--text-muted);
    font-weight: 600;
    padding: 10px 18px;
    font-size: 0.92rem;
}
.stTabs [aria-selected="true"] {
    background: rgba(56, 189, 248, 0.12) !important;
    color: var(--accent-blue) !important;
    border-bottom: 2px solid var(--accent-blue) !important;
}

/* Minimalist Clean Footer */
.app-footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.82rem;
    padding: 3rem 0 1.5rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
    margin-top: 4rem;
}
</style>
"""


def apply_theme():
    """Injects the global theme styling."""
    st.markdown(CUSTOM_THEME_CSS, unsafe_allow_html=True)


def format_currency(value: float, sym: str = "₹") -> str:
    """Formats numeric values into sleek currency strings (e.g. ₹15.42 L, $1.25 Cr, $45,000.00)."""
    if abs(value) >= 1e7:
        return f"{sym}{value / 1e7:.2f} Cr"
    elif abs(value) >= 1e5:
        return f"{sym}{value / 1e5:.2f} L"
    return f"{sym}{value:,.2f}"


def format_percentage(value: float) -> str:
    """Formats decimals into percentage strings."""
    return f"{value * 100:.2f}%"


def render_stat_card(
    label: str,
    value: str,
    subtext: Optional[str] = None,
    delta: Optional[str] = None,
    delta_type: str = "green",
    value_color: Optional[str] = None
):
    """Renders a sleek, responsive stat KPI card."""
    delta_html = ""
    if delta:
        delta_html = f'<span class="delta-badge delta-{delta_type}">{delta}</span>'

    color_style = f' style="color: {value_color};"' if value_color else ""
    subtext_html = f'<div class="card-subtext">{subtext}</div>' if subtext else ""

    html = f"""
    <div class="fdss-card">
        <div class="card-top">
            <span class="card-label">{label}</span>
            {delta_html}
        </div>
        <div class="card-value"{color_style}>{value}</div>
        {subtext_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_chart_header(title: str, subtitle: Optional[str] = None):
    """Renders a clean HTML header above the chart, completely eliminating canvas collisions."""
    sub_html = f'<div class="chart-subtitle">{subtitle}</div>' if subtitle else ""
    html = f"""
    <div style="margin-top: 1.2rem; margin-bottom: 0.4rem;">
        <div class="chart-title">{title}</div>
        {sub_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def plotly_base_layout(
    xaxis_title: str = "",
    yaxis_title: str = "",
    height: int = 380,
    show_legend: bool = True
) -> Dict[str, Any]:
    """
    Returns a unified dark terminal Plotly layout dictionary.
    Places horizontal legends at the top of the canvas, below the decoupled HTML header.
    """
    layout = dict(
        xaxis=dict(
            title=dict(text=xaxis_title, font=dict(color="#94A3B8", size=12)),
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#94A3B8", size=11)
        ),
        yaxis=dict(
            title=dict(text=yaxis_title, font=dict(color="#94A3B8", size=12)),
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#94A3B8", size=11)
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(14, 27, 49, 0.25)",
        hovermode="x unified",
        margin=dict(l=48, r=20, t=35, b=45),
        height=height,
    )
    if show_legend:
        layout["legend"] = dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#CBD5E1"),
            bgcolor="rgba(14, 27, 49, 0.70)",
            bordercolor="rgba(255, 255, 255, 0.08)",
            borderwidth=1
        )
    else:
        layout["showlegend"] = False
        layout["margin"] = dict(l=48, r=20, t=15, b=40)

    return layout


def format_fraction(numerator: str, denominator: str) -> str:
    """Returns an HTML string rendering a proper vertical mathematical fraction (numerator directly over denominator)."""
    return f'<span class="math-frac"><span class="math-num">{numerator}</span><span class="math-denom">{denominator}</span></span>'


def render_doubling_callout(exact_yrs: float, rule_72_yrs: float):
    """
    Renders an institutional mathematical callout box for Capital Doubling Horizon,
    featuring proper vertical fractions for both the exact Euler ODE solution and Rule of 72.
    """
    exact_frac = format_fraction("ln(2)", "<i>r</i>")
    rule_frac = format_fraction("72", "<i>r</i><sub>%</sub>")

    html = f"""
    <div class="math-callout">
        <div class="callout-header">⏱️ Capital Doubling Horizon</div>
        <div class="callout-body">
            <div class="callout-col">
                <span class="callout-val">{exact_yrs:.2f} yrs</span>
                <span class="callout-eq">Exact: {exact_frac}</span>
            </div>
            <div class="callout-sep">vs</div>
            <div class="callout-col">
                <span class="callout-val">{rule_72_yrs:.2f} yrs</span>
                <span class="callout-eq">Rule of 72: {rule_frac}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
