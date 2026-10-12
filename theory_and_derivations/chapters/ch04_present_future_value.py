"""
Chapter 04: Present Value, Future Value & Discounting Mechanics.
Textbook chapter on discount factors, temporal equivalence principle,
zero-coupon bond pricing, multi-stage cash flow stream discounting, and Python code.
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
    story.append(Paragraph("CHAPTER 4", styles['ChapterLabel']))
    story.append(Paragraph("Present Value, Future Value & Discounting", styles['ChapterTitle']))
    story.append(Paragraph(
        "Discount Factors, The Temporal Equivalence Principle, Multi-Period Cash Flow Sums, and No-Arbitrage Pricing",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=7))

    story.append(Paragraph("4.1 Definition & The Discounting Factor", styles['H1']))
    story.append(Paragraph(
        "The fundamental axiom of financial economics is the <b>Time Value of Money</b>: capital available today is worth "
        "more than an identical nominal amount in the future due to its earning capacity and risk premium. "
        "<b>Discounting</b> is the mathematical operation inverse to compounding, translating future obligations into today's capital.",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 4.1 (Discount Factors & Present Value)</b>", styles['DefHeader']),
        Paragraph(
            "Let a cash flow <i>FV</i> be received at time <i>t</i> &ge; 0, and let <i>r</i> &ge; 0 be the annual discount rate.<br/>"
            "The <b>discrete discount factor</b> <i>v</i>(<i>t</i>) and <b>Present Value</b> <i>PV</i> are defined by:",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("<i>PV</i> = <i>FV</i> &middot; (1 + <i>r</i>)<sup>&minus;<i>t</i></sup> = <i>FV</i> / (1 + <i>r</i>)<sup><i>t</i></sup>", styles['Equation']),
        Spacer(1, 1),
        Paragraph("<i>PV</i><sub>cont</sub> = <i>FV</i> &middot; <i>e</i><sup>&minus;<i>rt</i></sup> &nbsp; (under continuous discounting)", styles['Equation']),
        Spacer(1, 2),
        Paragraph("where <i>v</i> = (1 + <i>r</i>)<sup>&minus;1</sup> is the unit-period discount factor. Note <i>v</i>(0) = 1 and lim<sub><i>t</i>&rarr;&infin;</sub> <i>v</i>(<i>t</i>) = 0.", styles['EquationSub'])
    ]
    story.append(make_card(def_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 5))

    story.append(Paragraph("4.2 The Principle of Temporal Financial Equivalence", styles['H1']))
    story.append(Paragraph(
        "<b>No-Arbitrage Consistency:</b> Two cash flow streams are economically equivalent at discount rate <i>r</i> "
        "if and only if their present values at time <i>t</i> = 0 are identical. Under frictionless financial markets:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <b>Time Shift Invariance:</b> The value of capital <i>C</i> evaluated at time <i>t</i><sub>2</sub> "
        "from its valuation at <i>t</i><sub>1</sub> satisfies: <i>V</i>(<i>t</i><sub>2</sub>) = <i>V</i>(<i>t</i><sub>1</sub>) &middot; (1 + <i>r</i>)<sup><i>t</i><sub>2</sub> &minus; <i>t</i><sub>1</sub></sup>.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <b>Linear Additivity:</b> The present value of a multi-period cash flow stream {<i>C</i><sub>1</sub>, <i>C</i><sub>2</sub>, ..., <i>C</i><sub><i>m</i></sub>} "
        "at times {<i>t</i><sub>1</sub>, <i>t</i><sub>2</sub>, ..., <i>t</i><sub><i>m</i></sub>} is the linear sum:",
        styles['Body']
    ))

    # Additivity Box
    sum_content = [
        Paragraph("<b>Proposition 4.1 (Linear Valuation of Cash Flow Streams)</b>", styles['DefHeader']),
        Paragraph(
            "<font size=10.5><b><i>PV</i><sub>total</sub> = &sum;<sub><i>k</i>=1</sub><sup><i>m</i></sup> <i>C</i><sub><i>k</i></sub> &middot; (1 + <i>r</i>)<sup>&minus;<i>t</i><sub><i>k</i></sub></sup> "
            "= &sum;<sub><i>k</i>=1</sub><sup><i>m</i></sup> <i>C</i><sub><i>k</i></sub> &middot; <i>v</i><sup><i>t</i><sub><i>k</i></sub></sup></b></font>",
            styles['Equation']
        ),
        Paragraph(
            "Under continuous discounting with term-structure rate curve <i>r</i>(<i>s</i>): "
            "<i>PV</i> = &sum; <i>C</i><sub><i>k</i></sub> exp(&minus;&int;<sub>0</sub><sup><i>t</i><sub><i>k</i></sub></sup> <i>r</i>(<i>s</i>) <i>ds</i>).",
            styles['EquationSub']
        )
    ]
    story.append(make_card(sum_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLE 4.1 ====================
    story.append(Paragraph("4.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: pricing a zero-coupon sovereign treasury bond, "
        "and evaluating a multi-stage deferred corporate cash flow stream.",
        styles['Body']
    ))

    # Example 4.1 Card
    ex1_content = [
        Paragraph("<b>Example 4.1: Fair Valuation of a Zero-Coupon Sovereign Bond</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> A zero-coupon government security guarantees a bullet face value payment of "
            "<b><i>FV</i> = INR 1,000,000</b> at maturity in <b><i>t</i> = 7 years</b>. If the prevailing sovereign hurdle yield "
            "is <b><i>R</i> = 7.25% per annum</b>, determine the fair theoretical price today under:<br/>"
            "&nbsp;&nbsp;&bull; <b>Case A:</b> Annual Discounting &nbsp;|&nbsp; <b>Case B:</b> Continuous Discounting",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Case A (Annual Discounting):</b><br/>"
            "&nbsp;&nbsp;&bull; Parameter: <i>r</i> = 7.25 / 100 = 0.0725, &nbsp; <i>t</i> = 7 years.<br/>"
            "&nbsp;&nbsp;&bull; Compounding factor: (1 + 0.0725)<sup>7</sup> = (1.0725)<sup>7</sup> &approx; 1.6304018<br/>"
            "&nbsp;&nbsp;&bull; Discount factor: <i>v</i>(7) = (1.6304018)<sup>&minus;1</sup> &approx; 0.6133457<br/>"
            "&nbsp;&nbsp;&bull; Fair Price: <i>PV</i><sub>annual</sub> = 1,000,000 &times; 0.6133457 = <b>INR 613,345.70</b>.<br/><br/>"
            "<b>Case B (Continuous Discounting):</b><br/>"
            "&nbsp;&nbsp;&bull; Exponent: &minus;<i>r</i> &middot; <i>t</i> = &minus;(0.0725 &times; 7) = &minus;0.5075<br/>"
            "&nbsp;&nbsp;&bull; Discount kernel: <i>e</i><sup>&minus;0.5075</sup> &approx; 0.6019979<br/>"
            "&nbsp;&nbsp;&bull; Fair Price: <i>PV</i><sub>cont</sub> = 1,000,000 &times; 0.6019979 = <b>INR 601,997.90</b>.<br/><br/>"
            "<b>Pricing Spread Analysis:</b><br/>"
            "&nbsp;&nbsp;&bull; Difference: <i>PV</i><sub>annual</sub> &minus; <i>PV</i><sub>cont</sub> = 613,345.70 &minus; 601,997.90 = <b>INR 11,347.80</b>.<br/>"
            "&nbsp;&nbsp;&bull; <i>Insight:</i> Continuous discounting applies compounding infinitely often, creating a stronger discount drag "
            "that lowers the present fair price relative to discrete annual conventions.",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 3: WORKED EXAMPLE 4.2 ====================
    # Example 4.2 Card
    ex2_content = [
        Paragraph("<b>Example 4.2: Multi-Stage Deferred Corporate Cash Flow Stream</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> A corporate project promises three contractual cash inflows: "
            "<b><i>C</i><sub>1</sub> = INR 200,000</b> at <i>t</i><sub>1</sub> = 1 yr, "
            "<b><i>C</i><sub>2</sub> = INR 400,000</b> at <i>t</i><sub>2</sub> = 3 yrs, and "
            "<b><i>C</i><sub>3</sub> = INR 800,000</b> at <i>t</i><sub>3</sub> = 5 yrs. "
            "Using a benchmark discount rate of <b><i>R</i> = 8.00%</b>, compute:<br/>"
            "&nbsp;&nbsp;&bull; Total Present Value (<i>PV</i><sub>total</sub>) at <i>t</i> = 0<br/>"
            "&nbsp;&nbsp;&bull; Total Future Value (<i>FV</i><sub>5</sub>) accumulated at <i>t</i> = 5 years",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Discounting Individual Cash Inflows to <i>t</i> = 0):</b><br/>"
            "&nbsp;&nbsp;&bull; Year 1: <i>PV</i><sub>1</sub> = 200,000 / (1.08)<sup>1</sup> = 200,000 &times; 0.9259259 = <b>INR 185,185.19</b><br/>"
            "&nbsp;&nbsp;&bull; Year 3: <i>PV</i><sub>2</sub> = 400,000 / (1.08)<sup>3</sup> = 400,000 &times; 0.7938322 = <b>INR 317,532.90</b><br/>"
            "&nbsp;&nbsp;&bull; Year 5: <i>PV</i><sub>3</sub> = 800,000 / (1.08)<sup>5</sup> = 800,000 &times; 0.6805832 = <b>INR 544,466.56</b><br/><br/>"
            "<b>Step 2 (Linear Summation for Aggregate Present Value):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>PV</i><sub>total</sub> = 185,185.19 + 317,532.90 + 544,466.56 = <b>INR 1,047,184.65</b>.<br/><br/>"
            "<b>Step 3 (Compounding to Terminal Horizon <i>t</i> = 5):</b><br/>"
            "&nbsp;&nbsp;By the principle of temporal financial equivalence, compounding total PV to year 5 must exactly equal "
            "compounding each individual cash flow to year 5:<br/>"
            "&nbsp;&nbsp;&bull; <i>FV</i><sub>5</sub> = <i>PV</i><sub>total</sub> &times; (1.08)<sup>5</sup> = 1,047,184.65 &times; 1.4693281 = <b>INR 1,538,658.00</b>.<br/><br/>"
            "<b>Step 4 (Direct Forward Cash Flow Check):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>C</i><sub>1</sub> compounded 4 yrs: 200,000 &times; (1.08)<sup>4</sup> = 200,000 &times; 1.360489 = INR 272,097.80<br/>"
            "&nbsp;&nbsp;&bull; <i>C</i><sub>2</sub> compounded 2 yrs: 400,000 &times; (1.08)<sup>2</sup> = 400,000 &times; 1.166400 = INR 466,560.00<br/>"
            "&nbsp;&nbsp;&bull; <i>C</i><sub>3</sub> compounded 0 yrs: 800,000 &times; 1.000000 = INR 800,000.00<br/>"
            "&nbsp;&nbsp;&bull; Sum: 272,097.80 + 466,560.00 + 800,000.00 = <b>INR 1,538,657.80</b> (verified exact temporal equivalence).",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 4: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("4.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the production-grade Python implementation from <code>models/time_value.py</code>, "
        "supporting single cash flows and multi-stage cash flow stream valuations:",
        styles['Body']
    ))

    code_raw = (
        "from typing import List, Tuple\n"
        "import math\n\n"
        "def present_value(future_value: float, annual_rate: float, time_years: float) -> float:\n"
        "    \"\"\"Computes discrete present value: PV = FV / (1 + r) ** t.\"\"\"\n"
        "    if future_value < 0.0 or annual_rate < 0.0 or time_years < 0.0:\n"
        "        raise ValueError(\"Arguments must be non-negative.\")\n"
        "    return float(future_value / ((1.0 + annual_rate) ** time_years))\n\n\n"
        "def present_value_stream(cash_flows: List[Tuple[float, float]], annual_rate: float) -> float:\n"
        "    \"\"\"\n"
        "    Computes aggregate present value of stream: [(cash_flow, time_years), ...].\n"
        "    PV_total = sum(C_k / (1 + r) ** t_k).\n"
        "    \"\"\"\n"
        "    if annual_rate < 0.0:\n"
        "        raise ValueError(\"Discount rate must be non-negative.\")\n"
        "    return sum(float(cf / ((1.0 + annual_rate) ** t)) for cf, t in cash_flows)\n"
    )
    story.append(make_code_card(code_raw, title="models/time_value.py — Discounting & Valuation Engine"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("4.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Formula</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>Discount Factor</b>", styles['Body']), Paragraph("<i>v</i>(<i>t</i>) = (1 + <i>r</i>)<sup>&minus;<i>t</i></sup>", styles['Body']), Paragraph("Monotonically decaying pricing kernel", styles['Body'])],
        [Paragraph("<b>Asymptotic Horizon</b>", styles['Body']), Paragraph("lim<sub><i>t</i>&rarr;&infin;</sub> <i>v</i>(<i>t</i>) = 0", styles['Body']), Paragraph("Distant cash flows have negligible present economic weight", styles['Body'])],
        [Paragraph("<b>Rate Sensitivity (Duration)</b>", styles['Body']), Paragraph("<i>d</i>(<i>PV</i>)/<i>dr</i> = &minus;<i>t</i> &middot; <i>FV</i> (1+<i>r</i>)<sup>&minus;<i>t</i>&minus;1</sup>", styles['Body']), Paragraph("Negative first derivative reflects interest rate risk", styles['Body'])],
        [Paragraph("<b>Convexity</b>", styles['Body']), Paragraph("<i>d</i><sup>2</sup>(<i>PV</i>)/<i>dr</i><sup>2</sup> &gt; 0", styles['Body']), Paragraph("Bond price convexity protects long positions against rate swings", styles['Body'])],
        [Paragraph("<b>Continuous Kernel</b>", styles['Body']), Paragraph("<i>v</i><sub>cont</sub>(<i>t</i>) = <i>e</i><sup>&minus;<i>rt</i></sup>", styles['Body']), Paragraph("Standard continuous discount factor in stochastic finance", styles['Body'])]
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
    out_file = os.path.join(out_dir, "04_Present_Value_and_Future_Value.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
