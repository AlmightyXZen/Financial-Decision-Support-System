"""
ui/tab_capital_budgeting.py
Module 4: Capital Budgeting, Multi-Period NPV, Newton-Raphson IRR & Sensitivity Analysis.
Author: Atharv Ranade
"""

import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from models.capital_budgeting import (
    net_present_value,
    internal_rate_of_return_with_history,
    discounted_payback_period,
)
from ui.styles import render_stat_card, render_chart_header, format_currency, format_percentage, plotly_base_layout


def render_tab_capital_budgeting(curr_sym: str):
    """Renders the Capital Budgeting & IRR module."""
    
    # Preset quick-fill triggers across full container width
    b_cols = st.columns(3)
    c1_str = format_currency(500000.0, curr_sym)
    c2_str = format_currency(2000000.0, curr_sym)
    c3_str = format_currency(1500000.0, curr_sym)
    if b_cols[0].button(f"Enterprise SaaS ({c1_str} Outlay)", use_container_width=True):
        st.session_state["cb_flow"] = "-500000, 100000, 180000, 240000, 320000, 420000"
    if b_cols[1].button(f"Manufacturing Plant ({c2_str} Outlay)", use_container_width=True):
        st.session_state["cb_flow"] = "-2000000, 350000, 500000, 650000, 800000, 950000"
    if b_cols[2].button(f"Infrastructure Project ({c3_str} Outlay)", use_container_width=True):
        st.session_state["cb_flow"] = "-1500000, 200000, 250000, 300000, 350000, 400000, 450000"

    flow_default = st.session_state.get("cb_flow", "-500000, 100000, 180000, 240000, 320000, 420000")

    col1, col2 = st.columns([1, 2.2], gap="large")

    with col1:
        st.markdown("##### Project Financial Profile")
        cfs_text = st.text_input("Cash Flows [C₀, C₁, ..., C_T]", value=flow_default, key="cb_cfs_in")
        try:
            base_flows = [float(x.strip()) for x in cfs_text.split(",")]
        except Exception:
            base_flows = [-500000.0, 100000.0, 180000.0, 240000.0, 320000.0, 420000.0]

        hurdle_pct = st.slider("Hurdle Rate / Cost of Capital (%)", min_value=1.0, max_value=30.0, value=12.0, step=0.5, key="cb_hurdle_in")
        hurdle_rate = hurdle_pct / 100.0

        scenario = st.radio(
            "Scenario Stress Test",
            options=["Base Case (100%)", "Conservative (-20% Inflows)", "Optimistic (+25% Inflows)"],
            index=0,
            horizontal=True
        )

        if "Conservative" in scenario:
            active_flows = [base_flows[0]] + [cf * 0.80 for cf in base_flows[1:]]
        elif "Optimistic" in scenario:
            active_flows = [base_flows[0]] + [cf * 1.25 for cf in base_flows[1:]]
        else:
            active_flows = list(base_flows)

    # Computations
    try:
        npv_res = net_present_value(hurdle_rate, active_flows)
        irr_res, irr_trace = internal_rate_of_return_with_history(active_flows, initial_guess=0.10)
        payback_res = discounted_payback_period(hurdle_rate, active_flows)
        c0 = abs(active_flows[0]) if active_flows[0] < 0 else 1.0
        pv_inflows = sum(cf / math.pow(1.0 + hurdle_rate, t) for t, cf in enumerate(active_flows) if t > 0)
        pi_res = pv_inflows / c0
    except Exception:
        npv_res, irr_res, irr_trace, payback_res, pi_res = 0.0, 0.0, [], None, 1.0

    with col2:
        # High-Density 2x2 Responsive Metric Grid
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1:
            npv_color = "#10B981" if npv_res >= 0 else "#F43F5E"
            render_stat_card(
                label="Net Present Value (NPV)",
                value=format_currency(npv_res, curr_sym),
                subtext="Value Accretive" if npv_res >= 0 else "Destroys Value",
                delta=f"@ {hurdle_pct:.1f}% Hurdle",
                delta_type="green" if npv_res >= 0 else "red",
                value_color=npv_color
            )
        with r1_c2:
            irr_color = "#10B981" if irr_res >= hurdle_rate else "#F43F5E"
            render_stat_card(
                label="Internal Rate of Return (IRR)",
                value=format_percentage(irr_res),
                subtext=f"Spread: {(irr_res - hurdle_rate)*100:+.2f}% vs Hurdle",
                delta="Profitable" if irr_res >= hurdle_rate else "Below Hurdle",
                delta_type="green" if irr_res >= hurdle_rate else "red",
                value_color=irr_color
            )

        r2_c1, r2_c2 = st.columns(2)
        with r2_c1:
            render_stat_card(
                label="Discounted Payback",
                value=f"{payback_res:.2f} Yrs" if payback_res else "Never",
                subtext="Capital Breakeven Period",
                delta=None
            )
        with r2_c2:
            render_stat_card(
                label="Profitability Index (PI)",
                value=f"{pi_res:.2f}x",
                subtext="Accept Project" if pi_res >= 1.0 else "Reject Project",
                delta="PI ≥ 1.0 Accretive" if pi_res >= 1.0 else "PI < 1.0 Dilutive",
                delta_type="green" if pi_res >= 1.0 else "red",
                value_color="#38BDF8"
            )

        # Plot 1: NPV Profile Curve
        r_grid = np.linspace(-0.15, max(0.50, irr_res * 1.5), 200)
        npv_curve = [net_present_value(float(r), active_flows) for r in r_grid]

        fig_npv = go.Figure()
        fig_npv.add_trace(go.Scatter(x=r_grid * 100, y=npv_curve, mode="lines", name="NPV Profile <i>f</i>(<i>r</i>)", line=dict(color="#38BDF8", width=2.5)))
        fig_npv.add_hline(y=0.0, line_dash="solid", line_color="#64748B", line_width=1)
        fig_npv.add_trace(go.Scatter(x=[hurdle_pct], y=[npv_res], mode="markers+text", marker=dict(color="#F59E0B", size=10), text=["Hurdle"], textposition="top right", name="Hurdle Rate"))
        fig_npv.add_trace(go.Scatter(x=[irr_res * 100], y=[0.0], mode="markers+text", marker=dict(color="#10B981", size=12, symbol="star"), text=[f"IRR: {irr_res*100:.2f}%"], textposition="bottom right", name="IRR Root"))

        render_chart_header(
            "Net Present Value Profile Curve & Zero-Crossing Root",
            "Continuous yield function <i>f</i>(<i>r</i>) plotted against cost of capital and Newton–Raphson IRR root"
        )
        layout = plotly_base_layout(
            xaxis_title="Discount Rate (%)",
            yaxis_title=f"Net Present Value ({curr_sym})",
            height=360,
            show_legend=True
        )
        fig_npv.update_layout(**layout)
        st.plotly_chart(fig_npv, use_container_width=True)

    # Sensitivity Heatmap Matrix (NPV vs Discount Rate & Capex Shift)
    with st.expander("2D Sensitivity Matrix: Hurdle Rate vs. Initial Capital Outlay"):
        rates_test = [0.08, 0.10, 0.12, 0.14, 0.16, 0.18]
        capex_multipliers = [0.80, 0.90, 1.00, 1.10, 1.20]
        
        matrix_data = []
        for c_mult in capex_multipliers:
            row = []
            for r in rates_test:
                shifted_flows = [active_flows[0] * c_mult] + active_flows[1:]
                val = net_present_value(r, shifted_flows)
                row.append(val)
            matrix_data.append(row)

        fig_heat = go.Figure(data=go.Heatmap(
            z=matrix_data,
            x=[f"{r*100:.0f}%" for r in rates_test],
            y=[f"{int(m*100)}% ({format_currency(active_flows[0]*m, curr_sym)})" for m in capex_multipliers],
            colorscale="RdYlGn",
            text=[[format_currency(v, curr_sym) for v in row] for row in matrix_data],
            texttemplate="%{text}",
            textfont={"size": 11},
        ))
        render_chart_header(
            "2D NPV Sensitivity Matrix",
            "Simultaneous evaluation across discount rate shifts and initial capital outlay variance"
        )
        heat_layout = plotly_base_layout(
            xaxis_title="Cost of Capital (Discount Rate)",
            yaxis_title="Initial Outlay Scale",
            height=300,
            show_legend=False
        )
        fig_heat.update_layout(**heat_layout)
        st.plotly_chart(fig_heat, use_container_width=True)

        if irr_trace:
            st.markdown("##### Newton–Raphson Numerical Trajectory")
            trace_df = pd.DataFrame(irr_trace)
            trace_df["r_k (%)"] = (trace_df["r_k"] * 100).round(4)
            trace_df["npv_k"] = trace_df["npv_k"].round(2)
            st.dataframe(trace_df[["iteration", "r_k (%)", "npv_k", "method"]], use_container_width=True)

    # In-Tab Methodology & Interpretation Notes
    with st.expander("Module Methodology & Mathematical Notes: Multi-Period NPV & Newton–Raphson"):
        st.markdown(
            """
            - **Net Present Value (NPV):** Evaluates absolute enterprise wealth creation: $\\text{NPV}(r) = \\sum_{t=0}^T \\frac{C_t}{(1 + r)^t}$. If $\\text{NPV} \\ge 0$, the project generates returns exceeding the hurdle rate cost of capital.
            - **Newton–Raphson Root-Finding:** For multi-period projects ($T \\ge 5$), the Abel–Ruffini theorem precludes closed-form algebraic solutions. FDSS solves $\\text{NPV}(r^*) = 0$ numerically via Newton–Raphson updates $r_{k+1} = r_k - \\frac{f(r_k)}{f'(r_k)}$, utilizing the exact analytical derivative $f'(r) = -\\sum_{t=1}^T \\frac{t \\cdot C_t}{(1 + r)^{t+1}}$ with quadratic convergence.
            - **Descartes' Rule of Signs & The Multiple IRR Hazard:** When cash flows alternate signs more than once (e.g. initial capex $<0$, positive operational inflows $>0$, followed by plant decommissioning costs $<0$), the polynomial can yield multiple real roots or none at all. In non-conventional cash flow profiles, Net Present Value (NPV) remains the mathematically decisive criterion.
            """
        )
