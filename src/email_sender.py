from email.message import EmailMessage
import smtplib

def send_email_report(receiver_email, status, f0_value, deviations, repor_id):

    sender_email = "syedd8896@gmail.com"
    app_password = "oqza hwdo wuwi vgac"

    msg = EmailMessage()

    msg["Subject"] = f"Autoclave Validation Report - {status}"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Email Body
    msg.set_content(f"""
Dear Team,

Please find attached the Autoclave Validation Report.

Batch Status: {status}
F0 Value: {round(f0_value, 2)}

Remarks:
{'No deviations observed.' if len(deviations) == 0 else 'Deviations detected. Please review the report.'}

This is an automated system-generated report.

Regards,
Validation System
""")

    # Attach PDF
    with open("output/report.pdf", "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="Autoclave_Report.pdf"
        )

    # Send Email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)