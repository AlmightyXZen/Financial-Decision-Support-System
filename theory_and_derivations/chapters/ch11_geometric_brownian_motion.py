"""
Chapter 11: Geometric Brownian Motion (GBM) & Price Dynamics.
Textbook chapter on stochastic calculus, Itô's Lemma proof, volatility drag derivation,
lognormal distributions, 10-year mean vs median paths, manual 3-step simulation, and Python code.
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

    # ==================== PAGE 1: THEORY & ITÔ'S LEMMA DERIVATION ====================
    story.append(Paragraph("CHAPTER 11", styles['ChapterLabel']))
    story.append(Paragraph("Geometric Brownian Motion & Asset Dynamics", styles['ChapterTitle']))
    story.append(Paragraph(
        "Continuous Stochastic Calculus, It&ocirc;'s Lemma Proof, Lognormal Distributions, and The Volatility Drag Phenomenon",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=7))

    story.append(Paragraph("11.1 From Random Walks to Continuous Price Dynamics", styles['H1']))
    story.append(Paragraph(
        "In empirical financial markets, asset prices do not follow deterministic lines; they fluctuate randomly "
        "in response to continuous information arrivals. **Geometric Brownian Motion (GBM)** is the foundational "
        "continuous-time stochastic process governing modern quantitative finance (including the Black-Scholes-Merton model).",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 11.1 (The Stochastic Differential Equation of GBM)</b>", styles['DefHeader']),
        Paragraph(
            "Let asset price at time <i>t</i> be <i>S</i><sub><i>t</i></sub> &gt; 0, expected annual drift be &mu; &in; &#8477;, "
            "annualized volatility be &sigma; &gt; 0, and <i>W</i><sub><i>t</i></sub> be a standard Wiener process (Brownian Motion) "
            "with independent increments <i>dW</i><sub><i>t</i></sub> &sim; &#119977;(0, <i>dt</i>).<br/>"
            "The relative price return is governed by the Stochastic Differential Equation (SDE):",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("<i>dS</i><sub><i>t</i></sub> / <i>S</i><sub><i>t</i></sub> = &mu; <i>dt</i> + &sigma; <i>dW</i><sub><i>t</i></sub> &nbsp;&nbsp;&rArr;&nbsp;&nbsp; <i>dS</i><sub><i>t</i></sub> = &mu; <i>S</i><sub><i>t</i></sub> <i>dt</i> + &sigma; <i>S</i><sub><i>t</i></sub> <i>dW</i><sub><i>t</i></sub>", styles['Equation']),
        Spacer(1, 2),
        Paragraph("where &mu;<i>S</i><sub><i>t</i></sub><i>dt</i> is the deterministic drift term and &sigma;<i>S</i><sub><i>t</i></sub><i>dW</i><sub><i>t</i></sub> is the stochastic diffusion shock.", styles['EquationSub'])
    ]
    story.append(make_card(def_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 5))

    story.append(Paragraph("11.2 Analytical Solution via It&ocirc;'s Lemma", styles['H1']))
    story.append(Paragraph(
        "<b>Rigorous Stochastic Calculus Derivation:</b><br/>"
        "In standard calculus, <i>d</i>(ln <i>S</i>) = <i>dS</i> / <i>S</i>. However, in stochastic calculus, Brownian paths have infinite "
        "variation, so second-order terms (<i>dW</i><sub><i>t</i></sub>)<sup>2</sup> = <i>dt</i> contribute directly to the drift.<br/>"
        "Let <i>f</i>(<i>S</i>) = ln(<i>S</i>). Applying **It&ocirc;'s Lemma** in one dimension:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <i>df</i> = <i>f'</i>(<i>S</i>) <i>dS</i> + (1/2) <i>f''</i>(<i>S</i>) (<i>dS</i>)<sup>2</sup>.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Derivatives: <i>f'</i>(<i>S</i>) = 1 / <i>S</i>, &nbsp; <i>f''</i>(<i>S</i>) = &minus;1 / <i>S</i><sup>2</sup>.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Second-order term: (<i>dS</i>)<sup>2</sup> = (&mu;<i>S dt</i> + &sigma;<i>S dW</i>)<sup>2</sup> = &sigma;<sup>2</sup> <i>S</i><sup>2</sup> <i>dt</i>.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Substituting into It&ocirc;'s expansion:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>d</i>(ln <i>S</i>) = (1/<i>S</i>)(&mu;<i>S dt</i> + &sigma;<i>S dW</i>) &minus; (1/2)(1/<i>S</i><sup>2</sup>)(&sigma;<sup>2</sup> <i>S</i><sup>2</sup> <i>dt</i>) "
        "= <b>(&mu; &minus; &sigma;<sup>2</sup>/2) <i>dt</i> + &sigma; <i>dW</i><sub><i>t</i></sub></b>.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Integrating from 0 to <i>t</i> yields the exact analytical trajectory equation:",
        styles['Body']
    ))

    # Analytical Solution Box
    th_content = [
        Paragraph("<b>Theorem 11.1 (Exact Discrete Solution & Volatility Drag)</b>", styles['DefHeader']),
        Paragraph(
            "<font size=10.5><b><i>S</i><sub><i>t</i></sub> = <i>S</i><sub>0</sub> &middot; exp[ (&mu; &minus; &sigma;<sup>2</sup> / 2) &middot; <i>t</i> + &sigma; &middot; <i>W</i><sub><i>t</i></sub> ] "
            "= <i>S</i><sub>0</sub> &middot; exp[ (&mu; &minus; &sigma;<sup>2</sup> / 2) &middot; <i>t</i> + &sigma; &radic;<i>t</i> &middot; <i>Z</i> ]</b></font>",
            styles['Equation']
        ),
        Paragraph(
            "where <i>Z</i> &sim; &#119977;(0, 1) is a standard normal random variable.<br/>"
            "<b>The Volatility Drag Principle:</b> Because of Jensen's inequality and the negative term &minus;&sigma;<sup>2</sup>/2, "
            "the <b>median growth rate</b> is &mu; &minus; &sigma;<sup>2</sup>/2, whereas the arithmetic expected value is &#120124;[<i>S</i><sub><i>t</i></sub>] = <i>S</i><sub>0</sub> <i>e</i><sup>&mu;<i>t</i></sup>. "
            "More than 50% of simulated market outcomes strictly underperform the advertised arithmetic mean &mu;!",
            styles['Body']
        )
    ]
    story.append(make_card(th_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLE 11.1 ====================
    story.append(Paragraph("11.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: quantifying the volatility drag spread between mean and median, "
        "and manually executing a 3-step discretized stochastic trajectory.",
        styles['Body']
    ))

    # Example 11.1 Card
    ex1_content = [
        Paragraph("<b>Example 11.1: Volatility Drag Quantification over a 10-Year Horizon</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> An investor commits capital <b><i>S</i><sub>0</sub> = INR 1,000,000</b> into a diversified equity fund "
            "exhibiting an arithmetic expected return of <b>&mu; = 12.00% per annum</b> and annual volatility of <b>&sigma; = 20.00%</b> "
            "over a horizon of <b><i>t</i> = 10 years</b>. Calculate the theoretical arithmetic mean, the actual median trajectory, "
            "and the exact monetary volatility drag gap.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Compute Expected Arithmetic Mean Value):</b><br/>"
            "&nbsp;&nbsp;&bull; Formula: &#120124;[<i>S</i><sub>10</sub>] = <i>S</i><sub>0</sub> &middot; <i>e</i><sup>&mu;&middot;<i>t</i></sup> = 1,000,000 &times; <i>e</i><sup>0.12 &times; 10</sup> = 1,000,000 &times; <i>e</i><sup>1.20</sup>.<br/>"
            "&nbsp;&nbsp;&bull; Since <i>e</i><sup>1.20</sup> &approx; 3.3201169:<br/>"
            "&nbsp;&nbsp;&bull; <b>Theoretical Mean:</b> &#120124;[<i>S</i><sub>10</sub>] = <b>INR 3,320,116.92</b>.<br/><br/>"
            "<b>Step 2 (Compute Volatility Drag & Geometric Drift Rate):</b><br/>"
            "&nbsp;&nbsp;&bull; Volatility drag deduction: &sigma;<sup>2</sup> / 2 = (0.20)<sup>2</sup> / 2 = 0.0400 / 2 = <b>0.0200 (2.00% per annum drag!)</b>.<br/>"
            "&nbsp;&nbsp;&bull; Effective geometric median drift: &mu;* = &mu; &minus; &sigma;<sup>2</sup>/2 = 0.1200 &minus; 0.0200 = <b>0.1000 (10.00% per annum)</b>.<br/><br/>"
            "<b>Step 3 (Compute True Median Wealth Horizon):</b><br/>"
            "&nbsp;&nbsp;&bull; Formula: Median(<i>S</i><sub>10</sub>) = <i>S</i><sub>0</sub> &middot; <i>e</i><sup>&mu;* &middot; <i>t</i></sup> = 1,000,000 &times; <i>e</i><sup>0.10 &times; 10</sup> = 1,000,000 &times; <i>e</i><sup>1.00</sup>.<br/>"
            "&nbsp;&nbsp;&bull; Since <i>e</i><sup>1.00</sup> &approx; 2.7182818:<br/>"
            "&nbsp;&nbsp;&bull; <b>Typical Median Outcome:</b> Median(<i>S</i><sub>10</sub>) = <b>INR 2,718,281.83</b>.<br/><br/>"
            "<b>Step 4 (Volatility Drag Wealth Penalty Analysis):</b><br/>"
            "&nbsp;&nbsp;&bull; Monetary Disparity: 3,320,116.92 &minus; 2,718,281.83 = <b>INR 601,835.09 gap!</b><br/>"
            "&nbsp;&nbsp;&bull; <i>Crucial Insight:</i> Standard deterministic calculators advertise INR 3.32 Million, but because markets "
            "are stochastic, a typical investor will experience only INR 2.72 Million. The probability of falling below the arithmetic "
            "mean is <i>P</i>(<i>Z</i> &lt; &sigma;&radic;<i>t</i> / 2) = <i>P</i>(<i>Z</i> &lt; 0.316) &approx; <b>62.4% of all investors underperform the average!</b>",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 3: WORKED EXAMPLE 11.2 ====================
    # Example 11.2 Card
    ex2_content = [
        Paragraph("<b>Example 11.2: Discretized 3-Step Stochastic Trajectory by Hand</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> Starting from <b><i>S</i><sub>0</sub> = INR 100,000</b> with drift <b>&mu; = 10.0%</b> "
            "and volatility <b>&sigma; = 15.0%</b> (&Delta;<i>t</i> = 1 year), simulate a 3-year asset price path by hand "
            "using standard normal draws: <b><i>Z</i><sub>1</sub> = +0.65</b> (bull shock), <b><i>Z</i><sub>2</sub> = &minus;1.10</b> (bear crash), "
            "and <b><i>Z</i><sub>3</sub> = +0.40</b> (recovery shock).",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Parameters:</b> &mu; = 0.10, &sigma; = 0.15, &Delta;<i>t</i> = 1.0. Volatility drag: &mu; &minus; &sigma;<sup>2</sup>/2 = 0.10 &minus; (0.0225/2) = <b>0.08875</b>.<br/>"
            "Step equation: <i>S</i><sub><i>k</i></sub> = <i>S</i><sub><i>k</i>&minus;1</sub> &middot; exp[ 0.08875 + 0.15 &middot; <i>Z</i><sub><i>k</i></sub> ].<br/><br/>"
            "<b>Year 1 (Bull Shock, <i>Z</i><sub>1</sub> = +0.65):</b><br/>"
            "&nbsp;&nbsp;&bull; Exponent: 0.08875 + (0.15 &times; 0.65) = 0.08875 + 0.0975 = 0.18625.<br/>"
            "&nbsp;&nbsp;&bull; Factor: exp(0.18625) &approx; 1.204724.<br/>"
            "&nbsp;&nbsp;&bull; <b>Price Year 1:</b> <i>S</i><sub>1</sub> = 100,000 &times; 1.204724 = <b>INR 120,472.40</b> (+20.47%).<br/><br/>"
            "<b>Year 2 (Bear Crash, <i>Z</i><sub>2</sub> = &minus;1.10):</b><br/>"
            "&nbsp;&nbsp;&bull; Exponent: 0.08875 + (0.15 &times; (&minus;1.10)) = 0.08875 &minus; 0.1650 = &minus;0.07625.<br/>"
            "&nbsp;&nbsp;&bull; Factor: exp(&minus;0.07625) &approx; 0.926585.<br/>"
            "&nbsp;&nbsp;&bull; <b>Price Year 2:</b> <i>S</i><sub>2</sub> = 120,472.40 &times; 0.926585 = <b>INR 111,627.87</b> (&minus;7.34%).<br/><br/>"
            "<b>Year 3 (Recovery Shock, <i>Z</i><sub>3</sub> = +0.40):</b><br/>"
            "&nbsp;&nbsp;&bull; Exponent: 0.08875 + (0.15 &times; 0.40) = 0.08875 + 0.0600 = 0.14875.<br/>"
            "&nbsp;&nbsp;&bull; Factor: exp(0.14875) &approx; 1.160383.<br/>"
            "&nbsp;&nbsp;&bull; <b>Price Year 3:</b> <i>S</i><sub>3</sub> = 111,627.87 &times; 1.160383 = <b>INR 129,531.06</b> (+16.04%).<br/><br/>"
            "<b>3-Year Path Summary:</b> INR 100,000 &rarr; INR 120,472.40 &rarr; INR 111,627.87 &rarr; <b>INR 129,531.06</b>.<br/>"
            "<i>Takeaway:</i> This manual calculation is the exact arithmetic unit executed billions of times across "
            "Monte Carlo simulation clusters in quantitative risk management.",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 4: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("11.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the complete implementation from <code>models/monte_carlo.py</code>, "
        "providing vectorized Geometric Brownian Motion path generation using NumPy:",
        styles['Body']
    ))

    code_raw = (
        "import numpy as np\n"
        "from typing import Tuple\n\n"
        "def simulate_gbm_single_path(\n"
        "    s0: float, mu: float, sigma: float, time_years: float, steps: int, seed: int = None\n"
        ") -> Tuple[np.ndarray, np.ndarray]:\n"
        "    \"\"\"\n"
        "    Simulates exact GBM path: S_t = S_0 * exp((mu - 0.5 * sigma^2)*t + sigma * W_t).\n"
        "    \"\"\"\n"
        "    if s0 <= 0.0 or sigma < 0.0 or time_years <= 0.0 or steps <= 0:\n"
        "        raise ValueError(\"Invalid parameters for Geometric Brownian Motion.\")\n"
        "    if seed is not None:\n"
        "        np.random.seed(seed)\n"
        "    dt = time_years / float(steps)\n"
        "    time_grid = np.linspace(0.0, time_years, steps + 1)\n"
        "    drift_step = (mu - 0.5 * (sigma ** 2)) * dt\n"
        "    diffusion_step = sigma * np.sqrt(dt)\n"
        "    z = np.random.normal(0.0, 1.0, size=steps)\n"
        "    log_returns = np.concatenate([[0.0], drift_step + diffusion_step * z])\n"
        "    price_path = s0 * np.exp(np.cumsum(log_returns))\n"
        "    return time_grid, price_path\n"
    )
    story.append(make_code_card(code_raw, title="models/monte_carlo.py — Geometric Brownian Motion Path Generator"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("11.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Formula</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>Governing SDE</b>", styles['Body']), Paragraph("<i>dS</i> = &mu;<i>S dt</i> + &sigma;<i>S dW</i>", styles['Body']), Paragraph("Continuous-time stochastic dynamics of frictionless asset returns", styles['Body'])],
        [Paragraph("<b>It&ocirc; Solution</b>", styles['Body']), Paragraph("<i>S</i><sub><i>t</i></sub> = <i>S</i><sub>0</sub> <i>e</i><sup>(&mu;&minus;&sigma;<sup>2</sup>/2)<i>t</i> + &sigma;<i>W</i><sub><i>t</i></sub></sup>", styles['Body']), Paragraph("Closed-form path trajectory driven by Wiener process", styles['Body'])],
        [Paragraph("<b>Expected Mean</b>", styles['Body']), Paragraph("&#120124;[<i>S</i><sub><i>t</i></sub>] = <i>S</i><sub>0</sub> <i>e</i><sup>&mu;<i>t</i></sup>", styles['Body']), Paragraph("Arithmetic mean pulled upward by positive lognormal skewness", styles['Body'])],
        [Paragraph("<b>Typical Median</b>", styles['Body']), Paragraph("Median = <i>S</i><sub>0</sub> <i>e</i><sup>(&mu;&minus;&sigma;<sup>2</sup>/2)<i>t</i></sup>", styles['Body']), Paragraph("True geometric median path realized by typical investors", styles['Body'])],
        [Paragraph("<b>Volatility Drag</b>", styles['Body']), Paragraph("&Delta;&mu; = &minus;&sigma;<sup>2</sup> / 2", styles['Body']), Paragraph("Structural return penalty imposed by variance in continuous time", styles['Body'])]
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
    out_file = os.path.join(out_dir, "11_Geometric_Brownian_Motion.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
