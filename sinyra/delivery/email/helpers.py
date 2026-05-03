"""Template helpers ported from Apps Script (escape, impactColor, etc.)."""

import re

COMPANY_EMOJI: dict[str, str] = {
    "OpenAI": "🟢",
    "Google": "🔵",
    "Anthropic": "🟣",
    "Microsoft": "🟦",
    "Meta": "🔷",
    "xAI": "⚫",
    "Mistral": "🟠",
    "AWS": "🟧",
    "Apple": "⚪",
    "NVIDIA": "🟩",
    "Perplexity": "🔹",
}

_DAY_NAMES_TR = ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"]

_TYPE_MAP = {
    "new_feature": "Yeni özellik",
    "update": "Güncelleme",
    "announcement": "Duyuru",
    "research": "Araştırma",
    "none": "Diğer",
}


def escape(s: object) -> str:
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def impact_color(score: float) -> str:
    if score >= 90:
        return "#b91c1c"
    if score >= 75:
        return "#c2410c"
    if score >= 60:
        return "#a16207"
    return "#475569"


def impact_bg(score: float) -> str:
    if score >= 90:
        return "#fef2f2"
    if score >= 75:
        return "#fff7ed"
    if score >= 60:
        return "#fefce8"
    return "#f1f5f9"


def impact_label(score: float) -> str:
    if score >= 90:
        return "Kritik"
    if score >= 75:
        return "Yüksek"
    if score >= 60:
        return "Orta-Yüksek"
    if score >= 40:
        return "Orta"
    return "Düşük"


def translate_type(t: str) -> str:
    return _TYPE_MAP.get(t, t or "Diğer")


def get_day_name_tr(weekday: int) -> str:
    """weekday: Monday=0 … Sunday=6 (Python convention)."""
    py_to_js = [1, 2, 3, 4, 5, 6, 0]  # map Python weekday → JS getDay() index
    return _DAY_NAMES_TR[py_to_js[weekday]]


def company_emoji(company: str) -> str:
    return COMPANY_EMOJI.get(company, "🏢")


_TLD_RE = re.compile(
    r"^(?:www\.)?(.+?)\.(com|org|net|io|ai|de|fr|co|uk|eu|app|dev|news|tech)(/.*)?$",
    re.IGNORECASE,
)


def clean_source(name: str) -> str:
    """Convert domain-style source names (the-decoder.com) to readable form (The Decoder)."""
    m = _TLD_RE.match(name.strip())
    if not m:
        return name
    slug = m.group(1)
    slug = slug.replace("-", " ").replace("_", " ")
    return slug.strip().title()
