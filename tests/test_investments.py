"""
Unit Tests: tests/test_investments.py
Validates models/investment_plans.py against Annuity-Due closed forms and the exact Fisher Inflation Equation.
"""

import math
import pytest
from models.investment_plans import (
    calculate_sip_wealth,
    calculate_step_up_sip,
    real_rate_of_return,
    purchasing_power_erosion,
    purchasing_power_half_life
)


class TestSIPCalculations:
    def test_hand_benchmark(self):
        # Monograph Chapter 07 Hand Benchmark: C = 10,000/mo, r = 12%, t = 10 years (120 months)
        # Annuity-Due: FV = C * [ ((1+i)^n - 1) / i ] * (1+i)
        res = calculate_sip_wealth(10000.0, 0.12, 10.0)
        assert res["total_invested"] == 1200000.0
        # Expected: ~2,323,390.76
        assert math.isclose(res["future_value"], 2323390.76, rel_tol=1e-3)
        assert res["wealth_gain"] > 1100000.0

    def test_zero_return_boundary(self):
        res = calculate_sip_wealth(5000.0, 0.0, 5.0)
        assert res["total_invested"] == 300000.0
        assert res["future_value"] == 300000.0
        assert res["wealth_gain"] == 0.0

    def test_step_up_sip_superiority(self):
        # A 10% annual step-up SIP must strictly generate more wealth than a static SIP
        static_res = calculate_sip_wealth(10000.0, 0.12, 15.0)
        step_up_res, df = calculate_step_up_sip(10000.0, 0.12, 15, annual_step_up_percent=10.0)
        
        assert step_up_res["future_value"] > static_res["future_value"]
        assert len(df) == 180


class TestInflationAndFisherEquation:
    def test_exact_fisher_relation(self):
        # Nominal: 12%, Inflation: 6%
        # Linear approximation says: 12 - 6 = 6% (Flawed!)
        # Exact Fisher: (0.12 - 0.06) / 1.06 = 0.0566038 (5.66%)
        r_r = real_rate_of_return(0.12, 0.06)
        expected = (0.12 - 0.06) / 1.06
        assert math.isclose(r_r, expected, abs_tol=1e-7)

    def test_purchasing_power_half_life(self):
        # Inflation 7%: t_half = ln(2) / ln(1.07) ~= 10.24 years
        t_half = purchasing_power_half_life(0.07)
        expected = math.log(2.0) / math.log(1.07)
        assert math.isclose(t_half, expected, abs_tol=1e-6)

    def test_purchasing_power_erosion(self):
        # INR 1,000,000 in 10 years at 7% inflation
        real_val = purchasing_power_erosion(1000000.0, 0.07, 10.0)
        expected = 1000000.0 / math.pow(1.07, 10.0)
        assert math.isclose(real_val, expected, abs_tol=1e-4)
