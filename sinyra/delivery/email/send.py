"""Email dispatcher — factory selects provider from EMAIL_PROVIDER env."""

from pydantic import BaseModel

from sinyra import config
from sinyra.synthesis.brief import DailyBrief


class SendStats(BaseModel):
    attempted: int
    succeeded: int
    failed: int


def send_brief(brief: DailyBrief, recipients: list[str]) -> SendStats:
    # TODO(P5): instantiate provider based on config.EMAIL_PROVIDER
    #   "gmail_smtp" → GmailSmtpProvider
    #   (future) "resend" → ResendProvider
    # TODO(P5): render HTML + text, iterate over recipients, collect stats
    raise NotImplementedError
