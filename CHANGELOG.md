# Changelog

All notable changes to Sinyra Labs will be documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- P5 Synthesis + Email Delivery layer fully implemented:
  - `sinyra/synthesis/brief.py`: `generate_daily_brief()` — OpenAI call for TR summary/trends/insight, sorts by impact, groups by company
  - `sinyra/delivery/email/helpers.py`: `escape`, `impact_color`, `impact_bg`, `impact_label`, `translate_type`, `get_day_name_tr`, `company_emoji` ported from Apps Script
  - `sinyra/delivery/email/templates/brief.html`: full table-based layout (hero, stats strip, spotlight, company sections, trends, insight, share card, contact card) — Apps Script birebir port
  - `sinyra/delivery/email/templates/brief.txt`: plain-text fallback
  - `sinyra/delivery/email/render.py`: Jinja2 render with custom filters; `render_preview()` with fake data
  - `sinyra/delivery/email/gmail_smtp.py`: `GmailSmtpProvider` — SMTP_SSL port 465, App Password auth, per-recipient error isolation
  - `sinyra/delivery/email/send.py`: `send_brief()` factory dispatcher, `SendStats` model
  - `sinyra/run.py`: full pipeline wired — fetch → dedup → classify → filter → score → synthesize → deliver
  - `tests/__snapshots__/brief_sample.html`: HTML snapshot
  - `tests/unit/test_render.py`: render + snapshot + helpers tests (4 tests)
  - `.env.example`: `EMAIL_PROVIDER` variable added

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
