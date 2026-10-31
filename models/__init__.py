"""
Package: models
Financial Decision Support System (FDSS) - Mathematical Computation Engines.
"""

from .time_value import (
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

from .loans_and_credit import (
    calculate_emi,
    check_negative_amortization,
    generate_amortization_schedule,
    calculate_prepayment_savings
)

from .investment_plans import (
    calculate_sip_wealth,
    calculate_step_up_sip,
    real_rate_of_return,
    purchasing_power_erosion,
    purchasing_power_half_life
)

from .capital_budgeting import (
    net_present_value,
    npv_first_derivative,
    internal_rate_of_return,
    internal_rate_of_return_with_history,
    discounted_payback_period
)

from .monte_carlo import (
    calculate_volatility_drag,
    simulate_gbm_paths,
    goal_attainment_probability,
    calculate_value_at_risk,
    compute_simulation_statistics
)

__all__ = [
    # Time Value
    "simple_interest",
    "simple_interest_amount",
    "compound_interest_amount",
    "accrued_compound_interest",
    "continuous_compounding_amount",
    "discrete_to_continuous_yield",
    "continuous_to_discrete_yield",
    "present_value",
    "future_value",
    "nominal_to_effective_rate",
    "effective_to_nominal_rate",
    # Loans & Debt
    "calculate_emi",
    "check_negative_amortization",
    "generate_amortization_schedule",
    "calculate_prepayment_savings",
    # Investments & Inflation
    "calculate_sip_wealth",
    "calculate_step_up_sip",
    "real_rate_of_return",
    "purchasing_power_erosion",
    "purchasing_power_half_life",
    # Capital Budgeting
    "net_present_value",
    "npv_first_derivative",
    "internal_rate_of_return",
    "internal_rate_of_return_with_history",
    "discounted_payback_period",
    # Monte Carlo & Risk
    "calculate_volatility_drag",
    "simulate_gbm_paths",
    "goal_attainment_probability",
    "calculate_value_at_risk",
    "compute_simulation_statistics"
]
