---
name: impact-evaluator
description: |
  Run impact scoring on a sample feature list and report score distribution,
  outliers, and calibration issues. Use when impact scores seem off or when
  tuning the impact.v*.md prompt.
---

# Impact Evaluator

## When to use
- User says "skor çok düşük/yüksek geliyor", "impact scorer'ı kontrol et".
- After modifying `sinyra/intelligence/prompts/impact.*.md`.

## How to run
```bash
pytest tests/eval/test_impact_scorer.py -v
```

## Output contract
- Score distribution histogram (bins: 0-20, 20-40, 40-60, 60-80, 80-100)
- Items with score=0 or score=100 flagged as potential outliers
- Average score vs. expected range (40-80 for typical day)

## Failure modes
- All scores clustering near 0 → prompt is too strict; relax negative rules
- All scores > 80 → prompt is too permissive; add calibration examples
