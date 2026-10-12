# Mathematical Foundations of Finance: Theory, Derivations & Axiomatic Reference Series

This directory constitutes the theoretical reference monograph for the **Financial Decision Support System (FDSS)**. It bridges the gap between pure mathematical finance and production software engineering, ensuring that every financial algorithm implemented in the application layer is derived from rigorous first principles, proved analytically, and validated with step-by-step hand solutions.

---

## Pedagogical & Analytical Philosophy

In computational finance and quantitative risk modeling, software often treats financial formulas as opaque "black-box" routines. This repository rejects that convention. Every calculation engine in `models/` maps directly to an axiomatic chapter in this monograph series.

### Structural Standards for Every Chapter
Each chapter is formatted as a formal, spacious, textbook-grade PDF reference document featuring:
1. **First-Principles Axioms & Derivations:** Mathematical definitions, governing Ordinary Differential Equations (ODEs) or Stochastic Differential Equations (SDEs), analytic proofs, and limiting convergence behaviors.
2. **Two Hand-Solved Academic Case Studies:** Fully worked real-world problems with complete arithmetic steps, domain checks, and zero skipped intermediate operations.
3. **Algorithmic Python Implementation:** Production-grade, vectorized, and type-annotated code with input domain validation.
4. **Mathematical Properties Summary Table:** High-contrast summary comparing variables, governing bounds, analytical significance, and financial implications.
5. **Universal Typography & Clean Layout:** High-contrast palette (`#0F172A` body, `#1E3A8A` headers), dedicated margins, running textbook headers, and clean page breaks.

---

## Monograph Syllabus & Chapter Mapping

The monograph spans 12 structured chapters (56 total pages), organized into four progressive analytical tiers:

### Tier I: Elementary Discrete Accumulation & Discounting
* [**01_Simple_Interest.pdf**](01_Simple_Interest.pdf) (4 Pages)
  * *Topics:* Linear accumulation axiom, governing ODE $dA/dt = Pr$, Bernoulli's inequality, non-subadditivity proof ($A(t_1 + t_2) < A(t_1)A(t_2)$), money market conventions (Actual/365, Actual/360).
  * *Software Mapping:* `models/time_value.py` &rarr; `simple_interest()`, `simple_interest_amount()`
* [**02_Compound_Interest.pdf**](02_Compound_Interest.pdf) (5 Pages)
  * *Topics:* Geometric accumulation, discrete compounding frequencies ($m \in \{1, 2, 4, 12, 365\}$), binomial expansion, compounding frequency arbitrage proof, effective wealth growth.
  * *Software Mapping:* `models/time_value.py` &rarr; `compound_interest_amount()`, `accrued_compound_interest()`
* [**03_Continuous_Compounding.pdf**](03_Continuous_Compounding.pdf) (4 Pages)
  * *Topics:* Euler's constant $e$ as the infinitesimal limit $\lim_{m \to \infty} (1 + r/m)^{mt} = e^{rt}$, homogeneous linear ODE $dA/dt = rA(t)$, logarithmic returns additivity, infinitesimal cash flow modeling.
  * *Software Mapping:* `models/time_value.py` &rarr; `continuous_compounding_amount()`, `discrete_to_continuous_yield()`
* [**04_Present_Value_and_Future_Value.pdf**](04_Present_Value_and_Future_Value.pdf) (4 Pages)
  * *Topics:* Temporal financial equivalence, stochastic discount factor $v(t) = (1+r)^{-t}$, negative exponential time decay, asymptotic convergence as $t \to \infty$, multi-period lump-sum discounting.
  * *Software Mapping:* `models/time_value.py` &rarr; `present_value()`, `future_value()`
* [**05_Effective_Annual_Rate.pdf**](05_Effective_Annual_Rate.pdf) (4 Pages)
  * *Topics:* Nominal APR vs. Effective Annual Rate (EAR), compounding frequency spread, APY standardization under institutional lending regulations, consumer debt risk quantification.
  * *Software Mapping:* `models/time_value.py` &rarr; `nominal_to_effective_rate()`, `effective_to_nominal_rate()`

### Tier II: Consumer Finance & Amortization Analytics
* [**06_Equated_Monthly_Installment_EMI.pdf**](06_Equated_Monthly_Installment_EMI.pdf) (6 Pages)
  * *Topics:* Ordinary annuity discounting, closed-form summation of finite geometric series $\sum_{k=1}^n (1+R)^{-k}$, negative amortization thresholds, loan amortization schedule generation, principal/interest decomposition.
  * *Software Mapping:* `models/loans.py` &rarr; `calculate_emi()`, `generate_amortization_schedule()`
* [**07_Systematic_Investment_Plan_SIP.pdf**](07_Systematic_Investment_Plan_SIP.pdf) (6 Pages)
  * *Topics:* Annuity-due future value derivation, Dollar-Cost Averaging (DCA), harmonic mean vs. arithmetic mean purchasing advantage, step-up SIP with annual contribution escalation, long-term wealth compounding.
  * *Software Mapping:* `models/investments.py` &rarr; `calculate_sip_wealth()`, `calculate_step_up_sip()`
* [**08_Inflation_and_Purchasing_Power.pdf**](08_Inflation_and_Purchasing_Power.pdf) (4 Pages)
  * *Topics:* The Fisher Equation $(1+r_n) = (1+r_r)(1+i)$, purchasing power parity, monetary erosion half-life $t_{1/2} = \ln(2)/\ln(1+i)$, nominal wealth illusion, real inflation-adjusted wealth trajectories.
  * *Software Mapping:* `models/macro.py` &rarr; `real_rate_of_return()`, `purchasing_power_erosion()`

### Tier III: Capital Budgeting & Numerical Optimization
* [**09_Net_Present_Value_NPV.pdf**](09_Net_Present_Value_NPV.pdf) (4 Pages)
  * *Topics:* Discounted Cash Flow (DCF) framework, uneven multi-period cash flows, hurdle rates / WACC, convexity of NPV with respect to discount rate, investment acceptance criteria.
  * *Software Mapping:* `models/capital_budgeting.py` &rarr; `net_present_value()`, `discounted_payback_period()`
* [**10_Internal_Rate_of_Return_IRR.pdf**](10_Internal_Rate_of_Return_IRR.pdf) (5 Pages)
  * *Topics:* Non-linear polynomial root-finding $\text{NPV}(r) = 0$, Descartes' Rule of Signs, multiple internal rate singularities in non-conventional cash flows, Newton-Raphson iteration $r_{k+1} = r_k - \text{NPV}(r_k)/\text{NPV}'(r_k)$, quadratic convergence proofs.
  * *Software Mapping:* `models/capital_budgeting.py` &rarr; `internal_rate_of_return()`, `modified_internal_rate_of_return()`

### Tier IV: Stochastic Calculus & Quantitative Risk Simulation
* [**11_Geometric_Brownian_Motion.pdf**](11_Geometric_Brownian_Motion.pdf) (4 Pages)
  * *Topics:* Stochastic Differential Equations (SDEs), standard Wiener process $W_t$, It\u00f4's Lemma derivation for $f(S) = \ln S$, volatility drag theorem $\Delta \mu = -\sigma^2/2$, divergence between arithmetic mean path $\mathbb{E}[S_t] = S_0 e^{\mu t}$ and median investor path $S_0 e^{(\mu - \sigma^2/2)t}$.
  * *Software Mapping:* `models/monte_carlo.py` &rarr; `simulate_gbm_paths()`, `calculate_volatility_drag()`
* [**12_Monte_Carlo_Simulation.pdf**](12_Monte_Carlo_Simulation.pdf) (6 Pages)
  * *Topics:* Law of Large Numbers (SLLN), Central Limit Theorem convergence $\mathcal{O}(1/\sqrt{M})$, confidence intervals for stochastic estimators, empirical percentile calculation, goal attainment probability $\mathbb{P}(S_T \ge G)$, parametric vs. historical Value at Risk (VaR) and Conditional VaR (Expected Shortfall).
  * *Software Mapping:* `models/monte_carlo.py` &rarr; `run_monte_carlo_portfolio()`, `calculate_value_at_risk()`, `goal_attainment_probability()`

---

## Compiling the Monograph Series

All PDFs are programmatically generated using ReportLab and fully reproducible from source.

### Prerequisites
Ensure the virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Build All 12 Chapters in One Command
To compile all 12 chapters into their respective production PDFs:
```bash
python theory_and_derivations/build_all_chapters.py
```

### Build an Individual Chapter
To recompile a specific chapter:
```bash
python theory_and_derivations/chapters/ch01_simple_interest.py
python theory_and_derivations/chapters/ch12_monte_carlo_simulation.py
```

---

## Mathematical Notation Reference

| Symbol | Mathematical Description | Dimensional Unit |
| :--- | :--- | :--- |
| $P, S_0$ | Initial principal / Base asset price | Currency ($\text{INR}$) |
| $r, \mu$ | Annual nominal interest rate / Expected continuous drift | Percentage ($\text{yr}^{-1}$) |
| $\sigma$ | Annualized asset volatility | Percentage ($\text{yr}^{-1/2}$) |
| $t, T$ | Investment duration / Maturity horizon | Years ($\text{yr}$) |
| $m$ | Compounding frequency per annum | Integer ($\text{yr}^{-1}$) |
| $E$ | Equated Monthly Installment | Currency ($\text{INR} \cdot \text{mo}^{-1}$) |
| $W_t$ | Standard Brownian Motion (Wiener Process) | Stochastic ($\sim \mathcal{N}(0, t)$) |
| $M$ | Number of simulated stochastic trajectories | Integer paths |
