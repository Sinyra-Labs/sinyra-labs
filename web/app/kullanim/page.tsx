import type { Metadata } from "next";
import Link from "next/link";
import { Navbar } from "../_components/Navbar";
import { Footer } from "../_components/Footer";
import { CONTACT_EMAIL } from "@/lib/constants";

export const metadata: Metadata = {
  title: "Kullanım Koşulları — Sinyra Labs",
};

const LAST_UPDATED = "3 Mayıs 2026";

export default function KullanimPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 bg-white px-4 py-12">
        <div className="max-w-2xl mx-auto">
          <p className="text-slate-400 text-xs mb-2">Son güncelleme: {LAST_UPDATED}</p>
          <h1 className="text-slate-900 text-2xl font-bold mb-8">Kullanım Koşulları</h1>

          <Section title="Hizmet">
            Sinyra Labs, AI ürün lansmanlarını otomatik olarak takip edip özetleyen ve e-posta
            bülteni olarak sunan bir bireysel projedir. Herhangi bir ücret alınmamaktadır.
          </Section>

          <Section title="Abonelik">
            Listeye dahil olmak için başvuru formunu doldurmanız gerekmektedir. Abonelik tamamen
            isteğe bağlıdır ve her zaman ücretsiz olarak iptal edilebilir.
          </Section>

          <Section title="İçerik">
            Gönderilen brifingler otomatik araçlar ve yapay zeka yardımıyla üretilmektedir.
            Doğruluk garantisi verilmez; içerikler bilgilendirme amaçlıdır, yatırım veya
            iş kararlarına temel oluşturmak için kullanılamaz.
          </Section>

          <Section title="Sorumluluk sınırlaması">
            Sinyra Labs, içeriklerin kullanımından doğabilecek doğrudan veya dolaylı zararlardan
            sorumlu tutulamaz.
          </Section>

          <Section title="Değişiklikler">
            Bu koşullar önceden haber verilmeksizin güncellenebilir. Güncel koşullar her zaman bu
            sayfada yayınlanır.
          </Section>

          <Section title="İletişim">
            Sorularınız için:{" "}
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
