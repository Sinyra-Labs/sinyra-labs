# Sinyra Labs — Sıfırdan Başlangıç Planı (v2.1)

> **Versiyon:** 2.1 · **Tarih:** Mayıs 2026
> **Setup:** Antigravity (IDE) + Claude Code (agent) + GitHub Actions (scheduler) + **Gmail SMTP** (mail)
> **Hedef:** 1 hafta içinde Apps Script'ten Python pipeline'a geçiş (F2 tamamlandı).

> **v2.0'dan değişen:** Resend tamamen kaldırıldı. Mail gönderimi **Gmail SMTP** ile yapılacak (mevcut Apps Script `MailApp.sendEmail` davranışıyla aynı: $0 maliyet, kendi Gmail'inden, kolay setup). Resend gibi 3rd-party email provider'lar **F3 veya sonrasında** marka/abone büyüyünce konuşulur.

---

## Bu Doküman Ne, Ne Değil

**Ne:** Adım adım, baştan sona, Claude Code ile Sinyra Labs'ı kurma planı. Her adımın **çıktısı** ve **doğrulama testi** belli.

**Ne değil:** Mimari/konumlandırma dokümanı (o `sinyra-labs-rehber.md`'de). Bu dosya o dokümanın **uygulama planı**.

**İlişki:**
- `sinyra-labs-rehber.md` → REFERANS (mimari, MCP, skills, prompt taslakları)
- `sinyra-labs-baslangic-plani-v2.1.md` → AKSİYON (bu dosya, otorite bunda)

> **Çakışma durumu:** Rehber'in 8.5 bölümünde Resend prompt'u var. Bu plan ondan **daha güncel**. Mail için bu dosyadaki P5 prompt'unu kullan.

---

## Rol Dağılımı (Net)

| İş | Kim |
|---|---|
| Kod yazma, refactor, dosya üretme | **Claude Code** |
| Plan, mimari karar | **Claude Code** |
| Editor, dosya gezme, git diff | **Antigravity** (IDE) |
| Terminal komutları, test, git commit | **Sen** (manuel) |
| Cron, otomasyon | **GitHub Actions** |
| Mail gönderimi | **Gmail SMTP** (smtplib) |

> **Antigravity'nin native Agent Manager'ını (Gemini 3) KULLANMA.** İki agent çakışır.

---

## Ön Koşullar (15-30 dakika)

### A. GitHub
- [ ] github.com → New repository → `sinyra-labs`
- [ ] **Public** seç
- [ ] Add: README, `.gitignore` (Python), MIT License

### B. OpenAI
- [ ] platform.openai.com → API keys → "Create new secret key"
- [ ] **Settings → Limits → Monthly budget: $10** (zorunlu)
- [ ] **Settings → Limits → Email alert: $5**

### C. Anthropic (Claude Code için)
- [ ] console.anthropic.com → Hesap aç
- [ ] Billing → "Add credits" → **minimum $5 yükle**
- [ ] Settings → API Keys → "Create Key"

### D. Gmail App Password (mail için)

> **Resend YERİNE bunu kullanıyoruz.** $0 maliyet, 5 dakika setup.

- [ ] Google hesabınla giriş yap → myaccount.google.com
- [ ] Security → **2-Step Verification açık olmalı** (değilse önce aç)
- [ ] Security → **App passwords** → Yeni: "Sinyra Labs"
- [ ] Üretilen 16 karakterli password'ü kaydet (bir daha göstermez)

> **Not:** Bu, normal Gmail şifren değil. App-specific bir token. SMTP login için kullanılır.

> **Limit:** Consumer Gmail hesabı **günde 500 mail**. Şu an ~30 abonen var, bu uzun süre yeter. Workspace hesabı kullanıyorsan limit 2000.

### E. Lokal makine
```bash
python3 --version       # 3.12+
node --version          # 20+
git --version
```

### F. Antigravity
- [ ] antigravity.google → Kur → Login

---

## Gün 1 — Lokal Kurulum + Claude Code (1 saat)

### 1.1 Repo'yu klonla
```bash
cd ~/projects
git clone https://github.com/<sen>/sinyra-labs.git
cd sinyra-labs
```

### 1.2 Dokümanları içeri kopyala
```bash
mkdir docs
cp /yol/sinyra-labs-rehber.md docs/
cp /yol/sinyra-labs-baslangic-plani-v2.1.md docs/
```

### 1.3 Antigravity ile aç
- File → Open Folder → `sinyra-labs`

### 1.4 Claude Code kur (Antigravity terminal)
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

### 1.5 Login
```bash
export ANTHROPIC_API_KEY=sk-ant-...
claude
```

### 1.6 Hızlı test
```bash
> "Bu repo'nun durumunu özetle."
```

---

## Gün 2 — CLAUDE.md + MCP'ler + İlk Plan (1.5 saat)

### 2.1 `CLAUDE.md` oluştur

Repo kökünde `CLAUDE.md`:

```markdown
# Sinyra Labs — Project Rules for Claude Code

## Stack
- Python 3.12, type-hinted (mypy strict)
- pydantic v2 at every data boundary
- httpx, feedparser, openai, jinja2, sqlalchemy, alembic
- Mail: smtplib + Gmail SMTP (NOT Resend; that's F3+)
- Test: pytest + VCR.py
- Lint/format: ruff (line-length 100)
- Package manager: uv

## Behavior Rules
- DO NOT run tests automatically. Show command, let user run.
- DO NOT add new dependencies without asking first.
- DO NOT delete or rewrite existing files unless explicitly requested.
- LLM calls MUST pass `model` and `temperature` as parameters.
- All prompts in `sinyra/intelligence/prompts/*.md`, versioned (v1, v2, ...).
- All timestamps UTC. Convert to TR only at presentation layer.
- Secrets only via `os.environ`. Keep `.env.example` updated.
- Update CHANGELOG.md on every meaningful change.

## Email Provider Rule
- Use abstract `EmailProvider` interface in sinyra/delivery/email/.
- Default impl: `GmailSmtpProvider` (port 465, SSL, App Password auth).
- DO NOT integrate Resend, SendGrid, or any 3rd-party email API in F2.
- The interface MUST allow swapping provider in F3 by changing one config value.

## Code Style
- Functions short, single-purpose. > 50 lines → refactor.
- Error messages in Turkish, log messages in English.
- HTML/email render via Jinja2; string concat FORBIDDEN.

## Output Format
- 3-line plan first, then code, then "why this choice".
- If ambiguous, ASK — do not guess.
- Speak Turkish to user, but code/comments/logs/commits in English.

## Reference Documents
- Architecture: docs/sinyra-labs-rehber.md
- Action plan (authoritative): docs/sinyra-labs-baslangic-plani-v2.1.md
- Read these BEFORE non-trivial changes.
- If rehber says "Resend" anywhere, IGNORE — plan v2.1 supersedes.
```

Save + commit:
```bash
git add CLAUDE.md
git commit -m "Add project rules"
```

### 2.2 `.mcp.json` oluştur

Repo kökünde:
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}"
      }
    }
  }
}
```

GitHub PAT üret (fine-grained, repo + workflow scope), `.zshrc`'ye:
```bash
export GITHUB_PAT=github_pat_...
```

### 2.3 Claude Code restart + MCP doğrula
```bash
claude
> /mcp
```

4 MCP listede görünmeli.

### 2.4 `prompts/` klasörü
```bash
mkdir prompts
touch prompts/p01-scaffold.md
touch prompts/p02-ingestion.md
touch prompts/p03-storage-dedup.md
touch prompts/p04-intelligence.md
touch prompts/p05-synthesis-delivery-gmail.md   # Gmail versiyonu
touch prompts/p06-github-actions.md
```

> **DİKKAT:** P5 dosya adı `p05-synthesis-delivery-gmail.md`. Rehberin 8.5'indeki Resend versiyonunu kullanma. Aşağıdaki "Gün 5"te P5'in yeni versiyonunu vereceğim — onu kopyala.

P1, P2, P3, P4, P6 → rehberin 8.x bölümlerinden olduğu gibi al.

### 2.5 İlk oturum: dokümanı okut
```bash
claude
```

İlk mesaj:
```
Bu workspace neredeyse boş. Sinyra Labs adlı bir AI signal
intelligence platformu kuracağım.

ÖNCE şu iki dokümanı oku:
1. docs/sinyra-labs-rehber.md (mimari, REFERANS)
2. docs/sinyra-labs-baslangic-plani-v2.1.md (uygulama planı, OTORİTE)

ÖNEMLİ: Rehberde Resend geçen yerler ESKİ. Plan v2.1 esas alınacak;
mail provider Gmail SMTP. Bunu CLAUDE.md'de de belirttim.

Sonra:
- 2 paragrafla anladığını özetle
- Gün 2 sonundayız: CLAUDE.md, .mcp.json, prompts/ hazır
- Yarın Gün 3'te P1 (scaffold) çalıştıracağız
- Risk veya soru?

Hiçbir kod yazma. Sadece anlama.
```

Cevabı oku, anladıysa:
```
> /exit
```

Commit + push:
```bash
git add .mcp.json prompts/
git commit -m "Add MCP config and prompt scripts"
git push
```

---

## Gün 3 — P1 İskelet + P2 Ingestion (2 saat)

### 3.1 P1: Scaffold
```bash
claude < prompts/p01-scaffold.md
```

Çıktı: `pyproject.toml`, `requirements.txt`, klasör yapısı, `.env.example`.

> **Önemli:** `.env.example` içinde **`RESEND_API_KEY` OLMAMALI**. Onun yerine:
> ```
> GMAIL_ADDRESS=bilalabic78@gmail.com
> GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
> EMAIL_FROM_NAME=AI Ürün Radarı
> ```

Eğer Claude `RESEND_API_KEY` koyduysa:
```
> "RESEND_API_KEY'i .env.example'dan çıkar.
> Yerine GMAIL_ADDRESS, GMAIL_APP_PASSWORD, EMAIL_FROM_NAME ekle.
> requirements.txt'te resend paketi varsa da çıkar."
```

### 3.2 Hızlı kontrol
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
ruff check sinyra/
mypy sinyra/
```

### 3.3 Commit
```bash
git add .
git commit -m "Initial scaffold (P1)"
git push
```

### 3.4 P2: Ingestion
```bash
claude < prompts/p02-ingestion.md
```

### 3.5 Lokal test
```bash
python -c "from sinyra.ingest.rss import fetch_all; print(len(fetch_all()))"
```

### 3.6 Commit
```bash
git add .
git commit -m "RSS + Google News ingestion (P2)"
git push
```

---

## Gün 4 — P3 Storage + P4 Intelligence (3 saat)

### 4.1 P3: Storage + Dedup
```bash
claude < prompts/p03-storage-dedup.md
pytest tests/unit/test_dedup.py -v
git commit -am "Storage + dedup (P3)"
```

### 4.2 P4: Intelligence
```bash
claude < prompts/p04-intelligence.md
```

### 4.3 Smoke test
```bash
echo "OPENAI_API_KEY=sk-..." >> .env
python -c "
from sinyra.ingest.rss import fetch_all
from sinyra.intelligence.classifier import classify
items = fetch_all()[:5]
for item in items:
    r = classify(item)
    print(item.title[:60], '->', r.is_feature, r.confidence)
"
```

### 4.4 Eval
```bash
pytest tests/eval/test_classifier.py -v
```

### 4.5 Commit
```bash
git commit -am "Intelligence layer + golden set (P4)"
git push
```

---

## Gün 5 — P5 Synthesis + Gmail Mail (2 saat)

### 5.1 P5 promptu (dosyaya yaz)

`prompts/p05-synthesis-delivery-gmail.md` içine **bunu yapıştır**:

```
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
```

### 5.2 Çalıştır
```bash
claude < prompts/p05-synthesis-delivery-gmail.md
```

### 5.3 KRİTİK: HTML birebir mi?

Browser'da preview:
```bash
python -c "
from sinyra.delivery.email.render import render_preview
render_preview('docs/preview.html')
"
open docs/preview.html
```

Mevcut Apps Script tasarımına benzemiyorsa Claude'a:
```
> "preview.html mevcut Apps Script tasarımına benzemiyor.
> Şu farkları gör [yapıştır]. Birebir port et."
```

### 5.4 Gerçek mail testi
```bash
# .env'e ekle
echo "GMAIL_ADDRESS=bilalabic78@gmail.com" >> .env
echo "GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx" >> .env
echo "EMAIL_FROM_NAME=AI Ürün Radarı" >> .env
echo "EMAIL_TO=bilalabic78@gmail.com" >> .env

# Tek alıcı, gerçek mail
python -m sinyra.run
```

Inbox'ı aç. Apps Script versiyonuyla aynı görünüyor mu?

> **Spam'a düşme uyarısı:** Gmail'den Gmail'e gönderim genelde sorunsuz. Ama "Promotions" sekmesine düşebilir. İlk mailde bunu kontrol et, gerekirse alıcılara "Primary'e taşıyın" diye not at.

### 5.5 Commit
```bash
git commit -am "Synthesis + Gmail SMTP delivery (P5)"
git push
```

---

## Gün 6 — P6 GitHub Actions (1.5 saat)

### 6.1 P6
```bash
claude < prompts/p06-github-actions.md
```

### 6.2 Secrets

GitHub repo → Settings → Secrets → New:
- `OPENAI_API_KEY`
- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD`
- `EMAIL_FROM_NAME`
- `EMAIL_TO`
- `SLACK_WEBHOOK` (opsiyonel)

> **Resend secret'ı YOK.** Eski plandan kalan `RESEND_API_KEY`'i ekleme.

### 6.3 Manuel test
```bash
git push
# GitHub Actions → Run workflow → dry_run: true
```

### 6.4 İlk gerçek run
- dry_run: false → Run
- 5-10 dk bekle, mail kontrolü

### 6.5 Cron aktifleşti
Push'la birlikte cron canlı. Yarın 17:30 TR'de otomatik.

### 6.6 Commit
```bash
git commit -am "GitHub Actions live"
git push
```

---

## Gün 7 — Custom Skills + Stabilizasyon (2 saat)

### 7.1 Skills
```bash
mkdir -p .claude/skills
```

İlk 3 skill (rehber bölüm 7'den):
- `.claude/skills/rss-source-validator/SKILL.md`
- `.claude/skills/prompt-tuner/SKILL.md`
- `.claude/skills/github-actions-deploy/SKILL.md`

### 7.2 Apps Script paralel
- Apps Script trigger 2 hafta açık tut
- Python pipeline'ı izle
- Stabil → Apps Script `deleteAllTriggers()`

### 7.3 Final commit
```bash
git add .claude/
git commit -m "Custom skills"
git push
```

---

## Hata Çıkarsa — Hızlı Tanı

| Belirti | İlk bakılacak yer |
|---|---|
| Claude Code "API rate limit" | console.anthropic.com → Usage; biraz bekle |
| `npx` MCP server başlatamıyor | `~/.config/claude-code/logs`; node sürümü |
| OpenAI 429 | Pipeline retry + backoff aktif mi |
| GitHub Actions cron çalışmıyor | UTC saat doğru mu; repo public mi |
| **Gmail SMTP "535 Authentication failed"** | App Password doğru mu, 2-Step Verification açık mı |
| **Gmail SMTP "Daily sending quota exceeded"** | 500 mail aşıldı; 24 saat bekle veya Workspace hesabı |
| Mail spam'a düşüyor | Gmail'den Gmail için "Promotions" normal; Primary'e manuel taşıt |
| Pipeline 0 feature buluyor | confidence_min düşür (50), classify v1 promptunu kontrol et |
| `mypy` hata yağmuru | `mypy.ini`'de `ignore_missing_imports = true` |

---

## Token Bütçesi (Realistik)

| Aşama | Claude Code | OpenAI | Toplam |
|---|---|---|---|
| Gün 1-2 setup | ~50K tokens | $0 | $0.50 |
| Gün 3 (P1+P2) | ~150K tokens | $0.10 | $1.80 |
| Gün 4 (P3+P4) | ~250K tokens | $0.50 | $3.50 |
| Gün 5 (P5) | ~120K tokens | $0.20 | $1.50 |
| Gün 6 (P6) | ~80K tokens | $0.50 | $1.20 |
| Gün 7 (skills) | ~60K tokens | $0 | $0.80 |
| **Toplam** | ~710K | ~$1.30 | **~$9.30** |

> $5 Anthropic + $5 OpenAI bütçesi 1 hafta için yeter.

---

## Aylık Çalışma Maliyeti (F2 Production)

| Kalem | Aylık |
|---|---|
| OpenAI (gpt-4o-mini) | $1-2 |
| **Gmail SMTP** | **$0** |
| GitHub Actions (public repo) | $0 |
| Domain (varsa, opsiyonel) | $1 |
| **TOPLAM** | **~$2-3/ay** |

> Yıllık ~$30. Apps Script versiyonundan ~$30 daha pahalı (o $0 idi) ama:
> - Versiyon kontrolü ✓
> - Lokal test edilebilir ✓
> - Reproducible ✓
> - SaaS'a geçiş yolu açık ✓
> Bu fark iyi yatırım.

---

## Geliştirme Disiplini

1. **Her promptun sonunda commit.**
2. **Test'i sen koş, Claude değil.**
3. **`git diff` her commit öncesi.**
4. **Plan onayını oku, hızlı geçme.**
5. **Kütüphane sorulduğunda "neden" iste.**
6. **`/clear` uzun oturumlarda.**

---

## Bir Sonraki Adımlar (Hafta 2+)

- **Hafta 2:** Apps Script paralel; bug fix; classify v2 iterasyonu
- **Hafta 3-4:** F3 başla — Supabase, basit landing page (rehber P9)
- **Ay 2:** F4 multi-channel (Telegram bot)
- **Ay 3+:** F5 SaaS planlaması (rehber P10)

> **F3'te tartışılacak:** Resend gerekli mi? Kendi domain'in (sinyra.com) hazır olduğunda, marka için `radar@sinyra.com`'dan göndermek değer kazanır. O zaman EmailProvider arayüzünü genişlet, yeni `ResendProvider` ekle, env değişkeniyle aktif et. F2'de bu iş yok.

---

## Hızlı Referans — Komutlar

```bash
# Claude Code
claude
claude < prompts/p01-scaffold.md
/clear
/mcp
/exit

# Pipeline
python -m sinyra.run
python -m sinyra.run --dry-run

# Test
pytest tests/unit/ -v
pytest tests/eval/ -v

# Lint
ruff check sinyra/
ruff format sinyra/
mypy sinyra/

# GitHub Actions
gh workflow run daily-pipeline.yml
gh run list --workflow=daily-pipeline.yml
gh run view <run-id> --log

# Gmail SMTP test (Claude Code dışı, lokal hızlı kontrol)
python -c "
import smtplib, os
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
    s.login(os.environ['GMAIL_ADDRESS'], os.environ['GMAIL_APP_PASSWORD'])
    print('Login OK')
"
```

---

## Kontrol Listesi

- [ ] **Ön A** GitHub repo
- [ ] **Ön B** OpenAI key + budget
- [ ] **Ön C** Anthropic credit + key
- [ ] **Ön D** Gmail App Password
- [ ] **Ön E** Lokal Python 3.12 + Node 20
- [ ] **Ön F** Antigravity kurulu
- [ ] **Gün 1** Claude Code login
- [ ] **Gün 2** CLAUDE.md, .mcp.json, prompts/, ilk plan onaylandı
- [ ] **Gün 3** P1 + P2; RSS'ler geliyor
- [ ] **Gün 4** P3 + P4; LLM çağrısı çalışıyor
- [ ] **Gün 5** P5; ilk lokal mail Gmail'den geldi
- [ ] **Gün 6** P6; ilk otomatik mail (GitHub Actions)
- [ ] **Gün 7** Skills + paralel plan

---

**Bittiğinde:** F2 production'da. Toplam efor ~12-15 saat, tek seferlik maliyet ~$10, aylık çalışma maliyeti ~$2. Resend yok; Gmail SMTP ile her şey çözüldü.
