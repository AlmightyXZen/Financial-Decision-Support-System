# Financial Decision Support System (FDSS)
### *A Mathematical & Stochastic Framework for Financial Analysis and Decision Support*

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Research Convention](https://img.shields.io/badge/Research-Avishkar%20Convention%20(MU)-purple.svg)](https://mu.ac.in/)
[![Domain](https://img.shields.io/badge/Domain-Quantitative%20Finance%20%7C%20Applied%20Math-orange.svg)](#)

Developed by **Atharv Ranade**  
*Department of Mathematics, University of Mumbai*  
*Focus: Pure Mathematics, Statistics & Quantitative Finance*

---

## 1. Project Motivation & Philosophy

Most commercial and online financial calculators operate on a dangerous assumption: **deterministic certainty**. They present investors with static formulas—promising that an annual return of $12\%$ compounded over 20 years will yield an exact rupee figure. In real capital markets, returns are neither constant nor guaranteed; they are governed by stochastic processes, volatility drag, and macroeconomic uncertainty.

The **Financial Decision Support System (FDSS)** is designed to bridge pure mathematical theory with applied financial engineering. Rather than presenting a single hypothetical outcome, this system treats financial decisions as **probabilistic distributions**. It integrates:

1. **Analytical Financial Mathematics:** Exact closed-form formulas for time value of money, amortization schedules, and real purchasing power.
2. **Numerical Analysis:** Root-finding algorithms (Newton–Raphson and Bisection methods) to solve non-linear cash flow equations where closed-form algebraic solutions are mathematically impossible.
3. **Stochastic Simulation:** Monte Carlo modeling based on Geometric Brownian Motion (GBM) to simulate thousands of plausible market trajectories, computing downside tail risks and the empirical probability of achieving financial milestones.

This repository is built as an official submission for the **Avishkar Research Convention** (University of Mumbai / Maharashtra State Inter-University Convention) and serves as an evolving, lifelong open-source foundation for advanced research in **Quantitative Finance and Computational Mathematics**.

---

## 2. System Architecture

The project is structured into modular layers, separating pure mathematical logic from data manipulation, testing, and presentation:

```
Financial-Decision-Support-System/
├── .gitignore                      # Git exclusion rules for clean version control
├── requirements.txt                # Production and development dependencies
├── README.md                       # Research, theoretical, and technical overview
├── app.py                          # Interactive Streamlit application interface
│
├── models/                         # Mathematical and numerical computation core
│   ├── __init__.py
│   ├── time_value.py               # SI, CI, continuous compounding, EAR, PV/FV
│   ├── loans_and_credit.py         # Closed-form EMI, loan amortization schedules
│   ├── investment_plans.py         # SIP (annuity-due), SWP, inflation discounting
│   ├── capital_budgeting.py        # NPV, numerical IRR (Newton-Raphson & Bisection)
│   └── monte_carlo.py              # Geometric Brownian Motion, path & terminal simulation
│
├── tests/                          # Automated mathematical verification suite
│   ├── __init__.py
│   ├── test_time_value.py          # Analytical benchmarks & boundary tests
│   ├── test_loans.py               # Principal/interest balance verification
│   ├── test_capital_budgeting.py   # Root-finding convergence & tolerance checks
│   └── test_monte_carlo.py         # Seed reproducibility & statistical validation
│
├── theory_and_derivations/         # 12-chapter textbook mathematical reference series
│   ├── chapters/                   # Modular chapter generator scripts (Ch01 - Ch12)
│   ├── build_all_chapters.py       # Master monograph compilation engine
│   ├── styles.py                   # Textbook typography & layout framework
│   ├── README.md                   # Syllabus, proofs, and theory-to-software mapping
│   └── *.pdf                       # 12 production-grade textbook PDFs (56 pages total)
│
└── docs/                           # Academic papers, derivations, and convention notes
    ├── mathematical_specifications.md
    └── avishkar_synopsis.md
```

---

## 3. Mathematical Foundations

### Layer 1: Time Value of Money & Discrete Limits
Interest compounding is analyzed from both discrete algebraic and continuous real analysis viewpoints:
* **Discrete Compounding ($n$ times/year):**
  $$A(t) = P \left(1 + \frac{r}{n}\right)^{nt}$$
* **Continuous Compounding ($n \to \infty$):**
  $$\lim_{n \to \infty} P \left(1 + \frac{r}{n}\right)^{nt} = P e^{rt}$$
* **Effective Annual Rate (EAR):**
  $$\text{EAR} = \left(1 + \frac{r}{n}\right)^n - 1 \quad \implies \quad \text{EAR}_{\text{cont}} = e^r - 1$$

### Layer 2: Numerical Root-Finding for Yield Analysis (IRR)
For irregular cash flows $\{C_0, C_1, \dots, C_T\}$, finding the Internal Rate of Return ($r^*$) requires solving:
$$f(r) = \sum_{t=0}^T \frac{C_t}{(1 + r)^t} = 0$$

Since $f(r) = 0$ is a high-degree polynomial, Galois theory (the Abel–Ruffini theorem) proves that general algebraic radical solutions do not exist for $T > 4$. FDSS implements:
* **Newton–Raphson Method:** Fast quadratic convergence using the analytical first derivative:
  $$r_{k+1} = r_k - \frac{f(r_k)}{f'(r_k)}, \quad f'(r) = -\sum_{t=1}^T \frac{t \cdot C_t}{(1+r)^{t+1}}$$
* **Bisection Fallback:** Bracket-based interval halving on $[a, b]$ where $f(a) \cdot f(b) < 0$ ensuring guaranteed convergence when derivatives oscillate.

### Layer 3: Stochastic Modeling (Geometric Brownian Motion)
Market asset returns and portfolio paths are modeled using continuous-time stochastic calculus (Itô's Lemma):
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$
Discretized over interval $\Delta t$ with standard normal variate $Z \sim \mathcal{N}(0, 1)$:
$$S_{t+\Delta t} = S_t \exp\left[\left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} Z\right]$$

By generating $M = 10,000+$ independent stochastic paths, the system computes:
1. **Terminal Wealth Density:** The probability density function of terminal portfolio value.
2. **Empirical Probability of Target Achievement:**
   $$\hat{P}(S_T \ge \text{Target}) = \frac{1}{M}\sum_{m=1}^M \mathbf{1}_{\{S_{T, m} \ge \text{Target}\}}$$
3. **Downside Risk & Value at Risk (VaR):** Quantifying maximum expected loss at the 95th percentile confidence level.

### Dedicated Mathematical Monograph Series (`theory_and_derivations/`)

The theoretical proofs, ODE derivations, and step-by-step arithmetic hand solutions for every algorithm are compiled into a standalone 12-chapter textbook monograph series in [`theory_and_derivations/`](theory_and_derivations/README.md) (56 pages total):

| Chapter | Document Title | Pages | Key Proofs & Analytical Contributions |
| :---: | :--- | :---: | :--- |
| **01** | [Simple Interest & Linear Accumulation](theory_and_derivations/01_Simple_Interest.pdf) | 4 | ODE $dA/dt = Pr$, Bernoulli convexity theorem, non-subadditivity proof |
| **02** | [Compound Interest & Geometric Accumulation](theory_and_derivations/02_Compound_Interest.pdf) | 5 | Geometric progression, frequency arbitrage proof, binomial expansions |
| **03** | [Continuous Compounding & Infinitesimal Calculus](theory_and_derivations/03_Continuous_Compounding.pdf) | 4 | Euler's limit $\lim (1+r/m)^{mt} = e^{rt}$, homogeneous ODE $dA/dt = rA$ |
| **04** | [Present Value, Future Value & Discounting](theory_and_derivations/04_Present_Value_and_Future_Value.pdf) | 4 | Stochastic discount factor $v(t)$, negative exponential asymptotic decay |
| **05** | [Nominal vs. Effective Annual Rate (EAR)](theory_and_derivations/05_Effective_Annual_Rate.pdf) | 4 | Frequency divergence spread, APY regulatory standardization |
| **06** | [Equated Monthly Installment (EMI) & Debt Amortization](theory_and_derivations/06_Equated_Monthly_Installment_EMI.pdf) | 6 | Annuity discounting, finite geometric sum proof, negative amortization bounds |
| **07** | [Systematic Investment Plan (SIP) & Annuity Wealth Accumulation](theory_and_derivations/07_Systematic_Investment_Plan_SIP.pdf) | 6 | Annuity-due future value, Dollar-Cost Averaging, harmonic mean pricing advantage |
| **08** | [Inflation, Real Purchasing Power & The Fisher Equation](theory_and_derivations/08_Inflation_and_Purchasing_Power.pdf) | 4 | Exact Fisher relation $(1+r_n)=(1+r_r)(1+i)$, purchasing power half-life $t_{1/2}$ |
| **09** | [Net Present Value (NPV) & Capital Budgeting](theory_and_derivations/09_Net_Present_Value_NPV.pdf) | 4 | Multi-period DCF, Hurdle rate / WACC, convexity of NPV curve |
| **10** | [Internal Rate of Return (IRR) & Root Finding](theory_and_derivations/10_Internal_Rate_of_Return_IRR.pdf) | 5 | Abel-Ruffini theorem, Newton-Raphson iteration, Descartes' rule of signs |
| **11** | [Geometric Brownian Motion (GBM) & Itô's Lemma](theory_and_derivations/11_Geometric_Brownian_Motion.pdf) | 4 | Continuous SDE $dS = \mu S dt + \sigma S dW$, Itô's Lemma, Volatility drag $\Delta \mu = -\sigma^2/2$ |
| **12** | [Monte Carlo Simulation & Quantitative Risk Analysis](theory_and_derivations/12_Monte_Carlo_Simulation.pdf) | 6 | SLLN, Central Limit Theorem $\mathcal{O}(1/\sqrt{M})$, Empirical VaR & CVaR |

To build or recompile all 12 chapters locally:
```bash
python theory_and_derivations/build_all_chapters.py
```

---

## 4. Verification & Testing Methodology

Academic research requires uncompromising reproducibility. Every model in this system is verified against three standards:

1. **Analytical Hand Calculations:** Simple test vectors solved manually on paper to confirm raw formula accuracy.
2. **Independent Benchmarking:** Deterministic models are cross-checked against standard Microsoft Excel financial functions (`PMT`, `PV`, `FV`, `IRR`) with a floating-point tolerance of $\epsilon \le 10^{-5}$.
3. **Automated Unit Testing (`pytest`):** Comprehensive unit tests checking:
   * Standard inputs (typical investment/loan scenarios)
   * Boundary inputs ($r = 0$, $t = 0$, high-frequency compounding)
   * Exception handling (negative principals, nonsensical tenures, zero division)
   * Seed consistency for Monte Carlo reproducibility

---

## 5. Getting Started

### Prerequisites
* Python 3.10+ (tested on Python 3.14)
* Git

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AlmightyXZen/Financial-Decision-Support-System.git
   cd Financial-Decision-Support-System
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the automated test suite:
   ```bash
   pytest
   ```

5. Launch the interactive dashboard:
   ```bash
   streamlit run app.py
   ```

---

## 6. Long-Term Roadmap & Research Horizon

This project is developed with a long-term academic trajectory targeting **M.Sc. programs in Quantitative Finance, Computational Finance, and Financial Mathematics** in Europe (Universities of Padova, Bologna, Trento, and Pavia).

```
Phase 1: Avishkar Convention Edition (Current)
├── Analytical TVM & Amortization Schedules
├── Numerical Root-Finding for Cash Flow Yields (IRR)
├── Monte Carlo Simulation Engine (GBM Wealth Paths)
└── Interactive Streamlit Decision Support Dashboard

Phase 2: Modern Portfolio Theory (Post-Avishkar)
├── Markowitz Mean-Variance Optimization
├── Efficient Frontier Construction using Quadratic Programming
└── Capital Asset Pricing Model (CAPM) & Sharpe Ratio Maximization

Phase 3: Quantitative Risk & Derivative Pricing
├── Parametric & Historical Value at Risk (VaR) / Conditional VaR (CVaR)
├── Black-Scholes-Merton European Option Pricing Engine
└── Analytical Greeks Calculation (Delta, Gamma, Vega, Theta, Rho)
```

---

## 7. Citation & Academic Reference

If you reference this work or build upon this codebase for academic research, please cite:

```bibtex
@misc{ranade2026fdss,
  author = {Ranade, Atharv},
  title = {Financial Decision Support System: A Mathematical and Stochastic Framework for Financial Analysis},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/AlmightyXZen/Financial-Decision-Support-System}},
  note = {Avishkar Research Convention, Department of Students' Development, University of Mumbai}
}
```

---

## 8. License

This project is open-source and licensed under the **MIT License**. See the `LICENSE` file for full details.