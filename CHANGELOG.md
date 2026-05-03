# Changelog

All notable changes to Sinyra Labs will be documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added
- `classify.v2.md`: new classifier prompt with negative-first evaluation order
  - Expanded investment keywords: "invests", "investment", "Series A-F", "seed round", "backed by"
  - Explicit clarification: "research investment ≠ research release"
  - Hybrid article rule: funding headline + product mention → FALSE
  - Tier list title signals: "The N most...", "every developer should"
  - Availability language required for TRUE: "launches", "releases", "now available"
  - Expected to eliminate ~12% FP rate on investment/funding/valuation items
- `docs/prompt-evals/classify-v2.md`: v1 vs v2 eval comparison (golden set analysis)
- `CLASSIFY_PROMPT_VERSION` default changed to `v2` in config; v1 retained for rollback

### Fixed
- `feeds.yaml`: 5 broken feed URLs corrected
  - OpenAI: `/blog/rss/` (403) → `/news/rss.xml` (site yeniden tasarım sonrası taşındı)
  - Anthropic: native RSS yok → `Olshansk/rss-feeds` proxy: `feed_anthropic_news.xml` + `feed_anthropic_engineering.xml` eklendi
  - DeepMind: `/blog/rss/` (404) → `/blog/rss.xml`
  - Meta AI: native RSS yok → `Olshansk/rss-feeds` proxy: `feed_meta_ai.xml`
  - Mistral: native RSS yok, RSS entry kaldırıldı → `GNews · Mistral AI` sorgusuyla değiştirildi

### Added
- P6 GitHub Actions workflows corrected and completed:
  - `daily-pipeline.yml`: cron fixed to `0 15 * * *` (TR 18:00 = UTC 15:00), `contents: write` removed, `EMAIL_PROVIDER`/`DB_PATH` env vars added, failure notification URL enriched
  - `test.yml`: concurrency group added, install fixed (`-e .` + full dev deps incl. `types-*`), failure notification + artifact upload added
  - `manual-backfill.yml`: failure notification step added, `EMAIL_PROVIDER`/`DB_PATH` env vars added
  - `SECRETS_REQUIRED.md`: new — secret matrix per workflow, Gmail App Password setup guide, Slack webhook guide, `gh workflow run` test commands

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
