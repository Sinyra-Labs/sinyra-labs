"""Central configuration loaded from environment variables."""

import os

# --- LLM ---
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMPERATURE: float = float(os.environ.get("OPENAI_TEMPERATURE", "0.2"))

# --- Pipeline ---
DRY_RUN: bool = os.environ.get("DRY_RUN", "false").lower() == "true"
LOOKBACK_HOURS: int = int(os.environ.get("LOOKBACK_HOURS", "72"))
CONFIDENCE_MIN: float = float(os.environ.get("CONFIDENCE_MIN", "60"))
IMPACT_MIN: float = float(os.environ.get("IMPACT_MIN", "40"))

# --- Storage ---
DB_PATH: str = os.environ.get("DB_PATH", "data/sinyra.db")

# --- Email (Gmail SMTP) ---
GMAIL_ADDRESS: str = os.environ.get("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD: str = os.environ.get("GMAIL_APP_PASSWORD", "")
EMAIL_FROM_NAME: str = os.environ.get("EMAIL_FROM_NAME", "Sinyra Labs")
EMAIL_TO: list[str] = [
    addr.strip() for addr in os.environ.get("EMAIL_TO", "").split(",") if addr.strip()
]
EMAIL_PROVIDER: str = os.environ.get("EMAIL_PROVIDER", "gmail_smtp")

# --- Active prompt versions ---
CLASSIFY_PROMPT_VERSION: str = os.environ.get("CLASSIFY_PROMPT_VERSION", "v2")
IMPACT_PROMPT_VERSION: str = os.environ.get("IMPACT_PROMPT_VERSION", "v2")
