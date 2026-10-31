"""
Module: models/capital_budgeting.py
Theoretical Foundation: Chapters 09 (NPV) & 10 (IRR & The Abel-Ruffini Theorem) of FDSS Monograph.

Covers:
1. Multi-Period Net Present Value (NPV):
   NPV(r) = sum_{t=0}^T C_t / (1 + r)^t
2. Internal Rate of Return (IRR) Root-Finding:
   By the Abel-Ruffini Theorem (Galois Theory), general polynomials of degree T >= 5 
   have NO algebraic radical solutions. Hence, calculating financial yield mathematically mandates
   numerical analysis.
3. Dual-Engine Numerical Root Solver:
   - Primary: Newton-Raphson iteration using analytical first derivative f'(r) with quadratic convergence.
   - Robustness Fallback: Bisection Method on bracket [a, b] guaranteeing convergence if derivatives vanish or oscillate.
4. Discounted Payback Period & Profitability Index (PI).
"""

import math
from typing import List, Optional, Tuple, Dict, Any


def net_present_value(discount_rate: float, cash_flows: List[float]) -> float:
    """
    Computes Net Present Value (NPV) across multi-period cash flows:
    NPV(r) = sum_{t=0}^T C_t / (1 + r)^t
    
    Parameters:
        discount_rate: Hurdle rate / cost of capital r > -1.0.
        cash_flows: Sequence [C_0, C_1, ..., C_T] where C_0 is typically initial capital outflow (< 0).
    """
    if discount_rate <= -1.0:
        raise ValueError("Discount rate must be strictly greater than -100%.")
    if not cash_flows:
        return 0.0
        
    npv = 0.0
    for t, cf in enumerate(cash_flows):
        npv += cf / math.pow(1.0 + discount_rate, t)
    return float(npv)


def npv_first_derivative(discount_rate: float, cash_flows: List[float]) -> float:
    """
    Analytical first derivative of NPV with respect to discount rate r:
    f'(r) = - sum_{t=1}^T [ t * C_t / (1 + r)^(t + 1) ]
    
    Used by Newton-Raphson to achieve quadratic convergence without finite-difference errors.
    """
    if discount_rate <= -1.0:
        raise ValueError("Discount rate must be strictly greater than -100%.")
    if len(cash_flows) <= 1:
        return 0.0
        
    deriv = 0.0
    for t in range(1, len(cash_flows)):
        cf = cash_flows[t]
        deriv -= (t * cf) / math.pow(1.0 + discount_rate, t + 1)
    return float(deriv)


def _bisection_irr_fallback(
    cash_flows: List[float],
    low: float = -0.99,
    high: float = 10.0,
    tol: float = 1e-7,
    max_iter: int = 150
) -> float:
    """
    Interval halving (Bisection Method) fallback when Newton-Raphson diverges or encounters f'(r) ~ 0.
    Guaranteed linear convergence if f(low) * f(high) < 0.
    """
    f_low = net_present_value(low, cash_flows)
    f_high = net_present_value(high, cash_flows)
    
    if f_low * f_high > 0.0:
        # Dynamically scan for bracket sign change
        bracket_found = False
        scan_rates = [-0.9, -0.5, 0.0, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
        for i in range(len(scan_rates) - 1):
            r1, r2 = scan_rates[i], scan_rates[i+1]
            if net_present_value(r1, cash_flows) * net_present_value(r2, cash_flows) <= 0.0:
                low, high = r1, r2
                bracket_found = True
                break
        if not bracket_found:
            raise ValueError("Bisection failed: No real IRR root exists within searched parameter bounds.")
            
    for _ in range(max_iter):
        mid = 0.5 * (low + high)
        f_mid = net_present_value(mid, cash_flows)
        
        if abs(f_mid) <= tol or (high - low) * 0.5 <= tol:
            return float(mid)
            
        if f_low * f_mid < 0.0:
            high = mid
            f_high = f_mid
        else:
            low = mid
            f_low = f_mid
            
    return float(0.5 * (low + high))


def internal_rate_of_return(
    cash_flows: List[float],
    initial_guess: float = 0.1,
    max_iter: int = 100,
    tol: float = 1e-7
) -> float:
    """
    Calculates Internal Rate of Return (IRR) solving NPV(r) = 0.
    
    Implements Newton-Raphson iteration:
    r_{k+1} = r_k - NPV(r_k) / f'(r_k)
    with automatic Bisection fallback for pathological/multiple-sign cash flows.
    """
    if len(cash_flows) < 2:
        raise ValueError("IRR requires at least two cash flow periods (initial outlay and return).")
    
    # Check if all cash flows have the same sign (no IRR possible)
    has_positive = any(cf > 0 for cf in cash_flows)
    has_negative = any(cf < 0 for cf in cash_flows)
    if not (has_positive and has_negative):
        raise ValueError("Cash flows must contain both positive inflows and negative outflows to define IRR.")
        
    r = initial_guess
    
    for _ in range(max_iter):
        npv_val = net_present_value(r, cash_flows)
        if abs(npv_val) <= tol:
            return float(r)
            
        deriv = npv_first_derivative(r, cash_flows)
        
        # Derivative near singularity or divergence check
        if abs(deriv) < 1e-12 or r <= -0.999 or r > 50.0:
            return _bisection_irr_fallback(cash_flows, tol=tol)
            
        r_next = r - (npv_val / deriv)
        
        if abs(r_next - r) <= tol:
            return float(r_next)
            
        r = r_next
        
    # If Newton did not converge within max_iter, fallback to bisection
    return _bisection_irr_fallback(cash_flows, tol=tol)


def internal_rate_of_return_with_history(
    cash_flows: List[float],
    initial_guess: float = 0.1,
    max_iter: int = 50,
    tol: float = 1e-7
) -> Tuple[float, List[Dict[str, Any]]]:
    """
    Computes IRR while tracking the full numerical trajectory of the solver.
    Returns:
        (irr, history_records)
    where each step in history_records contains:
        iteration, r_k, npv_k, deriv_k, delta_r, method
    """
    if len(cash_flows) < 2:
        raise ValueError("IRR requires at least two cash flow periods.")
    
    has_positive = any(cf > 0 for cf in cash_flows)
    has_negative = any(cf < 0 for cf in cash_flows)
    if not (has_positive and has_negative):
        raise ValueError("Cash flows must contain both positive inflows and negative outflows.")
        
    history: List[Dict[str, Any]] = []
    r = initial_guess
    
    for k in range(max_iter):
        npv_val = net_present_value(r, cash_flows)
        deriv = npv_first_derivative(r, cash_flows)
        
        step_record = {
            "iteration": k + 1,
            "r_k": float(r),
            "npv_k": float(npv_val),
            "deriv_k": float(deriv),
            "method": "Newton-Raphson"
        }
        
        if abs(npv_val) <= tol:
            step_record["delta_r"] = 0.0
            history.append(step_record)
            return float(r), history
            
        if abs(deriv) < 1e-12 or r <= -0.999 or r > 50.0:
            # Fallback to Bisection
            step_record["delta_r"] = None
            step_record["method"] = "Switching to Bisection fallback"
            history.append(step_record)
            irr_fallback = _bisection_irr_fallback(cash_flows, tol=tol)
            history.append({
                "iteration": k + 2,
                "r_k": float(irr_fallback),
                "npv_k": float(net_present_value(irr_fallback, cash_flows)),
                "deriv_k": float(npv_first_derivative(irr_fallback, cash_flows)),
                "delta_r": 0.0,
                "method": "Bisection Converged"
            })
            return float(irr_fallback), history
            
        delta_r = -(npv_val / deriv)
        step_record["delta_r"] = float(delta_r)
        history.append(step_record)
        
        r_next = r + delta_r
        if abs(r_next - r) <= tol:
            history.append({
                "iteration": k + 2,
                "r_k": float(r_next),
                "npv_k": float(net_present_value(r_next, cash_flows)),
                "deriv_k": float(npv_first_derivative(r_next, cash_flows)),
                "delta_r": 0.0,
                "method": "Newton-Raphson Converged"
            })
            return float(r_next), history
            
        r = r_next
        
    irr_fallback = _bisection_irr_fallback(cash_flows, tol=tol)
    history.append({
        "iteration": len(history) + 1,
        "r_k": float(irr_fallback),
        "npv_k": float(net_present_value(irr_fallback, cash_flows)),
        "deriv_k": float(npv_first_derivative(irr_fallback, cash_flows)),
        "delta_r": 0.0,
        "method": "Bisection Converged"
    })
    return float(irr_fallback), history


def discounted_payback_period(
    discount_rate: float,
    cash_flows: List[float]
) -> Optional[float]:
    """
    Computes exact fractional time (in periods) when cumulative discounted cash flows break even.
    Returns None if project never pays back.
    """
    if discount_rate <= -1.0 or not cash_flows or cash_flows[0] >= 0:
        return None
        
    cum_npv = 0.0
    for t, cf in enumerate(cash_flows):
        pv_cf = cf / math.pow(1.0 + discount_rate, t)
        prev_cum = cum_npv
        cum_npv += pv_cf
        
        if t > 0 and cum_npv >= 0.0:
            # Linear interpolation for fractional year
            fraction = abs(prev_cum) / pv_cf
            return float((t - 1) + fraction)
            
    return None
