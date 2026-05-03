import { SITE_URL, SITE_NAME, SITE_DESCRIPTION, CONTACT_EMAIL, GITHUB_URL, FORMS_URL } from "@/lib/constants";

const org = {
  "@type": "Organization",
  "@id": `${SITE_URL}/#organization`,
  name: SITE_NAME,
  url: SITE_URL,
  description: SITE_DESCRIPTION,
  email: CONTACT_EMAIL,
  sameAs: [GITHUB_URL],
  founder: { "@type": "Person", name: "Bilal Abiç", email: CONTACT_EMAIL },
};

const website = {
  "@type": "WebSite",
  "@id": `${SITE_URL}/#website`,
  url: SITE_URL,
  name: SITE_NAME,
  description: SITE_DESCRIPTION,
  publisher: { "@id": `${SITE_URL}/#organization` },
  inLanguage: "tr-TR",
};

const service = {
  "@type": "Service",
  "@id": `${SITE_URL}/#service`,
  name: "Sinyra Labs Günlük AI Brifing",
  description:
    "AI ürün lansmanlarını izleyen ve her sabah Türkçe özetleyen ücretsiz e-posta bülten servisi.",
  provider: { "@id": `${SITE_URL}/#organization` },
  serviceType: "Email Newsletter",
  audience: {
    "@type": "Audience",
    audienceType: "Yazılım geliştiriciler, ürün yöneticileri, AI araştırmacıları",
    geographicArea: { "@type": "Country", name: "Turkey" },
  },
  offers: {
    "@type": "Offer",
    price: "0",
    priceCurrency: "TRY",
    url: FORMS_URL,
    eligibleRegion: { "@type": "Country", name: "Turkey" },
  },
  availableLanguage: { "@type": "Language", name: "Turkish", alternateName: "tr" },
};

export const FAQ_ITEMS = [
  {
    q: "Sinyra Labs nedir?",
    a: "Sinyra Labs, OpenAI, Google, Anthropic gibi AI şirketlerinin ürün lansmanlarını her gün otomatik olarak izleyen ve Türkçe özetleyen ücretsiz bir e-posta bülten servisidir.",
  },
  {
    q: "Sinyra Labs ücretli mi?",
    a: "Tamamen ücretsizdir. Kredi kartı veya ödeme bilgisi gerekmez.",
  },
  {
    q: "Brifing ne zaman gönderilir?",
    a: "Her gün Türkiye saatiyle 18:00'de (UTC 15:00) e-posta olarak gönderilir.",
  },
  {
    q: "Hangi AI kaynaklarını izliyor?",
    a: "OpenAI, Google DeepMind, Anthropic, Meta AI, xAI, Mistral, Hugging Face, GitHub Copilot, AWS AI, Microsoft Azure AI dahil 50'den fazla kaynak her gün taranır.",
  },
  {
    q: "Nasıl abone olabilirim?",
    a: "Başvuru formunu doldurmanız yeterli. Ücretsizdir ve bir sonraki brifingden itibaren listedesiniz.",
  },
  {
    q: "Aboneliği nasıl iptal edebilirim?",
    a: "bilalabic78@gmail.com adresine e-posta göndererek istediğiniz zaman ücretsiz iptal edebilirsiniz.",
  },
];

const faqPage = {
  "@type": "FAQPage",
  "@id": `${SITE_URL}/#faq`,
  mainEntity: FAQ_ITEMS.map(({ q, a }) => ({
    "@type": "Question",
    name: q,
    acceptedAnswer: { "@type": "Answer", text: a },
  })),
};

export function GlobalJsonLd() {
  const graph = {
    "@context": "https://schema.org",
    "@graph": [org, website, service],
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(graph) }}
    />
  );
}

export function HomeJsonLd() {
  const graph = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebPage",
        "@id": `${SITE_URL}/#webpage`,
        url: SITE_URL,
        name: "Sinyra Labs — Günlük AI Ürün Brifing",
        isPartOf: { "@id": `${SITE_URL}/#website` },
        about: { "@id": `${SITE_URL}/#service` },
        inLanguage: "tr-TR",
      },
      faqPage,
    ],
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(graph) }}
    />
  );
}

export function PageJsonLd({
  path,
  name,
  description,
}: {
  path: string;
  name: string;
  description: string;
}) {
  const url = `${SITE_URL}${path}`;
  const data = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "@id": `${url}#webpage`,
    url,
    name,
    description,
    isPartOf: { "@id": `${SITE_URL}/#website` },
    inLanguage: "tr-TR",
    breadcrumb: {
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "Ana Sayfa", item: SITE_URL },
        { "@type": "ListItem", position: 2, name, item: url },
      ],
    },
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
