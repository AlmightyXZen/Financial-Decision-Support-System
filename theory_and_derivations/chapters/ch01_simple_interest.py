"""
Chapter 01: Simple Interest & Linear Accumulation.
Comprehensive textbook chapter with formal axioms, ODE comparisons,
Bernoulli convexity theorem, hand-solved examples, and Python implementation.
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

    # ==================== PAGE 1: THEORY & FORMAL DERIVATIONS ====================
    story.append(Paragraph("CHAPTER 1", styles['ChapterLabel']))
    story.append(Paragraph("Simple Interest & Linear Accumulation", styles['ChapterTitle']))
    story.append(Paragraph(
        "Axiomatic Foundations, Differential Formulations, and Step-by-Step Analytical Solutions",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=8))

    story.append(Paragraph("1.1 Definition & Mathematical Axioms", styles['H1']))
    story.append(Paragraph(
        "Simple Interest represents the foundational linear valuation model in financial mathematics. "
        "The core axiom defining this accumulation regime is that interest accrued over any sub-interval is "
        "<b>never capitalized</b> into the earning principal; that is, interest does not generate further interest.",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 1.1 (Simple Accumulation Function)</b>", styles['DefHeader']),
        Paragraph(
            "Let initial capital principal be <i>P</i> &gt; 0, nominal annual interest rate be <i>r</i> &ge; 0 "
            "(expressed as a decimal fraction: <i>r</i> = <i>R</i> / 100 for percentage rate <i>R</i>%), "
            "and time horizon be <i>t</i> &ge; 0 measured in years.<br/>"
            "The <b>total accrued interest</b> <i>I</i>(<i>t</i>) and <b>terminal accumulated value</b> <i>A</i>(<i>t</i>) are defined by:",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("<i>I</i>(<i>t</i>) = <i>P</i> &middot; <i>r</i> &middot; <i>t</i>", styles['Equation']),
        Spacer(1, 1),
        Paragraph("<i>A</i>(<i>t</i>) = <i>P</i> + <i>I</i>(<i>t</i>) = <i>P</i>(1 + <i>r</i> &middot; <i>t</i>)", styles['Equation']),
        Spacer(1, 2),
        Paragraph("The accumulation factor is denoted as <i>a</i>(<i>t</i>) = 1 + <i>r</i> &middot; <i>t</i>, which satisfies <i>a</i>(0) = 1.", styles['EquationSub'])
    ]
    story.append(make_card(def_content, pad_v=7, pad_h=12))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.2 First-Principles Derivation & Differential Viewpoint", styles['H1']))
    story.append(Paragraph(
        "<b>Axiomatic Derivation:</b> Under simple accumulation, interest <i>I</i> satisfies three simultaneous physical properties: "
        "(1) <i>I</i> &prop; <i>P</i> (principal scale invariance), (2) <i>I</i> &prop; <i>r</i> (yield homogeneity), and (3) <i>I</i> &prop; <i>t</i> (temporal linearity). "
        "Combining these yields <i>I</i> = <i>k</i> &middot; <i>P</i> &middot; <i>r</i> &middot; <i>t</i>, with proportionality constant <i>k</i> = 1 by convention.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>Ordinary Differential Equation (ODE) Perspective:</b><br/>"
        "Examining instantaneous wealth rate of change <i>dA</i>/<i>dt</i> contrasts simple and continuous regimes:",
        styles['Body']
    ))

    # ODE Comparison Table
    ode_table_data = [
        [
            Paragraph("<b>Valuation Regime</b>", styles['H2']),
            Paragraph("<b>Governing Differential Equation</b>", styles['H2']),
            Paragraph("<b>Closed-Form Solution <i>A</i>(<i>t</i>)</b>", styles['H2']),
            Paragraph("<b>Growth Dynamic</b>", styles['H2'])
        ],
        [
            Paragraph("<b>Simple Interest</b>", styles['Body']),
            Paragraph("<i>d</i><i>A</i>/<i>dt</i> = <i>P</i> &middot; <i>r</i>", styles['Body']),
            Paragraph("<i>A</i>(<i>t</i>) = <i>P</i>(1 + <i>rt</i>)", styles['Body']),
            Paragraph("Constant slope (Linear)", styles['Body'])
        ],
        [
            Paragraph("<b>Continuous Compounding</b>", styles['Body']),
            Paragraph("<i>d</i><i>A</i>/<i>dt</i> = <i>r</i> &middot; <i>A</i>(<i>t</i>)", styles['Body']),
            Paragraph("<i>A</i>(<i>t</i>) = <i>P</i> &middot; <i>e</i><sup><i>rt</i></sup>", styles['Body']),
            Paragraph("Wealth-proportional (Exponential)", styles['Body'])
        ]
    ]
    t_ode = Table(ode_table_data, colWidths=[114, 140, 140, 110])
    t_ode.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.7, pal['border']),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, pal['border']),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_ode)
    story.append(Spacer(1, 6))

    # Theorem Box
    th_content = [
        Paragraph("<b>Theorem 1.1 (Sub-Period Dominance via Bernoulli's Inequality)</b>", styles['DefHeader']),
        Paragraph(
            "For any strictly positive rate <i>r</i> &gt; 0 and fractional duration <i>t</i> &in; (0, 1), simple interest accumulation "
            "is <i>strictly greater</i> than annual compound interest accumulation:<br/>"
            "<font size=10><b>1 + <i>r</i> &middot; <i>t</i> &gt; (1 + <i>r</i>)<sup><i>t</i></sup> &nbsp;&nbsp;&forall; <i>t</i> &in; (0, 1)</b></font>",
            styles['Body']
        ),
        Paragraph(
            "<b>Proof:</b> Let <i>f</i>(<i>t</i>) = (1 + <i>r</i>)<sup><i>t</i></sup> for <i>t</i> &ge; 0. The second derivative is "
            "<i>f''</i>(<i>t</i>) = [ln(1 + <i>r</i>)]<sup>2</sup>(1 + <i>r</i>)<sup><i>t</i></sup>. Since [ln(1+<i>r</i>)]<sup>2</sup> &gt; 0 "
            "and (1+<i>r</i>)<sup><i>t</i></sup> &gt; 0 for all <i>r</i> &gt; 0, <i>f''</i>(<i>t</i>) &gt; 0 strictly, confirming <i>f</i> is strictly convex.<br/>"
            "The secant line connecting (0, 1) and (1, 1+<i>r</i>) is <i>g</i>(<i>t</i>) = 1 + <i>rt</i>. By strict convexity, the graph of <i>f</i> "
            "lies strictly below chord <i>g</i> on the open interval (0, 1). Thus, (1 + <i>r</i>)<sup><i>t</i></sup> &lt; 1 + <i>rt</i>. &#9632;",
            styles['Body']
        )
    ]
    story.append(make_card(th_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLES ====================
    story.append(Paragraph("1.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: a multi-year sovereign bond yield and a money-market bridge facility with exact day counts.",
        styles['Body']
    ))

    # Example 1.1 Card
    ex1_content = [
        Paragraph("<b>Example 1.1: Multi-Year Sovereign Treasury Bond</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem:</b> An investor commits principal capital of <b><i>P</i> = INR 100,000</b> into a fixed-income "
            "treasury bond offering a simple interest rate of <b><i>R</i> = 7.50% per annum</b>. The bond matures in "
            "<b><i>t</i> = 3 years</b>. Calculate total interest accrued and final maturity amount.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=4, spaceBefore=2),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/>"
            "&bull; <b>Step 1 (Parameter Normalization):</b> <i>P</i> = 100,000, &nbsp; <i>r</i> = 7.50 / 100 = 0.075, &nbsp; <i>t</i> = 3.0 years.<br/>"
            "&bull; <b>Step 2 (Interest Calculation):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>I</i> = <i>P</i> &middot; <i>r</i> &middot; <i>t</i> = 100,000 &times; 0.075 &times; 3 = 100,000 &times; 0.225 = <b>INR 22,500.00</b><br/>"
            "&bull; <b>Step 3 (Terminal Wealth Calculation):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>A</i> = <i>P</i> + <i>I</i> = 100,000 + 22,500 = <b>INR 122,500.00</b><br/>"
            "&bull; <b>Step 4 (Annual Verification):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Year 1: <i>I</i><sub>1</sub> = INR 7,500.00 &nbsp;|&nbsp; Year 2: <i>I</i><sub>2</sub> = INR 7,500.00 &nbsp;|&nbsp; Year 3: <i>I</i><sub>3</sub> = INR 7,500.00<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Total sum: 3 &times; 7,500 = INR 22,500.00 (verified exact linear accumulation).",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 6))

    # Example 1.2 Card
    ex2_content = [
        Paragraph("<b>Example 1.2: Fractional Tenors & Day-Count Mechanics (The Banker's Rule)</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem:</b> A short-term commercial credit facility of <b><i>P</i> = INR 250,000</b> is issued on "
            "<b>March 15</b> at an annual simple rate of <b><i>R</i> = 9.20%</b>, and repaid on <b>October 28</b> of "
            "the same non-leap year. Compare interest accrued under:<br/>"
            "&nbsp;&nbsp;&bull; <b>Method A:</b> Exact / Actual/365 Convention (Common in sovereign bond markets)<br/>"
            "&nbsp;&nbsp;&bull; <b>Method B:</b> Banker's Rule / Actual/360 Convention (Standard in US money markets and commercial paper)",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=4, spaceBefore=2),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/>"
            "&bull; <b>Step 1 (Exact Elapsed Days):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;March (31 &minus; 15) = 16 | Apr = 30 | May = 31 | Jun = 30 | Jul = 31 | Aug = 31 | Sep = 30 | Oct = 28<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<b>Total days elapsed:</b> <i>d</i> = 16 + 30 + 31 + 30 + 31 + 31 + 30 + 28 = <b>227 days</b>.<br/>"
            "&bull; <b>Step 2 (Method A: Actual/365 Convention):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Annualized duration fraction: <i>t</i><sub>365</sub> = 227 / 365 &approx; 0.6219178 years<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>I</i><sub>365</sub> = 250,000 &times; 0.092 &times; (227 / 365) = 23,000 &times; 0.6219178 = <b>INR 14,304.11</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Terminal repayment: <i>A</i><sub>365</sub> = 250,000 + 14,304.11 = <b>INR 264,304.11</b>.<br/>"
            "&bull; <b>Step 3 (Method B: Actual/360 Convention — The Banker's Rule):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Annualized duration fraction: <i>t</i><sub>360</sub> = 227 / 360 &approx; 0.6305556 years<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>I</i><sub>360</sub> = 250,000 &times; 0.092 &times; (227 / 360) = 23,000 &times; 0.6305556 = <b>INR 14,502.78</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Terminal repayment: <i>A</i><sub>360</sub> = 250,000 + 14,502.78 = <b>INR 264,502.78</b>.<br/>"
            "&bull; <b>Step 4 (Yield Discrepancy & Economic Analysis):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Absolute difference: &Delta;<i>I</i> = <i>I</i><sub>360</sub> &minus; <i>I</i><sub>365</sub> = 14,502.78 &minus; 14,304.11 = <b>INR 198.67</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Ratio: <i>I</i><sub>360</sub> / <i>I</i><sub>365</sub> = 365 / 360 &approx; 1.013889 (+1.39%).<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>Takeaway:</i> The Actual/360 convention artificially magnifies the lender's effective annual yield "
            "by exactly 1.39%, demonstrating why institutional term sheets explicitly define day-count conventions.",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 3: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("1.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the complete implementation from <code>models/time_value.py</code>. "
        "It provides domain validation, typing, and clear docstrings for modular inclusion in the decision-support system:",
        styles['Body']
    ))

    code_raw = (
        "def simple_interest(principal: float, annual_rate: float, time_years: float) -> float:\n"
        "    \"\"\"\n"
        "    Computes accrued simple interest: I = P * r * t.\n"
        "    Parameters:\n"
        "        principal (float): Initial capital (P >= 0).\n"
        "        annual_rate (float): Nominal annual rate as decimal (r >= 0).\n"
        "        time_years (float): Duration in years (t >= 0).\n"
        "    \"\"\"\n"
        "    if principal < 0.0 or annual_rate < 0.0 or time_years < 0.0:\n"
        "        raise ValueError(\"Financial parameters must be non-negative.\")\n"
        "    return float(principal * annual_rate * time_years)\n\n\n"
        "def simple_interest_amount(principal: float, annual_rate: float, time_years: float) -> float:\n"
        "    \"\"\"Computes terminal accumulated wealth: A = P * (1 + r * t).\"\"\"\n"
        "    return float(principal + simple_interest(principal, annual_rate, time_years))\n"
    )
    story.append(make_code_card(code_raw, title="models/time_value.py — Simple Interest Engine"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Value</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>Domain & Constraints</b>", styles['Body']), Paragraph("<i>P</i> &gt; 0, <i>r</i> &ge; 0, <i>t</i> &ge; 0", styles['Body']), Paragraph("Strict non-negativity across economic state variables", styles['Body'])],
        [Paragraph("<b>Accumulation Function</b>", styles['Body']), Paragraph("<i>a</i>(<i>t</i>) = 1 + <i>rt</i>", styles['Body']), Paragraph("Affine linear operator with slope equal to nominal rate <i>r</i>", styles['Body'])],
        [Paragraph("<b>Marginal Accrual Rate</b>", styles['Body']), Paragraph("<i>da</i>/<i>dt</i> = <i>r</i>", styles['Body']), Paragraph("Invariant to elapsed time <i>t</i> and current accumulated wealth", styles['Body'])],
        [Paragraph("<b>Convexity / Curvature</b>", styles['Body']), Paragraph("<i>d</i><sup>2</sup><i>a</i>/<i>dt</i><sup>2</sup> = 0", styles['Body']), Paragraph("Zero second derivative; absence of compounding curvature", styles['Body'])]
    ]
    t_prop = Table(prop_data, colWidths=[130, 154, 220])
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
    out_file = os.path.join(out_dir, "01_Simple_Interest.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
