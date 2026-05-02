"""Seen-items store for deduplication (SQLite in F2, Postgres-ready for F3)."""

import hashlib
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast

import structlog
from sqlalchemy import CursorResult, create_engine, delete
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from sinyra import config
from sinyra.normalize.schema import RawItem
from sinyra.storage.models import Base, SeenItem

log = structlog.get_logger()

TTL_DAYS = 14


def _hash_item(item: RawItem) -> str:
    return hashlib.md5(f"{item.title}|{item.link}".encode()).hexdigest()


class SeenStore:
    def __init__(self, db_path: str | None = None) -> None:
        path = db_path or config.DB_PATH
        if path == ":memory:":
            self._engine = create_engine(
                "sqlite:///:memory:",
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
            Base.metadata.create_all(self._engine)
        else:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            self._engine = create_engine(f"sqlite:///{path}")
            self._run_migrations()
        self._prune()

    def _run_migrations(self) -> None:
        from alembic import command
        from alembic.config import Config as AlembicConfig

        cfg = AlembicConfig()
        cfg.set_main_option(
            "script_location",
            str(Path(__file__).parent / "migrations"),
        )
        cfg.set_main_option("sqlalchemy.url", str(self._engine.url))
        command.upgrade(cfg, "head")

    def _prune(self) -> None:
        cutoff = datetime.now(UTC) - timedelta(days=TTL_DAYS)
        with Session(self._engine) as session:
            result = session.execute(
                delete(SeenItem).where(SeenItem.last_seen_at < cutoff)
            )
            deleted = cast(CursorResult[Any], result).rowcount or 0
            session.commit()
        if deleted:
            log.info("seen_store.pruned", count=deleted, ttl_days=TTL_DAYS)

    def is_seen(self, hash_: str) -> bool:
        with Session(self._engine) as session:
            return session.get(SeenItem, hash_) is not None

    def remember(self, items: list[RawItem]) -> int:
        now = datetime.now(UTC)
        inserted = 0
        with Session(self._engine) as session:
            for item in items:
                h = _hash_item(item)
                existing = session.get(SeenItem, h)
                if existing:
                    existing.last_seen_at = now
                else:
                    session.add(
                        SeenItem(
                            hash=h,
                            title=item.title,
                            link=item.link,
                            first_seen_at=now,
                            last_seen_at=now,
                        )
                    )
                    inserted += 1
            session.commit()
        log.info("seen_store.remembered", inserted=inserted, total=len(items))
        return inserted
