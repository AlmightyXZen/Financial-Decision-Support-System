# Save this file inside: backend/simple_interest.py

class SimpleInterestCalculator:
    """
    Engine module for calculating Simple Interest values.
    Includes validation guards to prevent app crashes from faulty user inputs.
    """
    
    def __init__(self, principal: float, annual_rate: float, time_years: float):
        """
        Initialises the calculator state with user inputs and validates them.
        """
        # Validate that inputs are real numbers and are not negative
        try:
            self.principal = float(principal)
            self.rate_decimal = float(annual_rate) / 100.0
            self.time_years = float(time_years)
        except (ValueError, TypeError):
            raise ValueError("Inputs must be valid numbers.")

        # Business Logic Validation (Error Cautioning)
        if self.principal < 0:
            raise ValueError("Principal amount cannot be negative.")
            
        if self.rate_decimal < 0:
            raise ValueError("Interest rate cannot be negative.")
            
        if self.time_years <= 0:
            raise ValueError("Time duration must be greater than zero years.")

    def get_interest_only(self) -> float:
        """
        Calculates and returns ONLY the absolute interest earned or owed.
        Formula: I = P * R * T
        """
        interest = self.principal * self.rate_decimal * self.time_years
        return round(interest, 2)

    def get_total_amount(self) -> float:
        """
        Calculates and returns the final total maturity amount (Principal + Interest).
        Formula: A = P + I
        """
        total_amount = self.principal + self.get_interest_only()
        return round(total_amount, 2)
