from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

# print("PDF generation started")
# print("Rows:", len(df))
# print("Columns:", df.columns)

def generate_pdf_report(df, status, f0_value, deviations, report_id):

    # ✅ Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # ✅ File path
    file_path = f"output/report_{report_id}.pdf"

    # ✅ Document setup
    doc = SimpleDocTemplate(
        file_path,
        pagesize=landscape(letter),
        leftMargin=20,
        rightMargin=20
    )

    styles = getSampleStyleSheet()
    content = []

    # =========================
    # 🔹 HEADER
    # =========================
    content.append(Paragraph("Autoclave Validation Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Report ID: {report_id}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # =========================
    # 🔹 SUMMARY
    # =========================
    content.append(Paragraph("Summary", styles["Heading2"]))
    content.append(Spacer(1, 5))

    content.append(Paragraph(f"Batch Status: {status}", styles["Normal"]))
    content.append(Paragraph(f"F0 Value: {round(f0_value, 2)}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # =========================
    # 🔹 DEVIATIONS
    # =========================
    content.append(Paragraph("Deviations", styles["Heading2"]))
    content.append(Spacer(1, 5))

    if deviations:
        for d in deviations:
            content.append(Paragraph(d, styles["Normal"]))
    else:
        content.append(Paragraph("No deviations observed", styles["Normal"]))

    content.append(Spacer(1, 15))

    # =========================
    # 🔹 GRAPH
    # =========================
    content.append(Paragraph("Temperature Profile", styles["Heading2"]))
    content.append(Spacer(1, 5))

    graph_path = "output/temperature_graph.png"

    if os.path.exists(graph_path):
        content.append(Image(graph_path, width=450, height=250))
    else:
        content.append(Paragraph("Graph not available", styles["Normal"]))

    content.append(Spacer(1, 15))

    # =========================
    # 🔹 TABLE (FIXED)
    # =========================
    content.append(Paragraph("Sample Data (Top 10 Rows)", styles["Heading2"]))
    content.append(Spacer(1, 5))

    try:
        # 🔹 Select channels dynamically
        cols = [col for col in df.columns if "channel" in col.lower()]
        if "date" in df.columns:
                cols.append("date")

        if "time" in df.columns:
            cols.append("time")

        if "datetime" in df.columns:
            cols.append("datetime")

        # 🔹 Add all temperature channels
        channel_cols = [col for col in df.columns if "channel" in col.lower()]
        cols.extend(channel_cols)

        # 🔹 Prepare table
        table_data = [cols] + df[cols].head(10).values.tolist()

        # 🔹 Column width handling
        from reportlab.lib.units import inch

        col_widths = []
        for col in cols:
            if col in ["date", "time", "datetime"]:
                col_widths.append(1.2 * inch)   # wider
            else:
                col_widths.append(0.5 * inch)   # compact

        table = Table(table_data, colWidths=col_widths)

        table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 6),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))

        content.append(table)

    except Exception as e:
        content.append(Paragraph(f"Table error: {str(e)}", styles["Normal"]))

    print("Content length:", len(content))

    # =========================
    # 🔹 BUILD PDF
    # =========================
    doc.build(content)

    return file_path