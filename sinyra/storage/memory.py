"""Seen-items store for deduplication."""

# TODO(P3): implement SeenStore class
#   - backed by SQLite at config.DB_PATH
#   - is_seen(hash: str) -> bool
#   - remember(items: list[RawItem]) -> int  (returns count inserted)
#   - TTL: 14 days; prune on startup
#   - all timestamps UTC, timezone-aware (datetime.now(UTC))
