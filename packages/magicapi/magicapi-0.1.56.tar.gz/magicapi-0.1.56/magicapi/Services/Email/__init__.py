from typing import List
import smtplib
import ssl

from magicapi import settings


port, smtp_server = settings.email_port, settings.email_smtp_server
sender_email, sender_password = settings.sender_email, settings.sender_password
from magicapi.Decorators.background_tasks import run_in_background


def send_email(text_body: str, recipients: List[str], subject: str = None):
    if subject:
        text_body = f"Subject: {subject}\n\n{text_body}"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_password)
        for recipient in recipients:
            server.sendmail(sender_email, recipient, text_body)


@run_in_background
def send_email_in_background(
    text_body: str, recipients: List[str], subject: str = None
):
    send_email(text_body=text_body, recipients=recipients, subject=subject)


if __name__ == "__main__":
    send_email(
        subject="what do you know about Mactard Jones?",
        text_body="nothing, I hope",
        recipients=["fernando@basement.social"],
        # recipients=["kellycup8@gmail.com"],
    )
