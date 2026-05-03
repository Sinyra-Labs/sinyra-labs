import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sinyra Labs — Günlük AI Brifing",
  description: "Her gün gelen kutunuza: rakiplerinizin ne yaptığını özetliyoruz. Gürültüsüz, Türkçe.",
  openGraph: {
    title: "Sinyra Labs — Cut Through the Noise",
    description: "Günlük AI ürün lansmanı zekası. Otomatik tarama, AI sınıflandırma, Türkçe özet.",
    siteName: "Sinyra Labs",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr">
      <body>{children}</body>
    </html>
  );
}
