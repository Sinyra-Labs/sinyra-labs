import Link from "next/link";
import { CONTACT_EMAIL, GITHUB_URL, SITE_NAME } from "@/lib/constants";

export function Footer() {
  return (
    <footer className="bg-brand-navy border-t border-slate-800 px-4 py-10" role="contentinfo">
      <div className="max-w-3xl mx-auto">
        {/* Brand */}
        <div className="text-center mb-6">
          <p className="text-white font-bold tracking-widest text-xs uppercase mb-1">{SITE_NAME}</p>
          <p className="text-slate-500 text-xs">Otomatik RSS + AI taraması · Günlük Türkçe brifing</p>
        </div>

        {/* Links */}
        <nav aria-label="Footer navigasyon" className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-xs mb-6">
          <Link href="/hakkinda" className="text-slate-400 hover:text-white transition-colors">Hakkında</Link>
          <span className="text-slate-700" aria-hidden>·</span>
          <Link href="/gizlilik" className="text-slate-400 hover:text-white transition-colors">Gizlilik</Link>
          <span className="text-slate-700" aria-hidden>·</span>
          <Link href="/kullanim" className="text-slate-400 hover:text-white transition-colors">Kullanım Koşulları</Link>
          <span className="text-slate-700" aria-hidden>·</span>
          <a href={`mailto:${CONTACT_EMAIL}`} className="text-slate-400 hover:text-white transition-colors">İletişim</a>
          <span className="text-slate-700" aria-hidden>·</span>
          <a href={GITHUB_URL} target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-white transition-colors">GitHub</a>
        </nav>

        <p className="text-slate-600 text-xs text-center">
          © {new Date().getFullYear()} {SITE_NAME} · Tüm hakları saklıdır.
        </p>
      </div>
    </footer>
  );
}
