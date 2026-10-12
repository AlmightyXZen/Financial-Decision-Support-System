"""
Textbook Styling & Layout Framework for FDSS Mathematical Reference Series.
Provides high-contrast typography, spacious textbook layout, theorem environments,
and two-pass canvas for professional headers and footers.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Preformatted, PageBreak
)
from reportlab.pdfgen import canvas

class TextbookCanvas(canvas.Canvas):
    """
    Two-pass canvas for textbook running headers and footers.
    Even pages: Chapter title on left, system title on right.
    Odd pages: System title on left, topic title on right.
    Centered bottom pagination: '— Page X —'
    """
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
            self.setFont("Helvetica-Bold", 8.5)
            self.setFillColor(colors.HexColor("#1E293B"))  # High-contrast dark charcoal
            
            chapter_text = getattr(self, 'chapter_header', "FINANCIAL MATHEMATICS REFERENCE")
            topic_text = getattr(self, 'topic_header', "THEORY & DERIVATIONS")
            
            if self._pageNumber % 2 == 0:
                self.drawString(54, 748, chapter_text.upper())
                self.setFont("Helvetica", 8.5)
                self.drawRightString(558, 748, "FINANCIAL DECISION SUPPORT SYSTEM")
            else:
                self.setFont("Helvetica", 8.5)
                self.drawString(54, 748, "MATHEMATICAL FOUNDATIONS OF FINANCE")
                self.setFont("Helvetica-Bold", 8.5)
                self.drawRightString(558, 748, topic_text.upper())
                
            self.setStrokeColor(colors.HexColor("#94A3B8"))  # Solid crisp dividing rule
            self.setLineWidth(0.7)
            self.line(54, 740, 558, 740)

        # Running Footer (all pages)
        self.setFont("Helvetica", 9.5)
        self.setFillColor(colors.HexColor("#1E293B"))  # High-contrast readable page number
        page_text = f"—  {self._pageNumber}  —"
        self.drawCentredString(306, 32, page_text)
        
        self.restoreState()


def get_textbook_palette():
    """Returns high-contrast, accessible academic colors."""
    return {
        'primary': colors.HexColor("#0F172A"),     # Midnight slate (headings)
        'accent': colors.HexColor("#1E3A8A"),      # Academic navy blue (sections, theorems)
        'body': colors.HexColor("#0F172A"),        # Pure deep charcoal/black (body text)
        'sub': colors.HexColor("#1E293B"),         # Dark subtext (high legibility)
        'card_bg': colors.HexColor("#F8FAFC"),     # Clean off-white card background
        'border': colors.HexColor("#CBD5E1"),      # Crisp subtle border
        'th_bg': colors.HexColor("#EFF6FF"),       # Light blue theorem card fill
        'th_border': colors.HexColor("#3B82F6"),   # Solid blue theorem card border
        'eq_bg': colors.HexColor("#F1F5F9"),       # Formula callout background
        'code_bg': colors.HexColor("#F8FAFC"),     # Code listing background
        'code_border': colors.HexColor("#94A3B8"), # Code listing border
    }


def get_textbook_styles():
    """Builds and returns the comprehensive textbook typography style dictionary."""
    base_styles = getSampleStyleSheet()
    pal = get_textbook_palette()

    s = {}
    s['ChapterLabel'] = ParagraphStyle(
        'ChLabel', parent=base_styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=15,
        textColor=pal['accent'], spaceAfter=3
    )

    s['ChapterTitle'] = ParagraphStyle(
        'ChTitle', parent=base_styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=27,
        textColor=pal['primary'], spaceAfter=6
    )

    s['Subtitle'] = ParagraphStyle(
        'ChSubtitle', parent=base_styles['Normal'],
        fontName='Helvetica', fontSize=11, leading=16,
        textColor=pal['sub'], spaceAfter=10
    )

    s['H1'] = ParagraphStyle(
        'SectionH1', parent=base_styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=18,
        textColor=pal['accent'], spaceBefore=14, spaceAfter=6,
        keepWithNext=True
    )

    s['H2'] = ParagraphStyle(
        'SectionH2', parent=base_styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=15,
        textColor=pal['primary'], spaceBefore=10, spaceAfter=4,
        keepWithNext=True
    )

    s['Body'] = ParagraphStyle(
        'TextBody', parent=base_styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=15,
        textColor=pal['body'], spaceAfter=6
    )

    s['BodyBold'] = ParagraphStyle(
        'TextBodyBold', parent=s['Body'],
        fontName='Helvetica-Bold'
    )

    s['DefHeader'] = ParagraphStyle(
        'BoxHeader', parent=base_styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=15,
        textColor=pal['accent'], spaceAfter=4
    )

    s['Equation'] = ParagraphStyle(
        'DisplayEq', parent=base_styles['Normal'],
        fontName='Helvetica', fontSize=11.5, leading=17,
        textColor=pal['primary'], alignment=1
    )

    s['EquationSub'] = ParagraphStyle(
        'DisplayEqSub', parent=base_styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=9, leading=13,
        textColor=pal['sub'], alignment=1
    )

    s['PreCode'] = ParagraphStyle(
        'PreformattedListing', parent=base_styles['Normal'],
        fontName='Courier', fontSize=8, leading=11.5,
        textColor=colors.HexColor("#000000")  # Pure black code text
    )

    return s


def make_card(content_list, bg_color=None, border_color=None, pad_v=8, pad_h=14):
    """Wraps flowable content in a stylish, spacious bordered card."""
    pal = get_textbook_palette()
    bg = bg_color or pal['card_bg']
    border = border_color or pal['border']
    
    table_data = [[item] for item in content_list]
    t = Table(table_data, colWidths=[504])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('BOX', (0, 0), (-1, -1), 0.8, border),
        ('TOPPADDING', (0, 0), (-1, -1), pad_v),
        ('BOTTOMPADDING', (0, 0), (-1, -1), pad_v),
        ('LEFTPADDING', (0, 0), (-1, -1), pad_h),
        ('RIGHTPADDING', (0, 0), (-1, -1), pad_h),
    ]))
    return t


def make_code_card(code_text: str, title: str = "Python Implementation"):
    """Creates a beautifully styled, high-contrast code listing card."""
    pal = get_textbook_palette()
    styles = get_textbook_styles()
    
    header = Paragraph(f"<b>Listing:</b> {title}", styles['DefHeader'])
    divider = HRFlowable(width="100%", thickness=0.6, color=pal['border'], spaceBefore=3, spaceAfter=6)
    code_block = Preformatted(code_text.strip(), styles['PreCode'])
    
    return make_card([header, divider, code_block], bg_color=pal['card_bg'], border_color=pal['code_border'], pad_v=8, pad_h=12)
