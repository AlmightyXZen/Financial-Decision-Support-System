"""
Chapter 02: Discrete Compound Interest & Multi-Period Accumulation.
Textbook chapter with geometric progression derivation, frequency monotonicity proof,
exact doubling time logarithmic formulation, two hand-solved examples, and Python code.
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

    # ==================== PAGE 1: THEORY & DERIVATIONS ====================
    story.append(Paragraph("CHAPTER 2", styles['ChapterLabel']))
    story.append(Paragraph("Discrete Compound Interest & Multi-Period Accumulation", styles['ChapterTitle']))
    story.append(Paragraph(
        "Geometric Sequences, Compounding Frequencies, Monotonicity Theorems, and Logarithmic Doubling Time",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=7))

    story.append(Paragraph("2.1 Definition & Mathematical Axioms", styles['H1']))
    story.append(Paragraph(
        "Compound Interest is the engine of capital accumulation in modern finance. Unlike linear simple interest, "
        "compound accumulation operates on the principle that <b>accrued interest is periodically added to the principal</b>, "
        "generating additional return in all subsequent periods (interest on interest).",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 2.1 (Discrete Compounding Accumulation)</b>", styles['DefHeader']),
        Paragraph(
            "Let initial capital be <i>P</i> &gt; 0, nominal annual interest rate be <i>r</i> &ge; 0 "
            "(decimal fraction: <i>r</i> = <i>R</i> / 100), compounding frequency be <i>n</i> &ge; 1 "
            "(sub-intervals per year: annual <i>n</i>=1, semi-annual <i>n</i>=2, quarterly <i>n</i>=4, monthly <i>n</i>=12), "
            "and total time horizon be <i>t</i> &ge; 0 years.<br/>"
            "The <b>periodic interest rate</b> is <i>i</i> = <i>r</i> / <i>n</i>, and total compounding periods is <i>N</i> = <i>n</i> &middot; <i>t</i>.<br/>"
            "The <b>terminal accumulated value</b> <i>A</i>(<i>t</i>) and <b>net compound interest</b> <i>I</i><sub>comp</sub>(<i>t</i>) are:",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("<i>A</i>(<i>t</i>) = <i>P</i> &middot; (1 + <i>r</i> / <i>n</i>)<sup><i>n</i> &middot; <i>t</i></sup>", styles['Equation']),
        Spacer(1, 1),
        Paragraph("<i>I</i><sub>comp</sub>(<i>t</i>) = <i>A</i>(<i>t</i>) &minus; <i>P</i> = <i>P</i> [(1 + <i>r</i> / <i>n</i>)<sup><i>n</i> &middot; <i>t</i></sup> &minus; 1]", styles['Equation']),
        Spacer(1, 2),
        Paragraph("The accumulation factor is <i>a</i>(<i>t</i>) = (1 + <i>r</i> / <i>n</i>)<sup><i>nt</i></sup>, satisfying <i>a</i>(0) = 1 and <i>a'</i>(<i>t</i>) &gt; 0.", styles['EquationSub'])
    ]
    story.append(make_card(def_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 5))

    story.append(Paragraph("2.2 First-Principles Derivation & Frequency Monotonicity", styles['H1']))
    story.append(Paragraph(
        "<b>Geometric Progression Derivation:</b><br/>"
        "Let <i>A</i><sub><i>k</i></sub> denote wealth at the end of period <i>k</i> with periodic rate <i>i</i> = <i>r</i>/<i>n</i>:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Period 1: <i>A</i><sub>1</sub> = <i>P</i> + <i>P</i>&middot;<i>i</i> = <i>P</i>(1 + <i>i</i>)<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Period 2: <i>A</i><sub>2</sub> = <i>A</i><sub>1</sub>(1 + <i>i</i>) = <i>P</i>(1 + <i>i</i>)<sup>2</sup><br/>"
        "&nbsp;&nbsp;&bull;&nbsp; By induction for <i>N</i> = <i>nt</i> periods: <i>A</i><sub><i>N</i></sub> = <i>P</i>(1 + <i>i</i>)<sup><i>N</i></sup> = <i>P</i>(1 + <i>r</i>/<i>n</i>)<sup><i>nt</i></sup>. &#9632;",
        styles['Body']
    ))

    story.append(Spacer(1, 10))
    story.append(PageBreak())

    # Theorem 2.1
    th_content = [
        Paragraph("<b>Theorem 2.1 (Strict Monotonicity with Respect to Compounding Frequency)</b>", styles['DefHeader']),
        Paragraph(
            "For any fixed annual rate <i>r</i> &gt; 0 and time horizon <i>t</i> &gt; 0, the accumulation factor "
            "<i>a</i>(<i>n</i>) = (1 + <i>r</i>/<i>n</i>)<sup><i>nt</i></sup> is a <b>strictly increasing function</b> of compounding frequency <i>n</i>:<br/>"
            "<font size=9.5><b><i>n</i><sub>1</sub> &lt; <i>n</i><sub>2</sub> &nbsp;&rArr;&nbsp; (1 + <i>r</i>/<i>n</i><sub>1</sub>)<sup><i>n</i><sub>1</sub><i>t</i></sup> &lt; (1 + <i>r</i>/<i>n</i><sub>2</sub>)<sup><i>n</i><sub>2</sub><i>t</i></sup> &nbsp;&lt;&nbsp; <i>e</i><sup><i>rt</i></sup></b></font>",
            styles['Body']
        ),
        Paragraph(
            "<b>Proof:</b> Let <i>x</i> = <i>r</i> / <i>n</i> &gt; 0, so <i>n</i> = <i>r</i> / <i>x</i>. Taking the natural logarithm: "
            "ln <i>a</i>(<i>x</i>) = (<i>rt</i> / <i>x</i>) ln(1 + <i>x</i>) = <i>rt</i> &middot; [ln(1 + <i>x</i>) / <i>x</i>].<br/>"
            "Differentiating with respect to <i>x</i>: <i>d</i>/<i>dx</i> [ln(1 + <i>x</i>) / <i>x</i>] = [<i>x</i>/(1 + <i>x</i>) &minus; ln(1 + <i>x</i>)] / <i>x</i><sup>2</sup>.<br/>"
            "From real analysis, ln(1 + <i>x</i>) &gt; <i>x</i> / (1 + <i>x</i>) for all <i>x</i> &gt; 0. Thus the derivative with respect to <i>x</i> is strictly negative. "
            "Since <i>x</i> = <i>r</i> / <i>n</i> decreases as <i>n</i> increases, [ln(1 + <i>x</i>) / <i>x</i>] strictly increases with <i>n</i>. "
            "Applying the strictly increasing exponential function confirms <i>a</i>(<i>n</i>) is strictly increasing in <i>n</i>. &#9632;",
            styles['Body']
        )
    ]
    story.append(make_card(th_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLE 2.1 ====================
    story.append(Paragraph("2.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: multi-frequency corporate accumulation and exact logarithmic doubling time.",
        styles['Body']
    ))

    # Example 2.1 Card
    ex1_content = [
        Paragraph("<b>Example 2.1: Multi-Frequency Corporate Fixed Deposit</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> An investor commits principal <b><i>P</i> = INR 500,000</b> at nominal interest rate "
            "<b><i>R</i> = 8.40% per annum</b> for <b><i>t</i> = 5 years</b>. Compute terminal accumulated value under:<br/>"
            "&nbsp;&nbsp;&bull; <b>Case A:</b> Annual Compounding (<i>n</i> = 1)<br/>"
            "&nbsp;&nbsp;&bull; <b>Case B:</b> Quarterly Compounding (<i>n</i> = 4)<br/>"
            "&nbsp;&nbsp;&bull; <b>Case C:</b> Monthly Compounding (<i>n</i> = 12)",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Case A (Annual Compounding, <i>n</i> = 1):</b><br/>"
            "&nbsp;&nbsp;&bull; Periodic rate: <i>i</i> = 0.084 / 1 = 0.084<br/>"
            "&nbsp;&nbsp;&bull; Total periods: <i>N</i> = 1 &times; 5 = 5 periods<br/>"
            "&nbsp;&nbsp;&bull; Calculation: <i>A</i><sub>annual</sub> = 500,000 &times; (1.084)<sup>5</sup> = 500,000 &times; 1.4968593 = <b>INR 748,429.65</b><br/><br/>"
            "<b>Case B (Quarterly Compounding, <i>n</i> = 4):</b><br/>"
            "&nbsp;&nbsp;&bull; Periodic rate: <i>i</i> = 0.084 / 4 = 0.021<br/>"
            "&nbsp;&nbsp;&bull; Total periods: <i>N</i> = 4 &times; 5 = 20 periods<br/>"
            "&nbsp;&nbsp;&bull; Calculation: <i>A</i><sub>quarterly</sub> = 500,000 &times; (1.021)<sup>20</sup> = 500,000 &times; 1.5153830 = <b>INR 757,691.50</b><br/><br/>"
            "<b>Case C (Monthly Compounding, <i>n</i> = 12):</b><br/>"
            "&nbsp;&nbsp;&bull; Periodic rate: <i>i</i> = 0.084 / 12 = 0.007<br/>"
            "&nbsp;&nbsp;&bull; Total periods: <i>N</i> = 12 &times; 5 = 60 periods<br/>"
            "&nbsp;&nbsp;&bull; Calculation: <i>A</i><sub>monthly</sub> = 500,000 &times; (1.007)<sup>60</sup> = 500,000 &times; 1.5197581 = <b>INR 759,879.05</b><br/><br/>"
            "<b>Frequency Gain Analysis:</b><br/>"
            "&nbsp;&nbsp;&bull; Monthly vs Annual Surplus: 759,879.05 &minus; 748,429.65 = <b>INR 11,449.40</b> excess wealth.<br/>"
            "&nbsp;&nbsp;&bull; Quarterly vs Annual Surplus: 757,691.50 &minus; 748,429.65 = <b>INR 9,261.85</b> excess wealth.<br/>"
            "&nbsp;&nbsp;&bull; <i>Takeaway:</i> Increasing the compounding frequency from annual to monthly produces an incremental "
            "gain of 2.29% on initial principal with zero additional market risk.",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 3: WORKED EXAMPLE 2.2 ====================
    # Example 2.2 Card
    ex2_content = [
        Paragraph("<b>Example 2.2: Exact Doubling Time vs. The Heuristic 'Rule of 72'</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> Determine the exact time &tau;<sub>2</sub> required to double capital at nominal rate "
            "<b><i>R</i> = 9.00%</b> compounded quarterly (<i>n</i> = 4). Compare against the popular 'Rule of 72'.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Derivation of Exact Doubling Time Equation):</b><br/>"
            "&nbsp;&nbsp;Set terminal value equal to twice principal: <i>A</i>(&tau;<sub>2</sub>) = 2<i>P</i><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;2<i>P</i> = <i>P</i> (1 + <i>r</i>/<i>n</i>)<sup><i>n</i> &middot; &tau;<sub>2</sub></sup> &nbsp;&rArr;&nbsp; 2 = (1 + <i>r</i>/<i>n</i>)<sup><i>n</i> &middot; &tau;<sub>2</sub></sup><br/>"
            "&nbsp;&nbsp;Applying the natural logarithm to both sides:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;ln(2) = <i>n</i> &middot; &tau;<sub>2</sub> &middot; ln(1 + <i>r</i>/<i>n</i>)<br/>"
            "&nbsp;&nbsp;Solving algebraically for duration &tau;<sub>2</sub>:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<b>&tau;<sub>2</sub> = ln(2) / [<i>n</i> &middot; ln(1 + <i>r</i>/<i>n</i>)]</b><br/><br/>"
            "<b>Step 2 (Numerical Evaluation):</b><br/>"
            "&nbsp;&nbsp;&bull; Parameters: <i>r</i> = 0.09, &nbsp; <i>n</i> = 4 &nbsp;&rArr;&nbsp; <i>i</i> = 0.09 / 4 = 0.0225<br/>"
            "&nbsp;&nbsp;&bull; Logarithmic values: ln(2) &approx; 0.69314718, &nbsp; ln(1.0225) &approx; 0.02225059<br/>"
            "&nbsp;&nbsp;&bull; Denominator: 4 &times; 0.02225059 = 0.08900236<br/>"
            "&nbsp;&nbsp;&bull; Exact Doubling Horizon: &tau;<sub>2</sub> = 0.69314718 / 0.08900236 = <b>7.78796 years</b> (&approx; 7 yrs, 9.5 mos).<br/><br/>"
            "<b>Step 3 (Evaluation of Rule of 72 Heuristic):</b><br/>"
            "&nbsp;&nbsp;&tau;<sub>heuristic</sub> = 72 / <i>R</i> = 72 / 9 = <b>8.0000 years</b>.<br/><br/>"
            "<b>Step 4 (Error & Analytical Insight):</b><br/>"
            "&nbsp;&nbsp;&bull; Absolute error: &tau;<sub>heuristic</sub> &minus; &tau;<sub>2</sub> = 8.0000 &minus; 7.7880 = <b>+0.212 years</b> (+2.54 months).<br/>"
            "&nbsp;&nbsp;&bull; Relative error: 0.212 / 7.788 &approx; <b>+2.72%</b> overestimation.<br/>"
            "&nbsp;&nbsp;&bull; <i>Theoretical origin:</i> The Rule of 72 stems from ln(2) &approx; 0.693 &approx; 0.72 (adjusted to account for "
            "compounding drift at mid-range interest rates). In algorithmic financial systems, the closed-form logarithmic "
            "formula is required to avoid cumulative timing errors.",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 4: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("2.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the production-grade Python implementation from <code>models/time_value.py</code>, "
        "featuring frequency validation, type safety, and doubling time analysis:",
        styles['Body']
    ))

    code_raw = (
        "import math\n\n"
        "def compound_interest_amount(\n"
        "    principal: float, annual_rate: float, time_years: float, compounding_frequency: int = 1\n"
        ") -> float:\n"
        "    \"\"\"\n"
        "    Computes terminal wealth under discrete compounding: A = P * (1 + r / n) ** (n * t).\n"
        "    \"\"\"\n"
        "    if principal < 0.0 or annual_rate < 0.0 or time_years < 0.0 or compounding_frequency <= 0:\n"
        "        raise ValueError(\"Invalid parameters: financial arguments must be non-negative, n >= 1.\")\n"
        "    periodic_rate = annual_rate / compounding_frequency\n"
        "    total_periods = compounding_frequency * time_years\n"
        "    return float(principal * ((1.0 + periodic_rate) ** total_periods))\n\n\n"
        "def compound_doubling_time(annual_rate: float, compounding_frequency: int = 1) -> float:\n"
        "    \"\"\"\n"
        "    Computes exact doubling time: tau_2 = ln(2) / [n * ln(1 + r / n)].\n"
        "    \"\"\"\n"
        "    if annual_rate <= 0.0 or compounding_frequency <= 0:\n"
        "        raise ValueError(\"Rate must be strictly positive and n >= 1 for doubling.\")\n"
        "    periodic_rate = annual_rate / compounding_frequency\n"
        "    return float(math.log(2.0) / (compounding_frequency * math.log(1.0 + periodic_rate)))\n"
    )
    story.append(make_code_card(code_raw, title="models/time_value.py — Discrete Compounding Engine"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Formula</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>Domain & Constraints</b>", styles['Body']), Paragraph("<i>P</i> &gt; 0, <i>r</i> &ge; 0, <i>t</i> &ge; 0, <i>n</i> &ge; 1", styles['Body']), Paragraph("Discrete periodic compounding structure", styles['Body'])],
        [Paragraph("<b>Accumulation Factor</b>", styles['Body']), Paragraph("<i>a</i>(<i>t</i>) = (1 + <i>r</i>/<i>n</i>)<sup><i>nt</i></sup>", styles['Body']), Paragraph("Superlinear exponential growth operator", styles['Body'])],
        [Paragraph("<b>Frequency Limit</b>", styles['Body']), Paragraph("lim<sub><i>n</i>&rarr;&infin;</sub> <i>a</i>(<i>t</i>) = <i>e</i><sup><i>rt</i></sup>", styles['Body']), Paragraph("Upper supremum bound achieved under continuous compounding", styles['Body'])],
        [Paragraph("<b>Convexity</b>", styles['Body']), Paragraph("<i>d</i><sup>2</sup><i>a</i>/<i>dt</i><sup>2</sup> &gt; 0 &nbsp;&forall; <i>t</i> &ge; 0", styles['Body']), Paragraph("Strict convexity drives compounding velocity acceleration", styles['Body'])],
        [Paragraph("<b>Doubling Time</b>", styles['Body']), Paragraph("&tau;<sub>2</sub> = ln(2) / [<i>n</i> ln(1 + <i>r</i>/<i>n</i>)]", styles['Body']), Paragraph("Exact logarithmic capital replication milestone", styles['Body'])]
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
    out_file = os.path.join(out_dir, "02_Compound_Interest.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
