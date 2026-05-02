"""Impact scorer: 0-100 market impact score for classified features."""

import json
from pathlib import Path

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel, Field

from sinyra import config
from sinyra.intelligence import openai_client
from sinyra.normalize.schema import ClassifiedFeature, ImpactResult

_PROMPTS_DIR = Path(__file__).parent / "prompts"


class _ImpactLLMOutput(BaseModel):
    """Direct LLM output from the impact scorer (parsed via model_validate_json)."""

    impact_score: float = Field(ge=0, le=100)
    impact_label: str = ""
    rationale: str = ""


def _load_prompt(version: str) -> str:
    return (_PROMPTS_DIR / f"impact.{version}.md").read_text(encoding="utf-8")


def score(feature: ClassifiedFeature) -> ImpactResult:
    version = config.IMPACT_PROMPT_VERSION
    system_prompt = _load_prompt(version)
    user_message = json.dumps(
        {
            "title": feature.raw.title,
            "summary": feature.raw.summary or "",
            "feature_type": feature.feature_type,
            "company_hint": feature.raw.hint_company or "",
        },
        ensure_ascii=False,
    )
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    raw_json = openai_client.chat_json(
        messages=messages,
        model=config.OPENAI_MODEL,
        temperature=config.OPENAI_TEMPERATURE,
        prompt_version=version,
    )
    output = _ImpactLLMOutput.model_validate(raw_json)
    return ImpactResult(
        feature=feature,
        impact_score=output.impact_score,
        impact_label=output.impact_label,
        rationale=output.rationale,
        prompt_version=version,
    )
