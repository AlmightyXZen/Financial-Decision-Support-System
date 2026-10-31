"""
Unit Tests: tests/test_capital_budgeting.py
Validates models/capital_budgeting.py: analytical derivatives, Newton-Raphson quadratic root convergence,
and Abel-Ruffini high-degree polynomial solving.
"""

import math
import pytest
from models.capital_budgeting import (
    net_present_value,
    npv_first_derivative,
    internal_rate_of_return,
    discounted_payback_period
)


class TestNPVAndDerivatives:
    def test_analytical_npv(self):
        # Initial: -1000, Cash flows: 400, 400, 400 at 10% discount rate
        cf = [-1000.0, 400.0, 400.0, 400.0]
        r = 0.10
        expected = -1000.0 + (400.0 / 1.10) + (400.0 / 1.21) + (400.0 / 1.331)
        npv = net_present_value(r, cf)
        assert math.isclose(npv, expected, abs_tol=1e-7)

    def test_analytical_first_derivative_against_finite_differences(self):
        # Cross-validate exact analytical derivative f'(r) against central finite difference
        cf = [-500000.0, 150000.0, 200000.0, 250000.0, 180000.0]
        r = 0.12
        h = 1e-6
        
        analytical_deriv = npv_first_derivative(r, cf)
        numerical_deriv = (net_present_value(r + h, cf) - net_present_value(r - h, cf)) / (2.0 * h)
        
        assert math.isclose(analytical_deriv, numerical_deriv, rel_tol=1e-5)


class TestInternalRateOfReturn:
    def test_newton_raphson_quadratic_convergence(self):
        # Monograph Chapter 10 Hand Example: [-1000, 400, 400, 400]
        cf = [-1000.0, 400.0, 400.0, 400.0]
        irr = internal_rate_of_return(cf)
        
        # At IRR, NPV(r*) must strictly evaluate to zero
        npv_at_irr = net_present_value(irr, cf)
        assert abs(npv_at_irr) <= 1e-6
        # Expected root: ~0.09701 (9.70%)
        assert math.isclose(irr, 0.09701, abs_tol=1e-3)

    def test_high_degree_abel_ruffini_case(self):
        # Polynomial of degree T = 6 (Degree > 4: Galois theory proves radical solution impossible!)
        cf = [-1000000.0, 200000.0, 250000.0, 300000.0, 320000.0, 280000.0, 150000.0]
        irr = internal_rate_of_return(cf)
        
        assert irr > 0.0
        npv_at_irr = net_present_value(irr, cf)
        assert abs(npv_at_irr) <= 1e-6

    def test_invalid_cash_flows(self):
        # All positive: no root possible
        with pytest.raises(ValueError):
            internal_rate_of_return([100.0, 200.0, 300.0])


class TestDiscountedPayback:
    def test_payback_period_calculation(self):
        cf = [-1000.0, 500.0, 500.0, 500.0]
        # At 0% rate, payback is exactly 2.0 periods
        payback_zero = discounted_payback_period(0.0, cf)
        assert math.isclose(payback_zero, 2.0, abs_tol=1e-5)
        
        # At positive rate, discounted payback must take longer than undiscounted
        payback_pos = discounted_payback_period(0.10, cf)
        assert payback_pos > 2.0
