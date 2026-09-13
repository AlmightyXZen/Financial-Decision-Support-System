# Save this file inside: backend/monte_carlo_sim.py

import random

class MonteCarloProjectSimulator:
    """
    ENGINE ARCHITECTURE OVERVIEW:
    ----------------------------
    Simulates operational project outcome ranges by layering standard deviation normal variations 
    over the core cash flow array. It returns probabilistic data options to protect professional 
    investors from point-estimate forecasting vulnerabilities.
    """

    def __init__(self, initial_investment: float, expected_cash_flows: list, annual_volatility: float, discount_rate: float):
        """
        INITIALIZATION PIPELINE
        -----------------------
        :param expected_cash_flows: Baseline targeted operational inflows.
        :param annual_volatility: Expected forecast deviation percentage (e.g., 15 for 15% standard deviation margin).
        """
        self.initial_outlay = float(abs(initial_investment))
        self.base_flows = [float(cf) for cf in expected_cash_flows]
        self.volatility = float(annual_volatility) / 100.0
        self.discount_rate = float(discount_rate) / 100.0

    def run_risk_simulation(self, iterations: int = 2000) -> dict:
        """
        SIMULATION CORE PIPELINE
        ------------------------
        Runs thousands of simulated project lifecycles. In each iteration, every year's 
        cash flow is randomly generated using a normal distribution centered around that year's base flow.
        
        OUTPUT FORMAT:
        Returns a multi-value data map tracking worst/best case outcomes and probability of project loss.
        """
        simulated_npvs = []
        positive_npv_count = 0

        # Fix random seed optionally for unit validation stability during app reloads
        random.seed(42)

        for _ in range(int(iterations)):
            current_iteration_npv = -self.initial_outlay

            for year_index, base_cash_flow in enumerate(self.base_flows, start=1):
                # Calculate standard deviation variance window size in absolute dollars for this year
                std_dev_dollars = base_cash_flow * self.volatility
                
                # Draw a randomized cash flow using a Gaussian/Normal distribution curve
                simulated_flow = random.gauss(base_cash_flow, std_dev_dollars)
                
                # Accumulate the discounted simulated value into this lifetime's NPV run
                current_iteration_npv += simulated_flow / ((1.0 + self.discount_rate) ** year_index)

            simulated_npvs.append(current_iteration_npv)
            if current_iteration_npv > 0:
                positive_npv_count += 1

        # Sort the results array to isolate analytical probability percentile blocks
        simulated_npvs.sort()
        total_runs = len(simulated_npvs)

        probability_of_profit = (positive_npv_count / total_runs) * 100.0
        probability_of_loss = 100.0 - probability_of_profit

        return {
            "average_expected_npv": round(sum(simulated_npvs) / total_runs, 2),
            "worst_case_5th_percentile": round(simulated_npvs[int(total_runs * 0.05)], 2),
            "best_case_95th_percentile": round(simulated_npvs[int(total_runs * 0.95)], 2),
            "risk_probability_of_loss_percent": round(probability_of_loss, 2)
        }
