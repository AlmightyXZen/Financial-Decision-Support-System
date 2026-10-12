"""
Chapter 07: Systematic Investment Plan (SIP) & Wealth Accumulation.
Textbook chapter on annuity-due models, geometric series derivation,
15-year equity wealth accumulation, step-up SIP mechanics, and Python code.
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
    story.append(Paragraph("CHAPTER 7", styles['ChapterLabel']))
    story.append(Paragraph("Systematic Investment Plan (SIP) & Accumulation", styles['ChapterTitle']))
    story.append(Paragraph(
        "Annuity-Due Formulations, Geometric Progression Derivations, Dollar-Cost Averaging, and Step-Up Dynamics",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=7))

    story.append(Paragraph("7.1 Definition & The Annuity-Due Model", styles['H1']))
    story.append(Paragraph(
        "A Systematic Investment Plan (SIP) represents a disciplined capital accumulation model where an investor commits "
        "a constant periodic cash contribution <i>C</i> into a compounding financial asset. "
        "Because contributions are conventionally deposited at the <b>beginning of each periodic interval</b>, "
        "the financial cash flow stream is categorized mathematically as an <b>Annuity-Due</b>.",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 7.1 (Closed-Form SIP Future Value Equation)</b>", styles['DefHeader']),
        Paragraph(
            "Let periodic contribution be <i>C</i> &gt; 0, nominal annual return rate be <i>r</i> &ge; 0, "
            "and investment horizon be <i>t</i> years. With monthly contributions (<i>m</i> = 12), the periodic rate is "
            "<i>r</i><sub><i>m</i></sub> = <i>r</i> / 12 and total contribution count is <i>N</i> = 12 &middot; <i>t</i>.<br/>"
            "The <b>terminal future value</b> <i>FV</i><sub>SIP</sub> at the end of month <i>N</i> is:",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("<i>FV</i><sub>SIP</sub> = <i>C</i> &middot; (1 + <i>r</i><sub><i>m</i></sub>) &middot; [ ((1 + <i>r</i><sub><i>m</i></sub>)<sup><i>N</i></sup> &minus; 1) / <i>r</i><sub><i>m</i></sub> ]", styles['Equation']),
        Spacer(1, 2),
        Paragraph("When <i>r</i><sub><i>m</i></sub> = 0, the equation reduces to total uncompounded principal: <i>FV</i> = <i>C</i> &middot; <i>N</i>.", styles['EquationSub'])
    ]
    story.append(make_card(def_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 5))

    story.append(Paragraph("7.2 First-Principles Derivation via Geometric Series", styles['H1']))
    story.append(Paragraph(
        "<b>Step-by-Step Mathematical Proof:</b><br/>"
        "Consider the compounded value of each individual monthly contribution at terminal horizon <i>t</i> = <i>N</i>:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Deposit 1 (at start of Month 1, <i>t</i> = 0): compounds for <i>N</i> months &rArr; <i>C</i>(1 + <i>r</i><sub><i>m</i></sub>)<sup><i>N</i></sup><br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Deposit 2 (at start of Month 2, <i>t</i> = 1): compounds for <i>N</i>&minus;1 months &rArr; <i>C</i>(1 + <i>r</i><sub><i>m</i></sub>)<sup><i>N</i>&minus;1</sup><br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Deposit <i>N</i> (at start of Month <i>N</i>, <i>t</i> = <i>N</i>&minus;1): compounds for 1 month &rArr; <i>C</i>(1 + <i>r</i><sub><i>m</i></sub>)<sup>1</sup>.<br/>"
        "The total terminal wealth is the sum of these <i>N</i> compound values:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <i>FV</i> = &sum;<sub><i>k</i>=1</sub><sup><i>N</i></sup> <i>C</i> (1 + <i>r</i><sub><i>m</i></sub>)<sup><i>k</i></sup> "
        "= <i>C</i> &sum;<sub><i>k</i>=1</sub><sup><i>N</i></sup> <i>q</i><sup><i>k</i></sup>, &nbsp; where common ratio <i>q</i> = 1 + <i>r</i><sub><i>m</i></sub>.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Applying the finite geometric summation formula &sum;<sub><i>k</i>=1</sub><sup><i>N</i></sup> <i>q</i><sup><i>k</i></sup> = <i>q</i> [ (<i>q</i><sup><i>N</i></sup> &minus; 1) / (<i>q</i> &minus; 1) ]:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Since <i>q</i> &minus; 1 = (1 + <i>r</i><sub><i>m</i></sub>) &minus; 1 = <i>r</i><sub><i>m</i></sub>, substituting gives:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>FV</i> = <i>C</i> &middot; (1 + <i>r</i><sub><i>m</i></sub>) &middot; [ ((1 + <i>r</i><sub><i>m</i></sub>)<sup><i>N</i></sup> &minus; 1) / <i>r</i><sub><i>m</i></sub> ]. &#9632;",
        styles['Body']
    ))

    # Annuity Comparison Card
    th_content = [
        Paragraph("<b>Theorem 7.1 (Annuity-Due vs. Annuity-Immediate Relation)</b>", styles['DefHeader']),
        Paragraph(
            "An annuity-due investment stream strictly exceeds an annuity-immediate stream by a compound factor of (1 + <i>r</i><sub><i>m</i></sub>):<br/>"
            "<font size=10><b><i>FV</i><sub>due</sub> = <i>FV</i><sub>immediate</sub> &middot; (1 + <i>r</i><sub><i>m</i></sub>)</b></font>",
            styles['Body']
        ),
        Paragraph(
            "<i>Analytical Consequence:</i> Contributing at the start of each month rather than at month-end guarantees "
            "an immediate +<i>r</i><sub><i>m</i></sub> percentage boost across the entire terminal accumulated wealth.",
            styles['Body']
        )
    ]
    story.append(make_card(th_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLE 7.1 ====================
    story.append(Paragraph("7.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: a 15-year equity wealth accumulation plan, "
        "and an annually stepped-up SIP compounding trajectory.",
        styles['Body']
    ))

    # Example 7.1 Card
    ex1_content = [
        Paragraph("<b>Example 7.1: 15-Year Mutual Fund SIP Wealth Creation</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> An investor commits <b><i>C</i> = INR 10,000 per month</b> into an index equity fund "
            "generating an expected return of <b><i>R</i> = 12.00% per annum</b> for tenure <b><i>t</i> = 15 years</b> (<i>N</i> = 180 months). "
            "Calculate total principal invested, final maturity corpus, and total compound wealth created.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Parameter Normalization):</b><br/>"
            "&nbsp;&nbsp;&bull; Monthly contribution: <i>C</i> = INR 10,000<br/>"
            "&nbsp;&nbsp;&bull; Periodic rate: <i>r</i><sub><i>m</i></sub> = 0.12 / 12 = 0.0100 (1.00% per month)<br/>"
            "&nbsp;&nbsp;&bull; Total periods: <i>N</i> = 15 &times; 12 = 180 months.<br/><br/>"
            "<b>Step 2 (Geometric Growth Multiplier):</b><br/>"
            "&nbsp;&nbsp;&bull; Base factor: 1 + <i>r</i><sub><i>m</i></sub> = 1.0100<br/>"
            "&nbsp;&nbsp;&bull; Compound term: (1.01)<sup>180</sup> &approx; 5.99580198<br/>"
            "&nbsp;&nbsp;&bull; Bracket term: (5.99580198 &minus; 1) / 0.01 = 4.99580198 / 0.01 = 499.580198<br/><br/>"
            "<b>Step 3 (Terminal Future Value Calculation):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>FV</i><sub>SIP</sub> = 10,000 &times; 1.01 &times; 499.580198 = 10,100 &times; 499.580198<br/>"
            "&nbsp;&nbsp;&bull; <b>Terminal Corpus:</b> <i>FV</i><sub>SIP</sub> = <b>INR 5,045,760.00</b>.<br/><br/>"
            "<b>Step 4 (Wealth Decomposition):</b><br/>"
            "&nbsp;&nbsp;&bull; Cumulative Principal Contributed: 10,000 &times; 180 = <b>INR 1,800,000.00</b>.<br/>"
            "&nbsp;&nbsp;&bull; Net Compound Wealth Generated: 5,045,760.00 &minus; 1,800,000 = <b>INR 3,245,760.00</b>.<br/>"
            "&nbsp;&nbsp;&bull; <i>Analytical Insight:</i> Pure compound interest accounts for <b>64.33%</b> of the terminal portfolio, "
            "substantiating the exponential dominance of multi-decade systematic accumulation.",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 3: WORKED EXAMPLE 7.2 ====================
    # Example 7.2 Card
    ex2_content = [
        Paragraph("<b>Example 7.2: Step-Up SIP (Annual Contribution Escalation)</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> To reflect annual salary increments, an investor starts with <b><i>C</i><sub>1</sub> = INR 10,000 per month</b> "
            "in Year 1, and steps up the monthly contribution by <b>INR 2,000 each subsequent year</b> (+20% in Year 2, etc.) "
            "over a 3-year horizon at nominal return <b><i>R</i> = 12.00%</b> (<i>r</i><sub><i>m</i></sub> = 0.01). "
            "Compute the terminal corpus and compare against a flat SIP.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Decomposition into 12-Month Block Annuities):</b><br/>"
            "&nbsp;&nbsp;Terminal horizon <i>t</i> = 36 months. 12-month compounding factor: <i>F</i><sub>12</sub> = 1.01 &times; [ ((1.01)<sup>12</sup> &minus; 1) / 0.01 ] = 1.01 &times; 12.6825 = <b>12.80933</b>.<br/><br/>"
            "<b>Step 2 (Valuation of Year 1 Block — <i>C</i><sub>1</sub> = INR 10,000):</b><br/>"
            "&nbsp;&nbsp;&bull; Future value at month 12: 10,000 &times; 12.80933 = INR 128,093.30.<br/>"
            "&nbsp;&nbsp;&bull; Compounded for remaining 24 months to month 36: 128,093.30 &times; (1.01)<sup>24</sup> = 128,093.30 &times; 1.269735 = <b>INR 162,644.50</b>.<br/><br/>"
            "<b>Step 3 (Valuation of Year 2 Block — <i>C</i><sub>2</sub> = INR 12,000):</b><br/>"
            "&nbsp;&nbsp;&bull; Future value at month 24: 12,000 &times; 12.80933 = INR 153,711.96.<br/>"
            "&nbsp;&nbsp;&bull; Compounded for remaining 12 months to month 36: 153,711.96 &times; (1.01)<sup>12</sup> = 153,711.96 &times; 1.126825 = <b>INR 173,206.50</b>.<br/><br/>"
            "<b>Step 4 (Valuation of Year 3 Block — <i>C</i><sub>3</sub> = INR 14,000):</b><br/>"
            "&nbsp;&nbsp;&bull; Compounded directly to month 36: 14,000 &times; 12.80933 = <b>INR 179,330.62</b>.<br/><br/>"
            "<b>Step 5 (Total Terminal Corpus & Comparison):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>FV</i><sub>Step-Up</sub> = 162,644.50 + 173,206.50 + 179,330.62 = <b>INR 515,181.62</b>.<br/>"
            "&nbsp;&nbsp;&bull; Principal invested: (10,000 &times; 12) + (12,000 &times; 12) + (14,000 &times; 12) = <b>INR 432,000.00</b>.<br/>"
            "&nbsp;&nbsp;&bull; Standard Flat SIP Corpus (INR 10,000/mo for 36 mos): 10,000 &times; 1.01 &times; [ ((1.01)<sup>36</sup> &minus; 1)/0.01 ] = <b>INR 435,076.00</b>.<br/>"
            "&nbsp;&nbsp;&bull; <i>Gain:</i> Stepping up deposits generated <b>INR 80,105.62 (+18.4%)</b> in additional terminal corpus.",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 4: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("7.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the complete implementation from <code>models/investment_plans.py</code>, "
        "supporting standard annuity-due SIP and step-up annual contribution acceleration:",
        styles['Body']
    ))

    code_raw = (
        "def calculate_sip_future_value(monthly_contribution: float, annual_rate: float, tenure_years: float) -> float:\n"
        "    \"\"\"\n"
        "    Computes annuity-due SIP future value: FV = C * (1+r_m) * [((1+r_m)^N - 1) / r_m].\n"
        "    \"\"\"\n"
        "    if monthly_contribution <= 0.0 or annual_rate < 0.0 or tenure_years <= 0.0:\n"
        "        raise ValueError(\"SIP parameters must be non-negative.\")\n"
        "    if annual_rate == 0.0:\n"
        "        return float(monthly_contribution * tenure_years * 12.0)\n"
        "    monthly_rate = annual_rate / 12.0\n"
        "    total_months = int(round(tenure_years * 12.0))\n"
        "    growth_factor = (1.0 + monthly_rate) ** total_months\n"
        "    return float(monthly_contribution * (1.0 + monthly_rate) * ((growth_factor - 1.0) / monthly_rate))\n\n\n"
        "def calculate_step_up_sip(\n"
        "    initial_monthly: float, annual_step_up: float, annual_rate: float, tenure_years: float\n"
        ") -> float:\n"
        "    \"\"\"Computes future value of annually increasing SIP contributions.\"\"\"\n"
        "    monthly_rate = annual_rate / 12.0\n"
        "    total_months = int(round(tenure_years * 12.0))\n"
        "    accumulated_wealth = 0.0\n"
        "    for month in range(1, total_months + 1):\n"
        "        year_index = (month - 1) // 12\n"
        "        current_contribution = initial_monthly + (year_index * annual_step_up)\n"
        "        months_remaining = total_months - month + 1\n"
        "        accumulated_wealth += current_contribution * ((1.0 + monthly_rate) ** months_remaining)\n"
        "    return float(accumulated_wealth)\n"
    )
    story.append(make_code_card(code_raw, title="models/investment_plans.py — SIP Accumulation Engine"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("7.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Formula</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>Annuity Class</b>", styles['Body']), Paragraph("Annuity-Due", styles['Body']), Paragraph("Deposits executed at the beginning of each compounding period", styles['Body'])],
        [Paragraph("<b>Accumulation Multiplier</b>", styles['Body']), Paragraph("<i>s̈</i><sub><i>N</i>|<i>r</i></sub> = (1 + <i>r</i><sub><i>m</i></sub>) [ ((1+<i>r</i><sub><i>m</i></sub>)<sup><i>N</i></sup> &minus; 1) / <i>r</i><sub><i>m</i></sub> ]", styles['Body']), Paragraph("Standard actuarial annuity-due future value symbol", styles['Body'])],
        [Paragraph("<b>Zero-Rate Limit</b>", styles['Body']), Paragraph("lim<sub><i>r</i>&rarr;0</sub> <i>FV</i> = <i>C</i> &middot; <i>N</i>", styles['Body']), Paragraph("Uncompounded cumulative sum of raw deposits", styles['Body'])],
        [Paragraph("<b>Convexity / Velocity</b>", styles['Body']), Paragraph("&part;<sup>2</sup>(<i>FV</i>)/&part;<i>N</i><sup>2</sup> &gt; 0", styles['Body']), Paragraph("Accelerating terminal wealth slope during final years", styles['Body'])],
        [Paragraph("<b>Step-Up Sensitivity</b>", styles['Body']), Paragraph("&part;(<i>FV</i>)/&part;<i>g</i> &gt; 0", styles['Body']), Paragraph("Supercharges capital base before compounding phase transitions", styles['Body'])]
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
    out_file = os.path.join(out_dir, "07_Systematic_Investment_Plan_SIP.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
