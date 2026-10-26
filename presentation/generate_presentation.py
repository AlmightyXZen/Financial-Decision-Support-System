"""
Presentation Generator for College Seminar:
Produces both:
1. FDSS_Seminar_Presentation.pdf (Widescreen 16:9, vector text & mathematical formulas)
2. FDSS_Seminar_Presentation.pptx (Widescreen 16:9, native PowerPoint slides)

Strictly adhering to:
- 10 slides paced for a 7-minute presentation
- High-contrast academic typography (Deep Navy #1E3A8A, Charcoal #0F172A)
- Zero hardcoded dates
- Pure Sciences & Applied Mathematics orientation (Avishkar Category 3)
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
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(OUTPUT_DIR, "FDSS_Seminar_Presentation.pdf")
PPTX_PATH = os.path.join(OUTPUT_DIR, "FDSS_Seminar_Presentation.pptx")

# ==============================================================================
# 1. REPORTLAB 16:9 WIDESCREEN PDF GENERATOR
# ==============================================================================

# 16:9 dimensions in points: 960 x 540 pt (13.333 x 7.5 inches)
SLIDE_WIDTH = 960
SLIDE_HEIGHT = 540

class WidescreenSlideCanvas(canvas.Canvas):
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
            # Top Banner
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1E3A8A"))  # Deep Navy
            self.drawString(45, 510, "UNIVERSITY OF MUMBAI  •  DEPARTMENT OF MATHEMATICS & STATISTICS")
            
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#475569"))  # Slate
            self.drawRightString(915, 510, "RESEARCH SEMINAR  |  AVISHKAR CATEGORY 3 (PURE SCIENCES)")
            
            # Dividing Rule under header
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.8)
            self.line(45, 502, 915, 502)
            
            # Bottom Footer Rule
            self.line(45, 32, 915, 32)
            
            # Bottom Footer Text
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(45, 20, "Financial Decision Support System (FDSS) — Atharv Ranade")
            self.setFont("Helvetica-Bold", 8)
            self.drawRightString(915, 20, f"Slide {self._pageNumber} of {total_pages}")
            
        self.restoreState()

def get_slide_styles():
    base = getSampleStyleSheet()
    
    styles = {
        'Title_Main': ParagraphStyle(
            'Title_Main',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=26,
            leading=32,
            textColor=colors.HexColor("#1E3A8A"),
            alignment=0,
            spaceAfter=6
        ),
        'Title_Sub': ParagraphStyle(
            'Title_Sub',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=13,
            leading=18,
            textColor=colors.HexColor("#0F172A"),
            alignment=0,
            spaceAfter=15
        ),
        'Slide_Header': ParagraphStyle(
            'Slide_Header',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=19,
            leading=23,
            textColor=colors.HexColor("#1E3A8A"),
            spaceAfter=3
        ),
        'Slide_Subheader': ParagraphStyle(
            'Slide_Subheader',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#0284C7"),
            spaceAfter=12
        ),
        'Card_Title': ParagraphStyle(
            'Card_Title',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#1E3A8A"),
            spaceAfter=3
        ),
        'Card_Body': ParagraphStyle(
            'Card_Body',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=11.5,
            textColor=colors.HexColor("#0F172A")
        ),
        'Equation_Box': ParagraphStyle(
            'Equation_Box',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#0F172A"),
            alignment=1
        ),
        'Meta_Label': ParagraphStyle(
            'Meta_Label',
            parent=base['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#1E3A8A")
        ),
        'Meta_Val': ParagraphStyle(
            'Meta_Val',
            parent=base['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#0F172A")
        )
    }
    return styles

def make_slide_card(content_list, width=420, bg="#F8FAFC", border="#CBD5E1", pad=8):
    t = Table([[content_list]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg)),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor(border)),
        ('TOPPADDING', (0,0), (-1,-1), pad),
        ('BOTTOMPADDING', (0,0), (-1,-1), pad),
        ('LEFTPADDING', (0,0), (-1,-1), pad),
        ('RIGHTPADDING', (0,0), (-1,-1), pad),
    ]))
    return t

def generate_pdf(pdf_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=(SLIDE_WIDTH, SLIDE_HEIGHT),
        leftMargin=45,
        rightMargin=45,
        topMargin=46,
        bottomMargin=38
    )
    
    st = get_slide_styles()
    story = []
    
    # --------------------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # --------------------------------------------------------------------------
    story.append(Spacer(1, 20))
    story.append(Paragraph("RESEARCH SEMINAR  •  APPLIED MATHEMATICAL FINANCE", ParagraphStyle('Pill', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#0284C7"), spaceAfter=8)))
    story.append(Paragraph("Financial Decision Support System (FDSS)", st['Title_Main']))
    story.append(Paragraph("A Mathematical & Stochastic Framework for Retail Financial Risk Modeling", st['Title_Sub']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceAfter=20))
    
    info_table_data = [
        [
            Paragraph("<b>Investigator:</b> Atharv Ranade<br/><b>Department:</b> Department of Mathematics & Statistics<br/><b>Affiliation:</b> University of Mumbai", st['Card_Body']),
            Paragraph("<b>Research Category:</b> Category 3: Pure Sciences (Mathematics & Statistics)<br/><b>Focus:</b> Numerical Root-Finding & Stochastic Calculus (GBM)<br/><b>Repository:</b> github.com/AlmightyXZen/Financial-Decision-Support-System", st['Card_Body'])
        ]
    ]
    t_info = Table(info_table_data, colWidths=[420, 440])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(t_info)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 2: THE DETERMINISTIC FALLACY
    # --------------------------------------------------------------------------
    story.append(Paragraph("1. The Research Problem: The Deterministic Fallacy", st['Slide_Header']))
    story.append(Paragraph("Why conventional retail financial calculators are mathematically flawed and mislead the public", st['Slide_Subheader']))
    
    c1 = [
        Paragraph("<b>The Deterministic Expectation Assumption</b>", st['Card_Title']),
        Paragraph("• Commercial calculators project future wealth using single-point linear formulas: <i>A</i> = <i>P</i>(1 + <i>r</i>)<sup><i>t</i></sup>.<br/>"
                  "• They assume an invariant constant rate of return (e.g., exactly 12.00% every single year for 20 years).<br/>"
                  "• <b>The Flaw:</b> Real capital markets do not follow deterministic lines; they are governed by stochastic Brownian motion with non-zero variance &sigma;<sup>2</sup> &gt; 0.", st['Card_Body']),
        Spacer(1, 4),
        Paragraph("<b>Theoretical Violation: Jensen's Inequality</b>", st['Card_Title']),
        Paragraph("For a convex function <i>g</i>(<i>x</i>), &#120124;[<i>g</i>(<i>X</i>)] &ne; <i>g</i>(&#120124;[<i>X</i>]). Due to volatility drag, compounding under uncertainty yields a median trajectory strictly below the arithmetic average.", st['Card_Body'])
    ]
    
    c2 = [
        Paragraph("<b>Empirical Consequences for Citizens</b>", st['Card_Title']),
        Paragraph("• <b>Retirement Shortfall:</b> Investors base life savings on optimistic straight lines, experiencing catastrophic downside shortfalls.<br/>"
                  "• <b>Predatory Credit Traps:</b> Borrowers misunderstand compounding frequencies and fall into negative amortization loans.<br/>"
                  "• <b>Absence of Tail Risk:</b> Retail platforms completely omit Value at Risk (VaR) and goal attainment probabilities.", st['Card_Body']),
        Spacer(1, 6),
        Table([[Paragraph("<b>The Research Gap:</b> Institutional quantitative hedge funds model full stochastic distributions, while everyday citizens are relegated to flawed, 18th-century deterministic formulas.", st['Equation_Box'])]],
              colWidths=[400], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF2F2")), ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#F87171")), ('PADDING', (0,0), (-1,-1), 6)])
    ]
    
    t_slide2 = Table([[make_slide_card(c1, 425), make_slide_card(c2, 425)]], colWidths=[435, 435])
    story.append(t_slide2)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 3: HYPOTHESIS & OBJECTIVES
    # --------------------------------------------------------------------------
    story.append(Paragraph("2. Research Hypothesis & Core Objectives", st['Slide_Header']))
    story.append(Paragraph("Transforming financial decision support from static scalar estimates into rigorous probability densities", st['Slide_Subheader']))
    
    hyp_card = [
        Paragraph("<b>Central Research Hypothesis</b>", st['Card_Title']),
        Paragraph("<i>\"By replacing deterministic point expectations with numerical root-finding algorithms and continuous stochastic processes (Geometric Brownian Motion), retail investors can be equipped with robust, distribution-aware decision support that quantifies downside tail risk and eliminates the volatility drag illusion.\"</i>", st['Card_Body'])
    ]
    story.append(make_slide_card(hyp_card, width=870, bg="#EFF6FF", border="#93C5FD", pad=8))
    story.append(Spacer(1, 10))
    
    o1 = [
        Paragraph("<b>Objective 1: First-Principles Theory</b>", st['Card_Title']),
        Paragraph("Derive all financial laws from axiomatic foundations: governing ODEs, Euler limits, finite geometric series, and stochastic calculus.", st['Card_Body'])
    ]
    o2 = [
        Paragraph("<b>Objective 2: Numerical Optimization</b>", st['Card_Title']),
        Paragraph("Implement high-precision root-finding (Newton–Raphson & Bisection) to solve multi-period non-linear equations where Galois theory proves algebraic radicals fail.", st['Card_Body'])
    ]
    o3 = [
        Paragraph("<b>Objective 3: Stochastic Risk Simulation</b>", st['Card_Title']),
        Paragraph("Simulate 10,000+ stochastic price trajectories to compute terminal wealth densities, empirical goal attainment odds, and 95% Value at Risk (VaR).", st['Card_Body'])
    ]
    
    t_obj = Table([[make_slide_card(o1, 280), make_slide_card(o2, 280), make_slide_card(o3, 280)]], colWidths=[290, 290, 290])
    story.append(t_obj)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 4: PILLAR 1 - TIME VALUE & ODES
    # --------------------------------------------------------------------------
    story.append(Paragraph("3. Theoretical Pillar 1: Time Value of Money & Governing ODEs", st['Slide_Header']))
    story.append(Paragraph("Comparing linear accumulation, discrete geometric progression, and continuous infinitesimal limits", st['Slide_Subheader']))
    
    p1_left = [
        Paragraph("<b>Linear vs. Continuous Compounding ODEs</b>", st['Card_Title']),
        Paragraph("• <b>Simple Interest (Linear ODE):</b> Rate of growth is constant across all time:<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;<i>dA/dt</i> = <i>P &middot; r</i>, &nbsp; <i>A</i>(0) = <i>P</i> &nbsp;&rArr;&nbsp; <b><i>A</i>(<i>t</i>) = <i>P</i>(1 + <i>rt</i>)</b><br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;Violates temporal subadditivity: <i>A</i>(<i>t</i><sub>1</sub> + <i>t</i><sub>2</sub>) &lt; <i>A</i>(<i>t</i><sub>1</sub>)<i>A</i>(<i>t</i><sub>2</sub>)/<i>P</i>.<br/>"
                  "• <b>Continuous Compounding (Homogeneous Linear ODE):</b> Rate of growth is proportional to instantaneous wealth:<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;<i>dA/dt</i> = <i>r &middot; A</i>(<i>t</i>), &nbsp; <i>A</i>(0) = <i>P</i> &nbsp;&rArr;&nbsp; <b><i>A</i>(<i>t</i>) = <i>P e</i><sup><i>rt</i></sup></b>", st['Card_Body']),
        Spacer(1, 4),
        Paragraph("<b>Euler's Limit as Compounding Frequency <i>m</i> &rarr; &infin;</b>", st['Card_Title']),
        Paragraph("lim<sub><i>m</i>&rarr;&infin;</sub> <i>P</i>(1 + <i>r/m</i>)<sup><i>mt</i></sup> = <i>P</i> [lim<sub><i>x</i>&rarr;&infin;</sub> (1 + 1/<i>x</i>)<sup><i>x</i></sup>]<sup><i>rt</i></sup> = <b><i>P e</i><sup><i>rt</i></sup></b>", st['Equation_Box'])
    ]
    
    p1_right = [
        Paragraph("<b>Discrete to Continuous Yield Equivalence</b>", st['Card_Title']),
        Paragraph("To match the terminal wealth of an annual rate <i>r</i><sub><i>d</i></sub> compounded <i>m</i> times with a continuous rate <i>r</i><sub><i>c</i></sub>:<br/>"
                  "<i>e</i><sup><i>r</i><sub><i>c</i></sub></sup> = (1 + <i>r</i><sub><i>d</i></sub>/<i>m</i>)<sup><i>m</i></sup> &nbsp;&rArr;&nbsp; <b><i>r</i><sub><i>c</i></sub> = <i>m</i> &middot; ln(1 + <i>r</i><sub><i>d</i></sub>/<i>m</i>)</b>", st['Card_Body']),
        Spacer(1, 4),
        Paragraph("<b>Effective Annual Rate (EAR / APY)</b>", st['Card_Title']),
        Paragraph("Exposing the retail 'APR illusion':<br/>"
                  "<b>EAR = (1 + <i>r</i><sub>nom</sub>/<i>m</i>)<sup><i>m</i></sup> &minus; 1</b> &nbsp;&nbsp;&bull;&nbsp;&nbsp; <b>EAR<sub>cont</sub> = <i>e</i><sup><i>r</i><sub>nom</sub></sup> &minus; 1</b><br/>"
                  "A credit card charging 18.00% APR compounded monthly produces a true annualized cost of <b>19.56% EAR</b>.", st['Card_Body']),
        Spacer(1, 4),
        Paragraph("<b>The Stochastic Discount Factor</b>", st['Card_Title']),
        Paragraph("Present Value operator: <b>PV = FV &middot; (1 + <i>r/m</i>)<sup>&minus;<i>mt</i></sup></b> &nbsp;&nbsp;&bull;&nbsp;&nbsp; <b>PV<sub>cont</sub> = FV &middot; <i>e</i><sup>&minus;<i>rt</i></sup></b>", st['Card_Body'])
    ]
    
    t_p1 = Table([[make_slide_card(p1_left, 425), make_slide_card(p1_right, 425)]], colWidths=[435, 435])
    story.append(t_p1)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 5: PILLAR 2 - CONSUMER DEBT & NEGATIVE AMORTIZATION
    # --------------------------------------------------------------------------
    story.append(Paragraph("4. Theoretical Pillar 2: Consumer Debt & Negative Amortization", st['Slide_Header']))
    story.append(Paragraph("Finite geometric series summation and the mathematical boundary condition for debt traps", st['Slide_Subheader']))
    
    p2_left = [
        Paragraph("<b>Analytical Derivation of Equated Monthly Installment (EMI)</b>", st['Card_Title']),
        Paragraph("Equating the borrowed Principal <i>P</i> to the discounted present value of an <i>n</i>-period annuity with monthly interest rate <i>R</i> = <i>r</i>/12:<br/>"
                  "<i>P</i> = &sum;<sub><i>k</i>=1</sub><sup><i>n</i></sup> <i>E</i> &middot; (1 + <i>R</i>)<sup>&minus;<i>k</i></sup> = <i>E</i> &middot; [ (1 &minus; (1 + <i>R</i>)<sup>&minus;<i>n</i></sup>) / <i>R</i> ]", st['Card_Body']),
        Spacer(1, 4),
        Paragraph("Inverting the geometric sum yields the exact closed-form EMI equation:", st['Card_Body']),
        Spacer(1, 2),
        Paragraph("<b><i>E</i> = <i>P &middot; R</i> &middot; (1 + <i>R</i>)<sup><i>n</i></sup> / [ (1 + <i>R</i>)<sup><i>n</i></sup> &minus; 1 ]</b>", st['Equation_Box']),
        Spacer(1, 4),
        Paragraph("<b>Principal / Interest Amortization Dynamics</b>", st['Card_Title']),
        Paragraph("At month <i>k</i>: Interest component <i>I</i><sub><i>k</i></sub> = <i>B</i><sub><i>k</i>&minus;1</sub> &middot; <i>R</i>, Principal repaid <i>P</i><sub><i>k</i></sub> = <i>E</i> &minus; <i>I</i><sub><i>k</i></sub>.<br/>"
                  "Principal repayments form an escalating geometric progression: <i>P</i><sub><i>k</i></sub> = <i>P</i><sub>1</sub>(1 + <i>R</i>)<sup><i>k</i>&minus;1</sup>.", st['Card_Body'])
    ]
    
    p2_right = [
        Paragraph("<b>The Negative Amortization Boundary Condition</b>", st['Card_Title']),
        Paragraph("In retail finance, predatory 'teaser rate' loans or minimum credit card payments often charge an installment <i>E</i> below the monthly accrued interest.", st['Card_Body']),
        Spacer(1, 4),
        Table([[Paragraph("<b>Boundary Theorem:</b> A loan amortizes toward zero if and only if:<br/>"
                          "<b><i>E</i> &gt; <i>P</i> &middot; <i>R</i> &nbsp;&nbsp;&hArr;&nbsp;&nbsp; <i>E</i> &gt; <i>P</i> &middot; (<i>r</i> / 12)</b><br/>"
                          "If <i>E</i> &le; <i>P &middot; R</i>, outstanding debt balance diverges: lim<sub><i>n</i>&rarr;&infin;</sub> <i>B</i><sub><i>n</i></sub> = +&infin;.", st['Equation_Box'])]],
              colWidths=[400], style=[('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF2F2")), ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#EF4444")), ('PADDING', (0,0), (-1,-1), 8)]),
        Spacer(1, 6),
        Paragraph("<b>Societal Relevance for Consumer Protection</b>", st['Card_Title']),
        Paragraph("Our system implements automated boundary testing: detecting predatory credit structures and displaying exact inflection points where prepayments collapse total interest expense.", st['Card_Body'])
    ]
    
    t_p2 = Table([[make_slide_card(p2_left, 425), make_slide_card(p2_right, 425)]], colWidths=[435, 435])
    story.append(t_p2)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 6: PILLAR 3 - NUMERICAL ROOT-FINDING (IRR)
    # --------------------------------------------------------------------------
    story.append(Paragraph("5. Theoretical Pillar 3: Numerical Optimization for Yield Analysis", st['Slide_Header']))
    story.append(Paragraph("The Abel–Ruffini impossibility theorem and high-order Newton–Raphson root finding", st['Slide_Subheader']))
    
    p3_left = [
        Paragraph("<b>The Internal Rate of Return (IRR) Polynomial</b>", st['Card_Title']),
        Paragraph("For irregular cash flows {<i>C</i><sub>0</sub>, <i>C</i><sub>1</sub>, ..., <i>C</i><sub><i>T</i></sub>}, the IRR is the discount rate <i>r</i>* setting Net Present Value to zero:<br/>"
                  "NPV(<i>r</i>) = &sum;<sub><i>t</i>=0</sub><sup><i>T</i></sup> <i>C</i><sub><i>t</i></sub> / (1 + <i>r</i>)<sup><i>t</i></sup> = 0", st['Card_Body']),
        Spacer(1, 4),
        Paragraph("<b>Galois Theory & The Abel–Ruffini Theorem</b>", st['Card_Title']),
        Paragraph("Setting <i>x</i> = 1 / (1 + <i>r</i>) transforms NPV(<i>r</i>) = 0 into a polynomial of degree <i>T</i>: &sum; <i>C</i><sub><i>t</i></sub> <i>x</i><sup><i>t</i></sup> = 0.<br/>"
                  "<b>The Abel–Ruffini Theorem</b> proves that general algebraic solutions in radicals <b>do not exist for degree <i>T</i> &gt; 4</b>.<br/>"
                  "Therefore, calculating multi-year financial yields <b>strictly necessitates numerical analysis</b>.", st['Card_Body'])
    ]
    
    p3_right = [
        Paragraph("<b>Quadratic Convergence via Newton–Raphson</b>", st['Card_Title']),
        Paragraph("We utilize the analytical first derivative with respect to discount rate <i>r</i>:<br/>"
                  "<i>f'</i>(<i>r</i>) = &minus;&sum;<sub><i>t</i>=1</sub><sup><i>T</i></sup> [ <i>t &middot; C</i><sub><i>t</i></sub> / (1 + <i>r</i>)<sup><i>t</i>+1</sup> ]<br/>"
                  "Iterative update: <b><i>r</i><sub><i>k</i>+1</sub> = <i>r</i><sub><i>k</i></sub> &minus; [ NPV(<i>r</i><sub><i>k</i></sub>) / <i>f'</i>(<i>r</i><sub><i>k</i></sub>) ]</b><br/>"
                  "Exhibits quadratic convergence: |<i>e</i><sub><i>k</i>+1</sub>| &le; <i>M</i> |<i>e</i><sub><i>k</i></sub>|<sup>2</sup> (error squares every step).", st['Card_Body']),
        Spacer(1, 4),
        Paragraph("<b>Robustness: Bisection Fallback Mechanism</b>", st['Card_Title']),
        Paragraph("When non-conventional cash flows exhibit multiple sign changes (Descartes' Rule of Signs) or <i>f'</i>(<i>r</i>) &rarr; 0, our engine automatically falls back to interval bisection on [<i>a</i>, <i>b</i>] ensuring guaranteed linear convergence.", st['Card_Body'])
    ]
    
    t_p3 = Table([[make_slide_card(p3_left, 425), make_slide_card(p3_right, 425)]], colWidths=[435, 435])
    story.append(t_p3)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 7: PILLAR 4 - STOCHASTIC DYNAMICS & ITÔ'S LEMMA
    # --------------------------------------------------------------------------
    story.append(Paragraph("6. Theoretical Pillar 4: Stochastic Asset Dynamics & Itô's Lemma", st['Slide_Header']))
    story.append(Paragraph("Continuous-time Brownian motion and the mathematical proof of the volatility drag gap", st['Slide_Subheader']))
    
    p4_left = [
        Paragraph("<b>The Stochastic Differential Equation (GBM)</b>", st['Card_Title']),
        Paragraph("Asset prices evolve under continuous drift &mu; and volatility &sigma; driven by a standard Wiener process (Brownian Motion) <i>W</i><sub><i>t</i></sub>:<br/>"
                  "<b><i>dS</i><sub><i>t</i></sub> = &mu; <i>S</i><sub><i>t</i></sub> <i>dt</i> + &sigma; <i>S</i><sub><i>t</i></sub> <i>dW</i><sub><i>t</i></sub></b> &nbsp;&nbsp;&nbsp;&nbsp;(<i>dW</i><sub><i>t</i></sub> ~ &#119977;(0, <i>dt</i>))", st['Equation_Box']),
        Spacer(1, 4),
        Paragraph("<b>Proof of Volatility Drag via Itô's Lemma</b>", st['Card_Title']),
        Paragraph("In standard calculus, <i>d</i>(ln <i>S</i>) = <i>dS</i>/<i>S</i>. But Brownian paths have non-zero quadratic variation: (<i>dW</i><sub><i>t</i></sub>)<sup>2</sup> = <i>dt</i>.<br/>"
                  "Applying Itô's Lemma to <i>f</i>(<i>S</i>) = ln <i>S</i> with <i>f'</i> = 1/<i>S</i> and <i>f''</i> = &minus;1/<i>S</i><sup>2</sup>:<br/>"
                  "<i>d</i>(ln <i>S</i>) = (1/<i>S</i>)<i>dS</i> + (1/2)(&minus;1/<i>S</i><sup>2</sup>)(<i>dS</i>)<sup>2</sup><br/>"
                  "<i>d</i>(ln <i>S</i>) = (&mu; <i>dt</i> + &sigma; <i>dW</i>) &minus; (1/2)&sigma;<sup>2</sup> <i>dt</i><br/>"
                  "<b><i>d</i>(ln <i>S</i>) = (&mu; &minus; &frac12;&sigma;<sup>2</sup>) <i>dt</i> + &sigma; <i>dW</i><sub><i>t</i></sub></b>", st['Card_Body'])
    ]
    
    p4_right = [
        Paragraph("<b>The Exact Discrete Path Solution</b>", st['Card_Title']),
        Paragraph("Integrating yields the exact trajectory for time step &Delta;<i>t</i>:<br/>"
                  "<b><i>S</i><sub><i>t</i>+&Delta;<i>t</i></sub> = <i>S</i><sub><i>t</i></sub> &middot; exp[ (&mu; &minus; &frac12;&sigma;<sup>2</sup>)&Delta;<i>t</i> + &sigma; &radic;&Delta;<i>t</i> &middot; <i>Z</i> ]</b> &nbsp;(<i>Z</i> ~ &#119977;(0, 1))", st['Equation_Box']),
        Spacer(1, 4),
        Paragraph("<b>The Fundamental Divergence: Mean vs. Median</b>", st['Card_Title']),
        Paragraph("• <b>Arithmetic Mean:</b> &#120124;[<i>S</i><sub><i>t</i></sub>] = <i>S</i><sub>0</sub> <i>e</i><sup>&mu;<i>t</i></sup> (pulled up by extreme right-tail skewness).<br/>"
                  "• <b>Typical Median Path:</b> <i>S</i><sub>med</sub>(<i>t</i>) = <i>S</i><sub>0</sub> <i>e</i><sup>(&mu; &minus; &frac12;&sigma;<sup>2</sup>)<i>t</i></sup>.<br/>"
                  "• <b>Structural Volatility Drag:</b> &Delta;&mu; = &minus;&frac12;&sigma;<sup>2</sup>.<br/>"
                  "<i>Key Finding:</i> For a stock fund with &mu; = 12% and &sigma; = 20%, drag is &minus;2.00% per year! Over 10 years, median wealth lags arithmetic expectation by <b>INR 601,835 per Million invested</b>. More than 50% of investors underperform the average!", st['Card_Body'])
    ]
    
    t_p4 = Table([[make_slide_card(p4_left, 425), make_slide_card(p4_right, 425)]], colWidths=[435, 435])
    story.append(t_p4)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 8: PILLAR 5 - MONTE CARLO & RISK ESTIMATION
    # --------------------------------------------------------------------------
    story.append(Paragraph("7. Theoretical Pillar 5: Monte Carlo Simulation & Risk Estimation", st['Slide_Header']))
    story.append(Paragraph("Large-scale stochastic ensembles, Central Limit Theorem bounds, and downside tail risk metrics", st['Slide_Subheader']))
    
    p5_left = [
        Paragraph("<b>Monte Carlo Ensemble & CLT Convergence</b>", st['Card_Title']),
        Paragraph("We generate <i>M</i> = 10,000+ independent market paths using vectorized NumPy operations.<br/>"
                  "By the <b>Strong Law of Large Numbers (SLLN)</b>, the sample average converges almost surely to the true expectation: lim (1/<i>M</i>)&sum; <i>g</i>(<i>S</i><sub><i>T</i></sub>) = &#120124;[<i>g</i>(<i>S</i><sub><i>T</i></sub>)].<br/>"
                  "By the <b>Central Limit Theorem</b>, standard error decays at the canonical rate:<br/>"
                  "<b>Standard Error = &sigma;<sub>sample</sub> / &radic;<i>M</i> &nbsp;=&nbsp; &#119978;(1 / &radic;<i>M</i>)</b><br/>"
                  "For <i>M</i> = 10,000, estimator precision narrows to &plusmn;1% of sample variance.", st['Card_Body'])
    ]
    
    p5_right = [
        Paragraph("<b>Quantitative Downside Risk Metrics</b>", st['Card_Title']),
        Paragraph("• <b>Empirical Goal Attainment Probability:</b><br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;<b>P&#770;(<i>S</i><sub><i>T</i></sub> &ge; Goal) = (1 / <i>M</i>) &sum;<sub><i>m</i>=1</sub><sup><i>M</i></sup> &#120793;<sub>{<i>S</i><sub><i>T</i>, <i>m</i></sub> &ge; Goal}</sub></b><br/>"
                  "• <b>Value at Risk (VaR<sub>&alpha;</sub>):</b> Maximum expected loss at confidence level (1 &minus; &alpha;) over horizon <i>T</i>:<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;VaR<sub>0.95</sub> = <i>S</i><sub>0</sub> &minus; Quantile<sub>0.05</sub>(<i>S</i><sub><i>T</i></sub>)<br/>"
                  "• <b>Conditional VaR (CVaR / Expected Shortfall):</b> Average loss incurred in the worst 5% tail scenarios:<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;CVaR<sub>0.95</sub> = &#120124;[ <i>S</i><sub>0</sub> &minus; <i>S</i><sub><i>T</i></sub> | <i>S</i><sub><i>T</i></sub> &le; Quantile<sub>0.05</sub> ]", st['Card_Body'])
    ]
    
    t_p5 = Table([[make_slide_card(p5_left, 425), make_slide_card(p5_right, 425)]], colWidths=[435, 435])
    story.append(t_p5)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 9: ARCHITECTURE & VERIFICATION
    # --------------------------------------------------------------------------
    story.append(Paragraph("8. System Architecture & Mathematical Verification", st['Slide_Header']))
    story.append(Paragraph("Layered computational pipeline, zero-black-box design, and strict floating-point validation", st['Slide_Subheader']))
    
    p6_left = [
        Paragraph("<b>Three-Tier Computational Architecture</b>", st['Card_Title']),
        Paragraph("1. <b>Mathematical Core (<code>models/</code>):</b> Pure functional implementations of TVM, amortizations, Newton-Raphson root-finders, and vectorized GBM simulations.<br/>"
                  "2. <b>Verification Layer (<code>tests/</code>):</b> Automated test suite enforcing domain boundaries and numerical convergence.<br/>"
                  "3. <b>Interactive Visual Interface (<code>app.py</code>):</b> Streamlit dashboard rendering dynamic probability distributions, cash flow schedules, and sensitivity sliders.", st['Card_Body']),
        Spacer(1, 4),
        Paragraph("<b>Design Principle: Zero Black Boxes</b>", st['Card_Title']),
        Paragraph("Every single algorithm in code maps directly to an axiomatic chapter in our theoretical monograph series.", st['Card_Body'])
    ]
    
    p6_right = [
        Paragraph("<b>Automated Testing & Benchmark Methodology</b>", st['Card_Title']),
        Paragraph("Academic research demands uncompromising reproducibility. Every module is verified against three criteria:<br/>"
                  "• <b>Independent Benchmark:</b> Deterministic models cross-checked against Microsoft Excel standards (PMT, IRR, PV) to <b>&epsilon; &le; 10<sup>&minus;7</sup></b>.<br/>"
                  "• <b>Boundary Value Analysis:</b> Validating zero-interest limits (<i>r</i> &rarr; 0), instantaneous horizons (<i>t</i> &rarr; 0), and infinite compounding (<i>m</i> &rarr; &infin;).<br/>"
                  "• <b>Domain Guardrails:</b> Strict raising of <code>ValueError</code> on negative parameters, nonsensical loan tenors, and division by zero.", st['Card_Body'])
    ]
    
    t_p6 = Table([[make_slide_card(p6_left, 425), make_slide_card(p6_right, 425)]], colWidths=[435, 435])
    story.append(t_p6)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # SLIDE 10: ACADEMIC CONTRIBUTION & CONCLUSION
    # --------------------------------------------------------------------------
    story.append(Paragraph("9. Academic Contributions & Research Milestones", st['Slide_Header']))
    story.append(Paragraph("Current progress, societal impact, and research roadmap for the Avishkar Convention", st['Slide_Subheader']))
    
    p7_c1 = [
        Paragraph("<b>Completed Research Milestones</b>", st['Card_Title']),
        Paragraph("• <b>12-Volume Reference Monograph (56 Pages):</b> Fully authored, formatted, and compiled in <code>theory_and_derivations/</code>.<br/>"
                  "• <b>Analytical Verification:</b> Hand-solved academic case studies verifying all equations down to exact rupee arithmetic.<br/>"
                  "• <b>Open-Source Repository:</b> Publicly hosted on GitHub under MIT License with conventional semantic commits.", st['Card_Body'])
    ]
    
    p7_c2 = [
        Paragraph("<b>Societal Relevance & Consumer Protection</b>", st['Card_Title']),
        Paragraph("• <b>Democratizing Institutional Math:</b> Equipping common citizens with hedge-fund grade stochastic risk metrics.<br/>"
                  "• <b>Debt Trap Prevention:</b> Exposing predatory negative amortization structures before borrowers sign contracts.<br/>"
                  "• <b>Informed Wealth Planning:</b> Revealing actual probability densities of achieving financial independence.", st['Card_Body'])
    ]
    
    t_p7 = Table([[make_slide_card(p7_c1, 425), make_slide_card(p7_c2, 425)]], colWidths=[435, 435])
    story.append(t_p7)
    story.append(Spacer(1, 10))
    
    thx_card = [
        Paragraph("<b>Thank You!</b> &nbsp;&nbsp;|&nbsp;&nbsp; Open for Questions & Mathematical Defense", ParagraphStyle('Thx', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor("#1E3A8A"), alignment=1)),
        Spacer(1, 2),
        Paragraph("Atharv Ranade &nbsp;&bull;&nbsp; Department of Mathematics & Statistics &nbsp;&bull;&nbsp; University of Mumbai", ParagraphStyle('Thx2', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor("#475569"), alignment=1))
    ]
    story.append(make_slide_card(thx_card, width=870, bg="#EFF6FF", border="#93C5FD", pad=8))
    
    doc.build(story, canvasmaker=WidescreenSlideCanvas)
    print(f"Generated PDF: {pdf_path}")

# ==============================================================================
# 2. PYTHON-PPTX 16:9 WIDESCREEN GENERATOR
# ==============================================================================

def add_header(slide, title_text, category_text="UNIVERSITY OF MUMBAI  •  DEPARTMENT OF MATHEMATICS & STATISTICS  |  AVISHKAR CATEGORY 3"):
    # Header Category Label
    cat_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.13), Inches(0.3))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text
    p_c.font.size = Pt(8.5)
    p_c.font.bold = True
    p_c.font.color.rgb = RGBColor(2, 132, 199)  # Light Blue
    
    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.65), Inches(12.13), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = RGBColor(30, 58, 138)  # Deep Navy

def add_card(slide, left, top, width, height, title, bullet_points, bg_rgb=(248, 250, 252), border_rgb=(203, 213, 225)):
    # Shape
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*bg_rgb)
    shape.line.color.rgb = RGBColor(*border_rgb)
    shape.line.width = Pt(1)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    tf.margin_bottom = Inches(0.2)
    
    # Title
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(13)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(30, 58, 138)
    p_title.space_after = Pt(8)
    
    # Bullets
    for bp in bullet_points:
        p = tf.add_paragraph()
        p.text = "• " + bp
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(15, 23, 42)
        p.space_after = Pt(5)

def generate_pptx(pptx_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Slide 1: Title Slide
    s1 = prs.slides.add_slide(blank_layout)
    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "RESEARCH SEMINAR  •  APPLIED MATHEMATICAL FINANCE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(2, 132, 199)
    p.space_after = Pt(10)
    
    p = tf1.add_paragraph()
    p.text = "Financial Decision Support System (FDSS)"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(30, 58, 138)
    p.space_after = Pt(8)
    
    p = tf1.add_paragraph()
    p.text = "A Mathematical & Stochastic Framework for Retail Financial Risk Modeling"
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(15, 23, 42)
    p.space_after = Pt(30)
    
    p = tf1.add_paragraph()
    p.text = "Investigator: Atharv Ranade  |  Department of Mathematics & Statistics  |  University of Mumbai"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(30, 58, 138)
    p.space_after = Pt(5)
    
    p = tf1.add_paragraph()
    p.text = "Avishkar Research Convention: Category 3 (Pure Sciences — Mathematics & Statistics)"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(71, 85, 105)

    # Slide 2: The Deterministic Fallacy
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. The Research Problem: The Deterministic Fallacy in Retail Finance")
    add_card(s2, 0.6, 1.5, 5.8, 5.3, "The Deterministic Expectation Assumption", [
        "Commercial calculators project wealth using single-point linear formulas: A = P(1 + r)^t.",
        "They assume constant returns (e.g., exactly 12.00% every single year for 20 years).",
        "The Flaw: Real markets fluctuate under continuous Brownian motion with volatility sigma > 0.",
        "Theoretical Violation: Jensen's Inequality E[g(X)] != g(E[X]). Compounding under volatility creates a median return strictly below the arithmetic average."
    ])
    add_card(s2, 6.9, 1.5, 5.8, 5.3, "Empirical Consequences for Citizens", [
        "Retirement Shortfalls: Investors base life savings on straight lines, experiencing catastrophic downside shortfalls.",
        "Predatory Debt Traps: Borrowers misunderstand compounding frequencies and fall into negative amortization loans.",
        "Absence of Tail Risk: Retail tools completely omit Value at Risk (VaR) and goal attainment probabilities.",
        "The Research Gap: Institutional hedge funds use stochastic distributions; everyday citizens are left with flawed 18th-century scalar math."
    ])

    # Slide 3: Hypothesis & Objectives
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Research Hypothesis & Core Objectives")
    add_card(s3, 0.6, 1.5, 12.13, 1.8, "Central Research Hypothesis", [
        "\"By replacing deterministic point expectations with numerical root-finding algorithms and continuous stochastic processes (Geometric Brownian Motion), retail investors can be equipped with robust, distribution-aware decision support that quantifies downside tail risk and eliminates the volatility drag illusion.\""
    ], bg_rgb=(239, 246, 255), border_rgb=(147, 197, 253))
    add_card(s3, 0.6, 3.6, 3.8, 3.2, "Objective 1: First-Principles Theory", [
        "Derive all financial laws from axiomatic foundations: governing ODEs, Euler limits, finite geometric series, and stochastic calculus."
    ])
    add_card(s3, 4.75, 3.6, 3.8, 3.2, "Objective 2: Numerical Optimization", [
        "Implement high-precision root-finding (Newton-Raphson & Bisection) to solve multi-period cash flow equations where Galois theory proves radical formulas fail."
    ])
    add_card(s3, 8.9, 3.6, 3.8, 3.2, "Objective 3: Stochastic Risk Simulation", [
        "Simulate 10,000+ stochastic price trajectories to compute terminal wealth densities, empirical goal attainment odds, and 95% Value at Risk (VaR)."
    ])

    # Slide 4: Pillar 1 - Time Value & ODEs
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. Theoretical Pillar 1: Time Value of Money & Governing ODEs")
    add_card(s4, 0.6, 1.5, 5.8, 5.3, "Linear vs. Continuous Compounding ODEs", [
        "Simple Interest (Linear ODE): Constant growth rate dA/dt = P * r, A(0) = P => A(t) = P(1 + r*t).",
        "Violates subadditivity: A(t1 + t2) < A(t1)*A(t2)/P due to lost interest-on-interest.",
        "Continuous Compounding (Homogeneous Linear ODE): dA/dt = r * A(t) => A(t) = P * e^(rt).",
        "Euler Limit: lim (1 + r/m)^(mt) = e^(rt) as compounding frequency m -> infinity.",
        "Discount Factor: PV = FV * (1 + r/m)^(-mt), decaying asymptotically toward zero as t -> infinity."
    ])
    add_card(s4, 6.9, 1.5, 5.8, 5.3, "Yield Equivalences & Regulatory Standards", [
        "Discrete to Continuous Conversion: e^(rc) = (1 + rd/m)^m => rc = m * ln(1 + rd/m).",
        "The APR Illusion: Nominal APR ignores intra-year compounding.",
        "Effective Annual Rate (EAR / APY): EAR = (1 + r_nom/m)^m - 1.",
        "Example: 18.00% APR compounded monthly produces a true cost of 19.56% EAR.",
        "Why Quantitative Finance uses continuous rates: Logarithmic returns add linearly across time periods, enabling stochastic calculus."
    ])

    # Slide 5: Pillar 2 - Consumer Debt & Negative Amortization
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. Theoretical Pillar 2: Consumer Debt Analytics & Amortization")
    add_card(s5, 0.6, 1.5, 5.8, 5.3, "Closed-Form EMI Derivation", [
        "Equating Principal P to discounted finite annuity: P = sum [E * (1 + R)^(-k)] for k=1 to n, where R = r/12.",
        "Closed-form geometric sum: P = E * [1 - (1 + R)^(-n)] / R.",
        "Exact EMI Formula: E = P * R * (1 + R)^n / [ (1 + R)^n - 1 ].",
        "Principal / Interest Dynamics: Monthly interest Ik = Bk-1 * R. Principal repaid Pk = E - Ik.",
        "Principal repayments form an escalating geometric progression: Pk = P1 * (1 + R)^(k-1)."
    ])
    add_card(s5, 6.9, 1.5, 5.8, 5.3, "The Negative Amortization Boundary", [
        "Predatory Loan Mechanics: Lenders set monthly installment E below monthly accrued interest.",
        "Boundary Theorem: A loan amortizes to zero if and only if E > P * R <=> E > P * (r / 12).",
        "If E <= P * R, outstanding debt diverges: lim Bn = +infinity.",
        "Prepayment Optimization: Early capital injections reduce total interest exponentially due to shifting the geometric balance early in the amortization schedule.",
        "Societal Benefit: Consumer protection against deceptive retail loan structures."
    ])

    # Slide 6: Pillar 3 - Numerical Root-Finding (IRR)
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. Theoretical Pillar 3: Numerical Optimization for Yield Analysis")
    add_card(s6, 0.6, 1.5, 5.8, 5.3, "The Internal Rate of Return (IRR) Polynomial", [
        "For irregular cash flows {C0, C1, ..., CT}, IRR is the root r* setting NPV(r) = 0.",
        "NPV(r) = sum [ Ct / (1 + r)^t ] = 0.",
        "The Abel-Ruffini Theorem (Galois Theory): Setting x = 1/(1+r) yields a polynomial of degree T.",
        "General algebraic radical solutions do not exist for degree T > 4.",
        "Therefore, calculating multi-year financial yields strictly necessitates numerical methods."
    ])
    add_card(s6, 6.9, 1.5, 5.8, 5.3, "Newton-Raphson & Bisection Fallback", [
        "Analytical First Derivative: f'(r) = -sum [ t * Ct / (1 + r)^(t+1) ].",
        "Newton-Raphson Iteration: r_{k+1} = r_k - [ NPV(r_k) / f'(r_k) ].",
        "Quadratic Convergence: Error squares at each iteration (|e_{k+1}| <= M * |e_k|^2).",
        "Descartes' Rule of Signs: Irregular cash flows may have multiple sign changes and multiple roots.",
        "Bisection Fallback: Automatic bracket-halving ensures guaranteed convergence if derivatives oscillate or approach zero."
    ])

    # Slide 7: Pillar 4 - Stochastic Asset Dynamics (GBM)
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "6. Theoretical Pillar 4: Stochastic Asset Dynamics & Itô's Lemma")
    add_card(s7, 0.6, 1.5, 5.8, 5.3, "Geometric Brownian Motion & Itô's Lemma Proof", [
        "Governing SDE: dS = mu * S * dt + sigma * S * dW, with Wiener process dW ~ N(0, dt).",
        "Non-zero quadratic variation in stochastic calculus: (dW)^2 = dt.",
        "Applying Itô's Lemma to f(S) = ln(S): df = f'(S) dS + 0.5 * f''(S) (dS)^2.",
        "With f' = 1/S and f'' = -1/S^2: d(ln S) = (mu - 0.5*sigma^2) dt + sigma dW.",
        "Exact Discrete Solution: S_{t+dt} = St * exp[(mu - 0.5*sigma^2)dt + sigma * sqrt(dt) * Z]."
    ])
    add_card(s7, 6.9, 1.5, 5.8, 5.3, "The Volatility Drag Principle", [
        "Arithmetic Expected Mean: E[St] = S0 * e^(mu*t) (pulled up by positive skewness).",
        "Typical Median Trajectory: S_med(t) = S0 * e^[(mu - 0.5*sigma^2)t].",
        "Structural Return Penalty: Delta mu = -0.5 * sigma^2.",
        "Example (mu=12%, sigma=20%): Annual drag is -2.00%! Over 10 years, median wealth lags arithmetic average by INR 601,835 per Million invested.",
        "Over 50% of investors strictly underperform the advertised arithmetic average."
    ])

    # Slide 8: Pillar 5 - Monte Carlo & Risk Estimation
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "7. Theoretical Pillar 5: Monte Carlo Simulation & Risk Estimation")
    add_card(s8, 0.6, 1.5, 5.8, 5.3, "Large-Scale Ensembles & CLT Convergence", [
        "Vectorized simulation of M = 10,000+ stochastic price trajectories.",
        "Strong Law of Large Numbers (SLLN): Sample mean converges almost surely to true expectation.",
        "Central Limit Theorem: Error standard deviation decays as O(1 / sqrt(M)).",
        "For M = 10,000, estimator precision is within +/-1% of sample variance.",
        "Produces full empirical probability density function of terminal wealth."
    ])
    add_card(s8, 6.9, 1.5, 5.8, 5.3, "Quantitative Downside Risk Metrics", [
        "Goal Attainment Probability: P_hat(ST >= Goal) = (1/M) * sum [ 1_{ST,m >= Goal} ].",
        "Value at Risk (VaR 95%): Maximum expected loss at 95% confidence over horizon T.",
        "Conditional VaR (CVaR / Expected Shortfall): Expected loss given that loss exceeds VaR threshold (captures extreme tail risk).",
        "Empirical Milestone: Replaces false deterministic certainty with actionable risk distributions."
    ])

    # Slide 9: Architecture & Verification
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "8. System Architecture & Mathematical Verification")
    add_card(s9, 0.6, 1.5, 5.8, 5.3, "Modular Computational Pipeline", [
        "Mathematical Core (models/): Pure functional implementations of TVM, loans, Newton-Raphson, and vectorized GBM simulations.",
        "Verification Layer (tests/): Automated pytest suite enforcing boundary limits and convergence.",
        "Interactive Dashboard (app.py): Streamlit web interface with dynamic Plotly charts, parameter sliders, and sensitivity analyses.",
        "Zero Black Boxes: Every code routine maps 1:1 to an axiomatic chapter in the mathematical monograph."
    ])
    add_card(s9, 6.9, 1.5, 5.8, 5.3, "Verification Standards & Precision", [
        "Analytical Hand Benchmarks: Fully worked manual solutions verifying floating-point accuracy.",
        "Cross-Validation with Excel: Deterministic routines verified against Excel standards to error epsilon <= 10^-7.",
        "Boundary Value Testing: Evaluated at r -> 0, t -> 0, and infinite frequency m -> infinity.",
        "Domain Guardrails: Automated ValueError exceptions on invalid financial inputs or zero division."
    ])

    # Slide 10: Milestones & Conclusion
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "9. Academic Contributions & Research Milestones")
    add_card(s10, 0.6, 1.5, 5.8, 4.0, "Completed Research Milestones", [
        "12-Volume Reference Monograph (56 Pages): Complete theoretical foundation compiled to PDF in theory_and_derivations/.",
        "Analytical Case Studies: 24 fully worked hand solutions with complete arithmetic steps.",
        "Open-Source Repository: Publicly tracked on GitHub under MIT License with semantic conventional commits."
    ])
    add_card(s10, 6.9, 1.5, 5.8, 4.0, "Societal Relevance & Impact", [
        "Democratizing Institutional Math: Bringing hedge-fund stochastic modeling to retail citizens.",
        "Consumer Protection: Unmasking predatory debt structures and deceptive nominal APRs.",
        "Informed Decision Making: Empowering investors with true probability distributions rather than misleading point promises."
    ])
    
    # Bottom banner for Thank You / Q&A
    shape_thx = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.8), Inches(12.13), Inches(1.1))
    shape_thx.fill.solid()
    shape_thx.fill.fore_color.rgb = RGBColor(239, 246, 255)
    shape_thx.line.color.rgb = RGBColor(147, 197, 253)
    tf_thx = shape_thx.text_frame
    tf_thx.word_wrap = True
    p = tf_thx.paragraphs[0]
    p.text = "Thank You!  |  Open for Faculty Questions & Mathematical Defense"
    p.font.size = Pt(14)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = RGBColor(30, 58, 138)
    p = tf_thx.add_paragraph()
    p.text = "Atharv Ranade  •  Department of Mathematics & Statistics  •  University of Mumbai"
    p.font.size = Pt(10)
    p.alignment = PP_ALIGN.CENTER
    p.font.color.rgb = RGBColor(71, 85, 105)

    prs.save(pptx_path)
    print(f"Generated PPTX: {pptx_path}")

if __name__ == "__main__":
    generate_pdf(PDF_PATH)
    generate_pptx(PPTX_PATH)
