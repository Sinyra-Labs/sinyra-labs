# Secrets Required

Repo ayarları: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | daily-pipeline | manual-backfill | test | Açıklama |
|--------|:--------------:|:---------------:|:----:|----------|
| `OPENAI_API_KEY` | ✅ zorunlu | ✅ zorunlu | — | OpenAI API anahtarı (`sk-...`) |
| `GMAIL_ADDRESS` | ✅ zorunlu | ✅ zorunlu | — | Gönderici Gmail adresi |
| `GMAIL_APP_PASSWORD` | ✅ zorunlu | ✅ zorunlu | — | Gmail Uygulama Şifresi (16 karakter, boşluksuz) |
| `EMAIL_TO` | ✅ zorunlu | ✅ zorunlu | — | Alıcı adresler, virgülle ayrılmış (örn. `a@b.com,c@d.com`) |
| `EMAIL_FROM_NAME` | ⚪ opsiyonel | ⚪ opsiyonel | — | Gönderici adı (varsayılan: `AI Ürün Radarı`) |
| `SLACK_WEBHOOK` | ⚪ opsiyonel | ⚪ opsiyonel | ⚪ opsiyonel | Slack Incoming Webhook URL — yoksa bildirim adımı sessizce atlanır |

## Gmail App Password nasıl alınır?

1. Google Hesabınızda 2FA etkin olmalı
2. https://myaccount.google.com/apppasswords → "Mail" + "Diğer cihaz" seç
3. Üretilen 16 karakterlik şifreyi `GMAIL_APP_PASSWORD` olarak kaydet (boşluklar olmadan)

## Slack Webhook nasıl alınır?

1. https://api.slack.com/apps → Create App → Incoming Webhooks
2. Webhook URL'yi kopyala → `SLACK_WEBHOOK` secret olarak ekle
3. Eklenmezse pipeline çalışmaya devam eder, sadece Slack bildirimi gitmez

## Manuel test

```bash
# Dry-run ile pipeline'ı test et (mail gitmez)
gh workflow run daily-pipeline.yml -f dry_run=true -f lookback_hours=24

# 7 günlük backfill (dry-run=true varsayılan)
gh workflow run manual-backfill.yml -f lookback_hours=168 -f dry_run=true
```
