# Changelog

All notable changes to Sinyra Labs will be documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- Initial Python repo scaffold (P1)
- pyproject.toml with uv, ruff, mypy, pytest
- Directory structure: sinyra/, tests/, .github/workflows/, .agent/
- .env.example with Gmail SMTP variables
- CLAUDE.md project rules
- L1 Ingestion layer (P2): rss.py, google_news.py, feeds.yaml (12 sources)
- structlog JSON logging, PyYAML dependency
- RawItem pydantic schema with pub_date (UTC-aware)
- HTTP retry: exponential backoff (3 attempts, timeout=15s)
- HTML stripping: tags removed, entities unescaped, whitespace collapsed, max 600 chars
- Unit tests: 7 tests across happy-path, error handling, HTML stripping
- VCR cassette fixture for fetch_feed
