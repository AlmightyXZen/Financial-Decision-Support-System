# Save this file inside: backend/present_value.py

class PresentValueCalculator:
    """
    ENGINE ARCHITECTURE OVERVIEW:
    ----------------------------
    This engine computes the present worth of a future financial target. It is built 
    to accommodate professional valuation analysis and consumer goal planning.
    Outputs are split cleanly into two individual methods to accommodate a 
    dual-option UI button display.
    
    IN-LINE THEORY REFRESHER:
    ------------------------
    Discounting shifts future values back to the current day. 
    Formula: Present Value = Future Value / (1 + (Rate / Freq)) ^ (Freq * Years)
    Discount Interest Gap = Future Target Value - Present Value Required
    """

    def __init__(self, future_value: float, annual_discount_rate: float, time_years: float, compound_frequency: int = 1):
        """
        INITIALIZATION & INPUT SANITIZATION PIPELINE
        -------------------------------------------
        Converts interface textual inputs into clean numbers and enforces financial 
        boundaries to ensure the production APK does not experience system exceptions.
        
        :param future_value: The target future sum of money desired (FV). Must be positive.
        :param annual_discount_rate: The annual return/discount rate as a percentage (R) (e.g., 10 for 10%).
        :param time_years: Time horizon until the goal is reached in years (T). Must be above zero.
        :param compound_frequency: Number of compounding periods per year (N). (e.g., 1=Annual, 4=Quarterly).
        """
        # STEP 1: TYPE SANITIZATION
        try:
            self.future_value = float(future_value)
            self.rate_decimal = float(annual_discount_rate) / 100.0
            self.time_years = float(time_years)
            self.compound_frequency = int(compound_frequency)
        except (ValueError, TypeError):
            raise ValueError("Data Input Error: Numerical entries are required to calculate Present Value.")

        # STEP 2: BUSINESS LOGIC GUARD RAILS (Error Cautioning)
        if self.future_value <= 0:
            raise ValueError("Target Error: Future target amount must be greater than zero.")
            
        if self.rate_decimal < 0:
            raise ValueError("Risk Alert: Discount/return rate cannot be negative.")
            
        if self.time_years <= 0:
            raise ValueError("Timeline Error: Investment time horizon must be greater than zero years.")
            
        if self.compound_frequency <= 0:
            raise ValueError("Frequency Error: Annual compounding cycles must be 1 or higher.")

    def get_present_value(self) -> float:
        """
        OUTPUT OPTION A: REQUIRED STARTING PRINCIPAL (PRESENT VALUE)
        -----------------------------------------------------------
        Executes the discounting operation to find the money needed today.
        Math steps:
        1. Determine the periodic fractional rate (Rate / Freq).
        2. Determine total compounding intervals (Freq * Years).
        3. Divide Future Value by the compounded growth factor.
        """
        periodic_rate = self.rate_decimal / self.compound_frequency
        total_periods = self.compound_frequency * self.time_years
        
        # Present Value Discounting Equation: PV = FV / (1 + r/n)^(n*t)
        calculated_pv = self.future_value / ((1.0 + periodic_rate) ** total_periods)
        
        return round(calculated_pv, 2)

    def get_discount_interest_gap(self) -> float:
        """
        OUTPUT OPTION B: TOTAL INVESTMENT GROWTH CONTRIBUTION
        -----------------------------------------------------
        Calculates how much money is generated strictly by interest compounding. 
        This shows the user how much money they *save* by starting today.
        Formula: Interest Contribution = Future Target - Initial Capital Needed
        """
        required_pv = self.get_present_value()
        growth_contribution = self.future_value - required_pv
        
        return round(growth_contribution, 2)
