from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
import os
from reportlab.lib.pagesizes import letter, landscape

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
    doc = SimpleDocTemplate(
    file_path,
    pagesize=landscape(letter),
    leftMargin=20,
    rightMargin=20
    )
    
    styles = getSampleStyleSheet()
    content = []

    # 👉 (yahan tumhara content + table code rahega)

    doc.build(content)

    return file_path   # ✅ VERY IMPORTANT

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
        from reportlab.lib import colors
        from reportlab.platypus import Table, TableStyle
        from reportlab.lib.units import inch

        # 🔹 Select only useful columns (channels + time)
        cols = [col for col in df.columns if "channel" in col.lower()]
        if "time" in df.columns:
            cols.insert(0, "time")

        # 🔹 Prepare table data
        table_data = [cols] + df[cols].head(10).values.tolist()

        # 🔹 Column widths (Time wide, others compact)
        col_widths = [0.8 * inch] + [0.5 * inch] * (len(cols) - 1)

        # 🔹 Create table
        table = Table(table_data, colWidths=col_widths)

        # 🔹 Styling
        table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 6),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))

        # 🔹 Add to PDF
        content.append(table)

    except Exception as e:
        content.append(
            Paragraph(f"Table error: {str(e)}", styles["Normal"])
        )

        # =========================
        # 🔹 BUILD PDF
        # =========================
        doc.build(content)

    # ✅ RETURN FILE PATH (VERY IMPORTANT)
    return file_path