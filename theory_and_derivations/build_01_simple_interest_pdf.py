"""
Textbook-Grade PDF Builder for Topic 01: Simple Interest & Linear Accumulation.
Features Springer/Cambridge style layout:
- Exact 3-page modular chapter structure
- Page 1: Mathematical Foundations, ODE formulation, and Theorem 1.1
- Page 2: Two Complete Hand-Solved Examples (Bond Yield & Banker's Rule)
- Page 3: Clean Algorithmic Python Listing & Mathematical Properties Matrix
- Zero split cards, zero awkward line wrapping, beautiful reading flow
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Preformatted, PageBreak
)
from reportlab.pdfgen import canvas

class TextbookCanvas(canvas.Canvas):
    """Two-pass canvas for professional textbook running headers and footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        
        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica", 8.5)
            self.setFillColor(colors.HexColor("#64748B"))
            if self._pageNumber % 2 == 0:
                self.drawString(54, 750, "CHAPTER 1. SIMPLE INTEREST & LINEAR ACCUMULATION")
                self.setFont("Helvetica-Bold", 8.5)
                self.drawRightString(558, 750, "FINANCIAL DECISION SUPPORT SYSTEM")
            else:
                self.drawString(54, 750, "MATHEMATICAL FOUNDATIONS OF FINANCE")
                self.setFont("Helvetica-Bold", 8.5)
                self.drawRightString(558, 750, "TOPIC 01")
                
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.6)
            self.line(54, 742, 558, 742)

        # Running Footer (all pages)
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        page_text = f"—  {self._pageNumber}  —"
        self.drawCentredString(306, 32, page_text)
        
        self.restoreState()


def create_simple_interest_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=46,
        bottomMargin=44
    )

    styles = getSampleStyleSheet()

    # Textbook Palette
    c_primary = colors.HexColor("#0F172A")    # Deep slate
    c_accent = colors.HexColor("#1E3A8A")     # Formal navy
    c_body = colors.HexColor("#1E293B")       # Dark readable text
    c_sub = colors.HexColor("#475569")        # Subtext / meta
    c_box_bg = colors.HexColor("#F8FAFC")     # Clean card fill
    c_border = colors.HexColor("#CBD5E1")     # Light border rule
    c_th_bg = colors.HexColor("#EFF6FF")      # Theorem highlight fill
    c_th_border = colors.HexColor("#93C5FD")  # Theorem border

    # Typography Styles
    ch_label_style = ParagraphStyle(
        'ChapterLabel', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=13,
        textColor=c_accent, spaceAfter=2
    )

    title_style = ParagraphStyle(
        'ChapterTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=20, leading=24,
        textColor=c_primary, spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=14,
        textColor=c_sub, spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'H1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11.5, leading=15,
        textColor=c_accent, spaceBefore=7, spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=c_primary, spaceBefore=5, spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.7, leading=12.8,
        textColor=c_body, spaceAfter=4
    )

    def_header_style = ParagraphStyle(
        'DefHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=c_accent, spaceAfter=3
    )

    eq_style = ParagraphStyle(
        'Equation', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10.5, leading=15,
        textColor=c_primary, alignment=1
    )

    eq_sub_style = ParagraphStyle(
        'EquationSub', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8, leading=11,
        textColor=c_sub, alignment=1
    )

    pre_style = ParagraphStyle(
        'PreformattedCode', parent=styles['Normal'],
        fontName='Courier', fontSize=7.6, leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # ==================== PAGE 1: THEORY & FORMAL DERIVATIONS ====================
    story.append(Paragraph("CHAPTER 1", ch_label_style))
    story.append(Paragraph("Simple Interest & Linear Accumulation", title_style))
    story.append(Paragraph(
        "Axiomatic Foundations, Differential Formulations, and Step-by-Step Analytical Solutions",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=7))

    # Section 1.1
    story.append(Paragraph("1.1 Definition & Mathematical Axioms", h1_style))
    story.append(Paragraph(
        "Simple Interest represents the foundational linear model of capital valuation. "
        "The defining principle is that interest accrued over any sub-interval is <b>never capitalized</b> "
        "into the principal; earned interest remains isolated and generates zero additional return.",
        body_style
    ))

    # Definition Box
    def_content = [
        [Paragraph("<b>Definition 1.1 (Simple Accumulation Function)</b>", def_header_style)],
        [Paragraph(
            "Let initial capital principal be <i>P</i> &gt; 0, nominal annual interest rate be <i>r</i> &ge; 0 "
            "(decimal fraction: <i>r</i> = <i>R</i> / 100 for percentage rate <i>R</i>%), "
            "and time horizon be <i>t</i> &ge; 0 measured in years.<br/>"
            "The <b>total accrued interest</b> <i>I</i>(<i>t</i>) and <b>terminal accumulated value</b> <i>A</i>(<i>t</i>) are defined by:",
            body_style
        )],
        [Spacer(1, 2)],
        [Paragraph("<i>I</i>(<i>t</i>) = <i>P</i> &middot; <i>r</i> &middot; <i>t</i>", eq_style)],
        [Spacer(1, 1)],
        [Paragraph("<i>A</i>(<i>t</i>) = <i>P</i> + <i>I</i>(<i>t</i>) = <i>P</i>(1 + <i>r</i> &middot; <i>t</i>)", eq_style)],
        [Spacer(1, 2)],
        [Paragraph("The accumulation factor is denoted as <i>a</i>(<i>t</i>) = 1 + <i>r</i> &middot; <i>t</i>, which satisfies <i>a</i>(0) = 1.", eq_sub_style)]
    ]
    t_def = Table(def_content, colWidths=[504])
    t_def.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_box_bg),
        ('BOX', (0, 0), (-1, -1), 0.7, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_def)
    story.append(Spacer(1, 5))

    # Section 1.2
    story.append(Paragraph("1.2 First-Principles Derivation & Differential Viewpoint", h1_style))
    story.append(Paragraph(
        "<b>Axiomatic Derivation:</b> Under simple accumulation, interest <i>I</i> satisfies three simultaneous linear proportionalities: "
        "(1) <i>I</i> &prop; <i>P</i> (principal scale invariance), (2) <i>I</i> &prop; <i>r</i> (yield homogeneity), and (3) <i>I</i> &prop; <i>t</i> (temporal linearity). "
        "Combining these yields <i>I</i> = <i>k</i> &middot; <i>P</i> &middot; <i>r</i> &middot; <i>t</i>, with proportionality constant <i>k</i> = 1 by convention.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Ordinary Differential Equation (ODE) Perspective:</b><br/>"
        "Examining instantaneous wealth rate of change <i>dA</i>/<i>dt</i> contrasts simple and continuous regimes:",
        body_style
    ))

    # ODE Comparison Table
    ode_table_data = [
        [
            Paragraph("<b>Valuation Regime</b>", h2_style),
            Paragraph("<b>Governing Differential Equation</b>", h2_style),
            Paragraph("<b>Closed-Form Solution <i>A</i>(<i>t</i>)</b>", h2_style),
            Paragraph("<b>Growth Dynamic</b>", h2_style)
        ],
        [
            Paragraph("<b>Simple Interest</b>", body_style),
            Paragraph("<i>d</i><i>A</i>/<i>dt</i> = <i>P</i> &middot; <i>r</i>", body_style),
            Paragraph("<i>A</i>(<i>t</i>) = <i>P</i>(1 + <i>rt</i>)", body_style),
            Paragraph("Constant slope (Linear)", body_style)
        ],
        [
            Paragraph("<b>Continuous Compounding</b>", body_style),
            Paragraph("<i>d</i><i>A</i>/<i>dt</i> = <i>r</i> &middot; <i>A</i>(<i>t</i>)", body_style),
            Paragraph("<i>A</i>(<i>t</i>) = <i>P</i> &middot; <i>e</i><sup><i>rt</i></sup>", body_style),
            Paragraph("Wealth-proportional (Exponential)", body_style)
        ]
    ]
    t_ode = Table(ode_table_data, colWidths=[114, 140, 140, 110])
    t_ode.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.6, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_ode)
    story.append(Spacer(1, 5))

    # Theorem 1.1 Box
    th_content = [
        [Paragraph("<b>Theorem 1.1 (Sub-Period Dominance via Bernoulli's Inequality)</b>", def_header_style)],
        [Paragraph(
            "For any strictly positive rate <i>r</i> &gt; 0 and fractional duration <i>t</i> &in; (0, 1), simple interest accumulation "
            "is <i>strictly greater</i> than annual compound interest accumulation:<br/>"
            "<font size=9.5><b>1 + <i>r</i> &middot; <i>t</i> &gt; (1 + <i>r</i>)<sup><i>t</i></sup> &nbsp;&nbsp;&forall; <i>t</i> &in; (0, 1)</b></font>",
            body_style
        )],
        [Paragraph(
            "<b>Proof:</b> Let <i>f</i>(<i>t</i>) = (1 + <i>r</i>)<sup><i>t</i></sup> for <i>t</i> &ge; 0. The second derivative is "
            "<i>f''</i>(<i>t</i>) = [ln(1 + <i>r</i>)]<sup>2</sup>(1 + <i>r</i>)<sup><i>t</i></sup>. Since [ln(1+<i>r</i>)]<sup>2</sup> &gt; 0 "
            "and (1+<i>r</i>)<sup><i>t</i></sup> &gt; 0 for all <i>r</i> &gt; 0, <i>f''</i>(<i>t</i>) &gt; 0 strictly, confirming <i>f</i> is strictly convex.<br/>"
            "The secant line connecting (0, 1) and (1, 1+<i>r</i>) is <i>g</i>(<i>t</i>) = 1 + <i>rt</i>. By strict convexity, the graph of <i>f</i> "
            "lies strictly below chord <i>g</i> on the open interval (0, 1). Thus, (1 + <i>r</i>)<sup><i>t</i></sup> &lt; 1 + <i>rt</i>. &#9632;",
            body_style
        )]
    ]
    t_th = Table(th_content, colWidths=[504])
    t_th.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_th_bg),
        ('BOX', (0, 0), (-1, -1), 0.7, c_th_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_th)

    # Force Page Break to Page 2
    story.append(PageBreak())

    # ==================== PAGE 2: WORKED EXAMPLES ====================
    story.append(Paragraph("1.3 Step-by-Step Worked Examples", h1_style))
    story.append(Paragraph(
        "Below are two formal case studies solved by hand: a multi-year sovereign bond yield and a money-market bridge facility with exact day counts.",
        body_style
    ))

    # Example 1.1 Card
    ex1_content = [
        [Paragraph("<b>Example 1.1: Multi-Year Sovereign Treasury Bond</b>", def_header_style)],
        [Paragraph(
            "<b>Problem:</b> An investor commits principal capital of <b><i>P</i> = INR 100,000</b> into a fixed-income "
            "treasury bond offering a simple interest rate of <b><i>R</i> = 7.50% per annum</b>. The bond matures in "
            "<b><i>t</i> = 3 years</b>. Calculate total interest accrued and final maturity amount.",
            body_style
        )],
        [HRFlowable(width="100%", thickness=0.5, color=c_border, spaceAfter=4, spaceBefore=2)],
        [Paragraph(
            "<b>Step-by-Step Analytical Solution:</b><br/>"
            "&bull; <b>Step 1 (Parameter Normalization):</b> <i>P</i> = 100,000, &nbsp; <i>r</i> = 7.50 / 100 = 0.075, &nbsp; <i>t</i> = 3.0 years.<br/>"
            "&bull; <b>Step 2 (Interest Calculation):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>I</i> = <i>P</i> &middot; <i>r</i> &middot; <i>t</i> = 100,000 &times; 0.075 &times; 3 = 100,000 &times; 0.225 = <b>INR 22,500.00</b><br/>"
            "&bull; <b>Step 3 (Terminal Wealth Calculation):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>A</i> = <i>P</i> + <i>I</i> = 100,000 + 22,500 = <b>INR 122,500.00</b><br/>"
            "&bull; <b>Step 4 (Annual Verification):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Year 1: <i>I</i><sub>1</sub> = INR 7,500.00 &nbsp;|&nbsp; Year 2: <i>I</i><sub>2</sub> = INR 7,500.00 &nbsp;|&nbsp; Year 3: <i>I</i><sub>3</sub> = INR 7,500.00<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Total sum: 3 &times; 7,500 = INR 22,500.00 (verified exact linear accumulation).",
            body_style
        )]
    ]
    t_ex1 = Table(ex1_content, colWidths=[504])
    t_ex1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_box_bg),
        ('BOX', (0, 0), (-1, -1), 0.7, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_ex1)
    story.append(Spacer(1, 6))

    # Example 1.2 Card
    ex2_content = [
        [Paragraph("<b>Example 1.2: Fractional Tenors & Day-Count Mechanics (The Banker's Rule)</b>", def_header_style)],
        [Paragraph(
            "<b>Problem:</b> A short-term commercial credit facility of <b><i>P</i> = INR 250,000</b> is issued on "
            "<b>March 15</b> at an annual simple rate of <b><i>R</i> = 9.20%</b>, and repaid on <b>October 28</b> of "
            "the same non-leap year. Compare interest accrued under:<br/>"
            "&nbsp;&nbsp;&bull; <b>Method A:</b> Exact / Actual/365 Convention (Common in sovereign bond markets)<br/>"
            "&nbsp;&nbsp;&bull; <b>Method B:</b> Banker's Rule / Actual/360 Convention (Standard in US money markets and commercial paper)",
            body_style
        )],
        [HRFlowable(width="100%", thickness=0.5, color=c_border, spaceAfter=4, spaceBefore=2)],
        [Paragraph(
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
            body_style
        )]
    ]
    t_ex2 = Table(ex2_content, colWidths=[504])
    t_ex2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_box_bg),
        ('BOX', (0, 0), (-1, -1), 0.7, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_ex2)

    # Force Page Break to Page 3
    story.append(PageBreak())

    # ==================== PAGE 3: CODE & PROPERTIES SUMMARY ====================
    story.append(Paragraph("1.4 Algorithmic Implementation in Python", h1_style))
    story.append(Paragraph(
        "Below is the complete implementation from <code>models/time_value.py</code>. "
        "It provides domain validation, typing, and clear docstrings for modular inclusion in the system:",
        body_style
    ))

    code_raw = (
        "# models/time_value.py\n\n"
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

    t_code = Table([[Preformatted(code_raw, pre_style)]], colWidths=[504])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_code)
    story.append(Spacer(1, 10))

    # Properties Summary Table
    story.append(Paragraph("1.5 Mathematical Properties Summary", h1_style))
    prop_data = [
        [Paragraph("<b>Mathematical Property</b>", h2_style), Paragraph("<b>Specification & Value</b>", h2_style), Paragraph("<b>Analytical Significance</b>", h2_style)],
        [Paragraph("<b>Domain & Constraints</b>", body_style), Paragraph("<i>P</i> &gt; 0, <i>r</i> &ge; 0, <i>t</i> &ge; 0", body_style), Paragraph("Strict non-negativity across economic state variables", body_style)],
        [Paragraph("<b>Accumulation Function</b>", body_style), Paragraph("<i>a</i>(<i>t</i>) = 1 + <i>rt</i>", body_style), Paragraph("Affine linear operator with slope equal to nominal rate <i>r</i>", body_style)],
        [Paragraph("<b>Marginal Accrual Rate</b>", body_style), Paragraph("<i>da</i>/<i>dt</i> = <i>r</i>", body_style), Paragraph("Invariant to elapsed time <i>t</i> and current accumulated wealth", body_style)],
        [Paragraph("<b>Convexity / Curvature</b>", body_style), Paragraph("<i>d</i><sup>2</sup><i>a</i>/<i>dt</i><sup>2</sup> = 0", body_style), Paragraph("Zero second derivative; absence of compounding curvature", body_style)]
    ]
    t_prop = Table(prop_data, colWidths=[130, 154, 220])
    t_prop.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.7, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_prop)

    # Build document
    doc.build(story, canvasmaker=TextbookCanvas)
    print(f"Successfully generated clean 3-page textbook-style PDF: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Atharv Ranade\Atharv\Avishkar\Financial-Decision-Support-System\theory_and_derivations"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "01_Simple_Interest.pdf")
    create_simple_interest_pdf(out_file)
