"""
FDSS | Financial Decision Support System
A Modern Quantitative Financial Analytics & Stochastic Simulation System.
Author: Atharv Ranade
Version: 1.3.0 (Comprehensive Documentation & System Manual Integration)
"""

import streamlit as st
from ui.styles import apply_theme
from ui.tab_time_value import render_tab_time_value
from ui.tab_loans import render_tab_loans
from ui.tab_investments import render_tab_investments
from ui.tab_capital_budgeting import render_tab_capital_budgeting
from ui.tab_monte_carlo import render_tab_monte_carlo
from ui.tab_user_guide import render_tab_user_guide

# Page Configuration
st.set_page_config(
    page_title="FDSS | Financial Decision Support System",
    page_icon="📊",
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
    st.markdown("### Settings")
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
    st.markdown("##### About the System")
    st.markdown(
        """<div style="font-size: 0.78rem; color: #94A3B8; line-height: 1.55;">
<b>FDSS</b> is an open-source quantitative decision engine authored by 
<b>Atharv Ranade</b>.<br><br>
Designed to replace opaque commercial calculators with transparent first-principles mathematical derivations—spanning 
real analysis, numerical root-finding (Newton-Raphson &amp; Brent's method), and Itô stochastic calculus.<br><br>
<a href="https://github.com/AlmightyXZen/Financial-Decision-Support-System" target="_blank" style="color: #38BDF8; text-decoration: none; font-weight: 500;">
Source Code &amp; Documentation (GitHub) &rarr;
</a>
</div>""",
        unsafe_allow_html=True,
    )

# Modern Top App Header
st.markdown(
    """<div class="app-header">
<div class="brand-wrapper">
<div class="brand-pill">FDSS</div>
<div>
<div class="brand-title">Financial Decision Support System</div>
<div class="brand-subtitle">Quantitative Analytics &amp; Stochastic Simulation System</div>
</div>
</div>
</div>""",
    unsafe_allow_html=True,
)

# Main Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Time Value & Yields",
    "Debt & Amortization",
    "Wealth & SIP Planner",
    "Capital Budgeting & IRR",
    "Monte Carlo Risk Lab",
    "Documentation & Guide",
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

with tab6:
    render_tab_user_guide(curr_sym)

# Minimalist App Footer
st.markdown(
    """<div class="app-footer">
Financial Decision Support System (FDSS) • © 2026 Atharv Ranade. All rights reserved.
</div>""",
    unsafe_allow_html=True,
)
