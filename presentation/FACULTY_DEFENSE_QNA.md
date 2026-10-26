# Faculty Defense & Viva Voce Q&A Guide
### Project Title: *Financial Decision Support System (FDSS) Using Numerical Methods and Monte Carlo Simulation*
**Candidate:** Atharv Ranade  
**Department:** Department of Mathematics & Statistics, University of Mumbai  
**Research Convention Focus:** Avishkar Category 3 (Pure Sciences — Mathematics & Statistics)

---

## Strategic Guide for Candidate

When answering faculty questions during the seminar defense:
1. **Always lead with the mathematical principle** (e.g., *"By the Abel–Ruffini theorem..."* or *"By Itô's Lemma..."*).
2. **Never give a vague "computer programming" answer.** (Do not say: *"The Python library does it."* Say: *"Our algorithm implements the analytical first derivative of the polynomial..."*).
3. **Keep answers concise (20–40 seconds).** State the theorem, state the formula, state the physical/financial interpretation.

---

## 🏛️ Section 1: Research Categorization & Novelty

### Q1: "Why is this project submitted under Category 3 (Pure Sciences) instead of Commerce, Management, or Engineering?"
* **Core Defense:**
  > *"Respected Professors, this investigation is fundamentally rooted in **Applied Mathematics, Real Analysis, and Stochastic Calculus**, rather than commercial accounting or software engineering.
  > 
  > The primary scientific contribution is exposing the mathematical invalidity of **deterministic expectation models** under Jensen's Inequality, proving the non-solvability of multi-period cash flows via the **Abel–Ruffini Theorem**, and demonstrating the analytical divergence between geometric and arithmetic means using **Itô's Lemma**.
  > 
  > Software code and visualizations in our project serve purely as a numerical experimental laboratory to verify mathematical theorems to a precision of $\epsilon \le 10^{-7}$, exactly as computational physics models differential equations."*

---

## 📐 Section 2: Analysis, Calculus & Differential Equations

### Q2: "You presented two governing ODEs: $\frac{dA}{dt} = Pr$ and $\frac{dA}{dt} = rA(t)$. What is their exact mathematical significance?"
* **Core Defense:**
  > *"The two ODEs distinguish between **linear accumulation** and **autonomous exponential growth**:
  > 1. $\frac{dA}{dt} = Pr$ is a non-autonomous linear ODE where growth depends exclusively on the invariant initial condition $P$. Its solution $A(t) = P(1+rt)$ is an arithmetic progression that violates temporal subadditivity: $A(t_1 + t_2) < A(t_1)A(t_2)/P$.
  > 2. $\frac{dA}{dt} = rA(t)$ is a first-order homogeneous autonomous ODE where the instantaneous rate of change is proportional to current accumulated wealth. Separating variables yields $\int \frac{dA}{A} = \int r dt$, which integrates to $A(t) = P e^{rt}$. This satisfies the semigroup property $A(t_1+t_2) = A(t_1)A(t_2)/P$."*

### Q3: "Derive Euler's limit in continuous compounding. How does Euler's constant $e$ arise from discrete compounding?"
* **Core Defense:**
  > *"Starting from discrete compounding with frequency $m$:
  > $$A(t) = \lim_{m \to \infty} P \left(1 + \frac{r}{m}\right)^{mt}$$
  > We perform a substitution: let $x = \frac{m}{r}$, so as $m \to \infty$, $x \to \infty$, and $mt = x \cdot rt$.
  > Substituting $x$ into the expression:
  > $$A(t) = P \left[ \lim_{x \to \infty} \left(1 + \frac{1}{x}\right)^x \right]^{rt}$$
  > By the fundamental definition of the exponential constant in real analysis, $\lim_{x \to \infty} (1 + \frac{1}{x})^x = e$.
  > Therefore, $A(t) = P e^{rt}$."*

---

## 🔢 Section 3: Abstract Algebra & Numerical Root-Finding

### Q4: "You invoked the Abel–Ruffini theorem in your IRR slide. Why does an abstract algebra theorem apply to financial yields?"
* **Core Defense:**
  > *"The Internal Rate of Return equation equates Net Present Value to zero:
  > $$\sum_{t=0}^T \frac{C_t}{(1+r)^t} = 0$$
  > If we substitute the discount variable $x = \frac{1}{1+r}$, this becomes a polynomial equation of degree $T$:
  > $$C_0 + C_1 x + C_2 x^2 + \dots + C_T x^T = 0$$
  > By Galois theory and the **Abel–Ruffini Theorem**, there exists no general algebraic solution in radicals for polynomial equations of degree $T \ge 5$.
  > Because real-world loans, mortgages, and business cash flows regularly extend beyond 4 periods (e.g., 5-year bonds or 20-year mortgages), exact radical formulas are mathematically impossible. Hence, finding the yield strictly necessitates **numerical analysis**."*

### Q5: "Why did you choose Newton–Raphson over simple polynomial solvers? What happens if Newton–Raphson oscillates or diverges?"
* **Core Defense:**
  > *"Newton–Raphson was selected because it achieves **quadratic convergence** ($\mathcal{O}(e_k^2)$), doubling the number of correct significant digits with every iteration. Furthermore, the financial polynomial has a known closed-form analytical first derivative:
  > $$f'(r) = -\sum_{t=1}^T \frac{t \cdot C_t}{(1+r)^{t+1}}$$
  > which avoids expensive finite-difference approximations.
  > 
  > However, if cash flows are non-conventional—exhibiting multiple sign changes where Descartes' Rule of Signs indicates multiple real roots—the derivative can approach zero ($f'(r) \approx 0$). In our engine, if Newton–Raphson does not converge within 50 iterations or encounters a zero derivative, it automatically triggers a **Bisection Method fallback** on a bounded interval $[a, b]$ where $f(a) \cdot f(b) < 0$, guaranteeing robust linear convergence."*

---

## 📈 Section 4: Stochastic Calculus & Statistics

### Q6: "Where does the Itô correction term $-\frac{1}{2}\sigma^2$ come from in Geometric Brownian Motion?"
* **Core Defense:**
  > *"In classical deterministic calculus, Taylor's theorem allows us to discard terms of order $(dt)^2$ because they vanish faster than $dt$.
  > 
  > However, in stochastic calculus, the increment of a standard Brownian motion $dW_t$ has variance $\mathbb{E}[(dW_t)^2] = dt$. Therefore, by quadratic variation, $(dW_t)^2 = dt$, which is of first order!
  > 
  > Applying **Itô's Lemma** to the transformation $f(S) = \ln S$:
  > $$df = f'(S) dS + \frac{1}{2} f''(S) (dS)^2$$
  > Since $f'(S) = \frac{1}{S}$ and $f''(S) = -\frac{1}{S^2}$, and from the SDE $(dS)^2 = \sigma^2 S^2 dt$:
  > $$d(\ln S) = \frac{1}{S}(\mu S dt + \sigma S dW) + \frac{1}{2}\left(-\frac{1}{S^2}\right)(\sigma^2 S^2 dt)$$
  > Simplifying yields:
  > $$d(\ln S) = \left(\mu - \frac{1}{2}\sigma^2\right)dt + \sigma dW_t$$
  > The term $-\frac{1}{2}\sigma^2$ arises strictly from the non-zero second derivative $f''(S)$ interacting with the quadratic variation of Brownian paths."*

### Q7: "What is Volatility Drag, and why does the median trajectory underperform the arithmetic mean?"
* **Core Defense:**
  > *"Because the exponential function is strictly convex, asset prices under Geometric Brownian Motion are **lognormally distributed**, which introduces positive right-tail skewness.
  > 
  > The arithmetic expected mean is pulled upward by a small number of extraordinarily high-performing paths:
  > $$\mathbb{E}[S_t] = S_0 e^{\mu t}$$
  > However, because the normal distribution of log-returns is symmetric around its drift $(\mu - \frac{1}{2}\sigma^2)$, the **median path**—which separates the top 50% from the bottom 50% of real outcomes—is:
  > $$S_{\text{median}}(t) = S_0 e^{(\mu - \frac{1}{2}\sigma^2)t}$$
  > The difference $-\frac{1}{2}\sigma^2$ is the **volatility drag**. For an equity portfolio with $\mu = 12\%$ and $\sigma = 20\%$, the annual drag is $2.00\%$. Over ten years, more than 50% of investors will achieve wealth strictly below the arithmetic average."*

### Q8: "Why choose 10,000 paths for your Monte Carlo simulation? What governs its convergence speed?"
* **Core Defense:**
  > *"The convergence of Monte Carlo integration is governed by the **Central Limit Theorem**, which dictates that standard error decays at the rate:
  > $$\text{Standard Error} = \frac{\sigma_{\text{sample}}}{\sqrt{M}} = \mathcal{O}\left(\frac{1}{\sqrt{M}}\right)$$
  > Crucially, this convergence rate is independent of the dimensionality of the problem.
  > 
  > When $M = 10,000$, $\frac{1}{\sqrt{M}} = \frac{1}{100} = 0.01$. This guarantees that our empirical estimates for terminal wealth percentiles and Value at Risk (VaR) achieve an estimation precision within $\pm 1\%$ of the true distribution variance while executing in sub-second vectorized NumPy runtime."*

---

## 💳 Section 5: Consumer Debt & Applied Relevance

### Q9: "Explain the Negative Amortization Boundary condition in your loan module."
* **Core Defense:**
  > *"Let a loan principal be $P$, monthly interest rate be $R = \frac{r}{12}$, and fixed monthly installment be $E$.
  > In the first month, the interest accrued on the debt is $I_1 = P \cdot R$.
  > The principal repaid in month 1 is:
  > $$P_1 = E - I_1 = E - P \cdot R$$
  > If a lender structures a predatory or 'minimum payment' loan where $E \le P \cdot R$, then $P_1 \le 0$.
  > The unpaid interest is capitalized into the principal, causing the outstanding balance recurrence $B_k = B_{k-1}(1+R) - E$ to monotonically diverge toward positive infinity:
  > $$\lim_{n \to \infty} B_n = +\infty$$
  > Our system establishes the strict mathematical boundary condition: a debt amortizes if and only if $E > P \cdot \frac{r}{12}$."*

### Q10: "How do you verify the numerical accuracy of your software implementation?"
* **Core Defense:**
  > *"We enforce a three-stage verification methodology:
  > 1. **Axiomatic Hand Benchmarking:** Every algorithm is cross-checked against step-by-step paper calculations derived in our 56-page monograph.
  > 2. **Standard Reference Comparison:** Deterministic models are checked against IEEE 754 double-precision Microsoft Excel functions (PMT, PV, IRR) down to an absolute floating-point tolerance of $\epsilon \le 10^{-7}$.
  > 3. **Boundary Value Testing in `pytest`:** The test suite verifies mathematical limits, such as verifying that $A(t) \to P$ as $r \to 0$ or $t \to 0$, that continuous compounding matches discrete limits as $m \to 10^6$, and that illegal domains (e.g., negative principal, $r < -1$) reliably trigger `ValueError` exceptions."*
