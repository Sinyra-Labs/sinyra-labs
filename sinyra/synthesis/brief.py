"""Daily executive brief generator."""

from pydantic import BaseModel

from sinyra.normalize.schema import ImpactResult


class DailyBrief(BaseModel):
    date_tr: str  # presentation date, TR locale
    summary_tr: str
    trends: list[str]
    insight: str
    top_features: list[ImpactResult]
    stats: dict[str, int]  # e.g. {"fetched": 120, "filtered": 8, "avg_score": 72}


def generate_daily_brief(features: list[ImpactResult]) -> DailyBrief:
    # TODO(P5): call openai for summary_tr, trends, insight
    # TODO(P5): sort features by impact_score desc
    raise NotImplementedError
