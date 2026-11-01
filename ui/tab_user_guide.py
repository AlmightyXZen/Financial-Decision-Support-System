"""
ui/tab_user_guide.py
Module 6: Comprehensive User Guide, System Documentation & Mathematical Specifications.
Author: Atharv Ranade
"""

import streamlit as st
from ui.styles import render_chart_header, format_fraction


def render_tab_user_guide(curr_sym: str):
    """Renders the comprehensive User Guide & Documentation tab."""

    st.markdown(
        """
        <div style="background: rgba(14, 27, 49, 0.7); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.5rem 1.8rem; margin-bottom: 2rem;">
            <div style="margin-bottom: 0.5rem;">
                <h3 style="margin: 0; color: #FFFFFF; font-weight: 800; font-size: 1.4rem;">FDSS System Manual & User Guide</h3>
                <div style="color: #94A3B8; font-size: 0.88rem; margin-top: 0.2rem;">First-Principles Calculus, Numerical Root-Finding & Itô Stochastic Simulation</div>
            </div>
            <p style="color: #CBD5E1; font-size: 0.92rem; line-height: 1.6; margin-top: 0.8rem; margin-bottom: 0;">
                The <b>Financial Decision Support System (FDSS)</b> is an open-source quantitative finance engine 
                authored by <b>Atharv Ranade</b> (BSc Mathematics & Statistics, University of Mumbai). 
                Unlike conventional consumer financial tools that rely on opaque black-box APIs, every model in FDSS is derived 
                directly from first-principles calculus, differential equations, and rigorous probability theory.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Section 1: 3-Step Quick Start
    render_chart_header("Quick-Start Guide", "Three-step operational workflow for quantitative financial analysis")
    
    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        st.markdown(
            """
            <div class="fdss-card" style="min-height: 180px; height: 100%; display: flex; flex-direction: column; justify-content: flex-start;">
                <div class="card-top" style="margin-bottom: 0.5rem;">
                    <span class="card-label">STEP 1</span>
                    <span class="delta-badge delta-blue">WORKSPACE</span>
                </div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.4rem;">Configure Currency & Scale</div>
                <div class="guide-card-text">
                    Open the sidebar to select from <b>15 global currencies</b> (USD, INR, EUR, GBP, JPY, etc.) 
                    and toggle between <b>International (M / B)</b> and <b>Indian Vedic (L / Cr)</b> number systems.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_q2:
        st.markdown(
            """
            <div class="fdss-card" style="min-height: 180px; height: 100%; display: flex; flex-direction: column; justify-content: flex-start;">
                <div class="card-top" style="margin-bottom: 0.5rem;">
                    <span class="card-label">STEP 2</span>
                    <span class="delta-badge delta-green">ENGINES</span>
                </div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.4rem;">Select Engine & Calibrate Inputs</div>
                <div class="guide-card-text">
                    Navigate through the analytical tabs. Click calibrated <b>scenario preset buttons</b> 
                    (e.g. <i>Bull Market</i>, <i>2008 Financial Crisis</i>, <i>Home Mortgage</i>) or fine-tune parameters using interactive sliders.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_q3:
        st.markdown(
            """
            <div class="fdss-card" style="min-height: 180px; height: 100%; display: flex; flex-direction: column; justify-content: flex-start;">
                <div class="card-top" style="margin-bottom: 0.5rem;">
                    <span class="card-label">STEP 3</span>
                    <span class="delta-badge delta-amber">ANALYTICS</span>
                </div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.4rem;">Evaluate Metrics & Export Schedules</div>
                <div class="guide-card-text">
                    Analyze analytical KPI cards, interactive Plotly curvature charts, and 2D sensitivity matrices. 
                    Download complete month-by-month loan amortization schedules in raw CSV.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Section 2: Module-by-Module Operational Guide & Mathematics
    render_chart_header("Module Specifications & Mathematical Foundations", "In-depth functional overview and governing equations for all 5 core engines")

    # Module 1
    with st.expander("Module 1: Time Value of Money & Asymptotic Yield Curvature", expanded=True):
        st.markdown(
            f"""
            #### Overview & Use-Cases
            Analyzes how capital expands across compounding frequencies—ranging from discrete intervals (annual, monthly, daily) 
            to the continuous theoretical Euler limit. Useful for fixed deposit evaluation, bond yield analysis, and capital doubling forecasts.

            #### Governing Mathematical Equations
            1. **Discrete Compounding:**
               $$A(t) = P \\left(1 + \\frac{{r}}{{m}}\\right)^{{mt}}$$
               Where $P$ is principal capital, $r$ is nominal annual interest rate, $m$ is compounding frequency per year, and $t$ is horizon in years.
            
            2. **Continuous Compounding (The Euler Ceiling ODE):**
               As compounding frequency $m \\to \\infty$, terminal wealth converges asymptotically to Euler's ceiling:
               $$\\frac{{dA}}{{dt}} = r A \\implies A(t) = P \\cdot e^{{rt}}$$
               No compounding structure under the same nominal rate $r$ can ever exceed this theoretical limit.

            3. **Capital Doubling Horizon:**
               - **Exact Analytical Solution:** $\\tau_{{\\text{{double}}}} = \\frac{{\\ln(2)}}{{r}}$
               - **Retail Approximation (Rule of 72):** $\\tau \\approx \\frac{{72}}{{r_{{\\%}}}}$

            4. **Effective Annual Rate (EAR / APY):**
               $$\\text{{EAR}} = \\left(1 + \\frac{{r}}{{m}}\\right)^m - 1$$
            """
        )

    # Module 2
    with st.expander("Module 2: Consumer Debt, Amortization Mechanics & Prepayment Acceleration", expanded=False):
        st.markdown(
            f"""
            #### Overview & Use-Cases
            Models structured debt facilities (home mortgages, vehicle loans, personal credit lines). Features a real-time 
            **Negative Amortization Boundary Watch** and calculates the cost reduction of accelerated monthly prepayments.

            #### Governing Mathematical Equations
            1. **Equated Monthly Installment (EMI) Closed Form:**
               Derived from the finite geometric series present value sum of annuity cash flows:
               $$\\text{{EMI}} = P \\cdot \\frac{{r_m (1 + r_m)^n}}{{(1 + r_m)^n - 1}}$$
               Where $r_m = \\frac{{r}}{{12}}$ is monthly interest rate, and $n = t \\times 12$ is total tenure in months.

            2. **Negative Amortization Boundary Watch:**
               Monthly interest accrues at:
               $$\\text{{Accrued Interest}} = \\frac{{P \\cdot r}}{{12}}$$
               If a scheduled payment $C < \\frac{{P \\cdot r}}{{12}}$, the net principal reduction is negative, 
               and the outstanding loan balance **diverges toward infinity**.

            3. **Prepayment Savings:**
               Extra prepayments are subtracted directly from outstanding principal ($P_{{k}} = P_{{k-1}} - \\text{{Prepayment}}$), 
               shortening the amortization tail and collapsing total interest cost.
            """
        )

    # Module 3
    with st.expander("Module 3: Wealth Accumulation, Step-Up SIP & Fisher Inflation", expanded=False):
        st.markdown(
            f"""
            #### Overview & Use-Cases
            Plans systematic investment plans (SIPs), career salary step-up compounding, and tracks FIRE (Financial Independence, 
            Retire Early) corpus milestones discounted for inflation.

            #### Governing Mathematical Equations
            1. **Ordinary Annuity Fixed SIP:**
               $$\\text{{FV}} = \\text{{PMT}} \\cdot \\left[\\frac{{(1 + r_m)^n - 1}}{{r_m}}\\right] (1 + r_m)$$

            2. **Annual Step-Up Escalation:**
               Reflects annual salary increments by escalating monthly contributions by $g\\%$ each year:
               $$C_k = C_0 (1 + g)^{{\\lfloor (k-1)/12 \\rfloor}}$$

            3. **Irving Fisher Inflation Relation:**
               Quantifies real vs. nominal purchasing power erosion:
               $$1 + r_{{\\text{{nominal}}}} = (1 + r_{{\\text{{real}}}})(1 + i) \\implies r_{{\\text{{real}}}} = \\frac{{1 + r_{{\\text{{nominal}}}}}}{{1 + i}} - 1$$

            4. **Purchasing Power Half-Life:**
               The exact time in years for monetary value to degrade by 50% under inflation $i$:
               $$\\tau_{{1/2}} = \\frac{{\\ln(2)}}{{\\ln(1 + i)}}$$
            """
        )

    # Module 4
    with st.expander("Module 4: Capital Budgeting, Multi-Period NPV & Newton–Raphson IRR", expanded=False):
        st.markdown(
            f"""
            #### Overview & Use-Cases
            Evaluates corporate capital expenditure, enterprise investments, and private equity deals. Computes continuous NPV curves, 
            executes high-precision numerical root-finding for IRR, and performs 2D sensitivity analysis.

            #### Governing Mathematical Equations
            1. **Net Present Value (NPV):**
               $$\\text{{NPV}}(r) = \\sum_{{t=0}}^T \\frac{{C_t}}{{(1 + r)^t}}$$
               Where $C_0 < 0$ is initial capital outlay, and $C_t > 0$ are net periodic cash inflows.

            2. **Internal Rate of Return (IRR) via Newton–Raphson Numerical Root-Finding:**
               The IRR is the discount rate $r^*$ where $\\text{{NPV}}(r^*) = 0$. Since polynomial degrees exceed 5, 
               Abel–Ruffini theorem guarantees no general algebraic closed form exists. FDSS deploys **Newton–Raphson iteration**:
               $$r_{{k+1}} = r_k - \\frac{{f(r_k)}}{{f'(r_k)}}$$
               Where the analytical derivative $f'(r)$ is:
               $$f'(r) = \\frac{{d\\text{{NPV}}}}{{dr}} = -\\sum_{{t=1}}^T \\frac{{t \\cdot C_t}}{{(1 + r)^{{t+1}}}}$$
               Achieves quadratic local convergence: $|\\epsilon_{{k+1}}| \\propto |\\epsilon_k|^2$.

            3. **Profitability Index (PI):**
               $$\\text{{PI}} = \\frac{{\\sum_{{t=1}}^T \\frac{{C_t}}{{(1 + r)^t}}}}{{|C_0|}}$$
               An investment is value-accretive when $\\text{{PI}} \\ge 1.0$.
            """
        )

    # Module 5
    with st.expander("Module 5: Vectorized Itô Geometric Brownian Motion & Stochastic Risk Lab", expanded=False):
        st.markdown(
            f"""
            #### Overview & Use-Cases
            Stochastic Monte Carlo simulation for multi-year asset trajectory modeling, fat-tail risk analysis, 
            volatility drag quantification, and goal attainment probability estimation.

            #### Governing Mathematical Equations
            1. **Geometric Brownian Motion Stochastic Differential Equation (SDE):**
               $$dS_t = \\mu S_t dt + \\sigma S_t dW_t$$
               Where $\\mu$ is expected annual drift, $\\sigma$ is annualized volatility, and $W_t$ is a continuous Wiener process.

            2. **Exact Analytical Discrete Trajectory (via Itô's Lemma):**
               Applying Itô's formula to $f(S_t) = \\ln(S_t)$ yields the exact vectorized log-normal stepping generator:
               $$S_{{t+\\Delta t}} = S_t \\cdot \\exp\\left( \\left(\\mu - \\frac{{1}}{{2}}\\sigma^2\\right)\\Delta t + \\sigma \\sqrt{{\\Delta t}} \\, Z \\right), \\quad Z \\sim \\mathcal{{N}}(0, 1)$$

            3. **Volatility Drag Penalty:**
               High volatility systematically erodes compound geometric growth relative to arithmetic average drift:
               $$\\text{{Compound Growth Rate}} = \\mu - \\frac{{1}}{{2}}\\sigma^2$$
               The term $-\\frac{{1}}{{2}}\\sigma^2$ represents the exact continuous volatility drag penalty.

            4. **95% Value at Risk (VaR):**
               The empirical 5th percentile cutoff price $S_{{T, 0.05}}$ such that:
               $$P(S_T \\le S_{{T, 0.05}}) = 0.05$$
            """
        )

    st.markdown("---")

    # Section 3: Financial Decision Matrix
    render_chart_header("Decision Matrix: Problem-to-Module Mapping", "A quick-reference problem-to-solution mapping for common financial decisions")

    decision_data = [
        {"Goal / Decision": "Comparing Bank FDs vs. Corporate Debt Yields", "Recommended Engine": "Time Value & Yields (Tab 1)", "Key Focus Metric": "Effective APY (EAR) & Euler Ceiling"},
        {"Goal / Decision": "Deciding Between Home Mortgage Options", "Recommended Engine": "Debt & Amortization (Tab 2)", "Key Focus Metric": "Monthly EMI & Interest Saved via Prepayment"},
        {"Goal / Decision": "Checking if Custom Loan Payments Cover Interest", "Recommended Engine": "Debt & Amortization (Tab 2)", "Key Focus Metric": "Negative Amortization Divergence Alert"},
        {"Goal / Decision": "Planning Retirement Corpus with Annual Salary Hikes", "Recommended Engine": "Wealth & SIP Planner (Tab 3)", "Key Focus Metric": "Step-Up Corpus vs. Real Purchasing Power"},
        {"Goal / Decision": "Evaluating Commercial Capex or Business Acquisition", "Recommended Engine": "Capital Budgeting & IRR (Tab 4)", "Key Focus Metric": "Net Present Value (NPV) & Newton-Raphson IRR"},
        {"Goal / Decision": "Quantifying Equity Market Drawdown & Worst-Case Risk", "Recommended Engine": "Monte Carlo Risk Lab (Tab 5)", "Key Focus Metric": "95% VaR Floor & Volatility Drag (-½ σ²)"},
    ]
    st.table(decision_data)

    st.markdown("---")

    # Section 4: System Architecture & Verification
    render_chart_header("System Architecture & Verification Integrity", "Mathematical specifications verified via automated test suites")

    v_c1, v_c2 = st.columns(2)
    with v_c1:
        st.markdown(
            """
            <div style="background: rgba(14, 27, 49, 0.65); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 1.2rem; height: 100%;">
                <div style="font-weight: 700; color: #FFFFFF; font-size: 1rem; margin-bottom: 0.6rem;">Automated Verification Suite</div>
                <ul style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.7; padding-left: 1.2rem; margin: 0;">
                    <li><b>38 / 38 Unit Tests Passing:</b> 100% automated coverage across all 5 financial engines.</li>
                    <li><b>Multi-Python CI/CD:</b> GitHub Actions workflow continuously verified on Python 3.10, 3.11, and 3.12.</li>
                    <li><b>Numerical Stability:</b> Explicit boundary guards for zero division, negative amortization, and Newton-Raphson divergence.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    with v_c2:
        st.markdown(
            """
            <div style="background: rgba(14, 27, 49, 0.65); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 1.2rem; height: 100%;">
                <div style="font-weight: 700; color: #FFFFFF; font-size: 1rem; margin-bottom: 0.6rem;">Open Source & Attribution</div>
                <ul style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.7; padding-left: 1.2rem; margin: 0;">
                    <li><b>Author:</b> Atharv Ranade (BSc Mathematics & Statistics, University of Mumbai)</li>
                    <li><b>License:</b> MIT License (Open Source, Free for Academic & Commercial Use)</li>
                    <li><b>Source Code:</b> <a href="https://github.com/AlmightyXZen/Financial-Decision-Support-System" target="_blank" style="color: #38BDF8; text-decoration: none;">GitHub: AlmightyXZen/Financial-Decision-Support-System</a></li>
                    <li><b>Feedback & Issues:</b> <a href="https://github.com/AlmightyXZen/Financial-Decision-Support-System/issues" target="_blank" style="color: #38BDF8; text-decoration: none;">Submit Issue / Feedback</a></li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
