# Presentation Storyline & Academic Deck Outline
**Project:** Financial Decision Support System (FDSS)  
**Presenter:** Atharv Ranade | Department of Mathematics & Statistics, University of Mumbai  
**Domain:** Applied Mathematics & Stochastic Finance (Avishkar Category 3: Pure Sciences)  
**Target Duration:** 7 Minutes (10 Slides Total, ~40s per slide)

---

## Slide 01: Title & Academic Research Framework
* **Core Takeaway:** This research investigates retail financial decision-making from an Applied Mathematics and Stochastic Analysis perspective, not commercial software.
* **Layout Structure:** Minimalist academic hero cover with title, investigator metadata, department affiliation, and research category badge.
* **Key Elements:**
  - Project Title: Financial Decision Support System (FDSS)
  - Subtitle: A Mathematical & Stochastic Framework for Retail Financial Risk Modeling
  - Investigator: Atharv Ranade | BSc Mathematics & Statistics
  - Affiliation: University of Mumbai (Avishkar Category 3: Pure Sciences)

## Slide 02: The Core Problem — Why Retail Calculators Lie
* **Core Takeaway:** Conventional retail calculators assume zero volatility and linear expectations, directly violating Jensen's Inequality.
* **Layout Structure:** Side-by-side contrast cards (Linear Assumption vs. Stochastic Reality) anchored by Jensen's inequality formula.
* **Key Elements:**
  - Left Card: Invariant return $A(t) = P(1+r)^t$ assuming zero volatility ($\sigma = 0$).
  - Right Card: Continuous Brownian motion with volatility drag pulling median wealth down.
  - Hero Formula: $\mathbb{E}[g(X)] \ne g(\mathbb{E}[X])$ — Compounding under uncertainty cannot be evaluated using arithmetic averages.

## Slide 03: Research Hypothesis & Methodological Framework
* **Core Takeaway:** We bridge pure mathematical analysis, numerical root-finding, and stochastic calculus to replace single-point illusions with probability distributions.
* **Layout Structure:** Central highlighted hypothesis box over a 3-pillar horizontal methodology grid.
* **Key Elements:**
  - Hypothesis: Replacing point expectations with numerical optimization and stochastic differential equations provides distribution-aware decision support.
  - Pillar 1 (Analysis): Formulating capital accumulation through differential equations and Euler limits.
  - Pillar 2 (Numerical): Overcoming Abel–Ruffini algebraic insolvability using Newton–Raphson iteration.
  - Pillar 3 (Stochastic): Quantifying downside tail risk through Itô calculus and Monte Carlo simulation.

## Slide 04: Pillar 1 — Time Value of Money & Governing ODEs
* **Core Takeaway:** Continuous compounding is governed by an autonomous ODE whose exponential solution ensures linear additivity of logarithmic returns.
* **Layout Structure:** Dual ODE comparison columns with highlighted Euler limit and yield equivalence formulas.
* **Key Elements:**
  - Linear ODE (Simple Interest): $\frac{dA}{dt} = Pr \implies A(t) = P(1+rt)$ (violates subadditivity).
  - Autonomous ODE (Continuous): $\frac{dA}{dt} = rA(t) \implies A(t) = P e^{rt}$ (satisfies semigroup property).
  - Euler Limit: $\lim_{m \to \infty} P(1 + r/m)^{mt} = P e^{rt}$.
  - Quantitative Insight: Continuously compounded returns are linearly additive across multi-period horizons.

## Slide 05: Pillar 2 — Consumer Debt & Negative Amortization Boundary
* **Core Takeaway:** By inverting a finite geometric progression, we derive the exact condition where predatory credit triggers runaway debt divergence.
* **Layout Structure:** Top hero EMI formula over dual cards (Amortization Dynamics vs. Boundary Theorem).
* **Key Elements:**
  - EMI Formula: $E = P \cdot \frac{R(1+R)^n}{(1+R)^n - 1}$ derived from $\sum_{k=1}^n E(1+R)^{-k} = P$.
  - Amortization Dynamics: Monthly principal repayments form an escalating geometric progression $P_k = P_1(1+R)^{k-1}$.
  - Negative Amortization Boundary: Debt amortizes $\iff E > P \cdot \frac{r}{12}$.
  - Predatory Trap: If $E \le P \cdot R$, debt balance diverges to positive infinity ($\lim_{n \to \infty} B_n = +\infty$).

## Slide 06: Pillar 3 — Numerical Optimization for Yields & The Abel–Ruffini Theorem
* **Core Takeaway:** Multi-period internal rate of return equations cannot be solved algebraically by radicals; they fundamentally mandate numerical analysis.
* **Layout Structure:** Central IRR polynomial equation over dual cards (Galois Theory proof vs. Dual-Engine Numerical Solver).
* **Key Elements:**
  - The IRR Polynomial: $\text{NPV}(r) = \sum_{t=0}^T C_t (1+r)^{-t} = 0 \iff \sum C_t x^t = 0$.
  - The Abel–Ruffini Theorem: Polynomials of degree $T \ge 5$ have no general radical solution.
  - Newton–Raphson Engine: $r_{k+1} = r_k - \frac{\text{NPV}(r_k)}{f'(r_k)}$ with quadratic convergence $\mathcal{O}(e_k^2)$.
  - Robustness Fallback: Bisection method guarantees convergence if derivatives oscillate or approach zero.

## Slide 07: Pillar 4 — Stochastic Asset Dynamics & Itô's Volatility Drag
* **Core Takeaway:** Non-zero quadratic variation in Brownian motion introduces a structural drag $-\frac{1}{2}\sigma^2$, forcing over 50% of investors below the arithmetic mean.
* **Layout Structure:** Top SDE & Itô expansion formula over dual comparison cards (Itô Calculus vs. Mean/Median Divergence).
* **Key Elements:**
  - Governing SDE: $dS_t = \mu S_t dt + \sigma S_t dW_t$ with Wiener process $W_t$.
  - Itô's Lemma Expansion: $d(\ln S_t) = \left(\mu - \frac{1}{2}\sigma^2\right)dt + \sigma dW_t$.
  - The Volatility Drag Gap: Arithmetic mean is $S_0 e^{\mu t}$, but typical median path is $S_0 e^{(\mu - \frac{1}{2}\sigma^2)t}$.
  - Quantitative Finding: For $\mu=12\%$ and $\sigma=20\%$, volatility drag is $-2.00\%$ per year, creating an empirical lag of over ₹6 Lakhs per Million invested.

## Slide 08: Pillar 5 — Monte Carlo Simulation & Quantitative Risk Metrics
* **Core Takeaway:** Central Limit Theorem convergence allows vectorized ensembles to replace static expectations with complete probability densities and Value at Risk (VaR).
* **Layout Structure:** Top CLT convergence formula over dual cards (Ensemble Simulation vs. Downside Risk Metrics).
* **Key Elements:**
  - Vectorized Simulation: 10,000+ stochastic price paths generated in NumPy.
  - Central Limit Theorem: Standard error decays as $\mathcal{O}(1/\sqrt{M})$, narrowing estimation error to $\pm 1\%$.
  - Empirical Goal Attainment: $\hat{\mathbb{P}}(S_T \ge \text{Goal}) = \frac{1}{M}\sum \mathbf{1}_{\{S_{T,m} \ge \text{Goal}\}}$.
  - Tail Risk Metrics: 95% Value at Risk (VaR) and Conditional VaR (Expected Shortfall).

## Slide 09: System Architecture & Automated Verification Pipeline
* **Core Takeaway:** Zero-black-box design where every functional routine maps to first-principles proofs and passes automated floating-point tests to $\epsilon \le 10^{-7}$.
* **Layout Structure:** Horizontal three-tier pipeline flowchart over verification benchmark standards.
* **Key Elements:**
  - Mathematical Core (`models/`) $\to$ Automated Verification (`tests/`) $\to$ Interactive UI (`app.py`).
  - Excel Parity: Cross-benchmarked against PMT, PV, and IRR to $\epsilon \le 10^{-7}$.
  - Boundary Testing: Verified at limits $r \to 0$, $t \to 0$, and infinite frequency $m \to \infty$.
  - Automated Guardrails: Strict domain verification enforcing non-negative parameters via `ValueError`.

## Slide 10: Academic Contributions, Societal Impact & Conclusion
* **Core Takeaway:** Combining 56 pages of rigorous proofs with open-source tools to protect citizens from predatory credit and misleading investments.
* **Layout Structure:** Dual achievement cards over an open defense invitation banner.
* **Key Elements:**
  - Academic Milestones: Completed 12-volume monograph (56 pages) with 24 step-by-step hand-calculated case studies.
  - Societal Relevance: Democratizing hedge-fund stochastic risk modeling for ordinary Indian retail investors.
  - Open Source: MIT licensed on GitHub for full peer reproducibility.
  - Defense Invitation: Open for faculty questions and mathematical viva.
