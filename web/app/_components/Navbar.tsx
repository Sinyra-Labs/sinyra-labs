import Link from "next/link";
import { FORMS_URL } from "@/lib/constants";

export function Navbar() {
  return (
    <nav className="bg-brand-navy px-4 py-3 flex items-center justify-between">
      <Link href="/" className="text-white font-bold tracking-widest text-sm uppercase">
        Sinyra Labs
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
    </nav>
  );
}
