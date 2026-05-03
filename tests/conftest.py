"""Shared pytest fixtures and configuration."""

import os
from pathlib import Path

import pytest


# Load .env from repo root if it exists — mevcut env değerlerini ezmez.
def _load_dotenv() -> None:
    env_file = Path(__file__).parent.parent / ".env"
    if not env_file.exists():
        return
    for raw in env_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


@pytest.fixture(scope="module")
def vcr_config() -> dict[str, object]:
    """vcrpy / pytest-recording global config: match only on method+uri, no real network."""
    return {
        "record_mode": "none",
        "match_on": ["method", "uri"],
    }
