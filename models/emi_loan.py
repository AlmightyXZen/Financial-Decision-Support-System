# Save this file inside: backend/emi_loan.py

class EmiLoanCalculator:
    """
    ENGINE ARCHITECTURE OVERVIEW:
    ----------------------------
    This engine computes the monthly repayment requirements and lifecycle costs of a loan.
    It serves everyday consumers comparing bank loans and professionals modeling debt structures.
    Outputs are isolated into separate class methods to fit a multi-option UI layout.
    
    IN-LINE THEORY REFRESHER:
    ------------------------
    An EMI amortizes debt geometrically. Interest is calculated on the remaining balance 
    each month; the rest of the payment reduces the actual principal.
    Formula: EMI = [P * r * (1+r)^n] / [((1+r)^n) - 1]
    Total Payable = EMI * Total Months
    Total Interest = Total Payable - Starting Principal
    """

    def __init__(self, loan_amount: float, annual_interest_rate: float, tenure_years: float):
        """
        INITIALIZATION & INPUT SANITIZATION PIPELINE
        -------------------------------------------
        Converts text input strings from mobile entry elements into clean floats.
        Applies strict logic validation gates to catch math errors before execution.
        
        :param loan_amount: Total money borrowed (P). Must be greater than zero.
        :param annual_interest_rate: Nominal yearly interest rate percentage (R) (e.g., 10.5 for 10.5%).
        :param tenure_years: The length of the loan repayment term in years (T). Must be above zero.
        """
        # STEP 1: TYPE SANITIZATION
        try:
            self.loan_amount = float(loan_amount)
            self.annual_rate = float(annual_interest_rate)
            self.tenure_years = float(tenure_years)
        except (ValueError, TypeError):
            raise ValueError("Data Input Error: Clean numerical entries are required to calculate EMI.")

        # STEP 2: BUSINESS LOGIC GUARD RAILS (Error Cautioning)
        if self.loan_amount <= 0:
            raise ValueError("Loan Error: Borrowed loan principal must be greater than zero.")
            
        if self.annual_rate < 0:
            raise ValueError("Risk Alert: Loan interest rate metric cannot be negative.")
            
        if self.tenure_years <= 0:
            raise ValueError("Timeline Error: Loan repayment tenure must be greater than zero years.")

        # STEP 3: CONVERT YEARLY VARIABLES TO MONTHLY INCREMENTS
        # Loans are calculated on a monthly timeline.
        self.monthly_rate = (self.annual_rate / 100.0) / 12.0
        self.total_months = int(self.tenure_years * 12)

    def get_monthly_emi(self) -> float:
        """
        OUTPUT OPTION A: FIXED MONTHLY PAYMENT (EMI)
        -------------------------------------------
        Executes the standard reducing-balance loan amortization formula.
        Handles zero-percent interest loans as a special logic condition.
        """
        # Special logic check for 0% Interest Loans (No-Cost EMI schemes)
        if self.monthly_rate == 0:
            return round(self.loan_amount / self.total_months, 2)
            
        # Standard Formula: EMI = [P * r * (1+r)^n] / [((1+r)^n) - 1]
        compounded_growth_factor = (1.0 + self.monthly_rate) ** self.total_months
        numerator = self.loan_amount * self.monthly_rate * compounded_growth_factor
        denominator = compounded_growth_factor - 1.0
        
        calculated_emi = numerator / denominator
        return round(calculated_emi, 2)

    def get_total_payable_amount(self) -> float:
        """
        OUTPUT OPTION B: COMPLETE LIFECYCLE REPAYMENT COST
        --------------------------------------------------
        Calculates the true total cash amount paid to the lender over the loan term.
        Formula: Total Repayment = Fixed Monthly EMI * Total Months
        """
        fixed_emi = self.get_monthly_emi()
        total_payable = fixed_emi * self.total_months
        return round(total_payable, 2)

    def get_total_interest_only(self) -> float:
        """
        OUTPUT OPTION C: PURE BANK INTEREST CHARGE
        ------------------------------------------
        Isolates the net cost of borrowing by subtracting the original loan amount.
        Formula: Total Interest Cost = Total Repayment Amount - Original Loan Principal
        """
        total_payable = self.get_total_payable_amount()
        pure_interest_cost = total_payable - self.loan_amount
        return round(pure_interest_cost, 2)
