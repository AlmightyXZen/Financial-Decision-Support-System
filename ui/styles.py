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
    --card-bg: rgba(14, 27, 49, 0.72);
    --card-hover: rgba(18, 35, 64, 0.85);
    --border-subtle: rgba(56, 189, 248, 0.16);
    --border-hover: rgba(56, 189, 248, 0.40);
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
}

/* App Header / Top Navigation */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0 1.2rem 0;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1.25rem;
}

.brand-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-pill {
    background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
    color: #070F1E;
    font-weight: 900;
    font-size: 1.15rem;
    padding: 5px 12px;
    border-radius: 8px;
    letter-spacing: -0.03em;
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.25);
}

.brand-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.brand-subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
}

/* Refined Stat Cards */
.fdss-card {
    background: var(--card-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    backdrop-filter: blur(10px);
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.35);
    height: 100%;
}

.fdss-card:hover {
    border-color: var(--border-hover);
    background: var(--card-hover);
    transform: translateY(-2px);
}

.card-label {
    font-size: 0.76rem;
    text-transform: uppercase;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.05em;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.3rem;
}

.card-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #FFFFFF;
    font-family: 'JetBrains Mono', 'Segoe UI Mono', monospace;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.card-subtext {
    font-size: 0.77rem;
    color: var(--text-muted);
    margin-top: 0.35rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Micro Badges & Deltas */
.delta-badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.02em;
}
.delta-green { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }
.delta-red { background: rgba(244, 63, 94, 0.15); color: #F43F5E; border: 1px solid rgba(244, 63, 94, 0.3); }
.delta-blue { background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); }
.delta-amber { background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); }

/* Quick Preset Chips */
.preset-button {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #E2E8F0;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.78rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
}
.preset-button:hover {
    background: rgba(56, 189, 248, 0.15);
    border-color: #38BDF8;
    color: #38BDF8;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px 6px 0 0;
    color: var(--text-muted);
    font-weight: 600;
    padding: 8px 16px;
    font-size: 0.88rem;
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
    font-size: 0.8rem;
    padding: 2.5rem 0 1rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    margin-top: 3.5rem;
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
    height: int = 360
) -> Dict[str, Any]:
    """Returns a unified dark terminal Plotly layout dictionary."""
    return dict(
        title=dict(text=title, font=dict(color="#F8FAFC", size=14)),
        xaxis=dict(
            title=xaxis_title,
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
        ),
        yaxis=dict(
            title=yaxis_title,
            gridcolor="rgba(255, 255, 255, 0.06)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(14, 27, 49, 0.35)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        ),
        hovermode="x unified",
        margin=dict(l=10, r=10, t=35, b=10),
        height=height,
    )
