"""Convert a plain-text / markdown file to a simple PDF using reportlab."""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT


def md_to_pdf(src: Path, dst: Path) -> None:
    styles = getSampleStyleSheet()
    heading = ParagraphStyle(
        "heading",
        parent=styles["Normal"],
        fontSize=13,
        leading=18,
        spaceBefore=8,
        spaceAfter=2,
        fontName="Helvetica-Bold",
    )
    subheading = ParagraphStyle(
        "subheading",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        spaceBefore=6,
        spaceAfter=2,
        fontName="Helvetica-Bold",
    )
    body = ParagraphStyle(
        "body",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
    )

    doc = SimpleDocTemplate(
        str(dst),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    story = []
    for line in src.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 4))
        elif stripped.startswith("## "):
            story.append(Paragraph(stripped[3:], subheading))
        elif stripped.startswith("# "):
            story.append(Paragraph(stripped[2:], heading))
        else:
            # escape XML special chars for reportlab
            safe = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe, body))

    doc.build(story)
    print(f"Written: {dst}")


if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("documents/starbase_omega_policy.md")
    dst = src.with_suffix(".pdf")
    md_to_pdf(src, dst)
