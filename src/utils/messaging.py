# Built-in imports
import os
import smtplib
from email.mime.text import MIMEText

# Third-party imports


# Local imports
from base.config import logger
from base.exception import BillyResponse

EMAIL_SMTP = os.getenv("EMAIL_SMTP")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(subject: str, body: str, recipient: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join([recipient])
    try:
        with smtplib.SMTP_SSL(EMAIL_SMTP, EMAIL_PORT) as smtp_server:
            smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp_server.sendmail(EMAIL_ADDRESS, [recipient], msg.as_string())
        return BillyResponse.SUCCESS

    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return BillyResponse.SERVER_ERROR
