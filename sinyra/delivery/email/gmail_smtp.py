"""Gmail SMTP provider using smtplib (stdlib, no extra package needed)."""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sinyra import config

logger = logging.getLogger(__name__)


class GmailSmtpProvider:
    """Sends email via Gmail SMTP on port 465 (SSL) with App Password auth."""

    def send(self, to: str, subject: str, html: str, text: str) -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{config.EMAIL_FROM_NAME} <{config.GMAIL_ADDRESS}>"
        msg["To"] = to
        msg.attach(MIMEText(text, "plain", "utf-8"))
        msg.attach(MIMEText(html, "html", "utf-8"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(config.GMAIL_ADDRESS, config.GMAIL_APP_PASSWORD)
                server.sendmail(config.GMAIL_ADDRESS, to, msg.as_bytes())
            logger.info("email.sent to=%s", to)
        except smtplib.SMTPException as exc:
            logger.error("email.failed to=%s error=%s", to, exc)
            # do NOT re-raise — allow pipeline to continue to next recipient
