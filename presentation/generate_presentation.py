"""
Academic Presentation Generator for College Seminar (Redesigned):
Produces human-crafted, elegant applied mathematics slides:
1. FDSS_Seminar_Presentation.pdf (Widescreen 16:9, LaTeX-style typography, equation callouts)
2. FDSS_Seminar_Presentation.pptx (Widescreen 16:9, native PowerPoint slides, elegant layout)

Design Standards:
- Widescreen 16:9 with generous whitespace and visual breathing room.
- Maximum 3 to 4 crisp, punchy bullet points per slide (each line under 12 words).
- Equations as the visual hero (centered, prominent, LaTeX-typeset style).
- Side-by-side contrast columns and clean booktabs-style tables.
- Palette: Crisp White background (#FFFFFF), Deep Oxford Navy (#0A2540 / #0F2537),
  Subtle Slate (#475569), Clean Border (#E2E8F0).
- Paced strictly for a 7-minute presentation (10 slides max).
"""

import os
import sys
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(OUTPUT_DIR, "FDSS_Seminar_Presentation.pdf")
PPTX_PATH = os.path.join(OUTPUT_DIR, "FDSS_Seminar_Presentation.pptx")

# ==============================================================================
# 1. REPORTLAB 16:9 WIDESCREEN PDF GENERATOR (LATEX-BEAMER AESTHETIC)
# ==============================================================================

SLIDE_WIDTH = 960
SLIDE_HEIGHT = 540

class AcademicSlideCanvas(canvas.Canvas):
    """Two-pass canvas for running header, category banner, and page numbering."""
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
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, total_pages):
        self.saveState()
        
        # Don't draw top banner or footer on Title Slide (Slide 1)
        if self._pageNumber > 1:
            # Minimalist Running Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#0A2540"))  # Deep Oxford Navy
            self.drawString(50, 508, "UNIVERSITY OF MUMBAI  |  DEPARTMENT OF MATHEMATICS & STATISTICS")
            
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))  # Muted Slate
            self.drawRightString(910, 508, "AVISHKAR CATEGORY 3 (PURE SCIENCES)")
            
            # Ultra-clean dividing rule
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(50, 500, 910, 500)
            
            # Bottom Footer
            self.line(50, 34, 910, 34)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(50, 22, "Financial Decision Support System (FDSS)  —  Atharv Ranade")
            self.setFont("Helvetica-Bold", 8)
            self.drawRightString(910, 22, f"{self._pageNumber} / {total_pages}")
            
        self.restoreState()

def get_academic_styles():
    base = getSampleStyleSheet()
    
    styles = {
        'Title_Pill': ParagraphStyle(
            'Title_Pill',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#0284C7"),
            spaceAfter=12
        ),
        'Title_Main': ParagraphStyle(
            'Title_Main',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=28,
            leading=34,
            textColor=colors.HexColor("#0A2540"),
            spaceAfter=8
        ),
        'Title_Sub': ParagraphStyle(
            'Title_Sub',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=14,
            leading=19,
            textColor=colors.HexColor("#334155"),
            spaceAfter=25
        ),
        'Slide_Title': ParagraphStyle(
            'Slide_Title',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0A2540"),
            spaceAfter=4
        ),
        'Slide_Subtitle': ParagraphStyle(
            'Slide_Subtitle',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#475569"),
            spaceAfter=14
        ),
        'Section_Header': ParagraphStyle(
            'Section_Header',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#0A2540"),
            spaceAfter=6
        ),
        'Bullet_Point': ParagraphStyle(
            'Bullet_Point',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#1E293B"),
            spaceAfter=6
        ),
        'Hero_Equation': ParagraphStyle(
            'Hero_Equation',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=18,
            textColor=colors.HexColor("#0A2540"),
            alignment=1
        ),
        'Hero_Equation_Sub': ParagraphStyle(
            'Hero_Equation_Sub',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#475569"),
            alignment=1,
            spaceBefore=3
        ),
        'Callout_Text': ParagraphStyle(
            'Callout_Text',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#0A2540")
        )
    }
    return styles

def make_equation_card(eq_markup, sub_text=None, width=860, bg="#F8FAFC", border="#E2E8F0", pad_v=10):
    content = [Paragraph(eq_markup, get_academic_styles()['Hero_Equation'])]
    if sub_text:
        content.append(Paragraph(sub_text, get_academic_styles()['Hero_Equation_Sub']))
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border)),
        ('TOPPADDING', (0,0), (-1,-1), pad_v),
        ('BOTTOMPADDING', (0,0), (-1,-1), pad_v),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))
    return t

def make_column_card(header, bullets, width=415, bg="#FFFFFF", border="#E2E8F0"):
    st = get_academic_styles()
    content = [Paragraph(header, st['Section_Header']), Spacer(1, 4)]
    for b in bullets:
        content.append(Paragraph(f"&bull;&nbsp;&nbsp;{b}", st['Bullet_Point']))
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border)),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))
    return t

def generate_pdf(pdf_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=(SLIDE_WIDTH, SLIDE_HEIGHT),
        leftMargin=50,
        rightMargin=50,
        topMargin=46,
        bottomMargin=38
    )
    
    st = get_academic_styles()
    story = []
    
    # --------------------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE (Clean Academic LaTeX Minimalist)
    # --------------------------------------------------------------------------
    story.append(Spacer(1, 35))
    story.append(Paragraph("APPLIED MATHEMATICS &amp; COMPUTATIONAL FINANCE SEMINAR", st['Title_Pill']))
    story.append(Paragraph("Financial Decision Support System (FDSS)", st['Title_Main']))
    story.append(Paragraph("A Mathematical &amp; Stochastic Framework for Retail Financial Risk Modeling", st['Title_Sub']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0A2540"), spaceAfter=25))
    
    meta_box = [
        Paragraph("<b>Atharv Ranade</b>  |  Department of Mathematics &amp; Statistics, University of Mumbai", ParagraphStyle('M1', fontName='Helvetica-Bold', fontSize=10.5, leading=15, textColor=colors.HexColor("#0A2540"))),
        Paragraph("<b>Research Category:</b> Pure Sciences (Category 3 — Mathematics &amp; Statistics)<br/><b>Theoretical Focus:</b> Ordinary Differential Equations, Polynomial Root-Finding &amp; Stochastic Calculus", ParagraphStyle('M2', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor("#475569"), spaceBefore=4))
    ]
    t_meta = Table([[meta_box]], colWidths=[860])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 2: THE DETERMINISTIC FALLACY
    # --------------------------------------------------------------------------
    story.append(Paragraph("The Core Problem: Why Retail Calculators Lie", st['Slide_Title']))
    story.append(Paragraph("The dangerous mathematical gap between static expectations and volatile capital markets", st['Slide_Subtitle']))
    
    c1_bullets = [
        "Assumes invariant annual return: <i>A</i>(<i>t</i>) = <i>P</i>(1 + <i>r</i>)<sup><i>t</i></sup>.",
        "Projects lifetime wealth as an unrealistic straight line.",
        "Completely ignores volatility (&sigma; = 0 assumption).",
        "Violates Jensen's Inequality in multi-period compounding."
    ]
    c2_bullets = [
        "Capital markets fluctuate under continuous Brownian motion.",
        "Volatility exerts a structural mathematical drag on returns.",
        "Typical median wealth strictly lags the arithmetic average.",
        "Retail investors experience severe, unexpected shortfalls."
    ]
    
    t_s2 = Table([[make_column_card("Conventional Retail Projection", c1_bullets, width=420, bg="#FFFBEB", border="#FDE68A"),
                   make_column_card("Stochastic Market Reality", c2_bullets, width=420, bg="#F0FDF4", border="#BBF7D0")]], colWidths=[430, 430])
    story.append(t_s2)
    story.append(Spacer(1, 14))
    story.append(make_equation_card(
        "&#120124;[<i>g</i>(<i>X</i>)] &ne; <i>g</i>(&#120124;[<i>X</i>]) &nbsp;&nbsp;&rArr;&nbsp;&nbsp; Deterministic formulas hide downside tail risk.",
        "Jensen's Inequality: Non-linear compounding under variance invalidates simple average calculations.",
        width=860
    ))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 3: HYPOTHESIS & OBJECTIVES
    # --------------------------------------------------------------------------
    story.append(Paragraph("Research Hypothesis & Applied Mathematics Approach", st['Slide_Title']))
    story.append(Paragraph("Grounding retail financial planning in rigorous numerical analysis and probability theory", st['Slide_Subtitle']))
    
    story.append(make_equation_card(
        "<i>\"Replacing static scalar estimates with numerical root-finding and continuous stochastic processes equips investors with true distribution-aware risk modeling.\"</i>",
        "Central Research Hypothesis  |  Department of Mathematics &amp; Statistics, University of Mumbai",
        width=860, bg="#F0F9FF", border="#BAE6FD", pad_v=12
    ))
    story.append(Spacer(1, 14))
    
    p1 = ["Formulate capital accumulation using classical ODEs.", "Derive continuous compounding via Euler limits.", "Expose consumer loan APR illusions with EAR."]
    p2 = ["Overcome polynomial insolvability (Abel–Ruffini).", "Implement Newton–Raphson with analytical derivative.", "Guarantee convergence using Bisection fallback."]
    p3 = ["Model continuous prices via Geometric Brownian Motion.", "Derive volatility drag proof using It&ocirc;'s Lemma.", "Generate 10,000-path Monte Carlo risk distributions."]
    
    t_obj = Table([[
        make_column_card("1. Analytical Theory", p1, width=273),
        make_column_card("2. Numerical Optimization", p2, width=273),
        make_column_card("3. Stochastic Simulation", p3, width=273)
    ]], colWidths=[287, 287, 287])
    story.append(t_obj)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 4: PILLAR 1 - TIME VALUE OF MONEY ODES
    # --------------------------------------------------------------------------
    story.append(Paragraph("Theoretical Pillar 1: Time Value &amp; Governing ODEs", st['Slide_Title']))
    story.append(Paragraph("Linear accumulation versus infinitesimal autonomous growth in continuous time", st['Slide_Subtitle']))
    
    c_lin = [
        "Governing ODE: <i>dA/dt</i> = <i>P &middot; r</i>, &nbsp; with <i>A</i>(0) = <i>P</i>.",
        "Exact solution: <b><i>A</i>(<i>t</i>) = <i>P</i>(1 + <i>rt</i>)</b>.",
        "Linear growth with constant slope (Arithmetic Progression).",
        "Violates subadditivity: <i>A</i>(<i>t</i><sub>1</sub> + <i>t</i><sub>2</sub>) &lt; <i>A</i>(<i>t</i><sub>1</sub>)<i>A</i>(<i>t</i><sub>2</sub>)/<i>P</i>."
    ]
    c_cont = [
        "Governing ODE: <i>dA/dt</i> = <i>r &middot; A</i>(<i>t</i>), &nbsp; with <i>A</i>(0) = <i>P</i>.",
        "Exact solution: <b><i>A</i>(<i>t</i>) = <i>P e</i><sup><i>rt</i></sup></b>.",
        "Growth rate is directly proportional to accumulated wealth.",
        "Infinitesimal Euler limit: lim<sub><i>m</i>&rarr;&infin;</sub> (1 + <i>r/m</i>)<sup><i>mt</i></sup> = <i>e</i><sup><i>rt</i></sup>."
    ]
    
    t_p1 = Table([[make_column_card("Simple Accumulation (Linear ODE)", c_lin, width=420),
                   make_column_card("Continuous Compounding (Autonomous ODE)", c_cont, width=420)]], colWidths=[430, 430])
    story.append(t_p1)
    story.append(Spacer(1, 14))
    story.append(make_equation_card(
        "EAR = (1 + <i>r</i><sub>nom</sub>/<i>m</i>)<sup><i>m</i></sup> &minus; 1 &nbsp;&nbsp;&bull;&nbsp;&nbsp; <i>r</i><sub><i>c</i></sub> = <i>m</i> &middot; ln(1 + <i>r</i><sub><i>d</i></sub>/<i>m</i>)",
        "Key Insight: Continuously compounded logarithmic returns add linearly across time periods.",
        width=860
    ))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 5: PILLAR 2 - CONSUMER DEBT & NEGATIVE AMORTIZATION
    # --------------------------------------------------------------------------
    story.append(Paragraph("Theoretical Pillar 2: Consumer Debt Analytics", st['Slide_Title']))
    story.append(Paragraph("Finite geometric series summation and the negative amortization boundary theorem", st['Slide_Subtitle']))
    
    story.append(make_equation_card(
        "<i>P</i> = &sum;<sub><i>k</i>=1</sub><sup><i>n</i></sup> <i>E</i>(1 + <i>R</i>)<sup>&minus;<i>k</i></sup> &nbsp;&nbsp;&rArr;&nbsp;&nbsp; <b><i>E</i> = <i>P &middot; R</i> &middot; (1 + <i>R</i>)<sup><i>n</i></sup> / [ (1 + <i>R</i>)<sup><i>n</i></sup> &minus; 1 ]</b>",
        "Equated Monthly Installment (EMI) derived via closed-form inversion of a finite geometric progression (<i>R</i> = <i>r</i>/12).",
        width=860
    ))
    story.append(Spacer(1, 14))
    
    c_debt1 = [
        "Monthly interest: <i>I</i><sub><i>k</i></sub> = <i>B</i><sub><i>k</i>&minus;1</sub> &middot; <i>R</i>.",
        "Principal repaid: <i>P</i><sub><i>k</i></sub> = <i>E</i> &minus; <i>I</i><sub><i>k</i></sub>.",
        "Principal sequence forms an increasing geometric progression.",
        "Early prepayments collapse total interest exponentially."
    ]
    c_debt2 = [
        "Boundary condition: Loan amortizes &hArr; <b><i>E</i> &gt; <i>P &middot; r</i> / 12</b>.",
        "If <i>E</i> &le; <i>P &middot; R</i>, principal repaid is zero or negative.",
        "Debt balance diverges to infinity: lim<sub><i>n</i>&rarr;&infin;</sub> <i>B</i><sub><i>n</i></sub> = +&infin;.",
        "Exposes predatory 'minimum payment' credit card traps."
    ]
    
    t_p2 = Table([[make_column_card("Amortization Dynamics", c_debt1, width=420),
                   make_column_card("Negative Amortization Boundary", c_debt2, width=420, bg="#FEF2F2", border="#FECACA")]], colWidths=[430, 430])
    story.append(t_p2)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 6: PILLAR 3 - NUMERICAL ROOT-FINDING (IRR)
    # --------------------------------------------------------------------------
    story.append(Paragraph("Theoretical Pillar 3: Numerical Yield Optimization", st['Slide_Title']))
    story.append(Paragraph("Why Galois theory mandates numerical analysis for multi-period financial yields", st['Slide_Subtitle']))
    
    story.append(make_equation_card(
        "NPV(<i>r</i>) = &sum;<sub><i>t</i>=0</sub><sup><i>T</i></sup> <i>C</i><sub><i>t</i></sub> / (1 + <i>r</i>)<sup><i>t</i></sup> = 0 &nbsp;&nbsp;&hArr;&nbsp;&nbsp; &sum;<sub><i>t</i>=0</sub><sup><i>T</i></sup> <i>C</i><sub><i>t</i></sub> <i>x</i><sup><i>t</i></sup> = 0 &nbsp; (<i>x</i> = (1+<i>r</i>)<sup>&minus;1</sup>)",
        "The Internal Rate of Return (IRR) polynomial of degree <i>T</i>.",
        width=860
    ))
    story.append(Spacer(1, 14))
    
    c_irr1 = [
        "<b>The Abel–Ruffini Theorem (Galois Theory):</b>",
        "No general radical solution exists for degree <i>T</i> &ge; 5.",
        "Multi-period financial cash flows cannot be solved algebraically.",
        "Numerical analysis is fundamentally mathematically mandatory."
    ]
    c_irr2 = [
        "<b>Newton–Raphson with Analytical Derivative:</b>",
        "Iteration: <i>r</i><sub><i>k</i>+1</sub> = <i>r</i><sub><i>k</i></sub> &minus; [ NPV(<i>r</i><sub><i>k</i></sub>) / <i>f'</i>(<i>r</i><sub><i>k</i></sub>) ].",
        "Quadratic convergence rate: error squares at each step |<i>e</i><sub><i>k</i>+1</sub>| &le; <i>M</i> |<i>e</i><sub><i>k</i></sub>|<sup>2</sup>.",
        "Bisection fallback guarantees convergence if derivatives oscillate."
    ]
    
    t_p3 = Table([[make_column_card("Mathematical Insolvability", c_irr1, width=420),
                   make_column_card("Dual-Engine Numerical Solver", c_irr2, width=420)]], colWidths=[430, 430])
    story.append(t_p3)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 7: PILLAR 4 - STOCHASTIC DYNAMICS & ITÔ'S LEMMA
    # --------------------------------------------------------------------------
    story.append(Paragraph("Theoretical Pillar 4: Stochastic Asset Dynamics", st['Slide_Title']))
    story.append(Paragraph("Continuous-time Brownian motion and the mathematical proof of volatility drag", st['Slide_Subtitle']))
    
    story.append(make_equation_card(
        "<i>dS</i><sub><i>t</i></sub> = &mu; <i>S</i><sub><i>t</i></sub> <i>dt</i> + &sigma; <i>S</i><sub><i>t</i></sub> <i>dW</i><sub><i>t</i></sub> &nbsp;&nbsp;&rArr;&nbsp;&nbsp; <b><i>d</i>(ln <i>S</i><sub><i>t</i></sub>) = (&mu; &minus; &frac12;&sigma;<sup>2</sup>) <i>dt</i> + &sigma; <i>dW</i><sub><i>t</i></sub></b>",
        "It&ocirc;'s Lemma Proof: Non-zero quadratic variation (<i>dW</i><sub><i>t</i></sub>)<sup>2</sup> = <i>dt</i> creates structural drag &minus;&frac12;&sigma;<sup>2</sup>.",
        width=860
    ))
    story.append(Spacer(1, 14))
    
    c_g1 = [
        "In standard calculus, <i>d</i>(ln <i>S</i>) = <i>dS</i>/<i>S</i>.",
        "Brownian motion has non-zero variation: (<i>dW</i>)<sup>2</sup> = <i>dt</i>.",
        "It&ocirc; Taylor expansion includes second derivative: <i>f''</i>(<i>S</i>) = &minus;1/<i>S</i><sup>2</sup>.",
        "Generates exact discrete solution: <i>S</i><sub><i>t</i></sub> = <i>S</i><sub>0</sub> exp[(&mu;&minus;&frac12;&sigma;<sup>2</sup>)<i>t</i> + &sigma;<i>W</i><sub><i>t</i></sub>]."
    ]
    c_g2 = [
        "Arithmetic Mean: &#120124;[<i>S</i><sub><i>t</i></sub>] = <i>S</i><sub>0</sub> <i>e</i><sup>&mu;<i>t</i></sup> (pulled by right skew).",
        "Typical Median: <i>S</i><sub>med</sub>(<i>t</i>) = <i>S</i><sub>0</sub> <i>e</i><sup>(&mu; &minus; &frac12;&sigma;<sup>2</sup>)<i>t</i></sup>.",
        "Volatility Drag penalty: &Delta;&mu; = &minus;&frac12;&sigma;<sup>2</sup> per year.",
        "More than 50% of investors strictly underperform advertised average!"
    ]
    
    t_p4 = Table([[make_column_card("It&ocirc;'s Stochastic Calculus", c_g1, width=420),
                   make_column_card("The Volatility Drag Divergence", c_g2, width=420)]], colWidths=[430, 430])
    story.append(t_p4)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 8: PILLAR 5 - MONTE CARLO & RISK ESTIMATION
    # --------------------------------------------------------------------------
    story.append(Paragraph("Theoretical Pillar 5: Monte Carlo Simulation &amp; Risk", st['Slide_Title']))
    story.append(Paragraph("Vectorized stochastic ensembles, Central Limit Theorem bounds, and Value at Risk", st['Slide_Subtitle']))
    
    story.append(make_equation_card(
        "Standard Error = &sigma;<sub>sample</sub> / &radic;<i>M</i> = &#119978;(1 / &radic;<i>M</i>) &nbsp;&nbsp;&bull;&nbsp;&nbsp; <b>P&#770;(<i>S</i><sub><i>T</i></sub> &ge; Goal) = (1 / <i>M</i>) &sum; &#120793;<sub>{<i>S</i><sub><i>T</i></sub> &ge; Goal}</sub></b>",
        "Central Limit Theorem ensures convergence precision narrows to &plusmn;1% across <i>M</i> = 10,000 simulated paths.",
        width=860
    ))
    story.append(Spacer(1, 14))
    
    c_mc1 = [
        "Vectorized simulation of 10,000+ paths in NumPy.",
        "SLLN: sample mean converges almost surely to true expectation.",
        "Yields complete empirical probability density function.",
        "Replaces blind single-point estimates with full distribution."
    ]
    c_mc2 = [
        "<b>Goal Attainment Probability:</b> exact odds of hitting target.",
        "<b>Value at Risk (VaR 95%):</b> maximum loss at 95% confidence.",
        "<b>Conditional VaR (CVaR):</b> expected loss in worst 5% tail.",
        "Democratizes institutional hedge-fund risk metrics."
    ]
    
    t_p5 = Table([[make_column_card("Ensemble Convergence", c_mc1, width=420),
                   make_column_card("Downside Tail Risk Metrics", c_mc2, width=420)]], colWidths=[430, 430])
    story.append(t_p5)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 9: ARCHITECTURE & VERIFICATION
    # --------------------------------------------------------------------------
    story.append(Paragraph("System Architecture &amp; Mathematical Verification", st['Slide_Title']))
    story.append(Paragraph("Zero-black-box design, modular computation pipeline, and strict floating-point validation", st['Slide_Subtitle']))
    
    c_arch = [
        "<b>Mathematical Engine (<code>models/</code>):</b> pure functional routines.",
        "<b>Verification Suite (<code>tests/</code>):</b> automated pytest validation.",
        "<b>Interactive UI (<code>app.py</code>):</b> Streamlit parameters &amp; charts.",
        "<b>Zero Black Boxes:</b> every algorithm derived from first principles."
    ]
    c_ver = [
        "<b>Excel Parity:</b> verified against PMT, PV, IRR to &epsilon; &le; 10<sup>&minus;7</sup>.",
        "<b>Boundary Tests:</b> verified at limits <i>r</i> &rarr; 0, <i>t</i> &rarr; 0, and <i>m</i> &rarr; &infin;.",
        "<b>Domain Guardrails:</b> strict <code>ValueError</code> on invalid inputs.",
        "<b>Analytical Benchmarks:</b> validated against 24 hand-solved cases."
    ]
    
    t_p6 = Table([[make_column_card("Three-Tier Architecture", c_arch, width=420),
                   make_column_card("Verification Methodology", c_ver, width=420)]], colWidths=[430, 430])
    story.append(t_p6)
    story.append(Spacer(1, 14))
    story.append(make_equation_card(
        "| Computer Estimate &minus; Analytical Truth | &le; 10<sup>&minus;7</sup> &nbsp;&nbsp;&bull;&nbsp;&nbsp; Automated Pytest Suite Passing",
        "Mathematical reproducibility standard: rigorous verification across all parameter boundaries.",
        width=860
    ))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 10: CONCLUSION & IMPACT
    # --------------------------------------------------------------------------
    story.append(Paragraph("Academic Contributions &amp; Societal Impact", st['Slide_Title']))
    story.append(Paragraph("Completed milestones, consumer protection relevance, and open-source availability", st['Slide_Subtitle']))
    
    c_conc1 = [
        "<b>12-Volume Reference Monograph (56 Pages):</b>",
        "Complete mathematical derivations compiled in <code>theory_and_derivations/</code>.",
        "Covers discrete accumulation to It&ocirc; calculus and Monte Carlo.",
        "Includes 24 step-by-step hand-calculated case studies."
    ]
    c_conc2 = [
        "<b>Real-World Societal Benefits:</b>",
        "Prevents retail citizens from falling into predatory debt traps.",
        "Eliminates optimistic return illusions via volatility drag modeling.",
        "Open-source on GitHub under MIT License for public verification."
    ]
    
    t_p7 = Table([[make_column_card("Completed Research Milestones", c_conc1, width=420),
                   make_column_card("Consumer Protection Impact", c_conc2, width=420)]], colWidths=[430, 430])
    story.append(t_p7)
    story.append(Spacer(1, 14))
    
    thx_content = [
        Paragraph("<b>Thank You!</b> &nbsp;&nbsp;|&nbsp;&nbsp; Open for Questions &amp; Mathematical Defense", ParagraphStyle('Thx1', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor("#0A2540"), alignment=1)),
        Paragraph("Atharv Ranade &nbsp;&bull;&nbsp; Department of Mathematics &amp; Statistics &nbsp;&bull;&nbsp; University of Mumbai", ParagraphStyle('Thx2', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor("#64748B"), alignment=1, spaceBefore=3))
    ]
    t_thx = Table([[thx_content]], colWidths=[860])
    t_thx.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F9FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BAE6FD")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_thx)
    
    doc.build(story, canvasmaker=AcademicSlideCanvas)
    print(f"Generated Elegant PDF: {pdf_path}")

# ==============================================================================
# 2. PYTHON-PPTX 16:9 WIDESCREEN GENERATOR (LATEX-BEAMER AESTHETIC)
# ==============================================================================

def add_clean_header(slide, title_text, subtitle_text):
    # Category subtle pill
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.25))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = "UNIVERSITY OF MUMBAI  |  DEPARTMENT OF MATHEMATICS & STATISTICS  |  AVISHKAR CATEGORY 3"
    p_c.font.size = Pt(8.5)
    p_c.font.bold = True
    p_c.font.color.rgb = RGBColor(2, 132, 199)  # Light Blue
    
    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.733), Inches(0.55))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = RGBColor(10, 37, 64)  # Deep Oxford Navy
    
    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.733), Inches(0.35))
    tf_s = sub_box.text_frame
    tf_s.word_wrap = True
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle_text
    p_s.font.size = Pt(11)
    p_s.font.color.rgb = RGBColor(71, 85, 105)  # Muted Slate

def add_clean_card(slide, left, top, width, height, title, bullet_points, bg_rgb=(255, 255, 255), border_rgb=(226, 232, 240)):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*bg_rgb)
    shape.line.color.rgb = RGBColor(*border_rgb)
    shape.line.width = Pt(1)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    tf.margin_bottom = Inches(0.25)
    
    # Header
    p_head = tf.paragraphs[0]
    p_head.text = title
    p_head.font.size = Pt(13)
    p_head.font.bold = True
    p_head.font.color.rgb = RGBColor(10, 37, 64)
    p_head.space_after = Pt(10)
    
    for bp in bullet_points:
        p = tf.add_paragraph()
        p.text = "•  " + bp
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(30, 41, 59)
        p.space_after = Pt(8)

def add_hero_equation(slide, left, top, width, height, formula_text, sub_text, bg_rgb=(248, 250, 252), border_rgb=(226, 232, 240)):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*bg_rgb)
    shape.line.color.rgb = RGBColor(*border_rgb)
    shape.line.width = Pt(1)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.15)
    tf.margin_bottom = Inches(0.15)
    
    p = tf.paragraphs[0]
    p.text = formula_text
    p.font.size = Pt(13.5)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = RGBColor(10, 37, 64)
    
    p2 = tf.add_paragraph()
    p2.text = sub_text
    p2.font.size = Pt(9.5)
    p2.alignment = PP_ALIGN.CENTER
    p2.font.color.rgb = RGBColor(71, 85, 105)
    p2.space_before = Pt(3)

def generate_pptx(pptx_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # --------------------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # --------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "APPLIED MATHEMATICS & COMPUTATIONAL FINANCE SEMINAR"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(2, 132, 199)
    p.space_after = Pt(12)
    
    p = tf.add_paragraph()
    p.text = "Financial Decision Support System (FDSS)"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(10, 37, 64)
    p.space_after = Pt(8)
    
    p = tf.add_paragraph()
    p.text = "A Mathematical & Stochastic Framework for Retail Financial Risk Modeling"
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(51, 65, 85)
    p.space_after = Pt(35)
    
    p = tf.add_paragraph()
    p.text = "Atharv Ranade  |  Department of Mathematics & Statistics, University of Mumbai"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(10, 37, 64)
    p.space_after = Pt(5)
    
    p = tf.add_paragraph()
    p.text = "Research Category: Pure Sciences (Category 3 — Mathematics & Statistics)  •  Avishkar Research Convention"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(100, 116, 139)

    # --------------------------------------------------------------------------
    # SLIDE 2: THE DETERMINISTIC FALLACY
    # --------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_clean_header(s2, "The Core Problem: Why Retail Calculators Lie", "The dangerous mathematical gap between static expectations and volatile capital markets")
    add_clean_card(s2, 0.8, 1.8, 5.7, 3.8, "Conventional Retail Projection", [
        "Assumes invariant annual return: A(t) = P(1 + r)^t.",
        "Projects lifetime wealth as an unrealistic straight line.",
        "Completely ignores volatility (sigma = 0 assumption).",
        "Violates Jensen's Inequality in multi-period compounding."
    ], bg_rgb=(255, 251, 235), border_rgb=(253, 230, 138))
    add_clean_card(s2, 6.8, 1.8, 5.7, 3.8, "Stochastic Market Reality", [
        "Capital markets fluctuate under continuous Brownian motion.",
        "Volatility exerts a structural mathematical drag on returns.",
        "Typical median wealth strictly lags the arithmetic average.",
        "Retail investors experience severe, unexpected shortfalls."
    ], bg_rgb=(240, 253, 244), border_rgb=(187, 247, 208))
    add_hero_equation(s2, 0.8, 5.85, 11.7, 1.15,
                      "E[g(X)] != g(E[X])   ==>   Deterministic formulas hide downside tail risk.",
                      "Jensen's Inequality: Non-linear compounding under variance invalidates simple average projections.")

    # --------------------------------------------------------------------------
    # SLIDE 3: HYPOTHESIS & OBJECTIVES
    # --------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_clean_header(s3, "Research Hypothesis & Applied Mathematics Approach", "Grounding retail financial planning in rigorous numerical analysis and probability theory")
    add_hero_equation(s3, 0.8, 1.8, 11.7, 1.3,
                      "\"Replacing static scalar estimates with numerical root-finding and continuous stochastic processes equips investors with true distribution-aware risk modeling.\"",
                      "Central Research Hypothesis  |  Department of Mathematics & Statistics, University of Mumbai",
                      bg_rgb=(240, 249, 255), border_rgb=(186, 230, 253))
    add_clean_card(s3, 0.8, 3.35, 3.7, 3.65, "1. Analytical Theory", [
        "Formulate capital accumulation using classical ODEs.",
        "Derive continuous compounding via Euler limits.",
        "Expose consumer loan APR illusions with EAR."
    ])
    add_clean_card(s3, 4.8, 3.35, 3.7, 3.65, "2. Numerical Optimization", [
        "Overcome polynomial insolvability (Abel-Ruffini).",
        "Implement Newton-Raphson with analytical derivative.",
        "Guarantee convergence using Bisection fallback."
    ])
    add_clean_card(s3, 8.8, 3.35, 3.7, 3.65, "3. Stochastic Simulation", [
        "Model continuous prices via Geometric Brownian Motion.",
        "Derive volatility drag proof using Itô's Lemma.",
        "Generate 10,000-path Monte Carlo risk distributions."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 4: PILLAR 1 - TIME VALUE ODES
    # --------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_clean_header(s4, "Theoretical Pillar 1: Time Value & Governing ODEs", "Linear accumulation versus infinitesimal autonomous growth in continuous time")
    add_clean_card(s4, 0.8, 1.8, 5.7, 3.8, "Simple Accumulation (Linear ODE)", [
        "Governing ODE: dA/dt = P * r, with A(0) = P.",
        "Exact solution: A(t) = P(1 + r*t).",
        "Linear growth with constant slope (Arithmetic Progression).",
        "Violates subadditivity: A(t1 + t2) < A(t1)*A(t2)/P."
    ])
    add_clean_card(s4, 6.8, 1.8, 5.7, 3.8, "Continuous Compounding (Autonomous ODE)", [
        "Governing ODE: dA/dt = r * A(t), with A(0) = P.",
        "Exact solution: A(t) = P * e^(rt).",
        "Growth rate is directly proportional to accumulated wealth.",
        "Infinitesimal Euler limit: lim (1 + r/m)^(mt) = e^(rt)."
    ])
    add_hero_equation(s4, 0.8, 5.85, 11.7, 1.15,
                      "EAR = (1 + r_nom / m)^m - 1      •      r_c = m * ln(1 + r_d / m)",
                      "Key Mathematical Insight: Continuously compounded logarithmic returns add linearly across time periods.")

    # --------------------------------------------------------------------------
    # SLIDE 5: PILLAR 2 - CONSUMER DEBT & NEGATIVE AMORTIZATION
    # --------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_clean_header(s5, "Theoretical Pillar 2: Consumer Debt Analytics", "Finite geometric series summation and the negative amortization boundary theorem")
    add_hero_equation(s5, 0.8, 1.8, 11.7, 1.25,
                      "P = sum [ E * (1 + R)^(-k) ]   ==>   E = P * R * (1 + R)^n / [ (1 + R)^n - 1 ]",
                      "Equated Monthly Installment (EMI) derived via closed-form inversion of a finite geometric progression (R = r/12).")
    add_clean_card(s5, 0.8, 3.3, 5.7, 3.7, "Amortization Dynamics", [
        "Monthly interest: Ik = B_{k-1} * R.",
        "Principal repaid: Pk = E - Ik.",
        "Principal sequence forms an increasing geometric progression.",
        "Early prepayments collapse total interest exponentially."
    ])
    add_clean_card(s5, 6.8, 3.3, 5.7, 3.7, "Negative Amortization Boundary", [
        "Boundary condition: Loan amortizes <=> E > P * r / 12.",
        "If E <= P * R, principal repaid is zero or negative.",
        "Debt balance diverges to infinity: lim Bn = +infinity.",
        "Exposes predatory 'minimum payment' credit card traps."
    ], bg_rgb=(254, 242, 242), border_rgb=(254, 202, 202))

    # --------------------------------------------------------------------------
    # SLIDE 6: PILLAR 3 - NUMERICAL ROOT-FINDING (IRR)
    # --------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_clean_header(s6, "Theoretical Pillar 3: Numerical Yield Optimization", "Why Galois theory mandates numerical analysis for multi-period financial yields")
    add_hero_equation(s6, 0.8, 1.8, 11.7, 1.25,
                      "NPV(r) = sum [ Ct / (1 + r)^t ] = 0   <=>   sum [ Ct * x^t ] = 0   (x = 1 / (1 + r))",
                      "The Internal Rate of Return (IRR) polynomial of degree T.")
    add_clean_card(s6, 0.8, 3.3, 5.7, 3.7, "Mathematical Insolvability", [
        "The Abel-Ruffini Theorem (Galois Theory):",
        "No general radical solution exists for degree T >= 5.",
        "Multi-period financial cash flows cannot be solved algebraically.",
        "Numerical analysis is fundamentally mathematically mandatory."
    ])
    add_clean_card(s6, 6.8, 3.3, 5.7, 3.7, "Dual-Engine Numerical Solver", [
        "Newton-Raphson with Analytical Derivative:",
        "Iteration: r_{k+1} = r_k - [ NPV(r_k) / f'(r_k) ].",
        "Quadratic convergence rate: error squares at each step |e_{k+1}| <= M |e_k|^2.",
        "Bisection fallback guarantees convergence if derivatives oscillate."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 7: PILLAR 4 - STOCHASTIC ASSET DYNAMICS & ITÔ'S LEMMA
    # --------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_clean_header(s7, "Theoretical Pillar 4: Stochastic Asset Dynamics", "Continuous-time Brownian motion and the mathematical proof of volatility drag")
    add_hero_equation(s7, 0.8, 1.8, 11.7, 1.25,
                      "dS = mu * S * dt + sigma * S * dW   ==>   d(ln S) = (mu - 0.5 * sigma^2) dt + sigma * dW",
                      "Itô's Lemma Proof: Non-zero quadratic variation (dW)^2 = dt creates structural drag -0.5 * sigma^2.")
    add_clean_card(s7, 0.8, 3.3, 5.7, 3.7, "Itô's Stochastic Calculus", [
        "In standard calculus, d(ln S) = dS / S.",
        "Brownian motion has non-zero variation: (dW)^2 = dt.",
        "Itô Taylor expansion includes second derivative: f''(S) = -1/S^2.",
        "Generates exact discrete solution: St = S0 * exp[(mu - 0.5*sigma^2)t + sigma*Wt]."
    ])
    add_clean_card(s7, 6.8, 3.3, 5.7, 3.7, "The Volatility Drag Divergence", [
        "Arithmetic Mean: E[St] = S0 * e^(mu*t) (pulled by right skew).",
        "Typical Median: S_med(t) = S0 * e^[(mu - 0.5*sigma^2)t].",
        "Volatility Drag penalty: Delta mu = -0.5 * sigma^2 per year.",
        "More than 50% of investors strictly underperform advertised average!"
    ])

    # --------------------------------------------------------------------------
    # SLIDE 8: PILLAR 5 - MONTE CARLO & RISK ESTIMATION
    # --------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_clean_header(s8, "Theoretical Pillar 5: Monte Carlo Simulation & Risk", "Vectorized stochastic ensembles, Central Limit Theorem bounds, and Value at Risk")
    add_hero_equation(s8, 0.8, 1.8, 11.7, 1.25,
                      "Standard Error = sigma_sample / sqrt(M) = O(1 / sqrt(M))   •   P_hat(ST >= Goal) = (1/M) * sum [ 1_{ST >= Goal} ]",
                      "Central Limit Theorem ensures convergence precision narrows to +/-1% across M = 10,000 simulated paths.")
    add_clean_card(s8, 0.8, 3.3, 5.7, 3.7, "Ensemble Convergence", [
        "Vectorized simulation of 10,000+ paths in NumPy.",
        "SLLN: sample mean converges almost surely to true expectation.",
        "Yields complete empirical probability density function.",
        "Replaces blind single-point estimates with full distribution."
    ])
    add_clean_card(s8, 6.8, 3.3, 5.7, 3.7, "Downside Tail Risk Metrics", [
        "Goal Attainment Probability: exact odds of hitting target.",
        "Value at Risk (VaR 95%): maximum loss at 95% confidence.",
        "Conditional VaR (CVaR): expected loss in worst 5% tail.",
        "Democratizes institutional hedge-fund risk metrics."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 9: ARCHITECTURE & VERIFICATION
    # --------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_clean_header(s9, "System Architecture & Mathematical Verification", "Zero-black-box design, modular computation pipeline, and strict floating-point validation")
    add_clean_card(s9, 0.8, 1.8, 5.7, 3.8, "Three-Tier Architecture", [
        "Mathematical Engine (models/): pure functional routines.",
        "Verification Suite (tests/): automated pytest validation.",
        "Interactive UI (app.py): Streamlit parameters & charts.",
        "Zero Black Boxes: every algorithm derived from first principles."
    ])
    add_clean_card(s9, 6.8, 1.8, 5.7, 3.8, "Verification Methodology", [
        "Excel Parity: verified against PMT, PV, IRR to epsilon <= 10^-7.",
        "Boundary Tests: verified at limits r -> 0, t -> 0, and m -> infinity.",
        "Domain Guardrails: strict ValueError on invalid inputs.",
        "Analytical Benchmarks: validated against 24 hand-solved cases."
    ])
    add_hero_equation(s9, 0.8, 5.85, 11.7, 1.15,
                      "| Computer Estimate - Analytical Truth | <= 10^-7   •   Automated Pytest Suite Passing",
                      "Mathematical reproducibility standard: rigorous verification across all parameter boundaries.")

    # --------------------------------------------------------------------------
    # SLIDE 10: CONCLUSION & IMPACT
    # --------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_clean_header(s10, "Academic Contributions & Societal Impact", "Completed milestones, consumer protection relevance, and open-source availability")
    add_clean_card(s10, 0.8, 1.8, 5.7, 3.8, "Completed Research Milestones", [
        "12-Volume Reference Monograph (56 Pages):",
        "Complete mathematical derivations compiled in theory_and_derivations/.",
        "Covers discrete accumulation to Itô calculus and Monte Carlo.",
        "Includes 24 step-by-step hand-calculated case studies."
    ])
    add_clean_card(s10, 6.8, 1.8, 5.7, 3.8, "Consumer Protection Impact", [
        "Real-World Societal Benefits:",
        "Prevents retail citizens from falling into predatory debt traps.",
        "Eliminates optimistic return illusions via volatility drag modeling.",
        "Open-source on GitHub under MIT License for public verification."
    ])
    add_hero_equation(s10, 0.8, 5.85, 11.7, 1.15,
                      "Thank You!   |   Open for Questions & Mathematical Defense",
                      "Atharv Ranade  •  Department of Mathematics & Statistics  •  University of Mumbai",
                      bg_rgb=(240, 249, 255), border_rgb=(186, 230, 253))

    prs.save(pptx_path)
    print(f"Generated Elegant PPTX: {pptx_path}")

if __name__ == "__main__":
    generate_pdf(PDF_PATH)
    generate_pptx(PPTX_PATH)
