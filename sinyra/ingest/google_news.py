"""Google News RSS query helper."""

import urllib.parse

import structlog

from sinyra.ingest.rss import fetch_feed
from sinyra.normalize.schema import RawItem

log = structlog.get_logger(__name__)

_GNEWS_BASE = "https://news.google.com/rss/search"


def _build_url(query: str) -> str:
    params = urllib.parse.urlencode({"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"})
    return f"{_GNEWS_BASE}?{params}"


def fetch_gnews(query: str, source_name: str = "Google News") -> list[RawItem]:
    """Fetch items from Google News RSS for a given search query."""
    if not query.strip():
        log.warning("gnews_empty_query", source=source_name)
        return []
    url = _build_url(query)
    log.debug("gnews_fetch", query=query, source=source_name)
    return fetch_feed(url, source_name=source_name)
