# Built-in imports
import os
import smtplib
from email.mime.text import MIMEText

# Third-party imports


# Local imports


SMTP_SERVER = os.getenv("EMAIL_SMTP")
SMTP_PORT = int(os.getenv("EMAIL_PORT"))


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())

    return True
