"""Classifier eval: precision/recall report against golden_set.jsonl.

Run with:
    pytest tests/eval/test_classifier.py -v -s

Requires OPENAI_API_KEY environment variable. Skipped in CI without it.
"""

import json
import os
from pathlib import Path

import pytest

from sinyra.intelligence.classifier import classify
from sinyra.normalize.schema import RawItem

pytestmark = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY required for eval tests",
)

GOLDEN = Path(__file__).parent / "golden_set.jsonl"


def _load_golden() -> list[dict[str, object]]:
    return [json.loads(line) for line in GOLDEN.read_text().splitlines() if line.strip()]


def test_classifier_precision_recall() -> None:
    golden = _load_golden()

    tp = fp = fn = tn = 0
    misses: list[str] = []

    for i, entry in enumerate(golden):
        item = RawItem(
            title=str(entry["title"]),
            link=f"https://example.com/item-{i}",
        )
        result = classify(item)
        expected = bool(entry["is_feature"])

        if result.is_feature and expected:
            tp += 1
        elif result.is_feature and not expected:
            fp += 1
            misses.append(f"FP: {entry['title']}")
        elif not result.is_feature and expected:
            fn += 1
            misses.append(f"FN: {entry['title']}")
        else:
            tn += 1

    total = len(golden)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    accuracy = (tp + tn) / total if total > 0 else 0.0

    print(f"\n{'=' * 40}")
    print("Classifier Eval Report")
    print(f"{'=' * 40}")
    print(f"Total:     {total:>4}  (TP={tp} TN={tn} FP={fp} FN={fn})")
    print(f"Precision: {precision:>7.2%}")
    print(f"Recall:    {recall:>7.2%}")
    print(f"F1:        {f1:>7.2%}")
    print(f"Accuracy:  {accuracy:>7.2%}")
    if misses:
        print("\nMisclassified:")
        for m in misses:
            print(f"  {m}")

    assert precision >= 0.80, f"Precision {precision:.2%} below 80% threshold"
    assert recall >= 0.75, f"Recall {recall:.2%} below 75% threshold"
