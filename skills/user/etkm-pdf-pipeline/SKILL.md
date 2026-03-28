---
name: etkm-pdf-pipeline
version: 1.0
locked: 2026-03-25
description: >
  The locked production pipeline for ALL ETKM branded PDFs. Load this skill
  whenever building, rebuilding, or exporting any ETKM PDF deliverable —
  tier result PDFs, lead magnets, bonus guides, event materials, onboarding
  docs, or any other branded document. This skill defines the only approved
  toolchain. Never use ReportLab or WeasyPrint for branded PDFs — they cannot
  match the HTML output and produce font/layout failures. Trigger phrases:
  "build a PDF", "export to PDF", "generate the PDF", "make the PDF match the
  HTML", "PDF looks wrong", "font is wrong in PDF", "rebuild the PDF",
  "create a lead magnet PDF", "tier result PDF", "assessment PDF".
---

# ETKM PDF Production Pipeline

**Version:** 1.0
**Locked:** 2026-03-25
**Status:** Production — do not deviate without Nathan's explicit authorization

---

## Dependencies

| Skill | Why |
|-------|-----|
| `etkm-brand-kit` | Visual standard — colors, fonts, palette (already referenced) |
| `etkm-webpage-build` | PDF design system uses the same HTML patterns as web pages — same fonts, same color rules, same section patterns adapted for fixed-page layout |

---

## The One Rule

Every ETKM branded PDF is produced from a single pipeline:

```
HTML (embedded fonts) → Playwright/Chromium → PDF
```

This is the only pipeline that produces output matching the HTML design
exactly. All other methods have been tested and rejected.

| Tool | Status | Reason Rejected |
|------|--------|-----------------|
| ReportLab | ❌ NEVER USE | Font ceiling at Helvetica-Bold — cannot render Montserrat 900 Black |
| WeasyPrint | ❌ NEVER USE | Fetches Google Fonts over network — fails headless, outputs wrong font |
| Playwright/Chromium | ✅ LOCKED | Renders identical to browser — correct font, layout, margins |

---

## Typography (Non-Negotiable)

| Role | Font | Weight |
|------|------|--------|
| Cover headlines | Montserrat | 900 Black |
| Section headlines (H1) | Montserrat | 900 Black |
| Subheadings (H2) | Montserrat | 800 ExtraBold |
| Item titles (H3) | Montserrat | 700 Bold |
| Labels / kickers | Montserrat | 700 Bold, uppercase, letter-spacing |
| Body paragraphs | Inter | 400 Regular |
| Supporting body | Inter | 500 Medium |
| Captions / small data | Inter | 500 Medium, uppercase, letter-spacing |

---

## Font Embedding (Required for Every Build)

Google Fonts CDN is blocked in headless Playwright. Fonts MUST be
base64-encoded directly into the HTML `@font-face` declarations.

**Font sources (jsDelivr fontsource CDN):**

```
Montserrat weights 400–900:
https://cdn.jsdelivr.net/npm/@fontsource/montserrat@5.0.0/files/montserrat-latin-{weight}-normal.woff2

Inter weights 400, 500, 600:
https://fonts.gstatic.com/s/inter/v18/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfAZ9hiJ-Ek-_EeA.woff2  (400)
https://fonts.gstatic.com/s/inter/v18/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuI6fAZ9hiJ-Ek-_EeA.woff2  (500)
https://fonts.gstatic.com/s/inter/v18/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuGKYAZ9hiJ-Ek-_EeA.woff2  (600)
```

**Embedding script:**

```python
import base64, requests

weights = {'400':'Regular','500':'Medium','600':'SemiBold',
           '700':'Bold','800':'ExtraBold','900':'Black'}
base_url = 'https://cdn.jsdelivr.net/npm/@fontsource/montserrat@5.0.0/files/'

face_css = ''
for w, name in weights.items():
    url = f'{base_url}montserrat-latin-{w}-normal.woff2'
    data = base64.b64encode(requests.get(url).content).decode()
    face_css += f'@font-face {{ font-family: "Montserrat"; font-weight: {w}; src: url("data:font/woff2;base64,{data}") format("woff2"); }}\n'

# Repeat for Inter weights 400/500/600
# Replace @import Google Fonts line in HTML with face_css
```

**Verification — always confirm before export:**

```python
assert '@import url' not in html  # No external font calls
assert html.count('@font-face') >= 9  # All 9 faces embedded
```

---

## Playwright Conversion (Exact Command)

```python
from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f'file://{os.path.abspath("your_file.html")}')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)  # Font render buffer
    page.pdf(
        path='output.pdf',
        format='Letter',
        print_background=True,
        margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
    )
    browser.close()
```

**Critical parameters:**
- `format='Letter'` — 8.5×11in, always
- `print_background=True` — required for black backgrounds, colored blocks
- `margin` all zeros — page geometry is controlled entirely in CSS `@page`
- `wait_for_timeout(2000)` — required; skipping causes font render failures

---

## CSS Page Setup (Required in Every HTML Template)

```css
@page {
  size: 8.5in 11in;
  margin: 0;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

.page {
  width: 8.5in;
  height: 11in;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  page-break-after: always;
}
```

---

## Section Library

The master template lives at:
`ETKM_PDF_Design_System_embedded.html`

64 section types across 10 categories — all fonts embedded, all brand
standards applied. Every new PDF is built by:

1. Copying the embedded HTML template
2. Selecting the required sections
3. Replacing content
4. Running the Playwright export above

**Section categories:**
- Cover & Identity (§01–04)
- Opening & Framing (§05–10)
- Concepts & Frameworks (§11–19)
- Content & Instruction (§21–30)
- Evidence & Authority (§31–34)
- Voice & Narrative (§36–41)
- Social Proof & Trust (§42–45)
- Structural Elements (§48–53)
- Closing & CTA (§57–64)
- Image Placements (§IMG-01–05)

---

## Brand Standards (PDF-Specific)

| Element | Standard |
|---------|----------|
| Cover style | Dark (black background) — default |
| Cover alt | Light (white background) — bonus guides only |
| Interior pages | White background, black header bar, 3pt red rule |
| Logo | White/Red version on dark pages. Black/Red on light pages. Cover only — never on interior pages |
| Header | Black bar 32pt, Montserrat 700, white text, page number right |
| Footer | 0.5pt #BBBBBB rule, etxkravmaga.com left, doc title right, 7pt Inter |
| Red | One element per section maximum — never decorative |
| Margins | 52pt left/right, 36pt top body, footer anchored to bottom |

---

## QC Before Every Delivery

Run the etkm-deliverable-qc skill Gates 1–8 on every PDF before it ships.
Minimum visual checks specific to PDFs built with this pipeline:

- [ ] Open in PDF viewer — fonts render as Montserrat Black (thick, rounded strokes), not system sans-serif (thin, sharp strokes)
- [ ] Cover headline weight matches the HTML preview
- [ ] No content clipping off right edge of any page
- [ ] No kicker/headline overlaps on any interior page
- [ ] Header bar + red rule present on all interior pages
- [ ] Logo appears on cover only — not on interior pages
- [ ] Footer present on all pages including dark pages

---

## QC Gates

### Gate 1 — Font Rendering
- [ ] Montserrat is loading from base64 `@font-face` — not from Google CDN (CDN unreliable in Playwright)
- [ ] Inter is loading from base64 `@font-face`
- [ ] Headlines render in Montserrat 900 — not system fallback
- [ ] Body text renders in Inter — not system fallback
- [ ] Verify by screenshot: open the generated PDF and inspect font rendering

### Gate 2 — Brand Compliance
- [ ] Background is white (`#fff`) or black (`#000`) — correct for document type
- [ ] Accent is `#CC0000` only
- [ ] No emojis in the document
- [ ] No prohibited words
- [ ] Layout matches the HTML source — no float or grid collapse artifacts

---

## Known Failure Patterns

| Failure | Cause | Fix |
|---------|-------|-----|
| Wrong font in PDF (thin/system sans) | Google Fonts not fetched headless | Embed fonts as base64 — never use CDN import |
| Correct font in browser, wrong in PDF | WeasyPrint used instead of Playwright | Switch to Playwright pipeline |
| Black backgrounds missing | `print_background=True` omitted | Always include this parameter |
| Page content cut off | Missing `overflow: hidden` on `.page` | Add overflow hidden to page shell |
| Font renders but slightly wrong weight | `wait_for_timeout` too short or omitted | Use 2000ms minimum |
| Content bleeds between pages | Missing `page-break-after: always` | Add to every `.page` div |
