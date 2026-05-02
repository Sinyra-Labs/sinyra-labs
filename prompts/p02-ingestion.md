Workspace zaten kurulu. Şimdi L1 INGESTION LAYER:

GÖREV: sinyra/ingest/ altında üç dosya:
- feeds.yaml — kaynak listesi (RSS feeds + Google News queries). Mevcut Apps Script
  kodumdaki listeyi YAML'a çevir; her item: name, url, type (rss|gnews), company (optional).
- rss.py — feedparser kullanarak fetch fonksiyonu. async değil, sync yeterli ilk versiyonda.
- google_news.py — Google News RSS query helper.

ÇIKTI SCHEMA: pydantic model `RawItem` — fields: title, link, summary, pub_date, source_name, hint_company.

KURALLAR:
- Her HTTP isteği User-Agent ile, timeout=15, max 3 retry (exponential backoff via httpx).
- Logging: structlog kullan, JSON output. Debug log: feed başına item sayısı.
- Strip HTML, max 600 char summary (mevcut Apps Script davranışıyla aynı).
- Hatalı feed'i exception YAPMA — empty list döndür ve warning logla.

UNUTMA:
- Type hint zorunlu.
- requirements.txt'i güncelle.
- tests/unit/test_rss.py'a 1 sample fixture ile basit happy-path test ekle (VCR.py ile).

Bittiğinde diff özeti ver.