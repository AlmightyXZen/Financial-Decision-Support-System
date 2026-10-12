# Aavishkar Research Convention — Project Synopsis
### University of Mumbai | Department of Students' Development (DSD)

---

## 1. Project Identification

* **Project Title:** Development of a Financial Decision Support System Using Numerical Methods and Monte Carlo Simulation
* **Category:** Category 3 — Pure Sciences (PS)
* **Level:** Level 1 — Undergraduate (UG)
* **Author / Principal Investigator:** Atharv Ranade
* **Degree / Major:** B.Sc. Mathematics (Minor: Statistics)
* **Institution:** Department of Mathematics, University of Mumbai
* **Academic Discipline:** Applied Mathematics, Numerical Analysis & Financial Stochastics

---

## 2. Statement of the Research Problem

Retail financial planning tools and commercial web calculators suffer from a pervasive structural defect: **the deterministic fallacy**. Conventional calculators assume a static, invariant rate of return (e.g., claiming a Systematic Investment Plan will compound steadily at $12\%$ per annum over 25 years). 

In empirical financial markets, returns are stochastic, volatile, and time-dependent. Static projections ignore:
1. **Volatility Drag:** Compounded growth is governed by the geometric mean, which is systematically lower than the arithmetic mean ($\mu - \frac{1}{2}\sigma^2$).
2. **Sequence of Returns Risk:** Severe early drawdowns decimate a compounding corpus, a phenomenon completely concealed by linear formulas.
3. **Absence of Risk Metrics:** Deterministic calculators output a single optimistic point estimate with $0\%$ probability of actually occurring, concealing the probability of capital shortfall.

---

## 3. Research Hypothesis

> *By replacing deterministic point projections with numerical root-finding schemes and continuous-time stochastic differential equations (Geometric Brownian Motion simulated via Monte Carlo methods), a decision-support system can quantify downside tail risk, empirical terminal wealth distributions, and the true probability of financial goal attainment.*

---

## 4. Key Objectives

1. **Analytical Formulation:** Derive exact closed-form expressions for discrete vs. continuous compounding limits ($\lim_{n \to \infty} P(1 + r/n)^{nt} = P e^{rt}$), debt amortization schedules, and real inflation-discounted purchasing power.
2. **Numerical Root-Finding for Yield Analysis:** Formulate and implement the **Newton–Raphson** algorithm utilizing the analytical first derivative of irregular discounted cash flows, accompanied by a **Bisection** bracket fallback, to solve for the Internal Rate of Return (IRR) where the Abel–Ruffini theorem precludes closed-form algebraic solutions for $N > 4$.
3. **Stochastic Simulation Engine:** Implement a vectorized Euler–Maruyama discretization of **Geometric Brownian Motion (GBM)** based on Itô's Lemma to simulate $10,000+$ independent portfolio trajectories, reporting empirical percentiles ($5^{\text{th}}, 50^{\text{th}}, 95^{\text{th}}$) and Value at Risk (VaR).
4. **Verification & Testing Protocol:** Benchmark all deterministic algorithms against analytical hand calculations and Microsoft Excel financial specifications within floating-point error bounds ($\epsilon \le 10^{-5}$), with automated unit testing via `pytest`.
5. **Interactive Public Interface:** Deploy an open-source, interactive web application using Streamlit to democratize quantitative analysis for students, retail investors, and researchers.

---

## 5. Mathematical & Algorithmic Methodology

### 5.1 Continuous Compounding Limits
Analyzing the transition from periodic discrete compounding to continuous financial time:
$$\lim_{n \to \infty} P \left(1 + \frac{r}{n}\right)^{nt} = P \exp(rt)$$

### 5.2 Numerical Analysis of Cash Flow Yields
For cash flows $\{C_0, C_1, \dots, C_T\}$, the Internal Rate of Return ($r^*$) satisfies:
$$f(r) = \sum_{t=0}^T \frac{C_t}{(1 + r)^t} = 0$$
Because $f(r)$ is a polynomial of degree $T$, root finding requires iterative numerical schemes:
* **Newton–Raphson Scheme:**
  $$r_{k+1} = r_k - \frac{f(r_k)}{f'(r_k)}, \quad f'(r) = -\sum_{t=1}^T \frac{t \cdot C_t}{(1 + r)^{t+1}}$$
* **Bisection Scheme:** Applied when $f(a) \cdot f(b) < 0$ to guarantee bracketed convergence at rate $\mathcal{O}(2^{-k})$.

### 5.3 Stochastic Modeling via Geometric Brownian Motion (GBM)
Asset dynamics are governed by the stochastic differential equation (SDE):
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$
Applying **Itô's Lemma** yields the discrete time-stepping equation:
$$S_{t + \Delta t} = S_t \exp\left[\left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} Z\right], \quad Z \sim \mathcal{N}(0, 1)$$

By the **Central Limit Theorem**, simulating $M$ paths produces an empirical estimator with standard error decreasing at rate $\mathcal{O}(M^{-1/2})$, providing:
* Terminal wealth probability density function (PDF).
* Objective target attainment probability: $\hat{P}(S_T \ge \Gamma) = \frac{1}{M}\sum_{m=1}^M \mathbf{1}_{\{S_{T, m} \ge \Gamma\}}$.

---

## 6. Innovation & Novelty

* **Shifting Paradigm from Single Point to Distribution:** First open-source undergraduate tool to directly confront the misleading certainty of standard retail calculators by displaying full probability distributions and tail risks.
* **Algorithmic Transparency:** Avoids black-box libraries; implements explicit numerical root-finding and stochastic path generation from mathematical first principles.
* **Dual Theoretical & Empirical Grounding:** Connects pure mathematics (calculus limits, Galois polynomial theory, probability distributions) with practical personal finance.

---

## 7. Societal Relevance & Economic Impact (Avishkar Criteria)

* **Financial Literacy & Protection Against Mis-selling:** Retail investors in India and developing economies frequently fall victim to predatory investment schemes due to exaggerated promises of linear compounding. This system empowers the public with realistic probability distributions.
* **Accessible Open-Source Education:** The framework is fully open-source, modular, and accompanied by formal mathematical derivations, serving as a pedagogical tool for mathematics, economics, and finance students.

---

## 8. Presentation & Demonstration Plan

* **Poster Component:** Displays the mathematical derivations of limits, numerical iteration tables comparing Newton-Raphson vs Bisection, and visual trajectory charts of Geometric Brownian Motion paths.
* **Interactive Live Demo:** A responsive Streamlit dashboard allowing judges to alter volatility ($\sigma$), drift ($\mu$), and time horizons ($T$) in real time to witness simulated probability densities shift instantly.
