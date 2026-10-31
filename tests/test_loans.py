"""
Unit Tests: tests/test_loans.py
Validates models/loans_and_credit.py against closed-form benchmarks, amortization balance convergence,
and the Negative Amortization Boundary Theorem.
"""

import math
import pytest
from models.loans_and_credit import (
    calculate_emi,
    check_negative_amortization,
    generate_amortization_schedule,
    calculate_prepayment_savings
)

TOL = 1e-4


class TestEMICalculations:
    def test_hand_benchmark(self):
        # Monograph Chapter 06 Benchmark: P = 1,000,000, r = 8.5%, n = 240 months (20 years)
        p, r, n = 1000000.0, 0.085, 240
        emi = calculate_emi(p, r, n)
        # Expected EMI: 8678.23
        assert math.isclose(emi, 8678.23, rel_tol=1e-3)

    def test_zero_interest_rate(self):
        # r = 0%: EMI is pure linear division P / n
        emi = calculate_emi(120000.0, 0.0, 12)
        assert math.isclose(emi, 10000.0, abs_tol=1e-7)

    def test_domain_guardrails(self):
        with pytest.raises(ValueError):
            calculate_emi(-50000.0, 0.10, 12)
        with pytest.raises(ValueError):
            calculate_emi(50000.0, -0.05, 12)
        with pytest.raises(ValueError):
            calculate_emi(50000.0, 0.10, 0)


class TestAmortizationSchedule:
    def test_schedule_balance_convergence(self):
        # The closing balance on the final month must strictly equal 0.00
        p, r, n = 500000.0, 0.09, 60
        df = generate_amortization_schedule(p, r, n)
        
        assert len(df) == 60
        assert df.iloc[-1]["Closing_Balance"] == 0.00
        
        # Total principal repaid must match initial principal
        total_principal_paid = df["Principal_Paid"].sum()
        assert math.isclose(total_principal_paid, p, abs_tol=1.0)
        
        # Principal payments must strictly increase each month (geometric progression)
        for i in range(len(df) - 2):
            assert df.iloc[i+1]["Principal_Paid"] > df.iloc[i]["Principal_Paid"]


class TestNegativeAmortizationBoundary:
    def test_negative_amortization_detection(self):
        # Principal: 1,000,000, Rate: 12% (1% monthly = 10,000 interest)
        p, r = 1000000.0, 0.12
        monthly_interest = 10000.0
        
        # Test E = 8,000 (below interest -> divergent)
        res_fail = check_negative_amortization(p, r, 8000.0)
        assert res_fail["is_negative_amortization"] is True
        assert res_fail["status"] == "DIVERGENT_DEBT_TRAP"
        
        # Test E = 12,000 (above interest -> convergent)
        res_pass = check_negative_amortization(p, r, 12000.0)
        assert res_pass["is_negative_amortization"] is False
        assert res_pass["status"] == "CONVERGENT_AMORTIZING"

    def test_schedule_divergence_exception(self):
        # Generating a schedule with predatory monthly payment <= interest must raise ValueError
        with pytest.raises(ValueError, match="Negative Amortization Triggered"):
            generate_amortization_schedule(1000000.0, 0.12, 120, custom_monthly_payment=8000.0)


class TestPrepaymentSavings:
    def test_prepayment_accelerated_payoff(self):
        p, r, n = 1000000.0, 0.09, 240
        savings = calculate_prepayment_savings(p, r, n, monthly_prepayment=2000.0)
        
        # Adding prepayment must strictly reduce tenure and save interest
        assert savings["new_tenure_months"] < savings["original_tenure_months"]
        assert savings["months_saved"] > 0
        assert savings["interest_saved"] > 0.0
        assert savings["percentage_interest_saved"] > 0.0
