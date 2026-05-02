"""RSS/Atom feed fetcher using feedparser."""

# TODO(P2): implement fetch_feed(url: str) -> list[RawItem]
# TODO(P2): implement fetch_all() -> list[RawItem]  (reads feeds.yaml)
# Rules: User-Agent header, timeout=15, max 3 retries (exponential backoff)
# Rules: strip HTML, max 600 char summary
# Rules: return [] on error (do not raise), log warning
