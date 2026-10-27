# Save this file inside: backend/taxation_policy.py

class TaxationPolicyEngine:
    """
    ENGINE ARCHITECTURE OVERVIEW:
    ----------------------------
    Calculates the impact of fiscal tax policies on investment portfolios.
    It isolates calculations into discrete methods to support a dual-output UI layout:
    Option A solves for end-of-term flat Capital Gains, while Option B models continuous annual tax drag.
    
    IN-LINE THEORY REFRESHER:
    ------------------------
    Tax Drag reduces the compounding speed of money. Taxing returns annually destroys wealth 
    much faster than taxing profits as a flat lump sum at the very end of the investment lifespan.
    """

    def __init__(self, principal: float, nominal_rate: float, time_years: float, tax_bracket_percentage: float):
        """
        INITIALIZATION & INPUT SANITIZATION PIPELINE
        -------------------------------------------
        :param principal: The initial out-of-pocket investment capital.
        :param nominal_rate: The annual pre-tax growth/interest rate percentage (e.g., 10.0 for 10%).
        :param time_years: Total holding duration of the asset pool in years.
        :param tax_bracket_percentage: The user's applicable income or capital gains tax rate (e.g., 30.0 for 30%).
        """
        try:
            self.principal = float(principal)
            self.rate_decimal = float(nominal_rate) / 100.0
            self.time_years = float(time_years)
            self.tax_rate = float(tax_bracket_percentage) / 100.0
        except (ValueError, TypeError):
            raise ValueError("Data Input Error: Fiscal modeling requires clean numerical entries.")

        # Business Logic Validation (Error Cautioning)
        if self.principal < 0:
            raise ValueError("Asset Error: Investment principal base cannot be negative.")
        if self.rate_decimal < 0:
            raise ValueError("Risk Alert: Nominal interest rate cannot be negative.")
        if self.time_years <= 0:
            raise ValueError("Timeline Error: Financial horizon must be greater than zero years.")
        if not (0.0 <= self.tax_rate <= 0.90):
            raise ValueError("Tax Boundary Error: Tax rate must fall logically between 0% and 90%.")

    def get_flat_capital_gains_payout(self) -> float:
        """
        OUTPUT OPTION A: END-OF-TERM FLAT CAPITAL GAINS TAXATION
        --------------------------------------------------------
        Models an asset that compounds tax-free, with a flat tax levied *only* on profits at the end.
        Formula: Total Pre-Tax Value = P * (1 + r)^t
                 Profit = Pre-Tax Value - P
                 Net Payout = P + (Profit * (1 - Tax Rate))
        """
        # Step 1: Compute standard nominal compounded growth value
        pre_tax_future_value = self.principal * ((1.0 + self.rate_decimal) ** self.time_years)
        
        # Step 2: Isolate the total profit pool
        total_profit = pre_tax_future_value - self.principal
        
        # Step 3: Deduct tax from profit, then reinvest back into original principal base
        post_tax_payout = self.principal + (total_profit * (1.0 - self.tax_rate))
        return round(post_tax_payout, 2)

    def get_annual_tax_drag_balance(self) -> float:
        """
        OUTPUT OPTION B: CONTINUOUS ANNUAL INCOME TAX DRAG
        --------------------------------------------------
        Models an asset where interest is taxed every single year before compounding occurs.
        Formula: Effective Post-Tax Rate = Nominal Rate * (1 - Tax Rate)
                 Post-Tax Balance = P * (1 + Effective Post-Tax Rate)^t
        """
        # Step 1: Reduce the annual rate by the tax clip size right at the start
        effective_post_tax_rate = self.rate_decimal * (1.0 - self.tax_rate)
        
        # Step 2: Compound forward using the heavily degraded effective rate
        post_tax_accumulated_balance = self.principal * ((1.0 + effective_post_tax_rate) ** self.time_years)
        return round(post_tax_accumulated_balance, 2)
