"""
Module: models/monte_carlo.py
Theoretical Foundation: Chapters 11 (GBM & Itô's Lemma) & 12 (Monte Carlo & Risk Analysis) of FDSS Monograph.

Covers:
1. Geometric Brownian Motion (GBM) Continuous Stochastic Differential Equation:
   dS_t = mu * S_t * dt + sigma * S_t * dW_t
2. Itô's Lemma Exact Path Discretization:
   S_{t+dt} = S_t * exp[ (mu - 0.5 * sigma^2)*dt + sigma * sqrt(dt) * Z ], where Z ~ N(0, 1)
3. Structural Volatility Drag Quantification:
   Delta mu = -0.5 * sigma^2.
   Divergence between Arithmetic Mean E[S_T] = S_0 * e^(mu*T) and Median S_0 * e^((mu - 0.5*sigma^2)*T).
4. Central Limit Theorem Convergence:
   Standard Error = sigma_sample / sqrt(M) = O(1 / sqrt(M)).
5. Quantitative Downside Tail Risk:
   - Empirical Goal Attainment Probability: P_hat(S_T >= Goal) = (1/M) * sum 1_{S_T,m >= Goal}
   - Value at Risk (VaR at 95% / 99% confidence)
   - Conditional Value at Risk (CVaR / Expected Shortfall)
"""

import math
from typing import Tuple, Dict, Any, Optional
import numpy as np


def calculate_volatility_drag(
    s0: float,
    mu: float,
    sigma: float,
    t_years: float
) -> Dict[str, float]:
    """
    Quantifies the exact theoretical volatility drag gap over horizon T:
    - Arithmetic Expected Mean: E[S_T] = S_0 * e^(mu * T)
    - Geometric Median Path:    Median = S_0 * e^((mu - 0.5 * sigma^2) * T)
    - Volatility Drag:          Delta mu = -0.5 * sigma^2
    - Wealth Penalty:           E[S_T] - Median
    """
    if s0 <= 0.0 or sigma < 0.0 or t_years < 0.0:
        raise ValueError("Invalid parameters for volatility drag calculation.")
        
    expected_mean = s0 * math.exp(mu * t_years)
    vol_drag_rate = -0.5 * (sigma ** 2)
    geometric_median = s0 * math.exp((mu + vol_drag_rate) * t_years)
    monetary_drag_penalty = expected_mean - geometric_median
    
    return {
        "expected_mean_wealth": round(expected_mean, 2),
        "typical_median_wealth": round(geometric_median, 2),
        "annual_volatility_drag_rate": round(vol_drag_rate, 5),
        "annual_volatility_drag_percent": round(vol_drag_rate * 100.0, 3),
        "monetary_wealth_gap": round(monetary_drag_penalty, 2),
        "percentage_wealth_penalty": round((monetary_drag_penalty / expected_mean) * 100.0, 2)
    }


def simulate_gbm_paths(
    s0: float,
    mu: float,
    sigma: float,
    t_years: float,
    n_steps: int = 252,
    n_paths: int = 1000,
    seed: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulates M independent Geometric Brownian Motion trajectories using vectorized NumPy.
    
    Discretized via Itô's Lemma:
    ln(S_k) = ln(S_0) + sum_{j=1}^k [ (mu - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * Z_j ]
    
    Parameters:
        s0: Initial asset price or portfolio corpus S_0 > 0.
        mu: Expected continuous annual drift rate (e.g. 0.12 for 12%).
        sigma: Annualized continuous volatility (e.g. 0.20 for 20%).
        t_years: Simulation horizon in years (T > 0).
        n_steps: Time discretization steps (default 252 trading days per year).
        n_paths: Number of simulated trajectories M (default 1,000; up to 10,000+).
        seed: Optional RNG seed for exact academic reproducibility.
        
    Returns:
        time_grid: 1D array of shape (n_steps + 1,)
        paths: 2D array of shape (n_steps + 1, n_paths) where paths[0, :] == s0
    """
    if s0 <= 0.0:
        raise ValueError("Initial asset price S_0 must be strictly positive.")
    if sigma < 0.0:
        raise ValueError("Volatility sigma cannot be negative.")
    if t_years <= 0.0:
        raise ValueError("Time horizon T must be strictly positive.")
    if n_steps < 1 or n_paths < 1:
        raise ValueError("Number of steps and paths must be >= 1.")
        
    if seed is not None:
        np.random.seed(seed)
        
    dt = t_years / n_steps
    time_grid = np.linspace(0.0, t_years, n_steps + 1)
    
    # Generate standard normal variates Z ~ N(0, 1)
    # Shape: (n_steps, n_paths)
    z = np.random.standard_normal((n_steps, n_paths))
    
    # Daily logarithmic increment under Itô's Lemma
    drift_step = (mu - 0.5 * (sigma ** 2)) * dt
    diffusion_step = sigma * math.sqrt(dt) * z
    log_returns = drift_step + diffusion_step
    
    # Cumulative sum of logarithmic returns
    cum_log_returns = np.vstack([np.zeros((1, n_paths)), np.cumsum(log_returns, axis=0)])
    
    # Exponentiate to obtain price paths: S_t = S_0 * exp(cum_returns)
    paths = s0 * np.exp(cum_log_returns)
    
    return time_grid, paths


def goal_attainment_probability(
    terminal_prices: np.ndarray,
    target_goal: float
) -> float:
    """
    Computes empirical probability of reaching or exceeding a financial milestone target:
    P_hat(S_T >= Goal) = (1 / M) * sum 1_{S_{T, m} >= Goal}
    """
    if target_goal <= 0.0:
        return 1.0
    if len(terminal_prices) == 0:
        return 0.0
    return float(np.mean(terminal_prices >= target_goal))


def calculate_value_at_risk(
    terminal_prices: np.ndarray,
    s0: float,
    confidence_level: float = 0.95
) -> Dict[str, float]:
    """
    Computes empirical Value at Risk (VaR) and Conditional VaR (Expected Shortfall):
    - alpha = 1 - confidence_level (e.g. 0.05 for 95%)
    - Cutoff Price = Quantile_alpha(S_T)
    - VaR = max(0, S_0 - Cutoff Price)
    - CVaR = Expected loss in tail where S_T <= Cutoff Price
    """
    if not (0.5 < confidence_level < 1.0):
        raise ValueError("Confidence level must be strictly between 0.5 and 1.0 (e.g., 0.95 or 0.99).")
        
    alpha_pct = (1.0 - confidence_level) * 100.0
    cutoff_price = float(np.percentile(terminal_prices, alpha_pct))
    
    var_amount = max(0.0, s0 - cutoff_price)
    var_pct = (var_amount / s0) * 100.0
    
    # Tail losses for Conditional VaR
    tail_prices = terminal_prices[terminal_prices <= cutoff_price]
    if len(tail_prices) > 0:
        cvar_price = float(np.mean(tail_prices))
        cvar_amount = max(0.0, s0 - cvar_price)
        cvar_pct = (cvar_amount / s0) * 100.0
    else:
        cvar_amount = var_amount
        cvar_pct = var_pct
        
    return {
        "confidence_level": confidence_level,
        "cutoff_price": round(cutoff_price, 2),
        "value_at_risk": round(var_amount, 2),
        "var_percentage": round(var_pct, 2),
        "conditional_var": round(cvar_amount, 2),
        "cvar_percentage": round(cvar_pct, 2)
    }


def compute_simulation_statistics(
    terminal_prices: np.ndarray,
    s0: float
) -> Dict[str, float]:
    """
    Computes empirical statistical summary of the simulated terminal wealth ensemble:
    Mean, Standard Error (CLT), Median, Standard Deviation, Skewness, Min, Max, 5th, 95th Percentiles.
    """
    m = len(terminal_prices)
    mean_val = float(np.mean(terminal_prices))
    std_val = float(np.std(terminal_prices, ddof=1))
    median_val = float(np.median(terminal_prices))
    clt_standard_error = std_val / math.sqrt(m)
    
    return {
        "num_paths": m,
        "sample_mean": round(mean_val, 2),
        "clt_standard_error": round(clt_standard_error, 2),
        "clt_95_ci_lower": round(mean_val - 1.96 * clt_standard_error, 2),
        "clt_95_ci_upper": round(mean_val + 1.96 * clt_standard_error, 2),
        "sample_median": round(median_val, 2),
        "sample_std": round(std_val, 2),
        "p05_worst_case": round(float(np.percentile(terminal_prices, 5)), 2),
        "p25_lower_quartile": round(float(np.percentile(terminal_prices, 25)), 2),
        "p75_upper_quartile": round(float(np.percentile(terminal_prices, 75)), 2),
        "p95_best_case": round(float(np.percentile(terminal_prices, 95)), 2),
        "min_wealth": round(float(np.min(terminal_prices)), 2),
        "max_wealth": round(float(np.max(terminal_prices)), 2)
    }
