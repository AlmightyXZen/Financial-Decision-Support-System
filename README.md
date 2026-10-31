# Financial Decision Support System (FDSS)
### *A Quantitative Financial Mathematics, Numerical Root-Finding & Stochastic Simulation Studio*

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.31%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![CI Build](https://github.com/AlmightyXZen/Financial-Decision-Support-System/actions/workflows/ci.yml/badge.svg)](https://github.com/AlmightyXZen/Financial-Decision-Support-System/actions)
[![Unit Tests](https://img.shields.io/badge/Tests-38%2F38%20Passing-10B981?logo=pytest&logoColor=white)](#6-automated-test-suite)
[![License: MIT](https://img.shields.io/badge/License-MIT-38BDF8.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/Architecture-First--Principles%20Core-818CF8)](#3-mathematical-pillars)

Developed by **Atharv Ranade**  
*Focus: Pure Mathematics, Statistics & Quantitative Financial Modeling*

---

## 1. System Overview & Philosophy

Most commercial financial calculators rely on a dangerous fallacy: **deterministic certainty**. They present static formulas promising that an annual return of $12\%$ compounded over 20 years will yield an exact scalar figure. In real capital markets, returns are neither constant nor guaranteed; they are governed by stochastic differential equations, structural volatility drag, and macroeconomic inflation erosion.

The **Financial Decision Support System (FDSS)** bridges pure mathematical analysis with modern software engineering. Rather than presenting a single hypothetical outcome, this studio models financial dynamics using:

1. **Analytical Real Analysis & Calculus:** Exact closed-form equations for time value of money, continuous Euler limits, and finite geometric series loan amortization.
2. **Numerical Analysis & Root-Finding:** High-precision Newton–Raphson iteration with analytical first derivatives to compute internal yields (IRR) where the **Abel–Ruffini Theorem** proves closed-form algebraic solutions are impossible.
3. **Stochastic Calculus (Itô's Lemma):** Vectorized Geometric Brownian Motion (GBM) simulation modeling thousands of market trajectories, quantifying empirical Value at Risk (VaR), Conditional VaR (Expected Shortfall), and goal attainment probabilities.

---

## 2. Interactive Web Application

FDSS features a high-performance web dashboard built with **Streamlit** and **Plotly**, styled with a dark slate glassmorphic design system:

* **Sleek FinTech Design:** High-density stat KPI cards with live deltas, multi-currency toggles (`₹ INR`, `$ USD`, `€ EUR`, `£ GBP`), and Plotly charts with unified crosshairs.
* **Instant In-Memory Caching (`@st.cache_data`):** Heavy 5,000-path Monte Carlo simulations and multi-decade amortization tables recalculate instantaneously.
* **One-Click Pre-Sets & Milestones:** Pre-loaded macro market scenarios, debt stress labs, and retirement FIRE milestone trackers.
* **Data Portability:** Direct CSV download for all monthly amortization schedules and risk simulations.

---

## 3. Mathematical Pillars

### Layer 1: Time Value of Money & Asymptotic Yield Curvature
Compounding is analyzed from discrete periodic and continuous real analysis viewpoints:
* **Discrete Compounding:** $A(t) = P \left(1 + \frac{r}{m}\right)^{mt}$
* **Continuous Compounding (Euler's Limit):** $\lim_{m \to \infty} P \left(1 + \frac{r}{m}\right)^{mt} = P e^{rt}$
* **Autonomous Differential Equation:** $\frac{dA}{dt} = r A(t), \quad A(0) = P$
* **Effective Annual Rate (EAR):** $\text{EAR} = \left(1 + \frac{r}{m}\right)^m - 1 \xrightarrow{m \to \infty} e^r - 1$
* **Exact Capital Doubling Horizon:** $t_{\text{double}} = \frac{\ln 2}{r}$ (benchmarked against the empirical Rule of 72: $72 / 100r$).

### Layer 2: Debt Amortization Mechanics & The Negative Amortization Boundary
Loans are modeled via finite geometric series discounting:
* **Closed-Form Monthly Installment (EMI):**
  $$E = P \cdot \frac{\frac{r}{12}\left(1 + \frac{r}{12}\right)^n}{\left(1 + \frac{r}{12}\right)^n - 1}$$
* **Negative Amortization Singularity Theorem:** A loan converges toward zero if and only if:
  $$E > P \cdot \frac{r}{12}$$
  If payment $E \le P \cdot \frac{r}{12}$, the unpaid interest capitalizes into the principal, causing debt to diverge:
  $$\lim_{k \to \infty} B_k = +\infty$$
* **Prepayment Acceleration:** Exact analytics showing interest savings and months shaved from the tenure.

### Layer 3: Wealth Accumulation, Step-Up SIP & Exact Fisher Inflation
* **Annuity-Due SIP Accumulation:** Investments committed at the beginning of each period:
  $$S_n = P(1 + j)\frac{(1 + j)^n - 1}{j}, \quad j = \frac{r}{12}$$
* **Step-Up Escalation:** Annual contribution increases by $g\%$ to match career earnings growth.
* **The Exact Fisher Equation:** Exposing the mathematical flaw in linear return subtraction ($r - i$):
  $$1 + r_n = (1 + r_r)(1 + i) \implies r_r = \frac{1 + r_n}{1 + i} - 1$$
* **Monetary Purchasing Power Half-Life:** The exact time required for currency to lose half its real value under constant inflation:
  $$t_{1/2} = \frac{\ln 2}{\ln(1 + i)}$$

### Layer 4: Capital Budgeting & Newton–Raphson Numerical Root-Finding
For multi-period cash flows $\{C_0, C_1, \dots, C_T\}$, finding the Internal Rate of Return ($r^*$) requires solving the polynomial root problem:
$$f(r) = \text{NPV}(r) = \sum_{t=0}^T \frac{C_t}{(1 + r)^t} = 0$$

By Galois Theory and the **Abel–Ruffini Theorem**, general polynomials of degree $T \ge 5$ have **no algebraic radical solution**. Calculating internal yield mathematically mandates numerical analysis:
* **Newton–Raphson Method:** Quadratic convergence using the analytical first derivative:
  $$r_{k+1} = r_k - \frac{f(r_k)}{f'(r_k)}, \quad f'(r) = -\sum_{t=1}^T \frac{t \cdot C_t}{(1 + r)^{t+1}}$$
* **Bisection Safeguard:** Bracket interval halving on $[a, b]$ where $f(a) \cdot f(b) < 0$, guaranteeing convergence if derivatives oscillate.
* **2D Sensitivity Matrix:** Real-time heatmap of Net Present Value across hurdle rates and capital expenditure shifts.

### Layer 5: Itô Stochastic Calculus & Monte Carlo Risk Lab
Asset price trajectories are governed by continuous-time stochastic differential equations (SDEs):
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$

Discretized exactly under **Itô's Lemma** with standard normal variate $Z \sim \mathcal{N}(0, 1)$:
$$S_{t+\Delta t} = S_t \exp\left[\left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} Z\right]$$

* **Structural Volatility Drag:** Demonstrating why geometric compounding underperforms arithmetic expectation:
  $$\Delta \mu = -\frac{1}{2}\sigma^2, \quad \text{Median}(S_T) = S_0 e^{(\mu - \frac{1}{2}\sigma^2)T} < \mathbb{E}[S_T] = S_0 e^{\mu T}$$
* **Downside Tail Risk (VaR & CVaR):** 95% Value at Risk floor and Conditional VaR (Expected Shortfall in the worst 5% tail).
* **Empirical Milestone Probability:** $\hat{P}(S_T \ge \text{Goal}) = \frac{1}{M}\sum_{m=1}^M \mathbf{1}_{\{S_{T, m} \ge \text{Goal}\}}$.

---

## 4. System Architecture

```
Financial-Decision-Support-System/
├── app.py                          # Master application router & shell layout
├── requirements.txt                # Production Python dependencies
├── README.md                       # Comprehensive engineering & mathematical manual
├── .streamlit/
│   └── config.toml                 # Production dark theme & server deployment settings
│
├── ui/                             # Modular presentation layer
│   ├── __init__.py
│   ├── styles.py                   # Central CSS, stat card renderers & Plotly theme
│   ├── tab_time_value.py           # Module 1: Time Value & Doubling Time (Rule of 72)
│   ├── tab_loans.py                # Module 2: Loan Amortization, Payoff Calendar & CSV Export
│   ├── tab_investments.py          # Module 3: Wealth Accumulation & FIRE Milestones
│   ├── tab_capital_budgeting.py    # Module 4: Scenario Analysis & 2D Sensitivity Heatmaps
│   └── tab_monte_carlo.py          # Module 5: Vectorized Stochastic Risk Terminal
│
├── models/                         # First-principles computational core (zero black boxes)
│   ├── __init__.py                 # Clean API exports
│   ├── time_value.py               # SI, CI, continuous compounding, EAR, PV/FV
│   ├── loans_and_credit.py         # EMI, negative amortization boundary, schedules
│   ├── investment_plans.py         # Annuity-due SIP, step-up escalation, Fisher inflation
│   ├── capital_budgeting.py        # Multi-period NPV, Newton-Raphson & history solver
│   └── monte_carlo.py              # Vectorized GBM paths, volatility drag, VaR & CVaR
│
├── tests/                          # Automated mathematical verification suite
│   ├── test_time_value.py          # 13 tests: Monotonicity, Euler limits, inversion
│   ├── test_loans.py               # 7 tests: Hand benchmarks, divergence, prepayment
│   ├── test_investments.py         # 6 tests: Step-up superiority, half-life, Fisher exactness
│   ├── test_capital_budgeting.py   # 6 tests: Quadratic convergence, Abel-Ruffini, payback
│   └── test_monte_carlo.py         # 6 tests: CLT convergence, reproducibility, VaR bounds
│
└── theory_and_derivations/         # 12-volume textbook mathematical monograph series
    ├── chapters/                   # Modular PDF chapter compilation scripts
    ├── build_all_chapters.py       # Master compilation pipeline
    └── *.pdf                       # 12 compiled textbook PDFs (56 pages total)
```

---

## 5. Quickstart & Installation

### Local Setup
Ensure you have Python 3.10+ installed:

```bash
# Clone the repository
git clone https://github.com/AlmightyXZen/Financial-Decision-Support-System.git
cd Financial-Decision-Support-System

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch the interactive web studio
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 6. Automated Test Suite

Every financial model is verified against closed-form analytical benchmarks and IEEE 754 edge cases:

```bash
pytest -v
```

```
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.1
rootdir: Financial-Decision-Support-System

tests/test_capital_budgeting.py ......                                   [ 15%]
tests/test_investments.py ......                                         [ 31%]
tests/test_loans.py .......                                              [ 50%]
tests/test_monte_carlo.py ......                                         [ 65%]
tests/test_time_value.py .............                                   [100%]

============================= 38 passed in 0.64s ==============================
```

---

## 7. Cloud Deployment

This repository is pre-configured with [`.streamlit/config.toml`](.streamlit/config.toml) for zero-configuration, one-click deployment:

* **Streamlit Community Cloud:** Connect your GitHub account, select repository `AlmightyXZen/Financial-Decision-Support-System`, branch `main`, and main file `app.py`.
* **Render / Railway / Cloud VM:** Set build command to `pip install -r requirements.txt` and start command to `streamlit run app.py --server.port $PORT --server.headless true`.

---

## 8. License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

Copyright © 2026 **Atharv Ranade**. All rights reserved.
