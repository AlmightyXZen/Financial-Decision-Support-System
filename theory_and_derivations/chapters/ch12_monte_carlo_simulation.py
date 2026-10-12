"""
Chapter 12: Monte Carlo Simulation & Quantitative Risk Analysis.
Textbook chapter on stochastic simulation, Central Limit Theorem convergence rates,
empirical percentiles, goal attainment probabilities, Value at Risk (VaR), and vectorized Python code.
"""

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
)
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import TextbookCanvas, get_textbook_styles, get_textbook_palette, make_card, make_code_card

def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=46,
        bottomMargin=44
    )

    styles = get_textbook_styles()
    pal = get_textbook_palette()
    story = []

    # ==================== PAGE 1: THEORY & CLT CONVERGENCE ====================
    story.append(Paragraph("CHAPTER 12", styles['ChapterLabel']))
    story.append(Paragraph("Monte Carlo Simulation & Quantitative Risk Analysis", styles['ChapterTitle']))
    story.append(Paragraph(
        "Vectorized Stochastic Ensembles, The Central Limit Theorem, Goal Attainment Probabilities, and Value at Risk",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=7))

    story.append(Paragraph("12.1 The Paradigm Shift: From Point Estimates to Probability Densities", styles['H1']))
    story.append(Paragraph(
        "Traditional retail calculators suffer from **deterministic expectation bias**: they present investors with a single, "
        "static future corpus assuming zero market volatility. In reality, market outcomes form an entire **probability distribution**. "
        "**Monte Carlo simulation** bridges this gap by generating thousands of independent stochastic price trajectories, "
        "revealing downside tail risks, median paths, and empirical goal attainment odds.",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 12.1 (Monte Carlo Estimator & Law of Large Numbers)</b>", styles['DefHeader']),
        Paragraph(
            "Let <i>M</i> be the number of independent simulated market paths, and let <i>S</i><sub><i>T</i>, <i>m</i></sub> "
            "denote the terminal asset price for path <i>m</i> &in; {1, 2, ..., <i>M</i>}.<br/>"
            "By the <b>Strong Law of Large Numbers (SLLN)</b>, the empirical sample mean converges almost surely to the true expectation:",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("lim<sub><i>M</i>&rarr;&infin;</sub> (1 / <i>M</i>) &sum;<sub><i>m</i>=1</sub><sup><i>M</i></sup> <i>g</i>(<i>S</i><sub><i>T</i>, <i>m</i></sub>) = &#120124;[<i>g</i>(<i>S</i><sub><i>T</i></sub>)] &nbsp;&nbsp;(a.s.)", styles['Equation']),
        Spacer(1, 2),
        Paragraph("The <b>Target Goal Attainment Probability</b> for financial target &Gamma; is &Phi;̂(&Gamma;) = (1/<i>M</i>) &sum;<sub><i>m</i>=1</sub><sup><i>M</i></sup> &#120793;<sub>{<i>S</i><sub><i>T</i>, <i>m</i></sub> &ge; &Gamma;}</sub>.", styles['EquationSub'])
    ]
    story.append(make_card(def_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 5))

    story.append(Paragraph("12.2 Convergence Rate & Asymptotic Standard Error", styles['H1']))
    story.append(Paragraph(
        "<b>The Central Limit Theorem (CLT) Error Bound:</b><br/>"
        "Let &sigma;̂<sub><i>g</i></sub> denote the sample standard deviation of terminal simulated outcomes. "
        "By the Central Limit Theorem, the statistical error of the Monte Carlo estimator decays strictly at rate:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <b>Standard Error:</b> SE = &sigma;̂<sub><i>g</i></sub> / &radic;<i>M</i> = <i>O</i>(<i>M</i><sup>&minus;1/2</sup>).<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <b>Dimension Independence:</b> Unlike deterministic numerical quadrature (whose error explodes exponentially "
        "in higher dimensions as <i>O</i>(<i>N</i><sup>&minus;1/<i>d</i></sup>)), the Monte Carlo convergence rate <i>O</i>(<i>M</i><sup>&minus;1/2</sup>) "
        "is <b>strictly independent of dimension</b>. This makes simulation the preeminent tool for multi-asset portfolios and stochastic paths.",
        styles['Body']
    ))

    # Risk Metrics Box
    th_content = [
        Paragraph("<b>Theorem 12.1 (Quantitative Risk Metrics: Percentiles & Value at Risk)</b>", styles['DefHeader']),
        Paragraph(
            "For terminal wealth distribution vector <b>W</b><sub><i>T</i></sub> = {<i>W</i><sub><i>T</i>, 1</sub>, ..., <i>W</i><sub><i>T</i>, <i>M</i></sub>}:<br/>"
            "&nbsp;&nbsp;&bull;&nbsp; <b>Median Expected Wealth:</b> <i>P</i><sub>50</sub> = Percentile(<b>W</b><sub><i>T</i></sub>, 50)<br/>"
            "&nbsp;&nbsp;&bull;&nbsp; <b>Downside Bear Scenario (5th Percentile):</b> <i>P</i><sub>5</sub> = Percentile(<b>W</b><sub><i>T</i></sub>, 5)<br/>"
            "&nbsp;&nbsp;&bull;&nbsp; <b>Empirical Value at Risk (VaR at 95% Confidence):</b><br/>"
            "<font size=10><b>VaR<sub>95%</sub> = <i>W</i><sub>0</sub> &minus; <i>P</i><sub>5</sub> &nbsp; (or relative: <i>P</i><sub>50</sub> &minus; <i>P</i><sub>5</sub>)</b></font>",
            styles['Body']
        ),
        Paragraph(
            "<i>Decision Support Value:</i> VaR quantifies the maximum capital drawdown expected under 95% of all market states, "
            "allowing investors to stress-test financial plans before committing capital.",
            styles['Body']
        )
    ]
    story.append(make_card(th_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLE 12.1 ====================
    story.append(Paragraph("12.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: analytical goal attainment probability estimation, "
        "and empirical 10,000-path statistical error bounds with Value at Risk.",
        styles['Body']
    ))

    # Example 12.1 Card
    ex1_content = [
        Paragraph("<b>Example 12.1: Analytical Target Goal Attainment Probability</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> An investor commits <b><i>S</i><sub>0</sub> = INR 1,000,000</b> into a portfolio with "
            "expected drift <b>&mu; = 12.00%</b> and volatility <b>&sigma; = 20.00%</b> for <b><i>t</i> = 10 years</b>. "
            "The investor sets an ambitious milestone target of <b>&Gamma; = INR 5,000,000</b> (5x capital replication). "
            "Calculate the exact analytical probability <i>P</i>(<i>S</i><sub>10</sub> &ge; &Gamma;) and contrast with deterministic projections.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Transform to Lognormal Standard Normal Variable):</b><br/>"
            "&nbsp;&nbsp;From Chapter 11, ln(<i>S</i><sub><i>t</i></sub>) &sim; &#119977;[ ln(<i>S</i><sub>0</sub>) + (&mu;&minus;&sigma;<sup>2</sup>/2)<i>t</i>, &nbsp; &sigma;<sup>2</sup><i>t</i> ].<br/>"
            "&nbsp;&nbsp;&bull; Expected log mean: &mu;<sub>log</sub> = ln(1,000,000) + [0.12 &minus; (0.04/2)] &times; 10 = 13.815511 + (0.10 &times; 10) = <b>14.815511</b>.<br/>"
            "&nbsp;&nbsp;&bull; Log variance: &sigma;<sub>log</sub><sup>2</sup> = (0.20)<sup>2</sup> &times; 10 = 0.4000 &rArr; Standard Deviation: &sigma;<sub>log</sub> = &radic;0.40 &approx; <b>0.6324555</b>.<br/><br/>"
            "<b>Step 2 (Evaluate Target Logarithm & Z-Score):</b><br/>"
            "&nbsp;&nbsp;&bull; Target log: ln(&Gamma;) = ln(5,000,000) &approx; <b>15.424949</b>.<br/>"
            "&nbsp;&nbsp;&bull; Standard normal <i>Z</i>-statistic:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>Z</i> = [ ln(&Gamma;) &minus; &mu;<sub>log</sub> ] / &sigma;<sub>log</sub> = [ 15.424949 &minus; 14.815511 ] / 0.6324555 "
            "= 0.609438 / 0.6324555 &approx; <b>+0.963606</b>.<br/><br/>"
            "<b>Step 3 (Probability Computation via Standard Normal CDF &Phi;):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>P</i>(<i>S</i><sub>10</sub> &ge; 5,000,000) = 1 &minus; &Phi;(0.9636).<br/>"
            "&nbsp;&nbsp;&bull; From standard normal tables: &Phi;(0.9636) &approx; 0.83238.<br/>"
            "&nbsp;&nbsp;&bull; <b>Target Attainment Probability:</b> 1 &minus; 0.83238 = 0.16762 &implies; <b>16.76% success odds</b>.<br/><br/>"
            "<b>Step 4 (Deterministic Fallacy vs. Stochastic Reality):</b><br/>"
            "&nbsp;&nbsp;&bull; Deterministic Calculator Projection: 1,000,000 &times; (1.12)<sup>10</sup> = INR 3,105,848 (or continuous INR 3,320,117).<br/>"
            "&nbsp;&nbsp;&bull; <i>Crucial Insight:</i> A static calculator provides no probability metric. An investor targeting INR 5 Million "
            "might mistakenly believe their target is reasonably achievable, when the empirical mathematical reality reveals an <b>83.24% failure risk!</b>",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 3: WORKED EXAMPLE 12.2 ====================
    # Example 12.2 Card
    ex2_content = [
        Paragraph("<b>Example 12.2: 10,000-Path Simulation Statistics & Value at Risk (VaR)</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> A 10,000-path Monte Carlo simulation is executed on an equity investment of "
            "<b><i>S</i><sub>0</sub> = INR 1,000,000</b> over a <b><i>t</i> = 1-year horizon</b> with drift <b>&mu; = 14.0%</b> "
            "and volatility <b>&sigma; = 25.0%</b>. The sample statistics return sample mean <i>M̄</i> = INR 1,148,500, "
            "sample standard deviation <i>s</i> = INR 292,000, and 5th percentile <i>P</i><sub>5</sub> = INR 724,100. "
            "Calculate the 95% Confidence Interval for the mean and the 1-year Value at Risk (VaR<sub>95%</sub>).",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Compute Central Limit Theorem Standard Error):</b><br/>"
            "&nbsp;&nbsp;&bull; Number of simulation paths: <i>M</i> = 10,000 &rArr; &radic;<i>M</i> = &radic;10,000 = 100.<br/>"
            "&nbsp;&nbsp;&bull; Standard Error: SE = <i>s</i> / &radic;<i>M</i> = 292,000 / 100 = <b>INR 2,920.00</b>.<br/><br/>"
            "<b>Step 2 (Construct 95% Confidence Interval for Expected Mean):</b><br/>"
            "&nbsp;&nbsp;&bull; Margin of error: 1.96 &times; SE = 1.96 &times; 2,920.00 = <b>INR 5,723.20</b>.<br/>"
            "&nbsp;&nbsp;&bull; 95% Confidence Interval: [ 1,148,500 &minus; 5,723.20, &nbsp; 1,148,500 + 5,723.20 ]<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;= <b>[ INR 1,142,776.80, &nbsp; INR 1,154,223.20 ]</b>.<br/>"
            "&nbsp;&nbsp;&bull; Theoretical analytical mean: 1,000,000 &times; <i>e</i><sup>0.14</sup> = <b>INR 1,150,273.80</b> (lies perfectly within CI!).<br/><br/>"
            "<b>Step 3 (Calculate Absolute Value at Risk — VaR<sub>95%</sub>):</b><br/>"
            "&nbsp;&nbsp;&bull; 5th percentile terminal value: <i>P</i><sub>5</sub> = INR 724,100.00.<br/>"
            "&nbsp;&nbsp;&bull; Absolute Dollar VaR: VaR<sub>95%</sub> = <i>S</i><sub>0</sub> &minus; <i>P</i><sub>5</sub> = 1,000,000 &minus; 724,100 = <b>INR 275,900.00</b>.<br/>"
            "&nbsp;&nbsp;&bull; Percentage VaR: 275,900 / 1,000,000 = <b>27.59% maximum expected drawdown</b>.<br/><br/>"
            "<b>Step 4 (Risk Interpretation for Decision Support):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>Takeaway:</i> In 95% of all market years, the investor's maximum capital loss will not exceed INR 275,900. "
            "However, in 5% of severe bear-market years, capital losses will be even more severe. "
            "This empowers the investor to align risk tolerance before purchasing the asset.",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 4: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("12.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the complete vectorized Monte Carlo simulation engine from <code>models/monte_carlo.py</code>, "
        "generating full path ensembles, empirical percentiles, and goal attainment probability estimators:",
        styles['Body']
    ))

    code_raw = (
        "import numpy as np\n"
        "from typing import Dict\n\n"
        "def simulate_monte_carlo_portfolio(\n"
        "    s0: float, mu: float, sigma: float, time_years: float,\n"
        "    n_simulations: int = 10000, target_goal: float = None, seed: int = None\n"
        ") -> Dict:\n"
        "    \"\"\"\n"
        "    Executes vectorized Monte Carlo simulation under Geometric Brownian Motion.\n"
        "    Returns mean, median, percentiles (5th, 95th), VaR_95, and target probability.\n"
        "    \"\"\"\n"
        "    if s0 <= 0.0 or sigma < 0.0 or time_years <= 0.0 or n_simulations <= 0:\n"
        "        raise ValueError(\"Simulation parameters must be strictly positive.\")\n"
        "    if seed is not None:\n"
        "        np.random.seed(seed)\n"
        "    drift = (mu - 0.5 * (sigma ** 2)) * time_years\n"
        "    diffusion = sigma * np.sqrt(time_years)\n"
        "    z = np.random.normal(0.0, 1.0, size=n_simulations)\n"
        "    terminal_values = s0 * np.exp(drift + diffusion * z)\n"
        "    p5, p50, p95 = np.percentile(terminal_values, [5.0, 50.0, 95.0])\n"
        "    target_prob = float(np.mean(terminal_values >= target_goal)) if target_goal else None\n"
        "    return {\n"
        "        'mean': float(np.mean(terminal_values)),\n"
        "        'median': float(p50),\n"
        "        'p5': float(p5),\n"
        "        'p95': float(p95),\n"
        "        'var_95_abs': float(max(0.0, s0 - p5)),\n"
        "        'target_probability': target_prob,\n"
        "        'standard_error': float(np.std(terminal_values) / np.sqrt(n_simulations))\n"
        "    }\n"
    )
    story.append(make_code_card(code_raw, title="models/monte_carlo.py — Vectorized Simulation & Risk Engine"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("12.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Formula</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>LLN Convergence</b>", styles['Body']), Paragraph("lim <i>M̄</i> = &#120124;[<i>S</i><sub><i>T</i></sub>]", styles['Body']), Paragraph("Almost sure convergence of sample ensemble to true expectation", styles['Body'])],
        [Paragraph("<b>CLT Error Rate</b>", styles['Body']), Paragraph("SE = &sigma; / &radic;<i>M</i> = <i>O</i>(<i>M</i><sup>&minus;1/2</sup>)", styles['Body']), Paragraph("Dimension-independent convergence rate for stochastic integrals", styles['Body'])],
        [Paragraph("<b>Goal Probability</b>", styles['Body']), Paragraph("<i>P̂</i>(&Gamma;) = (1/<i>M</i>)&sum;&#120793;<sub>{<i>S</i><sub><i>T</i></sub>&ge;&Gamma;}</sub>", styles['Body']), Paragraph("Unbiased empirical estimator of milestone achievement likelihood", styles['Body'])],
        [Paragraph("<b>Value at Risk</b>", styles['Body']), Paragraph("VaR<sub>95%</sub> = <i>S</i><sub>0</sub> &minus; <i>P</i><sub>5</sub>", styles['Body']), Paragraph("Quantifies maximum capital drawdown at 95% confidence", styles['Body'])],
        [Paragraph("<b>Vectorization Speed</b>", styles['Body']), Paragraph("NumPy array operations", styles['Body']), Paragraph("High-throughput SIMD parallelization over 10,000+ paths", styles['Body'])]
    ]
    t_prop = Table(prop_data, colWidths=[120, 164, 220])
    t_prop.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.7, pal['border']),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, pal['border']),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_prop)

    canvas_factory = lambda *args, **kwargs: TextbookCanvas(*args, **kwargs)
    doc.build(story, canvasmaker=canvas_factory)

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.dirname(__file__))
    out_file = os.path.join(out_dir, "12_Monte_Carlo_Simulation.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
