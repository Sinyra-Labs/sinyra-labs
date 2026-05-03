"""Pipeline entrypoint: fetch → dedup → classify → score → synthesize → deliver."""

import logging
import time
from datetime import UTC, datetime, timedelta

import structlog

from sinyra import config
from sinyra.delivery.email.send import send_brief
from sinyra.ingest.google_news import fetch_gnews
from sinyra.ingest.rss import fetch_all as fetch_rss
from sinyra.intelligence.classifier import classify
from sinyra.intelligence.impact_scorer import score
from sinyra.normalize.schema import ClassifiedFeature, ImpactResult, RawItem
from sinyra.storage.memory import SeenStore
from sinyra.synthesis.brief import generate_daily_brief

log = structlog.get_logger()

_GNEWS_QUERIES = [
    ("Meta AI release OR Llama", "Meta"),
    ("xAI Grok update", "xAI"),
    ("Mistral AI release", "Mistral"),
    ("Anthropic Claude update", "Anthropic"),
    ("OpenAI GPT release", "OpenAI"),
    ("Google Gemini feature", "Google"),
    ("Microsoft Copilot update", "Microsoft"),
]


def _fetch_all_raw() -> list[RawItem]:
    items: list[RawItem] = fetch_rss()
    for query, company in _GNEWS_QUERIES:
        gn_items = fetch_gnews(query, source_name=f"Google News: {query}")
        for item in gn_items:
            item.hint_company = item.hint_company or company
        items.extend(gn_items)
    log.info("pipeline.fetch_done", total=len(items))
    return items


def _dedup(items: list[RawItem], store: SeenStore) -> list[RawItem]:
    import hashlib

    cutoff = datetime.now(UTC) - timedelta(hours=config.LOOKBACK_HOURS)
    kept: list[RawItem] = []
    rejected_old = rejected_seen = rejected_no_title = 0

    for item in items:
        if not item.title:
            rejected_no_title += 1
            continue
        if item.pub_date and item.pub_date < cutoff:
            rejected_old += 1
            continue
        h = hashlib.md5(f"{item.title}|{item.link}".encode()).hexdigest()
        if store.is_seen(h):
            rejected_seen += 1
            continue
        kept.append(item)

    log.info(
        "pipeline.dedup",
        kept=len(kept),
        rejected_old=rejected_old,
        rejected_seen=rejected_seen,
        rejected_no_title=rejected_no_title,
    )
    return kept


def _classify_all(items: list[RawItem]) -> list[ClassifiedFeature]:
    results: list[ClassifiedFeature] = []
    for idx, item in enumerate(items[: config.MAX_CLASSIFY if hasattr(config, "MAX_CLASSIFY") else 100]):
        try:
            cf = classify(item)
            results.append(cf)
        except Exception as exc:
            log.warning("pipeline.classify_error", title=item.title[:80], error=str(exc))
        if idx % 10 == 9:
            time.sleep(0.3)
    log.info("pipeline.classify_done", classified=len(results))
    return results


def _filter_features(classified: list[ClassifiedFeature]) -> list[ClassifiedFeature]:
    seen_key: set[str] = set()
    kept: list[ClassifiedFeature] = []
    for cf in classified:
        if not cf.is_feature:
            continue
        if cf.confidence < config.CONFIDENCE_MIN:
            continue
        key = f"{cf.raw.hint_company or ''}|{cf.raw.title}".lower()
        if key in seen_key:
            continue
        seen_key.add(key)
        kept.append(cf)
    log.info("pipeline.filter_done", kept=len(kept))
    return kept


def _score_all(features: list[ClassifiedFeature]) -> list[ImpactResult]:
    results: list[ImpactResult] = []
    for idx, cf in enumerate(features):
        try:
            results.append(score(cf))
        except Exception as exc:
            log.warning("pipeline.score_error", title=cf.raw.title[:80], error=str(exc))
        if idx % 10 == 9:
            time.sleep(0.3)

    above_min = [r for r in results if r.impact_score >= config.IMPACT_MIN]
    above_min.sort(key=lambda r: r.impact_score, reverse=True)
    log.info("pipeline.score_done", scored=len(results), above_min=len(above_min))
    return above_min


def main() -> None:
    log.info("pipeline.start")
    store = SeenStore()

    raw = _fetch_all_raw()
    deduped = _dedup(raw, store)
    classified = _classify_all(deduped)
    features = _filter_features(classified)
    scored = _score_all(features)

    brief = generate_daily_brief(scored)

    if config.DRY_RUN:
        log.info("pipeline.dry_run", recipients=config.EMAIL_TO)
    else:
        stats = send_brief(brief, config.EMAIL_TO)
        log.info(
            "pipeline.email_done",
            attempted=stats.attempted,
            succeeded=stats.succeeded,
            failed=stats.failed,
        )

    store.remember(deduped)
    log.info("pipeline.done")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
