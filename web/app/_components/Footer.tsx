import Link from "next/link";
import { CONTACT_EMAIL } from "@/lib/constants";

export function Footer() {
  return (
    <footer className="bg-brand-navy border-t border-slate-800 px-4 py-8">
      <div className="max-w-3xl mx-auto text-center space-y-3">
        <p className="text-white font-bold tracking-widest text-xs uppercase">Sinyra Labs</p>
        <p className="text-slate-500 text-xs">
          Otomatik RSS + AI taraması · Günlük Türkçe brifing
        </p>
        <div className="flex items-center justify-center gap-4 text-xs">
          <Link href="/gizlilik" className="text-slate-400 hover:text-white transition-colors">
            Gizlilik
          </Link>
          <span className="text-slate-700">·</span>
          <Link href="/kullanim" className="text-slate-400 hover:text-white transition-colors">
            Kullanım Koşulları
          </Link>
          <span className="text-slate-700">·</span>
          <a
            href={`mailto:${CONTACT_EMAIL}`}
            className="text-slate-400 hover:text-white transition-colors"
          >
            İletişim
          </a>
        </div>
        <p className="text-slate-600 text-xs">© {new Date().getFullYear()} Sinyra Labs</p>
      </div>
    </footer>
  );
}
