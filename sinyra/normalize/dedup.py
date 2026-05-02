"""Hash-based deduplication against the seen-items store."""

import hashlib
from datetime import UTC, datetime, timedelta

from sinyra import config
from sinyra.normalize.schema import RawItem
from sinyra.storage.memory import SeenStore


def compute_hash(item: RawItem) -> str:
    return hashlib.md5(f"{item.title}|{item.link}".encode()).hexdigest()


def dedup(
    items: list[RawItem],
    store: SeenStore,
    hours_lookback: int | None = None,
) -> tuple[list[RawItem], dict[str, int]]:
    lookback = hours_lookback if hours_lookback is not None else config.LOOKBACK_HOURS
    cutoff = datetime.now(UTC) - timedelta(hours=lookback)

    kept: list[RawItem] = []
    too_old = 0
    seen = 0

    for item in items:
        if item.pub_date is not None and item.pub_date < cutoff:
            too_old += 1
            continue
        h = compute_hash(item)
        if store.is_seen(h):
            seen += 1
            continue
        kept.append(item)

    stats: dict[str, int] = {
        "total": len(items),
        "kept": len(kept),
        "too_old": too_old,
        "seen": seen,
    }
    return kept, stats
