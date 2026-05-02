# Sinyra Labs — Agent Rules

## Stack
- Python 3.12, type-hinted (mypy strict)
- pydantic v2 at every data boundary
- httpx, feedparser, openai, jinja2, sqlalchemy, alembic
- Mail: smtplib + Gmail SMTP (NOT Resend — that's F3+)
- Test: pytest + VCR.py
- Lint/format: ruff (line-length 100)
- Package manager: uv

## Behavior Rules
- DO NOT run tests automatically. Show command, let user run.
- DO NOT add new dependencies without asking first.
- LLM calls MUST pass `model` and `temperature` as parameters.
- All prompts in `sinyra/intelligence/prompts/*.md`, versioned (v1, v2, ...).
- All timestamps UTC. Convert to TR only at presentation layer.
- Secrets only via `os.environ`. Keep `.env.example` updated.
- Update CHANGELOG.md on every meaningful change.

## Email Provider Rule
- Abstract `EmailProvider` Protocol in sinyra/delivery/email/provider.py
- Default impl: GmailSmtpProvider (port 465, SSL, App Password auth)
- DO NOT integrate Resend/SendGrid in F2. Interface allows F3 swap via one config value.

## Code Style
- Functions short, single-purpose. > 50 lines → refactor.
- Error messages in Turkish, log messages in English.
- HTML/email render via Jinja2; string concat FORBIDDEN.

## Output Format
- 3-line plan first, then code, then "why this choice".
- If ambiguous, ASK — do not guess.
- Speak Turkish to user, code/comments/logs/commits in English.
