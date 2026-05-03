"""Render DailyBrief to HTML and plain-text via Jinja2."""

from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from sinyra.delivery.email.helpers import (
    clean_source,
    company_emoji,
    impact_bg,
    impact_color,
    impact_label,
    translate_type,
)
from sinyra.normalize.schema import ImpactResult
from sinyra.synthesis.brief import DailyBrief

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=False,  # we escape manually via helpers in HTML; plain-text needs no escaping
    trim_blocks=True,
    lstrip_blocks=True,
)
_env.filters["impact_color"] = impact_color
_env.filters["impact_bg"] = impact_bg
_env.filters["impact_label"] = impact_label
_env.filters["translate_type"] = translate_type
_env.filters["company_emoji"] = company_emoji
_env.filters["clean_source"] = clean_source


def _group_by_company(features: list[ImpactResult]) -> dict[str, list[ImpactResult]]:
    groups: dict[str, list[ImpactResult]] = defaultdict(list)
    for f in features:
        company = f.feature.raw.hint_company or "Diğer"
        groups[company].append(f)
    # order companies by their highest impact score descending
    return dict(
        sorted(groups.items(), key=lambda kv: max(x.impact_score for x in kv[1]), reverse=True)
    )


def _build_context(brief: DailyBrief) -> dict[str, object]:
    return {
        "brief": brief,
    }


def render_html(brief: DailyBrief) -> str:
    ctx = _build_context(brief)
    return _env.get_template("brief.html").render(**ctx)


def render_text(brief: DailyBrief) -> str:
    ctx = _build_context(brief)
    return _env.get_template("brief.txt").render(**ctx)


def render_preview(output_path: str) -> None:
    """Render with sample data and write to output_path for browser preview."""
    from sinyra.normalize.schema import ClassifiedFeature, RawItem

    sample_features: list[ImpactResult] = [
        ImpactResult(
            feature=ClassifiedFeature(
                raw=RawItem(
                    title="Google launches Gemini 3.1 Flash-Lite",
                    link="https://blog.google/technology/ai/gemini-3-1",
                    summary="",
                    source_name="Google AI Blog",
                    hint_company="Google",
                ),
                is_feature=True,
                feature_type="new_feature",
                confidence=92,
            ),
            impact_score=82,
            impact_label="Yüksek",
            rationale="Düşük maliyetli hızlı modeller pazarında doğrudan rekabet.",
        ),
        ImpactResult(
            feature=ClassifiedFeature(
                raw=RawItem(
                    title="OpenAI introduces GPT-Rosalind",
                    link="https://openai.com/index/gpt-rosalind",
                    summary="",
                    source_name="OpenAI News",
                    hint_company="OpenAI",
                ),
                is_feature=True,
                feature_type="new_feature",
                confidence=95,
            ),
            impact_score=91,
            impact_label="Kritik",
            rationale="Alan-spesifik frontier modelinin yeni bir sektörü hedeflemesi paradigmatik.",
        ),
        ImpactResult(
            feature=ClassifiedFeature(
                raw=RawItem(
                    title="Anthropic launches Claude Design",
                    link="https://www.anthropic.com/news/claude-design",
                    summary="",
                    source_name="Anthropic News",
                    hint_company="Anthropic",
                ),
                is_feature=True,
                feature_type="new_feature",
                confidence=88,
            ),
            impact_score=74,
            impact_label="Yüksek",
            rationale="Canva/Figma tarafına AI ajanı olarak doğrudan rekabet.",
        ),
    ]

    now = datetime.now(tz=UTC)
    from sinyra.delivery.email.helpers import get_day_name_tr

    by_company = _group_by_company(sample_features)

    brief = DailyBrief(
        date_tr=now.strftime("%-d %B %Y"),
        day_name=get_day_name_tr(now.weekday()),
        time_str=now.strftime("%H:%M"),
        summary_tr=(
            "Bugün öne çıkan üç büyük hamle: OpenAI yaşam bilimleri modelini,"
            " Google maliyet-verimli Gemini 3.1'i, Anthropic tasarım ajanı Claude Design'ı tanıttı."
        ),
        trends=[
            "Alan-spesifik (biyoloji, tasarım) frontier modeller yaygınlaşıyor.",
            "Model pazarında 'hızlı + ucuz' segment rekabeti sertleşiyor.",
            "Hyperscaler platformlar çoklu-model stratejisini derinleştiriyor.",
        ],
        insight="Önümüzdeki çeyrekte kazananlar, belirli iş yüklerine özel modeller sunan sağlayıcılar olacak.",
        top_features=sample_features,
        by_company=by_company,
        stats={
            "total_features": len(sample_features),
            "unique_companies": len(by_company),
            "avg_impact": int(sum(f.impact_score for f in sample_features) / len(sample_features)),
        },
    )

    html = render_html(brief)
    Path(output_path).write_text(html, encoding="utf-8")
