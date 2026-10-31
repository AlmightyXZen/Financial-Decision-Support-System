"""
Module: models/time_value.py
Theoretical Foundation: Chapters 01, 02, 03, 04, and 05 of FDSS Monograph.

Covers:
1. Simple Interest (Linear ODE: dA/dt = P * r)
2. Compound Interest (Discrete Geometric Accumulation: A = P * (1 + r/m)^(mt))
3. Continuous Compounding (Autonomous Linear ODE: dA/dt = r * A(t) => A = P * e^(rt))
4. Temporal Equivalence & Discounting (Present Value & Future Value)
5. Yield Standardization (Nominal APR vs. Effective Annual Rate EAR)

Strict Engineering Standards:
- Zero external opaque black boxes (pure first-principles mathematics).
- Input domain validation with descriptive ValueError exceptions.
- Floating-point boundary handling (r = 0, t = 0, high m).
"""

import math
from typing import Union


def _validate_non_negative(val: float, name: str) -> None:
    """Helper to enforce domain non-negativity."""
    if val < 0.0:
        raise ValueError(f"Domain error: '{name}' must be non-negative (received {val}).")


# ==============================================================================
# 1. SIMPLE INTEREST & LINEAR ACCUMULATION (Chapter 01)
# ==============================================================================

def simple_interest(principal: float, annual_rate: float, time_years: float) -> float:
    """
    Computes accrued simple interest: I = P * r * t.
    
    Axiom: Interest accrues strictly on the invariant initial principal P.
    Governing ODE: dA/dt = P * r, A(0) = P.
    
    Parameters:
        principal: Initial capital committed (P >= 0).
        annual_rate: Annual nominal interest rate expressed as a decimal (r >= 0).
        time_years: Duration in years (t >= 0).
        
    Returns:
        Accrued simple interest (float).
    """
    _validate_non_negative(principal, "principal")
    _validate_non_negative(annual_rate, "annual_rate")
    _validate_non_negative(time_years, "time_years")
    
    return float(principal * annual_rate * time_years)


def simple_interest_amount(principal: float, annual_rate: float, time_years: float) -> float:
    """
    Computes terminal wealth under simple interest: A = P * (1 + r * t).
    
    Note: Simple interest violates temporal subadditivity:
    A(t1 + t2) < A(t1) * A(t2) / P for all r > 0, t1, t2 > 0.
    """
    return float(principal + simple_interest(principal, annual_rate, time_years))


# ==============================================================================
# 2. DISCRETE COMPOUND INTEREST (Chapter 02)
# ==============================================================================

def compound_interest_amount(
    principal: float,
    annual_rate: float,
    time_years: float,
    compounding_frequency: int = 1,
    m: Optional[int] = None
) -> float:
    """
    Computes terminal accumulated wealth under discrete compound interest:
    A = P * (1 + r / m)^(m * t)
    
    Parameters:
        principal: Initial capital (P >= 0).
        annual_rate: Nominal annual interest rate as a decimal (r >= 0).
        time_years: Investment horizon in years (t >= 0).
        compounding_frequency: Compounding periods per year m >= 1 (1=Annual, 4=Quarterly, 12=Monthly, 365=Daily).
        m: Optional shorthand alias for compounding_frequency.
        
    Returns:
        Terminal accumulated wealth (float).
    """
    if m is not None:
        compounding_frequency = m

    _validate_non_negative(principal, "principal")
    _validate_non_negative(annual_rate, "annual_rate")
    _validate_non_negative(time_years, "time_years")
    if compounding_frequency < 1:
        raise ValueError(f"Compounding frequency 'm' must be an integer >= 1 (received {compounding_frequency}).")
    
    if principal == 0.0 or time_years == 0.0:
        return float(principal)
    if annual_rate == 0.0:
        return float(principal)
    
    # Use math.pow for IEEE 754 precision
    rate_per_period = annual_rate / compounding_frequency
    total_periods = compounding_frequency * time_years
    
    # When rate_per_period is extremely small, use math.log1p and math.exp to avoid catastrophic cancellation
    if rate_per_period < 1e-7:
        growth_factor = math.exp(total_periods * math.log1p(rate_per_period))
    else:
        growth_factor = math.pow(1.0 + rate_per_period, total_periods)
        
    return float(principal * growth_factor)


def accrued_compound_interest(
    principal: float,
    annual_rate: float,
    time_years: float,
    compounding_frequency: int = 1,
    m: Optional[int] = None
) -> float:
    """
    Computes total accrued compound interest: I_comp = A(t) - P.
    """
    if m is not None:
        compounding_frequency = m
    terminal_wealth = compound_interest_amount(principal, annual_rate, time_years, compounding_frequency)
    return float(terminal_wealth - principal)


# ==============================================================================
# 3. CONTINUOUS COMPOUNDING & INFINITESIMAL CALCULUS (Chapter 03)
# ==============================================================================

def continuous_compounding_amount(
    principal: float,
    annual_rate: float,
    time_years: float
) -> float:
    """
    Computes terminal wealth under continuous compounding:
    A(t) = P * e^(r * t)
    
    Governing Autonomous ODE: dA/dt = r * A(t), A(0) = P.
    Euler Limit: lim_{m -> inf} P * (1 + r/m)^(mt) = P * e^(rt).
    """
    _validate_non_negative(principal, "principal")
    _validate_non_negative(annual_rate, "annual_rate")
    _validate_non_negative(time_years, "time_years")
    
    if principal == 0.0 or time_years == 0.0 or annual_rate == 0.0:
        return float(principal)
        
    return float(principal * math.exp(annual_rate * time_years))


def discrete_to_continuous_yield(discrete_rate: float, compounding_frequency: int) -> float:
    """
    Converts a discrete nominal yield into an equivalent continuous yield:
    r_c = m * ln(1 + r_d / m)
    
    Ensures: e^(r_c) = (1 + r_d / m)^m
    """
    _validate_non_negative(discrete_rate, "discrete_rate")
    if compounding_frequency < 1:
        raise ValueError("Compounding frequency must be >= 1.")
    if discrete_rate == 0.0:
        return 0.0
        
    return float(compounding_frequency * math.log1p(discrete_rate / compounding_frequency))


def continuous_to_discrete_yield(continuous_rate: float, compounding_frequency: int) -> float:
    """
    Converts a continuous yield into an equivalent discrete nominal yield:
    r_d = m * (e^(r_c / m) - 1)
    """
    _validate_non_negative(continuous_rate, "continuous_rate")
    if compounding_frequency < 1:
        raise ValueError("Compounding frequency must be >= 1.")
    if continuous_rate == 0.0:
        return 0.0
        
    return float(compounding_frequency * math.expm1(continuous_rate / compounding_frequency))


# ==============================================================================
# 4. TEMPORAL FINANCIAL EQUIVALENCE: PV & FV (Chapter 04)
# ==============================================================================

def present_value(
    future_value: float,
    annual_rate: float,
    time_years: float,
    compounding_frequency: int = 1,
    continuous: bool = False,
    m: Optional[int] = None
) -> float:
    """
    Discounts a future cash flow back to present value today:
    Discrete:   PV = FV * (1 + r/m)^(-mt)
    Continuous: PV = FV * e^(-rt)
    
    Stochastic Discount Factor v(t) satisfies: lim_{t -> inf} v(t) = 0 for r > 0.
    """
    if m is not None:
        compounding_frequency = m
    _validate_non_negative(future_value, "future_value")
    _validate_non_negative(annual_rate, "annual_rate")
    _validate_non_negative(time_years, "time_years")
    
    if future_value == 0.0:
        return 0.0
    if annual_rate == 0.0 or time_years == 0.0:
        return float(future_value)
        
    if continuous:
        discount_factor = math.exp(-annual_rate * time_years)
    else:
        if compounding_frequency < 1:
            raise ValueError("Compounding frequency must be >= 1.")
        rate_per_period = annual_rate / compounding_frequency
        total_periods = compounding_frequency * time_years
        discount_factor = math.pow(1.0 + rate_per_period, -total_periods)
        
    return float(future_value * discount_factor)


def future_value(
    present_val: float,
    annual_rate: float,
    time_years: float,
    compounding_frequency: int = 1,
    continuous: bool = False,
    m: Optional[int] = None
) -> float:
    """
    Compounds a present cash flow forward into future value:
    Discrete:   FV = PV * (1 + r/m)^(mt)
    Continuous: FV = PV * e^(rt)
    """
    if m is not None:
        compounding_frequency = m
    if continuous:
        return continuous_compounding_amount(present_val, annual_rate, time_years)
    return compound_interest_amount(present_val, annual_rate, time_years, compounding_frequency)


# ==============================================================================
# 5. NOMINAL VS. EFFECTIVE ANNUAL RATE (EAR / APY) (Chapter 05)
# ==============================================================================

def nominal_to_effective_rate(
    nominal_rate: float,
    compounding_frequency: int = 1,
    continuous: bool = False,
    m: Optional[int] = None
) -> float:
    """
    Converts nominal APR into Effective Annual Rate (EAR / APY):
    Discrete:   EAR = (1 + r_nom / m)^m - 1
    Continuous: EAR = e^(r_nom) - 1
    
    Exposes the retail 'APR Illusion' by incorporating intra-year compounding.
    """
    if m is not None:
        compounding_frequency = m
    _validate_non_negative(nominal_rate, "nominal_rate")
    if nominal_rate == 0.0:
        return 0.0
        
    if continuous:
        return float(math.expm1(nominal_rate))
    
    if compounding_frequency < 1:
        raise ValueError("Compounding frequency must be >= 1.")
    if compounding_frequency == 1:
        return float(nominal_rate)
        
    rate_per_period = nominal_rate / compounding_frequency
    return float(math.pow(1.0 + rate_per_period, compounding_frequency) - 1.0)


def effective_to_nominal_rate(
    effective_rate: float,
    compounding_frequency: int = 1,
    continuous: bool = False
) -> float:
    """
    Inverts EAR back to nominal APR for frequency m:
    Discrete:   r_nom = m * [ (1 + EAR)^(1/m) - 1 ]
    Continuous: r_nom = ln(1 + EAR)
    """
    _validate_non_negative(effective_rate, "effective_rate")
    if effective_rate == 0.0:
        return 0.0
        
    if continuous:
        return float(math.log1p(effective_rate))
        
    if compounding_frequency < 1:
        raise ValueError("Compounding frequency must be >= 1.")
    if compounding_frequency == 1:
        return float(effective_rate)
        
    return float(compounding_frequency * (math.pow(1.0 + effective_rate, 1.0 / compounding_frequency) - 1.0))
