# Save this file inside: backend/inflation_adjusted.py

class InflationAdjuster:
    """
    ENGINE ARCHITECTURE OVERVIEW:
    ----------------------------
    This engine adjusts nominal financial projections to reflect true macroeconomic reality.
    It isolates calculations into discrete methods to fit a dual-option UI choice layout:
    Option A delivers the true purchasing power of a future sum, while Option B calculates
    the exact cost increase needed to sustain a lifestyle baseline.

    IN-LINE THEORY REFRESHER:
    ------------------------
    Inflation compounds negatively against purchasing power. To find the real value of future cash,
    the nominal sum must be discounted backward using the inflation rate.
    Fisher Real Rate Formula: Real Return = ((1 + Nominal Rate) / (1 + Inflation Rate)) - 1
    """

    def __init__(self, nominal_amount: float, annual_inflation_rate: float, time_years: float):
        """
        INITIALIZATION & INPUT SANITIZATION PIPELINE
        -------------------------------------------
        Converts textual entries from mobile inputs into pristine float primitives.
        Guards against negative time horizons and extreme anomalies to secure the compiled APK.
        
        :param nominal_amount: The target future sum of money or current asset base.
        :param annual_inflation_rate: Estimated average annual inflation percentage (e.g., 5.0 for 5%).
        :param time_years: Time horizon for the analysis in years. Must be greater than zero.
        """
        # STEP 1: TYPE SANITIZATION
        try:
            self.nominal_amount = float(nominal_amount)
            self.inflation_decimal = float(annual_inflation_rate) / 100.0
            self.time_years = float(time_years)
        except (ValueError, TypeError):
            raise ValueError("Data Input Error: Clean numerical metrics are required for inflation modeling.")

        # STEP 2: BUSINESS LOGIC GUARD RAILS (Error Cautioning)
        if self.nominal_amount < 0:
            raise ValueError("Asset Error: Financial nominal base cannot be negative.")
            
        if self.inflation_decimal < -0.50:  # Enforces a realistic boundary even for hyper-deflation
            raise ValueError("Risk Alert: Extreme deflation bounds exceeded.")
            
        if self.time_years <= 0:
            raise ValueError("Timeline Error: Economic time horizon must be greater than zero years.")

    def get_adjusted_purchasing_power(self) -> float:
        """
        OUTPUT OPTION A: REAL PURCHASING POWER OF A FUTURE SUM
        ------------------------------------------------------
        Determines what a future nominal cash payout (like a insurance maturity or fixed fund) 
        will actually buy in terms of today's money.
        Formula: Real Value = Nominal Amount / (1 + Inflation Rate) ^ Years
        """
        demised_value = self.nominal_amount / ((1.0 + self.inflation_decimal) ** self.time_years)
        return round(demised_value, 2)

    def get_future_cost_of_living(self) -> float:
        """
        OUTPUT OPTION B: FUTURE NOMINAL COST OF TODAY'S BASKET
        ------------------------------------------------------
        Calculates how much a basket of goods costing 'nominal_amount' today will cost in the 
        future due to price inflation. Helps users adjust their milestone targets.
        Formula: Future Nominal Cost = Current Cost * (1 + Inflation Rate) ^ Years
        """
        inflated_cost = self.nominal_amount * ((1.0 + self.inflation_decimal) ** self.time_years)
        return round(inflated_cost, 2)

    @staticmethod
    def calculate_real_yield(nominal_return_rate: float, inflation_rate: float) -> float:
        """
        UTILITY CORE: THE EXACT FISHER EQUATION
        --------------------------------------
        An independent utility method that returns the real net growth rate of an asset pool.
        Returns the percentage value rounded to four decimal points for professional tracking.
        """
        r_nominal = float(nominal_return_rate) / 100.0
        i_inflation = float(inflation_rate) / 100.0
        
        # Real Rate = ((1 + r) / (1 + i)) - 1
        real_rate = ((1.0 + r_nominal) / (1.0 + i_inflation)) - 1.0
        return round(real_rate * 100.0, 4)
