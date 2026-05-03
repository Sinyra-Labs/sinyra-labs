import { Navbar } from "./_components/Navbar";
import { Footer } from "./_components/Footer";
import { HomeJsonLd, FAQ_ITEMS } from "./_components/JsonLd";
import { FORMS_URL, CONTACT_EMAIL, SUBSCRIBER_COUNT } from "@/lib/constants";
import type { Metadata } from "next";

export const metadata: Metadata = {
  alternates: { canonical: "https://sinyra.com" },
};

const HOW_IT_WORKS = [
  {
    icon: "🔍",
    title: "50+ Kaynak Taranır",
    body: "OpenAI, Google DeepMind, Anthropic, Meta AI, xAI, Mistral ve daha fazlasının blogu, RSS beslemeleri ve Google News akışları her gün otomatik toplanır.",
  },
  {
    icon: "🤖",
    title: "AI Sınıflandırır",
    body: "GPT-4o-mini her haberi inceler: gerçek ürün lansmanı mı, yatırım haberi mi, spekülatif mi? Yalnızca gerçek lansmanlar 0-100 etki puanı alır.",
  },
  {
    icon: "📬",
    title: "Türkçe Özetlenir",
    body: "Etki puanı en yüksek haberler seçilir, kısa Türkçe rationale ile birlikte her sabah 18:00'de e-postanıza ulaşır.",
  },
];

const SOURCES = [
  "OpenAI", "Google DeepMind", "Anthropic", "Meta AI",
  "xAI", "Mistral", "Hugging Face", "GitHub Copilot",
  "AWS AI", "Microsoft Copilot", "Vercel AI", "Cohere",
];

export default function HomePage() {
  return (
    <>
      <HomeJsonLd />
      <div className="min-h-screen flex flex-col">
        <Navbar />

        {/* HERO */}
        <section className="bg-brand-navy px-4 pt-20 pb-24 text-center" aria-label="Giriş">
          <p className="text-brand-yellow text-xs font-bold tracking-widest uppercase mb-4">
            Sinyra Labs
          </p>
          <h1 className="text-white text-4xl md:text-6xl font-bold leading-tight max-w-2xl mx-auto">
            Cut Through
            <br />
            <span className="text-brand-yellow">the Noise</span>
          </h1>
          <p className="text-slate-400 text-base md:text-lg mt-6 max-w-xl mx-auto leading-relaxed">
            Rakiplerinizin ne yaptığını her sabah özetliyoruz.
            AI ürün lansmanları — gürültüsüz, özetlenmiş, <strong className="text-slate-300">Türkçe</strong>.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row gap-3 justify-center">
            <a
              href={FORMS_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block bg-brand-yellow text-brand-navy font-bold text-sm
                         px-8 py-4 rounded-lg hover:bg-amber-300 transition-colors"
              aria-label="Ücretsiz abone olmak için formu aç"
            >
              → Ücretsiz Abone Ol
            </a>
            <a
              href="#nasil-calisir"
              className="inline-block border border-slate-600 text-slate-300 font-medium text-sm
                         px-8 py-4 rounded-lg hover:border-slate-400 hover:text-white transition-colors"
            >
              Nasıl çalışır?
            </a>
          </div>
          <p className="text-slate-600 text-xs mt-5">
            Günde 1 e-posta · Reklam yok · İstediğinizde çıkabilirsiniz
          </p>
        </section>

        {/* STATS BAR */}
        <section className="bg-brand-slate px-4 py-5" aria-label="İstatistikler">
          <div className="max-w-3xl mx-auto grid grid-cols-3 divide-x divide-slate-700 text-center">
            {[
              { v: `${SUBSCRIBER_COUNT}+`, l: "Okuyucu" },
              { v: "50+", l: "AI Kaynağı" },
              { v: "Her Gün", l: "18:00 TST" },
            ].map(({ v, l }) => (
              <div key={l} className="px-4 py-1">
                <div className="text-white font-bold text-xl">{v}</div>
                <div className="text-slate-400 text-xs mt-0.5">{l}</div>
              </div>
            ))}
          </div>
        </section>

        {/* HOW IT WORKS */}
        <section id="nasil-calisir" className="bg-white px-4 py-16" aria-labelledby="how-heading">
          <div className="max-w-3xl mx-auto">
            <h2 id="how-heading" className="text-slate-900 text-2xl font-bold text-center mb-2">
              Nasıl çalışır?
            </h2>
            <p className="text-slate-400 text-sm text-center mb-10">
              Pipeline tamamen otomatik — her gün UTC 15:00'de çalışır.
            </p>
            <div className="grid md:grid-cols-3 gap-6">
              {HOW_IT_WORKS.map((step) => (
                <article
                  key={step.title}
                  className="bg-slate-50 rounded-xl p-6 border border-slate-100"
                >
                  <div className="text-3xl mb-3" aria-hidden>{step.icon}</div>
                  <h3 className="text-slate-900 font-bold text-base mb-2">{step.title}</h3>
                  <p className="text-slate-500 text-sm leading-relaxed">{step.body}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* SOURCES */}
        <section className="bg-slate-50 border-y border-slate-100 px-4 py-10" aria-labelledby="sources-heading">
          <div className="max-w-3xl mx-auto text-center">
            <h2 id="sources-heading" className="text-slate-500 text-xs font-bold tracking-widest uppercase mb-6">
              Takip edilen kaynaklar
            </h2>
            <div className="flex flex-wrap justify-center gap-2">
              {SOURCES.map((s) => (
                <span
                  key={s}
                  className="text-xs text-slate-500 bg-white border border-slate-200
                             px-3 py-1.5 rounded-full font-medium"
                >
                  {s}
                </span>
              ))}
              <span className="text-xs text-slate-400 bg-white border border-slate-200 px-3 py-1.5 rounded-full">
                +38 daha
              </span>
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="bg-white px-4 py-16" aria-labelledby="faq-heading">
          <div className="max-w-2xl mx-auto">
            <h2 id="faq-heading" className="text-slate-900 text-2xl font-bold mb-8">
              Sık sorulan sorular
            </h2>
            <dl className="space-y-6">
              {FAQ_ITEMS.map(({ q, a }) => (
                <div key={q} className="border-b border-slate-100 pb-6 last:border-0">
                  <dt className="text-slate-800 font-semibold text-base mb-2">{q}</dt>
                  <dd className="text-slate-500 text-sm leading-relaxed">{a}</dd>
                </div>
              ))}
            </dl>
          </div>
        </section>

        {/* CTA */}
        <section className="bg-brand-navy px-4 py-16 text-center" aria-labelledby="cta-heading">
          <p className="text-brand-yellow text-xs font-bold tracking-widest uppercase mb-3">
            📬 Liste
          </p>
          <h2 id="cta-heading" className="text-white text-2xl md:text-3xl font-bold mb-4">
            AI haberlerinde öne geç
          </h2>
          <p className="text-slate-400 text-sm mb-8 max-w-sm mx-auto">
            Başvuru formunu doldurun — bir sonraki brifingden itibaren listedesiniz.
          </p>
          <a
            href={FORMS_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-brand-yellow text-brand-navy font-bold text-sm
                       px-8 py-4 rounded-lg hover:bg-amber-300 transition-colors"
          >
            Başvuru Formunu Aç →
          </a>
          <p className="text-slate-600 text-xs mt-4">
            Sorun mu var?{" "}
            <a href={`mailto:${CONTACT_EMAIL}`} className="text-slate-400 hover:text-white transition-colors">
              {CONTACT_EMAIL}
            </a>
          </p>
        </section>

        <Footer />
      </div>
    </>
  );
}
