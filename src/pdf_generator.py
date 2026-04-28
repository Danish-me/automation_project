from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(df, status, f0_value, deviations, report_id):

    doc = SimpleDocTemplate("output/report.pdf")
    styles = getSampleStyleSheet()
    content = []

    # Header
    content.append(Paragraph("XYZ Pharma Pvt Ltd", styles["Title"]))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"Report ID: {report_id}", styles["Normal"]))

    # Summary
    content.append(Paragraph(f"Batch Status: {status}", styles["Normal"]))
    content.append(Paragraph(f"F0 Value: {round(f0_value,2)}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # Deviations
    content.append(Paragraph("Deviations:", styles["Heading2"]))
    if deviations:
        for d in deviations:
            content.append(Paragraph(d, styles["Normal"]))
    else:
        content.append(Paragraph("No deviations", styles["Normal"]))

    content.append(Spacer(1, 15))

    # Graph
    content.append(Paragraph("Temperature Graph:", styles["Heading2"]))
    content.append(Image("output/temperature_graph.png", width=400, height=200))

    content.append(Spacer(1, 15))

    # Raw Data (Top 10 rows)
    content.append(Paragraph("Sample Raw Data:", styles["Heading2"]))

    table_data = [df.columns.tolist()] + df.head(10).values.tolist()
    table = Table(table_data)

    content.append(table)

    doc.build(content)
    file_path = f"output/report_{report_id}.pdf"