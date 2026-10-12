# Mathematical Specifications & Algorithmic Blueprint

This document outlines the rigorous mathematical and numerical specifications powering the **Financial Decision Support System (FDSS)**. It serves as both the technical appendix for the **Avishkar Research Convention** submission and the theoretical foundation for academic portfolio review.

---

## 1. Time Value of Money (TVM) & Compounding Dynamics

### 1.1 Simple & Discrete Compound Interest
For principal $P$, nominal annual interest rate $r \in [0, \infty)$, and time horizon $t \ge 0$:

* **Simple Interest:**
  $$SI = P \cdot r \cdot t$$
  $$A_{\text{simple}} = P(1 + r \cdot t)$$

* **Discrete Compounding ($n$ compoundings per year):**
  $$A(t) = P \left(1 + \frac{r}{n}\right)^{nt}$$

### 1.2 Continuous Compounding (Real Analysis Perspective)
In continuous financial mathematics, interest is compounded infinitely often ($n \to \infty$):
$$\lim_{n \to \infty} P \left(1 + \frac{r}{n}\right)^{nt} = P \exp(rt)$$
* **Discounting Factor:** $D(t) = \exp(-rt)$
* **Continuous Present Value:** $PV = FV \cdot \exp(-rt)$

### 1.3 Effective Annual Rate (EAR)
Standardizes nominal annual rates $r$ with compounding frequency $n$:
$$\text{EAR} = \left(1 + \frac{r}{n}\right)^n - 1$$
$$\text{EAR}_{\text{continuous}} = \exp(r) - 1$$

---

## 2. Annuities, Loans & Amortization Mechanics

### 2.1 Equated Monthly Installment (EMI)
For loan principal $P$, periodic monthly interest rate $r_m = \frac{r}{12}$, and total payment periods $N = 12 \cdot t$:
The present value of $N$ equal periodic cash flows $E$ must equate to principal $P$:
$$P = \sum_{k=1}^N \frac{E}{(1 + r_m)^k} = E \left[\frac{1 - (1 + r_m)^{-N}}{r_m}\right]$$

Inverting yields the closed-form EMI formula:
$$E = P \cdot \frac{r_m (1 + r_m)^N}{(1 + r_m)^N - 1}$$

### 2.2 Amortization Breakdown (Period $k$)
For outstanding balance $B_{k-1}$:
* **Interest component:** $I_k = B_{k-1} \cdot r_m$
* **Principal component:** $P_k = E - I_k$
* **New balance:** $B_k = B_{k-1} - P_k$

---

## 3. Systematic Investment Plans (SIP) & Inflation Adjustment

### 3.1 Future Value of Periodic Contributions (Annuity Due)
Assuming regular monthly contribution $C$, monthly return $r_m$, and tenure $N$ months, where payments occur at the beginning of each period:
$$FV_{\text{SIP}} = C \cdot \sum_{k=1}^N (1 + r_m)^k = C \cdot \frac{(1 + r_m) \left[(1 + r_m)^N - 1\right]}{r_m}$$

### 3.2 Real Purchasing Power (Inflation Drag)
For annual inflation rate $i$:
$$FV_{\text{real}} = \frac{FV_{\text{nominal}}}{(1 + i)^t}$$

---

## 4. Capital Budgeting & Numerical Root-Finding

### 4.1 Net Present Value (NPV)
For an initial cash outflow $C_0 < 0$ and subsequent periodic cash flows $\{C_1, C_2, \dots, C_T\}$ discounted at hurdle rate $r$:
$$\text{NPV}(r) = \sum_{t=0}^T \frac{C_t}{(1 + r)^t}$$

### 4.2 Internal Rate of Return (IRR) as a Root-Finding Problem
The IRR $r^*$ is the discount rate satisfying:
$$f(r) = \text{NPV}(r) = \sum_{t=0}^T \frac{C_t}{(1 + r)^t} = 0$$

Because $f(r) = 0$ is a non-linear polynomial of degree $T$, closed-form algebraic solutions do not exist for $T > 4$ (Abel-Ruffini theorem). We employ numerical analysis:

#### Method A: Newton-Raphson Iteration
Given derivative:
$$f'(r) = -\sum_{t=1}^T \frac{t \cdot C_t}{(1 + r)^{t+1}}$$
The iterative update sequence is:
$$r_{k+1} = r_k - \frac{f(r_k)}{f'(r_k)}$$
Stopping criterion: $|f(r_k)| < \epsilon$ or $|r_{k+1} - r_k| < \delta$ where $\epsilon, \delta = 10^{-7}$.

#### Method B: Bisection Algorithm (Fallback Bracket)
When Newton-Raphson encounters local extrema ($f'(r) \approx 0$) or oscillation, Bisection operates on an interval $[a, b]$ where $f(a) \cdot f(b) < 0$, guaranteeing convergence at linear rate:
$$r_{\text{mid}} = \frac{a + b}{2}$$

---

## 5. Stochastic Modeling & Monte Carlo Simulation

### 5.1 Asset Price Dynamics (Geometric Brownian Motion)
Rather than relying on misleading deterministic returns, portfolio asset dynamics are modeled via the stochastic differential equation (SDE):
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$
where $\mu$ is expected drift, $\sigma$ is annualized volatility, and $W_t$ is a standard Wiener process ($dW_t \sim \mathcal{N}(0, dt)$).

By **Itô's Lemma**, the exact discrete solution over time step $\Delta t$ is:
$$S_{t + \Delta t} = S_t \exp\left[\left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} Z\right], \quad Z \sim \mathcal{N}(0, 1)$$

### 5.2 Simulation Execution & Statistical Estimators
For $M$ Monte Carlo paths simulated across $K$ periods:
* **Terminal Wealth Vector:** $\mathbf{W}_T = \{W_{T, 1}, W_{T, 2}, \dots, W_{T, M}\}$
* **Empirical Expected Value:** $\hat{\mu}_{W} = \frac{1}{M}\sum_{m=1}^M W_{T, m}$
* **Standard Error of Estimate:** $\text{SE} = \frac{s_W}{\sqrt{M}} = \mathcal{O}\left(M^{-1/2}\right)$
* **Target Achievement Probability:**
  $$\hat{P}(W_T \ge \Gamma) = \frac{1}{M} \sum_{m=1}^M \mathbf{1}_{\{W_{T, m} \ge \Gamma\}}$$
* **Downside Tail Risk (Empirical VaR at $\alpha = 95\%$):**
  $$\text{VaR}_{95\%} = W_0 - \text{Percentile}(\mathbf{W}_T, 5)$$

---

## 6. Verification & Validation Protocol
All modules are subjected to a dual verification system:
1. **Analytical Benchmark:** Validated against closed-form mathematical equations and hand-calculated limits.
2. **Deterministic Cross-Check:** Cross-referenced against industry-standard financial functions in Microsoft Excel and Python `numpy-financial` tolerances ($10^{-5}$).
3. **Automated Unit Testing:** Enforced via `pytest` for normal, boundary ($r=0, t=0$), and invalid negative inputs.
