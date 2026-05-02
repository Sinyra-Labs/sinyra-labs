---
name: brief-renderer
description: |
  Render a DailyBrief to HTML and plain-text using Jinja2 templates, produce a
  browser-preview file, and verify visual parity with the original Apps Script design.
  Use when modifying email templates or debugging rendering issues.
---

# Brief Renderer

## When to use
- User says "email tasarımı değiştir", "template güncelle", "preview göster".
- After modifying `sinyra/delivery/email/templates/brief.html` or `brief.txt`.

## How to run (browser preview)
```bash
python -c "
from sinyra.delivery.email.render import render_preview
render_preview('docs/preview.html')
"
# Then open docs/preview.html in browser
```

## Visual parity checklist
- [ ] max-width 640px, centered
- [ ] Hero: background #0b1120, text white, accent #fbbf24
- [ ] Stats strip below hero
- [ ] Spotlight card for top feature
- [ ] Company-grouped feature list
- [ ] Trends card
- [ ] Insight card
- [ ] Share / feedback card
- [ ] Footer with unsubscribe link
- [ ] No flexbox (Gmail compat), inline CSS only

## Failure modes
- Gmail renders as plain text → check `MIMEMultipart("alternative")` order (text first, html second)
- Images broken in email clients → use absolute URLs or avoid images
