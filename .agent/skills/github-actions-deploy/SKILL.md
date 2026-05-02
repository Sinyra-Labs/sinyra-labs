---
name: github-actions-deploy
description: |
  Create or modify GitHub Actions workflows for Sinyra Labs. Handles UTC cron
  conversion, secret validation, dry-run verification, and deployment checklist.
  Use when scheduling jobs, adding new automations, or debugging workflow failures.
---

# GitHub Actions Deploy Skill

## When to use
- User says "deploy", "schedule", "automate this script", "workflow ekle".
- Existing workflow is failing and needs diagnosis.

## Mandatory checks before every workflow
1. **UTC conversion:** If user says "her gün 18:00 TR", convert: `0 15 * * *` (UTC+3 → -3h). Add ±15 min buffer.
2. **Secrets audit:** List all `${{ secrets.X }}` references; verify each exists via GitHub MCP.
3. **Concurrency block:** Long-running jobs MUST have `concurrency:` to prevent double-runs.
4. **Timeout:** Every job MUST have `timeout-minutes` (default 20).
5. **Failure notify:** Every prod cron MUST have `if: failure()` notification step.

## Required secrets (Sinyra production)
- `OPENAI_API_KEY`
- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD`
- `EMAIL_FROM_NAME`
- `EMAIL_TO`
- `SLACK_WEBHOOK` (optional — skip notify step if absent)

## Output
- Diff of `.github/workflows/<name>.yml`
- Checklist: ✅ UTC ✅ secrets ✅ concurrency ✅ timeout ✅ alert
- Manual test command: `gh workflow run <name>.yml --field dry_run=true`
