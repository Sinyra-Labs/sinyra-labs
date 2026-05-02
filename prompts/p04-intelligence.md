GÖREV: sinyra/intelligence/ — feature classifier + impact scorer.

Yapı:
- classifier.py: classify(item: RawItem) -> ClassificationResult
- impact_scorer.py: score(feature: ClassifiedFeature) -> ImpactResult
- prompts/classify.v1.md, prompts/impact.v1.md (mevcut Apps Script promptlarımı buraya
  port edeceğiz; Türkçe; JSON-only output)

LLM client: OpenAI Python SDK, response_format={"type": "json_object"}.

KURALLAR:
- Tek bir openai_client.py — token budget tracking, retry, structured logging.
- Her LLM çağrısı: model, temperature, prompt_version, latency_ms loglanır.
- ClassificationResult ve ImpactResult pydantic model — JSON parse'ı schema'ya bağla
  (Pydantic .model_validate_json kullan).
- Confidence < CONFIDENCE_MIN ise filtre. Impact < IMPACT_MIN ise filtre.

Eval: tests/eval/golden_set.jsonl — 30 satırlık örnek dataset oluştur (mevcut bilgine
göre uydurabilirsin, label'lar gerçekçi olsun). pytest tests/eval/test_classifier.py
ile çalışan basic precision/recall raporu yaz.