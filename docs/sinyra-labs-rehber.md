# Sinyra Labs — Stratejik Konumlandırma ve Antigravity ile Geliştirme Rehberi

> **Versiyon:** 1.0 · **Tarih:** Mayıs 2026 · **Hazırlayan:** Bilal Abıç (Sinyra Labs)
> **Kapsam:** Ürün konumlandırması, v2 mimarisi, GitHub Actions migrasyonu, Google Antigravity için MCP/Skills kurulumu ve hazır promptlar.

---

## 1. Yönetici Özeti (TL;DR)

Sinyra Labs, **"AI ekosistemindeki gürültüyü, ölçülebilir sinyallere çeviren bir Intelligence Platform"** olarak konumlandırılmalı. Mevcut Apps Script MVP'si kavramı kanıtladı; bir sonraki adım üç şeyle tanımlanıyor:

1. **Konumlandırma keskinliği:** "Bir başka AI haber bülteni" değil, **etki skorlamalı sinyal motoru**.
2. **Mimari upgrade:** Apps Script → **Python pipeline + GitHub Actions + kalıcı depolama**.
3. **Geliştirme deneyimi:** Antigravity'de doğru **MCP + Skill + Rule** seti ile "tek başına hızlı geliştiren" bir setup.

Bu doküman üçünü de uçtan uca verir; sonunda kopyala-yapıştır promptlar var.

---

## 2. Ürün Konumlandırması (Net)

### 2.1 Tek Cümlelik Konumlandırma

> **Sinyra Labs**, AI ekosistemindeki yüzlerce haber, blog ve duyurudan gerçek ürün/özellik lansmanlarını tespit eden, etkisini 0-100 arası skorlayan ve günlük yönetici brifingi üreten **AI Signal Intelligence Platform**'udur.

### 2.2 Üç Cümlelik Pitch (Pazarlama için)

> AI dünyasında her gün 500+ "duyuru" çıkıyor; çoğu hype, listicle veya yatırım haberi. Sinyra Labs bunu pipeline ile filtreliyor: önce gerçek lansman mı diye sınıflandırıyor, sonra sektör etkisini puanlıyor, sonra yönetici özeti yazıyor. Sonuç: 5 dakikada günün gerçek olayını öğrenirsiniz.

### 2.3 Hedef Kullanıcı Segmentleri (öncelik sırasıyla)

| Segment | Sinyra'dan Beklediği | Ödeme İsteği |
|---|---|---|
| **AI ürün/founder'ları** | Rekabet izleme, ne zaman pivot/copy edileceğine karar | Yüksek |
| **CTO/Tech lead'ler** | Stack ve roadmap kararları için sinyal | Yüksek |
| **VC/yatırımcılar** | Trend tespiti, deal sourcing | En yüksek (B2B SaaS) |
| **Developer Relations** | İçerik fikirleri, hangi feature'a yorum yazılacağı | Orta |
| **Tech gazetecileri** | Story sourcing | Düşük |
| **Meraklı developer** | Bilgi bülteni | Düşük (free tier) |

> **Kritik:** Faz 4'te SaaS olduğunda **founder + CTO + VC** üçlüsüne odaklan. "Meraklı developer" free tier'a düşer (kendi büyüme motorun zaten o).

### 2.4 Rekabet Tablosu

| Ürün | Yaklaşım | Sinyra'nın Farkı |
|---|---|---|
| TLDR AI, Ben's Bites, Rundown AI | Editöryel curation (insan editör) | **Otomatik + skorlu**; tek editöre bağımlı değil, ölçeklenir |
| AlphaSignal | Curation + bazı otomasyon | Sinyra **etki skoru ve tipoloji** veriyor (yeni özellik / model / araştırma) |
| Google Alerts | Anahtar kelime alarmı | Sinyra **gürültüyü filtreliyor**; anahtar kelime değil "gerçek lansman" tespiti |
| Smol AI / Latent Space | Derin teknik analiz | Sinyra **brifing seviyesi** (5 dk) — derinlemesine değil, kapsayıcı |
| Feedly + AI | Kullanıcının kendi setup'ı | Sinyra **opinionated**; sen düşünmeden gelir |

**Tek cümlelik diferansiyon:**
> "Diğerleri haberleri *seçer*; biz haberleri *skorlar* ve sektör etkisini ölçeriz."

### 2.5 Marka & Mesaj

- **Tagline (öneri):** *"Cut Through the Noise."* (Slogan listende vardı; en güçlüsü bu.)
- **İkinci tagline (yerel):** *"Veriden karara, gürültüden sinyale."*
- **Marka tonu:** Kısa, net, abartısız, "yöneticiye saygı duyan analist" sesi.
- **Görsel kimlik (öneri):** Koyu lacivert (#0b1120) + sarı vurgu (#fbbf24) + kırmızı uyarı (#b91c1c). Mevcut e-posta tasarımın bu yönde, koru.

### 2.6 Değer Önerisi Katmanları (Value Stack)

```
KATMAN 4 — STRATEJİK İÇGÖRÜ      (insight cümlesi)
KATMAN 3 — TREND TESPİTİ          (3 trend cümlesi)
KATMAN 2 — ETKİ SKORLAMASI        (her özellik 0-100)
KATMAN 1 — FİLTRELEME             (hype/listicle elenir)
KATMAN 0 — TOPLAMA                (RSS + Google News)
```

> Rakipler genelde Katman 0-1'de durur. Sinyra'nın savunma hattı **Katman 2-4**.

### 2.7 Konumlandırma Karşılaştırması: "Şu Değil, Bu"

| Sinyra Labs **şu değil** | Sinyra Labs **bu** |
|---|---|
| Haber agregatörü | Sinyal işleyici |
| AI bülteni | AI radarı |
| Curation servisi | Skorlama motoru |
| Generic özet | Yönetici brifingi |
| Editöre bağımlı | Pipeline'a bağımlı |

---

## 3. Vizyon ve Roadmap

### 3.1 Faz Faz Plan

| Faz | Süre | Çıktı | Başarı Metriği |
|---|---|---|---|
| **F1 — MVP (mevcut)** | tamamlandı | Apps Script + günlük e-posta | Çalışan pipeline, ~30+ alıcı |
| **F2 — Pro Pipeline** | 4-6 hafta | Python + GitHub Actions + SQLite | Apps Script bağımlılığı yok, %100 reproducible |
| **F3 — Veri Katmanı** | 4 hafta | Postgres/Supabase, embedding dedup, web dashboard | Geçmiş aranabilir, public landing page |
| **F4 — Multi-channel** | 4 hafta | Telegram bot, webhook, RSS-of-summaries | Kullanıcı kendi kanalını seçer |
| **F5 — SaaS** | 8+ hafta | Self-serve signup, Stripe, kullanıcıya özel filtreler | İlk 10 ödeyen kullanıcı |
| **F6 — API ürün** | sonra | Geliştiricilere ham sinyal API'si | API key satışı |

> **Karar:** F2'yi Antigravity ile yapıyoruz. Bu doküman F2-F3'e odaklı.

### 3.2 Monetizasyon (ileride)

- **Free tier:** Günlük genel brifing
- **Pro ($15/ay):** Kişiselleştirilmiş filtreler (örn. "sadece OpenAI + Anthropic"), Telegram, geçmişte arama
- **Team ($49/ay):** Ekip için ortak gündem, Slack entegrasyonu, custom skor kuralları
- **API ($99/ay+):** Diğer ürünlere ham sinyal akışı

---

## 4. Teknik Mimari (v2.0 — GitHub Actions Native)

### 4.1 Katman Katman

```
┌──────────────────────────────────────────────────────────┐
│  L0 SCHEDULER — GitHub Actions cron + workflow_dispatch  │
└──────────────────────┬───────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│  L1 INGESTION                                             │
│   • feedparser (RSS/Atom)                                 │
│   • httpx (Google News, fallback)                         │
│   • Firecrawl/Playwright (JS-rendered fallback, ileride)  │
└──────────────────────┬───────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│  L2 NORMALIZATION & DEDUP                                 │
│   • Pydantic schema                                       │
│   • Hash-based dedup → SQLite (F2) → Postgres (F3)        │
│   • Recency filter (configurable)                         │
└──────────────────────┬───────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│  L3 INTELLIGENCE (LLM)                                    │
│   • Feature classifier  (gpt-4o-mini)                     │
│   • Confidence scorer                                     │
│   • Impact scorer (0-100)                                 │
│   • Embedding-based semantic dedup (F3)                   │
└──────────────────────┬───────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│  L4 SYNTHESIS                                             │
│   • Daily executive brief                                 │
│   • Trend extraction                                      │
│   • Strategic insight                                     │
└──────────────────────┬───────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│  L5 DELIVERY                                              │
│   • Email (Resend / SendGrid / SMTP)                      │
│   • Telegram bot (F4)                                     │
│   • Webhook + JSON feed (F4)                              │
│   • Web dashboard (F3+)                                   │
└──────────────────────┬───────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────┐
│  L6 OBSERVABILITY                                         │
│   • Run logs (Actions artifacts)                          │
│   • Slack/Discord failure alerts                          │
│   • Daily metrics (kaç haber, kaç eleme, ort. skor)       │
└───────────────────────────────────────────────────────────┘
```

### 4.2 Tech Stack Kararları (opinionated)

| Katman | Tercih | Neden |
|---|---|---|
| Dil | **Python 3.12** | LLM ekosistemi, feedparser, hızlı yazma |
| HTTP | **httpx** (async-ready) | Modern, requests'ten daha iyi |
| RSS | **feedparser** | Standart, battle-tested |
| Validation | **pydantic v2** | Type-safe, JSON-friendly |
| LLM | **OpenAI** (mevcut) + opsiyonel **Anthropic Claude** A/B | Mevcut prompt yatırımını koru |
| Storage | **SQLite** (F2) → **Supabase Postgres** (F3) | Önce zero-ops, sonra cloud |
| Email | **Resend** | Apps Script GmailApp limiti yok, dev-friendly |
| Test | **pytest** + **VCR.py** (RSS cache) | Dış servislere bağımlı değil |
| Lint/Format | **ruff** | Hızlı, opinionated |
| Paket yönetimi | **uv** | pip'ten 10x hızlı, Antigravity'de iyi çalışıyor |
| CI/CD | **GitHub Actions** | Bedava, Cron yerleşik |

### 4.3 Önerilen Repo Yapısı

```
sinyra-labs/
├── .github/
│   └── workflows/
│       ├── daily-pipeline.yml        # ana cron
│       ├── manual-backfill.yml       # workflow_dispatch ile geçmiş tarama
│       ├── test.yml                  # PR/push tetikli
│       └── prompt-eval.yml           # haftalık prompt eval
│
├── .agent/                           # ANTIGRAVITY workspace
│   ├── rules.md                      # global proje kuralları
│   └── skills/
│       ├── rss-source-validator/
│       │   ├── SKILL.md
│       │   └── scripts/validate.py
│       ├── prompt-tuner/
│       │   ├── SKILL.md
│       │   └── scripts/eval.py
│       ├── impact-evaluator/
│       │   └── SKILL.md
│       ├── github-actions-deploy/
│       │   └── SKILL.md
│       ├── brief-renderer/
│       │   └── SKILL.md
│       └── db-migrator/
│           └── SKILL.md
│
├── sinyra/
│   ├── __init__.py
│   ├── config.py                     # tek yerden config (env-aware)
│   │
│   ├── ingest/
│   │   ├── __init__.py
│   │   ├── rss.py
│   │   ├── google_news.py
│   │   └── feeds.yaml                # kaynak listesi (kod değil!)
│   │
│   ├── normalize/
│   │   ├── schema.py                 # pydantic models
│   │   ├── dedup.py                  # hash + (F3) embedding
│   │   └── recency.py
│   │
│   ├── intelligence/
│   │   ├── classifier.py
│   │   ├── impact_scorer.py
│   │   └── prompts/                  # versiyonlanmış prompt dosyaları
│   │       ├── classify.v1.md
│   │       ├── classify.v2.md
│   │       └── impact.v1.md
│   │
│   ├── synthesis/
│   │   ├── brief.py
│   │   └── trends.py
│   │
│   ├── delivery/
│   │   ├── email/
│   │   │   ├── send.py
│   │   │   ├── render.py             # Jinja2 template
│   │   │   └── templates/
│   │   │       ├── brief.html
│   │   │       └── brief.txt
│   │   └── telegram.py               # F4
│   │
│   ├── storage/
│   │   ├── memory.py                 # seen-hashes
│   │   ├── models.py                 # SQLAlchemy
│   │   └── migrations/               # alembic
│   │
│   ├── observability/
│   │   ├── metrics.py
│   │   └── alerts.py
│   │
│   └── run.py                        # entrypoint
│
├── tests/
│   ├── fixtures/                     # VCR cassettes, sample feeds
│   ├── unit/
│   ├── integration/
│   └── eval/                         # prompt eval suite
│       └── golden_set.jsonl          # 50+ etiketli haber
│
├── data/                             # gitignore (run artifacts)
├── prompts/                          # public prompt registry (opsiyonel)
├── docs/
│   ├── architecture.md
│   ├── runbook.md
│   └── prompts.md
│
├── pyproject.toml                    # uv/poetry
├── requirements.txt                  # CI için lock
├── README.md
├── mcp_config.json                   # workspace MCP config
└── .env.example
```

### 4.4 GitHub Actions — Ana Workflow Şablonu

`.github/workflows/daily-pipeline.yml`:

```yaml
name: Sinyra · Daily Intelligence Run

on:
  schedule:
    # NOT: GitHub Actions UTC. TR (UTC+3) saat 18:00 = UTC 15:00.
    # Yine de 5-15 dk gecikme normaldir; safe-buffer için 14:30 UTC seçtim.
    - cron: '30 14 * * *'
  workflow_dispatch:
    inputs:
      lookback_hours:
        description: 'Geriye dönük tarama saati'
        required: false
        default: '72'
      dry_run:
        description: 'Mail gönderme, sadece logla'
        type: boolean
        default: false

concurrency:
  group: daily-pipeline
  cancel-in-progress: false

jobs:
  run:
    runs-on: ubuntu-latest
    timeout-minutes: 25
    permissions:
      contents: write   # cache commit için (opsiyonel)

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install deps (uv)
        run: |
          pip install uv
          uv pip install --system -r requirements.txt

      - name: Restore seen-hashes cache
        uses: actions/cache@v4
        with:
          path: data/seen.sqlite
          key: seen-${{ github.run_id }}
          restore-keys: seen-

      - name: Run pipeline
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
          GOOGLE_SHEET_ID: ${{ secrets.GOOGLE_SHEET_ID }}
          DRY_RUN:        ${{ github.event.inputs.dry_run || 'false' }}
          LOOKBACK_HOURS: ${{ github.event.inputs.lookback_hours || '72' }}
        run: python -m sinyra.run

      - name: Upload run artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: sinyra-run-${{ github.run_id }}
          path: |
            data/output/
            data/logs/
          retention-days: 30

      - name: Notify failure
        if: failure()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d "{\"text\":\"⚠️ Sinyra pipeline başarısız — Run #${{ github.run_id }}\"}"
```

> **GitHub Actions Pratik Notlar:**
> - Cron **her zaman UTC**. Türkiye saatine göre `+3` çıkar.
> - GitHub cron **5-15 dakika gecikebilir** (queue). Email saatini hassas planlama, ±15 dk tolerans bırak.
> - Free tier'da public repo unlimited, private 2000 dk/ay. Sinyra için fazlasıyla yeter.
> - Secret'ları **repo settings → Secrets and variables → Actions**'tan ekle. Asla commit etme.
> - `concurrency` aynı anda iki kez çalışmasını engeller.

---

## 5. Google Antigravity Kurulumu — Genel Çerçeve

### 5.1 Kafa Karışıklığı: Skill mi MCP mi?

İkisini şöyle ayır:

| | **MCP (Tool)** | **Skill** |
|---|---|---|
| Ne | "Eller" — deterministik fonksiyonlar (read_file, run_query) | "Beyin" — strateji & metodoloji |
| Mimari | Client-server, kalıcı süreç | Dosya tabanlı, ephemeral |
| Bulunma | `mcp_config.json` | `.agent/skills/` veya `~/.gemini/antigravity/skills/` |
| Yüklenme | Her zaman aktif | İhtiyaç anında progressive disclosure |
| Örnek | "Postgres MCP — query çalıştırır" | "Database Migration Skill — Postgres MCP'yi nasıl kullanacağını anlatır" |

**Pratik kural:**
- **Tekrarlanan, deterministik bir işlem var mı?** → MCP yaz/yükle.
- **Bir işin "doğru yapılma yöntemi" var mı?** → Skill yaz.
- **Hem yöntem hem araç gerekiyor mu?** → Skill, MCP'yi *çağırır*.

### 5.2 Antigravity Workspace Yapılandırması

Sinyra Labs için iki dosya kritik:

1. **`.agent/rules.md`** — projenin tamamı için kalıcı kurallar (her agent çağrısına dahil edilir)
2. **`mcp_config.json`** — bu workspace için aktif MCP sunucuları

#### `.agent/rules.md` (önerilen başlangıç)

```markdown
# Sinyra Labs — Agent Rules

## Stack
- Python 3.12, async-friendly, type-hinted (mypy strict)
- pydantic v2 modelleri her veri sınırında
- httpx, feedparser, openai, jinja2, sqlalchemy, alembic, resend
- Test: pytest + VCR.py
- Lint/format: ruff (line-length 100)

## Davranış Kuralları
- TEST OTOMATIK ÇALIŞTIRMA. Önce göster, kullanıcı manuel çalıştıracak.
- Yeni dış kütüphane eklemeden önce sor.
- LLM çağrılarında **mutlaka** `temperature` ve `model` parametre olarak geçir.
- Tüm prompt'lar `sinyra/intelligence/prompts/*.md` içinde versiyonlu (v1, v2, ...).
- Tüm zaman damgaları UTC. TR'ye sadece sunum katmanında çevir.
- Secret'lar yalnızca `os.environ`. `.env.example`'i güncel tut.
- Her PR'da CHANGELOG.md güncellenir.

## Kod Stili
- Functions short, single-purpose. > 50 satır → refactor.
- Hata mesajları Türkçe, log mesajları İngilizce.
- HTML/email render Jinja2; string concat YASAK.

## Çıktı Formatı
- Bana cevap verirken: önce 2 satır plan, sonra kod, sonra "neden bu seçim".
- Belirsizlik varsa varsayım yapma — sor.
```

#### `mcp_config.json` — Sinyra için minimum set

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
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${workspaceFolder}"]
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

> **Not:** Antigravity'de `MCP Store`'dan UI ile de kurabilirsin (Agent panel → "..." → MCP Servers). JSON yöntemi versiyon kontrolü için daha iyi.

---

## 6. Önerilen MCP Sunucuları (Sinyra Labs için)

### 6.1 Must Have (ilk gün)

#### 1. **Sequential Thinking MCP**
- **Ne işe yarar:** Çok adımlı planlamayı agent'a dayatır. "Önce bunu, sonra şunu, başarısız olursa şu fallback."
- **Sinyra'da nerede:** Pipeline tasarımı, prompt iterasyonu, mimari kararları.
- **Neden:** Antigravity Gemini 3.1 zaten iyi planlıyor ama bu skill onu **dışarı yazmaya** zorluyor — sen de gözden geçirebiliyorsun.
- **Kurulum:** MCP Store → Sequential Thinking → Install.

#### 2. **Context-7 MCP**
- **Ne işe yarar:** Live, taze dokümantasyon getiriyor — eğitim cutoff'u problemi yok.
- **Sinyra'da nerede:** OpenAI SDK, feedparser, pydantic v2, FastAPI, Resend, Supabase docs.
- **Neden:** Eğitim verisi 2024-2025 olabilir; SDK'lar değişti. Context7 her seferinde güncel.
- **Kullanım örneği:** "OpenAI structured output ile JSON schema vermek istiyorum, /context7 openai sdk".
- **Kurulum:** MCP Store'da var.

#### 3. **Filesystem MCP**
- **Ne işe yarar:** Workspace dosya okuma/yazma (genelde built-in ama explicit kontrol için).
- **Sinyra'da nerede:** Her yerde.
- **Neden:** Built-in olsa da limitleri açık tanımlamak güvenli.

#### 4. **GitHub MCP**
- **Ne işe yarar:** Repo, PR, Issue, Actions runs — agent doğrudan yönetir.
- **Sinyra'da nerede:** PR açma, workflow run logu, secret listesi check, issue triaging.
- **Neden:** "GitHub Actions failed" gördüğünde Antigravity'den çıkmadan log görebilirsin.
- **Token:** Repo + workflow scope'lu PAT (fine-grained).

### 6.2 Should Have (ilk ay)

#### 5. **Firecrawl MCP** *(veya Brave Search MCP)*
- **Ne işe yarar:** Web scraping + arama, Markdown output.
- **Sinyra'da nerede:** Yeni RSS kaynağı eklerken — "TechCrunch AI'nın RSS'i hâlâ aktif mi, son 5 başlık ne?" sorusu.
- **Alternatif:** Brave Search MCP, daha ucuz ama JS render etmez.

#### 6. **Supabase MCP** *(F3'te)*
- **Ne işe yarar:** Postgres ops doğrudan IDE'den.
- **Sinyra'da nerede:** F3'te seen-hashes ve features tablosu Supabase'e geçince.
- **Neden:** Schema explore + migration check.
- **Kurulum:** Supabase MCP Store'da; access token gerekli.

#### 7. **Playwright MCP** *(opsiyonel)*
- **Ne işe yarar:** JS-rendered sayfalar (örn. Anthropic'in news sayfası bazen).
- **Sinyra'da nerede:** RSS olmayan kaynaklara fallback.

### 6.3 Nice to Have

#### 8. **Rube MCP** *(by Composio)*
- **Ne işe yarar:** **Tek MCP üzerinden** Gmail, Slack, Notion, Stripe, Linear vs.
- **Neden:** Onlarca MCP yerine bir tane. Context window'u şişirmiyor — dinamik tool loading.
- **Sinyra'da nerede:** F4'te delivery channel'larını dağıtmaya başlayınca.

#### 9. **Notion MCP** veya **Slack MCP**
- **Ne işe yarar:** Çıktıları doğrudan workspace'e yollamak (F4 delivery).

### 6.4 Önerilen Kurulum Sırası

```
Hafta 1:  Sequential Thinking + Context-7 + Filesystem + GitHub
Hafta 2:  Firecrawl (yeni feed test ederken)
Hafta 4:  (F3) Supabase
Hafta 8:  (F4) Rube veya doğrudan Slack/Telegram MCP
```

---

## 7. Önerilen Skills (Custom Workspace Skills)

> Skills, `<workspace>/.agent/skills/<skill-name>/SKILL.md` yapısında. Her skill bir görevin "nasıl yapılacağını" anlatır ve gerekirse script çalıştırır.

### 7.1 `rss-source-validator`

**Ne yapar:** Verilen URL'in valid RSS/Atom olup olmadığını kontrol eder, son 5 item'ı çeker, encoding ve pubDate sorunlarını raporlar.

**Tetikleyici:** "Yeni feed ekle", "feed test et", "Bu URL RSS mi?"

```markdown
---
name: rss-source-validator
description: |
  Validate RSS/Atom feed URLs. Use when adding a new news source to feeds.yaml,
  diagnosing why a feed returns 0 items, or auditing feed health.
---

# RSS Source Validator

## When to use
- User mentions adding/testing/auditing an RSS or Atom feed.
- A feed in `sinyra/ingest/feeds.yaml` is suspected broken.

## How to run
```bash
python .agent/skills/rss-source-validator/scripts/validate.py <URL>
```

## Output contract
- Status (200/4xx/5xx)
- Format (RSS 2.0 / Atom)
- Item count, latest pubDate
- Encoding warnings
- Suggested entry for `feeds.yaml`

## Failure modes
- HTTP 403 → Add User-Agent header, retest
- Returns HTML not XML → not a feed; suggest Firecrawl scrape
- pubDate missing on all items → set `KEEP_IF_NO_DATE: true` in config
```

### 7.2 `prompt-tuner`

**Ne yapar:** Bir prompt versiyonunu (`prompts/classify.v2.md`) golden set'e karşı çalıştırır, precision/recall raporu basar.

**Tetikleyici:** "Classifier'ı iyileştir", "yeni prompt versiyonu", "false positive yüksek".

```markdown
---
name: prompt-tuner
description: |
  Evaluate and iterate on intelligence-layer prompts (classifier, impact scorer)
  against the golden test set in tests/eval/golden_set.jsonl. Use when modifying
  any file under sinyra/intelligence/prompts/ or when classification quality
  needs review.
---

# Prompt Tuner

## When to use
- User edits a prompt under `sinyra/intelligence/prompts/`.
- User asks "how good is the classifier".
- New noise pattern needs to be added.

## How to run
1. Read current prompt: `sinyra/intelligence/prompts/<name>.<version>.md`
2. Run: `pytest tests/eval/test_classifier.py -k <prompt_name>`
3. Inspect confusion matrix output
4. If precision < 85% or recall < 80%, propose 2-3 prompt deltas

## Iteration protocol
- Make ONE change at a time
- Bump version (v1 → v2)
- Save the eval report to `docs/prompt-evals/<name>-v<n>.md`
- DO NOT delete old versions — keep for A/B
```

### 7.3 `impact-evaluator`

**Ne yapar:** Impact scoring'i sample feature listesi üzerinde çalıştırır, skor dağılımını gösterir, outlier'ları flag'ler.

### 7.4 `github-actions-deploy`

**Ne yapar:** Yeni workflow yazıyor veya mevcut olanı güncelliyorsan: cron'u UTC'ye çevirir, secret'ları check eder, dry-run yapar.

```markdown
---
name: github-actions-deploy
description: |
  Create or modify GitHub Actions workflows for Sinyra Labs. Handles UTC cron
  conversion, secret validation, and dry-run before commit.
---

# GitHub Actions Deploy Skill

## When to use
- User wants a new scheduled job, ETL, or notification workflow.
- User says "deploy", "schedule", "automate this script".

## Mandatory checks
1. **UTC conversion:** If user says "her gün 18:00", confirm timezone, convert to UTC.
2. **Secrets audit:** List all `${{ secrets.X }}` references; verify each exists via GitHub MCP.
3. **Concurrency:** Long-running jobs MUST have `concurrency:` block.
4. **Timeout:** Every job MUST have `timeout-minutes` (default 20).
5. **Failure notify:** Every prod cron MUST have `if: failure()` notification step.

## Output
- Diff of `.github/workflows/<name>.yml`
- Checklist: ✅ UTC ✅ secrets ✅ concurrency ✅ timeout ✅ alert
- A `workflow_dispatch` test run command for manual verification
```

### 7.5 `brief-renderer`

**Ne yapar:** JSON brief output'unu alır, Jinja2 template'e basar, browser-preview HTML üretir, plain-text fallback'i kontrol eder.

### 7.6 `db-migrator` *(F3'te)*

**Ne yapar:** Alembic migration üretir, hem SQLite hem Postgres'te lokal smoke-test çalıştırır.

### 7.7 Skill Yazım Şablonu

Her skill için minimum:

```markdown
---
name: <kısa-slug>
description: |
  <2-3 cümle: ne yapar, ne zaman tetiklenir>
---

# <İsim>

## When to use
- <konkret tetikleyici 1>
- <konkret tetikleyici 2>

## How to run
<komutlar veya adımlar>

## Output contract
<ne dönmeli>

## Failure modes
<bilinen problemler ve çözümleri>
```

> **Önemli:** Antigravity, `description` alanını kullanıcı sorgusu ile **semantik olarak** karşılaştırıp skill'i otomatik yüklüyor. **Description'ı net yaz** — "RSS feed ekle/test et/doğrula" gibi tetikleyici fiilleri içine koy.

### 7.8 Hazır Skill Repository'leri (browse)

```bash
# Antigravity'ye 100,000+ skill bağlayan /learn komutu
git clone https://github.com/agentskill-sh/ags.git ~/.gemini/antigravity/skills/learn
```

Sonra Antigravity içinde `/learn rss`, `/learn changelog`, `/learn pytest` ile hazır skill'leri yükle.

---

## 8. Hazır Promptlar (kopyala-yapıştır)

> Bu promptlar Antigravity'de Agent Manager'a (Cmd+E) atılır. Hepsi Türkçe yazıldı; agent karışmasın diye kod açıklamalarını İngilizce kalmasını söyleyebilirsin.

### 8.1 P1 — Migrasyon Başlangıcı (Apps Script → Python)

```
Bağlam: Mevcut bir Google Apps Script projem var, AI haberleri RSS'lerden toplayıp
GPT-4o-mini ile sınıflandırıp etki skoru veriyor ve günlük HTML email gönderiyor.
Bu projeyi Python'a taşıyacağım. Scheduler GitHub Actions olacak. Storage başta
SQLite, ileride Supabase. Email Resend.

Mevcut kod elimde (tek dosya, 600 satır .gs).

GÖREV: Repo iskeletini oluştur. Bu doküman dışında dosya YAZMA, sadece şu çıktıyı ver:
1. /sinyra/, /tests/, /.github/workflows/, /.agent/ ağacı (klasörler ve dosya isimleri)
2. pyproject.toml içeriği (uv, ruff, mypy, pytest dahil)
3. requirements.txt (production)
4. .env.example
5. README.md taslağı (sadece bölüm başlıkları)

KISIT:
- Python 3.12+
- pydantic v2
- mypy --strict ile geçecek seviyede type hint
- Henüz kod yazma; sadece iskelet ve TODO comment'lar

Plan: önce tree, sonra her dosya tek tek. Bittiğinde "ready for next prompt" yaz.
```

### 8.2 P2 — Ingestion Layer

```
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
```

### 8.3 P3 — Storage + Dedup

```
GÖREV: sinyra/storage/ ve sinyra/normalize/dedup.py.

Kapsam:
- SQLite, dosya: data/sinyra.db
- Tek tablo (şimdilik): seen_items (hash TEXT PK, title, link, first_seen_at, last_seen_at)
- TTL: 14 gün (mevcut davranışla aynı)
- Alembic migration ile (F3 hazırlığı)
- API: SeenStore.is_seen(hash) -> bool, SeenStore.remember(items) -> int

dedup.py:
- input: List[RawItem]
- hash: md5(title + "|" + link)
- recency filter: HOURS_LOOKBACK config'ten (default 72)
- output: (kept_items, stats_dict)

Test: tests/unit/test_dedup.py — 3 case: seen, fresh, too_old.

KURAL: Tüm zaman damgaları UTC, naive datetime YOK — timezone-aware (datetime.now(UTC)).
```

### 8.4 P4 — Intelligence Layer

```
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
```

### 8.5 P5 — Synthesis + Delivery

```
GÖREV:
- sinyra/synthesis/brief.py: generate_daily_brief(features) -> DailyBrief
  (summary_tr, trends[], insight)
- sinyra/delivery/email/render.py: Jinja2 ile HTML render
- sinyra/delivery/email/send.py: Resend ile gönderim
- templates/brief.html: mevcut Apps Script tasarımını referans al; aynı koyu hero,
  istatistik şeridi, spotlight, şirket grupları, trends, insight, footer.
- templates/brief.txt: plain-text fallback

ÖNEMLİ: Mevcut HTML tasarımını birebir port et — table-based layout (Gmail uyumu),
inline CSS, flexbox YOK, max-width 640px. Mevcut Apps Script kodumdaki escape() ve
impactColor()/impactLabel() helper'larını da Python'a taşı.

Test: render edilmiş HTML'i tests/__snapshots__/ altında tut, snapshot test yaz.

Resend setup: RESEND_API_KEY env. From: "AI Ürün Radarı <radar@<your-domain>>".
```

### 8.6 P6 — GitHub Actions

```
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
```

### 8.7 P7 — Prompt İterasyonu

```
Mevcut classify.v1 promptum yanlış pozitif veriyor (yatırım haberlerini "yeni özellik"
diye işaretliyor, %12 false positive).

GÖREV: prompt-tuner skill'ini kullan.
1. tests/eval/golden_set.jsonl içindeki "investment", "funding", "valuation" etiketli
   örneklerden classifier'ın ürettiği outputları oku.
2. False positive pattern'lerini özetle.
3. classify.v2.md hazırla — mevcut prompt'a "investment_funding_news"
   "leadership_change" "tier_list" "speculation" gibi NEGATIVE rule'lar ekle.
4. v1 vs v2 eval karşılaştırması yap, sonucu docs/prompt-evals/classify-v2.md'ye yaz.
5. v2'yi aktif et.

KURAL: v1'i SİLME — tutuyoruz. config'te active_prompt_version: v2.
```

### 8.8 P8 — Trend Analizi (F3)

```
Bağlam: 30 günlük veri birikti. Şimdi trend extraction skill'i.

GÖREV: sinyra/synthesis/trends.py
- Input: son 30 gün features (DB'den)
- Embedding (text-embedding-3-small) ile cluster
- Her cluster için: en güçlü temsilci feature, üye sayısı, momentum (artış hızı)
- Output: List[Trend]
  (theme_tr, headline_tr, member_count, momentum_score, sample_features)

Cluster sayısı: HDBSCAN (min_cluster_size=3) veya basit cosine-similarity
threshold (>0.78 birleştir).

Çıktıyı brief.py'a entegre et — mevcut "trends" alanını LLM yerine bu pipeline besler.

Önce planını yaz, ben onaylayım.
```

### 8.9 P9 — Public Landing Page (F3)

```
GÖREV: Next.js 15 (app router) + Tailwind ile basit landing.

Sayfalar:
- / : hero ("Cut Through the Noise"), bugünkü brief preview, signup form (Resend
  audience'a ekleme), son 7 günün top-5 feature'ı
- /archive: geçmiş briefler (DB'den okur)
- /trends: 30 günlük trend cluster'ları

Stack:
- Next.js 15 + Tailwind + shadcn/ui
- Supabase client (Server Component)
- Marka rengi: #0b1120 (lacivert), #fbbf24 (sarı vurgu), beyaz arka plan
- Tipografi: Inter

Kısıt:
- Tek dosya component yok; feature klasörleri (features/brief/, features/signup/)
- Next 15 server actions ile signup
- Mobile-first

Önce wireframe ASCII çiz, sonra kod.
```

### 8.10 P10 — SaaS Pivot Plan (F5)

```
Sinyra Labs'ı SaaS'a çevirme planını yap (kod yazma, plan).

Kapsam:
- Auth: Clerk veya Supabase Auth
- Billing: Stripe (free, $15 pro, $49 team)
- Per-user filter: kullanıcı şirket/topic seçer, sadece eşleşen feature'lar
- Per-user delivery channel: email / telegram / webhook
- Multi-tenant DB schema
- Onboarding flow

Çıktı: docs/saas-plan.md
- Schema diff (mevcut → multi-tenant)
- Auth/RBAC kararları
- Billing webhook flow
- 6 haftalık delivery roadmap (haftalık milestone)
- Riskler ve karar noktaları

PLAN, KOD DEĞİL. Bittiğinde 3 risk + 3 hızlı kazanç listele.
```

### 8.11 Sistem Promptu (Antigravity için, .agent/rules.md zaten var ama ek)

Eğer Antigravity Agent Manager'da kalıcı bir "system prompt" tutmak istersen Settings → Custom Instructions'a:

```
You are working on Sinyra Labs, a Python-based AI signal intelligence platform.
Always:
- Read .agent/rules.md before any non-trivial change.
- Surface a 3-step plan before generating > 30 lines of code.
- Use the project's existing patterns (pydantic v2, structlog, jinja2).
- When touching prompts under sinyra/intelligence/prompts/, bump the version
  (v1 → v2) and update tests/eval/.
- Never run pytest or any LLM-call test automatically. Show command, let user run.
- Speak Turkish to the user, but keep code, comments, log messages, and Git
  commit messages in English.
```

---

## 9. İlk 7 Günlük Aksiyon Planı

| Gün | Görev | Çıktı |
|---|---|---|
| **D1** | Antigravity kur, MCP'leri yükle (4 tane), `.agent/rules.md` yaz | Workspace hazır |
| **D2** | P1 promptu çalıştır → repo iskeleti, P2 → ingestion | İlk çalışan `python -m sinyra.ingest` |
| **D3** | P3 → storage/dedup, P4 → classifier (sadece prompt port) | LLM çağrısı çalışıyor |
| **D4** | P4 devam → impact scorer + golden set | İlk eval raporu |
| **D5** | P5 → synthesis + email render | Local'de email preview |
| **D6** | P6 → GitHub Actions, secret'lar, ilk gerçek run | İlk otomatik mail |
| **D7** | Custom skills yaz (rss-validator, prompt-tuner, gha-deploy) | Workspace skill seti hazır |

> 7. günde Faz 1 (MVP'nin Python versiyonu) çalışır halde olur. F2 tamamlanmıştır.

---

## 10. Riskler ve Karar Noktaları

| Risk | Etki | Mitigasyon |
|---|---|---|
| OpenAI API maliyeti F3'te şişer | Aylık $100+ olabilir | Day 1'den `total_tokens` log; threshold alert; ayda bir model A/B (Haiku 4.5, Gemini 3 Flash) |
| GitHub Actions cron gecikmesi | Mail saat 18'de değil 18:30'da gider | Dokümantasyona "±30 dk" yaz, kullanıcıyı bilgilendir |
| RSS kaynakları kapanır | Pipeline boş döner | feeds.yaml health check ayda bir; Firecrawl fallback |
| Prompt drift (model güncellenince çıktı değişir) | Sınıflandırma kalitesi düşer | `model` parametresini PIN'le; haftalık golden set eval |
| Antigravity rate limit | Geliştirme yavaşlar | Kritik refactor'larda Claude Code'a fallback; basit refactor'lar Gemini Flash |
| Veri kaybı (cache silinirse) | Aynı haber tekrar gelir | F3'te Supabase'e geçince problem çözülür |
| Marka çakışması | "Sinyra" başka şirket olabilir | Hemen .com + .io domain'i + EUIPO/TPE marka taraması |

### 10.1 Karar Noktaları (önümüzdeki 30 gün)

- [ ] **Domain & marka tescili** — sinyra.io / sinyralabs.com
- [ ] **Tek dil mi, çift dil mi?** — Şu an TR. EN versiyonu F3'te mi yoksa baştan mı?
- [ ] **Closed beta veya açık launch?** — Kalite oturmadan public yapma; ilk 50 kullanıcı davetli.
- [ ] **Kendi domain'inden mail (radar@sinyra.io) vs Resend default**
- [ ] **Apps Script versiyonunu ne zaman emekliye ayır?** — Python paralel 14 gün stabil çalışınca.

---

## 11. Sonraki Adımlar (bu doküman bittikten sonra)

1. **Bu MD'yi repo'ya at:** `docs/01-positioning-and-antigravity-setup.md`
2. **`.agent/rules.md`'i kopyala**, projene özel kısımları daralt.
3. **MCP'leri kur** — section 6.4 sırasıyla.
4. **P1 promptunu** Antigravity Agent Manager'a at; iskelet çıkar.
5. **README.md'yi yaz**: tek paragraf konumlandırma + getting started.
6. **Marka taraması** + domain al.
7. **CHANGELOG.md başlat** — F2 sürecini buradan takip et.

---

## Ek A — Hızlı Referans

### MCP Komutları
- Yeni MCP ekle: Agent panel → "..." → MCP Servers → MCP Store
- Custom MCP: Manage MCP Servers → View raw config → `mcp_config.json` düzenle
- Skill eklemek: `.agent/skills/<name>/SKILL.md`
- Skill keşfet: `/learn <topic>` (ags kurulu ise)

### GitHub Actions Cron Cheatsheet (TR saat → UTC)
| TR Saati | UTC Saati | Cron |
|---|---|---|
| 06:00 | 03:00 | `0 3 * * *` |
| 12:00 | 09:00 | `0 9 * * *` |
| 18:00 | 15:00 | `0 15 * * *` |
| 21:00 | 18:00 | `0 18 * * *` |

> ±15 dakika gecikme normaldir. Hassas saatlerde 15 dk önceye al.

### Sinyra Komut Aliasları (öneri, .zshrc/.bashrc)
```bash
alias sinyra-run='python -m sinyra.run --dry-run'
alias sinyra-test='pytest -xvs'
alias sinyra-eval='pytest tests/eval/ -v'
alias sinyra-deploy='gh workflow run daily-pipeline.yml'
```

---

**Doküman sonu.** Sorular, geri bildirim, ek bölüm istekleri için: `bilalabic78@gmail.com`.
