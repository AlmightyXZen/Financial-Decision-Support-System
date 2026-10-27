# Faculty Defense & Viva Voce Q&A Guide
### Project Title: *Financial Decision Support System (FDSS)*
**Subtitle:** *Numerical Methods and Monte Carlo Simulation*  
**Team Members:** Atharv Ranade • Danish Shaikh • Abhijeet  
**Presenter:** Danish Shaikh  

---

## 📌 Defense Rules for Danish
* **Lead with the Theorem:** Always state the mathematical theorem first before explaining practical details.
* **Keep it Under 30 Seconds:** Clear, punchy, bulleted answers. Zero hesitation.
* **Point to the Proofs:** Mention our 12-volume reference monograph (`theory_and_derivations/`) as proof of rigorous first-principles derivations.

---

### Q1: "Why is this project an applied mathematics and numerical analysis project rather than a commercial financial calculator?"
* **Direct Answer:**
  * *"Because the core scientific contribution is the **mathematical modeling of capital accumulation under uncertainty and numerical convergence bounds**—not a commercial application."*
  * *"We mathematically prove why deterministic expectations break down under **Jensen's Inequality**."*
  * *"We apply **Galois Theory (the Abel–Ruffini Theorem)** to demonstrate the non-existence of radical solutions for multi-period yields, mandating numerical analysis."*
  * *"We derive the volatility drag correction $-\frac{1}{2}\sigma^2$ strictly via **Itô's Lemma in Stochastic Calculus**."*

---

### Q2: "What is the analytical distinction between your two governing ODEs: $\frac{dA}{dt} = Pr$ and $\frac{dA}{dt} = rA(t)$?"
* **Direct Answer:**
  * *"$\frac{dA}{dt} = Pr$ represents **linear accumulation (Simple Interest)**. The growth rate is constant and non-autonomous, depending only on the initial principal $P$. Its solution $A(t) = P(1+rt)$ violates subadditivity: $A(t_1+t_2) < \frac{A(t_1)A(t_2)}{P}$ because accrued interest is never reinvested."*
  * *"$\frac{dA}{dt} = rA(t)$ represents **autonomous exponential growth (Continuous Compounding)**. The growth rate is proportional to instantaneous wealth. Its solution $A(t) = P e^{rt}$ satisfies the semigroup property $A(t_1+t_2) = \frac{A(t_1)A(t_2)}{P}$, making continuous log-returns linearly additive across time."*

---

### Q3: "How does Euler's constant $e$ arise from the discrete compound interest formula?"
* **Direct Answer:**
  * *"Starting with discrete compounding frequency $m$:
    $$A(t) = \lim_{m \to \infty} P \left(1 + \frac{r}{m}\right)^{mt}$$"*
  * *"We substitute $x = \frac{m}{r}$, so that as $m \to \infty$, $x \to \infty$, and $mt = x \cdot rt$."*
  * *"This rearranges to:
    $$A(t) = P \left[ \lim_{x \to \infty} \left(1 + \frac{1}{x}\right)^x \right]^{rt}$$"*
  * *"By the classical definition of Euler's constant from real analysis, $\lim_{x \to \infty} (1 + 1/x)^x = e$. Therefore, $A(t) = P e^{rt}$."*

---

### Q4: "Why does the Abel–Ruffini theorem apply to the Internal Rate of Return (IRR)?"
* **Direct Answer:**
  * *"The IRR equation equates the Net Present Value polynomial to zero:
    $$\text{NPV}(r) = \sum_{t=0}^T \frac{C_t}{(1+r)^t} = 0$$"*
  * *"Substituting $x = \frac{1}{1+r}$ yields a standard algebraic polynomial of degree $T$:
    $$\sum_{t=0}^T C_t x^t = 0$$"*
  * *"By the **Abel–Ruffini Theorem in Galois Theory**, general polynomial equations of degree $T \ge 5$ have **no algebraic solution in radicals**."*
  * *"Since multi-period capital projects routinely exceed 4 periods (e.g., 5-year bonds or 20-year loans), calculating the financial yield **fundamentally mandates numerical root-finding**."*

---

### Q5: "Why did you implement Newton–Raphson, and what happens if it oscillates or diverges?"
* **Direct Answer:**
  * *"We chose Newton–Raphson because it provides **quadratic convergence** ($\mathcal{O}(e_k^2)$), doubling significant digits each step using the exact analytical first derivative:
    $$f'(r) = -\sum_{t=1}^T \frac{t \cdot C_t}{(1+r)^{t+1}}$$
    avoiding finite-difference rounding errors."*
  * *"If cash flows exhibit non-conventional sign changes where derivatives approach zero or oscillate, our solver automatically triggers a **Bisection Method fallback** on a bracketed interval $[a, b]$ where $f(a) \cdot f(b) < 0$, guaranteeing robust linear convergence."*

---

### Q6: "Where does the term $-\frac{1}{2}\sigma^2$ come from in Geometric Brownian Motion?"
* **Direct Answer:**
  * *"It originates strictly from the **non-zero quadratic variation of Brownian Motion**: $(dW_t)^2 = dt$."*
  * *"In classical Taylor calculus, second-order differentials $(dt)^2$ vanish. But in stochastic calculus, $(dW_t)^2 = dt$ contributes directly to the first-order drift."*
  * *"Applying **Itô's Lemma** to $f(S) = \ln S$ with $f'(S) = \frac{1}{S}$ and $f''(S) = -\frac{1}{S^2}$:
    $$df = f'(S) dS + \frac{1}{2} f''(S) (dS)^2$$
    $$d(\ln S) = \frac{1}{S}(\mu S dt + \sigma S dW) + \frac{1}{2}\left(-\frac{1}{S^2}\right)(\sigma^2 S^2 dt)$$
    $$d(\ln S) = \left(\mu - \frac{1}{2}\sigma^2\right)dt + \sigma dW_t$$"*
  * *"The term $-\frac{1}{2}\sigma^2$ is the direct mathematical consequence of the negative second derivative interacting with Brownian variance."*

---

### Q7: "What is Volatility Drag, and why does the median trajectory lag the arithmetic mean?"
* **Direct Answer:**
  * *"Asset prices under Geometric Brownian Motion are **lognormally distributed**, which introduces positive right-tail skewness."*
  * *"The expected arithmetic mean $\mathbb{E}[S_t] = S_0 e^{\mu t}$ is heavily pulled upward by rare, extreme positive outliers."*
  * *"However, the **median path**—which 50% of investors fail to achieve—is strictly:
    $$S_{\text{median}}(t) = S_0 e^{(\mu - \frac{1}{2}\sigma^2)t}$$"*
  * *"The difference $-\frac{1}{2}\sigma^2$ is the **volatility drag**. For $\mu = 12\%$ and $\sigma = 20\%$, the annual drag is $2.00\%$. Over 10 years, more than half of retail investors fall short of the advertised arithmetic expectation."*

---

### Q8: "Why simulate 10,000 paths in Monte Carlo? What governs the convergence speed?"
* **Direct Answer:**
  * *"Monte Carlo convergence is governed by the **Central Limit Theorem**, which guarantees that the standard error of the estimator decays as:
    $$\text{Standard Error} = \frac{\sigma_{\text{sample}}}{\sqrt{M}} = \mathcal{O}\left(\frac{1}{\sqrt{M}}\right)$$
    regardless of model dimensionality."*
  * *"For $M = 10,000$, $\frac{1}{\sqrt{M}} = 0.01$. This guarantees that our empirical estimates for terminal wealth percentiles and 95% Value at Risk (VaR) narrow to within $\pm 1\%$ of sample variance in sub-second vectorized NumPy runtime."*

---

### Q9: "Explain the Negative Amortization Boundary condition in your loan module."
* **Direct Answer:**
  * *"Let $P$ be principal, monthly rate $R = \frac{r}{12}$, and monthly installment $E$. First-month interest accrued is $I_1 = P \cdot R$. The principal repaid is $P_1 = E - P \cdot R$."*
  * *"If $E \le P \cdot R$, principal reduction is zero or negative ($P_1 \le 0$)."*
  * *"The unpaid interest is added to the debt, causing the loan balance recurrence sequence to monotonically diverge:
    $$\lim_{n \to \infty} B_n = +\infty$$"*
  * *"Our theorem proves that a loan amortizes to zero if and only if $E > P \cdot \frac{r}{12}$. This mathematically identifies predatory credit card and teaser-rate loans."*

---

### Q10: "How do you verify the numerical accuracy of your software?"
* **Direct Answer:**
  * *"We enforce three rigorous verification layers:
    1. **Analytical Hand Benchmarking:** All formulas are validated against 24 hand-solved cases in our 56-page monograph down to exact rupee arithmetic.
    2. **Parity with Microsoft Excel Standards:** Deterministic functions (PMT, PV, IRR) are cross-checked against IEEE 754 double precision to an absolute tolerance of $\epsilon \le 10^{-7}$.
    3. **Automated Boundary Testing:** Our automated `pytest` suite tests singular limits ($r \to 0$, $t \to 0$, $m \to \infty$) and enforces domain guardrails with strict `ValueError` exceptions."*
