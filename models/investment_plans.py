"""
Module: models/investment_plans.py
Theoretical Foundation: Chapters 07 (SIP Annuity-Due) & 08 (Inflation & The Fisher Equation) of FDSS Monograph.

Covers:
1. Systematic Investment Plan (SIP) Annuity-Due Future Value:
   FV = C * [ ((1+i)^n - 1) / i ] * (1+i), with i = r / 12, n = 12 * t
2. Step-Up SIP (Annual contribution escalation matching salary growth)
3. Systematic Withdrawal Plan (SWP) Capital Depletion
4. The Exact Fisher Equation for Inflation:
   (1 + r_n) = (1 + r_r) * (1 + i) => r_r = (r_n - i) / (1 + i)
5. Purchasing Power Half-Life & Monetary Erosion:
   t_{1/2} = ln(2) / ln(1 + i)
"""

import math
from typing import Dict, Any, Tuple
import pandas as pd


def calculate_sip_wealth(
    monthly_investment: float,
    annual_expected_return: float,
    tenure_years: float
) -> Dict[str, float]:
    """
    Computes wealth accumulated via a Systematic Investment Plan (SIP).
    Treated strictly as an Annuity-Due (investments committed at the start of each month).
    
    Formula:
        i = annual_expected_return / 12
        n = round(tenure_years * 12)
        FV = C * [ ((1 + i)^n - 1) / i ] * (1 + i)
    """
    if monthly_investment <= 0.0:
        raise ValueError("Monthly investment must be strictly positive.")
    if annual_expected_return < 0.0:
        raise ValueError("Expected annual return must be non-negative.")
    if tenure_years <= 0.0:
        raise ValueError("Tenure years must be strictly positive.")
        
    n_months = int(round(tenure_years * 12))
    total_invested = monthly_investment * n_months
    
    # Boundary: zero rate of return (pure linear savings)
    if annual_expected_return == 0.0:
        return {
            "future_value": float(total_invested),
            "total_invested": float(total_invested),
            "wealth_gain": 0.0,
            "absolute_return_pct": 0.0
        }
        
    i_monthly = annual_expected_return / 12.0
    fv = monthly_investment * ((math.pow(1.0 + i_monthly, n_months) - 1.0) / i_monthly) * (1.0 + i_monthly)
    wealth_gain = fv - total_invested
    abs_return_pct = (wealth_gain / total_invested) * 100.0
    
    return {
        "future_value": round(fv, 2),
        "total_invested": round(total_invested, 2),
        "wealth_gain": round(wealth_gain, 2),
        "absolute_return_pct": round(abs_return_pct, 2)
    }


def calculate_step_up_sip(
    initial_monthly_investment: float,
    annual_expected_return: float,
    tenure_years: int,
    annual_step_up_percent: float = 10.0
) -> Tuple[Dict[str, float], pd.DataFrame]:
    """
    Computes wealth accumulation under an escalating Step-Up SIP.
    Monthly contribution increases by `annual_step_up_percent` at the start of every year.
    
    Returns:
        Summary metrics dictionary and month-by-month trajectory DataFrame.
    """
    if initial_monthly_investment <= 0.0:
        raise ValueError("Initial monthly investment must be positive.")
    if annual_expected_return < 0.0:
        raise ValueError("Expected return must be non-negative.")
    if tenure_years < 1:
        raise ValueError("Tenure years must be at least 1.")
    if annual_step_up_percent < 0.0:
        raise ValueError("Step-up percentage cannot be negative.")
        
    monthly_rate = annual_expected_return / 12.0
    total_months = tenure_years * 12
    step_up_multiplier = 1.0 + (annual_step_up_percent / 100.0)
    
    corpus = 0.0
    total_invested = 0.0
    current_sip = initial_monthly_investment
    
    records = []
    
    for month in range(1, total_months + 1):
        # Step up contribution at the start of each new year (months 13, 25, 37...)
        if month > 1 and (month - 1) % 12 == 0:
            current_sip *= step_up_multiplier
            
        # Annuity-due: interest earned on (corpus + new investment)
        invested_this_month = current_sip
        total_invested += invested_this_month
        
        corpus = (corpus + invested_this_month) * (1.0 + monthly_rate)
        
        records.append({
            "Month": month,
            "Year": (month - 1) // 12 + 1,
            "Monthly_SIP": round(current_sip, 2),
            "Cumulative_Invested": round(total_invested, 2),
            "Corpus_Value": round(corpus, 2),
            "Wealth_Gain": round(corpus - total_invested, 2)
        })
        
    df = pd.DataFrame(records)
    summary = {
        "future_value": round(corpus, 2),
        "total_invested": round(total_invested, 2),
        "wealth_gain": round(corpus - total_invested, 2),
        "absolute_return_pct": round(((corpus - total_invested) / total_invested) * 100.0, 2)
    }
    return summary, df


# ==============================================================================
# INFLATION & REAL PURCHASING POWER (Chapter 08)
# ==============================================================================

def real_rate_of_return(nominal_rate: float, inflation_rate: float) -> float:
    """
    Computes exact real rate of return via the Fisher Equation:
    (1 + r_n) = (1 + r_r) * (1 + i)
    r_r = (r_n - i) / (1 + i)
    
    Prevents the classical linear approximation error (r_r ~= r_n - i).
    """
    if inflation_rate <= -1.0:
        raise ValueError("Inflation rate cannot be <= -100%.")
    return float((nominal_rate - inflation_rate) / (1.0 + inflation_rate))


def purchasing_power_erosion(
    future_amount: float,
    inflation_rate: float,
    time_years: float
) -> float:
    """
    Calculates the real purchasing power of a future nominal amount today:
    Real Value = FV / (1 + i)^t
    """
    if future_amount < 0.0 or time_years < 0.0 or inflation_rate < -1.0:
        raise ValueError("Invalid parameters for purchasing power erosion.")
    if time_years == 0.0 or inflation_rate == 0.0:
        return float(future_amount)
    return float(future_amount / math.pow(1.0 + inflation_rate, time_years))


def purchasing_power_half_life(inflation_rate: float) -> float:
    """
    Computes the exact monetary half-life (years required for inflation to halve purchasing power):
    t_{1/2} = ln(2) / ln(1 + i)
    """
    if inflation_rate <= 0.0:
        raise ValueError("Inflation rate must be strictly positive to calculate half-life.")
    return float(math.log(2.0) / math.log1p(inflation_rate))
