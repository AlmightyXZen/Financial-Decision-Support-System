"""
Chapter 08: Inflation Dynamics & Real Purchasing Power.
Textbook chapter on nominal vs real wealth, the exact Fisher relation,
purchasing power decay functions, 25-year retirement erosion, and Python code.
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
    story.append(Paragraph("CHAPTER 8", styles['ChapterLabel']))
    story.append(Paragraph("Inflation Dynamics & Real Purchasing Power", styles['ChapterTitle']))
    story.append(Paragraph(
        "The Fisher Equation, Purchasing Power Degradation Functions, Real vs Nominal Return Spreads, and Wealth Erosion",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=7))

    story.append(Paragraph("8.1 The Nominal Illusion & The Fisher Relation", styles['H1']))
    story.append(Paragraph(
        "Financial calculators and marketing materials often commit the fallacy of projecting wealth in **nominal currency units**, "
        "ignoring the compounding decay of monetary purchasing power caused by inflation. "
        "An investor's actual economic utility depends not on the number of currency units held, but on the basket of real goods and services "
        "those units can purchase.",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 8.1 (The Exact Fisher Equation & Real Yield)</b>", styles['DefHeader']),
        Paragraph(
            "Let nominal annual growth rate be <i>r</i><sub>nom</sub> &ge; 0 and annual headline inflation rate be <i>i</i> &ge; 0.<br/>"
            "The <b>exact real rate of return</b> <i>r</i><sub>real</sub> satisfies the multiplicative identity:<br/>"
            "(1 + <i>r</i><sub>nom</sub>) = (1 + <i>r</i><sub>real</sub>) &middot; (1 + <i>i</i>)",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("<i>r</i><sub>real</sub> = [ (1 + <i>r</i><sub>nom</sub>) / (1 + <i>i</i>) ] &minus; 1 = (<i>r</i><sub>nom</sub> &minus; <i>i</i>) / (1 + <i>i</i>)", styles['Equation']),
        Spacer(1, 2),
        Paragraph("The popular linear approximation <i>r</i><sub>real</sub> &approx; <i>r</i><sub>nom</sub> &minus; <i>i</i> omits the cross-term <i>r</i><sub>real</sub> &middot; <i>i</i>.", styles['EquationSub'])
    ]
    story.append(make_card(def_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 5))

    story.append(Paragraph("8.2 Purchasing Power Degradation Factor", styles['H1']))
    story.append(Paragraph(
        "<b>Exponential Purchasing Power Decay:</b><br/>"
        "Let a consumer basket price at time <i>t</i> = 0 be normalized to <i>P</i><sub>0</sub> = 1. "
        "Under constant compound inflation <i>i</i>, the price index at time <i>t</i> is <i>P</i>(<i>t</i>) = (1 + <i>i</i>)<sup><i>t</i></sup>.<br/>"
        "The **Purchasing Power Retention (PPR)** factor represents the fraction of initial purchasing power retained by a fixed nominal sum:",
        styles['Body']
    ))

    # Degradation Card
    th_content = [
        Paragraph("<b>Proposition 8.1 (Purchasing Power Discount Factor)</b>", styles['DefHeader']),
        Paragraph(
            "<font size=10.5><b><i>PPR</i>(<i>t</i>) = (1 + <i>i</i>)<sup>&minus;<i>t</i></sup> &nbsp;&nbsp;&rArr;&nbsp;&nbsp; <i>FV</i><sub>real</sub>(<i>t</i>) = <i>FV</i><sub>nom</sub>(<i>t</i>) &middot; (1 + <i>i</i>)<sup>&minus;<i>t</i></sup></b></font>",
            styles['Equation']
        ),
        Paragraph(
            "Under continuous inflation rate <i>i</i><sub>cont</sub>, <i>PPR</i>(<i>t</i>) = exp(&minus;<i>i</i><sub>cont</sub> &middot; <i>t</i>).<br/>"
            "<b>Half-Life of Currency Value (&tau;<sub>1/2</sub>):</b> Time required for inflation to halve purchasing power:<br/>"
            "&tau;<sub>1/2</sub> = ln(2) / ln(1 + <i>i</i>) &approx; 72 / <i>I</i><sub>%</sub>.",
            styles['Body']
        )
    ]
    story.append(make_card(th_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLE 8.1 ====================
    story.append(Paragraph("8.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: real purchasing power decay of a retirement corpus, "
        "and exact Fisher hurdle rate calibration for institutional portfolios.",
        styles['Body']
    ))

    # Example 8.1 Card
    ex1_content = [
        Paragraph("<b>Example 8.1: Real Purchasing Power Decay of a 25-Year Retirement Corpus</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> An investor accumulates a nominal retirement nest egg of <b><i>FV</i><sub>nom</sub> = INR 20,000,000</b> (2 Crores) "
            "over a career spanning <b><i>t</i> = 25 years</b>. Assuming long-term average consumer inflation averages "
            "<b><i>i</i> = 6.00% per annum</b>, determine the true real purchasing power of the corpus in today's rupees "
            "and compute the total purchasing power erosion percentage.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Compute Cumulative Price Level Deflator):</b><br/>"
            "&nbsp;&nbsp;&bull; Inflation factor: 1 + <i>i</i> = 1.0600<br/>"
            "&nbsp;&nbsp;&bull; Price expansion across 25 years: (1.06)<sup>25</sup> &approx; 4.2918707.<br/>"
            "&nbsp;&nbsp;&bull; <i>Meaning:</i> Goods costing INR 1.00 today will cost INR 4.29 after 25 years.<br/><br/>"
            "<b>Step 2 (Purchasing Power Retention Factor):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>PPR</i>(25) = (1.06)<sup>&minus;25</sup> = 1 / 4.2918707 &approx; <b>0.2329986</b> (23.30% retention).<br/><br/>"
            "<b>Step 3 (Terminal Real Wealth Calculation):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>FV</i><sub>real</sub> = <i>FV</i><sub>nom</sub> &times; <i>PPR</i>(25) = 20,000,000 &times; 0.2329986<br/>"
            "&nbsp;&nbsp;&bull; <b>Real Value in Today's Rupees:</b> <i>FV</i><sub>real</sub> = <b>INR 4,659,973.00</b>.<br/><br/>"
            "<b>Step 4 (Erosion Analysis & Macroeconomic Takeaway):</b><br/>"
            "&nbsp;&nbsp;&bull; Absolute purchasing power loss: 20,000,000 &minus; 4,659,973 = <b>INR 15,340,027.00</b>.<br/>"
            "&nbsp;&nbsp;&bull; Percentage Erosion: 15,340,027 / 20,000,000 = <b>76.70% total decay</b>.<br/>"
            "&nbsp;&nbsp;&bull; <i>Analytical Insight:</i> A 6% inflation rate strips away more than three-quarters of real capital over 25 years. "
            "Financial decision systems must mandate real inflation adjustments to prevent disastrous retirement shortfall.",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 3: WORKED EXAMPLE 8.2 ====================
    # Example 8.2 Card
    ex2_content = [
        Paragraph("<b>Example 8.2: Exact Fisher Hurdle Rate Calibration</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> An endowment fund targets a guaranteed <b>real annual return of <i>r</i><sub>real</sub> = 5.00%</b> "
            "to maintain intergenerational purchasing power. If long-term projected inflation is <b><i>i</i> = 7.00%</b>, "
            "compute the exact nominal return hurdle required. Compare against the common linear rule of thumb.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Exact Fisher Formulation):</b><br/>"
            "&nbsp;&nbsp;From Definition 8.1, the exact nominal yield required is:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;1 + <i>r</i><sub>nom</sub> = (1 + <i>r</i><sub>real</sub>) &middot; (1 + <i>i</i>)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;1 + <i>r</i><sub>nom</sub> = (1 + 0.05) &times; (1 + 0.07)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;1 + <i>r</i><sub>nom</sub> = 1.05 &times; 1.07 = 1.1235<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<b>Exact Nominal Hurdle:</b> <i>r</i><sub>nom</sub> = 1.1235 &minus; 1 = 0.1235 &implies; <b>12.35% per annum</b>.<br/><br/>"
            "<b>Step 2 (Linear Approximation Evaluation):</b><br/>"
            "&nbsp;&nbsp;&bull; Heuristic Formula: <i>r</i><sub>approx</sub> = <i>r</i><sub>real</sub> + <i>i</i> = 5.00% + 7.00% = <b>12.00% per annum</b>.<br/><br/>"
            "<b>Step 3 (Discrepancy & Cross-Term Derivation):</b><br/>"
            "&nbsp;&nbsp;&bull; Cross-product term: <i>r</i><sub>real</sub> &middot; <i>i</i> = 0.05 &times; 0.07 = 0.0035 = <b>+0.35% (+35 basis points)</b>.<br/>"
            "&nbsp;&nbsp;&bull; Discrepancy: 12.35% &minus; 12.00% = <b>0.35% underestimation</b>.<br/><br/>"
            "<b>Step 4 (Portfolio Compounding Consequence on INR 10,000,000 over 20 Years):</b><br/>"
            "&nbsp;&nbsp;&bull; Corpus at exact 12.35%: 10,000,000 &times; (1.1235)<sup>20</sup> = 10,000,000 &times; 10.2857 = <b>INR 102,857,000</b>.<br/>"
            "&nbsp;&nbsp;&bull; Corpus at heuristic 12.00%: 10,000,000 &times; (1.1200)<sup>20</sup> = 10,000,000 &times; 9.6463 = <b>INR 96,463,000</b>.<br/>"
            "&nbsp;&nbsp;&bull; Difference: <b>INR 6,394,000 shortfall</b> from omitting a 35 bps cross-term! "
            "This proves why quantitative systems must utilize the exact multiplicative Fisher identity.",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 4: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("8.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the complete implementation from <code>models/investment_plans.py</code>, "
        "featuring exact Fisher conversion, real wealth deflators, and purchasing power retention metrics:",
        styles['Body']
    ))

    code_raw = (
        "def real_rate_fisher(nominal_rate: float, inflation_rate: float) -> float:\n"
        "    \"\"\"\n"
        "    Computes exact real return: r_real = (r_nom - i) / (1 + i).\n"
        "    \"\"\"\n"
        "    if inflation_rate <= -1.0:\n"
        "        raise ValueError(\"Inflation rate must be strictly greater than -100%.\")\n"
        "    return float((nominal_rate - inflation_rate) / (1.0 + inflation_rate))\n\n\n"
        "def nominal_rate_from_real(real_rate: float, inflation_rate: float) -> float:\n"
        "    \"\"\"\n"
        "    Computes required nominal hurdle: r_nom = (1 + r_real) * (1 + i) - 1.\n"
        "    \"\"\"\n"
        "    return float(((1.0 + real_rate) * (1.0 + inflation_rate)) - 1.0)\n\n\n"
        "def real_future_value(nominal_fv: float, inflation_rate: float, time_years: float) -> float:\n"
        "    \"\"\"\n"
        "    Deflates nominal future value into today's purchasing power: FV_real = FV / (1 + i) ** t.\n"
        "    \"\"\"\n"
        "    if nominal_fv < 0.0 or inflation_rate < -1.0 or time_years < 0.0:\n"
        "        raise ValueError(\"Invalid parameters for inflation discounting.\")\n"
        "    return float(nominal_fv / ((1.0 + inflation_rate) ** time_years))\n"
    )
    story.append(make_code_card(code_raw, title="models/investment_plans.py — Inflation & Real Value Engine"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("8.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Formula</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>Fisher Relation</b>", styles['Body']), Paragraph("1 + <i>r</i><sub>nom</sub> = (1 + <i>r</i><sub>real</sub>)(1 + <i>i</i>)", styles['Body']), Paragraph("Fundamental multi-asset macroeconomic equilibrium", styles['Body'])],
        [Paragraph("<b>Cross-Term Drag</b>", styles['Body']), Paragraph("&Delta; = <i>r</i><sub>real</sub> &middot; <i>i</i>", styles['Body']), Paragraph("Source of structural underestimation in linear rules of thumb", styles['Body'])],
        [Paragraph("<b>PPR Function</b>", styles['Body']), Paragraph("<i>PPR</i>(<i>t</i>) = (1 + <i>i</i>)<sup>&minus;<i>t</i></sup>", styles['Body']), Paragraph("Exponential half-life decay of purchasing power over time", styles['Body'])],
        [Paragraph("<b>Continuous Fisher</b>", styles['Body']), Paragraph("<i>r</i><sub>real</sub> = <i>r</i><sub>nom</sub> &minus; <i>i</i>", styles['Body']), Paragraph("Exact additive relation holds cleanly under continuous logging", styles['Body'])],
        [Paragraph("<b>Inflation Half-Life</b>", styles['Body']), Paragraph("&tau;<sub>1/2</sub> = ln(2) / ln(1 + <i>i</i>)", styles['Body']), Paragraph("Exact capital halving period under sustained inflation", styles['Body'])]
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
    out_file = os.path.join(out_dir, "08_Inflation_and_Purchasing_Power.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
