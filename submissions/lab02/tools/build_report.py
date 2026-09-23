"""Render the completed report template; local authoring tool, not submitted."""
import argparse
import json
import re
import tempfile
from html import escape
from pathlib import Path

import pymupdf
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
# Relative column widths per table shape (number of columns).
COLUMN_FRACTIONS = {
    3: [0.21, 0.37, 0.42],
    4: [0.37, 0.21, 0.21, 0.21],
    5: [0.32, 0.17, 0.17, 0.17, 0.17],
}


def inline(text):
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"`(.+?)`", r"\1", text)


def build(preview=False):
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    identity_missing = results["student_id"] == "00000000" or results["name"] == "None"
    if identity_missing and not preview:
        raise ValueError("Actual student ID and name are required before final packaging.")
    values = {**results, **results["metrics"]}
    if preview:
        values["student_id"] = "PREVIEW"
        values["name"] = "student details pending"
    markdown = (ROOT / "report_template.md").read_text(encoding="utf-8").format(**values)

    font_dir = Path("C:/Windows/Fonts")
    pdfmetrics.registerFont(TTFont("Report", str(font_dir / "malgun.ttf")))
    pdfmetrics.registerFont(TTFont("ReportBold", str(font_dir / "malgunbd.ttf")))
    pdfmetrics.registerFontFamily("Report", normal="Report", bold="ReportBold",
                                  italic="Report", boldItalic="ReportBold")
    body = ParagraphStyle("body", fontName="Report", fontSize=9, leading=12.5,
                          spaceAfter=7, textColor=colors.HexColor("#23323A"))
    title = ParagraphStyle("title", parent=body, fontName="ReportBold", fontSize=15,
                           leading=20, spaceAfter=14)
    heading = ParagraphStyle("heading", parent=body, fontName="ReportBold", fontSize=11,
                             leading=15, spaceBefore=8, spaceAfter=7, keepWithNext=True)
    caption = ParagraphStyle("caption", parent=body, fontSize=8.5, leading=11.5,
                             spaceAfter=9)
    cell = ParagraphStyle("cell", parent=body, fontSize=8, leading=10.5, spaceAfter=0)
    width = A4[0] - 88
    story = []
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == "<!-- pagebreak -->":
            story.append(PageBreak())
        elif line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), title))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), heading))
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [v.strip() for v in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"[-: ]+", v) for v in row):
                    rows.append([Paragraph(inline(v), cell) for v in row])
                i += 1
            fractions = COLUMN_FRACTIONS[len(rows[0])]
            table = Table(rows, colWidths=[width * f for f in fractions], repeatRows=1,
                          hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3EFF1")),
                ("LINEBELOW", (0, 0), (-1, 0), 0.7, colors.HexColor("#277C8E")),
                ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#D5DFE2")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.extend([table, Spacer(1, 7)])
            continue
        elif line.startswith("!["):
            relative = re.search(r"\]\((.+)\)", line).group(1)
            picture = Image(str(ROOT / relative))
            picture_width = width * 0.82
            picture.drawHeight *= picture_width / picture.drawWidth
            picture.drawWidth = picture_width
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            figure_caption = Paragraph(inline(lines[j].strip()), caption)
            story.append(KeepTogether([picture, Spacer(1, 5), figure_caption]))
            i = j
        else:
            style = caption if line.startswith("**Table") else body
            story.append(Paragraph(inline(line), style))
        i += 1

    preview_dir = Path(tempfile.gettempdir()) / "machine-learning-project" / "lab02-pdf-preview"
    out_dir = preview_dir if preview else ROOT
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / ("report_preview.pdf" if preview else "report.pdf")

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D5DFE2"))
        canvas.line(44, 35, A4[0] - 44, 35)
        canvas.setFont("Report", 8)
        canvas.setFillColor(colors.HexColor("#53656E"))
        canvas.drawString(44, 23, "Lab 2 | Clinic no-show classification and wait-time regression | Seed 42")
        canvas.drawRightString(A4[0] - 44, 23, str(doc.page))
        canvas.restoreState()

    doc = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=44, leftMargin=44,
                            topMargin=36, bottomMargin=46,
                            title="Lab 2 - Classification and regression", author=results["name"])
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    reader = PdfReader(output)
    assert len(reader.pages) <= 3, f"Report has {len(reader.pages)} pages"
    for page in reader.pages:
        assert len(page.extract_text()) > 100, "Report must contain selectable text"
    render_dir = preview_dir
    render_dir.mkdir(parents=True, exist_ok=True)
    pdf = pymupdf.open(output)
    for number, page in enumerate(pdf, 1):
        page.get_pixmap(matrix=pymupdf.Matrix(1.4, 1.4)).save(render_dir / f"page-{number}.png")
    print(f"Report: {output} ({len(reader.pages)} text-based pages); previews in {render_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    build(parser.parse_args().preview)
