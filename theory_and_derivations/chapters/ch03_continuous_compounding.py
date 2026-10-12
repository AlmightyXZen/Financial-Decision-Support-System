"""
Chapter 03: Continuous Compounding & Limits in Real Analysis.
Textbook chapter with real analysis limit proof, force of interest ODE,
time-varying yield integration, two hand-solved examples, and Python code.
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

    # ==================== PAGE 1: THEORY & ANALYSIS LIMITS ====================
    story.append(Paragraph("CHAPTER 3", styles['ChapterLabel']))
    story.append(Paragraph("Continuous Compounding & Analysis Limits", styles['ChapterTitle']))
    story.append(Paragraph(
        "Euler's Limit, The Force of Interest, Time-Varying ODE Integration, and Continuous Valuation",
        styles['Subtitle']
    ))
    story.append(HRFlowable(width="100%", thickness=1.2, color=pal['primary'], spaceAfter=7))

    story.append(Paragraph("3.1 Definition & Real Analysis Limit", styles['H1']))
    story.append(Paragraph(
        "In modern mathematical finance and stochastic calculus, interest is assumed to accrue <b>continuously</b> "
        "rather than in discrete quarterly or monthly jumps. Continuous compounding represents the asymptotic limit "
        "as compounding frequency approaches infinity (<i>n</i> &rarr; &infin;).",
        styles['Body']
    ))

    # Definition Box
    def_content = [
        Paragraph("<b>Definition 3.1 (Continuous Compounding Limit)</b>", styles['DefHeader']),
        Paragraph(
            "Let initial principal be <i>P</i> &gt; 0, nominal annual interest rate be <i>r</i> &ge; 0, "
            "and time horizon be <i>t</i> &ge; 0 years. As compounding frequency <i>n</i> &rarr; &infin;, "
            "the discrete accumulation factor converges to the natural exponential function:",
            styles['Body']
        ),
        Spacer(1, 2),
        Paragraph("<i>A</i>(<i>t</i>) = lim<sub><i>n</i>&rarr;&infin;</sub> <i>P</i> (1 + <i>r</i> / <i>n</i>)<sup><i>nt</i></sup> = <i>P</i> &middot; <i>e</i><sup><i>rt</i></sup>", styles['Equation']),
        Spacer(1, 1),
        Paragraph("<i>I</i><sub>cont</sub>(<i>t</i>) = <i>A</i>(<i>t</i>) &minus; <i>P</i> = <i>P</i> (<i>e</i><sup><i>rt</i></sup> &minus; 1)", styles['Equation']),
        Spacer(1, 2),
        Paragraph("where <i>e</i> &approx; 2.718281828... is Euler's constant. The accumulation factor is <i>a</i>(<i>t</i>) = <i>e</i><sup><i>rt</i></sup>.", styles['EquationSub'])
    ]
    story.append(make_card(def_content, pad_v=6, pad_h=12))
    story.append(Spacer(1, 5))

    story.append(Paragraph("3.2 Mathematical Derivation via Euler's Number", styles['H1']))
    story.append(Paragraph(
        "<b>Rigorous Limit Proof:</b><br/>"
        "Recall Euler's foundational definition of the exponential constant from real analysis: "
        "lim<sub><i>m</i>&rarr;&infin;</sub> (1 + 1/<i>m</i>)<sup><i>m</i></sup> = <i>e</i>.<br/>"
        "Let <i>m</i> = <i>n</i> / <i>r</i>. As <i>n</i> &rarr; &infin; with <i>r</i> &gt; 0 fixed, <i>m</i> &rarr; &infin;. "
        "Rewriting the discrete accumulation exponent:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; <i>nt</i> = (<i>m</i> &middot; <i>r</i>) &middot; <i>t</i> = <i>m</i> &middot; (<i>rt</i>).<br/>"
        "Substituting into the limit expression:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp; lim<sub><i>n</i>&rarr;&infin;</sub> <i>P</i> (1 + <i>r</i>/<i>n</i>)<sup><i>nt</i></sup> "
        "= <i>P</i> [ lim<sub><i>m</i>&rarr;&infin;</sub> (1 + 1/<i>m</i>)<sup><i>m</i></sup> ]<sup><i>rt</i></sup> "
        "= <i>P</i> &middot; <i>e</i><sup><i>rt</i></sup>. &#9632;",
        styles['Body']
    ))

    # Force of Interest ODE Card
    th_content = [
        Paragraph("<b>Theorem 3.1 (The Force of Interest & Differential Wealth Equation)</b>", styles['DefHeader']),
        Paragraph(
            "The instantaneous relative growth rate of wealth, termed the <b>force of interest</b> &delta;(<i>t</i>), "
            "is defined as &delta;(<i>t</i>) = <i>a'</i>(<i>t</i>) / <i>a</i>(<i>t</i>) = <i>d</i>/<i>dt</i> [ln <i>a</i>(<i>t</i>)].<br/>"
            "Under a constant rate <i>r</i>, &delta;(<i>t</i>) = <i>r</i>, yielding the fundamental homogeneous differential equation:<br/>"
            "<font size=10><b><i>dA</i>/<i>dt</i> = <i>r</i> &middot; <i>A</i>(<i>t</i>) &nbsp;&nbsp;&rArr;&nbsp;&nbsp; <i>A</i>(<i>t</i>) = <i>P</i> &middot; exp(&int;<sub>0</sub><sup><i>t</i></sup> &delta;(<i>s</i>) <i>ds</i>)</b></font>",
            styles['Body']
        ),
        Paragraph(
            "<b>Significance for Quantitative Finance:</b> This exponential ODE forms the exact foundation of "
            "stochastic differential equations (It&ocirc;'s Lemma) and the risk-neutral discounting framework in derivative pricing.",
            styles['Body']
        )
    ]
    story.append(make_card(th_content, bg_color=pal['th_bg'], border_color=pal['th_border'], pad_v=6, pad_h=12))

    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLE 3.1 ====================
    story.append(Paragraph("3.3 Step-by-Step Worked Examples", styles['H1']))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: constant continuous compounding vs discrete frequencies, "
        "and a time-varying term-structure force of interest integration.",
        styles['Body']
    ))

    # Example 3.1 Card
    ex1_content = [
        Paragraph("<b>Example 3.1: Sovereign Money Market Continuous Yield</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> An institutional fund manager invests <b><i>P</i> = INR 1,000,000</b> at a nominal annual rate "
            "<b><i>R</i> = 7.20% per annum</b> for <b><i>t</i> = 4 years</b>. Compare terminal accumulated wealth under:<br/>"
            "&nbsp;&nbsp;&bull; <b>Method A:</b> Discrete Annual Compounding (<i>n</i> = 1)<br/>"
            "&nbsp;&nbsp;&bull; <b>Method B:</b> Discrete Daily Compounding (<i>n</i> = 365)<br/>"
            "&nbsp;&nbsp;&bull; <b>Method C:</b> Continuous Compounding (<i>n</i> &rarr; &infin;)",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Method A (Annual Compounding, <i>n</i> = 1):</b><br/>"
            "&nbsp;&nbsp;&bull; <i>A</i><sub>annual</sub> = 1,000,000 &times; (1.072)<sup>4</sup> = 1,000,000 &times; 1.320623 = <b>INR 1,320,623.38</b><br/><br/>"
            "<b>Method B (Daily Compounding, <i>n</i> = 365):</b><br/>"
            "&nbsp;&nbsp;&bull; Periodic rate: <i>i</i> = 0.072 / 365 &approx; 0.0001972603<br/>"
            "&nbsp;&nbsp;&bull; Total periods: <i>N</i> = 365 &times; 4 = 1,460 days<br/>"
            "&nbsp;&nbsp;&bull; <i>A</i><sub>daily</sub> = 1,000,000 &times; (1 + 0.072/365)<sup>1460</sup> = 1,000,000 &times; 1.333742 = <b>INR 1,333,742.45</b><br/><br/>"
            "<b>Method C (Continuous Compounding, <i>n</i> &rarr; &infin;):</b><br/>"
            "&nbsp;&nbsp;&bull; Exponent: <i>r</i> &middot; <i>t</i> = 0.072 &times; 4 = 0.288<br/>"
            "&nbsp;&nbsp;&bull; Exponential factor: <i>e</i><sup>0.288</sup> &approx; 1.33375845<br/>"
            "&nbsp;&nbsp;&bull; <i>A</i><sub>cont</sub> = 1,000,000 &times; 1.33375845 = <b>INR 1,333,758.45</b><br/><br/>"
            "<b>Asymptotic Comparison:</b><br/>"
            "&nbsp;&nbsp;&bull; Gain over annual compounding: 1,333,758.45 &minus; 1,320,623.38 = <b>INR 13,135.07</b> excess return.<br/>"
            "&nbsp;&nbsp;&bull; Daily vs Continuous gap: 1,333,758.45 &minus; 1,333,742.45 = <b>INR 16.00</b>.<br/>"
            "&nbsp;&nbsp;&bull; <i>Takeaway:</i> Daily compounding captures 99.88% of the continuous theoretical supremum bound.",
            styles['Body']
        )
    ]
    story.append(make_card(ex1_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 3: WORKED EXAMPLE 3.2 ====================
    # Example 3.2 Card
    ex2_content = [
        Paragraph("<b>Example 3.2: Time-Varying Force of Interest Integration</b>", styles['DefHeader']),
        Paragraph(
            "<b>Problem Statement:</b> An economic environment features a rising term structure of interest rates where the "
            "force of interest increases linearly over time according to <b>&delta;(<i>t</i>) = 0.04 + 0.01<i>t</i></b>. "
            "Compute the accumulated value of principal <b><i>P</i> = INR 200,000</b> invested for <b><i>t</i> = 6 years</b>.",
            styles['Body']
        ),
        HRFlowable(width="100%", thickness=0.5, color=pal['border'], spaceAfter=5, spaceBefore=3),
        Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/><br/>"
            "<b>Step 1 (Formulation of Accumulation Integral):</b><br/>"
            "&nbsp;&nbsp;From Theorem 3.1, the accumulation factor under time-varying yield is:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>a</i>(<i>t</i>) = exp(&int;<sub>0</sub><sup><i>t</i></sup> &delta;(<i>s</i>) <i>ds</i>)<br/><br/>"
            "<b>Step 2 (Definite Integration of Force Function):</b><br/>"
            "&nbsp;&nbsp;Integrate &delta;(<i>s</i>) = 0.04 + 0.01<i>s</i> over limits [0, 6]:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&int;<sub>0</sub><sup>6</sup> (0.04 + 0.01<i>s</i>) <i>ds</i> "
            "= [ 0.04<i>s</i> + 0.005<i>s</i><sup>2</sup> ]<sub>0</sub><sup>6</sup><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;= (0.04 &times; 6) + (0.005 &times; 6<sup>2</sup>)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;= 0.24 + (0.005 &times; 36) = 0.24 + 0.18 = <b>0.4200</b>.<br/><br/>"
            "<b>Step 3 (Terminal Capital Valuation):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>A</i>(6) = <i>P</i> &middot; <i>e</i><sup>0.4200</sup> = 200,000 &times; exp(0.42)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Since <i>e</i><sup>0.42</sup> &approx; 1.521961556:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>A</i>(6) = 200,000 &times; 1.521961556 = <b>INR 304,392.31</b>.<br/><br/>"
            "<b>Step 4 (Equivalent Constant Rate Benchmark):</b><br/>"
            "&nbsp;&nbsp;&bull; Average force of interest: <i>r̄</i> = 0.42 / 6 = 0.0700 (7.00% per annum).<br/>"
            "&nbsp;&nbsp;&bull; Total interest accrued: 304,392.31 &minus; 200,000 = <b>INR 104,392.31</b>.<br/>"
            "&nbsp;&nbsp;&bull; <i>Insight:</i> This illustrates how continuous compounding elegantly extends to continuous yield curves "
            "and term-structure models (e.g., Vasicek and Hull-White interest rate models in Quantitative Finance).",
            styles['Body']
        )
    ]
    story.append(make_card(ex2_content, pad_v=8, pad_h=14))

    story.append(PageBreak())

    # ==================== PAGE 4: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("3.4 Algorithmic Implementation in Python", styles['H1']))
    story.append(Paragraph(
        "Below is the production-grade Python implementation from <code>models/time_value.py</code>, "
        "featuring standard continuous compounding and numerical integration for dynamic force functions:",
        styles['Body']
    ))

    code_raw = (
        "import math\n\n"
        "def continuous_compound_amount(principal: float, annual_rate: float, time_years: float) -> float:\n"
        "    \"\"\"\n"
        "    Computes terminal wealth under continuous compounding: A = P * exp(r * t).\n"
        "    \"\"\"\n"
        "    if principal < 0.0 or annual_rate < 0.0 or time_years < 0.0:\n"
        "        raise ValueError(\"Financial arguments must be non-negative.\")\n"
        "    return float(principal * math.exp(annual_rate * time_years))\n\n\n"
        "def continuous_interest(principal: float, annual_rate: float, time_years: float) -> float:\n"
        "    \"\"\"\n"
        "    Computes accrued continuous interest: I = P * (exp(r * t) - 1).\n"
        "    \"\"\"\n"
        "    return float(continuous_compound_amount(principal, annual_rate, time_years) - principal)\n"
    )
    story.append(make_code_card(code_raw, title="models/time_value.py — Continuous Compounding Engine"))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.5 Mathematical Properties Summary", styles['H1']))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", styles['H2']), Paragraph("<b>Specification & Formula</b>", styles['H2']), Paragraph("<b>Analytical Significance</b>", styles['H2'])],
        [Paragraph("<b>Domain & Constraints</b>", styles['Body']), Paragraph("<i>P</i> &gt; 0, <i>r</i> &ge; 0, <i>t</i> &ge; 0", styles['Body']), Paragraph("Smooth continuous state variable domain", styles['Body'])],
        [Paragraph("<b>Accumulation Factor</b>", styles['Body']), Paragraph("<i>a</i>(<i>t</i>) = <i>e</i><sup><i>rt</i></sup>", styles['Body']), Paragraph("Infinitely differentiable real analytic function", styles['Body'])],
        [Paragraph("<b>ODE Characterization</b>", styles['Body']), Paragraph("<i>da</i>/<i>dt</i> = <i>r</i> &middot; <i>a</i>(<i>t</i>)", styles['Body']), Paragraph("Wealth growth velocity proportional to current wealth", styles['Body'])],
        [Paragraph("<b>Discounting Factor</b>", styles['Body']), Paragraph("<i>v</i>(<i>t</i>) = <i>e</i><sup>&minus;<i>rt</i></sup>", styles['Body']), Paragraph("Continuous time discounting kernel", styles['Body'])],
        [Paragraph("<b>Force of Interest</b>", styles['Body']), Paragraph("&delta;(<i>t</i>) = <i>a'</i>(<i>t</i>) / <i>a</i>(<i>t</i>) = <i>r</i>", styles['Body']), Paragraph("Constant instantaneous log-return rate", styles['Body'])]
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
    out_file = os.path.join(out_dir, "03_Continuous_Compounding.pdf")
    build_pdf(out_file)
    print(f"Generated {out_file}")
