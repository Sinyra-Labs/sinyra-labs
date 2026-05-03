import { Navbar } from "./_components/Navbar";
import { Footer } from "./_components/Footer";
import { HomeJsonLd, FAQ_ITEMS } from "./_components/JsonLd";
import { FORMS_URL, CONTACT_EMAIL, SITE_URL } from "@/lib/constants";
import type { Metadata } from "next";

export const metadata: Metadata = {
  alternates: { canonical: SITE_URL },
};

const HOW_IT_WORKS = [
  {
    step: "01",
    icon: "🔍",
    title: "50+ Kaynak Taranır",
    body: "OpenAI, Google DeepMind, Anthropic, Meta AI, xAI, Mistral ve daha fazlasının blogu, RSS beslemeleri ve Google News akışları her gün otomatik toplanır.",
  },
  {
    step: "02",
    icon: "🤖",
    title: "AI Sınıflandırır & Puanlar",
    body: "GPT-4o-mini her haberi inceler: gerçek ürün lansmanı mı, yatırım haberi mi, spekülatif mi? Yalnızca gerçek lansmanlar 0-100 etki puanı alır.",
  },
  {
    step: "03",
    icon: "📬",
    title: "Türkçe Özetlenir",
    body: "Etki puanı en yüksek haberler seçilir, kısa Türkçe rationale ile birlikte her gün 18:00'de e-postanıza ulaşır.",
  },
];

const SOURCES = [
  { name: "OpenAI", color: "#10a37f" },
  { name: "Google DeepMind", color: "#4285f4" },
  { name: "Anthropic", color: "#d97706" },
  { name: "Meta AI", color: "#0866ff" },
  { name: "xAI", color: "#ffffff" },
  { name: "Mistral", color: "#ff7000" },
  { name: "Hugging Face", color: "#ffd21e" },
  { name: "GitHub Copilot", color: "#6e40c9" },
  { name: "AWS AI", color: "#ff9900" },
  { name: "Microsoft Copilot", color: "#0078d4" },
  { name: "Vercel AI", color: "#ffffff" },
  { name: "Cohere", color: "#39d353" },
];

const SAMPLE_ITEMS = [
  { company: "OpenAI", title: "GPT-4o realtime API genel kullanıma açıldı", score: 94, type: "Yeni API" },
  { company: "Anthropic", title: "Claude Sonnet 4.5 — kod performansında %40 artış", score: 88, type: "Model Güncellemesi" },
  { company: "Google", title: "Gemini 2.0 Flash: $0.10/M token ile en ucuz frontier", score: 81, type: "Yeni Model" },
];

function ScoreBadge({ score }: { score: number }) {
  const color = score >= 90 ? "#ef4444" : score >= 75 ? "#f59e0b" : "#22c55e";
  return (
    <span
      style={{ color, borderColor: color + "44", backgroundColor: color + "11" }}
      className="text-[10px] font-bold px-2 py-0.5 rounded-full border whitespace-nowrap"
    >
      {score}/100
    </span>
  );
}

function MockEmailCard() {
  return (
    <div className="relative">
      {/* Glow effect */}
      <div className="absolute inset-0 bg-brand-yellow/10 rounded-2xl blur-2xl scale-105 pointer-events-none" />
      <div className="relative bg-[#0d1829] border border-slate-700/60 rounded-2xl overflow-hidden shadow-2xl">
        {/* Email header */}
        <div className="bg-[#080f1c] px-4 py-3 border-b border-slate-800 flex items-center gap-3">
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-red-500/70" />
            <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/70" />
            <div className="w-2.5 h-2.5 rounded-full bg-green-500/70" />
          </div>
          <div className="flex-1 bg-slate-800/60 rounded px-3 py-1 text-slate-500 text-[10px]">
            Gelen Kutusu — Sinyra Labs Brifing
          </div>
        </div>

        {/* Email meta */}
        <div className="px-4 pt-4 pb-2 border-b border-slate-800/60">
          <div className="flex items-start justify-between gap-2">
            <div>
              <div className="text-brand-yellow text-[10px] font-bold tracking-widest uppercase">SINYRA LABS</div>
              <div className="text-white font-bold text-sm mt-0.5">🧠 Günlük AI Brifing</div>
              <div className="text-slate-500 text-[10px] mt-0.5">Cumartesi, 3 Mayıs 2026 · 18:00</div>
            </div>
            <div className="text-right shrink-0">
              <div className="text-white text-lg font-bold">3</div>
              <div className="text-slate-500 text-[10px]">Öne çıkan</div>
            </div>
          </div>
          <p className="text-slate-400 text-[11px] leading-relaxed mt-2 border-t border-slate-800 pt-2">
            Bugün üç kritik hamle: OpenAI realtime API'yi, Anthropic dördüncü nesil Sonnet'i, Google en ucuz frontier modelini duyurdu.
          </p>
        </div>

        {/* Items */}
        <div className="divide-y divide-slate-800/60">
          {SAMPLE_ITEMS.map((item) => (
            <div key={item.title} className="px-4 py-3 flex items-start gap-3">
              <div className="flex-1 min-w-0">
                <div className="text-slate-500 text-[10px] font-semibold uppercase tracking-wide">{item.company}</div>
                <div className="text-slate-200 text-xs font-semibold leading-snug mt-0.5 truncate">{item.title}</div>
                <div className="text-slate-600 text-[10px] mt-0.5">{item.type}</div>
              </div>
              <ScoreBadge score={item.score} />
            </div>
          ))}
        </div>

        {/* Footer strip */}
        <div className="bg-brand-yellow/10 border-t border-brand-yellow/20 px-4 py-2.5 flex items-center justify-between">
          <span className="text-brand-yellow text-[10px] font-bold">Etki puanlarıyla sıralanmış</span>
          <span className="text-slate-500 text-[10px]">Kaynaklara git →</span>
        </div>
      </div>
    </div>
  );
}

export default function HomePage() {
  return (
    <>
      <HomeJsonLd />
      <div className="min-h-screen flex flex-col">
        <Navbar />

        {/* HERO — two column */}
        <section
          className="bg-brand-navy px-4 pt-16 pb-20 relative overflow-hidden"
          aria-label="Giriş"
        >
          {/* Background grid */}
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              backgroundImage:
                "linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)",
              backgroundSize: "40px 40px",
            }}
          />
          {/* Radial glow top-left */}
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-brand-yellow/5 rounded-full blur-3xl pointer-events-none" />

          <div className="max-w-5xl mx-auto relative">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              {/* Left: copy */}
              <div>
                <div className="inline-flex items-center gap-2 bg-brand-yellow/10 border border-brand-yellow/25 rounded-full px-4 py-1.5 mb-6">
                  <span className="w-2 h-2 rounded-full bg-brand-yellow animate-pulse" />
                  <span className="text-brand-yellow text-xs font-bold tracking-widest uppercase">
                    Her gün 18:00&apos;de gönderiliyor
                  </span>
                </div>

                <h1 className="text-white text-4xl md:text-5xl font-bold leading-tight">
                  Rakiplerinizin<br />
                  AI hamlelerini<br />
                  <span className="text-brand-yellow">kaçırmayın.</span>
                </h1>

                <p className="text-slate-400 text-base mt-5 leading-relaxed max-w-md">
                  50+ kaynak her gün otomatik taranır, GPT ile sınıflandırılır,
                  etki puanlanır — sadece önemli lansmanlar{" "}
                  <strong className="text-slate-300">Türkçe özetle</strong> e-postanıza ulaşır.
                </p>

                {/* Social proof */}
                <div className="flex items-center gap-3 mt-6">
                  <div className="flex -space-x-2">
                    {["B", "M", "A", "K", "S"].map((initial, i) => (
                      <div
                        key={i}
                        className="w-8 h-8 rounded-full border-2 border-brand-navy bg-brand-slate
                                   flex items-center justify-center text-xs font-bold text-slate-300"
                      >
                        {initial}
                      </div>
                    ))}
                  </div>
                  <div className="text-slate-400 text-sm">
                    <span className="text-white font-semibold">11+ okuyucu</span> zaten listeye katıldı
                  </div>
                </div>

                <div className="mt-8 flex flex-col sm:flex-row gap-3">
                  <a
                    href={FORMS_URL}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center gap-2
                               bg-brand-yellow text-brand-navy font-bold text-sm
                               px-7 py-3.5 rounded-lg hover:bg-amber-300 transition-colors"
                    aria-label="Ücretsiz abone olmak için formu aç"
                  >
                    Ücretsiz Abone Ol
                    <span aria-hidden>→</span>
                  </a>
                  <a
                    href="#nasil-calisir"
                    className="inline-flex items-center justify-center
                               border border-slate-700 text-slate-400 font-medium text-sm
                               px-7 py-3.5 rounded-lg hover:border-slate-500 hover:text-white transition-colors"
                  >
                    Nasıl çalışır?
                  </a>
                </div>

                <p className="text-slate-600 text-xs mt-4">
                  Günde 1 e-posta · Reklam yok · İstediğinizde çıkabilirsiniz
                </p>
              </div>

              {/* Right: mock email */}
              <div className="hidden lg:block">
                <MockEmailCard />
              </div>
            </div>
          </div>
        </section>

        {/* STATS BAR */}
        <section className="bg-[#111827] border-y border-slate-800 px-4 py-6" aria-label="İstatistikler">
          <div className="max-w-3xl mx-auto grid grid-cols-3 divide-x divide-slate-700/60 text-center">
            {[
              { v: "50+", l: "AI Kaynağı" },
              { v: "Her Gün", l: "Saat 18:00" },
              { v: "0₺", l: "Tamamen Ücretsiz" },
            ].map(({ v, l }) => (
              <div key={l} className="px-6 py-2">
                <div className="text-brand-yellow font-bold text-2xl">{v}</div>
                <div className="text-slate-500 text-xs mt-1 font-medium">{l}</div>
              </div>
            ))}
          </div>
        </section>

        {/* HOW IT WORKS */}
        <section id="nasil-calisir" className="bg-white px-4 py-20" aria-labelledby="how-heading">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-14">
              <p className="text-brand-navy text-xs font-bold tracking-widest uppercase mb-3">Pipeline</p>
              <h2 id="how-heading" className="text-slate-900 text-3xl font-bold">
                Nasıl çalışır?
              </h2>
              <p className="text-slate-500 text-sm mt-3 max-w-md mx-auto">
                Tamamen otomatik — siz akşam çayınızı içerken brifing gelen kutunuza düşer.
              </p>
            </div>
            <div className="grid md:grid-cols-3 gap-6">
              {HOW_IT_WORKS.map((step) => (
                <article
                  key={step.title}
                  className="relative bg-slate-50 rounded-2xl p-7 border border-slate-100
                             hover:border-slate-300 hover:shadow-md transition-all"
                >
                  <div className="absolute top-5 right-5 text-slate-200 text-4xl font-black select-none">
                    {step.step}
                  </div>
                  <div className="text-3xl mb-4" aria-hidden>{step.icon}</div>
                  <h3 className="text-slate-900 font-bold text-base mb-2">{step.title}</h3>
                  <p className="text-slate-500 text-sm leading-relaxed">{step.body}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* SAMPLE EMAIL PREVIEW (mobile-first, full-width) */}
        <section className="bg-[#080f1c] px-4 py-16 border-y border-slate-800" aria-labelledby="sample-heading">
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-10">
              <p className="text-brand-yellow text-xs font-bold tracking-widest uppercase mb-3">Örnek Brifing</p>
              <h2 id="sample-heading" className="text-white text-2xl font-bold">
                Her gün 18:00&apos;de böyle bir e-posta gelir
              </h2>
            </div>

            <div className="bg-[#0d1829] border border-slate-700/60 rounded-2xl overflow-hidden">
              {/* Items */}
              <div className="divide-y divide-slate-800">
                {SAMPLE_ITEMS.map((item, i) => (
                  <div key={item.title} className="px-5 py-4 flex items-start gap-4">
                    <div className="w-6 h-6 rounded-full bg-brand-yellow/10 border border-brand-yellow/30
                                    flex items-center justify-center shrink-0 mt-0.5">
                      <span className="text-brand-yellow text-[10px] font-black">{i + 1}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-0.5">
                        <span className="text-slate-500 text-[10px] font-bold uppercase tracking-wide">
                          {item.company}
                        </span>
                        <span className="text-slate-700 text-[10px]">·</span>
                        <span className="text-slate-600 text-[10px]">{item.type}</span>
                      </div>
                      <div className="text-slate-200 text-sm font-semibold leading-snug">
                        {item.title}
                      </div>
                    </div>
                    <ScoreBadge score={item.score} />
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/30 px-5 py-3 flex items-center justify-between">
                <span className="text-slate-500 text-[11px]">Etki puanına göre sıralanmış · Gerçek lansmanlar</span>
                <span className="text-brand-yellow text-[11px] font-semibold">+ 5 daha →</span>
              </div>
            </div>
          </div>
        </section>

        {/* SOURCES */}
        <section className="bg-slate-50 border-y border-slate-100 px-4 py-12" aria-labelledby="sources-heading">
          <div className="max-w-3xl mx-auto text-center">
            <h2 id="sources-heading" className="text-slate-400 text-xs font-bold tracking-widest uppercase mb-7">
              Takip edilen kaynaklar
            </h2>
            <div className="flex flex-wrap justify-center gap-2">
              {SOURCES.map((s) => (
                <span
                  key={s.name}
                  className="text-xs text-slate-600 bg-white border border-slate-200
                             px-3 py-1.5 rounded-full font-medium hover:border-slate-400 transition-colors"
                >
                  {s.name}
                </span>
              ))}
              <span className="text-xs text-slate-400 bg-white border border-dashed border-slate-300
                               px-3 py-1.5 rounded-full">
                +38 daha
              </span>
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="bg-white px-4 py-20" aria-labelledby="faq-heading">
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-12">
              <p className="text-brand-navy text-xs font-bold tracking-widest uppercase mb-3">SSS</p>
              <h2 id="faq-heading" className="text-slate-900 text-3xl font-bold">
                Sık sorulan sorular
              </h2>
            </div>
            <dl className="space-y-0 divide-y divide-slate-100 border-y border-slate-100">
              {FAQ_ITEMS.map(({ q, a }) => (
                <div key={q} className="py-5">
                  <dt className="text-slate-800 font-semibold text-sm mb-1.5">{q}</dt>
                  <dd className="text-slate-500 text-sm leading-relaxed">{a}</dd>
                </div>
              ))}
            </dl>
          </div>
        </section>

        {/* CTA */}
        <section
          className="bg-brand-navy px-4 py-20 text-center relative overflow-hidden"
          aria-labelledby="cta-heading"
        >
          <div className="absolute inset-0 pointer-events-none"
            style={{
              backgroundImage:
                "radial-gradient(circle at 60% 50%, rgba(251,191,36,0.07) 0%, transparent 60%)",
            }}
          />
          <div className="relative max-w-lg mx-auto">
            <div className="inline-flex items-center gap-2 bg-brand-yellow/10 border border-brand-yellow/25 rounded-full px-4 py-1.5 mb-6">
              <span className="w-2 h-2 rounded-full bg-brand-yellow" />
              <span className="text-brand-yellow text-xs font-bold tracking-widest uppercase">Ücretsiz</span>
            </div>
            <h2 id="cta-heading" className="text-white text-3xl md:text-4xl font-bold mb-4 leading-tight">
              AI haberlerinde<br />
              <span className="text-brand-yellow">bir adım önde</span> olun.
            </h2>
            <p className="text-slate-400 text-sm mb-8 max-w-sm mx-auto leading-relaxed">
              Başvuru formunu doldurun — bir sonraki brifingden itibaren listedesiniz. Kredi kartı gerekmez.
            </p>
            <a
              href={FORMS_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-brand-yellow text-brand-navy font-bold text-base
                         px-9 py-4 rounded-xl hover:bg-amber-300 transition-colors shadow-lg shadow-brand-yellow/20"
            >
              Başvuru Formunu Aç
              <span aria-hidden>→</span>
            </a>
            <p className="text-slate-600 text-xs mt-5">
              Sorun mu var?{" "}
              <a href={`mailto:${CONTACT_EMAIL}`} className="text-slate-400 hover:text-white transition-colors">
                {CONTACT_EMAIL}
              </a>
            </p>
          </div>
        </section>

        <Footer />
      </div>
    </>
  );
}
