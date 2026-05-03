import type { MetadataRoute } from "next";
import { SITE_URL, SITE_NAME, SITE_DESCRIPTION } from "@/lib/constants";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: SITE_NAME,
    short_name: "Sinyra",
    description: SITE_DESCRIPTION,
    start_url: "/",
    display: "standalone",
    background_color: "#0b1120",
    theme_color: "#0b1120",
    lang: "tr",
    dir: "ltr",
    scope: SITE_URL,
    icons: [
      { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
  };
}
