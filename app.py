"""
FDSS | Financial Decision Support System
A modern quantitative financial mathematics and stochastic simulation web application.
Author: Atharv Ranade
"""

import math
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# First-principles computational models
from models.time_value import (
    simple_interest,
    simple_interest_amount,
    compound_interest_amount,
    accrued_compound_interest,
    continuous_compounding_amount,
    nominal_to_effective_rate,
)
from models.loans_and_credit import (
    calculate_emi,
    check_negative_amortization,
    generate_amortization_schedule,
    calculate_prepayment_savings,
)
from models.investment_plans import (
    calculate_sip_wealth,
    calculate_step_up_sip,
    real_rate_of_return,
    purchasing_power_erosion,
    purchasing_power_half_life,
)
from models.capital_budgeting import (
    net_present_value,
    internal_rate_of_return,
    internal_rate_of_return_with_history,
    discounted_payback_period,
)
from models.monte_carlo import (
    calculate_volatility_drag,
    simulate_gbm_paths,
    goal_attainment_probability,
    calculate_value_at_risk,
    compute_simulation_statistics,
)

# ==============================================================================
# APP CONFIGURATION & STYLING
# ==============================================================================

st.set_page_config(
    page_title="FDSS | Quantitative Finance Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_CSS = """
<style>
:root {
    --bg-dark: #070F1E;
    --card-bg: rgba(14, 27, 49, 0.75);
    --border-subtle: rgba(56, 189, 248, 0.18);
    --accent-blue: #38BDF8;
    --accent-green: #10B981;
    --accent-red: #F43F5E;
    --accent-amber: #F59E0B;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
}

/* App Background */
.stApp {
    background: radial-gradient(circle at 10% 10%, #0B192C 0%, #070F1E 100%);
    color: var(--text-main);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Navbar / App Header */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0 1.25rem 0;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1.5rem;
}
.brand-container {
    display: flex;
    align-items: center;
    gap: 10px;
}
.brand-logo {
    background: linear-gradient(135deg, #38BDF8, #818CF8);
    color: #070F1E;
    font-weight: 900;
    font-size: 1.2rem;
    padding: 6px 12px;
    border-radius: 8px;
    letter-spacing: -0.03em;
}
.brand-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.02em;
}
.brand-tagline {
    font-size: 0.82rem;
    color: var(--text-muted);
}

/* Modern Metric Cards */
.fdss-stat-card {
    background: var(--card-bg);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    backdrop-filter: blur(8px);
    transition: border-color 0.2s ease, transform 0.2s ease;
}
.fdss-stat-card:hover {
    border-color: rgba(56, 189, 248, 0.45);
}
.stat-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}
.stat-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #FFFFFF;
    font-family: 'JetBrains Mono', 'Segoe UI Mono', monospace;
    letter-spacing: -0.02em;
}
.stat-subtext {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
}

/* Tab Headers */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 6px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px;
    color: var(--text-muted);
    font-weight: 600;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(56, 189, 248, 0.12) !important;
    color: var(--accent-blue) !important;
    border-bottom: 2px solid var(--accent-blue) !important;
}

/* Minimalist Footer */
.app-footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.8rem;
    padding: 2.5rem 0 1rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    margin-top: 3rem;
}
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)


# ==============================================================================
# CACHED COMPUTATION HELPERS FOR HIGH PERFORMANCE
# ==============================================================================

@st.cache_data(show_spinner=False)
def cached_amortization_schedule(
    principal: float,
    annual_rate: float,
    tenure_months: int,
    monthly_prepayment: float
) -> pd.DataFrame:
    return generate_amortization_schedule(
        principal=principal,
        annual_rate=annual_rate,
        tenure_months=tenure_months,
        monthly_prepayment=monthly_prepayment
    )

@st.cache_data(show_spinner=False)
def cached_monte_carlo(
    s0: float,
    mu: float,
    sigma: float,
    t_years: float,
    n_steps: int,
    n_paths: int,
    seed: int
):
    return simulate_gbm_paths(
        s0=s0,
        mu=mu,
        sigma=sigma,
        t_years=t_years,
        n_steps=n_steps,
        n_paths=n_paths,
        seed=seed
    )


# Helper for currency display
def format_curr(value: float, sym: str = "₹") -> str:
    if abs(value) >= 1e7:
        return f"{sym}{value / 1e7:.2f} Cr"
    elif abs(value) >= 1e5:
        return f"{sym}{value / 1e5:.2f} L"
    return f"{sym}{value:,.2f}"

def format_pct(value: float) -> str:
    return f"{value * 100:.2f}%"


# ==============================================================================
# APP HEADER & SIDEBAR
# ==============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Workspace Settings")
    currency_option = st.selectbox(
        "Currency Symbol",
        options=["₹ INR", "$ USD", "€ EUR", "£ GBP"],
        index=0
    )
    curr_sym = currency_option.split()[0]
    st.markdown("---")
    st.caption("FDSS Quantitative Financial Analytics Studio. Zero black boxes; deterministic and stochastic models computed from first principles.")

# Minimalist Top Navbar
st.markdown(
    """
    <div class="app-header">
        <div class="brand-container">
            <div class="brand-logo">⚡ FDSS</div>
            <div>
                <div class="brand-name">Financial Decision Support System</div>
                <div class="brand-tagline">Quantitative Analytics & Numerical Simulation Studio</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Time Value & Yields",
    "Debt & Amortization",
    "Wealth & SIP Planner",
    "Capital Budgeting & IRR",
    "Monte Carlo Risk Lab",
])


# ==============================================================================
# TAB 1: TIME VALUE & YIELDS
# ==============================================================================
with tab1:
    col1, col2 = st.columns([1, 2.2], gap="large")
    
    with col1:
        st.markdown("#### Capital Inputs")
        p_val = st.number_input("Principal ($P$)", min_value=1000.0, max_value=50000000.0, value=100000.0, step=10000.0, key="tvm_p")
        r_val_pct = st.slider("Nominal Rate ($r$ %)", min_value=0.5, max_value=30.0, value=10.0, step=0.1, key="tvm_r")
        r_val = r_val_pct / 100.0
        t_val = st.slider("Horizon ($t$ Years)", min_value=0.5, max_value=40.0, value=10.0, step=0.5, key="tvm_t")
        
        freq_dict = {"Annual (m=1)": 1, "Semi-Annual (m=2)": 2, "Quarterly (m=4)": 4, "Monthly (m=12)": 12, "Daily (m=365)": 365}
        freq_choice = st.selectbox("Frequency ($m$)", options=list(freq_dict.keys()), index=3, key="tvm_m")
        m_val = freq_dict[freq_choice]

        st.latex(r"A(t) = P \left(1 + \frac{r}{m}\right)^{mt} \xrightarrow{m \to \infty} P e^{rt}")

    # Calculations
    a_simple = simple_interest_amount(p_val, r_val, t_val)
    a_compound = compound_interest_amount(p_val, r_val, t_val, compounding_frequency=m_val)
    a_cont = continuous_compounding_amount(p_val, r_val, t_val)
    ear = nominal_to_effective_rate(r_val, compounding_frequency=m_val)

    with col2:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Simple Interest</div>
                    <div class="stat-value">{format_curr(a_simple, curr_sym)}</div>
                    <div class="stat-subtext">Linear: P(1 + rt)</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with m2:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Discrete Compound</div>
                    <div class="stat-value">{format_curr(a_compound, curr_sym)}</div>
                    <div class="stat-subtext">Frequency: {freq_choice.split()[0]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with m3:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Continuous (Euler)</div>
                    <div class="stat-value">{format_curr(a_cont, curr_sym)}</div>
                    <div class="stat-subtext">Ceiling: P · e^(rt)</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with m4:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Effective Rate (EAR)</div>
                    <div class="stat-value">{format_pct(ear)}</div>
                    <div class="stat-subtext">Nominal: {r_val_pct:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Plotly Trajectory Chart
        t_steps = np.linspace(0, t_val, 150)
        c_simple = [simple_interest_amount(p_val, r_val, float(s)) for s in t_steps]
        c_comp = [compound_interest_amount(p_val, r_val, float(s), compounding_frequency=m_val) for s in t_steps]
        c_cont = [continuous_compounding_amount(p_val, r_val, float(s)) for s in t_steps]

        fig_tvm = go.Figure()
        fig_tvm.add_trace(go.Scatter(x=t_steps, y=c_simple, mode='lines', name='Simple (Linear)', line=dict(color='#F59E0B', width=2)))
        fig_tvm.add_trace(go.Scatter(x=t_steps, y=c_comp, mode='lines', name=f'Compounded ({freq_choice.split()[0]})', line=dict(color='#38BDF8', width=3)))
        fig_tvm.add_trace(go.Scatter(x=t_steps, y=c_cont, mode='lines', name='Continuous Ceiling', line=dict(color='#10B981', width=2, dash='dot')))

        fig_tvm.update_layout(
            title="Capital Accumulation Curves",
            xaxis_title="Years",
            yaxis_title=f"Terminal Value ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            margin=dict(l=10, r=10, t=35, b=10),
            height=380,
        )
        st.plotly_chart(fig_tvm, use_container_width=True)


# ==============================================================================
# TAB 2: DEBT & AMORTIZATION
# ==============================================================================
with tab2:
    col_l1, col_l2 = st.columns([1, 2.2], gap="large")

    with col_l1:
        st.markdown("#### Loan Parameters")
        loan_p = st.number_input("Loan Amount ($P$)", min_value=10000.0, max_value=50000000.0, value=3000000.0, step=100000.0, key="loan_p")
        loan_r_pct = st.slider("Interest Rate (% p.a.)", min_value=1.0, max_value=24.0, value=8.5, step=0.1, key="loan_r")
        loan_r = loan_r_pct / 100.0
        loan_years = st.slider("Loan Tenure (Years)", min_value=1, max_value=30, value=20, step=1, key="loan_tenure")
        loan_months = loan_years * 12
        prepay_val = st.number_input("Monthly Prepayment Extra", min_value=0.0, max_value=200000.0, value=5000.0, step=1000.0, key="loan_prepay")

        # Negative Amortization Check
        base_monthly_interest = (loan_p * loan_r) / 12.0
        st.markdown("---")
        st.caption(f"Critical Monthly Interest Threshold: **{format_curr(base_monthly_interest, curr_sym)}/mo**")
        
        test_pmt = st.number_input("Stress Test Monthly Payment", min_value=500.0, max_value=float(base_monthly_interest * 2), value=float(round(base_monthly_interest * 0.9, -2)), step=500.0)
        neg_check = check_negative_amortization(loan_p, loan_r, test_pmt)
        if neg_check["is_negative_amortization"]:
            st.error(f"🚨 **Negative Amortization Triggered!** Payment is less than monthly interest ({format_curr(base_monthly_interest, curr_sym)}). Principal will diverge to infinity.")
        else:
            st.success("✅ **Amortizing:** Payment covers interest and reduces principal.")

    # Core Amortization Schedules
    base_emi = calculate_emi(loan_p, loan_r, loan_months)
    schedule_base_df = cached_amortization_schedule(loan_p, loan_r, loan_months, 0.0)
    schedule_prep_df = cached_amortization_schedule(loan_p, loan_r, loan_months, prepay_val)
    prep_stats = calculate_prepayment_savings(loan_p, loan_r, loan_months, prepay_val)

    with col_l2:
        lm1, lm2, lm3, lm4 = st.columns(4)
        with lm1:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Monthly EMI</div>
                    <div class="stat-value">{format_curr(base_emi, curr_sym)}</div>
                    <div class="stat-subtext">{loan_months} months scheduled</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with lm2:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Total Interest (Base)</div>
                    <div class="stat-value">{format_curr(prep_stats['original_total_interest'], curr_sym)}</div>
                    <div class="stat-subtext">{(prep_stats['original_total_interest']/loan_p)*100:.1f}% of loan amount</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with lm3:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Interest Saved</div>
                    <div class="stat-value" style="color: #10B981;">{format_curr(prep_stats['interest_saved'], curr_sym)}</div>
                    <div class="stat-subtext">{prep_stats['percentage_interest_saved']:.1f}% cost reduction</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with lm4:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Tenure Shortened</div>
                    <div class="stat-value" style="color: #38BDF8;">{prep_stats['months_saved']} Mo</div>
                    <div class="stat-subtext">Paid off in {prep_stats['new_tenure_months']/12:.1f} yrs</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Plot 1: Stacked Principal vs Interest Breakdown
        fig_breakdown = go.Figure()
        fig_breakdown.add_trace(go.Scatter(
            x=schedule_base_df["Month"],
            y=schedule_base_df["Principal_Paid"],
            mode='lines',
            name='Principal Paid',
            stackgroup='one',
            fillcolor='rgba(16, 185, 129, 0.65)',
            line=dict(color='#10B981', width=1)
        ))
        fig_breakdown.add_trace(go.Scatter(
            x=schedule_base_df["Month"],
            y=schedule_base_df["Interest_Paid"],
            mode='lines',
            name='Interest Paid',
            stackgroup='one',
            fillcolor='rgba(244, 63, 94, 0.65)',
            line=dict(color='#F43F5E', width=1)
        ))
        fig_breakdown.update_layout(
            title="Monthly Payment Split: Principal vs. Interest Over Time",
            xaxis_title="Month",
            yaxis_title=f"Amount ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            hovermode="x unified",
            margin=dict(l=10, r=10, t=35, b=10),
            height=300,
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)

        # Plot 2: Outstanding Balance Trajectory
        fig_bal = go.Figure()
        fig_bal.add_trace(go.Scatter(x=schedule_base_df["Month"], y=schedule_base_df["Closing_Balance"], mode='lines', name='Baseline Loan', line=dict(color='#F43F5E', width=2)))
        fig_bal.add_trace(go.Scatter(x=schedule_prep_df["Month"], y=schedule_prep_df["Closing_Balance"], mode='lines', name=f'Accelerated (+{format_curr(prepay_val, curr_sym)}/mo)', line=dict(color='#38BDF8', width=2, dash='dash')))
        fig_bal.update_layout(
            title="Loan Balance Payoff Curve",
            xaxis_title="Month",
            yaxis_title=f"Balance ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            hovermode="x unified",
            margin=dict(l=10, r=10, t=35, b=10),
            height=280,
        )
        st.plotly_chart(fig_bal, use_container_width=True)

        # Download Button
        csv_bytes = schedule_base_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Amortization Schedule (CSV)",
            data=csv_bytes,
            file_name="fdss_loan_amortization_schedule.csv",
            mime="text/csv",
        )


# ==============================================================================
# TAB 3: WEALTH & SIP PLANNER
# ==============================================================================
with tab3:
    col_s1, col_s2 = st.columns([1, 2.2], gap="large")

    with col_s1:
        st.markdown("#### Investment & Inflation Inputs")
        sip_amount = st.number_input("Monthly Contribution", min_value=500.0, max_value=1000000.0, value=15000.0, step=1000.0, key="sip_amt")
        sip_r_pct = st.slider("Expected Nominal Return (% p.a.)", min_value=1.0, max_value=30.0, value=12.0, step=0.5, key="sip_r")
        sip_r = sip_r_pct / 100.0
        sip_tenure = st.slider("Investment Horizon (Years)", min_value=1, max_value=40, value=20, step=1, key="sip_t")
        sip_step_pct = st.slider("Annual Step-Up Escalation (%)", min_value=0.0, max_value=30.0, value=10.0, step=1.0, key="sip_step")
        sip_inf_pct = st.slider("Expected Annual Inflation (%)", min_value=0.0, max_value=15.0, value=6.0, step=0.5, key="sip_inf")
        sip_inf = sip_inf_pct / 100.0

    # Computations
    sip_base = calculate_sip_wealth(sip_amount, sip_r, sip_tenure)
    sip_step_summary, sip_step_df = calculate_step_up_sip(sip_amount, sip_r, sip_tenure, annual_step_up_percent=sip_step_pct)
    r_fisher = real_rate_of_return(sip_r, sip_inf)
    half_life_val = purchasing_power_half_life(sip_inf) if sip_inf > 0 else float('inf')

    with col_s2:
        sm1, sm2, sm3, sm4 = st.columns(4)
        with sm1:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Fixed SIP Corpus</div>
                    <div class="stat-value">{format_curr(sip_base['future_value'], curr_sym)}</div>
                    <div class="stat-subtext">Invested: {format_curr(sip_base['total_invested'], curr_sym)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with sm2:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Step-Up Corpus (+{sip_step_pct:.0f}%)</div>
                    <div class="stat-value" style="color: #10B981;">{format_curr(sip_step_summary['future_value'], curr_sym)}</div>
                    <div class="stat-subtext">Invested: {format_curr(sip_step_summary['total_invested'], curr_sym)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with sm3:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Fisher Real Return</div>
                    <div class="stat-value">{format_pct(r_fisher)}</div>
                    <div class="stat-subtext">Nominal {sip_r_pct:.1f}% - Inf {sip_inf_pct:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with sm4:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Monetary Half-Life</div>
                    <div class="stat-value" style="color: #F59E0B;">{half_life_val:.1f} Yrs</div>
                    <div class="stat-subtext">50% Purchasing Power Loss</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Multi-Year Corpus Trajectory
        years_list = list(range(1, sip_tenure + 1))
        corpus_base_list, corpus_step_list, corpus_real_list, capital_list = [], [], [], []
        
        for y in years_list:
            b_res = calculate_sip_wealth(sip_amount, sip_r, y)
            s_sum, _ = calculate_step_up_sip(sip_amount, sip_r, y, annual_step_up_percent=sip_step_pct)
            corpus_base_list.append(b_res["future_value"])
            corpus_step_list.append(s_sum["future_value"])
            corpus_real_list.append(s_sum["future_value"] * math.pow(1.0 + sip_inf, -y))
            capital_list.append(s_sum["total_invested"])

        fig_wealth = go.Figure()
        fig_wealth.add_trace(go.Scatter(x=years_list, y=corpus_step_list, mode='lines', name=f'Step-Up SIP (+{sip_step_pct:.0f}%/yr)', line=dict(color='#10B981', width=3)))
        fig_wealth.add_trace(go.Scatter(x=years_list, y=corpus_base_list, mode='lines', name='Fixed Monthly SIP', line=dict(color='#38BDF8', width=2.5)))
        fig_wealth.add_trace(go.Scatter(x=years_list, y=corpus_real_list, mode='lines', name='Inflation-Adjusted Real Value', line=dict(color='#F59E0B', width=2, dash='dash')))
        fig_wealth.add_trace(go.Scatter(x=years_list, y=capital_list, mode='lines', name='Capital Outlay', line=dict(color='#64748B', width=1.5, dash='dot')))

        fig_wealth.update_layout(
            title="Corpus Growth: Nominal vs. Inflation-Adjusted Purchasing Power",
            xaxis_title="Years",
            yaxis_title=f"Valuation ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            hovermode="x unified",
            margin=dict(l=10, r=10, t=35, b=10),
            height=380,
        )
        st.plotly_chart(fig_wealth, use_container_width=True)


# ==============================================================================
# TAB 4: CAPITAL BUDGETING & IRR
# ==============================================================================
with tab4:
    col_c1, col_c2 = st.columns([1, 2.2], gap="large")

    with col_c1:
        st.markdown("#### Project Cash Flows")
        preset = st.selectbox(
            "Project Template",
            options=["Commercial Tech Venture", "Infrastructure Expansion", "Manufacturing Plant", "Custom"],
            index=0
        )
        if preset == "Commercial Tech Venture":
            default_flow = "-500000, 100000, 180000, 240000, 320000, 400000"
        elif preset == "Infrastructure Expansion":
            default_flow = "-1000000, 150000, 180000, 220000, 250000, 280000, 310000, 350000"
        elif preset == "Manufacturing Plant":
            default_flow = "-2500000, 400000, 600000, 800000, 1000000, 1200000"
        else:
            default_flow = "-100000, 30000, 40000, 50000, 60000"

        cfs_str = st.text_input("Cash Flows [C_0, C_1, ..., C_T]", value=default_flow)
        try:
            cash_flow_list = [float(x.strip()) for x in cfs_str.split(",")]
        except Exception:
            cash_flow_list = [-100000.0, 30000.0, 40000.0, 50000.0, 60000.0]

        hurdle_pct = st.slider("Hurdle Rate / Cost of Capital (%)", min_value=1.0, max_value=30.0, value=12.0, step=0.5, key="cb_hurdle")
        hurdle_rate = hurdle_pct / 100.0

    # Solvers
    try:
        npv_val = net_present_value(hurdle_rate, cash_flow_list)
        irr_val, irr_trace = internal_rate_of_return_with_history(cash_flow_list, initial_guess=0.10)
        payback_val = discounted_payback_period(hurdle_rate, cash_flow_list)
        initial_invest = abs(cash_flow_list[0]) if cash_flow_list[0] < 0 else 1.0
        pv_in = sum(cf / math.pow(1.0 + hurdle_rate, t) for t, cf in enumerate(cash_flow_list) if t > 0)
        profit_index = pv_in / initial_invest
    except Exception as e:
        npv_val, irr_val, irr_trace, payback_val, profit_index = 0.0, 0.0, [], None, 1.0

    with col_c2:
        cm1, cm2, cm3, cm4 = st.columns(4)
        with cm1:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Net Present Value</div>
                    <div class="stat-value" style="color: {'#10B981' if npv_val >= 0 else '#F43F5E'};">{format_curr(npv_val, curr_sym)}</div>
                    <div class="stat-subtext">{'Value Accretive' if npv_val>=0 else 'Destroys Value'}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with cm2:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Internal Rate of Return</div>
                    <div class="stat-value" style="color: {'#10B981' if irr_val >= hurdle_rate else '#F43F5E'};">{format_pct(irr_val)}</div>
                    <div class="stat-subtext">Spread: {(irr_val - hurdle_rate)*100:+.2f}% vs Hurdle</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with cm3:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Discounted Payback</div>
                    <div class="stat-value">{f"{payback_val:.2f} Yrs" if payback_val else "Never"}</div>
                    <div class="stat-subtext">Breakeven period</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with cm4:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Profitability Index</div>
                    <div class="stat-value">{profit_index:.2f}</div>
                    <div class="stat-subtext">{'PI > 1.0 (Accept)' if profit_index > 1.0 else 'PI < 1.0 (Reject)'}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Plotly NPV Profile Curve
        r_scan = np.linspace(-0.15, max(0.50, irr_val * 1.5), 200)
        npv_curve = [net_present_value(float(r), cash_flow_list) for r in r_scan]

        fig_npv = go.Figure()
        fig_npv.add_trace(go.Scatter(x=r_scan * 100, y=npv_curve, mode='lines', name='NPV Profile', line=dict(color='#38BDF8', width=2.5)))
        fig_npv.add_hline(y=0.0, line_dash="solid", line_color="#64748B", line_width=1)
        fig_npv.add_trace(go.Scatter(
            x=[hurdle_pct], y=[npv_val], mode='markers+text',
            marker=dict(color='#F59E0B', size=10), text=["Hurdle"], textposition="top right", name="Hurdle Rate"
        ))
        fig_npv.add_trace(go.Scatter(
            x=[irr_val * 100], y=[0.0], mode='markers+text',
            marker=dict(color='#10B981', size=12, symbol='star'), text=[f"IRR: {irr_val*100:.2f}%"], textposition="bottom right", name="IRR Root"
        ))
        fig_npv.update_layout(
            title="NPV Profile Curve & Zero-Crossing Root",
            xaxis_title="Discount Rate (%)",
            yaxis_title=f"NPV ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            hovermode="x unified",
            margin=dict(l=10, r=10, t=35, b=10),
            height=360,
        )
        st.plotly_chart(fig_npv, use_container_width=True)

        if irr_trace:
            with st.expander("🔬 View Newton–Raphson Solver Convergence Iterations"):
                trace_df = pd.DataFrame(irr_trace)
                trace_df["r_k (%)"] = (trace_df["r_k"] * 100).round(4)
                trace_df["npv_k"] = trace_df["npv_k"].round(2)
                st.dataframe(trace_df[["iteration", "r_k (%)", "npv_k", "method"]], use_container_width=True)


# ==============================================================================
# TAB 5: MONTE CARLO RISK LAB
# ==============================================================================
with tab5:
    col_m1, col_m2 = st.columns([1, 2.2], gap="large")

    with col_m1:
        st.markdown("#### Stochastic Parameters")
        mc_s0 = st.number_input("Initial Portfolio ($S_0$)", min_value=10000.0, max_value=20000000.0, value=500000.0, step=50000.0, key="mc_s0")
        mc_mu_pct = st.slider("Expected Annual Drift (μ %)", min_value=-10.0, max_value=30.0, value=12.0, step=0.5, key="mc_mu")
        mc_mu = mc_mu_pct / 100.0
        mc_sigma_pct = st.slider("Annual Volatility (σ %)", min_value=2.0, max_value=60.0, value=18.0, step=0.5, key="mc_sigma")
        mc_sigma = mc_sigma_pct / 100.0
        mc_years = st.slider("Horizon ($T$ Years)", min_value=1, max_value=30, value=10, step=1, key="mc_t")
        mc_paths = st.select_slider("Simulation Trajectories ($M$)", options=[250, 500, 1000, 2000, 5000], value=1000, key="mc_paths")
        mc_target = st.number_input("Target Wealth Milestone", min_value=100000.0, max_value=50000000.0, value=1500000.0, step=100000.0, key="mc_target")
        mc_seed = st.number_input("RNG Seed", min_value=1, max_value=999999, value=42, step=1, key="mc_seed")

    # Vectorized Simulation via Cache
    time_grid, paths_matrix = cached_monte_carlo(
        s0=mc_s0,
        mu=mc_mu,
        sigma=mc_sigma,
        t_years=float(mc_years),
        n_steps=mc_years * 12,
        n_paths=mc_paths,
        seed=int(mc_seed)
    )

    terminal_wealths = paths_matrix[-1, :]
    stats_dict = compute_simulation_statistics(terminal_wealths, s0=mc_s0)
    drag_dict = calculate_volatility_drag(mc_s0, mc_mu, mc_sigma, float(mc_years))
    goal_prob = goal_attainment_probability(terminal_wealths, mc_target)
    risk_dict = calculate_value_at_risk(terminal_wealths, s0=mc_s0, confidence_level=0.95)

    with col_m2:
        mm1, mm2, mm3, mm4 = st.columns(4)
        with mm1:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Expected Mean</div>
                    <div class="stat-value">{format_curr(stats_dict['sample_mean'], curr_sym)}</div>
                    <div class="stat-subtext">Median: {format_curr(stats_dict['sample_median'], curr_sym)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with mm2:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Volatility Drag</div>
                    <div class="stat-value" style="color: #F43F5E;">{drag_dict['annual_volatility_drag_percent']:.2f}%</div>
                    <div class="stat-subtext">Compounding drag: -½ σ²</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with mm3:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">Goal Probability</div>
                    <div class="stat-value" style="color: #10B981;">{format_pct(goal_prob)}</div>
                    <div class="stat-subtext">Target: {format_curr(mc_target, curr_sym)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with mm4:
            st.markdown(
                f"""
                <div class="fdss-stat-card">
                    <div class="stat-label">95% Value at Risk</div>
                    <div class="stat-value" style="color: #818CF8;">{format_curr(risk_dict['cutoff_price'], curr_sym)}</div>
                    <div class="stat-subtext">Max Loss: {format_curr(risk_dict['value_at_risk'], curr_sym)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Plot 1: Vectorized Trajectory Fan Chart
        fig_fan = go.Figure()
        sample_subset = min(60, mc_paths)
        for i in range(sample_subset):
            fig_fan.add_trace(go.Scatter(
                x=time_grid, y=paths_matrix[:, i], mode='lines',
                line=dict(color='rgba(56, 189, 248, 0.12)', width=1), hoverinfo='skip', showlegend=False
            ))

        mean_path = np.mean(paths_matrix, axis=1)
        median_path = np.median(paths_matrix, axis=1)
        p05_path = np.percentile(paths_matrix, 5, axis=1)

        fig_fan.add_trace(go.Scatter(x=time_grid, y=mean_path, mode='lines', name='Expected Mean', line=dict(color='#10B981', width=3)))
        fig_fan.add_trace(go.Scatter(x=time_grid, y=median_path, mode='lines', name='Median Path (50th %)', line=dict(color='#38BDF8', width=2.5)))
        fig_fan.add_trace(go.Scatter(x=time_grid, y=p05_path, mode='lines', name='5th %ile (95% VaR Floor)', line=dict(color='#F43F5E', width=2, dash='dash')))
        fig_fan.add_hline(y=mc_target, line_dash="solid", line_color="#F59E0B", annotation_text=f"Target: {format_curr(mc_target, curr_sym)}", annotation_position="top left")

        fig_fan.update_layout(
            title=f"Geometric Brownian Motion Simulation ({mc_paths:,} Paths)",
            xaxis_title="Years",
            yaxis_title=f"Portfolio Valuation ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            margin=dict(l=10, r=10, t=35, b=10),
            height=360,
        )
        st.plotly_chart(fig_fan, use_container_width=True)

        # Plot 2: Terminal Wealth Distribution Histogram
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=terminal_wealths, nbinsx=50,
            marker=dict(color='rgba(56, 189, 248, 0.7)', line=dict(color='#38BDF8', width=1)),
            name="Terminal Wealth"
        ))
        fig_hist.add_vline(x=risk_dict['cutoff_price'], line_dash="dash", line_color="#F43F5E", line_width=2, annotation_text="95% VaR Floor", annotation_position="top left")
        fig_hist.add_vline(x=mc_target, line_dash="dash", line_color="#F59E0B", line_width=2, annotation_text="Target Goal", annotation_position="top right")
        fig_hist.update_layout(
            title="Terminal Wealth Distribution at Horizon T",
            xaxis_title=f"Terminal Value ({curr_sym})",
            yaxis_title="Path Frequency",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            margin=dict(l=10, r=10, t=35, b=10),
            height=260,
        )
        st.plotly_chart(fig_hist, use_container_width=True)


# ==============================================================================
# MINIMALIST FOOTER
# ==============================================================================

st.markdown(
    """
    <div class="app-footer">
        FDSS Quantitative Finance Studio • © 2026 Atharv Ranade. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
