import Link from "next/link";
import { FORMS_URL } from "@/lib/constants";

export function Navbar() {
  return (
    <nav className="bg-brand-navy px-4 py-3 flex items-center justify-between" role="navigation" aria-label="Ana navigasyon">
      <Link href="/" className="text-white font-bold tracking-widest text-sm uppercase" aria-label="Sinyra Labs ana sayfa">
        Sinyra Labs
      </Link>
      <div className="flex items-center gap-4">
        <Link href="/hakkinda" className="text-slate-400 hover:text-white text-sm transition-colors hidden sm:block">
          Hakkında
        </Link>
        <a
          href={FORMS_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="bg-brand-yellow text-brand-navy text-xs font-bold px-4 py-2 rounded-lg
                     hover:bg-amber-300 transition-colors"
        >
          Abone Ol →
        </a>
      </div>
    </nav>
  );
}
