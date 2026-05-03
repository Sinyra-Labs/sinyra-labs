"""Email dispatcher — factory selects provider from EMAIL_PROVIDER env."""

import logging

from pydantic import BaseModel

from sinyra import config
from sinyra.delivery.email.provider import EmailProvider
from sinyra.delivery.email.render import render_html, render_text
from sinyra.synthesis.brief import DailyBrief

logger = logging.getLogger(__name__)

_SUBJECT = "🧠 Günlük AI Ürün Radarı"


class SendStats(BaseModel):
    attempted: int
    succeeded: int
    failed: int


def _get_provider() -> EmailProvider:
    provider_name = config.EMAIL_PROVIDER
    if provider_name == "gmail_smtp":
        from sinyra.delivery.email.gmail_smtp import GmailSmtpProvider

        return GmailSmtpProvider()
    raise ValueError(f"Bilinmeyen EMAIL_PROVIDER: {provider_name!r}")


def send_brief(brief: DailyBrief, recipients: list[str]) -> SendStats:
    if not recipients:
        logger.warning("email.send_brief: no recipients, skipping")
        return SendStats(attempted=0, succeeded=0, failed=0)

    html = render_html(brief)
    text = render_text(brief)
    subject = f"{_SUBJECT} — {brief.date_tr}"

    provider = _get_provider()
    attempted = len(recipients)
    succeeded = 0
    failed = 0

    for to in recipients:
        try:
            provider.send(to=to, subject=subject, html=html, text=text)
            succeeded += 1
        except Exception as exc:
            logger.error("email.dispatch_error to=%s error=%s", to, exc)
            failed += 1

    logger.info(
        "email.send_brief.done attempted=%d succeeded=%d failed=%d",
        attempted,
        succeeded,
        failed,
    )
    return SendStats(attempted=attempted, succeeded=succeeded, failed=failed)
