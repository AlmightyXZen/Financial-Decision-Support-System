"""
ui/tab_investments.py
Module 3: Wealth Accumulation, Step-Up SIP, FIRE Milestones & Fisher Inflation.
Author: Atharv Ranade
"""

import math
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from models.investment_plans import (
    calculate_sip_wealth,
    calculate_step_up_sip,
    real_rate_of_return,
    purchasing_power_half_life,
)
from ui.styles import render_stat_card, render_chart_header, format_currency, format_percentage, plotly_base_layout


def render_tab_investments(curr_sym: str):
    """Renders the Wealth Accumulation & SIP Planner module."""
    
    # Preset quick-fill triggers across full container width
    s_cols = st.columns(3)
    if s_cols[0].button("🌱 Conservative (10% Ret, 5% Step)", use_container_width=True):
        st.session_state["sip_r_val"] = 10.0
        st.session_state["sip_step_val"] = 5.0
    if s_cols[1].button("🚀 Growth Equity (13% Ret, 10% Step)", use_container_width=True):
        st.session_state["sip_r_val"] = 13.0
        st.session_state["sip_step_val"] = 10.0
    if s_cols[2].button("🔥 Aggressive FIRE (15% Ret, 15% Step)", use_container_width=True):
        st.session_state["sip_r_val"] = 15.0
        st.session_state["sip_step_val"] = 15.0

    r_default = st.session_state.get("sip_r_val", 12.0)
    step_default = st.session_state.get("sip_step_val", 10.0)

    col1, col2 = st.columns([1, 2.2], gap="large")

    with col1:
        st.markdown("##### Investment Strategy")
        sip_monthly = st.number_input("Monthly Contribution", min_value=500.0, max_value=1000000.0, value=15000.0, step=1000.0, key="sip_m_in")
        sip_r_pct = st.slider("Expected Nominal Return (% p.a.)", min_value=1.0, max_value=25.0, value=float(r_default), step=0.5, key="sip_r_in")
        sip_r = sip_r_pct / 100.0
        sip_years = st.slider("Horizon in Years", min_value=1, max_value=40, value=20, step=1, key="sip_y_in")
        sip_step_pct = st.slider("Annual Contribution Escalation (%)", min_value=0.0, max_value=30.0, value=float(step_default), step=1.0, key="sip_step_in")
        
        st.markdown("---")
        st.markdown("##### Inflation & FIRE Milestone")
        sip_inf_pct = st.slider("Expected Annual Inflation (%)", min_value=0.0, max_value=15.0, value=6.0, step=0.5, key="sip_inf_in")
        sip_inf = sip_inf_pct / 100.0
        fire_milestone = st.number_input("Target Wealth Milestone", min_value=100000.0, max_value=100000000.0, value=10000000.0, step=500000.0, key="sip_target_in")

    # Computations
    sip_base = calculate_sip_wealth(sip_monthly, sip_r, sip_years)
    sip_step_sum, sip_step_df = calculate_step_up_sip(sip_monthly, sip_r, sip_years, annual_step_up_percent=sip_step_pct)
    r_fisher = real_rate_of_return(sip_r, sip_inf)
    half_life_yrs = purchasing_power_half_life(sip_inf) if sip_inf > 0 else float("inf")

    # Milestone hit calculation
    milestone_hit_year = None
    years_scan = list(range(1, sip_years + 1))
    checkpoints = []
    
    for y in years_scan:
        b_res = calculate_sip_wealth(sip_monthly, sip_r, y)
        s_res, _ = calculate_step_up_sip(sip_monthly, sip_r, y, annual_step_up_percent=sip_step_pct)
        real_val = s_res["future_value"] * math.pow(1.0 + sip_inf, -y)
        if milestone_hit_year is None and s_res["future_value"] >= fire_milestone:
            milestone_hit_year = y

        if y in [5, 10, 15, 20, 25, 30, 35, 40] or y == sip_years:
            checkpoints.append({
                "Year": y,
                "Capital Invested": format_currency(s_res["total_invested"], curr_sym),
                "Fixed SIP Corpus": format_currency(b_res["future_value"], curr_sym),
                "Step-Up Corpus": format_currency(s_res["future_value"], curr_sym),
                "Real Purchasing Power": format_currency(real_val, curr_sym),
            })

    with col2:
        # High-Density 2x2 Responsive Metric Grid
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1:
            render_stat_card(
                label="Fixed SIP Corpus",
                value=format_currency(sip_base["future_value"], curr_sym),
                subtext=f"Capital: {format_currency(sip_base['total_invested'], curr_sym)}",
                delta="Flat Baseline",
                delta_type="amber"
            )
        with r1_c2:
            render_stat_card(
                label=f"Step-Up Corpus (+{sip_step_pct:.0f}%)",
                value=format_currency(sip_step_sum["future_value"], curr_sym),
                subtext=f"Capital: {format_currency(sip_step_sum['total_invested'], curr_sym)}",
                delta=f"+{(sip_step_sum['future_value']/sip_base['future_value'] - 1)*100:.1f}% vs Flat",
                delta_type="green",
                value_color="#10B981"
            )

        r2_c1, r2_c2 = st.columns(2)
        with r2_c1:
            render_stat_card(
                label="Fisher Real Return",
                value=format_percentage(r_fisher),
                subtext=f"Nominal {sip_r_pct:.1f}% - Inf {sip_inf_pct:.1f}%",
                delta="Real Rate",
                delta_type="blue"
            )
        with r2_c2:
            hit_subtext = f"Achieved in Year {milestone_hit_year}" if milestone_hit_year else "Beyond Horizon"
            render_stat_card(
                label="Milestone Target",
                value=f"{format_currency(fire_milestone, curr_sym)}",
                subtext=hit_subtext,
                delta=f"Year {milestone_hit_year}" if milestone_hit_year else "Pending",
                delta_type="green" if milestone_hit_year else "red",
                value_color="#38BDF8"
            )

        # Multi-Year Plot
        step_corpus_series, base_corpus_series, real_corpus_series, capital_series = [], [], [], []
        for y in years_scan:
            b_s = calculate_sip_wealth(sip_monthly, sip_r, y)
            s_s, _ = calculate_step_up_sip(sip_monthly, sip_r, y, annual_step_up_percent=sip_step_pct)
            step_corpus_series.append(s_s["future_value"])
            base_corpus_series.append(b_s["future_value"])
            real_corpus_series.append(s_s["future_value"] * math.pow(1.0 + sip_inf, -y))
            capital_series.append(s_s["total_invested"])

        fig_sip = go.Figure()
        fig_sip.add_trace(go.Scatter(x=years_scan, y=step_corpus_series, mode="lines", name=f"Step-Up SIP (+{sip_step_pct:.0f}%/yr)", line=dict(color="#10B981", width=3)))
        fig_sip.add_trace(go.Scatter(x=years_scan, y=base_corpus_series, mode="lines", name="Fixed Monthly SIP", line=dict(color="#38BDF8", width=2.5)))
        fig_sip.add_trace(go.Scatter(x=years_scan, y=real_corpus_series, mode="lines", name="Real Purchasing Power (Step-Up)", line=dict(color="#F59E0B", width=2, dash="dash")))
        fig_sip.add_trace(go.Scatter(x=years_scan, y=capital_series, mode="lines", name="Cumulative Capital Invested", line=dict(color="#64748B", width=1.5, dash="dot")))
        fig_sip.add_hline(y=fire_milestone, line_dash="solid", line_color="#818CF8", annotation_text=f"Milestone Target: {format_currency(fire_milestone, curr_sym)}", annotation_position="top left")

        render_chart_header(
            "Wealth Accumulation Trajectory: Nominal vs. Inflation-Adjusted Reality",
            "Fixed contributions vs. escalating Step-Up compounding discounted by the Fisher equation"
        )
        layout = plotly_base_layout(
            xaxis_title="Investment Horizon (Years)",
            yaxis_title=f"Portfolio Valuation ({curr_sym})",
            height=380,
            show_legend=True
        )
        fig_sip.update_layout(**layout)
        st.plotly_chart(fig_sip, use_container_width=True)

    # Checkpoint Table
    with st.expander("📅 View Milestone Checkpoints (5-Year Intervals)"):
        chk_df = pd.DataFrame(checkpoints)
        st.dataframe(chk_df, use_container_width=True)
