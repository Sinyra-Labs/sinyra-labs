Bağlam: Mevcut bir Google Apps Script projem var, AI haberleri RSS'lerden toplayıp
GPT-4o-mini ile sınıflandırıp etki skoru veriyor ve günlük HTML email gönderiyor.
Bu projeyi Python'a taşıyacağım. Scheduler GitHub Actions olacak. Storage başta
SQLite, ileride Supabase. Email Resend.

Mevcut kod elimde (tek dosya, 600 satır .gs).

GÖREV: Repo iskeletini oluştur. Bu doküman dışında dosya YAZMA, sadece şu çıktıyı ver:
1. /sinyra/, /tests/, /.github/workflows/, /.agent/ ağacı (klasörler ve dosya isimleri)
2. pyproject.toml içeriği (uv, ruff, mypy, pytest dahil)
3. requirements.txt (production)
4. .env.example
5. README.md taslağı (sadece bölüm başlıkları)

KISIT:
- Python 3.12+
- pydantic v2
- mypy --strict ile geçecek seviyede type hint
- Henüz kod yazma; sadece iskelet ve TODO comment'lar

Plan: önce tree, sonra her dosya tek tek. Bittiğinde "ready for next prompt" yaz.