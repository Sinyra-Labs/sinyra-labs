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
- Storage layer (P3): SQLAlchemy SeenItem model, SeenStore (is_seen/remember/TTL prune)
- Alembic migration setup with initial seen_items table (F3 Postgres-ready)
- normalize/dedup.py: compute_hash (md5), dedup() with recency + seen filtering
- Unit tests for dedup: seen, fresh, too_old cases (tests/unit/test_dedup.py)
- alembic.ini at repo root for CLI migrations
- DB_PATH added to .env.example
- Intelligence layer (P4): openai_client.py (singleton, retry, token tracking, structlog)
- classifier.py: classify(RawItem) -> ClassifiedFeature using classify.v1.md prompt
- impact_scorer.py: score(ClassifiedFeature) -> ImpactResult using impact.v1.md prompt
- classify.v1.md + impact.v1.md: full prompt content with positive/negative rules
- ClassificationResult pydantic model added to schema.py (LLM JSON parse target)
- golden_set.jsonl extended to 30 items (15 positive / 15 negative, balanced)
- tests/eval/test_classifier.py: precision/recall report (skips without OPENAI_API_KEY)
