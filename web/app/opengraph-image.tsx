import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "Sinyra Labs — Cut Through the Noise";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OGImage() {
  return new ImageResponse(
    (
      <div
        style={{
          background: "#0b1120",
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          justifyContent: "space-between",
          padding: "72px 80px",
          fontFamily: "system-ui, sans-serif",
        }}
      >
        {/* Top: logo + tagline */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <span
            style={{
              color: "#94a3b8",
              fontSize: 18,
              fontWeight: 700,
              letterSpacing: "0.2em",
              textTransform: "uppercase",
            }}
          >
            SINYRA LABS
          </span>
          <span
            style={{
              color: "#ffffff",
              fontSize: 72,
              fontWeight: 800,
              lineHeight: 1.1,
            }}
          >
            Cut Through
            <br />
            <span style={{ color: "#fbbf24" }}>the Noise</span>
          </span>
        </div>

        {/* Bottom: description + pill */}
        <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
          <span style={{ color: "#94a3b8", fontSize: 26, lineHeight: 1.5 }}>
            Günlük AI ürün lansmanı zekası — gürültüsüz, Türkçe.
          </span>
          <div style={{ display: "flex", gap: 12 }}>
            {["50+ Kaynak", "GPT Sınıflandırma", "Her gün 18:00"].map((t) => (
              <span
                key={t}
                style={{
                  background: "#1e293b",
                  color: "#cbd5e1",
                  fontSize: 18,
                  fontWeight: 600,
                  padding: "8px 20px",
                  borderRadius: 8,
                  border: "1px solid #334155",
                }}
              >
                {t}
              </span>
            ))}
          </div>
        </div>
      </div>
    ),
    { ...size },
  );
}
