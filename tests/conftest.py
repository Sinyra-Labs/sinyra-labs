"""Shared pytest fixtures and configuration."""

import pytest


@pytest.fixture(scope="module")
def vcr_config() -> dict[str, object]:
    """vcrpy / pytest-recording global config: match only on method+uri, no real network."""
    return {
        "record_mode": "none",
        "match_on": ["method", "uri"],
    }
