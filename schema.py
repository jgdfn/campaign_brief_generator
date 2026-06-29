"""Exports the brief to a PDF, using reportlab."""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schema import BRIEF_FIELDS


def build_pdf_bytes(response_json: dict, campaign_title: str = "Campaign Brief") -> bytes:
    brief = response_json["brief"]
    buf = io.BytesIO()

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=18, textColor=colors.HexColor("#1F2937"), spaceAfter=14,
    )
    label_style = ParagraphStyle(
        "LabelStyle", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=11, spaceAfter=2, textColor=colors.HexColor("#111827"),
    )
    value_style = ParagraphStyle(
        "ValueStyle", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10, leading=14, spaceAfter=10,
    )
    missing_style = ParagraphStyle(
        "MissingStyle", parent=value_style, textColor=colors.HexColor("#B45309"),
        fontName="Helvetica-Oblique",
    )

    elements = [Paragraph(campaign_title, title_style), Spacer(1, 6)]

    for field in BRIEF_FIELDS:
        entry = brief.get(field, {"value": "Missing", "source_type": "Missing"})
        value = str(entry.get("value", "")).replace("\n", "<br/>")
        elements.append(Paragraph(field, label_style))
        style = missing_style if entry.get("source_type") == "Missing" else value_style
        elements.append(Paragraph(value, style))

    doc.build(elements)
    buf.seek(0)
    return buf.read()
