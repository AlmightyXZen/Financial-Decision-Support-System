"""
Chapter 05: Effective Annual Rate (EAR) & Yield Equivalence.
Textbook chapter on nominal vs effective yields, consumer APR distortion,
inversion formulas, yield equivalence across frequencies, and Python code.
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
    story.append(Paragraph("CHAPTER 5", styles['ChapterLabel']))
    story.append(Paragraph("Effective Annual Rate (EAR) & Yield Equivalence", styles['ChapterTitle']))
    story.append(Paragraph(
        "Standardizing Compounding Frequencies, Nominal vs Effective Spreads, and Analytical Rate Inversion",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=7))

    story.append(Paragraph("5.1 Definition & The Need for Standardized Yields", styles['H1']))
    story.append(Paragraph(
        "In global financial markets, interest rates are routinely quoted as an **Annual Percentage Rate (APR)** "
        "or nominal rate, but paired with disparate compounding frequencies (e.g., credit cards compounded monthly, "
        "corporate bonds semi-annually, money markets daily). Comparing nominal rates directly leads to severe financial mispricing. "
        "The **Effective Annual Rate (EAR)** standardizes all borrowing and investing yields to an annualized equivalent basis.",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 5.1 (Effective Annual Rate Formulation)</b>", styles['DefHeader']),
        Paragraph(
            "Let nominal annual interest rate be <i>r</i><sub>nom</sub> &ge; 0 compounded <i>n</i> times per year.<br/>"
            "The <b>Effective Annual Rate (EAR)</b> is the true annual yield satisfying (1 + EAR) = (1 + <i>r</i><sub>nom</sub>/<i>n</i>)<sup><i>n</i></sup>:",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("EAR = (1 + <i>r</i><sub>nom</sub> / <i>n</i>)<sup><i>n</i></sup> &minus; 1", styles['Equation']),
        Spacer(1, 1),
        Paragraph("EAR<sub>cont</sub> = lim<sub><i>n</i>&rarr;&infin;</sub> (1 + <i>r</i><sub>nom</sub> / <i>n</i>)<sup><i>n</i></sup> &minus; 1 = <i>e</i><sup><i>r</i><sub>nom</sub></sup> &minus; 1", styles['Equation']),
        Spacer(1, 2),
        Paragraph("where EAR &ge; <i>r</i><sub>nom</sub> for all <i>n</i> &ge; 1, with equality holding if and only if <i>n</i> = 1 or <i>r</i><sub>nom</sub> = 0.", styles['EquationSub'])
    ]
    story.append(make_card(def_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 5))

    story.append(Paragraph("5.2 Rate Inversion & Yield Equivalence Across Frequencies", styles['H1']))
    story.append(Paragraph(
        "<b>Analytical Rate Inversion:</b> Given a desired effective annual yield EAR, what nominal rate "
        "<i>r</i><sub>nom</sub> must a financial product quote under compounding frequency <i>n</i>?<br/>"
        "Inverting Definition 5.1 algebraically:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; (1 + <i>r</i><sub>nom</sub> / <i>n</i>)<sup><i>n</i></sup> = 1 + EAR &nbsp;&rArr;&nbsp; "
        "1 + <i>r</i><sub>nom</sub> / <i>n</i> = (1 + EAR)<sup>1/<i>n</i></sup><br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <b>Discrete Inversion:</b> <i>r</i><sub>nom</sub>(<i>n</i>) = <i>n</i> [(1 + EAR)<sup>1/<i>n</i></sup> &minus; 1]<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <b>Continuous Inversion:</b> <i>e</i><sup><i>r</i><sub>cont</sub></sup> = 1 + EAR &nbsp;&rArr;&nbsp; "
        "<i>r</i><sub>cont</sub> = ln(1 + EAR).",
        styles['Body']
    ))

    # Spread Theorem Box
    th_content = [
        Paragraph("<b>Theorem 5.1 (Binomial Expansion of the Compounding Spread)</b>", styles['DefHeader']),
        Paragraph(
            "The spread between the Effective Annual Rate and the nominal rate &Delta;(<i>n</i>) = EAR &minus; <i>r</i><sub>nom</sub> "
            "expands as compounding frequency increases, governed by the binomial second-order term:<br/>"
            "<font size=9.5><b>&Delta;(<i>n</i>) &approx; [(<i>n</i> &minus; 1) / (2<i>n</i>)] &middot; <i>r</i><sub>nom</sub><sup>2</sup></b></font>",
            styles['Body']
        ),
        Paragraph(
            "<b>Proof:</b> Expanding (1 + <i>r</i>/<i>n</i>)<sup><i>n</i></sup> via the Binomial Theorem: "
            "1 + <i>n</i>(<i>r</i>/<i>n</i>) + [<i>n</i>(<i>n</i>&minus;1)/2](<i>r</i>/<i>n</i>)<sup>2</sup> + ... "
            "= 1 + <i>r</i> + [(<i>n</i>&minus;1)/(2<i>n</i>)]<i>r</i><sup>2</sup> + <i>O</i>(<i>r</i><sup>3</sup>). "
            "Subtracting 1 and <i>r</i> yields the result. As <i>n</i> &rarr; &infin;, the maximum continuous spread converges to (1/2)<i>r</i><sup>2</sup>. &#9632;",
            styles['Body']
        )
    ]
    story.append(make_card(th_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLE 5.1 ====================
    story.append(Paragraph("5.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: evaluating predatory consumer credit APR distortion, "
        "and constructing equivalent nominal yields across diverse compounding frequencies.",
        styles['Body']
    ))

    # Example 5.1 Card
    ex1_content = [
        Paragraph("<b>Example 5.1: Consumer Credit Card APR vs. NBFC Personal Loan</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> A borrower compares two competing credit facilities:<br/>"
            "&nbsp;&nbsp;&bull; <b>Facility A (Credit Card):</b> Advertised nominal rate <b><i>R</i> = 36.00% APR</b> compounded monthly (<i>n</i> = 12)<br/>"
            "&nbsp;&nbsp;&bull; <b>Facility B (NBFC Loan):</b> Advertised nominal rate <b><i>R</i> = 39.50% APR</b> compounded annually (<i>n</i> = 1)<br/>"
            "Which borrowing facility imposes the higher true economic borrowing cost?",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Facility A (Credit Card):</b><br/>"
            "&nbsp;&nbsp;&bull; Nominal rate decimal: <i>r</i><sub>nom</sub> = 0.36, &nbsp; frequency <i>n</i> = 12.<br/>"
            "&nbsp;&nbsp;&bull; Periodic monthly rate: <i>i</i> = 0.36 / 12 = 0.0300 (3.00% per month).<br/>"
            "&nbsp;&nbsp;&bull; Applying the EAR formula:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;EAR<sub><i>A</i></sub> = (1 + 0.03)<sup>12</sup> &minus; 1 = (1.03)<sup>12</sup> &minus; 1<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Since (1.03)<sup>12</sup> &approx; 1.42576089:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;EAR<sub><i>A</i></sub> = 1.42576089 &minus; 1 = 0.42576089 &implies; <b>42.58% Effective Annual Rate</b>.<br/><br/>"
            "<b>Facility B (NBFC Loan):</b><br/>"
            "&nbsp;&nbsp;&bull; Since <i>n</i> = 1: EAR<sub><i>B</i></sub> = (1 + 0.395)<sup>1</sup> &minus; 1 = <b>39.50% Effective Annual Rate</b>.<br/><br/>"
            "<b>Economic Analysis & Decision:</b><br/>"
            "&nbsp;&nbsp;&bull; Cost discrepancy: EAR<sub><i>A</i></sub> &minus; EAR<sub><i>B</i></sub> = 42.58% &minus; 39.50% = <b>+3.08% excess cost</b>.<br/>"
            "&nbsp;&nbsp;&bull; <i>Takeaway:</i> Despite Facility A marketing an APR that appears 3.50% lower than Facility B (36% vs 39.5%), "
            "its true annualized cost is over 3.0% higher due to monthly compounding velocity. "
            "This highlights why financial regulations require disclosure of Effective Annual Rates.",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 3: WORKED EXAMPLE 5.2 ====================
    # Example 5.2 Card
    ex2_content = [
        Paragraph("<b>Example 5.2: Yield Equivalence Calibration Across Frequencies</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> An institutional wealth fund sets an absolute performance hurdle of "
            "<b>EAR = 10.00%</b> effective annual yield. Determine the equivalent nominal rates <i>r</i><sub>nom</sub> "
            "that must be contracted under:<br/>"
            "&nbsp;&nbsp;&bull; <b>Case A:</b> Semi-annual compounding (<i>n</i> = 2)<br/>"
            "&nbsp;&nbsp;&bull; <b>Case B:</b> Monthly compounding (<i>n</i> = 12)<br/>"
            "&nbsp;&nbsp;&bull; <b>Case C:</b> Continuous compounding (<i>n</i> &rarr; &infin;)",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Case A (Semi-Annual Compounding, <i>n</i> = 2):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>r</i><sub>nom</sub>(2) = 2 &times; [(1 + 0.10)<sup>1/2</sup> &minus; 1]<br/>"
            "&nbsp;&nbsp;&bull; (1.10)<sup>0.5</sup> &approx; 1.04880885<br/>"
            "&nbsp;&nbsp;&bull; <i>r</i><sub>nom</sub>(2) = 2 &times; (0.04880885) = 0.0976177 &implies; <b>9.7618% per annum</b>.<br/><br/>"
            "<b>Case B (Monthly Compounding, <i>n</i> = 12):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>r</i><sub>nom</sub>(12) = 12 &times; [(1 + 0.10)<sup>1/12</sup> &minus; 1]<br/>"
            "&nbsp;&nbsp;&bull; (1.10)<sup>1/12</sup> &approx; 1.00797414<br/>"
            "&nbsp;&nbsp;&bull; <i>r</i><sub>nom</sub>(12) = 12 &times; (0.00797414) = 0.0956897 &implies; <b>9.5690% per annum</b>.<br/><br/>"
            "<b>Case C (Continuous Compounding, <i>n</i> &rarr; &infin;):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>r</i><sub>cont</sub> = ln(1 + EAR) = ln(1.10)<br/>"
            "&nbsp;&nbsp;&bull; <i>r</i><sub>cont</sub> = 0.09531018 &implies; <b>9.5310% per annum</b>.<br/><br/>"
            "<b>Summary of Equivalence:</b><br/>"
            "&nbsp;&nbsp;&bull; 10.00% annual &equiv; 9.7618% semi-annual &equiv; 9.5690% monthly &equiv; 9.5310% continuous.<br/>"
            "&nbsp;&nbsp;&bull; <i>Analytical Insight:</i> As compounding frequency increases, a lower nominal quoted rate "
            "suffices to achieve the exact same terminal dollar wealth.",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 4: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("5.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the complete implementation from <code>models/time_value.py</code>, "
        "providing bidirectional conversion between nominal rates and effective yields:",
        styles['Body']
    ))

    code_raw = (
        "import math\n\n"
        "def effective_annual_rate(nominal_rate: float, compounding_frequency: int) -> float:\n"
        "    \"\"\"\n"
        "    Computes discrete EAR: EAR = (1 + r / n) ** n - 1.\n"
        "    \"\"\"\n"
        "    if nominal_rate < 0.0 or compounding_frequency <= 0:\n"
        "        raise ValueError(\"Nominal rate must be non-negative and frequency n >= 1.\")\n"
        "    periodic_rate = nominal_rate / compounding_frequency\n"
        "    return float(((1.0 + periodic_rate) ** compounding_frequency) - 1.0)\n\n\n"
        "def continuous_effective_annual_rate(nominal_rate: float) -> float:\n"
        "    \"\"\"Computes continuous EAR: EAR_cont = exp(r) - 1.\"\"\"\n"
        "    if nominal_rate < 0.0:\n"
        "        raise ValueError(\"Nominal rate must be non-negative.\")\n"
        "    return float(math.exp(nominal_rate) - 1.0)\n\n\n"
        "def nominal_rate_from_ear(ear: float, compounding_frequency: int) -> float:\n"
        "    \"\"\"Inverts EAR to nominal rate: r = n * [(1 + EAR) ** (1/n) - 1].\"\"\"\n"
        "    if ear < 0.0 or compounding_frequency <= 0:\n"
        "        raise ValueError(\"EAR must be non-negative and n >= 1.\")\n"
        "    return float(compounding_frequency * (((1.0 + ear) ** (1.0 / compounding_frequency)) - 1.0))\n"
    )
    story.append(make_code_card(code_raw, title="models/time_value.py — Yield Equivalence Engine"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("5.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Formula</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>Discrete Formula</b>", styles['Body']), Paragraph("EAR = (1 + <i>r</i>/<i>n</i>)<sup><i>n</i></sup> &minus; 1", styles['Body']), Paragraph("Standardizes periodic yields to annual equivalent", styles['Body'])],
        [Paragraph("<b>Continuous Bound</b>", styles['Body']), Paragraph("lim<sub><i>n</i>&rarr;&infin;</sub> EAR = <i>e</i><sup><i>r</i></sup> &minus; 1", styles['Body']), Paragraph("Asymptotic maximum effective return for given nominal rate", styles['Body'])],
        [Paragraph("<b>Monotonicity in <i>n</i></b>", styles['Body']), Paragraph("&part;(EAR)/&part;<i>n</i> &gt; 0 &nbsp;&forall; <i>r</i> &gt; 0", styles['Body']), Paragraph("Higher compounding frequency strictly expands yield spread", styles['Body'])],
        [Paragraph("<b>Inversion Operator</b>", styles['Body']), Paragraph("<i>r</i><sub>nom</sub> = <i>n</i>[(1+EAR)<sup>1/<i>n</i></sup> &minus; 1]", styles['Body']), Paragraph("Calibrates contract rates to target hurdle returns", styles['Body'])],
        [Paragraph("<b>Continuous Inversion</b>", styles['Body']), Paragraph("<i>r</i><sub>cont</sub> = ln(1 + EAR)", styles['Body']), Paragraph("Standard log-yield transformation in financial modeling", styles['Body'])]
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
    out_file = os.path.join(out_dir, "05_Effective_Annual_Rate.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
