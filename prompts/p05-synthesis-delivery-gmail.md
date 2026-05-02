GÖREV: Synthesis + Email delivery layer.

Yapı:
- sinyra/synthesis/brief.py: generate_daily_brief(features) -> DailyBrief
  (summary_tr, trends[], insight)
- sinyra/delivery/email/render.py: Jinja2 ile HTML render
- sinyra/delivery/email/templates/brief.html: mevcut Apps Script tasarımı
  birebir port — table-based layout, inline CSS, max-width 640px,
  koyu hero (#0b1120), istatistik şeridi, spotlight kartı, şirket grupları,
  trends kartı, insight kartı, paylaş kartı (forms.gle/...), iletişim kartı.
  Apps Script'teki escape, impactColor, impactLabel, impactBg, translateType,
  getDayNameTR helper'larını Python'a port et (sinyra/delivery/email/helpers.py).
- sinyra/delivery/email/templates/brief.txt: plain text fallback (mevcut Apps
  Script buildPlainText birebir).

EMAIL PROVIDER (KRİTİK):
- sinyra/delivery/email/provider.py içinde abstract base class:

  class EmailProvider(Protocol):
      def send(self, to: str, subject: str, html: str, text: str) -> None: ...

- sinyra/delivery/email/gmail_smtp.py içinde implementation:
  - smtplib.SMTP_SSL("smtp.gmail.com", 465)
  - login: GMAIL_ADDRESS + GMAIL_APP_PASSWORD env
  - From: f"{EMAIL_FROM_NAME} <{GMAIL_ADDRESS}>"
  - MIMEMultipart("alternative") ile text + html
  - Hata yönetimi: SMTPException yakalanıp loglansın, fail edip pipeline'ı
    durdurmasın (bir alıcıya gidemediyse diğerlerine devam etsin)

- sinyra/delivery/email/send.py: factory/dispatcher
  def send_brief(brief: DailyBrief, recipients: list[str]) -> SendStats
  - Provider'ı os.environ.get("EMAIL_PROVIDER", "gmail_smtp") ile seçer
  - Şu an sadece "gmail_smtp" desteklenir; F3'te "resend" eklenebilir

- sinyra/run.py: tüm pipeline'ı bağlar:
  fetch -> dedup -> classify -> filter -> score -> synthesis -> render -> send

KAPSAM DIŞI:
- Resend, SendGrid, Mailgun YOK. Sadece smtplib + Gmail.
- Webhook, bounce handling YOK (Gmail'de gerek yok; F3'te konuşulur).

KURAL:
- requirements.txt'e SADECE jinja2 ekle (smtplib stdlib, paket gerekmiyor).
- resend paketi yüklü ise çıkar.
- HTML hardcoded string YOK; Jinja2 template.
- Snapshot test: tests/__snapshots__/brief_sample.html (sample data ile render).

Mail listesi şimdilik:
- .env'den EMAIL_TO (virgülle ayrılmış) okur
- F2.1'de Google Sheets entegrasyonu eklenecek (ayrı PR)

Önce planı 3 satırla anlat, onayımı bekle, sonra kod.