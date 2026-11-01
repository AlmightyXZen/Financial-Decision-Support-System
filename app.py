"""
FDSS | Financial Decision Support System
A Modern Quantitative Financial Analytics & Stochastic Simulation Web Studio.
Author: Atharv Ranade
Version: 1.2.0 (High-Density Spacing & Collision-Free Canvas Layout)
"""

import streamlit as st
from ui.styles import apply_theme
from ui.tab_time_value import render_tab_time_value
from ui.tab_loans import render_tab_loans
from ui.tab_investments import render_tab_investments
from ui.tab_capital_budgeting import render_tab_capital_budgeting
from ui.tab_monte_carlo import render_tab_monte_carlo

# Page Configuration
st.set_page_config(
    page_title="FDSS | Quantitative Finance Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply global styling
apply_theme()

# Supported Major Global Currencies
CURRENCY_CONFIG = {
    "₹ INR — Indian Rupee": "₹",
    "$ USD — US Dollar": "$",
    "€ EUR — Eurozone Euro": "€",
    "£ GBP — British Pound": "£",
    "¥ JPY — Japanese Yen": "¥",
    "CHF — Swiss Franc": "CHF ",
    "C$ CAD — Canadian Dollar": "C$",
    "A$ AUD — Australian Dollar": "A$",
    "S$ SGD — Singapore Dollar": "S$",
    "HK$ HKD — Hong Kong Dollar": "HK$",
    "¥ CNY — Chinese Yuan": "CN¥ ",
    "AED — UAE Dirham": "AED ",
    "₩ KRW — South Korean Won": "₩",
    "R$ BRL — Brazilian Real": "R$",
    "kr SEK — Swedish Krona": "kr ",
}

# Sidebar Controls
with st.sidebar:
    st.markdown("### ⚙️ Workspace Settings")
    currency_option = st.selectbox(
        "Currency Display",
        options=list(CURRENCY_CONFIG.keys()),
        index=0,
        key="global_currency_select",
        help="Select presentation currency across all analytical modules."
    )
    curr_sym = CURRENCY_CONFIG[currency_option]

    st.markdown("---")
    st.markdown("##### Denomination Scale")
    scale_option = st.radio(
        "Number System",
        options=["Auto (By Currency)", "International (M / B)", "Indian (L / Cr)"],
        index=0,
        key="global_scale_select",
        help="Switch between International (Thousands, Millions, Billions) and Indian Vedic (Lakhs, Crores) systems."
    )

    st.markdown("---")
    st.markdown("##### About the Studio")
    st.caption(
        "FDSS is a quantitative finance platform combining first-principles calculus, "
        "numerical root-finding (Newton–Raphson), and Itô stochastic simulation. "
        "Zero third-party financial black boxes."
    )
    st.caption("Engineered for transparent retail and institutional financial decision-making.")

# Modern Top App Header
st.markdown(
    """
    <div class="app-header">
        <div class="brand-wrapper">
            <div class="brand-pill">⚡ FDSS</div>
            <div>
                <div class="brand-title">Financial Decision Support System</div>
                <div class="brand-subtitle">Quantitative Analytics & Stochastic Simulation Studio</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Main Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Time Value & Yields",
    "Debt & Amortization",
    "Wealth & SIP Planner",
    "Capital Budgeting & IRR",
    "Monte Carlo Risk Lab",
])

with tab1:
    render_tab_time_value(curr_sym)

with tab2:
    render_tab_loans(curr_sym)

with tab3:
    render_tab_investments(curr_sym)

with tab4:
    render_tab_capital_budgeting(curr_sym)

with tab5:
    render_tab_monte_carlo(curr_sym)

# Minimalist App Footer
st.markdown(
    """
    <div class="app-footer">
        FDSS Quantitative Finance Studio • © 2026 Atharv Ranade. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
