# Save this file inside: backend/future_value.py

class FutureValueCalculator:
    """
    ENGINE ARCHITECTURE OVERVIEW:
    ----------------------------
    This engine computes the future terminal value of a current lump-sum asset today.
    It supports professional investment analysis and retail wealth growth forecasting.
    Outputs are isolated into separate class methods to fit a dual-option UI button layout.
    
    IN-LINE THEORY REFRESHER:
    ------------------------
    Future Value compounds a current asset value forward into a future date.
    Formula: Future Value = Present Value * (1 + (Rate / Freq)) ^ (Freq * Years)
    Compound Wealth Added = Future Value - Present Value Invested
    """

    def __init__(self, present_value: float, annual_growth_rate: float, time_years: float, compound_frequency: int = 1):
        """
        INITIALIZATION & INPUT SANITIZATION PIPELINE
        -------------------------------------------
        Converts text input strings from mobile entry elements into floating-point numbers.
        Applies logic validations to prevent algebraic errors or runtime mobile app crashes.
        
        :param present_value: The starting cash asset value today (PV). Must be non-negative.
        :param annual_growth_rate: Nominal annual growth yield percentage (R) (e.g., 8.5 for 8.5%).
        :param time_years: Investment lifecycle duration in years (T). Must be greater than zero.
        :param compound_frequency: Compounding intervals per annum (N). (e.g., 12=Monthly, 365=Daily).
        """
        # STEP 1: TYPE SANITIZATION
        try:
            self.present_value = float(present_value)
            self.rate_decimal = float(annual_growth_rate) / 100.0
            self.time_years = float(time_years)
            self.compound_frequency = int(compound_frequency)
        except (ValueError, TypeError):
            raise ValueError("Data Input Error: Clean numerical entries are required to calculate Future Value.")

        # STEP 2: BUSINESS LOGIC GUARD RAILS (Error Cautioning)
        if self.present_value < 0:
            raise ValueError("Risk Alert: Starting Present Value asset base cannot be negative.")
            
        if self.rate_decimal < 0:
            raise ValueError("Risk Alert: Growth interest rate metric cannot be negative.")
            
        if self.time_years <= 0:
            raise ValueError("Timeline Error: Investment time horizon must be greater than zero years.")
            
        if self.compound_frequency <= 0:
            raise ValueError("Frequency Error: Annual compounding cycles must be 1 or higher.")

    def get_future_value(self) -> float:
        """
        OUTPUT OPTION A: TOTAL MATURITY BALANCE (FUTURE VALUE)
        -----------------------------------------------------
        Executes exponential compounding to track asset value forward through time.
        Math steps:
        1. Parse the periodic growth factor (Rate / Freq).
        2. Formulate total compounding iterations (Freq * Years).
        3. Multiply Present Value by the compounded interest factor.
        """
        periodic_rate = self.rate_decimal / self.compound_frequency
        total_periods = self.compound_frequency * self.time_years
        
        # Future Value Equation: FV = PV * (1 + r/n)^(n*t)
        calculated_fv = self.present_value * ((1.0 + periodic_rate) ** total_periods)
        
        return round(calculated_fv, 2)

    def get_wealth_added_only(self) -> float:
        """
        OUTPUT OPTION B: PURE COMPOUND WEALTH GENERATED
        ----------------------------------------------
        Isolates the net growth revenue by removing the starting present asset base.
        Formula: Wealth Added = Calculated Future Value - Initial Present Value
        """
        total_fv = self.get_future_value()
        net_wealth_gained = total_fv - self.present_value
        
        return round(net_wealth_gained, 2)
