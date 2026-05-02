GÖREV: sinyra/storage/ ve sinyra/normalize/dedup.py.

Kapsam:
- SQLite, dosya: data/sinyra.db
- Tek tablo (şimdilik): seen_items (hash TEXT PK, title, link, first_seen_at, last_seen_at)
- TTL: 14 gün (mevcut davranışla aynı)
- Alembic migration ile (F3 hazırlığı)
- API: SeenStore.is_seen(hash) -> bool, SeenStore.remember(items) -> int

dedup.py:
- input: List[RawItem]
- hash: md5(title + "|" + link)
- recency filter: HOURS_LOOKBACK config'ten (default 72)
- output: (kept_items, stats_dict)

Test: tests/unit/test_dedup.py — 3 case: seen, fresh, too_old.

KURAL: Tüm zaman damgaları UTC, naive datetime YOK — timezone-aware (datetime.now(UTC)).