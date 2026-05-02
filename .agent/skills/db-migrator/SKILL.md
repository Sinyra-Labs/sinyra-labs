---
name: db-migrator
description: |
  Generate and apply Alembic database migrations for Sinyra Labs. Smoke-tests
  migrations on SQLite (F2) and optionally Postgres (F3+). Use when adding new
  tables, columns, or indexes to the storage layer.
---

# DB Migrator

## When to use
- User says "yeni tablo ekle", "migration oluştur", "schema değişikliği".
- After modifying `sinyra/storage/models.py`.

## How to run
```bash
# Generate migration
alembic revision --autogenerate -m "describe_change"

# Apply to local SQLite
alembic upgrade head

# Smoke-test
python -c "from sinyra.storage.memory import SeenStore; s = SeenStore(); print('DB OK')"
```

## Safety rules
- NEVER run `alembic downgrade` in production without explicit user confirmation.
- Always review auto-generated migration file before applying.
- Test on SQLite first; only apply to Postgres (F3) after local validation.

## Output contract
- Generated migration file path
- Summary of schema changes (tables added/modified/dropped)
- Smoke-test pass/fail result
