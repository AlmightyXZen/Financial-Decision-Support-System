"""
Financial Decision Support System (FDSS)
================================================================================
An Interactive Mathematical Modeling, Numerical Analysis & Stochastic Simulation
Web Application for Rigorous Financial Decision-Making.

Research Portfolio & Convention Submission:
Category: Pure Sciences (Applied Mathematics & Statistics)
================================================================================
"""

import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

# Import the 5 First-Principles Mathematical Engines
from models.time_value import (
    simple_interest,
    simple_interest_amount,
    compound_interest_amount,
    accrued_compound_interest,
    continuous_compounding_amount,
    discrete_to_continuous_yield,
    continuous_to_discrete_yield,
    present_value,
    future_value,
    nominal_to_effective_rate,
    effective_to_nominal_rate,
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
    npv_first_derivative,
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
# 1. PAGE CONFIGURATION & THEME STYLING
# ==============================================================================

st.set_page_config(
    page_title="FDSS | Financial Decision Support System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
/* Global Dark Slate Glassmorphism Theme */
:root {
    --bg-primary: #070F1E;
    --bg-card: rgba(14, 27, 49, 0.75);
    --border-card: rgba(56, 189, 248, 0.2);
    --accent-cyan: #38BDF8;
    --accent-emerald: #10B981;
    --accent-rose: #F43F5E;
    --accent-amber: #F59E0B;
    --accent-purple: #818CF8;
    --text-primary: #F8FAFC;
    --text-muted: #94A3B8;
}

.stApp {
    background: radial-gradient(circle at 15% 15%, #0B192C 0%, #070F1E 100%);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Glassmorphism Card Containers */
.fdss-card {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.45);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.fdss-card:hover {
    border-color: rgba(56, 189, 248, 0.45);
}

.fdss-card-danger {
    background: rgba(244, 63, 94, 0.08);
    border: 1px solid rgba(244, 63, 94, 0.4);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1.2rem;
}

.fdss-card-success {
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.4);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1.2rem;
}

/* Metric Display Badges */
.metric-badge {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.4rem;
}

.badge-cyan { background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); }
.badge-emerald { background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }
.badge-rose { background: rgba(244, 63, 94, 0.15); color: #F43F5E; border: 1px solid rgba(244, 63, 94, 0.3); }
.badge-amber { background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); }
.badge-purple { background: rgba(129, 140, 248, 0.15); color: #818CF8; border: 1px solid rgba(129, 140, 248, 0.3); }

.kpi-title {
    color: var(--text-muted);
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 0.2rem;
}

.kpi-value {
    color: var(--text-primary);
    font-size: 1.7rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    font-family: 'JetBrains Mono', monospace;
}

.kpi-subtext {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
}

/* Tab Header Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    padding-bottom: 4px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 8px 8px 0 0;
    color: var(--text-muted);
    font-weight: 600;
    padding: 8px 16px;
}

.stTabs [aria-selected="true"] {
    background-color: rgba(56, 189, 248, 0.12) !important;
    color: var(--accent-cyan) !important;
    border-bottom: 2px solid var(--accent-cyan) !important;
}

/* Sidebar Branding */
.sidebar-brand {
    padding: 1rem 0;
    border-bottom: 1px solid rgba(56, 189, 248, 0.15);
    margin-bottom: 1.5rem;
}

.sidebar-title {
    font-size: 1.25rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38BDF8, #818CF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Helper function for currency formatting
def format_curr(value: float, symbol: str = "₹") -> str:
    if abs(value) >= 1e7:
        return f"{symbol}{value / 1e7:.2f} Cr"
    elif abs(value) >= 1e5:
        return f"{symbol}{value / 1e5:.2f} L"
    return f"{symbol}{value:,.2f}"

def format_pct(value: float) -> str:
    return f"{value * 100:.2f}%"


# ==============================================================================
# 2. SIDEBAR CONTROLS & GLOBAL NAVIGATION
# ==============================================================================

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-title">⚡ FDSS Core Engine</div>
            <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px;">
                Financial Decision Support System<br>
                Applied Mathematics & Statistics Lab
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    currency_choice = st.selectbox(
        "Currency Display Unit",
        options=["₹ (INR)", "$ (USD)", "€ (EUR)", "£ (GBP)"],
        index=0,
    )
    curr_sym = currency_choice.split()[0]
    
    st.markdown("---")
    st.markdown("### 📚 Mathematical Foundations")
    st.caption(
        "Every calculation is derived from first-principles calculus, differential equations, "
        "and stochastic integration. Zero third-party financial black boxes."
    )
    
    st.markdown(
        r"""
        - **ODE:** $dA/dt = rA \implies A(t) = Pe^{rt}$
        - **Annuities:** $S_n = P \frac{(1+r)^n - 1}{r}$
        - **Amortization:** $E > P \cdot \frac{r}{12}$
        - **Roots:** Newton–Raphson + Abel–Ruffini
        - **SDE:** $dS = \mu S dt + \sigma S dW$
        """
    )
    
    st.markdown("---")
    st.caption("Avishkar Research Convention | Category 3: Pure Sciences")


# ==============================================================================
# 3. HERO BANNER
# ==============================================================================

st.markdown(
    """
    <div style="margin-bottom: 1.5rem;">
        <span class="metric-badge badge-cyan">Pure Sciences Category 3</span>
        <span class="metric-badge badge-emerald">First-Principles Derivations</span>
        <span class="metric-badge badge-purple">IEEE 754 Verified</span>
        <h1 style="font-size: 2.3rem; font-weight: 800; margin-top: 0.4rem; margin-bottom: 0.2rem; letter-spacing: -0.02em;">
            Financial Decision Support System (FDSS)
        </h1>
        <p style="color: #94A3B8; font-size: 1.05rem; margin-top: 0;">
            A Rigorous Analytical Platform for Deterministic Yield Curvature, Amortization Singularities, 
            Numerical Root-Finding, and Itô Stochastic Monte Carlo Simulation.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⏳ Time Value & Yields",
    "💳 Debt & Amortization",
    "📈 SIP & Inflation Reality",
    "📊 Capital Budgeting & IRR",
    "🎲 Monte Carlo Stochastic Lab",
])


# ==============================================================================
# TAB 1: TIME VALUE OF MONEY & ASYMPTOTIC YIELDS
# ==============================================================================
with tab1:
    st.markdown("### ⏳ Deterministic Growth & Asymptotic Compounding")
    st.markdown(
        "Compare linear subadditive simple interest against discrete exponential growth and its "
        "autonomous differential equation limit: $\\lim_{m \\to \\infty} P(1 + r/m)^{mt} = P e^{rt}$."
    )
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="fdss-card">', unsafe_allow_html=True)
        st.markdown("#### Input Parameters")
        p_val = st.number_input("Principal Capital ($P$)", min_value=1000.0, max_value=10000000.0, value=100000.0, step=10000.0, key="tvm_p")
        r_val_pct = st.slider("Nominal Annual Rate ($r$ %)", min_value=0.1, max_value=30.0, value=10.0, step=0.1, key="tvm_r")
        r_val = r_val_pct / 100.0
        t_val = st.slider("Horizon ($t$ in Years)", min_value=0.5, max_value=40.0, value=10.0, step=0.5, key="tvm_t")
        m_options = {"Annual (m=1)": 1, "Semi-Annual (m=2)": 2, "Quarterly (m=4)": 4, "Monthly (m=12)": 12, "Daily (m=365)": 365}
        m_label = st.selectbox("Compounding Frequency ($m$)", options=list(m_options.keys()), index=3, key="tvm_m")
        m_val = m_options[m_label]
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Mathematical Banner
        st.latex(r"\frac{dA}{dt} = r A(t) \implies A(t) = P \cdot e^{rt}")
        st.latex(r"\text{EAR} = \left(1 + \frac{r}{m}\right)^m - 1")

    # Compute outcomes
    a_simple = simple_interest_amount(p_val, r_val, t_val)
    a_compound = compound_interest_amount(p_val, r_val, t_val, compounding_frequency=m_val)
    a_cont = continuous_compounding_amount(p_val, r_val, t_val)
    ear = nominal_to_effective_rate(r_val, compounding_frequency=m_val)
    comp_bonus = a_compound - a_simple
    euler_bonus = a_cont - a_compound

    with col2:
        # KPI Cards
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-amber">Simple Interest</span>
                    <div class="kpi-title">Terminal Wealth</div>
                    <div class="kpi-value">{format_curr(a_simple, curr_sym)}</div>
                    <div class="kpi-subtext">Linear growth: $P(1+rt)$</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kpi2:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-cyan">Discrete Compounding</span>
                    <div class="kpi-title">Terminal Wealth ({m_label.split()[0]})</div>
                    <div class="kpi-value">{format_curr(a_compound, curr_sym)}</div>
                    <div class="kpi-subtext">+{format_curr(comp_bonus, curr_sym)} vs Simple</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kpi3:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-emerald">Continuous (Euler)</span>
                    <div class="kpi-title">Infinitesimal Limit</div>
                    <div class="kpi-value">{format_curr(a_cont, curr_sym)}</div>
                    <div class="kpi-subtext">Theoretical Maximum</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kpi4:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-purple">True Yield</span>
                    <div class="kpi-title">Effective Annual Rate</div>
                    <div class="kpi-value">{format_pct(ear)}</div>
                    <div class="kpi-subtext">Nominal: {r_val_pct:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Plotly Trajectory Graph
        time_steps = np.linspace(0, t_val, 200)
        curve_simple = [simple_interest_amount(p_val, r_val, float(s)) for s in time_steps]
        curve_compound = [compound_interest_amount(p_val, r_val, float(s), compounding_frequency=m_val) for s in time_steps]
        curve_cont = [continuous_compounding_amount(p_val, r_val, float(s)) for s in time_steps]

        fig_tvm = go.Figure()
        fig_tvm.add_trace(go.Scatter(x=time_steps, y=[p_val]*len(time_steps), mode='lines', name='Initial Capital', line=dict(color='#64748B', dash='dash')))
        fig_tvm.add_trace(go.Scatter(x=time_steps, y=curve_simple, mode='lines', name='Simple Interest (Linear)', line=dict(color='#F59E0B', width=2)))
        fig_tvm.add_trace(go.Scatter(x=time_steps, y=curve_compound, mode='lines', name=f'Discrete Compounding ({m_label.split()[0]})', line=dict(color='#38BDF8', width=3)))
        fig_tvm.add_trace(go.Scatter(x=time_steps, y=curve_cont, mode='lines', name='Continuous Compounding (Euler ODE)', line=dict(color='#10B981', width=2, dash='dot')))

        fig_tvm.update_layout(
            title="Capital Trajectories: Linear Subadditivity vs. Exponential Expansion",
            xaxis_title="Time (Years)",
            yaxis_title=f"Accumulated Capital ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode="x unified",
        )
        st.plotly_chart(fig_tvm, use_container_width=True)

    # Frequency Asymptote Exploration
    st.markdown("#### 🔬 Compounding Frequency Monotonicity & Asymptotic Convergence")
    freqs = [1, 2, 4, 12, 52, 365, 1000]
    freq_labels = ["Annual", "Semi-Ann", "Quarterly", "Monthly", "Weekly", "Daily", "Ultra-High"]
    terminal_by_freq = [compound_interest_amount(p_val, r_val, t_val, compounding_frequency=f) for f in freqs]
    ears_by_freq = [nominal_to_effective_rate(r_val, compounding_frequency=f) for f in freqs]

    fig_freq = go.Figure()
    fig_freq.add_trace(go.Bar(
        x=freq_labels,
        y=terminal_by_freq,
        text=[format_curr(v, curr_sym) for v in terminal_by_freq],
        textposition="auto",
        marker=dict(color=terminal_by_freq, colorscale="Viridis"),
        name="Terminal Wealth"
    ))
    fig_freq.add_hline(y=a_cont, line_dash="dash", line_color="#F43F5E", annotation_text=f"Continuous Limit: {format_curr(a_cont, curr_sym)}", annotation_position="top left")
    fig_freq.update_layout(
        title="Terminal Wealth vs. Compounding Frequency (Approaching Euler's Limit)",
        xaxis_title="Compounding Schedule",
        yaxis_title=f"Terminal Wealth ({curr_sym})",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(14, 27, 49, 0.4)",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_freq, use_container_width=True)


# ==============================================================================
# TAB 2: CONSUMER DEBT & LOAN AMORTIZATION
# ==============================================================================
with tab2:
    st.markdown("### 💳 Consumer Debt, EMI Mathematics & Negative Amortization")
    st.markdown(
        "Derived from finite geometric series discounting. Explore loan amortization mechanics, "
        "interest-to-principal crossover, accelerated prepayment savings, and the severe mathematical "
        "singularity of **negative amortization**."
    )
    
    col_l1, col_l2 = st.columns([1, 2])
    
    with col_l1:
        st.markdown('<div class="fdss-card">', unsafe_allow_html=True)
        st.markdown("#### Loan Parameters")
        loan_p = st.number_input("Loan Principal ($P$)", min_value=10000.0, max_value=50000000.0, value=3000000.0, step=100000.0, key="loan_p")
        loan_r_pct = st.slider("Interest Rate (% per annum)", min_value=1.0, max_value=24.0, value=8.5, step=0.1, key="loan_r")
        loan_r = loan_r_pct / 100.0
        loan_tenure_years = st.slider("Tenure (Years)", min_value=1, max_value=30, value=20, step=1, key="loan_tenure")
        loan_tenure_months = loan_tenure_years * 12
        
        prepayment_val = st.number_input("Extra Monthly Prepayment", min_value=0.0, max_value=200000.0, value=5000.0, step=1000.0, key="loan_prep")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Negative Amortization Stress Test Widget
        st.markdown('<div class="fdss-card">', unsafe_allow_html=True)
        st.markdown("#### ⚠️ Negative Amortization Stress Lab")
        monthly_interest_accrual = (loan_p * loan_r) / 12.0
        st.caption(f"Initial monthly interest accrual: **{format_curr(monthly_interest_accrual, curr_sym)}**")
        
        test_payment = st.number_input(
            "Test Custom Payment ($E$)",
            min_value=1000.0,
            max_value=float(monthly_interest_accrual * 2),
            value=float(round(monthly_interest_accrual * 0.9, -2)),
            step=500.0,
            key="test_pmt"
        )
        
        is_neg_amort, shortfall = check_negative_amortization(loan_p, loan_r, test_payment)
        if is_neg_amort:
            st.error(
                f"🚨 **DIVERGENCE ALERT:** Payment of {format_curr(test_payment, curr_sym)} is LESS than monthly interest "
                f"of {format_curr(monthly_interest_accrual, curr_sym)}. Unpaid interest shortfall "
                f"({format_curr(shortfall, curr_sym)}/mo) capitalizes into the principal! Debt diverges to infinity."
            )
            st.latex(r"\lim_{k \to \infty} B_k = +\infty")
        else:
            st.success(
                f"✅ **CONVERGENT:** Payment {format_curr(test_payment, curr_sym)} exceeds monthly interest accrual. Principal amortizes."
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.latex(r"E = P \cdot \frac{\frac{r}{12}\left(1 + \frac{r}{12}\right)^n}{\left(1 + \frac{r}{12}\right)^n - 1}")

    # Standard calculations
    base_emi = calculate_emi(loan_p, loan_r, loan_tenure_months)
    schedule_base = generate_amortization_schedule(loan_p, loan_r, loan_tenure_months, prepayment_per_month=0.0)
    total_interest_base = sum(entry["interest"] for entry in schedule_base)
    total_outflow_base = sum(entry["payment"] for entry in schedule_base)

    # Prepayment calculations
    prep_analytics = calculate_prepayment_savings(loan_p, loan_r, loan_tenure_months, prepayment_val)
    schedule_prep = generate_amortization_schedule(loan_p, loan_r, loan_tenure_months, prepayment_per_month=prepayment_val)

    with col_l2:
        # KPI Row
        kp1, kp2, kp3, kp4 = st.columns(4)
        with kp1:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-cyan">Standard EMI</span>
                    <div class="kpi-title">Monthly Obligation</div>
                    <div class="kpi-value">{format_curr(base_emi, curr_sym)}</div>
                    <div class="kpi-subtext">{loan_tenure_months} Scheduled Months</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kp2:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-rose">Total Interest</span>
                    <div class="kpi-title">Cumulative Cost</div>
                    <div class="kpi-value">{format_curr(total_interest_base, curr_sym)}</div>
                    <div class="kpi-subtext">{(total_interest_base/loan_p)*100:.1f}% of Principal</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kp3:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-emerald">Interest Saved</span>
                    <div class="kpi-title">With Prepayment</div>
                    <div class="kpi-value">{format_curr(prep_analytics['interest_saved'], curr_sym)}</div>
                    <div class="kpi-subtext">{(prep_analytics['interest_saved']/total_interest_base)*100:.1f}% Reduction</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kp4:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-purple">Time Shortened</span>
                    <div class="kpi-title">Tenure Reduction</div>
                    <div class="kpi-value">{prep_analytics['months_saved']} Mo</div>
                    <div class="kpi-subtext">Finished in {prep_analytics['new_tenure_months']/12:.1f} yrs</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Plot 1: Stacked Area Breakdown of Principal vs Interest Over Time
        df_base = pd.DataFrame(schedule_base)
        fig_amort = go.Figure()
        fig_amort.add_trace(go.Scatter(
            x=df_base["month"],
            y=df_base["principal"],
            mode='lines',
            name='Principal Paid',
            stackgroup='one',
            fillcolor='rgba(16, 185, 129, 0.65)',
            line=dict(color='#10B981', width=1)
        ))
        fig_amort.add_trace(go.Scatter(
            x=df_base["month"],
            y=df_base["interest"],
            mode='lines',
            name='Interest Paid',
            stackgroup='one',
            fillcolor='rgba(244, 63, 94, 0.65)',
            line=dict(color='#F43F5E', width=1)
        ))
        fig_amort.update_layout(
            title="Monthly Payment Composition: The 'Interest Flip' Phenomenon",
            xaxis_title="Tenure Month",
            yaxis_title=f"Monthly Payment Breakdown ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            hovermode="x unified",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_amort, use_container_width=True)

        # Plot 2: Outstanding Balance Trajectory (Baseline vs Accelerated Prepayment)
        df_prep = pd.DataFrame(schedule_prep)
        fig_bal = go.Figure()
        fig_bal.add_trace(go.Scatter(
            x=df_base["month"],
            y=df_base["remaining_balance"],
            mode='lines',
            name='Baseline Schedule',
            line=dict(color='#F43F5E', width=2.5)
        ))
        fig_bal.add_trace(go.Scatter(
            x=df_prep["month"],
            y=df_prep["remaining_balance"],
            mode='lines',
            name=f'Accelerated (+{format_curr(prepayment_val, curr_sym)}/mo)',
            line=dict(color='#38BDF8', width=2.5, dash='dash')
        ))
        fig_bal.update_layout(
            title="Principal Balance Amortization Trajectory",
            xaxis_title="Tenure Month",
            yaxis_title=f"Remaining Balance ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            hovermode="x unified",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_bal, use_container_width=True)

    # Schedule Table & CSV Download
    with st.expander("📄 View & Download Full Amortization Schedule (CSV)"):
        st.dataframe(df_base[["month", "payment", "principal", "interest", "remaining_balance"]].head(60), use_container_width=True)
        csv_data = df_base.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Complete Schedule CSV",
            data=csv_data,
            file_name="fdss_loan_amortization_schedule.csv",
            mime="text/csv",
        )


# ==============================================================================
# TAB 3: WEALTH ACCUMULATION & INFLATION REALITY
# ==============================================================================
with tab3:
    st.markdown("### 📈 Wealth Accumulation, Step-Up SIP & Exact Fisher Inflation")
    st.markdown(
        "Demonstrates regular Annuity-Due SIP accumulation, annual step-up compounding escalation, "
        "and the devastating reality of monetary purchasing power erosion via the exact Fisher equation: "
        "$(1 + r_{\\text{nom}}) = (1 + r_{\\text{real}})(1 + i)$."
    )
    
    col_s1, col_s2 = st.columns([1, 2])
    
    with col_s1:
        st.markdown('<div class="fdss-card">', unsafe_allow_html=True)
        st.markdown("#### Investment & Inflation Inputs")
        sip_monthly = st.number_input("Monthly Investment ($P$)", min_value=500.0, max_value=500000.0, value=15000.0, step=1000.0, key="sip_p")
        sip_r_pct = st.slider("Expected Nominal Annual Return ($r$ %)", min_value=1.0, max_value=25.0, value=12.0, step=0.5, key="sip_r")
        sip_r = sip_r_pct / 100.0
        sip_years = st.slider("Horizon ($T$ in Years)", min_value=1, max_value=40, value=20, step=1, key="sip_t")
        sip_step_up_pct = st.slider("Annual Step-Up Rate ($g$ %)", min_value=0.0, max_value=25.0, value=10.0, step=1.0, key="sip_g")
        sip_step_up = sip_step_up_pct / 100.0
        sip_inf_pct = st.slider("Expected Annual Inflation ($i$ %)", min_value=0.0, max_value=15.0, value=6.0, step=0.5, key="sip_inf")
        sip_inf = sip_inf_pct / 100.0
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.latex(r"S_n = P(1 + j)\frac{(1 + j)^n - 1}{j}")
        st.latex(r"1 + r_n = (1 + r_r)(1 + i) \implies r_r = \frac{1 + r_n}{1 + i} - 1")
        st.latex(r"t_{1/2} = \frac{\ln 2}{\ln(1 + i)}")

    # Computations
    standard_sip_res = calculate_sip_wealth(sip_monthly, sip_r, sip_years)
    stepup_sip_res = calculate_step_up_sip(sip_monthly, sip_r, sip_years, sip_step_up)
    r_real = real_rate_of_return(sip_r, sip_inf)
    half_life = purchasing_power_half_life(sip_inf) if sip_inf > 0 else float('inf')
    
    # Real purchasing power of terminal corpora
    real_wealth_standard = standard_sip_res["future_value"] * math.pow(1.0 + sip_inf, -sip_years)
    real_wealth_stepup = stepup_sip_res["future_value"] * math.pow(1.0 + sip_inf, -sip_years)

    with col_s2:
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-cyan">Standard SIP</span>
                    <div class="kpi-title">Terminal Nominal Corpus</div>
                    <div class="kpi-value">{format_curr(standard_sip_res['future_value'], curr_sym)}</div>
                    <div class="kpi-subtext">Invested: {format_curr(standard_sip_res['total_invested'], curr_sym)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k2:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-emerald">Step-Up SIP (+{sip_step_up_pct:.0f}%)</span>
                    <div class="kpi-title">Escalated Corpus</div>
                    <div class="kpi-value">{format_curr(stepup_sip_res['future_value'], curr_sym)}</div>
                    <div class="kpi-subtext">Invested: {format_curr(stepup_sip_res['total_invested'], curr_sym)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k3:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-rose">Fisher Real Return</span>
                    <div class="kpi-title">Net After Inflation</div>
                    <div class="kpi-value">{format_pct(r_real)}</div>
                    <div class="kpi-subtext">Nominal {sip_r_pct:.1f}% - Inf {sip_inf_pct:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k4:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-amber">Monetary Half-Life</span>
                    <div class="kpi-title">50% Purchasing Power Loss</div>
                    <div class="kpi-value">{half_life:.1f} Yrs</div>
                    <div class="kpi-subtext">At {sip_inf_pct:.1f}% constant inflation</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Multi-Year Wealth Trajectory Chart
        years_arr = list(range(1, sip_years + 1))
        inv_std, val_std, val_step, val_real = [], [], [], []
        
        for y in years_arr:
            s_std = calculate_sip_wealth(sip_monthly, sip_r, y)
            s_step = calculate_step_up_sip(sip_monthly, sip_r, y, sip_step_up)
            inv_std.append(s_std["total_invested"])
            val_std.append(s_std["future_value"])
            val_step.append(s_step["future_value"])
            val_real.append(s_step["future_value"] * math.pow(1.0 + sip_inf, -y))

        fig_wealth = go.Figure()
        fig_wealth.add_trace(go.Scatter(x=years_arr, y=val_step, mode='lines', name=f'Step-Up SIP ({sip_step_up_pct:.0f}%/yr)', line=dict(color='#10B981', width=3)))
        fig_wealth.add_trace(go.Scatter(x=years_arr, y=val_std, mode='lines', name='Standard Fixed SIP', line=dict(color='#38BDF8', width=2.5)))
        fig_wealth.add_trace(go.Scatter(x=years_arr, y=val_real, mode='lines', name='Real Purchasing Power (Step-Up)', line=dict(color='#F59E0B', width=2, dash='dash')))
        fig_wealth.add_trace(go.Scatter(x=years_arr, y=inv_std, mode='lines', name='Capital Outlay (Standard)', line=dict(color='#64748B', width=1.5, dash='dot')))

        fig_wealth.update_layout(
            title="Corpus Accumulation: Nominal vs. Inflation-Eroded Purchasing Power",
            xaxis_title="Investment Horizon (Years)",
            yaxis_title=f"Wealth Valuation ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            hovermode="x unified",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_wealth, use_container_width=True)

    # Purchasing Power Decay Visualization
    st.markdown("#### 📉 Currency Purchasing Power Decay ($P(t) = P_0 (1 + i)^{-t}$)")
    decay_years = np.arange(0, 31, 1)
    base_100k = 100000.0
    decay_curve = [purchasing_power_erosion(base_100k, sip_inf, float(yr)) for yr in decay_years]
    
    fig_decay = go.Figure()
    fig_decay.add_trace(go.Scatter(
        x=decay_years,
        y=decay_curve,
        mode='lines+markers',
        name='Purchasing Power',
        line=dict(color='#F43F5E', width=3),
        marker=dict(size=5)
    ))
    fig_decay.add_hline(y=50000.0, line_dash="dash", line_color="#F59E0B", annotation_text=f"Half-Life: {half_life:.1f} Yrs (50% Decay)", annotation_position="top right")
    fig_decay.update_layout(
        title=f"Erosion of {format_curr(base_100k, curr_sym)} Real Purchasing Power at {sip_inf_pct:.1f}% Inflation",
        xaxis_title="Years into the Future",
        yaxis_title=f"Equivalent Purchasing Value ({curr_sym})",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(14, 27, 49, 0.4)",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_decay, use_container_width=True)


# ==============================================================================
# TAB 4: CAPITAL BUDGETING & NEWTON-RAPHSON IRR SOLVER
# ==============================================================================
with tab4:
    st.markdown("### 📊 Capital Budgeting, Analytical NPV & Newton–Raphson IRR Solver")
    st.markdown(
        "By Galois Theory and the **Abel–Ruffini Theorem**, general polynomial root equations of degree $T \\ge 5$ "
        "have **no algebraic radical solution**. Calculating the Internal Rate of Return (IRR) mathematically mandates "
        "numerical analysis. This module implements quadratic-convergent Newton–Raphson with exact analytical derivatives."
    )
    
    col_c1, col_c2 = st.columns([1, 2])
    
    with col_c1:
        st.markdown('<div class="fdss-card">', unsafe_allow_html=True)
        st.markdown("#### Project Cash Flow Profile")
        
        cf_preset = st.selectbox(
            "Project Archetype Preset",
            options=["High-Yield Tech Venture", "Renewable Infrastructure", "Industrial Plant", "Custom"],
            index=0
        )
        
        if cf_preset == "High-Yield Tech Venture":
            default_cfs = "-500000, 100000, 180000, 240000, 320000, 400000"
        elif cf_preset == "Renewable Infrastructure":
            default_cfs = "-1000000, 150000, 180000, 220000, 250000, 280000, 310000, 350000"
        elif cf_preset == "Industrial Plant":
            default_cfs = "-2500000, 400000, 600000, 800000, 1000000, 1200000"
        else:
            default_cfs = "-100000, 30000, 40000, 50000, 60000"
            
        cfs_input_str = st.text_input("Cash Flows $C_0, C_1, \\dots, C_T$ (comma separated)", value=default_cfs)
        try:
            cash_flows = [float(x.strip()) for x in cfs_input_str.split(",")]
        except Exception:
            cash_flows = [-100000.0, 30000.0, 40000.0, 50000.0, 60000.0]
            
        hurdle_rate_pct = st.slider("Hurdle Rate / Cost of Capital ($r_h$ %)", min_value=1.0, max_value=30.0, value=12.0, step=0.5, key="cb_hurdle")
        hurdle_rate = hurdle_rate_pct / 100.0
        initial_guess_pct = st.slider("Newton Initial Guess ($r_0$ %)", min_value=-10.0, max_value=50.0, value=10.0, step=1.0, key="cb_guess")
        initial_guess = initial_guess_pct / 100.0
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.latex(r"\text{NPV}(r) = \sum_{t=0}^T \frac{C_t}{(1 + r)^t} = 0")
        st.latex(r"r_{k+1} = r_k - \frac{\text{NPV}(r_k)}{\text{NPV}'(r_k)}")
        st.latex(r"\text{NPV}'(r) = -\sum_{t=1}^T \frac{t \cdot C_t}{(1 + r)^{t+1}}")

    # Run solver
    try:
        project_npv = net_present_value(hurdle_rate, cash_flows)
        project_irr, irr_history = internal_rate_of_return_with_history(cash_flows, initial_guess=initial_guess)
        payback = discounted_payback_period(hurdle_rate, cash_flows)
        # Profitability Index
        initial_outflow = abs(cash_flows[0]) if cash_flows[0] < 0 else 1.0
        pv_inflows = sum(cf / math.pow(1.0 + hurdle_rate, t) for t, cf in enumerate(cash_flows) if t > 0)
        pi = pv_inflows / initial_outflow
    except Exception as e:
        st.error(f"Computation error: {e}")
        project_npv, project_irr, irr_history, payback, pi = 0.0, 0.0, [], None, 1.0

    with col_c2:
        kc1, kc2, kc3, kc4 = st.columns(4)
        with kc1:
            npv_badge = "badge-emerald" if project_npv >= 0 else "badge-rose"
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge {npv_badge}">Net Present Value</span>
                    <div class="kpi-title">NPV @ {hurdle_rate_pct:.1f}%</div>
                    <div class="kpi-value">{format_curr(project_npv, curr_sym)}</div>
                    <div class="kpi-subtext">{'Value Accretive' if project_npv>=0 else 'Destroys Value'}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kc2:
            irr_badge = "badge-emerald" if project_irr >= hurdle_rate else "badge-rose"
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge {irr_badge}">Internal Rate of Return</span>
                    <div class="kpi-title">Exact Root $r^*$</div>
                    <div class="kpi-value">{format_pct(project_irr)}</div>
                    <div class="kpi-subtext">Spread: {(project_irr - hurdle_rate)*100:+.2f}% vs Hurdle</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kc3:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-cyan">Discounted Payback</span>
                    <div class="kpi-title">Capital Breakeven</div>
                    <div class="kpi-value">{f"{payback:.2f} Yrs" if payback else "Never"}</div>
                    <div class="kpi-subtext">Fractionally interpolated</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kc4:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-purple">Profitability Index</span>
                    <div class="kpi-title">Benefit / Cost Ratio</div>
                    <div class="kpi-value">{pi:.2f}</div>
                    <div class="kpi-subtext">{'PI > 1.0 (Accept)' if pi > 1 else 'PI < 1.0 (Reject)'}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Plotly Continuous NPV Profile Curve
        r_scan = np.linspace(-0.15, max(0.50, project_irr * 1.5), 250)
        npv_curve = [net_present_value(float(r), cash_flows) for r in r_scan]

        fig_npv = go.Figure()
        fig_npv.add_trace(go.Scatter(x=r_scan * 100, y=npv_curve, mode='lines', name='NPV Profile f(r)', line=dict(color='#38BDF8', width=3)))
        fig_npv.add_hline(y=0.0, line_dash="solid", line_color="#64748B", line_width=1)
        # Highlight Hurdle Rate
        fig_npv.add_trace(go.Scatter(
            x=[hurdle_rate_pct],
            y=[project_npv],
            mode='markers+text',
            marker=dict(color='#F59E0B', size=11),
            text=["Hurdle Rate"],
            textposition="top right",
            name="Hurdle Rate NPV"
        ))
        # Highlight IRR Root
        fig_npv.add_trace(go.Scatter(
            x=[project_irr * 100],
            y=[0.0],
            mode='markers+text',
            marker=dict(color='#10B981', size=13, symbol='star'),
            text=[f"IRR: {project_irr*100:.2f}%"],
            textposition="bottom right",
            name="IRR Root Crossing"
        ))

        fig_npv.update_layout(
            title="Net Present Value Profile Curve f(r) & Root Crossing",
            xaxis_title="Discount Rate r (%)",
            yaxis_title=f"Net Present Value ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            hovermode="x unified",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_npv, use_container_width=True)

    # Newton-Raphson Iteration History Table
    st.markdown("#### 🔬 Newton–Raphson Quadratic Convergence Trace")
    if irr_history:
        df_history = pd.DataFrame(irr_history)
        df_history["r_k (%)"] = (df_history["r_k"] * 100).round(4)
        df_history["npv_k"] = df_history["npv_k"].round(2)
        df_history["deriv_k"] = df_history["deriv_k"].round(2)
        if "delta_r" in df_history.columns:
            df_history["delta_r (%)"] = (df_history["delta_r"] * 100).round(4)
            
        st.dataframe(
            df_history[["iteration", "r_k (%)", "npv_k", "deriv_k", "delta_r (%)", "method"]],
            use_container_width=True,
        )


# ==============================================================================
# TAB 5: MONTE CARLO STOCHASTIC RISK LAB
# ==============================================================================
with tab5:
    st.markdown("### 🎲 Monte Carlo Stochastic Risk Lab & Itô Calculus")
    st.markdown(
        "Real-world financial asset prices are non-deterministic and driven by stochastic differential equations: "
        "$dS_t = \\mu S_t dt + \\sigma S_t dW_t$. By **Itô's Lemma**, volatility induces an analytical drag: "
        "$\\Delta \\mu = -\\frac{1}{2}\\sigma^2$. This vectorized simulator models thousands of geometric Brownian motion "
        "paths to quantify empirical Value at Risk (VaR) and goal attainment probability."
    )
    
    col_m1, col_m2 = st.columns([1, 2])
    
    with col_m1:
        st.markdown('<div class="fdss-card">', unsafe_allow_html=True)
        st.markdown("#### Stochastic Parameters")
        mc_s0 = st.number_input("Initial Wealth ($S_0$)", min_value=10000.0, max_value=10000000.0, value=500000.0, step=50000.0, key="mc_s0")
        mc_mu_pct = st.slider("Expected Annual Drift ($\\mu$ %)", min_value=-10.0, max_value=30.0, value=12.0, step=0.5, key="mc_mu")
        mc_mu = mc_mu_pct / 100.0
        mc_sigma_pct = st.slider("Annual Volatility ($\\sigma$ %)", min_value=1.0, max_value=60.0, value=18.0, step=0.5, key="mc_sigma")
        mc_sigma = mc_sigma_pct / 100.0
        mc_years = st.slider("Simulation Horizon ($T$ in Years)", min_value=1, max_value=30, value=10, step=1, key="mc_t")
        mc_paths = st.select_slider("Number of Trajectories ($M$)", options=[250, 500, 1000, 2500, 5000], value=1000, key="mc_m")
        mc_target = st.number_input("Target Wealth Goal ($G$)", min_value=100000.0, max_value=50000000.0, value=1500000.0, step=100000.0, key="mc_target")
        mc_seed = st.number_input("Random Seed (for reproducibility)", min_value=1, max_value=999999, value=42, step=1, key="mc_seed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.latex(r"dS_t = \mu S_t dt + \sigma S_t dW_t")
        st.latex(r"S_T = S_0 \exp\left[ \left(\mu - \frac{1}{2}\sigma^2\right)T + \sigma \sqrt{T} Z \right]")
        st.latex(r"\Delta \mu = -\frac{1}{2}\sigma^2 \quad \text{(Volatility Drag)}")

    # Vectorized Simulation Execution
    with st.spinner("Generating stochastic trajectories..."):
        time_grid, paths_matrix = simulate_gbm_paths(
            initial_price=mc_s0,
            annual_drift=mc_mu,
            annual_volatility=mc_sigma,
            time_horizon_years=float(mc_years),
            num_steps_per_year=12,
            num_simulations=mc_paths,
            random_seed=int(mc_seed)
        )
        
        terminal_prices = paths_matrix[-1, :]
        sim_stats = compute_simulation_statistics(terminal_prices)
        vol_drag = calculate_volatility_drag(mc_sigma)
        goal_prob = goal_attainment_probability(terminal_prices, mc_target)
        var_95, cvar_95 = calculate_value_at_risk(terminal_prices, confidence_level=0.95)

    with col_m2:
        km1, km2, km3, km4 = st.columns(4)
        with km1:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-emerald">Expected Mean</span>
                    <div class="kpi-title">Average Terminal Wealth</div>
                    <div class="kpi-value">{format_curr(sim_stats['mean'], curr_sym)}</div>
                    <div class="kpi-subtext">Median: {format_curr(sim_stats['median'], curr_sym)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with km2:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-rose">Volatility Drag</span>
                    <div class="kpi-title">Geometric Penalty</div>
                    <div class="kpi-value">-{vol_drag*100:.2f}%</div>
                    <div class="kpi-subtext">Compounding loss -½ σ²</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with km3:
            goal_badge = "badge-emerald" if goal_prob >= 0.70 else ("badge-amber" if goal_prob >= 0.40 else "badge-rose")
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge {goal_badge}">Goal Probability</span>
                    <div class="kpi-title">P(Wealth $\\ge$ Goal)</div>
                    <div class="kpi-value">{format_pct(goal_prob)}</div>
                    <div class="kpi-subtext">Target: {format_curr(mc_target, curr_sym)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with km4:
            st.markdown(
                f"""
                <div class="fdss-card">
                    <span class="metric-badge badge-purple">95% Value at Risk</span>
                    <div class="kpi-title">5th Percentile Floor</div>
                    <div class="kpi-value">{format_curr(var_95, curr_sym)}</div>
                    <div class="kpi-subtext">CVaR: {format_curr(cvar_95, curr_sym)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Plot 1: Vectorized Fan Chart of Stochastic Paths
        fig_fan = go.Figure()
        # Plot up to 75 translucent sample paths
        sample_subset = min(75, mc_paths)
        for i in range(sample_subset):
            fig_fan.add_trace(go.Scatter(
                x=time_grid,
                y=paths_matrix[:, i],
                mode='lines',
                line=dict(color='rgba(56, 189, 248, 0.12)', width=1),
                hoverinfo='skip',
                showlegend=False
            ))
            
        # Overlay Mean, Median, and 95% Confidence Bounds
        mean_path = np.mean(paths_matrix, axis=1)
        median_path = np.median(paths_matrix, axis=1)
        p05_path = np.percentile(paths_matrix, 5, axis=1)
        p95_path = np.percentile(paths_matrix, 95, axis=1)

        fig_fan.add_trace(go.Scatter(x=time_grid, y=mean_path, mode='lines', name='Expected Mean E[S_t]', line=dict(color='#10B981', width=3)))
        fig_fan.add_trace(go.Scatter(x=time_grid, y=median_path, mode='lines', name='Median Path (50th %)', line=dict(color='#38BDF8', width=2.5)))
        fig_fan.add_trace(go.Scatter(x=time_grid, y=p05_path, mode='lines', name='5th Percentile (95% VaR Floor)', line=dict(color='#F43F5E', width=2, dash='dash')))
        fig_fan.add_trace(go.Scatter(x=time_grid, y=p95_path, mode='lines', name='95th Percentile Upper Bound', line=dict(color='#818CF8', width=2, dash='dot')))
        fig_fan.add_hline(y=mc_target, line_dash="solid", line_color="#F59E0B", annotation_text=f"Target Goal: {format_curr(mc_target, curr_sym)}", annotation_position="top left")

        fig_fan.update_layout(
            title=f"Geometric Brownian Motion: {mc_paths:,} Vectorized Trajectories ($T={mc_years}$ Yrs)",
            xaxis_title="Time (Years)",
            yaxis_title=f"Portfolio Valuation ({curr_sym})",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(14, 27, 49, 0.4)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_fan, use_container_width=True)

    # Terminal Wealth Probability Distribution (Histogram + KDE)
    st.markdown("#### 📊 Terminal Wealth Distribution & Downside Risk Profile")
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=terminal_prices,
        nbinsx=60,
        marker=dict(color='rgba(56, 189, 248, 0.75)', line=dict(color='#38BDF8', width=1)),
        name="Terminal Wealth Frequency",
    ))
    fig_hist.add_vline(x=var_95, line_dash="dash", line_color="#F43F5E", line_width=2.5, annotation_text=f"95% VaR Cutoff: {format_curr(var_95, curr_sym)}", annotation_position="top left")
    fig_hist.add_vline(x=mc_target, line_dash="dash", line_color="#F59E0B", line_width=2.5, annotation_text=f"Target Goal: {format_curr(mc_target, curr_sym)}", annotation_position="top right")
    fig_hist.add_vline(x=sim_stats['median'], line_dash="dot", line_color="#10B981", line_width=2, annotation_text=f"Median: {format_curr(sim_stats['median'], curr_sym)}", annotation_position="bottom right")

    fig_hist.update_layout(
        title="Terminal Wealth Frequency Distribution at Horizon T",
        xaxis_title=f"Terminal Portfolio Value ({curr_sym})",
        yaxis_title="Path Count",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(14, 27, 49, 0.4)",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_hist, use_container_width=True)


# ==============================================================================
# 4. FOOTER & CITATIONS
# ==============================================================================

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #94A3B8; font-size: 0.85rem; padding: 1.5rem 0;">
        <strong>Financial Decision Support System (FDSS)</strong> • Pure Sciences Category 3 Research Project<br>
        Developed by Atharv Ranade, Danish Shaikh, Abhijeet • Built with Streamlit, Plotly & NumPy Vectorization<br>
        <span style="color: #38BDF8;">All analytical proofs benchmarked against closed-form mathematical equations and IEEE 754 precision standards.</span>
    </div>
    """,
    unsafe_allow_html=True,
)
