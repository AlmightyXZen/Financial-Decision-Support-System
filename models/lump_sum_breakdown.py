# Save this file inside: backend/lump_sum_breakdown.py

class AssetVelocityCalculator:
    """
    ENGINE ARCHITECTURE OVERVIEW:
    ----------------------------
    Solves user wealth questions regarding compounding timeline horizons.
    Uses log structures to provide exact timelines alongside rule-based shortcuts.
    """

    def __init__(self, annual_interest_rate: float):
        """
        :param annual_interest_rate: The constant interest/yield rate percentage (e.g., 8.0 for 8%).
        """
        try:
            self.rate = float(annual_interest_rate)
        except (ValueError, TypeError):
            raise ValueError("Input Error: Rate entry must be a valid number.")

        if self.rate <= 0:
            raise ValueError("Rate Error: Growth interest rate must be greater than zero.")

    def get_years_to_double(self) -> float:
        """
        OUTPUT OPTION A: EXACT YEARS REQUIRED TO DOUBLE FUNDS
        ----------------------------------------------------
        Calculates the time to double capital using precise logarithmic progression.
        """
        import math
        rate_decimal = self.rate / 100.0
        # Precise Math: t = ln(2) / ln(1 + r)
        exact_years = math.log(2.0) / math.log(1.0 + rate_decimal)
        return round(exact_years, 2)

    def get_rule_of_72_approximation(self) -> float:
        """
        OUTPUT OPTION B: RULE OF 72 SHORTCUT DISPLAY
        --------------------------------------------
        Provides the classic financial rule-of-thumb estimate.
        """
        return round(72.0 / self.rate, 2)
