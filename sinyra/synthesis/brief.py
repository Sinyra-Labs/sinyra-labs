"""Daily executive brief generator."""

from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

import structlog
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel

from sinyra import config
from sinyra.intelligence import openai_client
from sinyra.normalize.schema import ImpactResult

log = structlog.get_logger()

_PROMPTS_DIR = Path(__file__).parent.parent / "intelligence" / "prompts"


class DailyBrief(BaseModel):
    date_tr: str
    day_name: str
    time_str: str
    summary_tr: str
    trends: list[str]
    insight: str
    top_features: list[ImpactResult]
    by_company: dict[str, list[ImpactResult]]
    stats: dict[str, int]


class _BriefLLMOutput(BaseModel):
    summary: str = ""
    trends: list[str] = []
    insight: str = ""


def _group_by_company(features: list[ImpactResult]) -> dict[str, list[ImpactResult]]:
    groups: dict[str, list[ImpactResult]] = defaultdict(list)
    for f in features:
        company = f.feature.raw.hint_company or "Diğer"
        groups[company].append(f)
    return dict(
        sorted(groups.items(), key=lambda kv: max(x.impact_score for x in kv[1]), reverse=True)
    )


def _call_llm(features: list[ImpactResult]) -> _BriefLLMOutput:
    system_prompt = "\n".join(
        [
            "Sen kıdemli bir AI/teknoloji sektörü analistisin ve günlük yönetici brifingi yazıyorsun.",
            "Girdi: filtrelenmiş ve skorlanmış gerçek AI ürün lansmanları listesi.",
            "",
            "SADECE şu JSON'u döndür:",
            '{"summary": "2-3 cümle yönetici özeti Türkçe",',
            ' "trends": ["trend cümlesi 1", "trend cümlesi 2", "trend cümlesi 3"],',
            ' "insight": "1 cümle stratejik içgörü Türkçe"}',
            "",
            "Stil: kısa, net, abartısız, profesyonel Türkçe. Klişe kaçın.",
            "",
            "DİL KURALLARI:",
            "- Teknik kısaltmaları ÇEVIRME: AI, API, LLM, SDK, GPU, ML → olduğu gibi yaz.",
            "- Ürün/marka adlarını çevirme: ChatGPT, Gemini, Claude, Copilot, Grok → olduğu gibi.",
            "- 'YZ', 'MÖ' gibi Türkçe karşılıklar YASAK.",
        ]
    )
    bullets = "\n".join(
        f"{i + 1}) [{f.feature.raw.hint_company or '?'}] {f.feature.raw.title}"
        f" | etki={int(f.impact_score)} | tip={f.feature.feature_type}"
        f" | neden={f.rationale}"
        for i, f in enumerate(features)
    )
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": bullets},
    ]
    raw = openai_client.chat_json(
        messages=messages,
        model=config.OPENAI_MODEL,
        temperature=0.3,
        prompt_version="synthesis-v1",
    )
    return _BriefLLMOutput.model_validate(raw)


def generate_daily_brief(features: list[ImpactResult]) -> DailyBrief:
    from sinyra.delivery.email.helpers import get_day_name_tr

    features_sorted = sorted(features, key=lambda f: f.impact_score, reverse=True)
    by_company = _group_by_company(features_sorted)

    now = datetime.now(tz=UTC)
    date_tr = now.strftime("%-d %B %Y") if hasattr(now, "strftime") else now.strftime("%d %B %Y")
    # strftime %-d is Linux only; use lstrip on Windows
    date_tr = str(now.day) + now.strftime(" %B %Y")
    day_name = get_day_name_tr(now.weekday())
    time_str = now.strftime("%H:%M")

    unique_companies = len(by_company)
    avg_impact = (
        int(sum(f.impact_score for f in features_sorted) / len(features_sorted))
        if features_sorted
        else 0
    )

    if not features_sorted:
        log.info("synthesis.brief.empty")
        return DailyBrief(
            date_tr=date_tr,
            day_name=day_name,
            time_str=time_str,
            summary_tr="Son 72 saatte kayda değer bir AI ürün/özellik lansmanı tespit edilmedi.",
            trends=[],
            insight="Sakin bir gün. Kendi roadmap'inize odaklanmak için iyi bir fırsat.",
            top_features=[],
            by_company={},
            stats={"total_features": 0, "unique_companies": 0, "avg_impact": 0},
        )

    llm_out = _call_llm(features_sorted)
    log.info("synthesis.brief.generated", feature_count=len(features_sorted))

    return DailyBrief(
        date_tr=date_tr,
        day_name=day_name,
        time_str=time_str,
        summary_tr=llm_out.summary or "Günün AI ürün radarı.",
        trends=llm_out.trends,
        insight=llm_out.insight,
        top_features=features_sorted,
        by_company=by_company,
        stats={
            "total_features": len(features_sorted),
            "unique_companies": unique_companies,
            "avg_impact": avg_impact,
        },
    )
