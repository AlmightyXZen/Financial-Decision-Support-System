"""
ui/tab_loans.py
Module 2: Consumer Debt, Amortization Mechanics & Prepayment Acceleration.
Author: Atharv Ranade
"""

import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from models.loans_and_credit import (
    calculate_emi,
    check_negative_amortization,
    generate_amortization_schedule,
    calculate_prepayment_savings,
)
from ui.styles import render_stat_card, render_chart_header, format_currency, plotly_base_layout, format_fraction


@st.cache_data(show_spinner=False)
def get_cached_schedule(principal: float, annual_rate: float, tenure_months: int, monthly_prepayment: float) -> pd.DataFrame:
    return generate_amortization_schedule(principal, annual_rate, tenure_months, monthly_prepayment=monthly_prepayment)


def render_tab_loans(curr_sym: str):
    """Renders the Debt & Amortization module."""
    
    # Preset quick-fill triggers across full container width
    l_cols = st.columns(3)
    p1_str = format_currency(3500000.0, curr_sym)
    p2_str = format_currency(1000000.0, curr_sym)
    p3_str = format_currency(500000.0, curr_sym)
    if l_cols[0].button(f"🏡 Home Loan ({p1_str} @ 8.5%, 20Y)", use_container_width=True):
        st.session_state["loan_p_val"] = 3500000.0
        st.session_state["loan_r_val"] = 8.5
        st.session_state["loan_t_val"] = 20
    if l_cols[1].button(f"🚗 Auto Loan ({p2_str} @ 9.2%, 5Y)", use_container_width=True):
        st.session_state["loan_p_val"] = 1000000.0
        st.session_state["loan_r_val"] = 9.2
        st.session_state["loan_t_val"] = 5
    if l_cols[2].button(f"💼 Personal Note ({p3_str} @ 12.5%, 3Y)", use_container_width=True):
        st.session_state["loan_p_val"] = 500000.0
        st.session_state["loan_r_val"] = 12.5
        st.session_state["loan_t_val"] = 3

    p_default = st.session_state.get("loan_p_val", 3000000.0)
    r_default = st.session_state.get("loan_r_val", 8.5)
    t_default = st.session_state.get("loan_t_val", 20)

    col1, col2 = st.columns([1, 2.2], gap="large")

    with col1:
        st.markdown("##### Debt Specifications")
        loan_p = st.number_input("Loan Amount ($P$)", min_value=10000.0, max_value=50000000.0, value=float(p_default), step=100000.0, key="loan_p_in")
        loan_r_pct = st.slider("Interest Rate (% per annum)", min_value=1.0, max_value=24.0, value=float(r_default), step=0.1, key="loan_r_in")
        loan_r = loan_r_pct / 100.0
        loan_years = st.slider("Tenure in Years", min_value=1, max_value=30, value=int(t_default), step=1, key="loan_y_in")
        loan_months = loan_years * 12
        prepay_val = st.number_input("Extra Monthly Principal Prepayment", min_value=0.0, max_value=200000.0, value=5000.0, step=1000.0, key="loan_prep_in")

        # Negative Amortization Boundary Watch
        base_monthly_interest = (loan_p * loan_r) / 12.0
        st.markdown("---")
        frac_accrual = format_fraction("<i>P</i> &middot; <i>r</i>", "12")
        st.markdown(
            f"""
            <div style="background: rgba(14, 27, 49, 0.70); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 0.65rem 0.85rem; margin-top: 0.6rem; margin-bottom: 0.8rem; font-size: 0.8rem; color: #94A3B8; display: flex; align-items: center; justify-content: space-between;">
                <span>⚠️ <b>Interest-Only Accrual:</b></span>
                <span style="color: #F8FAFC; font-weight: 700; font-family: 'JetBrains Mono', monospace;">{format_currency(base_monthly_interest, curr_sym)}/mo</span>
                <span style="font-size: 0.75rem; color: #94A3B8;">({frac_accrual})</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        test_pmt = st.number_input("Stress Test Custom Monthly Payment", min_value=500.0, max_value=float(base_monthly_interest * 2.5), value=float(round(base_monthly_interest * 0.9, -2)), step=500.0)
        neg_check = check_negative_amortization(loan_p, loan_r, test_pmt)
        if neg_check["is_negative_amortization"]:
            st.error(f"🚨 **Divergence Warning:** Payment is below monthly interest accrual ({format_currency(base_monthly_interest, curr_sym)}). Outstanding balance diverges to infinity.")
        else:
            st.success(f"✅ **Amortizing:** Net principal reduction of {format_currency(neg_check['net_principal_reduction'], curr_sym)} per month.")

    # Generate schedules
    base_emi = calculate_emi(loan_p, loan_r, loan_months)
    df_base = get_cached_schedule(loan_p, loan_r, loan_months, 0.0)
    df_prep = get_cached_schedule(loan_p, loan_r, loan_months, prepay_val)
    savings = calculate_prepayment_savings(loan_p, loan_r, loan_months, prepay_val)

    # Date projections
    start_date = datetime.date.today()
    base_payoff_date = start_date + datetime.timedelta(days=int(savings["original_tenure_months"] * 30.4375))
    prep_payoff_date = start_date + datetime.timedelta(days=int(savings["new_tenure_months"] * 30.4375))

    # 50% Debt-free milestone
    milestone_50_row = df_base[df_base["Closing_Balance"] <= (loan_p * 0.5)]
    month_50_pct = milestone_50_row.iloc[0]["Month"] if not milestone_50_row.empty else None

    with col2:
        # High-Density 2x2 Responsive Metric Grid
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1:
            render_stat_card(
                label="Monthly EMI",
                value=format_currency(base_emi, curr_sym),
                subtext=f"{loan_months} months scheduled",
                delta=f"Payoff: {base_payoff_date.strftime('%b %Y')}",
                delta_type="blue"
            )
        with r1_c2:
            render_stat_card(
                label="Total Interest (Base)",
                value=format_currency(savings["original_total_interest"], curr_sym),
                subtext=f"{(savings['original_total_interest']/loan_p)*100:.1f}% of principal cost",
                delta="Baseline Cost",
                delta_type="amber"
            )

        r2_c1, r2_c2 = st.columns(2)
        with r2_c1:
            render_stat_card(
                label="Interest Saved",
                value=format_currency(savings["interest_saved"], curr_sym),
                subtext=f"{savings['percentage_interest_saved']:.1f}% cost reduction",
                delta=f"-{savings['percentage_interest_saved']:.1f}% Saved",
                delta_type="green",
                value_color="#10B981"
            )
        with r2_c2:
            render_stat_card(
                label="Accelerated Payoff",
                value=f"{savings['months_saved']} Mo Saved",
                subtext=f"Payoff: {prep_payoff_date.strftime('%b %Y')} ({savings['new_tenure_months']/12:.1f} yrs)",
                delta=f"-{savings['months_saved']/12:.1f} Yrs Tenure",
                delta_type="blue",
                value_color="#38BDF8"
            )

        # Plot 1: Stacked Area Breakdown of Payment Split
        fig_breakdown = go.Figure()
        fig_breakdown.add_trace(go.Scatter(
            x=df_base["Month"],
            y=df_base["Principal_Paid"],
            mode="lines",
            name="Principal Paid",
            stackgroup="one",
            fillcolor="rgba(16, 185, 129, 0.65)",
            line=dict(color="#10B981", width=1)
        ))
        fig_breakdown.add_trace(go.Scatter(
            x=df_base["Month"],
            y=df_base["Interest_Paid"],
            mode="lines",
            name="Interest Paid",
            stackgroup="one",
            fillcolor="rgba(244, 63, 94, 0.65)",
            line=dict(color="#F43F5E", width=1)
        ))
        if month_50_pct:
            fig_breakdown.add_vline(
                x=month_50_pct,
                line_dash="dot",
                line_color="#38BDF8",
                annotation_text=f"50% Principal Milestone (Mo {month_50_pct})",
                annotation_position="top right"
            )

        render_chart_header(
            "Monthly Payment Breakdown: Principal vs. Interest Split",
            "The interest-to-principal crossover trajectory over the loan tenure"
        )
        layout1 = plotly_base_layout(
            xaxis_title="Tenure Month",
            yaxis_title=f"Monthly Split ({curr_sym})",
            height=340,
            show_legend=True
        )
        fig_breakdown.update_layout(**layout1)
        st.plotly_chart(fig_breakdown, use_container_width=True)

        # Plot 2: Outstanding Balance Trajectory (Baseline vs Prepayment)
        render_chart_header(
            "Loan Principal Balance Trajectory",
            f"Comparing standard amortization vs. accelerated prepayment (+{format_currency(prepay_val, curr_sym)}/mo)"
        )
        fig_bal = go.Figure()
        fig_bal.add_trace(go.Scatter(x=df_base["Month"], y=df_base["Closing_Balance"], mode="lines", name="Standard EMI", line=dict(color="#F43F5E", width=2.5)))
        fig_bal.add_trace(go.Scatter(x=df_prep["Month"], y=df_prep["Closing_Balance"], mode="lines", name=f"Accelerated (+{format_currency(prepay_val, curr_sym)}/mo)", line=dict(color="#38BDF8", width=2.5, dash="dash")))

        layout2 = plotly_base_layout(
            xaxis_title="Tenure Month",
            yaxis_title=f"Principal Balance ({curr_sym})",
            height=300,
            show_legend=True
        )
        fig_bal.update_layout(**layout2)
        st.plotly_chart(fig_bal, use_container_width=True)

    # Annual Summary Table & CSV Export
    with st.expander("📊 View Annual Schedule & Export Full CSV"):
        df_base["Year"] = (df_base["Month"] - 1) // 12 + 1
        annual_df = df_base.groupby("Year").agg({
            "Principal_Paid": "sum",
            "Interest_Paid": "sum",
            "Total_Payment": "sum",
            "Closing_Balance": "last"
        }).reset_index()
        annual_df.columns = ["Year", "Total Principal Paid", "Total Interest Paid", "Total Payment", "Year-End Balance"]

        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            st.dataframe(annual_df, use_container_width=True)
        with col_t2:
            st.markdown("##### Export Data")
            csv_data = df_base.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Full Month-by-Month CSV",
                data=csv_data,
                file_name="loan_amortization_schedule.csv",
                mime="text/csv",
                use_container_width=True
            )
