"""
Chapter 09: Net Present Value (NPV) & Capital Budgeting.
Textbook chapter on discounted cash flow sums, hurdle rate sensitivity,
convexity theorems, industrial project evaluation, Fisher intersection, and Python code.
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
    story.append(Paragraph("CHAPTER 9", styles['ChapterLabel']))
    story.append(Paragraph("Net Present Value (NPV) & Capital Budgeting", styles['ChapterTitle']))
    story.append(Paragraph(
        "Discounted Cash Flow Sums, Hurdle Rate Sensitivity, Profile Convexity, and Value Maximization Criteria",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=7))

    story.append(Paragraph("9.1 Definition & The Discounted Cash Flow Criterion", styles['H1']))
    story.append(Paragraph(
        "Net Present Value (NPV) is the gold standard decision-support metric in capital allocation and financial engineering. "
        "It evaluates an investment opportunity by discounting all future periodic cash inflows and outflows back to time zero "
        "at an appropriate risk-adjusted cost of capital (hurdle rate), then subtracting the initial capital expenditure.",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 9.1 (The Net Present Value Equation)</b>", styles['DefHeader']),
        Paragraph(
            "Let {<i>C</i><sub>0</sub>, <i>C</i><sub>1</sub>, ..., <i>C</i><sub><i>T</i></sub>} represent a finite series of periodic cash flows "
            "occurring at integer times <i>t</i> &in; {0, 1, ..., <i>T</i>}, where initial outlay <i>C</i><sub>0</sub> &lt; 0. "
            "Let <i>r</i> &ge; 0 denote the hurdle discount rate.<br/>"
            "The <b>Net Present Value</b> of the project is defined by:",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("NPV(<i>r</i>) = &sum;<sub><i>t</i>=0</sub><sup><i>T</i></sup> [ <i>C</i><sub><i>t</i></sub> / (1 + <i>r</i>)<sup><i>t</i></sup> ] = <i>C</i><sub>0</sub> + &sum;<sub><i>t</i>=1</sub><sup><i>T</i></sup> [ <i>C</i><sub><i>t</i></sub> / (1 + <i>r</i>)<sup><i>t</i></sup> ]", styles['Equation']),
        Spacer(1, 2),
        Paragraph("Decision Criteria: NPV(<i>r</i>) &gt; 0 &rArr; Accept (Value Creation) &nbsp;|&nbsp; NPV(<i>r</i>) &lt; 0 &rArr; Reject (Value Destruction)", styles['EquationSub'])
    ]
    story.append(make_card(def_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 5))

    story.append(Paragraph("9.2 Calculus of the NPV Profile: Slope & Convexity", styles['H1']))
    story.append(Paragraph(
        "<b>Derivative Analysis:</b> Viewing NPV as a continuous real function of the discount rate <i>r</i> &in; (&minus;1, &infin;):<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <b>First Derivative (Rate Sensitivity):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>d</i>(NPV)/<i>dr</i> = &minus;&sum;<sub><i>t</i>=1</sub><sup><i>T</i></sup> [ <i>t</i> &middot; <i>C</i><sub><i>t</i></sub> / (1 + <i>r</i>)<sup><i>t</i>+1</sup> ].<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;For conventional projects (where all subsequent cash flows <i>C</i><sub><i>t</i></sub> &gt; 0), "
        "<i>d</i>(NPV)/<i>dr</i> &lt; 0 strictly, confirming NPV is a monotonically decreasing function of rate <i>r</i>.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <b>Second Derivative (Convexity):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>d</i><sup>2</sup>(NPV)/<i>dr</i><sup>2</sup> = &sum;<sub><i>t</i>=1</sub><sup><i>T</i></sup> [ <i>t</i>(<i>t</i>+1) &middot; <i>C</i><sub><i>t</i></sub> / (1 + <i>r</i>)<sup><i>t</i>+2</sup> ] &gt; 0.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Strict positive second derivative proves the NPV profile is <b>strictly convex</b> across all positive rates.",
        styles['Body']
    ))

    # Convexity Card
    th_content = [
        Paragraph("<b>Theorem 9.1 (NPV Reinvestment Rate Principle)</b>", styles['DefHeader']),
        Paragraph(
            "The mathematical formulation of NPV implicitly assumes that all intermediate positive cash inflows "
            "<i>C</i><sub>1</sub>, <i>C</i><sub>2</sub>, ..., <i>C</i><sub><i>T</i>&minus;1</sub> are reinvested across time "
            "at the exact hurdle rate <i>r</i>, not at the project's internal yield rate.<br/>"
            "<font size=10><b><i>FV</i><sub>terminal</sub> = NPV(<i>r</i>) &middot; (1 + <i>r</i>)<sup><i>T</i></sup> &minus; <i>C</i><sub>0</sub>(1 + <i>r</i>)<sup><i>T</i></sup></b></font>",
            styles['Body']
        ),
        Paragraph(
            "<i>Significance:</i> This reinvestment assumption makes NPV economically superior to naive yield metrics (such as IRR) "
            "when ranking mutually exclusive investment proposals.",
            styles['Body']
        )
    ]
    story.append(make_card(th_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLE 9.1 ====================
    story.append(Paragraph("9.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: evaluating an industrial asset capital acquisition, "
        "and resolving the Fisher intersection rate between competing projects.",
        styles['Body']
    ))

    # Example 9.1 Card
    ex1_content = [
        Paragraph("<b>Example 9.1: Industrial Infrastructure Asset Evaluation</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> An industrial firm evaluates acquiring automated manufacturing equipment. "
            "The initial expenditure is <b><i>C</i><sub>0</sub> = &minus;INR 1,000,000</b>. The asset generates five annual cash inflows: "
            "<b><i>C</i><sub>1</sub> = INR 250,000</b>, <b><i>C</i><sub>2</sub> = INR 350,000</b>, <b><i>C</i><sub>3</sub> = INR 350,000</b>, "
            "<b><i>C</i><sub>4</sub> = INR 300,000</b>, and <b><i>C</i><sub>5</sub> = INR 200,000</b>. "
            "The firm's cost of capital is <b><i>R</i> = 10.00% per annum</b>. Calculate the project NPV and state the investment verdict.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Discount Inflows at <i>r</i> = 0.10):</b><br/>"
            "&nbsp;&nbsp;&bull; Year 1: <i>PV</i><sub>1</sub> = 250,000 / (1.10)<sup>1</sup> = 250,000 / 1.10000 = <b>INR 227,272.73</b><br/>"
            "&nbsp;&nbsp;&bull; Year 2: <i>PV</i><sub>2</sub> = 350,000 / (1.10)<sup>2</sup> = 350,000 / 1.21000 = <b>INR 289,256.20</b><br/>"
            "&nbsp;&nbsp;&bull; Year 3: <i>PV</i><sub>3</sub> = 350,000 / (1.10)<sup>3</sup> = 350,000 / 1.33100 = <b>INR 262,960.18</b><br/>"
            "&nbsp;&nbsp;&bull; Year 4: <i>PV</i><sub>4</sub> = 300,000 / (1.10)<sup>4</sup> = 300,000 / 1.46410 = <b>INR 204,904.04</b><br/>"
            "&nbsp;&nbsp;&bull; Year 5: <i>PV</i><sub>5</sub> = 200,000 / (1.10)<sup>5</sup> = 200,000 / 1.61051 = <b>INR 124,184.26</b><br/><br/>"
            "<b>Step 2 (Sum Inflows & Subtract Outlay):</b><br/>"
            "&nbsp;&nbsp;&bull; Total PV of Inflows: 227,272.73 + 289,256.20 + 262,960.18 + 204,904.04 + 124,184.26 = <b>INR 1,108,577.41</b>.<br/>"
            "&nbsp;&nbsp;&bull; Net Present Value: NPV = &minus;1,000,000 + 1,108,577.41 = <b>+INR 108,577.41</b>.<br/><br/>"
            "<b>Step 3 (Financial Decision & Economic Interpretation):</b><br/>"
            "&nbsp;&nbsp;&bull; Verdict: <b>ACCEPT THE INVESTMENT</b>.<br/>"
            "&nbsp;&nbsp;&bull; <i>Economic Meaning:</i> The project recovers all initial capital, covers the full 10% annual cost of capital, "
            "and generates an incremental <b>INR 108,577.41</b> in pure economic profit today for the enterprise.",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 3: WORKED EXAMPLE 9.2 ====================
    # Example 9.2 Card
    ex2_content = [
        Paragraph("<b>Example 9.2: Mutually Exclusive Projects & The Fisher Intersection</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> Two competing investments require identical initial outlays of <b><i>C</i><sub>0</sub> = &minus;INR 100,000</b>:<br/>"
            "&nbsp;&nbsp;&bull; <b>Project Alpha (Short-term):</b> Inflows: <i>C</i><sub>1</sub> = INR 70,000, <i>C</i><sub>2</sub> = INR 60,000.<br/>"
            "&nbsp;&nbsp;&bull; <b>Project Beta (Long-term):</b> Inflows: <i>C</i><sub>1</sub> = INR 20,000, <i>C</i><sub>2</sub> = INR 120,000.<br/>"
            "Determine the <b>Fisher Intersection Rate <i>r</i>*</b> where both projects have identical NPVs, and state which project "
            "dominates for cost of capital below vs above <i>r</i>*.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Formulate Differential Cash Flow Stream &Delta;<i>C</i>):</b><br/>"
            "&nbsp;&nbsp;At the Fisher rate <i>r</i>*: NPV<sub>&alpha;</sub>(<i>r</i>*) = NPV<sub>&beta;</sub>(<i>r</i>*) &rArr; NPV(&Delta;<i>C</i>) = 0.<br/>"
            "&nbsp;&nbsp;&bull; &Delta;<i>C</i><sub>0</sub> = &minus;100,000 &minus; (&minus;100,000) = 0.<br/>"
            "&nbsp;&nbsp;&bull; &Delta;<i>C</i><sub>1</sub> = 70,000 &minus; 20,000 = +50,000.<br/>"
            "&nbsp;&nbsp;&bull; &Delta;<i>C</i><sub>2</sub> = 60,000 &minus; 120,000 = &minus;60,000.<br/><br/>"
            "<b>Step 2 (Solve the Root Equation):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;50,000 / (1 + <i>r</i>*) &minus; 60,000 / (1 + <i>r</i>*)<sup>2</sup> = 0.<br/>"
            "&nbsp;&nbsp;Multiplying by (1 + <i>r</i>*)<sup>2</sup>:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;50,000(1 + <i>r</i>*) &minus; 60,000 = 0 &rArr; 50,000(1 + <i>r</i>*) = 60,000<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;1 + <i>r</i>* = 60,000 / 50,000 = 1.2000.<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<b>Fisher Intersection Rate:</b> <i>r</i>* = 1.2000 &minus; 1 = <b>0.2000 (20.00%)</b>.<br/><br/>"
            "<b>Step 3 (Dominance Decision Matrix):</b><br/>"
            "&nbsp;&nbsp;&bull; For <b><i>r</i> &lt; 20%</b> (e.g. 10%): Project Beta dominates (e.g., at 10%: NPV<sub>&beta;</sub> = INR 17,355 vs NPV<sub>&alpha;</sub> = INR 13,223).<br/>"
            "&nbsp;&nbsp;&bull; For <b><i>r</i> &gt; 20%</b> (e.g. 25%): Project Alpha dominates (e.g., at 25%: NPV<sub>&alpha;</sub> = &minus;INR 5,600 vs NPV<sub>&beta;</sub> = &minus;INR 7,200).<br/>"
            "&nbsp;&nbsp;&bull; <i>Takeaway:</i> At low discount rates, back-loaded cash flows (Beta) have massive value. "
            "As discount rates rise, front-loaded early cash flows (Alpha) suffer far less discount penalty.",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 4: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("9.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the complete implementation from <code>models/capital_budgeting.py</code>, "
        "featuring multi-period discounted cash flow summation and sensitivity profiling:",
        styles['Body']
    ))

    code_raw = (
        "from typing import List, Tuple\n\n"
        "def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:\n"
        "    \"\"\"\n"
        "    Computes Net Present Value: NPV(r) = sum(C_t / (1 + r) ** t).\n"
        "    \"\"\"\n"
        "    if discount_rate <= -1.0:\n"
        "        raise ValueError(\"Discount rate must be strictly greater than -100%.\")\n"
        "    return float(sum(cf / ((1.0 + discount_rate) ** t) for t, cf in enumerate(cash_flows)))\n\n\n"
        "def npv_profile(\n"
        "    cash_flows: List[float], min_rate: float = 0.0, max_rate: float = 0.30, steps: int = 31\n"
        ") -> List[Tuple[float, float]]:\n"
        "    \"\"\"Generates (rate, npv) sensitivity points for profile curve visualization.\"\"\"\n"
        "    step_size = (max_rate - min_rate) / (steps - 1)\n"
        "    profile = []\n"
        "    for i in range(steps):\n"
        "        r = min_rate + (i * step_size)\n"
        "        profile.append((r, calculate_npv(cash_flows, r)))\n"
        "    return profile\n"
    )
    story.append(make_code_card(code_raw, title="models/capital_budgeting.py — Net Present Value Engine"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("9.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Formula</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>DCF Operator</b>", styles['Body']), Paragraph("NPV(<i>r</i>) = &sum; <i>C</i><sub><i>t</i></sub>(1+<i>r</i>)<sup>&minus;<i>t</i></sup>", styles['Body']), Paragraph("Linear functional mapping cash streams to present wealth", styles['Body'])],
        [Paragraph("<b>Rate Monotonicity</b>", styles['Body']), Paragraph("<i>d</i>(NPV)/<i>dr</i> &lt; 0", styles['Body']), Paragraph("Strictly decreasing profile for conventional project structures", styles['Body'])],
        [Paragraph("<b>Profile Convexity</b>", styles['Body']), Paragraph("<i>d</i><sup>2</sup>(NPV)/<i>dr</i><sup>2</sup> &gt; 0", styles['Body']), Paragraph("Guarantees uniqueness of roots for standard investment outflows", styles['Body'])],
        [Paragraph("<b>Reinvestment Axiom</b>", styles['Body']), Paragraph("Reinvestment at hurdle <i>r</i>", styles['Body']), Paragraph("Avoids unrealistic yield compounding assumptions of IRR", styles['Body'])],
        [Paragraph("<b>Fisher Intersection</b>", styles['Body']), Paragraph("NPV<sub><i>A</i></sub>(<i>r</i>*) = NPV<sub><i>B</i></sub>(<i>r</i>*)", styles['Body']), Paragraph("Threshold crossover rate for mutually exclusive projects", styles['Body'])]
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
    out_file = os.path.join(out_dir, "09_Net_Present_Value_NPV.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
