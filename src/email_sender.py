import smtplib
from email.message import EmailMessage
import os

def send_email_report(receiver_email):

    sender_email = "syedd8896@gmail.com"
    app_password = "oqza hwdo wuwi vgac"

    msg = EmailMessage()
    msg["Subject"] = "Autoclave Validation Report"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content("Please find attached validation report and graph.")

    # Attach Excel
    with open("output/report.xlsx", "rb") as f:
        msg.add_attachment(f.read(), maintype="application",
                           subtype="octet-stream", filename="report.xlsx")

    # Attach Graph
    with open("output/temperature_graph.png", "rb") as f:
        msg.add_attachment(f.read(), maintype="image",
                           subtype="png", filename="temperature_graph.png")

    # Send Email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

    print("Email sent successfully ✅")