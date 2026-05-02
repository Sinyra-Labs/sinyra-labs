---
name: rss-source-validator
description: |
  Validate RSS/Atom feed URLs. Use when adding a new news source to feeds.yaml,
  diagnosing why a feed returns 0 items, or auditing overall feed health.
---

# RSS Source Validator

## When to use
- User says "yeni feed ekle", "feed test et", "Bu URL RSS mi?"
- A feed in `sinyra/ingest/feeds.yaml` is suspected broken or returning 0 items.

## How to run
```bash
python .agent/skills/rss-source-validator/scripts/validate.py <URL>
```

## Output contract
- HTTP status (200 / 4xx / 5xx)
- Format detected (RSS 2.0 / Atom)
- Item count and latest pubDate
- Encoding warnings
- Suggested YAML entry for `feeds.yaml`

## Failure modes
- HTTP 403 → Add `User-Agent` header, retest
- Returns HTML not XML → not a feed; suggest Firecrawl scrape instead
- pubDate missing on all items → set `KEEP_IF_NO_DATE: true` in config
