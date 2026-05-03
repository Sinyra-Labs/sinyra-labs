import type { Metadata } from "next";
import Link from "next/link";
import { Navbar } from "../_components/Navbar";
import { Footer } from "../_components/Footer";
import { PageJsonLd } from "../_components/JsonLd";
import { FORMS_URL, CONTACT_EMAIL, SITE_URL, GITHUB_URL } from "@/lib/constants";

export const metadata: Metadata = {
  title: "Hakkında",
  description:
    "Sinyra Labs nedir, nasıl çalışır ve kim tarafından yapılıyor? AI ürün lansmanı brifing servisi hakkında her şey.",
  alternates: { canonical: `${SITE_URL}/hakkinda` },
  openGraph: {
    title: "Hakkında — Sinyra Labs",
    description: "Sinyra Labs nasıl çalışır? Teknoloji, misyon ve ekip.",
    url: `${SITE_URL}/hakkinda`,
  },
};

const TECH_STACK = [
  { label: "Dil", value: "Python 3.12" },
  { label: "Sınıflandırma", value: "GPT-4o-mini (OpenAI)" },
  { label: "Tarama", value: "RSS + Google News API" },
  { label: "E-posta", value: "Gmail SMTP" },
  { label: "Depolama", value: "SQLite (dedup)" },
  { label: "CI/CD", value: "GitHub Actions" },
  { label: "Web", value: "Next.js 15 / Vercel" },
];

export default function HakkindaPage() {
  return (
    <>
      <PageJsonLd
        path="/hakkinda"
        name="Hakkında — Sinyra Labs"
        description="Sinyra Labs nedir, nasıl çalışır ve kim tarafından yapılıyor."
      />
      <div className="min-h-screen flex flex-col">
        <Navbar />

        {/* HEADER */}
        <section className="bg-brand-navy px-4 py-14" aria-label="Sayfa başlığı">
          <div className="max-w-2xl mx-auto">
            <nav aria-label="Breadcrumb" className="mb-4">
              <ol className="flex gap-2 text-xs text-slate-500">
                <li><Link href="/" className="hover:text-slate-300 transition-colors">Ana Sayfa</Link></li>
                <li aria-hidden>›</li>
                <li className="text-slate-400">Hakkında</li>
              </ol>
            </nav>
            <p className="text-brand-yellow text-xs font-bold tracking-widest uppercase mb-3">Hakkında</p>
            <h1 className="text-white text-3xl md:text-4xl font-bold leading-snug">
              Sinyra Labs nedir?
            </h1>
            <p className="text-slate-400 text-base mt-4 leading-relaxed">
              AI ürün lansmanlarını otomatik izleyen ve her gün Türkçe özetleyen ücretsiz bir e-posta bülten servisi.
            </p>
          </div>
        </section>

        <main className="flex-1 bg-white px-4 py-12">
          <div className="max-w-2xl mx-auto space-y-12">

            {/* MISSION */}
            <section aria-labelledby="mission-heading">
              <h2 id="mission-heading" className="text-slate-800 font-bold text-lg mb-3">Misyon</h2>
              <p className="text-slate-600 text-sm leading-relaxed">
                AI ekosistemi hızla büyüyor; OpenAI, Google, Anthropic ve onlarca şirket her hafta yeni model, araç ve API yayınlıyor.
                Bu gürültüde önemli olanı bulmak giderek zorlaşıyor.
              </p>
              <p className="text-slate-600 text-sm leading-relaxed mt-3">
                Sinyra Labs bu gürültüyü filtreliyor: 50'den fazla kaynağı otomatik tarar, gerçek ürün lansmanlarını yapay zeka ile
                sınıflandırır, etki puanı hesaplar ve her gün 18:00'de gelen kutunuza özetlenmiş, Türkçe bir brifing gönderir.
              </p>
            </section>

            {/* HOW */}
            <section aria-labelledby="how-heading">
              <h2 id="how-heading" className="text-slate-800 font-bold text-lg mb-3">Teknik yapı</h2>
              <p className="text-slate-600 text-sm leading-relaxed mb-4">
                Pipeline GitHub Actions üzerinde her gün otomatik çalışır, brifing saat 18:00'de gelen kutunuza ulaşır:
              </p>
              <ol className="space-y-3 text-sm text-slate-600">
                {[
                  "RSS beslemeleri ve Google News sorguları toplanır (50+ kaynak, ~1500-2000 haber/gün)",
                  "Daha önce görülen haberler SQLite dedup store ile elenir",
                  "GPT-4o-mini her haberi sınıflandırır: gerçek ürün lansmanı mı? (classify.v2 prompt)",
                  "Geçen haberler 0-100 arası etki puanı alır (impact.v2 prompt, Türkçe rationale)",
                  "En etkili lansmanlar seçilir, LLM ile günlük özet + stratejik içgörü üretilir",
                  "Gmail SMTP ile abone listesine gönderilir",
                ].map((step, i) => (
                  <li key={i} className="flex gap-3">
                    <span className="shrink-0 w-5 h-5 rounded-full bg-brand-yellow text-brand-navy text-xs font-bold flex items-center justify-center mt-0.5">
                      {i + 1}
                    </span>
                    <span>{step}</span>
                  </li>
                ))}
              </ol>
            </section>

            {/* TECH STACK */}
            <section aria-labelledby="stack-heading">
              <h2 id="stack-heading" className="text-slate-800 font-bold text-lg mb-3">Teknoloji</h2>
              <div className="bg-slate-50 rounded-xl border border-slate-100 overflow-hidden">
                {TECH_STACK.map(({ label, value }, i) => (
                  <div
                    key={label}
                    className={`flex justify-between px-4 py-3 text-sm ${i < TECH_STACK.length - 1 ? "border-b border-slate-100" : ""}`}
                  >
                    <span className="text-slate-500">{label}</span>
                    <span className="text-slate-800 font-medium">{value}</span>
                  </div>
                ))}
              </div>
            </section>

            {/* CREATOR */}
            <section aria-labelledby="creator-heading">
              <h2 id="creator-heading" className="text-slate-800 font-bold text-lg mb-3">Yapan</h2>
              <div className="bg-slate-50 rounded-xl border border-slate-100 p-5">
                <p className="text-slate-800 font-semibold">Bilal Abiç</p>
                <p className="text-slate-500 text-sm mt-1">
                  Yazılım geliştirici. Sinyra Labs'ı AI ekosistemini Türkçe konuşan toplulukla
                  buluşturmak amacıyla geliştiriyor.
                </p>
                <div className="flex gap-4 mt-3 text-xs">
                  <a href={`mailto:${CONTACT_EMAIL}`} className="text-blue-600 hover:underline">
                    {CONTACT_EMAIL}
                  </a>
                  <a href={GITHUB_URL} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                    GitHub →
                  </a>
                </div>
              </div>
            </section>

            {/* CTA */}
            <section className="bg-brand-navy rounded-2xl p-8 text-center" aria-label="Abone ol">
              <p className="text-white font-bold text-lg mb-2">Listeye katıl</p>
              <p className="text-slate-400 text-sm mb-5">Ücretsiz. İstediğinizde çıkabilirsiniz.</p>
              <a
                href={FORMS_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block bg-brand-yellow text-brand-navy font-bold text-sm
                           px-6 py-3 rounded-lg hover:bg-amber-300 transition-colors"
              >
                Başvuru Formunu Aç →
              </a>
            </section>

            <div>
              <Link href="/" className="text-blue-600 text-sm hover:underline">← Ana sayfaya dön</Link>
            </div>
          </div>
        </main>

        <Footer />
      </div>
    </>
  );
}
