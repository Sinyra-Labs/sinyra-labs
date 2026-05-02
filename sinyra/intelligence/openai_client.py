"""Shared OpenAI client with retry, token tracking, and structured logging."""

import json
import time
from typing import Any

import structlog
from openai import OpenAI, RateLimitError
from openai.types.chat import ChatCompletionMessageParam

from sinyra import config

log = structlog.get_logger()

_client: OpenAI | None = None
_total_prompt_tokens: int = 0
_total_completion_tokens: int = 0


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=config.OPENAI_API_KEY)
    return _client


def get_token_usage() -> dict[str, int]:
    return {
        "prompt_tokens": _total_prompt_tokens,
        "completion_tokens": _total_completion_tokens,
        "total_tokens": _total_prompt_tokens + _total_completion_tokens,
    }


def chat_json(
    messages: list[ChatCompletionMessageParam],
    model: str,
    temperature: float,
    prompt_version: str,
    max_retries: int = 3,
) -> dict[str, Any]:
    global _total_prompt_tokens, _total_completion_tokens

    client = get_client()
    delay = 1.0
    last_error: Exception | None = None

    for attempt in range(1, max_retries + 1):
        start = time.monotonic()
        try:
            resp = client.chat.completions.create(
                model=model,
                temperature=temperature,
                response_format={"type": "json_object"},
                messages=messages,
            )
            latency_ms = int((time.monotonic() - start) * 1000)
            usage = resp.usage
            if usage:
                _total_prompt_tokens += usage.prompt_tokens
                _total_completion_tokens += usage.completion_tokens
            log.info(
                "openai.chat_json",
                model=model,
                temperature=temperature,
                prompt_version=prompt_version,
                latency_ms=latency_ms,
                prompt_tokens=usage.prompt_tokens if usage else None,
                completion_tokens=usage.completion_tokens if usage else None,
            )
            content = resp.choices[0].message.content or "{}"
            result: dict[str, Any] = json.loads(content)
            return result
        except RateLimitError as e:
            last_error = e
            log.warning("openai.rate_limit", attempt=attempt, retry_in=delay)
            if attempt < max_retries:
                time.sleep(delay)
                delay *= 2
        except Exception:
            raise

    raise RuntimeError(f"OpenAI call failed after {max_retries} retries") from last_error
