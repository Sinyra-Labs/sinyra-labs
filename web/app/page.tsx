import { Navbar } from "./_components/Navbar";
import { Footer } from "./_components/Footer";
import { FORMS_URL, CONTACT_EMAIL } from "@/lib/constants";

const HOW_IT_WORKS = [
  {
    icon: "🔍",
    title: "50+ Kaynak Taranır",
    body: "OpenAI, Google, Anthropic, Meta ve daha fazlasının blogu, RSS beslemeleri ve haber akışları günlük toplanır.",
  },
  {
    icon: "🤖",
    title: "AI Sınıflandırır",
    body: "GPT ile her haber incelenir: gerçek ürün lansmanı mı, yatırım haberi mi, spekülatif mi? Sadece lansmanlar geçer.",
  },
  {
    icon: "📬",
    title: "Özetlenmiş Gelir",
    body: "Etki skoru en yüksek haberler seçilir, kısa Türkçe rationale ile birlikte her sabah e-postanıza ulaşır.",
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      {/* HERO */}
      <section className="bg-brand-navy px-4 pt-20 pb-24 text-center">
        <p className="text-brand-yellow text-xs font-bold tracking-widest uppercase mb-4">
          Sinyra Labs
        </p>
        <h1 className="text-white text-4xl md:text-6xl font-bold leading-tight max-w-2xl mx-auto">
          Cut Through
          <br />
          <span className="text-brand-yellow">the Noise</span>
        </h1>
        <p className="text-slate-400 text-base md:text-lg mt-6 max-w-lg mx-auto leading-relaxed">
          Rakiplerinizin ne yaptığını her sabah özetliyoruz.
          <br />
          AI ürün lansmanları — gürültüsüz, Türkçe.
        </p>
        <div className="mt-10 flex flex-col sm:flex-row gap-3 justify-center">
          <a
            href={FORMS_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block bg-brand-yellow text-brand-navy font-bold text-sm
                       px-8 py-4 rounded-lg hover:bg-amber-300 transition-colors"
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

      {/* HOW IT WORKS */}
      <section id="nasil-calisir" className="bg-white px-4 py-16">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-slate-900 text-2xl font-bold text-center mb-2">
            Nasıl çalışır?
          </h2>
          <p className="text-slate-400 text-sm text-center mb-10">
            Pipeline tamamen otomatik, her gün çalışır.
          </p>
          <div className="grid md:grid-cols-3 gap-6">
            {HOW_IT_WORKS.map((step) => (
              <div
                key={step.title}
                className="bg-slate-50 rounded-xl p-6 border border-slate-100"
              >
                <div className="text-3xl mb-3">{step.icon}</div>
                <h3 className="text-slate-900 font-bold text-base mb-2">{step.title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{step.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SOCIAL PROOF */}
      <section className="bg-slate-50 border-y border-slate-100 px-4 py-10 text-center">
        <p className="text-slate-400 text-xs uppercase tracking-widest font-semibold mb-3">
          Şu an takip edenler
        </p>
        <p className="text-slate-700 text-2xl font-bold">11 okuyucu</p>
        <p className="text-slate-400 text-sm mt-1">
          Yazılım geliştirici, öğrenci, ürün yöneticisi
        </p>
      </section>

      {/* CTA */}
      <section className="bg-brand-navy px-4 py-16 text-center">
        <p className="text-brand-yellow text-xs font-bold tracking-widest uppercase mb-3">
          📬 Liste
        </p>
        <h2 className="text-white text-2xl md:text-3xl font-bold mb-4">
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
          <a href={`mailto:${CONTACT_EMAIL}`} className="text-slate-400 hover:text-white">
            {CONTACT_EMAIL}
          </a>{" "}
          adresine yazın.
        </p>
      </section>

      <Footer />
    </div>
  );
}
