from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf_report(df, status, f0_value, deviations, report_id):
    """
    Generate Autoclave Validation PDF Report
    Compatible with Streamlit + Cloud Deployment
    """

    # ✅ Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # ✅ Dynamic file path
    file_path = f"output/report_{report_id}.pdf"

    # ✅ Create document
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []

    # =========================
    # 🔹 HEADER
    # =========================
    content.append(Paragraph("Autoclave Validation Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Report ID:</b> {report_id}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # =========================
    # 🔹 SUMMARY
    # =========================
    content.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    content.append(Spacer(1, 5))

    content.append(Paragraph(f"Batch Status: {status}", styles["Normal"]))
    content.append(Paragraph(f"F0 Value: {round(f0_value, 2)}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # =========================
    # 🔹 DEVIATIONS
    # =========================
    content.append(Paragraph("<b>Deviations</b>", styles["Heading2"]))
    content.append(Spacer(1, 5))

    if deviations:
        for d in deviations:
            content.append(Paragraph(d, styles["Normal"]))
    else:
        content.append(Paragraph("No deviations observed", styles["Normal"]))

    content.append(Spacer(1, 15))

    # =========================
    # 🔹 GRAPH SECTION
    # =========================
    content.append(Paragraph("<b>Temperature Profile</b>", styles["Heading2"]))
    content.append(Spacer(1, 5))

    graph_path = "output/temperature_graph.png"

    if os.path.exists(graph_path):
        try:
            content.append(Image(graph_path, width=450, height=250))
        except Exception:
            content.append(Paragraph("Graph could not be loaded", styles["Normal"]))
    else:
        content.append(Paragraph("Graph not available", styles["Normal"]))

    content.append(Spacer(1, 15))

    # =========================
    # 🔹 RAW DATA SAMPLE
    # =========================
    content.append(Paragraph("<b>Sample Data (Top 10 Rows)</b>", styles["Heading2"]))
    content.append(Spacer(1, 5))

    try:
        table_data = [df.columns.tolist()] + df.head(10).values.tolist()
        table = Table(table_data)
        content.append(table)
    except Exception:
        content.append(Paragraph("Unable to render table data", styles["Normal"]))

    # =========================
    # 🔹 BUILD PDF
    # =========================
    doc.build(content)

    # ✅ RETURN FILE PATH (VERY IMPORTANT)
    return file_path