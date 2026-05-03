"""Recipient list loader — reads from Google Sheets, falls back to config.EMAIL_TO."""

import json
import logging

import structlog

from sinyra import config

log = structlog.get_logger()

_EMAIL_COL = 1   # "E-posta adresin?" column index
_AKTIF_COL = 6   # "AKTİF Mİ?" column index


def _from_sheet(sheet_id: str, gid: int, creds_json: str) -> list[str]:
    import gspread
    from google.oauth2.service_account import Credentials  # type: ignore[import-untyped]

    creds_dict: dict[str, object] = json.loads(creds_json)
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
    )
    gc = gspread.Client(auth=creds)
    ws = gc.open_by_key(sheet_id).get_worksheet_by_id(gid)
    rows: list[list[str]] = ws.get_all_values()

    emails: list[str] = []
    for row in rows[1:]:  # skip header
        if len(row) <= _EMAIL_COL:
            continue
        email = row[_EMAIL_COL].strip()
        aktif = (row[_AKTIF_COL].strip().upper() if len(row) > _AKTIF_COL else "")
        if email and aktif != "HAYIR":
            emails.append(email)

    log.info("recipients.sheet_loaded", count=len(emails), sheet_id=sheet_id)
    return emails


def load_recipients() -> list[str]:
    """Return active recipient emails. Sheets if configured, else config.EMAIL_TO."""
    sheet_id = config.GSHEET_ID
    creds_json = config.GOOGLE_CREDENTIALS_JSON

    if not sheet_id or not creds_json:
        log.info("recipients.using_env", count=len(config.EMAIL_TO))
        return config.EMAIL_TO

    try:
        return _from_sheet(sheet_id, config.GSHEET_GID, creds_json)
    except Exception as exc:
        logging.warning("recipients.sheet_error — falling back to EMAIL_TO: %s", exc)
        return config.EMAIL_TO
