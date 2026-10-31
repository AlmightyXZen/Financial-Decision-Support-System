"""
Module: models/loans_and_credit.py
Theoretical Foundation: Chapter 06 of FDSS Monograph (Equated Monthly Installment & Debt Amortization).

Covers:
1. Analytical EMI derivation via finite geometric progression inversion:
   P = sum_{k=1}^n E * (1+R)^(-k) => E = P * R * (1+R)^n / [ (1+R)^n - 1 ]
2. Negative Amortization Boundary Theorem:
   A loan amortizes to zero iff E > P * R <=> E > P * (r / 12).
   If E <= P * R, the balance sequence diverges to positive infinity.
3. Month-by-month debt amortization schedules decomposing Principal vs. Interest.
4. Prepayment impact quantification (tenure reduction & interest savings).
"""

import math
from typing import Dict, Any, Optional
import pandas as pd


def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """
    Computes exact closed-form Equated Monthly Installment (EMI):
    E = P * R * (1+R)^n / [ (1+R)^n - 1 ]
    
    Parameters:
        principal: Borrowed loan capital P > 0.
        annual_rate: Annual nominal interest rate as decimal r >= 0.
        tenure_months: Total loan repayment duration in months n >= 1.
        
    Returns:
        Monthly installment amount E (float).
    """
    if principal <= 0.0:
        raise ValueError(f"Loan principal must be strictly positive (received {principal}).")
    if annual_rate < 0.0:
        raise ValueError(f"Annual interest rate must be non-negative (received {annual_rate}).")
    if tenure_months < 1:
        raise ValueError(f"Tenure in months must be >= 1 (received {tenure_months}).")
        
    # Zero interest rate boundary condition: pure linear split
    if annual_rate == 0.0:
        return float(principal / tenure_months)
        
    r_monthly = annual_rate / 12.0
    factor = math.pow(1.0 + r_monthly, tenure_months)
    
    emi = principal * (r_monthly * factor) / (factor - 1.0)
    return float(emi)


def check_negative_amortization(
    principal: float,
    annual_rate: float,
    monthly_payment: float
) -> Dict[str, Any]:
    """
    Evaluates the Negative Amortization Boundary Condition:
    A loan amortizes toward zero iff E > P * R <=> E > P * (r / 12).
    
    If E <= P * R, interest accrued exceeds monthly payment, causing
    unpaid interest to capitalize and outstanding balance to diverge to infinity.
    """
    if principal <= 0.0 or annual_rate < 0.0 or monthly_payment <= 0.0:
        raise ValueError("Principal, rate, and monthly payment must be positive.")
        
    monthly_rate = annual_rate / 12.0
    monthly_accrued_interest = principal * monthly_rate
    
    is_divergent = monthly_payment <= monthly_accrued_interest
    principal_component = monthly_payment - monthly_accrued_interest
    
    return {
        "is_negative_amortization": is_divergent,
        "monthly_accrued_interest": float(monthly_accrued_interest),
        "monthly_payment": float(monthly_payment),
        "net_principal_reduction": float(principal_component),
        "status": "DIVERGENT_DEBT_TRAP" if is_divergent else "CONVERGENT_AMORTIZING"
    }


def generate_amortization_schedule(
    principal: float,
    annual_rate: float,
    tenure_months: int,
    custom_monthly_payment: Optional[float] = None,
    monthly_prepayment: float = 0.0
) -> pd.DataFrame:
    """
    Generates a full month-by-month loan amortization schedule.
    
    Columns produced:
    - Month: 1 to n
    - Opening_Balance
    - EMI: Scheduled base installment
    - Prepayment: Additional principal paid
    - Total_Payment: EMI + Prepayment
    - Interest_Paid: Opening_Balance * R
    - Principal_Paid: Total_Payment - Interest_Paid
    - Closing_Balance: Opening_Balance - Principal_Paid
    - Cumulative_Interest
    - Cumulative_Principal
    
    Raises:
        ValueError if monthly payment causes negative amortization.
    """
    if principal <= 0.0:
        raise ValueError("Principal must be strictly positive.")
    if annual_rate < 0.0:
        raise ValueError("Interest rate must be non-negative.")
    if tenure_months < 1:
        raise ValueError("Tenure months must be >= 1.")
    if monthly_prepayment < 0.0:
        raise ValueError("Monthly prepayment cannot be negative.")
        
    monthly_rate = annual_rate / 12.0
    scheduled_emi = calculate_emi(principal, annual_rate, tenure_months)
    actual_base_payment = custom_monthly_payment if custom_monthly_payment is not None else scheduled_emi
    
    # Negative amortization check
    boundary_check = check_negative_amortization(principal, annual_rate, actual_base_payment + monthly_prepayment)
    if boundary_check["is_negative_amortization"]:
        raise ValueError(
            f"Negative Amortization Triggered! Monthly payment (INR {actual_base_payment + monthly_prepayment:.2f}) "
            f"is <= monthly accrued interest (INR {boundary_check['monthly_accrued_interest']:.2f}). "
            f"Debt diverges to +infinity."
        )

    schedule = []
    balance = float(principal)
    cum_interest = 0.0
    cum_principal = 0.0
    
    month = 1
    # Cap loop at 1200 months (100 years) as numerical safeguard
    while balance > 1e-4 and month <= 1200:
        opening_bal = balance
        interest_paid = opening_bal * monthly_rate
        
        # Determine total payment needed to close
        total_payment_intended = actual_base_payment + monthly_prepayment
        
        if opening_bal + interest_paid <= total_payment_intended:
            # Final payoff month
            total_payment = opening_bal + interest_paid
            principal_paid = opening_bal
            closing_bal = 0.0
            actual_prepay = max(0.0, total_payment - actual_base_payment)
            base_emi_paid = total_payment - actual_prepay
        else:
            base_emi_paid = actual_base_payment
            actual_prepay = monthly_prepayment
            total_payment = base_emi_paid + actual_prepay
            principal_paid = total_payment - interest_paid
            closing_bal = opening_bal - principal_paid
            
        cum_interest += interest_paid
        cum_principal += principal_paid
        balance = closing_bal
        
        schedule.append({
            "Month": month,
            "Opening_Balance": round(opening_bal, 2),
            "EMI": round(base_emi_paid, 2),
            "Prepayment": round(actual_prepay, 2),
            "Total_Payment": round(total_payment, 2),
            "Interest_Paid": round(interest_paid, 2),
            "Principal_Paid": round(principal_paid, 2),
            "Closing_Balance": round(max(0.0, closing_bal), 2),
            "Cumulative_Interest": round(cum_interest, 2),
            "Cumulative_Principal": round(cum_principal, 2)
        })
        
        month += 1
        
    df = pd.DataFrame(schedule)
    return df


def calculate_prepayment_savings(
    principal: float,
    annual_rate: float,
    tenure_months: int,
    monthly_prepayment: float
) -> Dict[str, Any]:
    """
    Compares baseline loan against a prepayment-accelerated schedule.
    Quantifies exact interest savings and months shaved off the loan.
    """
    baseline_df = generate_amortization_schedule(principal, annual_rate, tenure_months, monthly_prepayment=0.0)
    accelerated_df = generate_amortization_schedule(principal, annual_rate, tenure_months, monthly_prepayment=monthly_prepayment)
    
    base_interest = baseline_df["Interest_Paid"].sum()
    acc_interest = accelerated_df["Interest_Paid"].sum()
    
    base_months = len(baseline_df)
    acc_months = len(accelerated_df)
    
    return {
        "original_tenure_months": base_months,
        "new_tenure_months": acc_months,
        "months_saved": base_months - acc_months,
        "original_total_interest": round(base_interest, 2),
        "new_total_interest": round(acc_interest, 2),
        "interest_saved": round(base_interest - acc_interest, 2),
        "percentage_interest_saved": round(((base_interest - acc_interest) / base_interest) * 100.0, 2)
    }
