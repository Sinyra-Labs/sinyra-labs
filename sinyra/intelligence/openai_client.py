"""Shared OpenAI client with retry, token tracking, and structured logging."""

# TODO(P4): implement get_client() -> openai.OpenAI  (singleton)
# TODO(P4): implement chat_json(messages, model, temperature, prompt_version) -> dict[str, Any]
#   - logs: model, temperature, prompt_version, latency_ms, tokens_used
#   - retries on RateLimitError (exponential backoff, max 3)
#   - raises on persistent failure
