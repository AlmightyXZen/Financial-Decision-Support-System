# Save this file inside: backend/capital_budgeting.py

class CapitalBudgetingEngine:
    """
    ENGINE ARCHITECTURE OVERVIEW:
    ----------------------------
    Processes non-uniform cash flow arrays to calculate capital viability metrics.
    Uses an internal custom implementation of the Newton-Raphson math model to approximate
    Internal Rate of Return without relying on massive framework dependencies.

    IN-LINE THEORY REFRESHER:
    ------------------------
    NPV maps multi-year cash segments back to Year 0 using a discount rate hurdle.
    IRR solves for the specific discount hurdle rate that forces NPV to equal zero.
    """

    def __init__(self, initial_investment: float, cash_flows: list, discount_rate: float):
        """
        INITIALIZATION & INPUT SANITIZATION PIPELINE
        -------------------------------------------
        :param initial_investment: Upfront Year 0 cash outlay. Input as a positive absolute float.
        :param cash_flows: A Python list of floats representing net collections per period (Year 1, 2, 3...).
        :param discount_rate: The annual hurdle cost of capital (WACC) as a percentage (e.g., 8.5 for 8.5%).
        """
        try:
            self.initial_outlay = float(abs(initial_investment))
            self.cash_flows = [float(cf) for cf in cash_flows]
            self.hurdle_rate = float(discount_rate) / 100.0
        except (ValueError, TypeError):
            raise ValueError("Data Input Error: Capital budgeting requires clear numerical cash arrays.")

        if self.hurdle_rate < -0.99:
            raise ValueError("Risk Alert: Rate constraint limits breached.")
        if not self.cash_flows:
            raise ValueError("Data Structure Error: Cash flow sequence array cannot be empty.")

    def get_net_present_value(self, optional_custom_rate: float = None) -> float:
        """
        OUTPUT OPTION A: NET PRESENT VALUE (NPV)
        ----------------------------------------
        Discounts each periodic segment. Year 0 investment is treated as a native negative outflow.
        """
        rate = self.hurdle_rate if optional_custom_rate is None else optional_custom_rate
        
        # Start with the initial negative investment outflow at Year 0
        npv = -self.initial_outlay
        
        # Dynamically loop and compound discount future cash flows down the timeline array
        for year_index, cash_flow in enumerate(self.cash_flows, start=1):
            npv += cash_flow / ((1.0 + rate) ** year_index)
            
        return round(npv, 2)

    def get_internal_rate_of_return(self) -> float:
        """
        OUTPUT OPTION B: INTERNAL RATE OF RETURN (IRR)
        ----------------------------------------------
        Applies a Newton-Raphson iteration framework to find the exact zero root of the NPV equation.
        """
        # Initial guess baseline rate setup (10% standard financial seed value)
        current_guess = 0.10
        tolerance = 1e-6
        max_iterations = 100

        for _ in range(max_iterations):
            npv_value = -self.initial_outlay
            derivative_value = 0.0

            # Compute NPV and its derivative value simultaneously for current guess rate
            for year_index, cash_flow in enumerate(self.cash_flows, start=1):
                discount_factor = (1.0 + current_guess) ** year_index
                npv_value += cash_flow / discount_factor
                
                # Derivative of CF / (1+r)^t with respect to r is: -t * CF / (1+r)^(t+1)
                derivative_value -= (year_index * cash_flow) / (discount_factor * (1.0 + current_guess))

            # Guard loop mechanism against zero math division crashes if derivative hits flat baseline
            if derivative_value == 0:
                break

            # Newton-Raphson standard correction stepping: x_new = x - f(x)/f'(x)
            next_guess = current_guess - (npv_value / derivative_value)

            # Check if calculation variation convergence meets tolerance criteria
            if abs(next_guess - current_guess) < tolerance:
                # Convert back to standard percentage format and filter out illogical extreme bounds
                irr_percentage = round(next_guess * 100.0, 2)
                if irr_percentage < -100:
                    raise ValueError("Math Limit: Project cash flows do not converge to a logical positive IRR.")
                return irr_percentage

            current_guess = next_guess

        raise ValueError("Convergence Error: Complex cash fluctuations prevent stable IRR approximation.")

    def get_profitability_index(self) -> float:
        """
        OUTPUT OPTION C: PROFITABILITY INDEX (PI)
        -----------------------------------------
        Measures the absolute efficiency ratio of value creation per unit of dollar investment currency.
        Formula: Present Value of Inflows / Initial Outlay
        """
        present_value_inflows = self.get_net_present_value() + self.initial_outlay
        if self.initial_outlay == 0:
            return 0.0
        return round(present_value_inflows / self.initial_outlay, 2)
