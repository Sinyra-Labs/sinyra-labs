/\*\*

- ============================================================
- AI FEATURE INTELLIGENCE SYSTEM (v3.0 — Türkçe)
- ***
- v2.1'den değişenler:
- - Tüm AI çıktıları TÜRKÇE (özet, trendler, insight, skor sebebi)
- - Mail tasarımı baştan yazıldı:
-       · Table-based layout (Gmail/Outlook uyumlu, flexbox yok)
-       · Açık ve koyu renk hiyerarşisi, okunaklı tipografi
-       · İstatistik şeridi (toplam feature / şirket / ortalama etki)
-       · Impact rozetleri renk kodlu (kırmızı/turuncu/sarı/gri)
-       · "En önemli gelişme" spotlight kartı
-       · Şirket bazlı gruplama, temiz kartlar, hover-friendly linkler
-       · Plain-text fallback (mail client'ın HTML göstermediği durum)
- Gerekli ScriptProperty: OPENAI_KEY
- ============================================================
  \*/

/_ =========================================================
CONFIG
========================================================= _/
const CONFIG = {
MODEL_CLASSIFY: "gpt-4o-mini",
MODEL_REPORT: "gpt-4o-mini",
// Eski EMAIL_TO array'i yerine:
MAIL_LIST_SHEET_ID: "164XhD-ff7OcGIAVjjW8J-AlBFuo81b9UpYeJP8pqMLc",
MAIL_LIST_SHEET_NAME: "Form Yanıtları 1", // sekme adı (Türkçe Sheets'te genelde "Sayfa1"),

EMAIL_SUBJECT: "🧠 Günlük AI Ürün Radarı",
PER_FEED_LIMIT: 15,
MAX_CLASSIFY: 100,
CONFIDENCE_MIN: 60,
IMPACT_MIN: 40,
HOURS_LOOKBACK: 72,
KEEP_IF_NO_DATE: true,
CACHE_KEY: "AI_FI_SEEN_HASHES",
CACHE_TTL_DAYS: 14,

RSS_FEEDS: [
{ name: "OpenAI News", url: "https://openai.com/news/rss.xml", company: "OpenAI" },
{ name: "Google AI Blog", url: "https://blog.google/technology/ai/rss/", company: "Google" },
{ name: "Google DeepMind", url: "https://deepmind.google/blog/rss.xml", company: "Google" },
{ name: "Google Research", url: "https://research.google/blog/rss/", company: "Google" },
{ name: "Anthropic News", url: "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml", company: "Anthropic" },
{ name: "Anthropic Engineering", url: "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml", company: "Anthropic" },
{ name: "Microsoft AI Blog", url: "https://blogs.microsoft.com/ai/feed/", company: "Microsoft" },
{ name: "Microsoft Research", url: "https://www.microsoft.com/en-us/research/feed/", company: "Microsoft" },
{ name: "AWS ML Blog", url: "https://aws.amazon.com/blogs/machine-learning/feed/", company: "AWS" },
{ name: "TechCrunch AI", url: "https://techcrunch.com/category/artificial-intelligence/feed/", company: null },
{ name: "The Verge AI", url: "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", company: null },
{ name: "Ars Technica AI", url: "https://arstechnica.com/ai/feed/", company: null },
{ name: "VentureBeat AI", url: "https://venturebeat.com/category/ai/feed/", company: null },
{ name: "MIT Tech Review", url: "https://www.technologyreview.com/feed/", company: null }
],

GOOGLE_NEWS_QUERIES: [
{ q: "Meta AI release OR Llama", company: "Meta" },
{ q: "xAI Grok update", company: "xAI" },
{ q: "Mistral AI release", company: "Mistral" },
{ q: "Anthropic Claude update", company: "Anthropic" },
{ q: "OpenAI GPT release", company: "OpenAI" },
{ q: "Google Gemini feature", company: "Google" },
{ q: "Microsoft Copilot update", company: "Microsoft" }
]
};

/_ ---- Şirket başına emoji (görsel ayrım için) ---- _/
const COMPANY_EMOJI = {
"OpenAI": "🟢", "Google": "🔵", "Anthropic": "🟣",
"Microsoft": "🟦", "Meta": "🔷", "xAI": "⚫",
"Mistral": "🟠", "AWS": "🟧", "Apple": "⚪",
"NVIDIA": "🟩", "Perplexity": "🔹"
};
function checkMailQuota() {
Logger.log("Kalan günlük mail kotası: " + MailApp.getRemainingDailyQuota());
}
/_ ---- Etki seviyesi etiketleri ---- _/
function impactLabel(s) {
if (s >= 90) return "Kritik";
if (s >= 75) return "Yüksek";
if (s >= 60) return "Orta-Yüksek";
if (s >= 40) return "Orta";
return "Düşük";
}
function impactColor(s) {
if (s >= 90) return "#b91c1c";
if (s >= 75) return "#c2410c";
if (s >= 60) return "#a16207";
return "#475569";
}
function impactBg(s) {
if (s >= 90) return "#fef2f2";
if (s >= 75) return "#fff7ed";
if (s >= 60) return "#fefce8";
return "#f1f5f9";
}

/_ =========================================================
MAIN
========================================================= _/
function runDailyIntelligence() {
try {
Logger.log("=== AI Ürün Radarı v3.0 — BAŞLADI ===");

    const raw = fetchNews();
    Logger.log("Adım 1 (fetchNews): " + raw.length);

    const deduped = dedupeAndFreshness(raw);
    Logger.log("Adım 2 (dedupe+recency): " + deduped.length);

    const classified = classifyBatch(deduped);
    Logger.log("Adım 3 (sınıflandırma): " + classified.length);
    logClassificationBreakdown(classified);

    const features = filterFeatures(classified);
    Logger.log("Adım 4 (filter): " + features.length);

    const scored = analyzeImpact(features);
    Logger.log("Adım 5 (impact): " + scored.length);

    const report = generateReport(scored);
    sendEmail(report, scored);
    rememberSeen(deduped);
    Logger.log("=== TAMAMLANDI ===");

} catch (e) {
Logger.log("HATA: " + e.stack);
MailApp.sendEmail({
to: CONFIG.EMAIL_TO,
subject: "⚠️ AI Ürün Radarı — Sistem Hatası",
body: "Hata:\n\n" + e.stack
});
}
}

function logClassificationBreakdown(items) {
let isFeature = 0, confOk = 0, rejLow = 0, rejNot = 0, rejMiss = 0;
items.forEach(it => {
const c = it.classification;
if (!c) { rejMiss++; return; }
if (!c.isFeature) { rejNot++; return; }
isFeature++;
if ((c.confidence || 0) < CONFIG.CONFIDENCE_MIN) rejLow++; else confOk++;
});
Logger.log(" └ feature=true: " + isFeature +
" | conf geçen: " + confOk +
" | red (feature değil): " + rejNot +
" | red (düşük conf): " + rejLow +
" | red (JSON yok): " + rejMiss);
}

/\* =========================================================

1.  FETCH
    ========================================================= \*/
    function fetchNews() {
    const out = [];
    CONFIG.RSS_FEEDS.forEach(feed => {
    const items = safeParseRss(feed.url, CONFIG.PER_FEED_LIMIT);
    Logger.log(" [" + feed.name + "] -> " + items.length);
    items.forEach(it => out.push({
    title: it.title, link: it.link, summary: it.summary,
    pubDate: it.pubDate, source: feed.name, hintCompany: feed.company || null
    }));
    });
    CONFIG.GOOGLE_NEWS_QUERIES.forEach(q => {
    const url = "https://news.google.com/rss/search?q=" +
    encodeURIComponent(q.q) + "&hl=tr-TR&gl=TR&ceid=TR:tr";
    const items = safeParseRss(url, CONFIG.PER_FEED_LIMIT);
    Logger.log(" [GNews: " + q.q + "] -> " + items.length);
    items.forEach(it => out.push({
    title: it.title, link: it.link, summary: it.summary,
    pubDate: it.pubDate, source: "Google News: " + q.q, hintCompany: q.company
    }));
    });
    return out;
    }

function safeParseRss(url, limit) {
const results = [];
try {
const resp = UrlFetchApp.fetch(url, {
muteHttpExceptions: true, followRedirects: true,
headers: { "User-Agent": "Mozilla/5.0 (compatible; AI-Feature-Intel/3.0)" }
});
if (resp.getResponseCode() !== 200) {
Logger.log(" RSS HTTP " + resp.getResponseCode() + " :: " + url);
return results;
}
const xml = resp.getContentText();
const doc = XmlService.parse(xml);
const root = doc.getRootElement();

    const channel = root.getChild("channel");
    if (channel) {
      channel.getChildren("item").slice(0, limit).forEach(it => {
        results.push({
          title:   (it.getChildText("title") || "").trim(),
          link:    (it.getChildText("link")  || "").trim(),
          summary: stripHtml(it.getChildText("description") || ""),
          pubDate: parseDate(it.getChildText("pubDate"))
        });
      });
      return results;
    }
    const atomNs = XmlService.getNamespace("http://www.w3.org/2005/Atom");
    root.getChildren("entry", atomNs).slice(0, limit).forEach(e => {
      const linkEl = e.getChild("link", atomNs);
      const link   = linkEl ? linkEl.getAttribute("href").getValue() : "";
      const summary = stripHtml(
        (e.getChildText("summary", atomNs) || e.getChildText("content", atomNs) || "")
      );
      results.push({
        title:   (e.getChildText("title", atomNs) || "").trim(),
        link:    link,
        summary: summary,
        pubDate: parseDate(e.getChildText("updated", atomNs) ||
                           e.getChildText("published", atomNs))
      });
    });

} catch (e) {
Logger.log(" RSS hata [" + url + "]: " + e);
}
return results;
}

function stripHtml(s) {
if (!s) return "";
return s.replace(/<[^>]+>/g, " ")
.replace(/&nbsp;/g, " ").replace(/&amp;/g, "&")
.replace(/&quot;/g, '"').replace(/&#39;/g, "'")
.replace(/\s+/g, " ").trim().slice(0, 600);
}
function parseDate(s) {
if (!s) return null;
const d = new Date(s);
return isNaN(d.getTime()) ? null : d;
}

/_ ========================================================= 2) DEDUPE + RECENCY
========================================================= _/
function dedupeAndFreshness(items) {
const seenStore = loadSeenHashes();
const cutoff = new Date(Date.now() - CONFIG.HOURS_LOOKBACK _ 3600 _ 1000);
const keptHash = {};
const kept = [];
let rejOld = 0, rejSeen = 0, rejNoTitle = 0;

items.forEach(it => {
if (!it.title) { rejNoTitle++; return; }
if (it.pubDate && it.pubDate < cutoff) { rejOld++; return; }
if (!it.pubDate && !CONFIG.KEEP_IF_NO_DATE) { rejOld++; return; }

    const h = hash(it.title + "|" + (it.link || ""));
    if (seenStore[h] || keptHash[h]) { rejSeen++; return; }
    keptHash[h] = true;
    it._hash = h;
    kept.push(it);

});

Logger.log(" └ eski: " + rejOld + " | görüldü: " + rejSeen + " | başlıksız: " + rejNoTitle);
return kept;
}

function hash(s) {
const bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, s);
return bytes.map(b => ("0" + (b & 0xFF).toString(16)).slice(-2)).join("");
}
function loadSeenHashes() {
const raw = PropertiesService.getScriptProperties().getProperty(CONFIG.CACHE_KEY);
if (!raw) return {};
try {
const obj = JSON.parse(raw);
const cutoff = Date.now() - CONFIG.CACHE_TTL_DAYS _ 86400 _ 1000;
const fresh = {};
Object.keys(obj).forEach(k => { if (obj[k] > cutoff) fresh[k] = obj[k]; });
return fresh;
} catch(e) { return {}; }
}
function rememberSeen(items) {
const store = loadSeenHashes();
const now = Date.now();
items.forEach(it => { if (it.\_hash) store[it._hash] = now; });
PropertiesService.getScriptProperties()
.setProperty(CONFIG.CACHE_KEY, JSON.stringify(store));
}

/_ ========================================================= 3) CLASSIFY — prompt TR
========================================================= _/
function classifyBatch(items) {
const slice = items.slice(0, CONFIG.MAX_CLASSIFY);
Logger.log(" sınıflandırılıyor: " + slice.length + "/" + items.length);
const out = [];
slice.forEach((n, idx) => {
try {
const data = classifyFeatureWithAI(n);
if (data) { n.classification = data; out.push(n); }
if (idx % 10 === 9) Utilities.sleep(300);
} catch (e) {
Logger.log(" classify err: " + e);
}
});
return out;
}

function classifyFeatureWithAI(item) {
const systemPrompt = [
"Sen kıdemli bir teknoloji ürün analistisin.",
"Girdi olarak bir haber başlığı ve özet veriliyor.",
"Görev: Bu haber, büyük bir AI/teknoloji şirketinden GERÇEK bir ürün/model/özellik lansmanı",
"ya da güncellemesi hakkında mı? Kaynak şirketin kendi blogu olabileceği gibi",
"güvenilir teknoloji basını (TechCrunch, Verge, Ars, VentureBeat vs.) da olabilir.",
"",
"SADECE şu JSON'u döndür (markdown kullanma):",
'{"isFeature": true|false, "company": "", "feature": "", "type": "new_feature|update|announcement|research|none", "confidence": 0-100,',
' "feature_tr": "", "summary_tr": ""}',
"",
"- feature_tr: Özelliğin kısa Türkçe adı (örn: 'Gemini Canlı Görüntü Özelliği').",
"- summary_tr: 1-2 cümlelik, akıcı Türkçe özet (haberin esasını anlatsın).",
"",
"TRUE olarak işaretle:",
"- Yeni model/ürün lansmanları (örn. 'Gemini 3.1', 'GPT-5', 'Claude Opus 4.7')",
"- Mevcut üründe yeni veya güncellenmiş özellik (örn. 'ChatGPT'ye hafıza eklendi')",
"- Genel kullanıma açılma (GA), public preview, beta lansmanları",
"- Güvenilir basının raporladığı anlamlı yeni yetenekler",
"- Yeni yetenek getiren resmi ortaklık/entegrasyonlar",
"",
"FALSE olarak işaretle:",
"- Salt yorum, analiz, spekülasyon, söylenti",
"- Yatırım turu, işe alım, değerleme, yönetici transferi",
"- Politika tartışmaları, davalar (ürün boyutu yoksa)",
"- 'En iyi 10 araç' listeleri, rehberler",
"",
"Tercih edilen şirketler: OpenAI, Google, DeepMind, Anthropic, Microsoft, Meta,",
"xAI, Mistral, Amazon/AWS, Apple, NVIDIA, Cohere, Stability, Perplexity."
].join("\n");

const userMsg = [
"BAŞLIK: " + (item.title || ""),
"KAYNAK: " + (item.source || ""),
"IPUCU_ŞİRKET: " + (item.hintCompany || "bilinmiyor"),
"ÖZET: " + (item.summary || "").slice(0, 500)
].join("\n");

const raw = callOpenAI(CONFIG.MODEL_CLASSIFY, [
{ role: "system", content: systemPrompt },
{ role: "user", content: userMsg }
], 0);
return safeJson(raw);
}

/_ ========================================================= 4) FILTER
========================================================= _/
function filterFeatures(items) {
const kept = [];
const seenKey = {};
items.forEach(it => {
const c = it.classification;
if (!c || !c.isFeature) return;
if ((c.confidence || 0) < CONFIG.CONFIDENCE_MIN) return;
if (!c.company || !c.feature) return;
const k = (c.company + "|" + c.feature).toLowerCase();
if (seenKey[k]) return;
seenKey[k] = true;
kept.push(it);
});
return kept;
}

/_ ========================================================= 5) IMPACT — TR
========================================================= _/
function analyzeImpact(items) {
items.forEach((n, idx) => {
try {
n.impact = scoreOne(n);
if (idx % 10 === 9) Utilities.sleep(300);
} catch(e) { n.impact = { score: 50, reason: "Skorlama başarısız" }; }
});
const strong = items.filter(x => (x.impact.score || 0) >= CONFIG.IMPACT_MIN);
strong.sort((a, b) => (b.impact.score || 0) - (a.impact.score || 0));
return strong;
}

function scoreOne(item) {
const systemPrompt = [
"Sen AI sektörü stratejistisin. Aşağıdaki özelliğin etkisini 0-100 arası puanla.",
"- 90+ sektörü değiştirir (yeni model ailesi, paradigma kırılması)",
"- 75+ büyük ürün etkisi (flagship GA, yeni büyük yetenek)",
"- 50+ anlamlı güncelleme",
"- <50 küçük iyileştirme / UI",
"",
'SADECE JSON: {"score": 0-100, "reason": "Tek cümle Türkçe gerekçe"}'
].join("\n");

const c = item.classification || {};
const userMsg = [
"ŞİRKET: " + (c.company || "?"),
"ÖZELLİK: " + (c.feature || c.feature_tr || "?"),
"TİP: " + (c.type || "?"),
"BAŞLIK: " + item.title,
"ÖZET: " + (c.summary_tr || (item.summary || "")).slice(0, 500)
].join("\n");

const raw = callOpenAI(CONFIG.MODEL_REPORT, [
{ role: "system", content: systemPrompt },
{ role: "user", content: userMsg }
], 0.1);
const j = safeJson(raw);
if (!j) return { score: 50, reason: "Analiz edilemedi" };
j.score = Math.max(0, Math.min(100, j.score || 0));
return j;
}

/_ ========================================================= 6) REPORT — TR
========================================================= _/
function generateReport(features) {
if (!features.length) {
return {
summary: "Son " + CONFIG.HOURS_LOOKBACK + " saatte kayda değer bir AI ürün/özellik lansmanı tespit edilmedi.",
trends: [],
insight: "Sakin bir gün. Kendi roadmap'inize odaklanmak için iyi bir fırsat."
};
}

const bullets = features.map((f, i) => {
const c = f.classification;
return (i + 1) + ") [" + c.company + "] " + (c.feature_tr || c.feature) +
" | etki=" + f.impact.score + " | tip=" + c.type +
" | neden=" + (f.impact.reason || "");
}).join("\n");

const systemPrompt = [
"Sen kıdemli bir AI/teknoloji sektörü analistisin ve günlük yönetici brifingi yazıyorsun.",
"Girdi: filtrelenmiş ve skorlanmış gerçek AI ürün lansmanları listesi.",
"",
"SADECE şu JSON'u döndür:",
'{"summary": "2-3 cümle yönetici özeti Türkçe",',
' "trends": ["trend cümlesi 1", "trend cümlesi 2", "trend cümlesi 3"],',
' "insight": "1 cümle stratejik içgörü Türkçe"}',
"",
"Stil: kısa, net, abartısız, profesyonel Türkçe. Klişe kaçın."
].join("\n");

const raw = callOpenAI(CONFIG.MODEL_REPORT, [
{ role: "system", content: systemPrompt },
{ role: "user", content: bullets }
], 0.3);
return safeJson(raw) || {
summary: "Günün AI ürün radarı.",
trends: [],
insight: ""
};
}

/_ ========================================================= 7) EMAIL — YENİDEN TASARLANDI (table-based, Gmail uyumlu)
========================================================= _/
function sendEmail(report, features) {
const dateStr = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "d MMMM yyyy");
const timeStr = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "HH:mm");
const dayName = getDayNameTR(new Date().getDay());

// stats
const totalF = features.length;
const companies = {};
features.forEach(f => companies[f.classification.company] = true);
const uniqueCompanies = Object.keys(companies).length;
const avgImpact = totalF ? Math.round(features.reduce((a, f) => a + f.impact.score, 0) / totalF) : 0;
const topItem = features[0] || null;

// group by company
const byCompany = {};
features.forEach(f => {
const co = f.classification.company;
(byCompany[co] = byCompany[co] || []).push(f);
});
// order companies by their max impact descending
const companyOrder = Object.keys(byCompany).sort((a, b) => {
const am = Math.max.apply(null, byCompany[a].map(x => x.impact.score));
const bm = Math.max.apply(null, byCompany[b].map(x => x.impact.score));
return bm - am;
});

const html = buildHtmlEmail({
dateStr: dateStr, timeStr: timeStr, dayName: dayName,
report: report, features: features,
totalF: totalF, uniqueCompanies: uniqueCompanies,
avgImpact: avgImpact, topItem: topItem,
byCompany: byCompany, companyOrder: companyOrder
});

const plainText = buildPlainText({
dateStr: dateStr, report: report, features: features,
byCompany: byCompany, companyOrder: companyOrder
});

const recipients = getMailListFromSheet();
if (!recipients.length) {
Logger.log("⚠️ Aktif alıcı yok, mail gönderimi atlandı.");
return;
}

recipients.forEach(to => {
try {
MailApp.sendEmail({
to: to,
subject: CONFIG.EMAIL_SUBJECT + " — " + dateStr,
body: plainText,
htmlBody: html,
name: "AI Ürün Radarı"
});
Logger.log("✅ Gönderildi: " + to);
} catch (e) {
Logger.log("❌ Başarısız [" + to + "]: " + e);
}
});
}

/_ ---- HTML builder ---- _/
function buildHtmlEmail(d) {
const fmtDate = d.dayName + ", " + d.dateStr;

// HERO
const hero =
'<tr><td style="padding:0;">' +
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" ' +
'style="background:#0b1120;border-radius:14px 14px 0 0;">' +
'<tr><td style="padding:28px 28px 22px 28px;">' +
'<div style="font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;">' +
'<div style="color:#94a3b8;font-size:11px;letter-spacing:2px;font-weight:600;">AI ÜRÜN RADARI</div>' +
'<div style="color:#ffffff;font-size:26px;font-weight:700;margin-top:6px;line-height:1.25;">' +
'🧠 Günlük Brifing' +
'</div>' +
'<div style="color:#cbd5e1;font-size:13px;margin-top:4px;">' +
escape(fmtDate) + ' · ' + escape(d.timeStr) +
'</div>' +
'<div style="color:#e2e8f0;font-size:14px;line-height:1.6;margin-top:16px;' +
                         'border-top:1px solid rgba(255,255,255,0.1);padding-top:14px;">' +
escape(d.report.summary || "") +
'</div>' +
'</div>' +
'</td></tr>' +
'</table>' +
'</td></tr>';

// STATS STRIP
const stats =
'<tr><td style="padding:0;">' +
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" ' +
'style="background:#1e293b;border-radius:0;">' +
'<tr>' +
statBox(d.totalF, "Ürün / Özellik") +
statBox(d.uniqueCompanies, "Şirket") +
statBox(d.avgImpact || "–", "Ort. Etki") +
'</tr>' +
'</table>' +
'</td></tr>';

// SPOTLIGHT (top item)
let spotlight = "";
if (d.topItem) {
const c = d.topItem.classification;
const color = impactColor(d.topItem.impact.score);
spotlight =
'<tr><td style="padding:20px 20px 0 20px;">' +
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" ' +
'style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;">' +
'<tr><td style="background:' + color + ';padding:10px 16px;">' +
'<div style="font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;' +
                         'color:#ffffff;font-size:11px;font-weight:700;letter-spacing:1.5px;">' +
'⭐ GÜNÜN ÖNE ÇIKAN GELİŞMESİ' +
'</div>' +
'</td></tr>' +
'<tr><td style="padding:18px 20px;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;">' +
'<div style="color:#64748b;font-size:12px;font-weight:600;">' +
(COMPANY_EMOJI[c.company] || "🏢") + '&nbsp;&nbsp;' + escape(c.company.toUpperCase()) +
'</div>' +
'<div style="color:#0f172a;font-size:19px;font-weight:700;margin-top:4px;line-height:1.3;">' +
escape(c.feature_tr || c.feature) +
'</div>' +
'<div style="color:#334155;font-size:14px;line-height:1.6;margin-top:10px;">' +
escape(c.summary_tr || d.topItem.impact.reason || "") +
'</div>' +
'<div style="margin-top:14px;">' +
'<span style="display:inline-block;background:' + impactBg(d.topItem.impact.score) + ';' +
                          'color:' + color + ';font-size:12px;font-weight:700;' +
                          'padding:4px 10px;border-radius:20px;border:1px solid ' + color + '33;">' +
'Etki: ' + d.topItem.impact.score + '/100 · ' + impactLabel(d.topItem.impact.score) +
'</span>' +
'&nbsp;&nbsp;' +
'<a href="' + escape(d.topItem.link) + '" ' +
'style="display:inline-block;font-size:12px;color:#2563eb;' +
'text-decoration:none;font-weight:600;">Kaynağa git →</a>' +
'</div>' +
'</td></tr>' +
'</table>' +
'</td></tr>';
}

// COMPANY SECTIONS
let companySections = "";
d.companyOrder.forEach(co => {
const emoji = COMPANY_EMOJI[co] || "🏢";
const items = d.byCompany[co];
let cards = "";
items.forEach(f => {
cards += featureCard(f);
});
companySections +=
'<tr><td style="padding:22px 20px 0 20px;">' +
'<div style="font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;' +
                     'font-size:13px;font-weight:700;color:#475569;letter-spacing:0.5px;' +
                     'text-transform:uppercase;border-bottom:2px solid #e2e8f0;padding-bottom:6px;margin-bottom:10px;">' +
emoji + '&nbsp;&nbsp;' + escape(co) + ' <span style="color:#94a3b8;font-weight:500;">(' + items.length + ')</span>' +
'</div>' +
cards +
'</td></tr>';
});

// TRENDS
let trendsSection = "";
if ((d.report.trends || []).length) {
let trendItems = "";
d.report.trends.forEach(t => {
trendItems +=
'<tr><td style="padding:8px 0;vertical-align:top;width:24px;">' +
'<div style="width:6px;height:6px;background:#2563eb;border-radius:50%;margin-top:8px;"></div>' +
'</td><td style="padding:8px 0;color:#334155;font-size:14px;line-height:1.55;">' +
escape(t) +
'</td></tr>';
});
trendsSection =
'<tr><td style="padding:22px 20px 0 20px;">' +
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" ' +
'style="background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;">' +
'<tr><td style="padding:18px 20px;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;">' +
'<div style="font-size:11px;font-weight:700;color:#2563eb;letter-spacing:1.5px;margin-bottom:8px;">' +
'📈 TRENDLER' +
'</div>' +
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">' +
trendItems +
'</table>' +
'</td></tr>' +
'</table>' +
'</td></tr>';
}

// INSIGHT
let insightSection = "";
if (d.report.insight) {
insightSection =
'<tr><td style="padding:16px 20px 0 20px;">' +
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" ' +
'style="background:#1e293b;border-radius:12px;">' +
'<tr><td style="padding:18px 20px;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;">' +
'<div style="font-size:11px;font-weight:700;color:#fbbf24;letter-spacing:1.5px;margin-bottom:6px;">' +
'🧠 STRATEJİK İÇGÖRÜ' +
'</div>' +
'<div style="color:#f1f5f9;font-size:14px;line-height:1.6;">' +
escape(d.report.insight) +
'</div>' +
'</td></tr>' +
'</table>' +
'</td></tr>';
}

// EMPTY STATE
let emptyState = "";
if (!d.features.length) {
emptyState =
'<tr><td style="padding:22px 20px 0 20px;">' +
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" ' +
'style="background:#ffffff;border:1px dashed #cbd5e1;border-radius:12px;">' +
'<tr><td style="padding:28px 20px;text-align:center;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;">' +
'<div style="font-size:36px;margin-bottom:8px;">🌤️</div>' +
'<div style="color:#475569;font-size:14px;font-weight:600;">Bugün sakin bir gün</div>' +
'<div style="color:#94a3b8;font-size:12px;margin-top:4px;">' +
'Son ' + CONFIG.HOURS_LOOKBACK + ' saatte eşiği geçen kayda değer bir lansman yok.' +
'</div>' +
'</td></tr>' +
'</table>' +
'</td></tr>';
}

// FOOTER
const footer =
// PAYLAŞIM KARTI — koyu arkaplan, sarı vurgu (insight kartına paralel)
'<tr><td style="padding:22px 20px 0 20px;">' +
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" ' +
'style="background:#0b1120;border-radius:12px;overflow:hidden;">' +
'<tr><td style="background:#fbbf24;padding:8px 16px;">' +
'<div style="font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;' +
                       'color:#0b1120;font-size:11px;font-weight:700;letter-spacing:1.5px;">' +
'📢 PAYLAŞ · BÜYÜT' +
'</div>' +
'</td></tr>' +
'<tr><td style="padding:20px 22px;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;">' +
'<div style="color:#ffffff;font-size:16px;font-weight:700;line-height:1.35;margin-bottom:6px;">' +
'Bu brifingi faydalı buldun mu?' +
'</div>' +
'<div style="color:#cbd5e1;font-size:13px;line-height:1.6;margin-bottom:14px;">' +
'Arkadaşlarına öner — tek bir formla listeye katılabilirler. ' +
'AI\'daki son durumu kaçırmasınlar.' +
'</div>' +
'<a href="https://forms.gle/mWKvXgTJbZNVwHKk9" ' +
'style="display:inline-block;background:#fbbf24;color:#0b1120;' +
'font-size:13px;font-weight:700;text-decoration:none;' +
'padding:10px 20px;border-radius:6px;letter-spacing:0.3px;">' +
'Başvuru formunu aç →' +
'</a>' +
'</td></tr>' +
'</table>' +
'</td></tr>' +

    // İLETİŞİM KARTI — beyaz kart (feature card diline paralel)
    '<tr><td style="padding:12px 20px 0 20px;">' +
      '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" ' +
             'style="background:#ffffff;border:1px solid #e2e8f0;border-left:3px solid #2563eb;' +
                    'border-radius:8px;">' +
        '<tr><td style="padding:14px 16px;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;">' +
          '<div style="color:#64748b;font-size:11px;font-weight:700;letter-spacing:1.2px;margin-bottom:4px;">' +
            '✉️ İLETİŞİM & GERİ BİLDİRİM' +
          '</div>' +
          '<div style="color:#334155;font-size:13px;line-height:1.55;">' +
            'Bu maili almak istemiyorsanız ya da geri bildirim vermek isterseniz, ' +
            '<a href="mailto:bilalabic78@gmail.com?subject=AI%20Ürün%20Radarı%20-%20İletişim" ' +
               'style="color:#2563eb;text-decoration:none;font-weight:600;">' +
              'bilalabic78@gmail.com' +
            '</a> adresinden Bilal\'e ulaşabilirsiniz.' +
          '</div>' +
        '</td></tr>' +
      '</table>' +
    '</td></tr>' +

    // ALT META ŞERİT
    '<tr><td style="padding:18px 20px 24px 20px;text-align:center;' +
                   'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;">' +
      '<div style="color:#94a3b8;font-size:11px;line-height:1.6;">' +
        '<span style="color:#64748b;font-weight:600;">AI ÜRÜN RADARI</span> · ' +
        CONFIG.RSS_FEEDS.length + ' RSS + ' + CONFIG.GOOGLE_NEWS_QUERIES.length + ' arama sorgusu tarandı<br>' +
        '<span style="color:#cbd5e1;">·</span> ' +
        'Google Apps Script ile otomatik üretildi ' +
        '<span style="color:#cbd5e1;">·</span>' +
      '</div>' +
    '</td></tr>';

// ASSEMBLE
return (
'<div style="background:#f1f5f9;padding:20px 10px;margin:0;">' +
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" ' +
'style="max-width:640px;margin:0 auto;background:#f1f5f9;">' +
hero +
stats +
spotlight +
emptyState +
(d.features.length > 1 ? companySections : "") +
trendsSection +
insightSection +
footer +
'</table>' +
'</div>'
);
}

function statBox(value, label) {
return (
'<td width="33.33%" style="padding:14px 10px;text-align:center;border-right:1px solid rgba(255,255,255,0.08);' +
                              'font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;">' +
'<div style="color:#ffffff;font-size:24px;font-weight:700;line-height:1;">' + escape(String(value)) + '</div>' +
'<div style="color:#94a3b8;font-size:10px;letter-spacing:1.5px;font-weight:600;' +
                   'text-transform:uppercase;margin-top:4px;">' + escape(label) + '</div>' +
'</td>'
);
}

function featureCard(f) {
const c = f.classification;
const color = impactColor(f.impact.score);
const bg = impactBg(f.impact.score);
const typeTr = translateType(c.type);

return (
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" ' +
'style="background:#ffffff;border:1px solid #e2e8f0;border-left:3px solid ' + color + ';' +
'border-radius:8px;margin-bottom:10px;">' +
'<tr><td style="padding:14px 16px;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;">' +
'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">' +
'<tr>' +
'<td style="vertical-align:top;padding-right:12px;">' +
'<div style="color:#0f172a;font-size:15px;font-weight:600;line-height:1.35;">' +
escape(c.feature_tr || c.feature) +
'</div>' +
'</td>' +
'<td align="right" style="vertical-align:top;white-space:nowrap;">' +
'<div style="display:inline-block;background:' + bg + ';color:' + color + ';' +
                          'font-size:11px;font-weight:700;padding:3px 9px;border-radius:20px;' +
                          'border:1px solid ' + color + '33;">' +
f.impact.score + ' / 100' +
'</div>' +
'</td>' +
'</tr>' +
'<tr><td colspan="2" style="padding-top:8px;color:#475569;font-size:13px;line-height:1.55;">' +
escape((c.summary_tr || f.impact.reason || "").slice(0, 240)) +
'</td></tr>' +
'<tr><td colspan="2" style="padding-top:10px;">' +
'<span style="display:inline-block;font-size:11px;color:#64748b;' +
                        'background:#f1f5f9;padding:2px 8px;border-radius:4px;margin-right:6px;">' +
escape(typeTr) +
'</span>' +
'<span style="display:inline-block;font-size:11px;color:#94a3b8;">' +
'· ' + escape(f.source) +
'</span>' +
'<span style="float:right;">' +
'<a href="' + escape(f.link) + '" ' +
'style="font-size:12px;color:#2563eb;text-decoration:none;font-weight:600;">Kaynak →</a>' +
'</span>' +
'</td></tr>' +
'</table>' +
'</td></tr>' +
'</table>'
);
}

function translateType(t) {
const map = {
"new_feature": "Yeni özellik",
"update": "Güncelleme",
"announcement": "Duyuru",
"research": "Araştırma",
"none": "Diğer"
};
return map[t] || t || "Diğer";
}

function getDayNameTR(d) {
return ["Pazar","Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi"][d];
}

/_ ---- Plain text fallback ---- _/
function buildPlainText(d) {
let t = "AI ÜRÜN RADARI — " + d.dateStr + "\n";
t += "=".repeat(50) + "\n\n";
t += (d.report.summary || "") + "\n\n";

if (!d.features.length) {
t += "Bugün kayda değer bir lansman tespit edilmedi.\n\n";
} else {
d.companyOrder.forEach(co => {
t += "🏢 " + co.toUpperCase() + "\n";
t += "-".repeat(40) + "\n";
d.byCompany[co].forEach(f => {
const c = f.classification;
t += "• " + (c.feature_tr || c.feature) + " [" + f.impact.score + "/100]\n";
t += " " + (c.summary_tr || f.impact.reason || "") + "\n";
t += " " + f.link + "\n\n";
});
});
}

if ((d.report.trends || []).length) {
t += "\n📈 TRENDLER\n";
t += "-".repeat(40) + "\n";
d.report.trends.forEach(tr => t += "• " + tr + "\n");
}
if (d.report.insight) {
t += "\n🧠 STRATEJİK İÇGÖRÜ\n";
t += "-".repeat(40) + "\n";
t += d.report.insight + "\n";
}
t += "\n\n" + "-".repeat(50) + "\n";
t += "📢 Arkadaşlarına önermek ister misin?\n";
t += "Başvuru formu: https://forms.gle/mWKvXgTJbZNVwHKk9\n\n";
t += "Bu maili almak istemiyorsan ya da geri bildirim için\n";
t += "Bilal'e ulaşabilirsin: bilalabic78@gmail.com\n";
return t;
}

/_ =========================================================
MAIL LİSTESİ — Google Sheets'ten oku
========================================================= _/
function getMailListFromSheet() {
try {
const ss = SpreadsheetApp.openById(CONFIG.MAIL_LIST_SHEET_ID);
const sheet = ss.getSheetByName(CONFIG.MAIL_LIST_SHEET_NAME);
if (!sheet) {
throw new Error("Sekme bulunamadı: " + CONFIG.MAIL_LIST_SHEET_NAME);
}

    const data = sheet.getDataRange().getValues();
    if (data.length < 2) {
      Logger.log("⚠️ Mail listesi boş (sadece başlık var).");
      return [];
    }

    // Başlık satırını atla, kolonları işle: A=Email, B=İsim, C=Aktif
    const recipients = [];
    for (let i = 1; i < data.length; i++) {
      // Kolonlar: A=Zaman damgası, B=E-posta, C=İsim, D=İlgi, E=Nereden, F=Not, G=Aktif
      const email = String(data[i][1] || "").trim();  // B sütunu = E-posta
      const aktif = String(data[i][6] || "").trim().toUpperCase();  // G sütunu = Aktif

      // Geçerli email ve aktif olanları al
      if (email && email.indexOf("@") > 0 && aktif === "EVET") {
        recipients.push(email);
      }
    }

    Logger.log("📧 Mail listesi yüklendi: " + recipients.length + " aktif alıcı");
    return recipients;

} catch (e) {
Logger.log("❌ Mail listesi okunamadı: " + e);
// Güvenlik ağı: hata durumunda en azından sana gitsin
return ["bilalabic78@gmail.com"];
}
}
/_ =========================================================
OpenAI helper
========================================================= _/
function callOpenAI(model, messages, temperature) {
const apiKey = PropertiesService.getScriptProperties().getProperty("OPENAI_KEY");
if (!apiKey) throw new Error("OPENAI_KEY ayarlı değil.");
const resp = UrlFetchApp.fetch("https://api.openai.com/v1/chat/completions", {
method: "post", contentType: "application/json", muteHttpExceptions: true,
headers: { Authorization: "Bearer " + apiKey },
payload: JSON.stringify({
model: model, messages: messages,
temperature: (temperature == null ? 0.2 : temperature),
response_format: { type: "json_object" }
})
});
if (resp.getResponseCode() !== 200) {
throw new Error("OpenAI " + resp.getResponseCode() + ": " + resp.getContentText().slice(0, 300));
}
return JSON.parse(resp.getContentText()).choices[0].message.content;
}

function safeJson(raw) {
if (!raw) return null;
const cleaned = String(raw).replace(/`json|`/g, "").trim();
try { return JSON.parse(cleaned); } catch(e) {
Logger.log(" JSON parse hatası: " + cleaned.slice(0, 200));
return null;
}
}

function escape(s) {
if (s === null || s === undefined) return "";
return String(s)
.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
.replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

/_ =========================================================
TRIGGERS & SETUP
========================================================= _/
function installDailyTrigger() {
ScriptApp.getProjectTriggers().forEach(t => {
if (t.getHandlerFunction() === "runDailyIntelligence") ScriptApp.deleteTrigger(t);
});
ScriptApp.newTrigger("runDailyIntelligence")
.timeBased().atHour(18).everyDays(1).create();
Logger.log("Günlük tetikleyici saat 18:00 için kuruldu.");
}
function deleteAllTriggers() {
ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
Logger.log("Tüm tetikleyiciler silindi.");
}
function setApiKey(key) {
PropertiesService.getScriptProperties().setProperty("OPENAI_KEY", key);
Logger.log("API anahtarı kaydedildi.");
}
function testRunNow() { runDailyIntelligence(); }
function clearMemory() {
PropertiesService.getScriptProperties().deleteProperty(CONFIG.CACHE_KEY);
Logger.log("Hafıza temizlendi.");
}

/_ =========================================================
DIAGNOSTIC — classifier gerçekten ne diyor?
========================================================= _/
function diagnoseOneRun() {
const raw = fetchNews();
const deduped = dedupeAndFreshness(raw);
const sample = deduped.slice(0, 20);
Logger.log("=== TEŞHİS: ilk 20 haber sınıflandırılıyor ===");
sample.forEach(n => {
const c = classifyFeatureWithAI(n);
Logger.log("• " + (n.title.slice(0, 80)) +
"\n kaynak=" + n.source +
"\n => " + JSON.stringify(c));
});
}

/_ =========================================================
MAIL ÖNİZLEME — tarayıcıda nasıl görüneceğini kontrol et
(fake data ile sendEmail çalıştırır)
========================================================= _/
function previewEmailWithFakeData() {
const fake = [
{
title: "Google launches Gemini 3.1 Flash-Lite",
link: "https://blog.google/technology/ai/gemini-3-1",
source: "Google AI Blog",
summary: "",
classification: {
isFeature: true, company: "Google",
feature: "Gemini 3.1 Flash-Lite",
feature_tr: "Gemini 3.1 Flash-Lite",
summary_tr: "Google, hızlı ve maliyet-verimli yeni modeli Gemini 3.1 Flash-Lite'ı duyurdu. Model, düşük gecikmeli uygulamalar için optimize edildi.",
type: "new_feature", confidence: 92
},
impact: { score: 82, reason: "Düşük maliyetli hızlı modeller pazarında doğrudan rekabet." }
},
{
title: "OpenAI introduces GPT-Rosalind",
link: "https://openai.com/index/gpt-rosalind",
source: "OpenAI News",
summary: "",
classification: {
isFeature: true, company: "OpenAI",
feature: "GPT-Rosalind",
feature_tr: "GPT-Rosalind (yaşam bilimleri modeli)",
summary_tr: "OpenAI, biyoloji, ilaç keşfi ve translasyonel tıp için optimize edilmiş frontier muhakeme modelini tanıttı.",
type: "new_feature", confidence: 95
},
impact: { score: 91, reason: "Alan-spesifik frontier modelinin yeni bir sektörü hedeflemesi paradigmatik." }
},
{
title: "Anthropic launches Claude Design",
link: "https://www.anthropic.com/news/claude-design",
source: "Anthropic News",
summary: "",
classification: {
isFeature: true, company: "Anthropic",
feature: "Claude Design",
feature_tr: "Claude Design",
summary_tr: "Anthropic, tasarım, prototip ve sunum üretimine yönelik yeni bir Claude Labs ürünü olan Claude Design'ı başlattı.",
type: "new_feature", confidence: 88
},
impact: { score: 74, reason: "Canva/Figma tarafına AI ajanı olarak doğrudan rekabet." }
},
{
title: "Microsoft adds Grok 4.20 to Foundry",
link: "https://techcommunity.microsoft.com/foundry-grok",
source: "Microsoft AI Blog",
summary: "",
classification: {
isFeature: true, company: "Microsoft",
feature: "Grok 4.20 in Foundry",
feature_tr: "Foundry'de Grok 4.20 entegrasyonu",
summary_tr: "Microsoft Foundry'de xAI'nin Grok 4.20 modeli artık üretim-grade AI uygulamaları için kullanılabilir.",
type: "update", confidence: 82
},
impact: { score: 58, reason: "Azure AI portföyüne güçlü bir frontier model eklenmesi." }
}
];

const report = {
summary: "Bugün öne çıkan dört büyük hamle var: OpenAI yaşam bilimleri modelini, Google maliyet-verimli Gemini 3.1'i, Anthropic tasarım ajanı Claude Design'ı tanıttı; Microsoft Foundry'ye Grok 4.20 eklendi.",
trends: [
"Alan-spesifik (biyoloji, tasarım) frontier modeller yaygınlaşıyor.",
"Model pazarında 'hızlı + ucuz' segment rekabeti sertleşiyor.",
"Hyperscaler platformlar çoklu-model stratejisini derinleştiriyor."
],
insight: "Önümüzdeki çeyrekte kazananlar, tek modelle değil belirli iş yüklerine özel modeller sunan sağlayıcılar olacak."
};

sendEmail(report, fake);
Logger.log("Önizleme maili gönderildi: " + CONFIG.EMAIL_TO);
}
