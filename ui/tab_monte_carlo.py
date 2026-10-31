"""
ui/tab_monte_carlo.py
Module 5: Vectorized Itô Geometric Brownian Motion & Stochastic Risk Simulation.
Author: Atharv Ranade
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from models.monte_carlo import (
    calculate_volatility_drag,
    simulate_gbm_paths,
    goal_attainment_probability,
    calculate_value_at_risk,
    compute_simulation_statistics,
)
from ui.styles import render_stat_card, render_chart_header, format_currency, format_percentage, plotly_base_layout


@st.cache_data(show_spinner=False)
def get_cached_monte_carlo_paths(s0: float, mu: float, sigma: float, t_years: float, n_steps: int, n_paths: int, seed: int):
    return simulate_gbm_paths(s0, mu, sigma, t_years, n_steps=n_steps, n_paths=n_paths, seed=seed)


def render_tab_monte_carlo(curr_sym: str):
    """Renders the Monte Carlo Stochastic Risk Lab module."""
    
    # Presets
    col_pre, _ = st.columns([3, 1])
    with col_pre:
        m_cols = st.columns(4)
        if m_cols[0].button("🚀 Tech Bull (18% μ, 16% σ)", use_container_width=True):
            st.session_state["mc_mu_val"] = 18.0
            st.session_state["mc_sigma_val"] = 16.0
        if m_cols[1].button("📉 2008 Crash Shock (-4% μ, 34% σ)", use_container_width=True):
            st.session_state["mc_mu_val"] = -4.0
            st.session_state["mc_sigma_val"] = 34.0
        if m_cols[2].button("🌪️ Stagflation (4% μ, 24% σ)", use_container_width=True):
            st.session_state["mc_mu_val"] = 4.0
            st.session_state["mc_sigma_val"] = 24.0
        if m_cols[3].button("🛡️ All-Weather (9% μ, 11% σ)", use_container_width=True):
            st.session_state["mc_mu_val"] = 9.0
            st.session_state["mc_sigma_val"] = 11.0

    mu_default = st.session_state.get("mc_mu_val", 12.0)
    sigma_default = st.session_state.get("mc_sigma_val", 18.0)

    col1, col2 = st.columns([1, 2.2], gap="large")

    with col1:
        st.markdown("##### Stochastic Parameters")
        mc_s0 = st.number_input("Initial Portfolio ($S_0$)", min_value=10000.0, max_value=20000000.0, value=500000.0, step=50000.0, key="mc_s0_in")
        mc_mu_pct = st.slider("Expected Annual Drift (μ %)", min_value=-10.0, max_value=30.0, value=float(mu_default), step=0.5, key="mc_mu_in")
        mc_mu = mc_mu_pct / 100.0
        mc_sigma_pct = st.slider("Annual Volatility (σ %)", min_value=2.0, max_value=60.0, value=float(sigma_default), step=0.5, key="mc_sigma_in")
        mc_sigma = mc_sigma_pct / 100.0
        mc_years = st.slider("Simulation Horizon ($T$ in Years)", min_value=1, max_value=30, value=10, step=1, key="mc_t_in")
        mc_paths = st.select_slider("Simulation Trajectories ($M$)", options=[250, 500, 1000, 2000, 5000], value=1000, key="mc_paths_in")
        mc_target = st.number_input("Target Wealth Milestone", min_value=100000.0, max_value=50000000.0, value=1500000.0, step=100000.0, key="mc_target_in")
        mc_seed = st.number_input("Random Seed (for reproducibility)", min_value=1, max_value=999999, value=42, step=1, key="mc_seed_in")

    # Simulation execution
    time_grid, paths_matrix = get_cached_monte_carlo_paths(
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

    with col2:
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_stat_card(
                label="Expected Mean",
                value=format_currency(stats_dict["sample_mean"], curr_sym),
                subtext=f"Median: {format_currency(stats_dict['sample_median'], curr_sym)}",
                delta=f"+{((stats_dict['sample_mean']/mc_s0)-1)*100:.1f}%",
                delta_type="green" if stats_dict["sample_mean"] >= mc_s0 else "red",
                value_color="#10B981"
            )
        with k2:
            render_stat_card(
                label="Volatility Drag",
                value=f"{drag_dict['annual_volatility_drag_percent']:.2f}%/yr",
                subtext=f"Gap: {format_currency(drag_dict['monetary_wealth_gap'], curr_sym)}",
                delta="Penalty -½ σ²",
                delta_type="red",
                value_color="#F43F5E"
            )
        with k3:
            goal_color = "#10B981" if goal_prob >= 0.70 else ("#F59E0B" if goal_prob >= 0.40 else "#F43F5E")
            render_stat_card(
                label="Goal Attainment",
                value=format_percentage(goal_prob),
                subtext=f"Target: {format_currency(mc_target, curr_sym)}",
                delta="P(Wealth >= Goal)",
                delta_type="green" if goal_prob >= 0.50 else "amber",
                value_color=goal_color
            )
        with k4:
            render_stat_card(
                label="95% Value at Risk (VaR)",
                value=format_currency(risk_dict["cutoff_price"], curr_sym),
                subtext=f"Max Tail Loss: {format_currency(risk_dict['value_at_risk'], curr_sym)}",
                delta="5th %ile Floor",
                delta_type="blue",
                value_color="#818CF8"
            )

        # Plot 1: Vectorized Path Fan Chart
        fig_fan = go.Figure()
        sample_subset = min(60, mc_paths)
        for i in range(sample_subset):
            fig_fan.add_trace(go.Scatter(
                x=time_grid, y=paths_matrix[:, i], mode="lines",
                line=dict(color="rgba(56, 189, 248, 0.12)", width=1), hoverinfo="skip", showlegend=False
            ))

        mean_path = np.mean(paths_matrix, axis=1)
        median_path = np.median(paths_matrix, axis=1)
        p05_path = np.percentile(paths_matrix, 5, axis=1)
        p95_path = np.percentile(paths_matrix, 95, axis=1)

        fig_fan.add_trace(go.Scatter(x=time_grid, y=mean_path, mode="lines", name="Expected Mean E[S_t]", line=dict(color="#10B981", width=3)))
        fig_fan.add_trace(go.Scatter(x=time_grid, y=median_path, mode="lines", name="Median Path (50th %)", line=dict(color="#38BDF8", width=2.5)))
        fig_fan.add_trace(go.Scatter(x=time_grid, y=p05_path, mode="lines", name="5th %ile (95% VaR Floor)", line=dict(color="#F43F5E", width=2, dash="dash")))
        fig_fan.add_trace(go.Scatter(x=time_grid, y=p95_path, mode="lines", name="95th %ile Upper Bound", line=dict(color="#818CF8", width=2, dash="dot")))
        fig_fan.add_hline(y=mc_target, line_dash="solid", line_color="#F59E0B", annotation_text=f"Target: {format_currency(mc_target, curr_sym)}", annotation_position="top left")

        render_chart_header(
            "Geometric Brownian Motion Simulation",
            f"{mc_paths:,} Vectorized Stochastic Trajectories • Horizon T = {mc_years} Years"
        )
        layout1 = plotly_base_layout(
            xaxis_title="Time Horizon (Years)",
            yaxis_title=f"Portfolio Valuation ({curr_sym})",
            height=400,
            show_legend=True
        )
        fig_fan.update_layout(**layout1)
        st.plotly_chart(fig_fan, use_container_width=True)

        # Plot 2: Terminal Wealth Distribution Histogram
        render_chart_header(
            "Terminal Wealth Distribution & Downside Tail Risk",
            f"Ensemble probability density across {mc_paths:,} simulated terminal outcomes"
        )
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=terminal_wealths, nbinsx=50,
            marker=dict(color="rgba(56, 189, 248, 0.7)", line=dict(color="#38BDF8", width=1)),
            name="Terminal Wealth"
        ))
        fig_hist.add_vline(x=risk_dict["cutoff_price"], line_dash="dash", line_color="#F43F5E", line_width=2, annotation_text="95% VaR Floor", annotation_position="top left")
        fig_hist.add_vline(x=mc_target, line_dash="dash", line_color="#F59E0B", line_width=2, annotation_text="Target Milestone", annotation_position="top right")
        fig_hist.add_vline(x=stats_dict["sample_median"], line_dash="dot", line_color="#10B981", line_width=2, annotation_text="Median", annotation_position="bottom right")

        layout2 = plotly_base_layout(
            xaxis_title=f"Terminal Value ({curr_sym})",
            yaxis_title="Path Frequency",
            height=280,
            show_legend=False
        )
        fig_hist.update_layout(**layout2)
        st.plotly_chart(fig_hist, use_container_width=True)
