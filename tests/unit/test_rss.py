"""Unit tests for sinyra.ingest.rss."""

from datetime import UTC
from unittest.mock import patch

import pytest

from sinyra.ingest.rss import _strip_html, fetch_feed

# ---------------------------------------------------------------------------
# Inline RSS fixture — used by both the VCR cassette and monkeypatch tests
# ---------------------------------------------------------------------------
_SAMPLE_RSS: bytes = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test AI Feed</title>
    <link>https://example-feed.test</link>
    <item>
      <title>OpenAI launches GPT-5</title>
      <link>https://example-feed.test/gpt5</link>
      <description>&lt;p&gt;OpenAI today announced GPT-5.&lt;/p&gt;</description>
      <pubDate>Mon, 15 Jan 2024 10:00:00 +0000</pubDate>
    </item>
    <item>
      <title>Anthropic releases Claude 4</title>
      <link>https://example-feed.test/claude4</link>
      <description>Anthropic released Claude 4 with extended context.</description>
      <pubDate>Mon, 15 Jan 2024 11:00:00 +0000</pubDate>
    </item>
  </channel>
</rss>
"""


# ---------------------------------------------------------------------------
# VCR cassette test (pytest-recording — cassette in cassettes/ subdirectory)
# ---------------------------------------------------------------------------
@pytest.mark.vcr
def test_fetch_feed_with_cassette() -> None:
    """fetch_feed parses a pre-recorded RSS response via VCR cassette."""
    items = fetch_feed("https://example-feed.test/rss", source_name="Test Feed")
    assert len(items) == 2
    assert items[0].title == "OpenAI launches GPT-5"
    assert items[0].link == "https://example-feed.test/gpt5"
    assert items[0].source_name == "Test Feed"


# ---------------------------------------------------------------------------
# Monkeypatch tests — fast, no network, no VCR overhead
# ---------------------------------------------------------------------------
def test_fetch_feed_happy_path() -> None:
    """fetch_feed returns correct RawItems from valid RSS bytes."""
    with patch("sinyra.ingest.rss._fetch_raw", return_value=_SAMPLE_RSS):
        items = fetch_feed(
            "https://example-feed.test/rss",
            source_name="Test Feed",
            hint_company="test-co",
        )

    assert len(items) == 2

    first = items[0]
    assert first.title == "OpenAI launches GPT-5"
    assert first.link == "https://example-feed.test/gpt5"
    assert first.source_name == "Test Feed"
    assert first.hint_company == "test-co"
    assert first.pub_date is not None
    assert first.pub_date.tzinfo is UTC
    assert "<p>" not in first.summary  # HTML stripped
    assert "GPT-5" in first.summary


def test_fetch_feed_returns_empty_on_http_error() -> None:
    """fetch_feed returns [] on HTTP failure and does not raise."""
    import httpx

    with patch("sinyra.ingest.rss._fetch_raw", side_effect=httpx.ConnectError("timeout")):
        items = fetch_feed("https://broken-feed.test/rss")

    assert items == []


def test_fetch_feed_skips_entries_without_title_or_link() -> None:
    """Entries missing title or link are silently dropped."""
    broken_rss: bytes = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item><title>No link item</title></item>
    <item><link>https://example.com/no-title</link></item>
    <item>
      <title>Valid item</title>
      <link>https://example.com/valid</link>
    </item>
  </channel>
</rss>
"""
    with patch("sinyra.ingest.rss._fetch_raw", return_value=broken_rss):
        items = fetch_feed("https://example.com/feed")

    assert len(items) == 1
    assert items[0].title == "Valid item"


# ---------------------------------------------------------------------------
# _strip_html unit tests
# ---------------------------------------------------------------------------
def test_strip_html_removes_tags() -> None:
    assert _strip_html("<p>Hello <b>world</b></p>") == "Hello world"


def test_strip_html_unescapes_entities() -> None:
    assert _strip_html("&amp; &lt;p&gt;") == "& <p>"


def test_strip_html_collapses_whitespace() -> None:
    assert _strip_html("  extra   spaces  ") == "extra spaces"


def test_strip_html_passthrough_plain_text() -> None:
    assert _strip_html("No tags here") == "No tags here"
