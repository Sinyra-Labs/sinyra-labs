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
        # TODO(P5): implement full send logic
        # - smtplib.SMTP_SSL("smtp.gmail.com", 465)
        # - login with config.GMAIL_ADDRESS + config.GMAIL_APP_PASSWORD
        # - MIMEMultipart("alternative") with text + html parts
        # - on SMTPException: log error, do NOT re-raise (continue to next recipient)
        raise NotImplementedError
