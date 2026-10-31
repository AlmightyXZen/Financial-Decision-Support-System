"""
Unit Tests: tests/test_time_value.py
Validates models/time_value.py against analytical benchmarks and IEEE 754 precision standards (epsilon <= 1e-7).
"""

import math
import pytest
from models.time_value import (
    simple_interest,
    simple_interest_amount,
    compound_interest_amount,
    accrued_compound_interest,
    continuous_compounding_amount,
    discrete_to_continuous_yield,
    continuous_to_discrete_yield,
    present_value,
    future_value,
    nominal_to_effective_rate,
    effective_to_nominal_rate
)

TOL = 1e-7


class TestSimpleInterest:
    def test_analytical_hand_benchmark(self):
        # Monograph Chapter 01 Hand Example: P = 100,000, r = 8%, t = 3 years
        p, r, t = 100000.0, 0.08, 3.0
        assert math.isclose(simple_interest(p, r, t), 24000.0, abs_tol=TOL)
        assert math.isclose(simple_interest_amount(p, r, t), 124000.0, abs_tol=TOL)

    def test_subadditivity_violation(self):
        # Theorem: A(t1 + t2) < A(t1) * A(t2) / P
        p, r = 100000.0, 0.10
        t1, t2 = 1.0, 2.0
        a_combined = simple_interest_amount(p, r, t1 + t2)
        a_separate = (simple_interest_amount(p, r, t1) * simple_interest_amount(p, r, t2)) / p
        assert a_combined < a_separate

    def test_zero_boundaries(self):
        assert simple_interest(0.0, 0.10, 5.0) == 0.0
        assert simple_interest(10000.0, 0.0, 5.0) == 0.0
        assert simple_interest(10000.0, 0.10, 0.0) == 0.0
        assert simple_interest_amount(10000.0, 0.0, 5.0) == 10000.0

    def test_domain_validation(self):
        with pytest.raises(ValueError):
            simple_interest(-1000.0, 0.05, 1.0)
        with pytest.raises(ValueError):
            simple_interest(1000.0, -0.05, 1.0)
        with pytest.raises(ValueError):
            simple_interest(1000.0, 0.05, -1.0)


class TestCompoundInterest:
    def test_analytical_hand_benchmark(self):
        # Monograph Chapter 02 Hand Example: P = 100,000, r = 10%, t = 2 years, annual compounding
        p, r, t = 100000.0, 0.10, 2.0
        assert math.isclose(compound_interest_amount(p, r, t, m=1), 121000.0, abs_tol=TOL)
        assert math.isclose(accrued_compound_interest(p, r, t, m=1), 21000.0, abs_tol=TOL)

    def test_compounding_frequency_monotonicity(self):
        # Theorem: Wealth is strictly monotonically increasing with frequency m
        p, r, t = 100000.0, 0.12, 5.0
        a_annual = compound_interest_amount(p, r, t, compounding_frequency=1)
        a_semi = compound_interest_amount(p, r, t, compounding_frequency=2)
        a_quarterly = compound_interest_amount(p, r, t, compounding_frequency=4)
        a_monthly = compound_interest_amount(p, r, t, compounding_frequency=12)
        a_daily = compound_interest_amount(p, r, t, compounding_frequency=365)
        
        assert a_annual < a_semi < a_quarterly < a_monthly < a_daily

    def test_invalid_frequency(self):
        with pytest.raises(ValueError):
            compound_interest_amount(1000.0, 0.10, 2.0, compounding_frequency=0)


class TestContinuousCompounding:
    def test_euler_limit_convergence(self):
        # As m -> infinity, discrete compounding approaches continuous compounding P * e^(rt)
        p, r, t = 100000.0, 0.08, 5.0
        continuous_val = continuous_compounding_amount(p, r, t)
        assert math.isclose(continuous_val, 100000.0 * math.exp(0.40), abs_tol=TOL)
        
        discrete_m_huge = compound_interest_amount(p, r, t, compounding_frequency=100000)
        assert math.isclose(discrete_m_huge, continuous_val, rel_tol=1e-5)

    def test_yield_conversion_roundtrip(self):
        # Roundtrip: discrete -> continuous -> discrete
        r_d, m = 0.12, 12
        r_c = discrete_to_continuous_yield(r_d, m)
        r_d_recovered = continuous_to_discrete_yield(r_c, m)
        assert math.isclose(r_d, r_d_recovered, abs_tol=TOL)


class TestPresentAndFutureValue:
    def test_discounting_inversion(self):
        p, r, t, m = 250000.0, 0.075, 4.0, 12
        fv = future_value(p, r, t, compounding_frequency=m)
        pv = present_value(fv, r, t, compounding_frequency=m)
        assert math.isclose(p, pv, abs_tol=TOL)

    def test_continuous_discounting_inversion(self):
        p, r, t = 500000.0, 0.09, 3.0
        fv = future_value(p, r, t, continuous=True)
        pv = present_value(fv, r, t, continuous=True)
        assert math.isclose(p, pv, abs_tol=TOL)


class TestNominalVsEffectiveRate:
    def test_ear_calculation(self):
        # 12% APR compounded monthly: EAR = (1 + 0.01)^12 - 1 = 12.6825%
        r_nom, m = 0.12, 12
        ear = nominal_to_effective_rate(r_nom, m)
        expected_ear = math.pow(1.01, 12) - 1.0
        assert math.isclose(ear, expected_ear, abs_tol=TOL)

    def test_ear_roundtrip(self):
        r_nom, m = 0.18, 12
        ear = nominal_to_effective_rate(r_nom, m)
        r_recovered = effective_to_nominal_rate(ear, m)
        assert math.isclose(r_nom, r_recovered, abs_tol=TOL)
