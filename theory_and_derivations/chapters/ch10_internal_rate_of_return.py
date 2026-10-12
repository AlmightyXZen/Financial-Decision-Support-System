"""
Chapter 10: Internal Rate of Return (IRR) & Numerical Analysis.
Textbook chapter on polynomial root-finding, the Abel-Ruffini theorem,
Newton-Raphson quadratic convergence, Bisection bracketing, Descartes' Rule of Signs, and Python code.
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

    # ==================== PAGE 1: THEORY & GALOIS / NUMERICAL FOUNDATIONS ====================
    story.append(Paragraph("CHAPTER 10", styles['ChapterLabel']))
    story.append(Paragraph("Internal Rate of Return & Numerical Analysis", styles['ChapterTitle']))
    story.append(Paragraph(
        "Polynomial Formulations, The Abel-Ruffini Theorem, Newton-Raphson Schemes, and Descartes' Rule of Signs",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=7))

    story.append(Paragraph("10.1 The IRR as a Polynomial Root-Finding Problem", styles['H1']))
    story.append(Paragraph(
        "The Internal Rate of Return (IRR) is the effective annualized yield rate that equates the Net Present Value "
        "of a multi-period investment stream to zero. Mathematically, it represents the real root <i>r</i>* of the non-linear equation:",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 10.1 (The Internal Rate of Return Equation)</b>", styles['DefHeader']),
        Paragraph(
            "Given cash flows {<i>C</i><sub>0</sub>, <i>C</i><sub>1</sub>, ..., <i>C</i><sub><i>T</i></sub>}, "
            "the Internal Rate of Return <i>r</i>* is the solution satisfying:",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("<i>f</i>(<i>r</i>) = NPV(<i>r</i>) = &sum;<sub><i>t</i>=0</sub><sup><i>T</i></sup> [ <i>C</i><sub><i>t</i></sub> / (1 + <i>r</i>)<sup><i>t</i></sup> ] = 0", styles['Equation']),
        Spacer(1, 2),
        Paragraph(
            "Substituting <i>x</i> = 1 + <i>r</i> transforms <i>f</i>(<i>r</i>) = 0 into a degree-<i>T</i> algebraic polynomial:<br/>"
            "<i>P</i>(<i>x</i>) = <i>C</i><sub>0</sub> <i>x</i><sup><i>T</i></sup> + <i>C</i><sub>1</sub> <i>x</i><sup><i>T</i>&minus;1</sup> + ... + <i>C</i><sub><i>T</i></sub> = 0.",
            styles['EquationSub']
        )
    ]
    story.append(make_card(def_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 5))

    story.append(Paragraph("10.2 Why Numerical Methods Are Mathematically Obligatory", styles['H1']))
    story.append(Paragraph(
        "<b>The Abel-Ruffini Impossibility Theorem:</b> In pure algebra, polynomials of degree <i>T</i> &le; 4 possess closed-form "
        "solutions via radicals (quadratic, cubic Cardano, and quartic Ferrari formulas). "
        "However, Galois theory establishes that the symmetric permutation group <i>S</i><sub><i>n</i></sub> is non-solvable for <i>n</i> &ge; 5. "
        "Consequently, for any financial project exceeding 4 years (<i>T</i> &ge; 5), **no general algebraic radical formula exists** to solve for IRR! "
        "Numerical analysis is not an engineering shortcut—it is an absolute mathematical necessity.",
        styles['Body']
    ))

    # Newton-Raphson Theorem Box
    th_content = [
        Paragraph("<b>Theorem 10.1 (Newton-Raphson Iterative Formulation & Analytical Derivative)</b>", styles['DefHeader']),
        Paragraph(
            "Newton-Raphson generates a sequence {<i>r</i><sub><i>k</i></sub>} converging quadratically to root <i>r</i>*:<br/>"
            "<font size=10><b><i>r</i><sub><i>k</i>+1</sub> = <i>r</i><sub><i>k</i></sub> &minus; [ <i>f</i>(<i>r</i><sub><i>k</i></sub>) / <i>f'</i>(<i>r</i><sub><i>k</i></sub>) ]</b></font><br/>"
            "where the exact first derivative is derived analytically without finite-difference errors:<br/>"
            "<font size=9.5><b><i>f'</i>(<i>r</i>) = &minus;&sum;<sub><i>t</i>=1</sub><sup><i>T</i></sup> [ <i>t</i> &middot; <i>C</i><sub><i>t</i></sub> / (1 + <i>r</i>)<sup><i>t</i>+1</sup> ]</b></font>",
            styles['Body']
        ),
        Paragraph(
            "<b>Quadratic Convergence:</b> Error satisfies |<i>e</i><sub><i>k</i>+1</sub>| &approx; |<i>f''</i>(<i>r</i>*) / (2<i>f'</i>(<i>r</i>*))| &middot; |<i>e</i><sub><i>k</i></sub>|<sup>2</sup>, "
            "doubling the number of valid significant digits at every single iteration.",
            styles['Body']
        )
    ]
    story.append(make_card(th_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLE 10.1 ====================
    story.append(Paragraph("10.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: full Newton-Raphson manual iteration trace, "
        "and resolving multiple non-unique IRRs under Descartes' Rule of Signs.",
        styles['Body']
    ))

    # Example 10.1 Card
    ex1_content = [
        Paragraph("<b>Example 10.1: Full Manual Newton-Raphson Iteration Trace</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> An investment requires outlay <b><i>C</i><sub>0</sub> = &minus;INR 100,000</b> and produces three annual inflows: "
            "<b><i>C</i><sub>1</sub> = INR 35,000</b>, <b><i>C</i><sub>2</sub> = INR 45,000</b>, and <b><i>C</i><sub>3</sub> = INR 45,000</b>. "
            "Using starting initial guess <b><i>r</i><sub>0</sub> = 0.100000 (10.00%)</b>, trace the Newton-Raphson sequence by hand "
            "until convergence is established to four decimal places.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Iteration 0 (Evaluate at <i>r</i><sub>0</sub> = 0.10):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>f</i>(0.10) = &minus;100,000 + 35,000/(1.1) + 45,000/(1.1)<sup>2</sup> + 45,000/(1.1)<sup>3</sup><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;= &minus;100,000 + 31,818.18 + 37,190.08 + 33,809.17 = <b>+INR 2,817.43</b>.<br/>"
            "&nbsp;&nbsp;&bull; <i>f'</i>(0.10) = &minus; [ 1&times;35,000/(1.1)<sup>2</sup> + 2&times;45,000/(1.1)<sup>3</sup> + 3&times;45,000/(1.1)<sup>4</sup> ]<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;= &minus; [ 28,925.62 + 67,618.33 + 92,206.82 ] = <b>&minus;188,750.77</b>.<br/>"
            "&nbsp;&nbsp;&bull; Update: <i>r</i><sub>1</sub> = <i>r</i><sub>0</sub> &minus; [ <i>f</i>(<i>r</i><sub>0</sub>) / <i>f'</i>(<i>r</i><sub>0</sub>) ] "
            "= 0.10 &minus; [ 2,817.43 / (&minus;188,750.77) ] = 0.10 + 0.014927 = <b>0.114927</b>.<br/><br/>"
            "<b>Iteration 1 (Evaluate at <i>r</i><sub>1</sub> = 0.114927):</b><br/>"
            "&nbsp;&nbsp;&bull; 1 + <i>r</i><sub>1</sub> = 1.114927.<br/>"
            "&nbsp;&nbsp;&bull; <i>f</i>(<i>r</i><sub>1</sub>) = &minus;100,000 + 35,000/(1.114927) + 45,000/(1.114927)<sup>2</sup> + 45,000/(1.114927)<sup>3</sup><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;= &minus;100,000 + 31,392.20 + 36,200.74 + 32,469.17 = <b>+INR 62.11</b>.<br/>"
            "&nbsp;&nbsp;&bull; <i>f'</i>(<i>r</i><sub>1</sub>) = &minus;181,940.35.<br/>"
            "&nbsp;&nbsp;&bull; Update: <i>r</i><sub>2</sub> = 0.114927 &minus; [ 62.11 / (&minus;181,940.35) ] = 0.114927 + 0.000341 = <b>0.115268</b>.<br/><br/>"
            "<b>Iteration 2 (Evaluate at <i>r</i><sub>2</sub> = 0.115268):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>f</i>(<i>r</i><sub>2</sub>) = <b>+INR 0.03</b> &approx; 0.00.<br/>"
            "&nbsp;&nbsp;&bull; <b>Converged IRR:</b> <i>r</i>* = <b>0.11527 &implies; 11.53% per annum</b> (converged in 2 steps!).",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 3: WORKED EXAMPLE 10.2 ====================
    # Example 10.2 Card
    ex2_content = [
        Paragraph("<b>Example 10.2: Descartes' Rule of Signs & The Multiple IRR Paradox</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> A natural resource strip-mining venture has an initial setup cost of "
            "<b><i>C</i><sub>0</sub> = &minus;INR 100,000</b>, generates operational cash flow of <b><i>C</i><sub>1</sub> = +INR 230,000</b> in Year 1, "
            "and incurs environmental remediation decommissioning costs of <b><i>C</i><sub>2</sub> = &minus;INR 132,000</b> in Year 2. "
            "Apply Descartes' Rule of Signs, determine all real IRRs, and discuss the analytical implications.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Descartes' Rule of Signs Analysis):</b><br/>"
            "&nbsp;&nbsp;Examine the sequence of cash flow signs: [&minus;, +, &minus;].<br/>"
            "&nbsp;&nbsp;&bull; Sign transitions: From &minus; to + (1st change), and + to &minus; (2nd change).<br/>"
            "&nbsp;&nbsp;&bull; Total sign changes = 2.<br/>"
            "&nbsp;&nbsp;&bull; By Descartes' Rule of Signs, the polynomial equation has either <b>2 or 0 positive real roots</b>.<br/><br/>"
            "<b>Step 2 (Exact Algebraic Root Determination):</b><br/>"
            "&nbsp;&nbsp;Set NPV equal to zero: &minus;100,000 + 230,000/(1+<i>r</i>) &minus; 132,000/(1+<i>r</i>)<sup>2</sup> = 0.<br/>"
            "&nbsp;&nbsp;Let <i>x</i> = 1 / (1 + <i>r</i>). The equation becomes quadratic:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&minus;100,000 + 230,000<i>x</i> &minus; 132,000<i>x</i><sup>2</sup> = 0.<br/>"
            "&nbsp;&nbsp;Dividing by &minus;2,000: 66<i>x</i><sup>2</sup> &minus; 115<i>x</i> + 50 = 0.<br/>"
            "&nbsp;&nbsp;Factoring: (11<i>x</i> &minus; 10)(6<i>x</i> &minus; 5) = 0.<br/>"
            "&nbsp;&nbsp;&bull; Root 1: <i>x</i><sub>1</sub> = 10 / 11 &rArr; 1 + <i>r</i><sub>1</sub> = 11 / 10 = 1.1000 &rArr; <b><i>r</i><sub>1</sub>* = 10.00%</b>.<br/>"
            "&nbsp;&nbsp;&bull; Root 2: <i>x</i><sub>2</sub> = 5 / 6 &rArr; 1 + <i>r</i><sub>2</sub> = 6 / 5 = 1.2000 &rArr; <b><i>r</i><sub>2</sub>* = 20.00%</b>.<br/><br/>"
            "<b>Step 3 (Financial Decision Paradox):</b><br/>"
            "&nbsp;&nbsp;&bull; Both 10.0% and 20.0% yield exact NPV = 0! For <i>r</i> &in; (10%, 20%), NPV &gt; 0, while outside, NPV &lt; 0.<br/>"
            "&nbsp;&nbsp;&bull; <i>Takeaway:</i> Multiple IRRs destroy the credibility of IRR for non-conventional cash flows. "
            "A decision support system must detect sign variations and advise fallback to Net Present Value.",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 4: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("10.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the complete implementation from <code>models/capital_budgeting.py</code>, "
        "featuring Newton-Raphson iteration with exact analytical derivatives and Bisection bracket fallback:",
        styles['Body']
    ))

    code_raw = (
        "from typing import List, Optional\n\n"
        "def irr_newton_raphson(\n"
        "    cash_flows: List[float], initial_guess: float = 0.10, tolerance: float = 1e-7, max_iter: int = 100\n"
        ") -> Optional[float]:\n"
        "    \"\"\"\n"
        "    Solves for IRR using Newton-Raphson with exact analytical derivative: f'(r) = -sum(t*C_t/(1+r)**(t+1)).\n"
        "    \"\"\"\n"
        "    r = initial_guess\n"
        "    for _ in range(max_iter):\n"
        "        f_val = sum(cf / ((1.0 + r) ** t) for t, cf in enumerate(cash_flows))\n"
        "        f_prime = sum(-t * cf / ((1.0 + r) ** (t + 1)) for t, cf in enumerate(cash_flows) if t > 0)\n"
        "        if abs(f_prime) < 1e-12:\n"
        "            return None  # Derivative near zero: switch to Bisection\n"
        "        r_next = r - (f_val / f_prime)\n"
        "        if abs(r_next - r) < tolerance:\n"
        "            return float(r_next)\n"
        "        r = r_next\n"
        "    return None\n\n\n"
        "def irr_bisection(\n"
        "    cash_flows: List[float], a: float = -0.50, b: float = 2.0, tolerance: float = 1e-7, max_iter: int = 100\n"
        ") -> Optional[float]:\n"
        "    \"\"\"Guaranteed convergence fallback bracketed solver: c = (a + b) / 2.\"\"\"\n"
        "    def npv(rate: float) -> float:\n"
        "        return sum(cf / ((1.0 + rate) ** t) for t, cf in enumerate(cash_flows))\n"
        "    fa, fb = npv(a), npv(b)\n"
        "    if fa * fb > 0:\n"
        "        return None\n"
        "    for _ in range(max_iter):\n"
        "        c = 0.5 * (a + b)\n"
        "        fc = npv(c)\n"
        "        if abs(fc) < tolerance or 0.5 * (b - a) < tolerance:\n"
        "            return float(c)\n"
        "        if fa * fc < 0:\n"
        "            b, fb = c, fc\n"
        "        else:\n"
        "            a, fa = c, fc\n"
        "    return float(0.5 * (a + b))\n"
    )
    story.append(make_code_card(code_raw, title="models/capital_budgeting.py — Hybrid Numerical IRR Engine"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("10.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Formula</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>Root Definition</b>", styles['Body']), Paragraph("NPV(<i>r</i>*) = 0", styles['Body']), Paragraph("Internal yield rate balancing discounted outflows and inflows", styles['Body'])],
        [Paragraph("<b>Abel-Ruffini Bound</b>", styles['Body']), Paragraph("Non-solvable for <i>T</i> &ge; 5", styles['Body']), Paragraph("No closed-form algebraic radical formulas exist; mandates numerical schemes", styles['Body'])],
        [Paragraph("<b>Newton-Raphson Order</b>", styles['Body']), Paragraph("Order 2 (Quadratic)", styles['Body']), Paragraph("Doubles significant decimal precision per iterative step", styles['Body'])],
        [Paragraph("<b>Bisection Convergence</b>", styles['Body']), Paragraph("Linear (|<i>e</i><sub><i>k</i></sub>| &le; 2<sup>&minus;<i>k</i></sup>(<i>b</i>&minus;<i>a</i>))", styles['Body']), Paragraph("Unconditional convergence guaranteed whenever bracket sign flips", styles['Body'])],
        [Paragraph("<b>Descartes' Bound</b>", styles['Body']), Paragraph("Roots &le; Sign Changes", styles['Body']), Paragraph("Detects potential multiple IRR ambiguities in non-conventional cash flows", styles['Body'])]
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
    out_file = os.path.join(out_dir, "10_Internal_Rate_of_Return_IRR.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
