# =========================================================
# 📄 Slide PDF Export Engine — v7.7R-BOD
# Converts Executive Presentation slides into a boardroom PDF
# Fully compatible with executive_presentation.py & dashboard
# =========================================================

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet


def export_slides_to_pdf(slides, filename="Fox_Valley_Executive_Presentation.pdf"):
    """
    Accepts list of slides (title + content) and
    generates fully formatted slide PDF deck.

    slides = [
        {"title": "...", "content": "..."},
        ...
    ]
    """

    styles = getSampleStyleSheet()
    story = []
    
    for slide in slides:
        # Slide Title
        story.append(Paragraph(f"<b>{slide['title']}</b>", styles["Title"]))
        story.append(Spacer(1, 12))
        
        # Slide Content
        story.append(Paragraph(slide["content"].replace("\n", "<br/>"), styles["BodyText"]))
        
        # Page Break
        story.append(PageBreak())

    # Build PDF
    doc = SimpleDocTemplate(
        filename,
        pagesize=LETTER,
        title="Fox Valley Executive Presentation"
    )
    doc.build(story)

    return filename
