"""
Master Build Script: Compiles all 12 textbook chapters in theory_and_derivations.
Usage:
    python theory_and_derivations/build_all_chapters.py
"""

import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from chapters import (
    ch01_simple_interest,
    ch02_compound_interest,
    ch03_continuous_compounding,
    ch04_present_future_value,
    ch05_effective_annual_rate,
    ch06_emi_amortization,
    ch07_sip_wealth_accumulation,
    ch08_inflation_purchasing_power,
    ch09_net_present_value,
    ch10_internal_rate_of_return,
    ch11_geometric_brownian_motion,
    ch12_monte_carlo_simulation,
)

CHAPTERS = [
    ("Chapter 01: Simple Interest & Linear Accumulation", ch01_simple_interest, "01_Simple_Interest.pdf"),
    ("Chapter 02: Compound Interest & Geometric Accumulation", ch02_compound_interest, "02_Compound_Interest.pdf"),
    ("Chapter 03: Continuous Compounding & Infinitesimal Calculus", ch03_continuous_compounding, "03_Continuous_Compounding.pdf"),
    ("Chapter 04: Present Value, Future Value & Discounting", ch04_present_future_value, "04_Present_Value_and_Future_Value.pdf"),
    ("Chapter 05: Nominal vs. Effective Annual Rate (EAR)", ch05_effective_annual_rate, "05_Effective_Annual_Rate.pdf"),
    ("Chapter 06: Equated Monthly Installment (EMI) & Debt Amortization", ch06_emi_amortization, "06_Equated_Monthly_Installment_EMI.pdf"),
    ("Chapter 07: Systematic Investment Plan (SIP) & Annuity Wealth Accumulation", ch07_sip_wealth_accumulation, "07_Systematic_Investment_Plan_SIP.pdf"),
    ("Chapter 08: Inflation, Real Purchasing Power & The Fisher Equation", ch08_inflation_purchasing_power, "08_Inflation_and_Purchasing_Power.pdf"),
    ("Chapter 09: Net Present Value (NPV) & Capital Budgeting", ch09_net_present_value, "09_Net_Present_Value_NPV.pdf"),
    ("Chapter 10: Internal Rate of Return (IRR) & Root Finding", ch10_internal_rate_of_return, "10_Internal_Rate_of_Return_IRR.pdf"),
    ("Chapter 11: Geometric Brownian Motion (GBM) & Ito's Lemma", ch11_geometric_brownian_motion, "11_Geometric_Brownian_Motion.pdf"),
    ("Chapter 12: Monte Carlo Simulation & Quantitative Risk Analysis", ch12_monte_carlo_simulation, "12_Monte_Carlo_Simulation.pdf"),
]

def build_all():
    print("=" * 78)
    print(" FINANCIAL DECISION SUPPORT SYSTEM (FDSS) - MATHEMATICAL MONOGRAPH SERIES")
    print(" Compiling all 12 Textbook Chapters to PDF...")
    print("=" * 78)

    t0 = time.time()
    for idx, (title, module, filename) in enumerate(CHAPTERS, 1):
        target_path = os.path.join(CURRENT_DIR, filename)
        module.build_pdf(target_path)
        file_size_kb = os.path.getsize(target_path) / 1024.0
        print(f"[{idx:02d}/12] [OK] {title:<60} -> {filename} ({file_size_kb:.1f} KB)")

    elapsed = time.time() - t0
    print("=" * 78)
    print(f"SUCCESS: All 12 textbook chapters built cleanly in {elapsed:.2f} seconds.")
    print("=" * 78)

if __name__ == "__main__":
    build_all()
