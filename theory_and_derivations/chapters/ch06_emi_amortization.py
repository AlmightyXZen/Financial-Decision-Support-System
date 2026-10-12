"""
Chapter 06: Equated Monthly Installment (EMI) & Loan Amortization.
Textbook chapter with geometric progression derivation, balance recurrence relations,
20-year home loan breakdown, prepayment acceleration analysis, and Python code.
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
    story.append(Paragraph("CHAPTER 6", styles['ChapterLabel']))
    story.append(Paragraph("Equated Monthly Installment (EMI) & Amortization", styles['ChapterTitle']))
    story.append(Paragraph(
        "Annuity-Immediate Valuation, Finite Geometric Series Proofs, Balance Recurrence Relations, and Prepayment Mechanics",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=7))

    story.append(Paragraph("6.1 Definition & Axioms of Debt Amortization", styles['H1']))
    story.append(Paragraph(
        "An Equated Monthly Installment (EMI) is a fixed periodic payment made by a borrower to a lender to fully "
        "amortize an outstanding debt over a specified term. Each installment is partitioned into two distinct components: "
        "an <b>interest payment</b> covering the cost of unpaid capital, and a <b>principal repayment</b> that reduces the balance.",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 6.1 (The Closed-Form EMI Equation)</b>", styles['DefHeader']),
        Paragraph(
            "Let loan principal be <i>P</i> &gt; 0, nominal annual interest rate be <i>r</i> &ge; 0, "
            "and total tenure be <i>t</i> years. The periodic monthly interest rate is <i>r</i><sub><i>m</i></sub> = <i>r</i> / 12, "
            "and total payment count is <i>N</i> = 12 &middot; <i>t</i>.<br/>"
            "The constant monthly installment <i>E</i> satisfying full amortization is:",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("<i>E</i> = <i>P</i> &middot; [ <i>r</i><sub><i>m</i></sub> (1 + <i>r</i><sub><i>m</i></sub>)<sup><i>N</i></sup> ] / [ (1 + <i>r</i><sub><i>m</i></sub>)<sup><i>N</i></sup> &minus; 1 ]", styles['Equation']),
        Spacer(1, 2),
        Paragraph("When <i>r</i><sub><i>m</i></sub> = 0, the equation reduces by L'H&ocirc;pital's Rule to <i>E</i> = <i>P</i> / <i>N</i>.", styles['EquationSub'])
    ]
    story.append(make_card(def_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 5))

    story.append(Paragraph("6.2 First-Principles Derivation via Geometric Series", styles['H1']))
    story.append(Paragraph(
        "<b>No-Arbitrage Equilibrium Proof:</b><br/>"
        "By the Principle of Temporal Financial Equivalence, the borrowed principal <i>P</i> must equal the sum "
        "of the present values of all future <i>N</i> monthly installments discounted at periodic rate <i>r</i><sub><i>m</i></sub>:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <i>P</i> = &sum;<sub><i>k</i>=1</sub><sup><i>N</i></sup> [ <i>E</i> / (1 + <i>r</i><sub><i>m</i></sub>)<sup><i>k</i></sup> ] "
        "= <i>E</i> &sum;<sub><i>k</i>=1</sub><sup><i>N</i></sup> <i>v</i><sup><i>k</i></sup>, &nbsp; where <i>v</i> = (1 + <i>r</i><sub><i>m</i></sub>)<sup>&minus;1</sup>.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; The summation is a finite geometric series with initial term <i>a</i><sub>1</sub> = <i>v</i>, ratio <i>q</i> = <i>v</i>, and <i>N</i> terms:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&sum;<sub><i>k</i>=1</sub><sup><i>N</i></sup> <i>v</i><sup><i>k</i></sup> = <i>v</i> [ (1 &minus; <i>v</i><sup><i>N</i></sup>) / (1 &minus; <i>v</i>) ].<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Substituting <i>v</i> = 1 / (1 + <i>r</i><sub><i>m</i></sub>):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1 &minus; <i>v</i> = 1 &minus; 1/(1 + <i>r</i><sub><i>m</i></sub>) = <i>r</i><sub><i>m</i></sub> / (1 + <i>r</i><sub><i>m</i></sub>) = <i>r</i><sub><i>m</i></sub> &middot; <i>v</i>.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Therefore: &sum;<sub><i>k</i>=1</sub><sup><i>N</i></sup> <i>v</i><sup><i>k</i></sup> = <i>v</i> [ (1 &minus; (1+<i>r</i><sub><i>m</i></sub>)<sup>&minus;<i>N</i></sup>) / (<i>r</i><sub><i>m</i></sub> &middot; <i>v</i>) ] "
        "= [ 1 &minus; (1 + <i>r</i><sub><i>m</i></sub>)<sup>&minus;<i>N</i></sup> ] / <i>r</i><sub><i>m</i></sub>.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; Equating <i>P</i> = <i>E</i> &middot; [ (1 &minus; (1+<i>r</i><sub><i>m</i></sub>)<sup>&minus;<i>N</i></sup>) / <i>r</i><sub><i>m</i></sub> ] and multiplying numerator and denominator "
        "by (1+<i>r</i><sub><i>m</i></sub>)<sup><i>N</i></sup> yields Definition 6.1. &#9632;",
        styles['Body']
    ))

    # Recurrence Relation Card
    th_content = [
        Paragraph("<b>Theorem 6.1 (Amortization Balance Recurrence & Principal Growth)</b>", styles['DefHeader']),
        Paragraph(
            "For payment period <i>k</i> &in; {1, 2, ..., <i>N</i>} with opening balance <i>B</i><sub><i>k</i>&minus;1</sub> (where <i>B</i><sub>0</sub> = <i>P</i>):<br/>"
            "&nbsp;&nbsp;&bull;&nbsp; <b>Interest Component:</b> <i>I</i><sub><i>k</i></sub> = <i>B</i><sub><i>k</i>&minus;1</sub> &middot; <i>r</i><sub><i>m</i></sub><br/>"
            "&nbsp;&nbsp;&bull;&nbsp; <b>Principal Component:</b> <i>P</i><sub><i>k</i></sub> = <i>E</i> &minus; <i>I</i><sub><i>k</i></sub><br/>"
            "&nbsp;&nbsp;&bull;&nbsp; <b>Closing Balance:</b> <i>B</i><sub><i>k</i></sub> = <i>B</i><sub><i>k</i>&minus;1</sub> &minus; <i>P</i><sub><i>k</i></sub> = <i>B</i><sub><i>k</i>&minus;1</sub>(1 + <i>r</i><sub><i>m</i></sub>) &minus; <i>E</i>.<br/>"
            "<font size=9.5><b>Principal Progression Property:</b> <i>P</i><sub><i>k</i></sub> = <i>P</i><sub>1</sub> &middot; (1 + <i>r</i><sub><i>m</i></sub>)<sup><i>k</i>&minus;1</sup></font>",
            styles['Body']
        ),
        Paragraph(
            "<i>Analytical Consequence:</i> Principal repayment grows exponentially over time at rate <i>r</i><sub><i>m</i></sub>, "
            "meaning early installments consist overwhelmingly of interest, while terminal installments consist almost entirely of principal.",
            styles['Body']
        )
    ]
    story.append(make_card(th_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLE 6.1 ====================
    story.append(Paragraph("6.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: full amortization breakdown of a 20-year mortgage, "
        "and prepayment acceleration savings analysis.",
        styles['Body']
    ))

    # Example 6.1 Card
    ex1_content = [
        Paragraph("<b>Example 6.1: 20-Year Home Loan with 3-Month Amortization Trace</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> A borrower secures a residential mortgage of <b><i>P</i> = INR 5,000,000</b> at an annual nominal rate "
            "<b><i>R</i> = 8.50%</b> for tenure <b><i>t</i> = 20 years</b> (<i>N</i> = 240 months). Calculate the exact monthly EMI, "
            "lifetime total interest liability, and the first 3 monthly amortization splits.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Parameter Normalization & Monthly Rate):</b><br/>"
            "&nbsp;&nbsp;&bull; Monthly rate: <i>r</i><sub><i>m</i></sub> = 0.085 / 12 = 0.007083333...<br/>"
            "&nbsp;&nbsp;&bull; Total payment count: <i>N</i> = 20 &times; 12 = 240 months.<br/>"
            "&nbsp;&nbsp;&bull; Growth factor: (1 + <i>r</i><sub><i>m</i></sub>)<sup>240</sup> = (1.007083333)<sup>240</sup> &approx; 5.4344755.<br/><br/>"
            "<b>Step 2 (Closed-Form EMI Calculation):</b><br/>"
            "&nbsp;&nbsp;&bull; Numerator: 5,000,000 &times; 0.007083333 &times; 5.4344755 = 192,471.01<br/>"
            "&nbsp;&nbsp;&bull; Denominator: 5.4344755 &minus; 1 = 4.4344755<br/>"
            "&nbsp;&nbsp;&bull; <b>EMI:</b> <i>E</i> = 192,471.01 / 4.4344755 = <b>INR 43,407.84</b> per month.<br/><br/>"
            "<b>Step 3 (Lifetime Interest Obligation):</b><br/>"
            "&nbsp;&nbsp;&bull; Total Outflow: 43,407.84 &times; 240 = <b>INR 10,417,881.60</b>.<br/>"
            "&nbsp;&nbsp;&bull; Total Interest: 10,417,881.60 &minus; 5,000,000 = <b>INR 5,417,881.60</b> (exceeds borrowed capital!).<br/><br/>"
            "<b>Step 4 (First 3-Month Amortization Schedule Trace):</b><br/>"
            "&nbsp;&nbsp;&bull; <b>Month 1:</b> Interest <i>I</i><sub>1</sub> = 5,000,000 &times; 0.00708333 = INR 35,416.67.<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Principal <i>P</i><sub>1</sub> = 43,407.84 &minus; 35,416.67 = <b>INR 7,991.17</b>. &nbsp; Balance <i>B</i><sub>1</sub> = <b>INR 4,992,008.83</b>.<br/>"
            "&nbsp;&nbsp;&bull; <b>Month 2:</b> Interest <i>I</i><sub>2</sub> = 4,992,008.83 &times; 0.00708333 = INR 35,360.06.<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Principal <i>P</i><sub>2</sub> = 43,407.84 &minus; 35,360.06 = <b>INR 8,047.78</b>. &nbsp; Balance <i>B</i><sub>2</sub> = <b>INR 4,983,961.05</b>.<br/>"
            "&nbsp;&nbsp;&bull; <b>Month 3:</b> Interest <i>I</i><sub>3</sub> = 4,983,961.05 &times; 0.00708333 = INR 35,303.06.<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Principal <i>P</i><sub>3</sub> = 43,407.84 &minus; 35,303.06 = <b>INR 8,104.78</b>. &nbsp; Balance <i>B</i><sub>3</sub> = <b>INR 4,975,856.27</b>.",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 3: WORKED EXAMPLE 6.2 ====================
    # Example 6.2 Card
    ex2_content = [
        Paragraph("<b>Example 6.2: Prepayment Acceleration & Lifetime Interest Savings</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> On the mortgage in Example 6.1, the borrower executes a lump-sum principal prepayment "
            "of <b>INR 500,000 at the end of Year 1 (Month 12)</b>. If the EMI remains unchanged at <b>INR 43,407.84</b>, "
            "calculate the revised remaining tenure and total interest saved.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Balance at Month 12 Before Prepayment):</b><br/>"
            "&nbsp;&nbsp;Balance after 12 payments: <i>B</i><sub>12</sub> = <i>P</i>(1+<i>r</i><sub><i>m</i></sub>)<sup>12</sup> &minus; <i>E</i> [ ((1+<i>r</i><sub><i>m</i></sub>)<sup>12</sup> &minus; 1) / <i>r</i><sub><i>m</i></sub> ].<br/>"
            "&nbsp;&nbsp;&bull; Compound principal: 5,000,000 &times; (1.00708333)<sup>12</sup> = 5,000,000 &times; 1.0883909 = INR 5,441,954.50.<br/>"
            "&nbsp;&nbsp;&bull; Future value of 12 EMIs: 43,407.84 &times; (0.0883909 / 0.00708333) = 43,407.84 &times; 12.4787 = INR 541,673.50.<br/>"
            "&nbsp;&nbsp;&bull; Balance <i>B</i><sub>12</sub> = 5,441,954.50 &minus; 541,673.50 = <b>INR 4,900,281.00</b>.<br/><br/>"
            "<b>Step 2 (Adjusting Balance Post-Prepayment):</b><br/>"
            "&nbsp;&nbsp;&bull; Revised Balance: <i>B</i>'<sub>12</sub> = 4,900,281.00 &minus; 500,000 = <b>INR 4,400,281.00</b>.<br/><br/>"
            "<b>Step 3 (Solving for Revised Remaining Tenure <i>N</i>'):</b><br/>"
            "&nbsp;&nbsp;From Definition 6.1: 1 &minus; (1 + <i>r</i><sub><i>m</i></sub>)<sup>&minus;<i>N</i>'</sup> = (<i>B</i>'<sub>12</sub> &middot; <i>r</i><sub><i>m</i></sub>) / <i>E</i>.<br/>"
            "&nbsp;&nbsp;&bull; (4,400,281.00 &times; 0.007083333) / 43,407.84 = 31,168.66 / 43,407.84 = 0.718042.<br/>"
            "&nbsp;&nbsp;&bull; (1.007083333)<sup>&minus;<i>N</i>'</sup> = 1 &minus; 0.718042 = 0.281958.<br/>"
            "&nbsp;&nbsp;&bull; &minus;<i>N</i>' &middot; ln(1.007083333) = ln(0.281958) &implies; &minus;<i>N</i>' &times; 0.0070584 = &minus;1.265997.<br/>"
            "&nbsp;&nbsp;&bull; <b>Revised Remaining Months:</b> <i>N</i>' = 1.265997 / 0.0070584 &approx; <b>179.36 months</b> (&approx; 180 months / 15 years).<br/><br/>"
            "<b>Step 4 (Total Interest Savings Analysis):</b><br/>"
            "&nbsp;&nbsp;&bull; Original remaining payments: 240 &minus; 12 = 228 months.<br/>"
            "&nbsp;&nbsp;&bull; Months saved: 228 &minus; 180 = <b>48 months (4 full years eliminated!)</b>.<br/>"
            "&nbsp;&nbsp;&bull; Total Outflow Saved: 48 &times; 43,407.84 = <b>INR 2,083,576.32</b>.<br/>"
            "&nbsp;&nbsp;&bull; Net Interest Saved: 2,083,576.32 &minus; 500,000 prepayment = <b>INR 1,583,576.32 pure savings</b>.",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 4: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("6.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the complete implementation from <code>models/loans_and_credit.py</code>, "
        "featuring closed-form EMI calculation and full amortization schedule generation:",
        styles['Body']
    ))

    code_raw = (
        "from typing import List, Dict\n\n"
        "def calculate_emi(principal: float, annual_rate: float, tenure_years: float) -> float:\n"
        "    \"\"\"Computes closed-form EMI: E = P * [r_m * (1+r_m)^N] / [(1+r_m)^N - 1].\"\"\"\n"
        "    if principal <= 0.0 or annual_rate < 0.0 or tenure_years <= 0.0:\n"
        "        raise ValueError(\"Principal and tenure must be strictly positive.\")\n"
        "    if annual_rate == 0.0:\n"
        "        return float(principal / (tenure_years * 12.0))\n"
        "    monthly_rate = annual_rate / 12.0\n"
        "    total_months = int(round(tenure_years * 12.0))\n"
        "    growth_factor = (1.0 + monthly_rate) ** total_months\n"
        "    return float(principal * (monthly_rate * growth_factor) / (growth_factor - 1.0))\n\n\n"
        "def generate_amortization_schedule(principal: float, annual_rate: float, tenure_years: float) -> List[Dict]:\n"
        "    \"\"\"Generates detailed monthly amortization schedule with balance recurrence.\"\"\"\n"
        "    emi = calculate_emi(principal, annual_rate, tenure_years)\n"
        "    monthly_rate = annual_rate / 12.0\n"
        "    balance = principal\n"
        "    schedule = []\n"
        "    total_months = int(round(tenure_years * 12.0))\n"
        "    for month in range(1, total_months + 1):\n"
        "        interest_paid = balance * monthly_rate\n"
        "        principal_paid = emi - interest_paid\n"
        "        balance -= principal_paid\n"
        "        schedule.append({'month': month, 'interest': interest_paid, 'principal': principal_paid, 'balance': max(0.0, balance)})\n"
        "    return schedule\n"
    )
    story.append(make_code_card(code_raw, title="models/loans_and_credit.py — Loan Amortization Engine"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("6.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Formula</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>Annuity Class</b>", styles['Body']), Paragraph("Annuity-Immediate", styles['Body']), Paragraph("Cash flows transacted at the end of each payment period", styles['Body'])],
        [Paragraph("<b>Principal Component</b>", styles['Body']), Paragraph("<i>P</i><sub><i>k</i></sub> = <i>P</i><sub>1</sub>(1 + <i>r</i><sub><i>m</i></sub>)<sup><i>k</i>&minus;1</sup>", styles['Body']), Paragraph("Principal repayment accelerates exponentially over tenure", styles['Body'])],
        [Paragraph("<b>Interest Component</b>", styles['Body']), Paragraph("<i>I</i><sub><i>k</i></sub> = <i>E</i> &minus; <i>P</i><sub><i>k</i></sub>", styles['Body']), Paragraph("Interest burden declines monotonically to zero at terminal month", styles['Body'])],
        [Paragraph("<b>Zero-Rate Limit</b>", styles['Body']), Paragraph("lim<sub><i>r</i>&rarr;0</sub> <i>E</i> = <i>P</i> / <i>N</i>", styles['Body']), Paragraph("Smooth algebraic recovery of interest-free straight amortization", styles['Body'])],
        [Paragraph("<b>Prepayment Elasticity</b>", styles['Body']), Paragraph("&part;<i>N</i>/&part;<i>B</i> &gt; 0", styles['Body']), Paragraph("Early balance reduction yields superlinear tenure compression", styles['Body'])]
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
    out_file = os.path.join(out_dir, "06_Equated_Monthly_Installment_EMI.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
