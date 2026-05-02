GÖREV: .github/workflows/daily-pipeline.yml

Doküman'ın 4.4 bölümündeki şablonu referans al, ama:
- TR saat 18:00'e karşılık gelen UTC cron'u doğru hesapla
- workflow_dispatch input'u ekle (lookback_hours, dry_run)
- Cache: data/sinyra.db (seen-hashes için)
- Failure: Slack webhook'a post

Ayrıca:
- .github/workflows/test.yml — push/PR'da pytest + ruff
- .github/workflows/manual-backfill.yml — workflow_dispatch only, geçmiş 7 gün backfill

KONTROL LİSTESİ (her workflow için):
✅ timeout-minutes
✅ concurrency
✅ secrets değişkenleri Secrets sekmesinde
✅ artifacts upload
✅ failure notification

Output: 3 yml dosyası + bir SECRETS_REQUIRED.md (hangi secret hangi job'da).