"""RSS/Atom feed fetcher using feedparser + httpx."""

import html
import re
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import feedparser
import httpx
import structlog
import yaml

from sinyra.normalize.schema import RawItem

log = structlog.get_logger(__name__)

_USER_AGENT = "Sinyra-Labs/0.1 (+https://github.com/sinyra-labs/sinyra-labs)"
_HEADERS: dict[str, str] = {"User-Agent": _USER_AGENT}
_TIMEOUT = 15.0
_MAX_RETRIES = 3
_SUMMARY_MAX_CHARS = 600


def _strip_html(text: str) -> str:
    """Strip HTML tags and unescape HTML entities, collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def _parse_date(entry: Any) -> datetime | None:
    """Convert feedparser's published_parsed (UTC struct_time) to timezone-aware datetime."""
    parsed = getattr(entry, "published_parsed", None)
    if parsed is None:
        return None
    try:
        return datetime(*parsed[:6]).replace(tzinfo=UTC)
    except (ValueError, TypeError):
        return None


def _fetch_raw(url: str) -> bytes:
    """GET a URL with exponential-backoff retry. Raises on final failure."""
    last_exc: Exception = RuntimeError("no attempts made")
    for attempt in range(_MAX_RETRIES):
        try:
            resp = httpx.get(url, headers=_HEADERS, timeout=_TIMEOUT, follow_redirects=True)
            resp.raise_for_status()
            return resp.content
        except (httpx.HTTPStatusError, httpx.RequestError) as exc:
            last_exc = exc
            if attempt < _MAX_RETRIES - 1:
                sleep_s = 2**attempt
                log.warning("feed_fetch_retry", url=url, attempt=attempt + 1, sleep_s=sleep_s)
                time.sleep(sleep_s)
    raise last_exc


def _entries_to_items(
    entries: list[Any],
    source_name: str,
    hint_company: str | None,
) -> list[RawItem]:
    """Convert feedparser entry objects to RawItem list, skipping malformed entries."""
    items: list[RawItem] = []
    for entry in entries:
        title: str = (getattr(entry, "title", "") or "").strip()
        link: str = (getattr(entry, "link", "") or "").strip()
        if not title or not link:
            continue
        raw_summary: str = (
            getattr(entry, "summary", None) or getattr(entry, "description", "") or ""
        )
        items.append(
            RawItem(
                title=title,
                link=link,
                summary=_strip_html(raw_summary)[:_SUMMARY_MAX_CHARS],
                pub_date=_parse_date(entry),
                source_name=source_name,
                hint_company=hint_company,
            )
        )
    return items


def fetch_feed(
    url: str,
    source_name: str = "",
    hint_company: str | None = None,
) -> list[RawItem]:
    """Fetch and parse a single RSS/Atom feed. Returns [] on any error (never raises)."""
    try:
        raw = _fetch_raw(url)
    except Exception as exc:
        log.warning("feed_fetch_failed", url=url, source=source_name, error=str(exc))
        return []

    parsed = feedparser.parse(raw)
    items = _entries_to_items(parsed.entries, source_name, hint_company)
    log.debug("feed_fetched", url=url, source=source_name, item_count=len(items))
    return items


def fetch_all() -> list[RawItem]:
    """Fetch all feeds defined in feeds.yaml. Aggregates results from all sources."""
    feeds_path = Path(__file__).parent / "feeds.yaml"
    with feeds_path.open() as fh:
        cfg: dict[str, Any] = yaml.safe_load(fh)

    all_items: list[RawItem] = []
    for feed in cfg.get("feeds", []):
        feed_type: str = feed.get("type", "rss")
        name: str = feed.get("name", "")
        company: str | None = feed.get("company")

        if feed_type == "gnews":
            from sinyra.ingest.google_news import fetch_gnews  # avoid top-level circular import

            query: str = feed.get("query", "")
            items = fetch_gnews(query, source_name=name) if query else []
        else:
            feed_url: str = feed.get("url", "")
            items = fetch_feed(feed_url, source_name=name, hint_company=company) if feed_url else []

        all_items.extend(items)

    log.info("ingest_complete", total_items=len(all_items))
    return all_items
