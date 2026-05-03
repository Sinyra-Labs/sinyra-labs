"""Snapshot test for HTML/text email rendering."""

from pathlib import Path

import pytest

from sinyra.delivery.email.helpers import get_day_name_tr
from sinyra.delivery.email.render import render_html, render_text
from sinyra.normalize.schema import ClassifiedFeature, ImpactResult, RawItem
from sinyra.synthesis.brief import DailyBrief

_SNAPSHOT_DIR = Path(__file__).parent.parent / "__snapshots__"

_SAMPLE_FEATURES: list[ImpactResult] = [
    ImpactResult(
        feature=ClassifiedFeature(
            raw=RawItem(
                title="Google launches Gemini 3.1 Flash-Lite",
                link="https://blog.google/technology/ai/gemini-3-1",
                summary="",
                source_name="Google AI Blog",
                hint_company="Google",
            ),
            is_feature=True,
            feature_type="new_feature",
            confidence=92,
        ),
        impact_score=82,
        impact_label="Yüksek",
        rationale="Düşük maliyetli hızlı modeller pazarında doğrudan rekabet.",
    ),
    ImpactResult(
        feature=ClassifiedFeature(
            raw=RawItem(
                title="OpenAI introduces GPT-Rosalind",
                link="https://openai.com/index/gpt-rosalind",
                summary="",
                source_name="OpenAI News",
                hint_company="OpenAI",
            ),
            is_feature=True,
            feature_type="new_feature",
            confidence=95,
        ),
        impact_score=91,
        impact_label="Kritik",
        rationale="Alan-spesifik frontier modelinin yeni bir sektörü hedeflemesi paradigmatik.",
    ),
]


def _make_brief() -> DailyBrief:
    from collections import defaultdict

    by_company: dict = defaultdict(list)
    for f in _SAMPLE_FEATURES:
        by_company[f.feature.raw.hint_company or "Diğer"].append(f)
    by_company = dict(
        sorted(by_company.items(), key=lambda kv: max(x.impact_score for x in kv[1]), reverse=True)
    )

    return DailyBrief(
        date_tr="3 Mayıs 2026",
        day_name="Pazar",
        time_str="18:00",
        summary_tr="Bugün iki büyük hamle öne çıktı.",
        trends=["Hızlı modeller yaygınlaşıyor.", "Rekabet sertleşiyor."],
        insight="Önümüzdeki çeyrekte kazananlar alan-spesifik sağlayıcılar olacak.",
        top_features=_SAMPLE_FEATURES,
        by_company=by_company,
        stats={"total_features": 2, "unique_companies": 2, "avg_impact": 86},
    )


def test_render_html_contains_key_elements():
    brief = _make_brief()
    html = render_html(brief)
    assert "AI ÜRÜN RADARI" in html
    assert "Gemini 3.1 Flash-Lite" in html
    assert "GPT-Rosalind" in html
    assert "GÜNÜN ÖNE ÇIKAN GELİŞMESİ" in html
    assert "TRENDLER" in html
    assert "STRATEJİK İÇGÖRÜ" in html
    assert "forms.gle" in html


def test_render_text_contains_key_elements():
    brief = _make_brief()
    text = render_text(brief)
    assert "AI ÜRÜN RADARI" in text
    assert "Gemini 3.1 Flash-Lite" in text
    assert "TRENDLER" in text
    assert "bilalabic78@gmail.com" in text


def test_snapshot_html(tmp_path):
    brief = _make_brief()
    html = render_html(brief)

    snapshot_path = _SNAPSHOT_DIR / "brief_sample.html"
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)

    if not snapshot_path.exists():
        snapshot_path.write_text(html, encoding="utf-8")
        pytest.skip("Snapshot created — run again to verify")

    expected = snapshot_path.read_text(encoding="utf-8")
    assert html == expected, (
        "HTML snapshot mismatch. Delete tests/__snapshots__/brief_sample.html to regenerate."
    )


def test_get_day_name_tr():
    # Monday=0 → Pazartesi
    assert get_day_name_tr(0) == "Pazartesi"
    # Sunday=6 → Pazar
    assert get_day_name_tr(6) == "Pazar"
