from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import os
from datetime import datetime

REPORT_FOLDER = "reports"

os.makedirs(REPORT_FOLDER, exist_ok=True)


def list_to_text(items):
    if not items:
        return "None"

    return "<br/>".join([f"• {item}" for item in items])


def generate_pdf(result):

    filename = f"SentinelAI_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    filepath = os.path.join(REPORT_FOLDER, filename)

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("SentinelAI Malware Analysis Report", styles["Title"])
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            f"<b>Risk Score:</b> {result['risk_score']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Severity:</b> {result['severity']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Malware Family:</b> {result['malware_family']}",
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>Behavior Summary</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(result["behavior_summary"], styles["Normal"])
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>Suspicious Permissions</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            list_to_text(result["suspicious_permissions"]),
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>Possible Data Theft</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            list_to_text(result["possible_data_theft"]),
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>MITRE ATT&CK</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            list_to_text(result["mitre_attack"]),
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>OWASP Mobile Risks</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            list_to_text(result["owasp_mobile"]),
            styles["Normal"]
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph("<b>Recommendations</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            list_to_text(result["recommendation"]),
            styles["Normal"]
        )
    )

    doc.build(story)

    return filepath