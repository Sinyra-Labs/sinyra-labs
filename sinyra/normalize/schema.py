"""Pydantic models for raw and classified items."""

from datetime import datetime

from pydantic import BaseModel, Field


class RawItem(BaseModel):
    """Single news item as fetched from a feed."""

    title: str
    link: str
    summary: str = ""
    pub_date: datetime | None = None
    source_name: str = ""
    hint_company: str | None = None  # optional company hint from feeds.yaml


class ClassifiedFeature(BaseModel):
    """RawItem enriched with classifier output."""

    raw: RawItem
    is_feature: bool
    feature_type: str = ""  # e.g. "new_model", "new_product", "research"
    confidence: float = Field(ge=0, le=100)
    prompt_version: str = "v1"


class ImpactResult(BaseModel):
    """Impact scoring output."""

    feature: ClassifiedFeature
    impact_score: float = Field(ge=0, le=100)
    impact_label: str = ""  # e.g. "high", "medium", "low"
    rationale: str = ""
    prompt_version: str = "v1"
