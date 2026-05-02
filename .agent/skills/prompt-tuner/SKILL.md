---
name: prompt-tuner
description: |
  Evaluate and iterate on intelligence-layer prompts (classifier, impact scorer)
  against the golden test set in tests/eval/golden_set.jsonl. Use when modifying
  any file under sinyra/intelligence/prompts/ or when classification quality needs review.
---

# Prompt Tuner

## When to use
- User edits a prompt under `sinyra/intelligence/prompts/`.
- User asks "classifier'ı iyileştir", "false positive yüksek", "yeni prompt versiyonu".
- Classification quality metrics are declining.

## How to run
1. Read current prompt: `sinyra/intelligence/prompts/<name>.<version>.md`
2. Run: `pytest tests/eval/test_classifier.py -k <prompt_name> -v`
3. Inspect precision/recall/confusion matrix output
4. If precision < 85% or recall < 80%, propose 2-3 targeted prompt deltas

## Iteration protocol
- Make ONE change at a time
- Bump version (v1 → v2), do NOT delete old version
- Save eval report to `docs/prompt-evals/<name>-v<n>.md`
- Update `CLASSIFY_PROMPT_VERSION` env / config when promoting

## Output contract
- Precision, recall, F1 against golden_set.jsonl
- Confusion matrix (TP, FP, TN, FN)
- List of misclassified examples
