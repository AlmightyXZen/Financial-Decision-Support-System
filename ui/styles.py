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
    margin-top: 0.5rem !important;
}

/* Preset Buttons Container */
div[data-testid="stHorizontalBlock"]:has(button) {
    margin-top: 0.4rem;
    margin-bottom: 1.6rem;
    gap: 12px;
}

/* Form Input Element Spacing */
div[data-testid="stSlider"] {
    margin-bottom: 1.4rem;
}
div[data-testid="stNumberInput"] {
    margin-bottom: 1.4rem;
}
div[data-testid="stSelectbox"] {
    margin-bottom: 1.4rem;
}
div[data-testid="stTextInput"] {
    margin-bottom: 1.4rem;
}

/* Refined Stat Cards with Generous Breathing Room */
.fdss-card {
    background: var(--card-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 1.2rem 1.35rem;
    backdrop-filter: blur(12px);
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 6px 24px -2px rgba(0, 0, 0, 0.40);
    margin-bottom: 1.8rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 118px;
}

.fdss-card:hover {
    border-color: var(--border-hover);
    background: var(--card-hover);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px -4px rgba(56, 189, 248, 0.15);
}

.card-label {
    font-size: 0.76rem;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 0.45rem;
    line-height: 1.3;
}

.card-value {
    font-size: 1.68rem;
    font-weight: 700;
    color: #FFFFFF;
    font-family: 'JetBrains Mono', 'Segoe UI Mono', monospace;
    letter-spacing: -0.02em;
    line-height: 1.25;
    margin: 0.35rem 0;
}

.card-subtext {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
    line-height: 1.4;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Micro Badges & Deltas */
.delta-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 5px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    white-space: nowrap;
}
.delta-green { background: rgba(16, 185, 129, 0.16); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.35); }
.delta-red { background: rgba(244, 63, 94, 0.16); color: #F43F5E; border: 1px solid rgba(244, 63, 94, 0.35); }
.delta-blue { background: rgba(56, 189, 248, 0.16); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.35); }
.delta-amber { background: rgba(245, 158, 11, 0.16); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.35); }

/* Chart Container Spacing */
div[data-testid="stPlotlyChart"] {
    margin-top: 1.2rem;
    margin-bottom: 2.2rem;
    background: rgba(14, 27, 49, 0.3);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 8px;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 6px;
    margin-bottom: 1.5rem;
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
        <div class="card-label">
            <span>{label}</span>
            {delta_html}
        </div>
        <div class="card-value"{color_style}>{value}</div>
        {subtext_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def plotly_base_layout(
    title: str,
    xaxis_title: str,
    yaxis_title: str,
    height: int = 400
) -> Dict[str, Any]:
    """
    Returns a unified dark terminal Plotly layout dictionary.
    Guarantees that the legend is placed safely below the chart (y=-0.22)
    and the title is at the top left (y=0.98), completely eliminating overlap!
    """
    return dict(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(color="#F8FAFC", size=13),
            x=0.01,
            y=0.97,
            xanchor="left",
            yanchor="top"
        ),
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
        plot_bgcolor="rgba(14, 27, 49, 0.30)",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#CBD5E1"),
            bgcolor="rgba(14, 27, 49, 0.65)",
            bordercolor="rgba(255, 255, 255, 0.08)",
            borderwidth=1
        ),
        hovermode="x unified",
        margin=dict(l=25, r=20, t=55, b=65),
        height=height,
    )
