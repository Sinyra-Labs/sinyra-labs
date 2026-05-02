"""Feature classifier: is this a real product/feature launch?"""

import json
from pathlib import Path

from openai.types.chat import ChatCompletionMessageParam

from sinyra import config
from sinyra.intelligence import openai_client
from sinyra.normalize.schema import ClassificationResult, ClassifiedFeature, RawItem

_PROMPTS_DIR = Path(__file__).parent / "prompts"


def _load_prompt(version: str) -> str:
    return (_PROMPTS_DIR / f"classify.{version}.md").read_text(encoding="utf-8")


def classify(item: RawItem) -> ClassifiedFeature:
    version = config.CLASSIFY_PROMPT_VERSION
    system_prompt = _load_prompt(version)
    user_message = json.dumps(
        {"title": item.title, "summary": item.summary or ""},
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
    result = ClassificationResult.model_validate(raw_json)
    return ClassifiedFeature(
        raw=item,
        is_feature=result.is_feature,
        feature_type=result.feature_type,
        confidence=result.confidence,
        prompt_version=version,
    )
