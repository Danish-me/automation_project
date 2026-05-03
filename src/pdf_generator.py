from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os


def generate_pdf_report(df, status, f0_value, deviations, report_id, mode="validation"):

    # =========================
    # 🔹 SETUP
    # =========================
    os.makedirs("output", exist_ok=True)
    file_path = f"output/report_{report_id}.pdf"

    doc = SimpleDocTemplate(
        file_path,
        pagesize=landscape(letter),
        leftMargin=20,
        rightMargin=20
    )

    styles = getSampleStyleSheet()
    content = []

    # =========================
    # 🔹 DATE & TIME (AUTO)
    # =========================
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # =========================
    # 🔹 HEADER
    # =========================
    content.append(Paragraph("Autoclave Validation Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Report ID: {report_id}", styles["Normal"]))
    content.append(Paragraph(f"Date: {date_str}", styles["Normal"]))
    content.append(Paragraph(f"Time: {time_str}", styles["Normal"]))
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
    # 🔹 TEMPERATURE SUMMARY
    # =========================
    content.append(Paragraph("Temperature Summary", styles["Heading2"]))
    content.append(Spacer(1, 5))

    try:
        channel_cols = [col for col in df.columns if "channel" in col.lower()]

        if len(channel_cols) == 0:
            content.append(Paragraph("No temperature channels found", styles["Normal"]))

        else:
            latest_row = df.iloc[-1]

            if mode == "validation":
                # 12 probes
                for i, col in enumerate(channel_cols[:12], start=1):
                    temp = round(float(latest_row[col]), 2)
                    content.append(Paragraph(f"Probe {i}: {temp} °C", styles["Normal"]))

            elif mode == "routine":
                # Single probe
                temp = round(float(latest_row[channel_cols[0]]), 2)
                content.append(Paragraph(f"Temperature (Routine): {temp} °C", styles["Normal"]))

    except Exception as e:
        content.append(Paragraph(f"Temperature summary error: {str(e)}", styles["Normal"]))

    content.append(Spacer(1, 15))

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
    # 🔹 TABLE (FIXED CLEAN)
    # =========================
    content.append(Paragraph("Sample Data (Top 10 Rows)", styles["Heading2"]))
    content.append(Spacer(1, 5))

    try:
        cols = []

        # Date/time first priority
        for col in ["date", "time", "datetime"]:
            if col in df.columns:
                cols.append(col)

        # Channels (only once)
        channel_cols = [col for col in df.columns if "channel" in col.lower()]
        cols.extend(channel_cols)

        if len(cols) == 0:
            content.append(Paragraph("No valid columns found for table", styles["Normal"]))

        else:
            table_data = [cols] + df[cols].head(10).values.tolist()

            # Column width control
            col_widths = []
            for col in cols:
                if col in ["date", "time", "datetime"]:
                    col_widths.append(1.2 * inch)
                else:
                    col_widths.append(0.5 * inch)

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

    # =========================
    # 🔹 BUILD PDF
    # =========================
    doc.build(content)

    return file_path