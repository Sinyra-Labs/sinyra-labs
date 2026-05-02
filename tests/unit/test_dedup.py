"""Unit tests for normalize.dedup: seen, fresh, too_old cases."""

from datetime import UTC, datetime, timedelta

import pytest

from sinyra.normalize.dedup import dedup
from sinyra.normalize.schema import RawItem
from sinyra.storage.memory import SeenStore


@pytest.fixture
def store() -> SeenStore:
    return SeenStore(db_path=":memory:")


def _item(
    title: str = "Test item",
    link: str = "https://example.com",
    pub_date: datetime | None = None,
) -> RawItem:
    return RawItem(title=title, link=link, pub_date=pub_date or datetime.now(UTC))


def test_seen_item_filtered(store: SeenStore) -> None:
    item = _item()
    store.remember([item])
    kept, stats = dedup([item], store)
    assert kept == []
    assert stats["seen"] == 1
    assert stats["kept"] == 0


def test_fresh_item_kept(store: SeenStore) -> None:
    item = _item(pub_date=datetime.now(UTC) - timedelta(hours=1))
    kept, stats = dedup([item], store, hours_lookback=72)
    assert len(kept) == 1
    assert stats["kept"] == 1
    assert stats["seen"] == 0
    assert stats["too_old"] == 0


def test_too_old_item_filtered(store: SeenStore) -> None:
    item = _item(pub_date=datetime.now(UTC) - timedelta(hours=100))
    kept, stats = dedup([item], store, hours_lookback=72)
    assert kept == []
    assert stats["too_old"] == 1
    assert stats["kept"] == 0
