from __future__ import annotations

from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT = DOCS / "YellowSphere_Manual.pdf"

DOC_ORDER = [
    "Recovery.txt",
    "OpSec.txt",
    "LinuxRelease.txt",
    "BuildReproducability.txt",
    "Passphrase.txt",
    "FileFormat.txt",
    "Encryption.txt",
    "Derivation.txt",
    "QR.txt",
    "TestVectors.txt",
]

SCREENSHOTS = [
    ("yellowsphere-main-recovery.png", "Figure 1. Main recovery workspace with test-vector mnemonic validation controls."),
    ("yellowsphere-derived-output.png", "Figure 2. Derived output table after address derivation, with output tabs and export controls."),
    ("yellowsphere-qr-export.png", "Figure 3. QR Export modal generating an address QR code without external services."),
    ("yellowsphere-settings.png", "Figure 4. Settings dialog with theme selection and advanced recovery preferences."),
    ("yellowsphere-light.png", "Figure 5. Light theme interface."),
    ("yellowsphere-dark.png", "Figure 6. Dark theme interface."),
    ("yellowsphere-dark-plus.png", "Figure 7. Dark+ theme interface."),
    ("yellowsphere-terminal.png", "Figure 8. Terminal theme interface."),
]


def clean_text(text: str) -> str:
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
        "\u00d7": "x",
        "\u2265": ">=",
        "\u2208": "in",
        "\u00b7": ".",
        "\ufffd": "?",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def first_heading(lines: list[str], index: int) -> tuple[str | None, int]:
    if index + 1 >= len(lines):
        return None, 0
    underline = lines[index + 1].strip()
    if lines[index].strip() and len(underline) >= 3:
        if set(underline) <= {"="}:
            return lines[index].strip(), 1
        if set(underline) <= {"-"}:
            return lines[index].strip(), 2
    return None, 0


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ManualTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=29,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "ManualSubtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4B5563"),
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "ManualH1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#111827"),
            spaceBefore=8,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "ManualH2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#1F2937"),
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "ManualBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#111827"),
            spaceAfter=5,
        ),
        "caption": ParagraphStyle(
            "ManualCaption",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#4B5563"),
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=10,
        ),
        "code": ParagraphStyle(
            "ManualCode",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.2,
            leading=8.8,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#F3F4F6"),
            borderColor=colors.HexColor("#D1D5DB"),
            borderWidth=0.25,
            borderPadding=5,
            leftIndent=0,
            rightIndent=0,
            spaceBefore=4,
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "ManualBullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=11.5,
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=3,
        ),
        "note": ParagraphStyle(
            "ManualNote",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.7,
            leading=11.5,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#FEF3C7"),
            borderColor=colors.HexColor("#F59E0B"),
            borderWidth=0.5,
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=8,
        ),
    }


def classify_block(block: list[str]) -> str:
    stripped = [line.rstrip() for line in block]
    if not stripped:
        return "blank"
    non_empty = [line for line in stripped if line.strip()]
    if not non_empty:
        return "blank"
    if all(re.match(r"^\s*(-|\d+\.|\[[ xX]\])\s+", line) for line in non_empty):
        return "list"
    if any(line.startswith("  ") or line.startswith("\t") for line in stripped):
        return "code"
    if len(non_empty) >= 2 and any("  " in line.strip() for line in non_empty):
        return "code"
    return "para"


def add_text_doc(story, path: Path, styles):
    text = clean_text(path.read_text(encoding="utf-8"))
    lines = text.splitlines()
    i = 0
    pending: list[str] = []

    def flush():
        nonlocal pending
        if not pending:
            return
        kind = classify_block(pending)
        if kind == "list":
            items = []
            for line in pending:
                content = re.sub(r"^\s*(-|\d+\.|\[[ xX]\])\s+", "", line).strip()
                items.append(ListItem(Paragraph(escape(content), styles["bullet"])))
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=18, bulletFontSize=5))
        elif kind == "code":
            story.append(Preformatted(clean_text("\n".join(pending)).rstrip(), styles["code"], maxLineLength=92))
        elif kind == "para":
            paragraph = " ".join(line.strip() for line in pending if line.strip())
            style = styles["note"] if paragraph.startswith(("Note:", "Security note:", "Desktop wrapper requirement:")) else styles["body"]
            story.append(Paragraph(escape(paragraph), style))
        pending = []

    while i < len(lines):
        heading, level = first_heading(lines, i)
        if heading:
            flush()
            story.append(Paragraph(escape(heading), styles["h1" if level == 1 else "h2"]))
            i += 2
            continue
        if not lines[i].strip():
            flush()
        else:
            pending.append(lines[i])
        i += 1
    flush()


def add_screenshots(story, styles):
    story.append(PageBreak())
    story.append(Paragraph("Interface Guide", styles["h1"]))
    story.append(
        Paragraph(
            "The screenshots below show the primary user-facing layout and theme variants. "
            "The HTML application is the canonical GUI surface. PySide6 and Tauri package "
            "the same interface for desktop use, so the screenshots apply to all GUI editions.",
            styles["body"],
        )
    )
    max_width = 6.7 * inch
    max_height = 3.2 * inch
    for filename, caption in SCREENSHOTS:
        image_path = DOCS / "screenshots" / filename
        if not image_path.exists():
            continue
        img = Image(str(image_path))
        scale = min(max_width / img.imageWidth, max_height / img.imageHeight)
        img.drawWidth = img.imageWidth * scale
        img.drawHeight = img.imageHeight * scale
        story.append(KeepTogether([img, Paragraph(escape(caption), styles["caption"])]))


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(doc.leftMargin, 0.45 * inch, "YellowSphere v1.6.6 User Guide")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="YellowSphere v1.6.6 User Guide",
        author="YellowSphere",
    )

    story = [
        Spacer(1, 1.35 * inch),
        Paragraph("YellowSphere v1.6.6", styles["title"]),
        Paragraph("User Guide and Technical Reference", styles["subtitle"]),
        Paragraph(
            "Offline BIP39/BIP32 recovery, encrypted seed backup, QR export, "
            "file-format reference, and operational security procedures.",
            styles["subtitle"],
        ),
        Spacer(1, 0.2 * inch),
        Table(
            [
                ["Primary GUI", "Standalone HTML application"],
                ["Desktop GUI", "PySide6 WebEngine wrapper"],
                ["Desktop Package", "Tauri wrapper with native export bridge"],
                ["CLI", "Python derivation and export interface"],
                ["Generated", "June 18, 2026"],
            ],
            colWidths=[1.6 * inch, 4.7 * inch],
            style=TableStyle(
                [
                    ("FONT", (0, 0), (-1, -1), "Helvetica", 8),
                    ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#374151")),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F9FAFB")),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D1D5DB")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            ),
        ),
        PageBreak(),
    ]

    add_text_doc(story, DOCS / "UserGuide.txt", styles)
    add_screenshots(story, styles)

    for doc_name in DOC_ORDER:
        story.append(PageBreak())
        add_text_doc(story, DOCS / doc_name, styles)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


if __name__ == "__main__":
    build()
