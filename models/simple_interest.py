def calculate_simple_interest(principal: float, rate: float, time: float) -> dict:
    """
    Calculates Simple Interest and total accumulated amount.
    
    Formula:
      Simple Interest (SI) = (P * R * T) / 100
      Total Amount (A)    = P + SI
      
    Parameters:
      principal (P): Initial invested amount (> 0)
      rate (R): Annual interest rate in percentage (> 0)
      time (T): Time period in years (> 0)
    """
    if principal <= 0 or rate < 0 or time <= 0:
        raise ValueError("Principal, rate, and time must be positive values.")
        
    interest = (principal * rate * time) / 100.0
    total_amount = principal + interest
    
    return {
        "principal": principal,
        "interest": interest,
        "total_amount": total_amount
    }
