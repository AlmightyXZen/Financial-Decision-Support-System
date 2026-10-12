"""
Refined PDF Builder for Topic 01: Simple Interest & Linear Time Value of Money.
Creates a 2-page academic reference dossier with proper font glyphs (INR),
clean mathematical typography, and balanced layout.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for professional headers and 'Page X of Y' footers."""
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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 752, "FINANCIAL DECISION SUPPORT SYSTEM (FDSS)  |  MATHEMATICAL REFERENCE DOSSIER")
            self.setFont("Helvetica", 8)
            self.drawRightString(558, 752, "TOPIC 01: SIMPLE INTEREST")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(54, 746, 558, 746)
        
        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 34, "Avishkar Research Convention (MU)  *  Pure Sciences: Mathematics & Statistics")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 34, page_text)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.6)
        self.line(54, 44, 558, 44)
        self.restoreState()


def create_simple_interest_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Custom palette
    c_primary = colors.HexColor("#0F172A")    # Deep navy slate
    c_accent = colors.HexColor("#1E40AF")     # Academic cobalt blue
    c_dark = colors.HexColor("#1E293B")       # Dark charcoal body
    c_muted = colors.HexColor("#64748B")      # Muted gray
    c_card_bg = colors.HexColor("#F8FAFC")    # Clean slate card background
    c_border = colors.HexColor("#E2E8F0")     # Subtle border
    c_box_bg = colors.HexColor("#EFF6FF")     # Equation callout box
    c_code_bg = colors.HexColor("#F1F5F9")    # Code block background

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=17, leading=21,
        textColor=c_primary, spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=13,
        textColor=c_accent, spaceAfter=4
    )

    meta_style = ParagraphStyle(
        'DocMeta', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11,
        textColor=c_muted, spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'H1_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=c_accent, spaceBefore=7, spaceAfter=3
    )

    h2_style = ParagraphStyle(
        'H2_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=c_primary
    )

    body_style = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.3, leading=11.8,
        textColor=c_dark, spaceAfter=4
    )

    eq_box_style = ParagraphStyle(
        'Equation_Box', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=14,
        textColor=c_accent, alignment=1
    )

    eq_sub_style = ParagraphStyle(
        'Equation_Sub', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11,
        textColor=c_dark, alignment=1
    )

    code_style = ParagraphStyle(
        'Code_Custom', parent=styles['Normal'],
        fontName='Courier', fontSize=7.5, leading=10,
        textColor=colors.HexColor("#0F172A")
    )

    qa_q_style = ParagraphStyle(
        'QA_Q', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.2, leading=11.5,
        textColor=c_accent, spaceBefore=3, spaceAfter=1
    )

    qa_a_style = ParagraphStyle(
        'QA_A', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11,
        textColor=c_dark, spaceAfter=4
    )

    story = []

    # ==================== PAGE 1 ====================
    # Title Banner
    story.append(Paragraph("TOPIC 01: SIMPLE INTEREST & LINEAR TIME VALUE", title_style))
    story.append(Paragraph("Formal Mathematical Foundations, Real Analysis Bounds, and Hand-Solved Case Studies", subtitle_style))
    story.append(Paragraph("<b>Author:</b> Atharv Ranade &nbsp;|&nbsp; <b>Field:</b> B.Sc. Mathematics & Statistics &nbsp;|&nbsp; <b>Affiliation:</b> University of Mumbai", meta_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=6))

    # Section 1: Axiomatic Definition
    story.append(Paragraph("1. Mathematical Definition & Axiomatic Assumptions", h1_style))
    story.append(Paragraph(
        "Simple Interest represents the foundational linear model in financial valuation. It assumes that interest "
        "earned across any discrete time increment is <i>never reinvested</i> into the principal base.",
        body_style
    ))
    story.append(Paragraph(
        "Let the initial principal be <i>P</i> &gt; 0, nominal annual interest rate be <i>r</i> &ge; 0 "
        "(decimal fraction: <i>r</i> = <i>R</i> / 100 for percentage rate <i>R</i>%), and investment horizon be <i>t</i> &ge; 0 years.",
        body_style
    ))

    # Display Equation Box
    eq_content = [
        [Paragraph("<i>I</i>(<i>t</i>) = <i>P</i> &middot; <i>r</i> &middot; <i>t</i>", eq_box_style)],
        [Paragraph("<i>A</i>(<i>t</i>) = <i>P</i> + <i>I</i>(<i>t</i>) = <i>P</i>(1 + <i>r</i> &middot; <i>t</i>)", eq_box_style)],
        [Paragraph("where <i>I</i>(<i>t</i>) is accrued interest and <i>A</i>(<i>t</i>) is terminal accumulated capital.", eq_sub_style)]
    ]
    t_eq = Table(eq_content, colWidths=[512])
    t_eq.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_box_bg),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_eq)
    story.append(Spacer(1, 4))

    # Section 2: Mathematical Derivation & Differential Formulation
    story.append(Paragraph("2. Mathematical Derivation & Differential Formulation", h1_style))
    story.append(Paragraph(
        "<b>Axiomatic Derivation:</b> Under simple accumulation, interest <i>I</i> satisfies three simultaneous linear proportionalities: "
        "(1) <i>I</i> &prop; <i>P</i> (scale invariance), (2) <i>I</i> &prop; <i>r</i> (yield homogeneity), and (3) <i>I</i> &prop; <i>t</i> (temporal linearity). "
        "Combining these yields <i>I</i> = <i>k</i> &middot; <i>P</i> &middot; <i>r</i> &middot; <i>t</i>, with <i>k</i> = 1 by convention.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Differential Equation Perspective:</b> Examining instantaneous wealth growth <i>A</i>(<i>t</i>) reveals the key distinction between linear and compound regimes:",
        body_style
    ))

    # ODE Comparison Table
    ode_data = [
        [Paragraph("<b>Model</b>", h2_style), Paragraph("<b>Governing Differential Equation</b>", h2_style), Paragraph("<b>Solution Function <i>A</i>(<i>t</i>)</b>", h2_style)],
        [Paragraph("<b>Simple Interest</b>", body_style), Paragraph("<i>d</i><i>A</i>/<i>dt</i> = <i>P</i> &middot; <i>r</i> &nbsp; (constant rate)", body_style), Paragraph("<i>A</i>(<i>t</i>) = <i>P</i>(1 + <i>r</i>&middot;<i>t</i>) &nbsp; [Linear]", body_style)],
        [Paragraph("<b>Continuous Compounding</b>", body_style), Paragraph("<i>d</i><i>A</i>/<i>dt</i> = <i>r</i> &middot; <i>A</i>(<i>t</i>) &nbsp; (wealth-dependent)", body_style), Paragraph("<i>A</i>(<i>t</i>) = <i>P</i> &middot; <i>e</i><sup><i>rt</i></sup> &nbsp; [Exponential]", body_style)]
    ]
    t_ode = Table(ode_data, colWidths=[120, 202, 190])
    t_ode.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.6, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_ode)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Real Analysis Theorem (Bernoulli Inequality Application):</b><br/>"
        "For any annual rate <i>r</i> &gt; 0 and fractional time period <i>t</i> &in; (0, 1), simple interest is <i>strictly superior</i> to annual compound interest:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>(1 + <i>r</i>)<sup><i>t</i></sup> &lt; 1 + <i>r</i> &middot; <i>t</i> &nbsp;&nbsp;&forall; <i>t</i> &in; (0, 1)</b><br/>"
        "<i>Proof:</i> Define <i>f</i>(<i>t</i>) = (1 + <i>r</i>)<sup><i>t</i></sup>. The second derivative <i>f''</i>(<i>t</i>) = [ln(1 + <i>r</i>)]<sup>2</sup>(1 + <i>r</i>)<sup><i>t</i></sup> &gt; 0, "
        "establishing strict convexity on [0, 1]. The linear chord connecting (0, 1) and (1, 1+<i>r</i>) is <i>g</i>(<i>t</i>) = 1 + <i>rt</i>. "
        "By strict convexity, the curve <i>f</i>(<i>t</i>) lies strictly beneath its chord <i>g</i>(<i>t</i>) on the interior (0, 1).",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Section 3: Worked Example 1 (Standard Case)
    story.append(Paragraph("3. Worked Example 1: Standard Multi-Year Bond Yield (Hand Solved)", h1_style))
    ex1_card = [
        [Paragraph("<b>Problem:</b> An investor places <i>P</i> = INR 100,000 in a sovereign debt instrument at an annual simple interest rate of <i>R</i> = 7.50% for <i>t</i> = 3 years. Compute total interest accrued and final maturity amount.", body_style)],
        [Paragraph(
            "<b>Formal Step-by-Step Hand Solution:</b><br/>"
            "&bull; <b>Step 1: Parameter Identification:</b> <i>P</i> = 100,000, &nbsp; <i>r</i> = 7.50 / 100 = 0.075, &nbsp; <i>t</i> = 3.0 years.<br/>"
            "&bull; <b>Step 2: Interest Accrual:</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>I</i> = <i>P</i> &middot; <i>r</i> &middot; <i>t</i> = 100,000 &times; 0.075 &times; 3 = 100,000 &times; 0.225 = <b>INR 22,500.00</b>.<br/>"
            "&bull; <b>Step 3: Terminal Capital:</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>A</i> = <i>P</i> + <i>I</i> = 100,000 + 22,500 = <b>INR 122,500.00</b>.<br/>"
            "&bull; <b>Step 4: Annual Periodic Verification:</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Year 1: <i>I</i><sub>1</sub> = INR 7,500.00 &nbsp;|&nbsp; Year 2: <i>I</i><sub>2</sub> = INR 7,500.00 &nbsp;|&nbsp; Year 3: <i>I</i><sub>3</sub> = INR 7,500.00.<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Total = 3 &times; 7,500 = INR 22,500.00 (verified exact linear accumulation).",
            body_style
        )]
    ]
    t_ex1 = Table(ex1_card, colWidths=[512])
    t_ex1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 0.7, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_ex1)

    # ==================== PAGE 2 ====================
    # Section 4: Worked Example 2 (Complex Day-Count Case)
    story.append(Paragraph("4. Worked Example 2: Fractional Tenors & The Banker's Rule (Hand Solved)", h1_style))
    ex2_card = [
        [Paragraph(
            "<b>Problem:</b> A short-term bridge loan of <i>P</i> = INR 250,000 is issued on <b>March 15</b> at an annual simple interest rate of <i>R</i> = 9.20%, and settled on <b>October 28</b> of the same non-leap year. Compare interest under:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<b>Method A:</b> Exact / Actual/365 Convention (Sovereign bonds) &nbsp;|&nbsp; <b>Method B:</b> Banker's Rule / Actual/360 Convention (Money markets)",
            body_style
        )],
        [Paragraph(
            "<b>Formal Step-by-Step Hand Solution:</b><br/>"
            "&bull; <b>Step 1: Compute Exact Elapsed Days (<i>d</i>):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;March: (31 &minus; 15) = 16 | Apr: 30 | May: 31 | Jun: 30 | Jul: 31 | Aug: 31 | Sep: 30 | Oct: 28.<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<b>Total elapsed days:</b> <i>d</i> = 16 + 30 + 31 + 30 + 31 + 31 + 30 + 28 = <b>227 days</b>.<br/>"
            "&bull; <b>Step 2: Method A (Actual/365 Convention):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Time fraction <i>t</i><sub>365</sub> = 227 / 365 &approx; 0.6219178 years.<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>I</i><sub>365</sub> = 250,000 &times; 0.092 &times; (227 / 365) = 23,000 &times; 0.6219178 = <b>INR 14,304.11</b>.<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Maturity payment: <i>A</i><sub>365</sub> = 250,000 + 14,304.11 = <b>INR 264,304.11</b>.<br/>"
            "&bull; <b>Step 3: Method B (Banker's Rule — Actual/360 Convention):</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Time fraction <i>t</i><sub>360</sub> = 227 / 360 &approx; 0.6305556 years.<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>I</i><sub>360</sub> = 250,000 &times; 0.092 &times; (227 / 360) = 23,000 &times; 0.6305556 = <b>INR 14,502.78</b>.<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;Maturity payment: <i>A</i><sub>360</sub> = 250,000 + 14,502.78 = <b>INR 264,502.78</b>.<br/>"
            "&bull; <b>Yield Discrepancy Analysis:</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&Delta;<i>I</i> = <i>I</i><sub>360</sub> &minus; <i>I</i><sub>365</sub> = 14,502.78 &minus; 14,304.11 = <b>INR 198.67</b> excess interest.<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<i>Mathematical insight:</i> Actual/360 artificially scales the effective interest rate by 365 / 360 &approx; 1.01389 (+1.39% yield boost), illustrating why day-count definitions are contractual prerequisites in fixed-income mathematics.",
            body_style
        )]
    ]
    t_ex2 = Table(ex2_card, colWidths=[512])
    t_ex2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 0.7, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_ex2)
    story.append(Spacer(1, 4))

    # Section 5: Python Implementation
    story.append(Paragraph("5. Algorithmic Implementation in Python", h1_style))
    code_text = (
        "def simple_interest(principal: float, annual_rate: float, time_years: float) -&gt; float:\n"
        "    \"\"\"\n"
        "    Computes accrued simple interest: I = P * r * t.\n"
        "    Enforces domain constraints: principal &gt;= 0, annual_rate &gt;= 0, time_years &gt;= 0.\n"
        "    \"\"\"\n"
        "    if principal &lt; 0 or annual_rate &lt; 0 or time_years &lt; 0:\n"
        "        raise ValueError(\"Financial parameters must be non-negative.\")\n"
        "    return float(principal * annual_rate * time_years)\n\n"
        "def simple_interest_amount(principal: float, annual_rate: float, time_years: float) -&gt; float:\n"
        "    \"\"\"Computes terminal accumulated wealth: A = P * (1 + r * t).\"\"\"\n"
        "    return float(principal + simple_interest(principal, annual_rate, time_years))"
    )
    t_code = Table([[Paragraph(code_text.replace('\n', '<br/>'), code_style)]], colWidths=[512])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_code_bg),
        ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_code)
    story.append(Spacer(1, 4))

    # Section 6: Avishkar Viva Defense
    story.append(Paragraph("6. Avishkar Jury & MSc Admissions Defense Q&A", h1_style))
    qa_rows = [
        [Paragraph("<b>Q1: Why is Simple Interest unsuited for modeling multi-period long-term investments?</b>", qa_q_style)],
        [Paragraph("<b>Defense:</b> Simple interest violates the principle of temporal financial equivalence. In financial mathematics, money received at <i>t</i> = 1 has an opportunity cost; reinvesting that interest should yield further returns. By restricting the growth rate <i>dA</i>/<i>dt</i> = <i>Pr</i> to a constant, simple interest ignores the compounding of reinvested gains, underestimating long-term wealth accumulation exponentially.", qa_a_style)],
        [Paragraph("<b>Q2: Under what conditions does Simple Interest yield more than Compound Interest?</b>", qa_q_style)],
        [Paragraph("<b>Defense:</b> By the strict convexity of the exponential function and Bernoulli's inequality, for any positive rate <i>r</i> &gt; 0 and fractional time period <i>t</i> &in; (0, 1), simple interest accumulation 1 + <i>rt</i> strictly exceeds annual compounding (1 + <i>r</i>)<sup><i>t</i></sup>. They intersect at exactly two points: <i>t</i> = 0 where both equal 1, and <i>t</i> = 1 where both equal 1 + <i>r</i>.", qa_a_style)],
        [Paragraph("<b>Q3: What role does Simple Interest play in institutional Quantitative Finance today?</b>", qa_q_style)],
        [Paragraph("<b>Defense:</b> While rarely used for multi-year retail loans, simple interest remains the global market standard for <i>money market instruments</i> with tenors under one year (e.g., Treasury Bills, Commercial Paper, and Interbank repo rates) governed by exact day-count conventions such as Actual/360 and Actual/365.", qa_a_style)],
    ]
    t_qa = Table(qa_rows, colWidths=[512])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('BOX', (0, 0), (-1, -1), 0.7, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_qa)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Atharv Ranade\Atharv\Avishkar\Financial-Decision-Support-System\theory_and_derivations"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "01_Simple_Interest.pdf")
    create_simple_interest_pdf(out_file)
