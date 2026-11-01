"""
ui/tab_time_value.py
Module 1: Deterministic Time Value of Money & Asymptotic Yield Curvature.
Author: Atharv Ranade
"""

import math
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from models.time_value import (
    simple_interest_amount,
    compound_interest_amount,
    continuous_compounding_amount,
    nominal_to_effective_rate,
)
from ui.styles import (
    render_stat_card,
    render_chart_header,
    format_currency,
    format_percentage,
    plotly_base_layout,
    render_doubling_callout,
)


def render_tab_time_value(curr_sym: str):
    """Renders the Time Value & Yields module."""
    
    # Preset quick-fill triggers across full container width
    p_cols = st.columns(4)
    if p_cols[0].button("🏛️ Sovereign Bond (7.1%)", use_container_width=True):
        st.session_state["tvm_r_val"] = 7.1
    if p_cols[1].button("🏦 Fixed Deposit (8.5%)", use_container_width=True):
        st.session_state["tvm_r_val"] = 8.5
    if p_cols[2].button("📈 Corporate Debt (11.5%)", use_container_width=True):
        st.session_state["tvm_r_val"] = 11.5
    if p_cols[3].button("🚀 Venture Note (18.0%)", use_container_width=True):
        st.session_state["tvm_r_val"] = 18.0

    default_r = st.session_state.get("tvm_r_val", 10.0)

    col1, col2 = st.columns([1, 2.2], gap="large")

    with col1:
        st.markdown("##### Capital & Horizon Inputs")
        p_val = st.number_input("Principal Capital ($P$)", min_value=1000.0, max_value=50000000.0, value=100000.0, step=10000.0, key="tvm_p_input")
        r_pct = st.slider("Nominal Annual Rate ($r$ %)", min_value=0.5, max_value=30.0, value=float(default_r), step=0.1, key="tvm_r_slider")
        r_val = r_pct / 100.0
        t_val = st.slider("Horizon ($t$ in Years)", min_value=0.5, max_value=40.0, value=10.0, step=0.5, key="tvm_t_slider")

        freq_options = {
            "Annual (m=1)": 1,
            "Semi-Annual (m=2)": 2,
            "Quarterly (m=4)": 4,
            "Monthly (m=12)": 12,
            "Daily (m=365)": 365,
        }
        freq_label = st.selectbox("Compounding Frequency ($m$)", options=list(freq_options.keys()), index=3, key="tvm_freq_select")
        m_val = freq_options[freq_label]

        # Exact Doubling Time vs Rule of 72
        exact_double_yrs = math.log(2.0) / r_val if r_val > 0 else float("inf")
        rule_72_yrs = 72.0 / r_pct if r_pct > 0 else float("inf")
        st.markdown("---")
        render_doubling_callout(exact_double_yrs, rule_72_yrs)

    # Core Calculations
    a_simple = simple_interest_amount(p_val, r_val, t_val)
    a_compound = compound_interest_amount(p_val, r_val, t_val, compounding_frequency=m_val)
    a_cont = continuous_compounding_amount(p_val, r_val, t_val)
    ear = nominal_to_effective_rate(r_val, compounding_frequency=m_val)
    comp_bonus = a_compound - a_simple
    euler_gap = a_cont - a_compound

    with col2:
        # High-Density 2x2 Responsive Metric Grid
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1:
            render_stat_card(
                label="Simple Interest",
                value=format_currency(a_simple, curr_sym),
                subtext="Linear Baseline",
                delta="Linear Baseline",
                delta_type="amber"
            )
        with r1_c2:
            render_stat_card(
                label="Discrete Compound",
                value=format_currency(a_compound, curr_sym),
                subtext=f"+{format_currency(comp_bonus, curr_sym)} vs Simple",
                delta=f"+{(comp_bonus/p_val)*100:.1f}% Yield",
                delta_type="blue"
            )

        r2_c1, r2_c2 = st.columns(2)
        with r2_c1:
            render_stat_card(
                label="Continuous Limit",
                value=format_currency(a_cont, curr_sym),
                subtext="Theoretical Euler Ceiling",
                delta="Euler Ceiling",
                delta_type="green",
                value_color="#10B981"
            )
        with r2_c2:
            render_stat_card(
                label="Effective APY (EAR)",
                value=format_percentage(ear),
                subtext=f"Nominal: {r_pct:.1f}%",
                delta=f"+{(ear - r_val)*100:.2f}% Comp Bonus",
                delta_type="blue"
            )

        # Plot 1: Capital Trajectory Curves
        t_arr = np.linspace(0, t_val, 150)
        y_simple = [simple_interest_amount(p_val, r_val, float(s)) for s in t_arr]
        y_comp = [compound_interest_amount(p_val, r_val, float(s), compounding_frequency=m_val) for s in t_arr]
        y_cont = [continuous_compounding_amount(p_val, r_val, float(s)) for s in t_arr]

        fig_tvm = go.Figure()
        fig_tvm.add_trace(go.Scatter(x=t_arr, y=y_simple, mode="lines", name="Simple Interest", line=dict(color="#F59E0B", width=2)))
        fig_tvm.add_trace(go.Scatter(x=t_arr, y=y_comp, mode="lines", name=f"Discrete ({freq_label.split()[0]})", line=dict(color="#38BDF8", width=3)))
        fig_tvm.add_trace(go.Scatter(x=t_arr, y=y_cont, mode="lines", name="Continuous Limit (P·e<sup>rt</sup>)", line=dict(color="#10B981", width=2, dash="dot")))

        render_chart_header(
            "Capital Growth Trajectory",
            "Linear Subadditivity (Simple) vs. Exponential Expansion (Discrete) vs. Continuous (Euler Limit)"
        )
        layout = plotly_base_layout(
            xaxis_title="Investment Horizon (Years)",
            yaxis_title=f"Terminal Portfolio Value ({curr_sym})",
            height=380,
            show_legend=True
        )
        fig_tvm.update_layout(**layout)
        st.plotly_chart(fig_tvm, use_container_width=True)

        # Plot 2: Compounding Frequency Monotonicity
        render_chart_header(
            "Frequency Asymptote: Convergence to Euler's Ceiling",
            "Terminal wealth across compounding frequencies approaching the continuous ODE ceiling <i>P</i> &middot; <i>e</i><sup><i>rt</i></sup>"
        )
        freq_keys = [1, 2, 4, 12, 52, 365, 1000]
        freq_names = ["Annual (1)", "Semi (2)", "Quarterly (4)", "Monthly (12)", "Weekly (52)", "Daily (365)", "Ultra (1000)"]
        freq_wealths = [compound_interest_amount(p_val, r_val, t_val, compounding_frequency=f) for f in freq_keys]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=freq_names,
            y=freq_wealths,
            text=[format_currency(v, curr_sym) for v in freq_wealths],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=11, color="#FFFFFF", family="JetBrains Mono, monospace"),
            marker=dict(color=freq_wealths, colorscale="Tealgrn"),
            name="Terminal Wealth"
        ))
        fig_bar.add_hline(
            y=a_cont,
            line_dash="dash",
            line_color="#F43F5E",
            annotation_text=f"Euler Ceiling: {format_currency(a_cont, curr_sym)}",
            annotation_position="top left",
            annotation_font=dict(size=11, color="#F43F5E")
        )
        bar_layout = plotly_base_layout(
            xaxis_title="Compounding Regimes",
            yaxis_title=f"Terminal Wealth ({curr_sym})",
            height=280,
            show_legend=False
        )
        bar_layout["yaxis"]["range"] = [0, a_cont * 1.15]
        fig_bar.update_layout(**bar_layout)
        st.plotly_chart(fig_bar, use_container_width=True)
