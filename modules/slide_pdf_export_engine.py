# =========================================================
# 📄 Slide PDF Export Engine — v7.7R-BOD
# Converts Executive Presentation slides into boardroom-grade PDF
# Fully compatible with Executive Presentation, Archive Engine, and Dashboard
# =========================================================

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet


def export_slides_to_pdf(slides, filename="Fox_Valley_Executive_Presentation.pdf"):
    """
    Accepts list of slides (list of dicts with 'title' and 'content')
    Generates fully formatted PDF slide deck.
    """

    styles = getSampleStyleSheet()
    story = []

    for i, slide in enumerate(slides, start=1):
        # Slide Title
        story.append(Paragraph(f"<b>{i}. {slide['title']}</b>", styles["Title"]))
        story.append(Spacer(1, 12))

        # Slide Content
        content = slide["content"].replace("\n", "<br/>")
        story.append(Paragraph(content, styles["BodyText"]))

        # Add space and slide break
        story.append(PageBreak())

    # Build PDF
    doc = SimpleDocTemplate(
        filename,
        pagesize=LETTER,
        title="Fox Valley Executive Tactical Presentation"
    )
    doc.build(story)

    return filename
