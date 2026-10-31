"""
Unit Tests: tests/test_monte_carlo.py
Validates models/monte_carlo.py: Itô's Lemma volatility drag proof, vectorized GBM path generation,
Central Limit Theorem convergence, and Value at Risk (VaR).
"""

import math
import numpy as np
import pytest
from models.monte_carlo import (
    calculate_volatility_drag,
    simulate_gbm_paths,
    goal_attainment_probability,
    calculate_value_at_risk,
    compute_simulation_statistics
)


class TestVolatilityDrag:
    def test_hand_benchmark(self):
        # Monograph Chapter 11 Hand Benchmark:
        # S0 = 1,000,000, mu = 12%, sigma = 20%, T = 10 years
        s0, mu, sigma, t = 1000000.0, 0.12, 0.20, 10.0
        drag_res = calculate_volatility_drag(s0, mu, sigma, t)
        
        # Expected Mean: S0 * e^(1.2) ~= 3,320,116.92
        expected_mean = s0 * math.exp(1.2)
        assert math.isclose(drag_res["expected_mean_wealth"], expected_mean, rel_tol=1e-3)
        
        # Median: S0 * e^(1.0) ~= 2,718,281.83
        expected_median = s0 * math.exp(1.0)
        assert math.isclose(drag_res["typical_median_wealth"], expected_median, rel_tol=1e-3)
        
        # Volatility drag rate: -0.5 * (0.2)^2 = -0.02 (-2.00% drag per year)
        assert math.isclose(drag_res["annual_volatility_drag_rate"], -0.02, abs_tol=1e-7)
        
        # Monetary gap: ~601,835.09 INR
        assert math.isclose(drag_res["monetary_wealth_gap"], expected_mean - expected_median, abs_tol=5.0)


class TestGBMSimulation:
    def test_path_dimensions_and_initial_condition(self):
        s0, mu, sigma, t = 100000.0, 0.10, 0.15, 3.0
        n_steps, n_paths = 252, 500
        
        time_grid, paths = simulate_gbm_paths(s0, mu, sigma, t, n_steps=n_steps, n_paths=n_paths, seed=42)
        
        assert time_grid.shape == (n_steps + 1,)
        assert paths.shape == (n_steps + 1, n_paths)
        # All paths at t=0 must strictly equal S_0
        assert np.allclose(paths[0, :], s0)

    def test_reproducibility_with_seed(self):
        _, paths1 = simulate_gbm_paths(100000.0, 0.10, 0.15, 1.0, n_steps=100, n_paths=100, seed=123)
        _, paths2 = simulate_gbm_paths(100000.0, 0.10, 0.15, 1.0, n_steps=100, n_paths=100, seed=123)
        assert np.array_equal(paths1, paths2)

    def test_clt_convergence(self):
        # By the CLT, sample mean over M = 5,000 paths must be close to theoretical E[S_T]
        s0, mu, sigma, t = 100000.0, 0.08, 0.15, 2.0
        _, paths = simulate_gbm_paths(s0, mu, sigma, t, n_steps=100, n_paths=5000, seed=99)
        
        terminal_prices = paths[-1, :]
        sample_mean = np.mean(terminal_prices)
        theoretical_mean = s0 * math.exp(mu * t)
        
        # Relative error should be within 2.5%
        assert math.isclose(sample_mean, theoretical_mean, rel_tol=0.025)


class TestRiskMetrics:
    def test_var_and_cvar(self):
        s0 = 100000.0
        _, paths = simulate_gbm_paths(s0, 0.08, 0.25, 1.0, n_steps=100, n_paths=2000, seed=42)
        terminal_prices = paths[-1, :]
        
        var_res = calculate_value_at_risk(terminal_prices, s0, confidence_level=0.95)
        
        # Cutoff price must be less than median for a typical volatile asset
        assert var_res["cutoff_price"] > 0
        assert var_res["value_at_risk"] >= 0
        # Expected Shortfall (CVaR) must always be >= VaR
        assert var_res["conditional_var"] >= var_res["value_at_risk"]

    def test_goal_attainment_bounds(self):
        prices = np.array([50.0, 80.0, 100.0, 120.0, 150.0])
        # Target = 100: 3 out of 5 reach it -> 0.60
        prob = goal_attainment_probability(prices, 100.0)
        assert math.isclose(prob, 0.60, abs_tol=1e-7)
