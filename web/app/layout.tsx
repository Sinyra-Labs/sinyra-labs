import type { Metadata } from "next";
import "./globals.css";
import { GlobalJsonLd } from "./_components/JsonLd";
import { SITE_URL, SITE_NAME, SITE_DESCRIPTION, CONTACT_EMAIL } from "@/lib/constants";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),

  title: {
    default: `${SITE_NAME} — Günlük AI Ürün Brifing`,
    template: `%s | ${SITE_NAME}`,
  },
  description: SITE_DESCRIPTION,

  keywords: [
    "AI brifing",
    "yapay zeka haberleri",
    "AI ürün lansmanları",
    "günlük AI bülteni",
    "Türkçe AI haberleri",
    "OpenAI haberleri",
    "Google Gemini",
    "Anthropic Claude",
    "yapay zeka takip",
    "AI newsletter Türkçe",
    "sinyra",
    "sinyra labs",
  ],

  authors: [{ name: "Bilal Abiç", url: SITE_URL }],
  creator: SITE_NAME,
  publisher: SITE_NAME,

  openGraph: {
    type: "website",
    locale: "tr_TR",
    alternateLocale: "en_US",
    url: SITE_URL,
    siteName: SITE_NAME,
    title: `${SITE_NAME} — Cut Through the Noise`,
    description: SITE_DESCRIPTION,
    images: [
      {
        url: "/opengraph-image",
        width: 1200,
        height: 630,
        alt: "Sinyra Labs — Cut Through the Noise",
      },
    ],
  },

  twitter: {
    card: "summary_large_image",
    title: `${SITE_NAME} — Cut Through the Noise`,
    description: SITE_DESCRIPTION,
    images: ["/opengraph-image"],
    creator: "@sinyralabs",
  },

  alternates: {
    canonical: SITE_URL,
    languages: { "tr-TR": SITE_URL, "x-default": SITE_URL },
  },

  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },

  verification: {
    // google: "ADD_AFTER_SEARCH_CONSOLE_SETUP",
  },

  category: "technology",

  other: {
    "contact:email": CONTACT_EMAIL,
    "language": "Turkish",
    "revisit-after": "1 day",
    "rating": "general",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr" dir="ltr">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <GlobalJsonLd />
      </head>
      <body>{children}</body>
    </html>
  );
}
