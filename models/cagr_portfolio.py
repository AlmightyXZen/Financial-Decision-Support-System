# Save this file inside: backend/cagr_portfolio.py

class AdvancedInvestmentMetrics:
    """
    ENGINE ARCHITECTURE OVERVIEW:
    ----------------------------
    Calculates historical compound growth performance metrics and velocity targets
    for high-net-worth investors and everyday consumer portfolio analysis.
    Outputs are isolated into discrete methods to feed multi-button UI cards.
    """

    def __init__(self, beginning_value: float, ending_value: float, time_years: float):
        """
        INITIALIZATION & DATA VALIDATION PIPELINE
        -----------------------------------------
        :param beginning_value: Initial cost basis or acquisition price of the asset.
        :param ending_value: Current market value or final sale price of the asset.
        :param time_years: The exact length of the holding period timeline in years.
        """
        try:
            self.start_val = float(beginning_value)
            self.end_val = float(ending_value)
            self.years = float(time_years)
        except (ValueError, TypeError):
            raise ValueError("Data Input Error: Valuation metrics require clean numerical entries.")

        # Business Logic Validation (Error Cautioning)
        if self.start_val <= 0 or self.end_val <= 0:
            raise ValueError("Valuation Error: Asset values must be positive non-zero numbers.")
            
        if self.years <= 0:
            raise ValueError("Timeline Error: Holding duration must be greater than zero years.")

    def get_cagr_percentage(self) -> float:
        """
        OUTPUT OPTION A: SMOOTHED COMPOUND ANNUAL GROWTH RATE
        ----------------------------------------------------
        Calculates the exact geometric annualized growth rate of the asset.
        Formula: CAGR = (End / Start) ^ (1 / Years) - 1
        """
        # Geometric growth formula calculation step
        cagr_decimal = (self.end_val / self.start_val) ** (1.0 / self.years) - 1.0
        return round(cagr_decimal * 100.0, 2)

    def get_absolute_roi_percentage(self) -> float:
        """
        OUTPUT OPTION B: TOTAL ABSOLUTE RETURN ON INVESTMENT (ROI)
        ---------------------------------------------------------
        Calculates the raw, un-smoothed total percentage gain over the entire timeline.
        Formula: ROI = ((End - Start) / Start) * 100
        """
        raw_gain = self.end_val - self.start_val
        roi_decimal = raw_gain / self.start_val
        return round(roi_decimal * 100.0, 2)
