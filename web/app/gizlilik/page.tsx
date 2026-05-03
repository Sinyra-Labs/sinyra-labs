import type { Metadata } from "next";
import Link from "next/link";
import { Navbar } from "../_components/Navbar";
import { Footer } from "../_components/Footer";
import { CONTACT_EMAIL } from "@/lib/constants";

export const metadata: Metadata = {
  title: "Gizlilik Politikası — Sinyra Labs",
};

const LAST_UPDATED = "3 Mayıs 2026";

export default function GizlilikPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 bg-white px-4 py-12">
        <div className="max-w-2xl mx-auto prose-sm">
          <p className="text-slate-400 text-xs mb-2">Son güncelleme: {LAST_UPDATED}</p>
          <h1 className="text-slate-900 text-2xl font-bold mb-8">Gizlilik Politikası</h1>

          <Section title="Hangi verileri topluyoruz?">
            Yalnızca başvuru formunda gönderdiğiniz <strong>e-posta adresinizi</strong> ve adınızı
            saklıyoruz. Başka kişisel veri toplanmaz.
          </Section>

          <Section title="Bu verileri nasıl kullanıyoruz?">
            Topladığımız veriler yalnızca <strong>günlük AI brifingini göndermek</strong> için
            kullanılır. Üçüncü taraflarla paylaşılmaz, reklam veya profil oluşturma amacıyla
            kullanılmaz.
          </Section>

          <Section title="Verilerinizi kimlerle paylaşıyoruz?">
            E-posta gönderimi için Google Gmail altyapısını kullanıyoruz. Başka hiçbir üçüncü
            tarafla veri paylaşılmaz.
          </Section>

          <Section title="Aboneliği nasıl iptal edebilirsiniz?">
            İstediğiniz zaman{" "}
            <a href={`mailto:${CONTACT_EMAIL}`} className="text-blue-600 underline">
              {CONTACT_EMAIL}
            </a>{" "}
            adresine e-posta göndererek listeden çıkabilirsiniz. Talebiniz en geç 48 saat içinde
            işlenir.
          </Section>

          <Section title="Çerezler">
            Bu site herhangi bir çerez veya izleme kodu kullanmamaktadır.
          </Section>

          <Section title="İletişim">
            Gizlilikle ilgili sorularınız için:{" "}
            <a href={`mailto:${CONTACT_EMAIL}`} className="text-blue-600 underline">
              {CONTACT_EMAIL}
            </a>
          </Section>

          <div className="mt-10">
            <Link href="/" className="text-blue-600 text-sm hover:underline">
              ← Ana sayfaya dön
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mb-7">
      <h2 className="text-slate-800 font-semibold text-base mb-2">{title}</h2>
      <p className="text-slate-600 text-sm leading-relaxed">{children}</p>
    </div>
  );
}
